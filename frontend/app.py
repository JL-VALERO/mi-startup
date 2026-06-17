"""Rendir.ai — frontend Streamlit.

Día 1: sube una foto de apuntes y extrae el texto con PaddleOCR (backend /ocr).
Día 2: el botón "Generar simulacro" llamará a /generate (Claude API).
"""
import os

import requests
import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Rendir.ai", page_icon="📝", layout="centered")

st.title("📝 Rendir.ai")
st.subheader("Convierte una foto de tus apuntes en un simulacro al estilo de tu profesor")

with st.form("entrada"):
    col1, col2 = st.columns(2)
    curso = col1.text_input("Curso", placeholder="Ej. Microeconomía II")
    profesor = col2.text_input("Profesor", placeholder="Ej. A. Quispe")
    apuntes = st.file_uploader(
        "Sube una foto de tus apuntes (PNG o JPG)", type=["png", "jpg", "jpeg"]
    )
    extraer = st.form_submit_button("📷 Extraer texto de mis apuntes (OCR)")

if extraer:
    if apuntes is None:
        st.warning("Primero sube una imagen de tus apuntes.")
    else:
        with st.spinner("Leyendo tus apuntes con PaddleOCR..."):
            try:
                files = {"file": (apuntes.name, apuntes.getvalue(), apuntes.type)}
                resp = requests.post(f"{BACKEND_URL}/ocr", files=files, timeout=180)
                resp.raise_for_status()
                data = resp.json()
                st.session_state["ocr_text"] = data["text"]
                st.success(
                    f"✅ Texto extraído: {data['num_lines']} líneas · "
                    f"confianza media {data['avg_confidence']:.0%}"
                )
            except requests.exceptions.ConnectionError:
                st.error(
                    f"No pude conectar con el backend en {BACKEND_URL}. "
                    "¿Está corriendo `uvicorn app.main:app`?"
                )
            except Exception as exc:  # noqa: BLE001
                st.error(f"Error al procesar la imagen: {exc}")

if "ocr_text" in st.session_state:
    st.text_area(
        "Texto detectado (puedes editarlo antes de generar el simulacro)",
        key="ocr_text",
        height=300,
    )
    st.button(
        "🧠 Generar simulacro al estilo del profe (Día 2)",
        disabled=True,
        help="Disponible en el Día 2: conexión a Claude API (/generate).",
    )
