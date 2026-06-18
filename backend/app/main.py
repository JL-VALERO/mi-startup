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

app = FastAPI(title="Rendir.ai API", version="0.2.0")

# Permite que el frontend (Streamlit) llame al backend desde otro dominio.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}


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
async def ocr(file: UploadFile = File(...)):
    """Material IMPRESO/PDF: extrae texto con PaddleOCR (gratis, sin tokens)."""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Tipo no soportado: {file.content_type}. Usa PNG o JPG.",
        )
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")
    try:
        return extract_text(data)
    except ModuleNotFoundError as exc:
        # En el deploy "solo-Claude" no se instala PaddleOCR a propósito.
        raise HTTPException(
            status_code=503,
            detail=(
                "OCR de impresos (PaddleOCR) no disponible en este despliegue. "
                "Usa el modo Manuscrito / pizarra (Claude visión)."
            ),
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error en OCR: {exc}") from exc


@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Manuscrito/PIZARRA: lee la imagen con Claude visión (mejor que OCR clásico)."""
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Tipo no soportado: {file.content_type}. Usa PNG o JPG.",
        )
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")
    # Import diferido: claude_client importa el SDK anthropic solo al usarse.
    from .claude_client import transcribe_image

    try:
        return transcribe_image(data, media_type=file.content_type)
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
