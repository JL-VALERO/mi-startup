"""Tests de contrato de /transcribe y /generate (sin llamar a la API de Claude).

Validan la validación de entrada — no requieren ANTHROPIC_API_KEY ni red, así que
el CI sigue verde. La generación real se prueba manualmente (ver README).
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_transcribe_rechaza_tipo_no_imagen():
    resp = client.post(
        "/transcribe", files={"files": ("notas.txt", b"hola", "text/plain")}
    )
    assert resp.status_code == 415


def test_generate_requiere_cuerpo():
    resp = client.post("/generate", json={})
    assert resp.status_code == 422  # falta `content`


def test_generate_rechaza_contenido_vacio():
    resp = client.post("/generate", json={"content": "   "})
    assert resp.status_code == 400


def test_generate_pdf_requiere_contenido():
    # Valida la entrada antes de llamar a Claude o compilar LaTeX.
    resp = client.post("/generate_pdf", json={"content": "   "})
    assert resp.status_code == 400
