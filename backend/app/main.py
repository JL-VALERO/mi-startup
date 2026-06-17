"""Rendir.ai — backend FastAPI.

Endpoints:
  GET  /health    -> verificación de vida
  POST /ocr       -> recibe imagen de apuntes, devuelve texto (PaddleOCR)   [Día 1]
  POST /generate  -> recibe texto + estilo del profe, devuelve simulacro    [Día 2]
"""
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .ocr import extract_text

app = FastAPI(title="Rendir.ai API", version="0.1.0")

# Permite que el frontend (Streamlit) llame al backend desde otro dominio.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "rendir.ai", "version": "0.1.0"}


@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    """Extrae el texto de una foto de apuntes con PaddleOCR."""
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
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error en OCR: {exc}") from exc


# TODO (Día 2): POST /generate -> Claude API genera simulacro al estilo del profesor
