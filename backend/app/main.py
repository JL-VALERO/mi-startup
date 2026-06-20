"""Rendir.ai — backend FastAPI.

Endpoints:
  GET  /health     -> verificación de vida
  POST /ocr        -> material IMPRESO/PDF: texto con PaddleOCR (Lectura 14)
  POST /transcribe -> manuscrito/PIZARRA: texto con Claude visión (Lectura 14)
  POST /generate   -> simulacro de preguntas al estilo del profesor (Claude)
"""
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .ocr import extract_text

app = FastAPI(title="Rendir.ai API", version="0.3.0")

# Permite que el frontend (Streamlit) llame al backend desde otro dominio.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}
PDF_TYPE = "application/pdf"


def _is_pdf(file: UploadFile) -> bool:
    return file.content_type == PDF_TYPE or (file.filename or "").lower().endswith(".pdf")


_OCR_UNAVAILABLE = (
    "OCR de impresos (PaddleOCR) no disponible en este despliegue. "
    "Usa el modo Manuscrito / pizarra (Claude visión)."
)


class GenerateRequest(BaseModel):
    content: str
    curso: str = ""
    profesor: str = ""
    past_exam_text: str | None = None
    n: int = 5


@app.get("/health")
def health():
    return {"status": "ok", "service": "rendir.ai", "version": "0.2.0"}


@app.post("/ocr")
async def ocr(files: list[UploadFile] = File(...)):
    """Material IMPRESO/PDF: extrae texto con PaddleOCR (gratis, sin tokens).

    Acepta varias imágenes y/o PDFs. El PDF digital se lee como texto directo
    (sin OCR); el PDF escaneado se renderiza a imagen y pasa por PaddleOCR.
    """
    from .pdf import pdf_extract, pdf_render_images

    textos: list[str] = []
    try:
        for file in files:
            data = await file.read()
            if not data:
                continue
            if _is_pdf(file):
                info = pdf_extract(data)
                if not info["is_scanned"] and info["text"]:
                    textos.append(info["text"])  # PDF digital: texto directo, sin OCR
                else:
                    for img in pdf_render_images(data):
                        textos.append(extract_text(img)["text"])
            elif file.content_type in ALLOWED_IMAGE_TYPES:
                textos.append(extract_text(data)["text"])
            else:
                raise HTTPException(
                    status_code=415,
                    detail=f"Tipo no soportado: {file.content_type}. Usa PNG, JPG o PDF.",
                )
    except ModuleNotFoundError as exc:
        # En el deploy "solo-Claude" no se instala PaddleOCR a propósito.
        raise HTTPException(status_code=503, detail=_OCR_UNAVAILABLE) from exc
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error en OCR: {exc}") from exc

    return {"text": "\n\n".join(t for t in textos if t)}


@app.post("/transcribe")
async def transcribe(files: list[UploadFile] = File(...)):
    """Manuscrito/PIZARRA: lee imágenes con Claude visión (mejor que OCR clásico).

    Acepta varias imágenes y/o PDFs en una sola pasada. El PDF digital aporta su
    texto sin gastar tokens; las imágenes (y PDFs escaneados) van a Claude visión.
    """
    from .claude_client import transcribe_images
    from .pdf import pdf_extract, pdf_render_images

    images: list[tuple[bytes, str]] = []
    extra_text: list[str] = []
    for file in files:
        data = await file.read()
        if not data:
            continue
        if _is_pdf(file):
            info = pdf_extract(data)
            if not info["is_scanned"] and info["text"]:
                extra_text.append(info["text"])
            else:
                images.extend((img, "image/png") for img in pdf_render_images(data))
        elif file.content_type in ALLOWED_IMAGE_TYPES:
            images.append((data, file.content_type))
        else:
            raise HTTPException(
                status_code=415,
                detail=f"Tipo no soportado: {file.content_type}. Usa PNG, JPG o PDF.",
            )

    joined_text = "\n\n".join(extra_text)
    if not images and not joined_text:
        raise HTTPException(status_code=400, detail="No se recibió contenido legible.")
    # PDF digital sin imágenes: ya tenemos el texto, no hace falta llamar a Claude.
    if not images:
        return {"text": joined_text, "topics": []}

    try:
        return transcribe_images(images, extra_text=joined_text)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error al transcribir: {exc}") from exc


@app.post("/generate")
async def generate(req: GenerateRequest):
    """Genera un simulacro de preguntas de desarrollo al estilo del profesor."""
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Falta el texto de los apuntes.")
    from .claude_client import generate_simulacro

    try:
        return generate_simulacro(
            content=req.content,
            curso=req.curso,
            profesor=req.profesor,
            past_exam_text=req.past_exam_text,
            n=req.n,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error al generar: {exc}") from exc
