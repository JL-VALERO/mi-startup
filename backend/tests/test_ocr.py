"""Tests del endpoint /ocr que NO requieren cargar PaddleOCR.

Validan el contrato del endpoint (validación de entrada) sin descargar el modelo
pesado, para mantener el CI rápido. El OCR real se prueba manualmente con una
imagen de apuntes (ver README, sección "Verificación").
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ocr_rechaza_tipo_no_imagen():
    resp = client.post(
        "/ocr", files={"file": ("notas.txt", b"hola", "text/plain")}
    )
    assert resp.status_code == 415


def test_ocr_requiere_archivo():
    resp = client.post("/ocr")
    assert resp.status_code == 422  # falta el campo `file`
