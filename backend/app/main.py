"""Rendir.ai — backend FastAPI (esqueleto, Día 0).

Endpoints planificados:
  GET  /health    -> verificación de vida
  POST /ocr       -> recibe imagen de apuntes, devuelve texto (PaddleOCR)   [Día 1]
  POST /generate  -> recibe texto + estilo del profe, devuelve simulacro    [Día 2]
"""
from fastapi import FastAPI

app = FastAPI(title="Rendir.ai API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "service": "rendir.ai", "version": "0.1.0"}


# TODO (Día 1): POST /ocr  -> PaddleOCR sobre la imagen de apuntes
# TODO (Día 2): POST /generate -> Claude API genera simulacro al estilo del profesor
