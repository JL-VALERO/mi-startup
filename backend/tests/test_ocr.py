"""Tests del endpoint /ocr que NO requieren cargar PaddleOCR.

Validan el contrato del endpoint (validación de entrada y la ruta de PDF digital,
que no usa OCR) sin descargar el modelo pesado, para mantener el CI rápido. El OCR
real de imágenes se prueba manualmente (ver README, sección "Verificación").
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ocr_rechaza_tipo_no_imagen():
    resp = client.post(
        "/ocr", files={"files": ("notas.txt", b"hola", "text/plain")}
    )
    assert resp.status_code == 415


def test_ocr_requiere_archivo():
    resp = client.post("/ocr")
    assert resp.status_code == 422  # falta el campo `files`


def test_ocr_pdf_digital_extrae_texto_sin_paddle():
    """Un PDF con texto se lee directo (PyMuPDF), sin tocar PaddleOCR."""
    fitz = pytest.importorskip("fitz")  # se salta en CI (no instala pymupdf)
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hola desde un PDF digital de prueba")
    pdf_bytes = doc.tobytes()
    doc.close()

    resp = client.post(
        "/ocr", files={"files": ("apuntes.pdf", pdf_bytes, "application/pdf")}
    )
    assert resp.status_code == 200
    assert "PDF digital de prueba" in resp.json()["text"]
