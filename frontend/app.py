"""Rendir.ai — frontend Streamlit.

Flujo: sube apuntes -> lee (Claude visión para manuscrito/pizarra, PaddleOCR para
impreso) -> edita el texto -> genera un simulacro de preguntas al estilo del profe.
"""
import os

import requests
import streamlit as st

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

def _resolve_backend_url() -> str:
    """Prioridad: secret de Streamlit Cloud -> variable de entorno -> localhost.

    Streamlit Community Cloud entrega los secrets vía `st.secrets`, no siempre
    como variable de entorno; por eso se lee primero de ahí.
    """
    try:
        if "BACKEND_URL" in st.secrets:
            return st.secrets["BACKEND_URL"]
    except Exception:  # noqa: BLE001 -- st.secrets lanza si no hay secrets configurados
        pass
    # Default = URL pública del backend en Render, para que el demo desplegado
    # funcione AUNQUE no se configure el secret/env. Para apuntar a un backend
    # local, define BACKEND_URL=http://localhost:8000 (secret de Streamlit o env).
    return os.getenv("BACKEND_URL", "https://rendir-ai-backend.onrender.com")


BACKEND_URL = _resolve_backend_url()

st.set_page_config(
    page_title="Rendir.ai — simulacros al estilo de tu profe",
    page_icon="📝",
    layout="centered",
    menu_items={
        "about": "Rendir.ai — convierte una foto de tus apuntes en un simulacro "
        "de examen con el estilo de preguntas de tu propio profesor."
    },
)

# Vista más limpia para el demo: oculta el menú/footer por defecto de Streamlit.
st.markdown(
    "<style>#MainMenu{visibility:hidden} footer{visibility:hidden}</style>",
    unsafe_allow_html=True,
)

# --- Cabecera con identidad de marca ---
st.title("📝 Rendir.ai")
st.markdown("##### Convierte una foto de tus apuntes en un simulacro al estilo de tu profesor")
st.caption(
    "Sube tus apuntes → los leemos (Claude visión para manuscrito/pizarra · PaddleOCR para "
    "impreso) → generamos preguntas de desarrollo al estilo de **ESE** profesor."
)
st.divider()

st.markdown("##### 📷 Paso 1 — Sube tus apuntes y léelos")
with st.form("entrada"):
    col1, col2 = st.columns(2)
    curso = col1.text_input("Curso", placeholder="Ej. Microeconomía II")
    profesor = col2.text_input("Profesor", placeholder="Ej. A. Quispe")

    tipo = st.radio(
        "Tipo de material",
        ["Manuscrito / pizarra (Claude visión)", "Impreso / PDF (PaddleOCR)"],
        help="El manuscrito y la pizarra los lee Claude visión; lo impreso, PaddleOCR.",
    )
    apuntes = st.file_uploader(
        "Sube una foto de tus apuntes (PNG o JPG)", type=["png", "jpg", "jpeg"]
    )
    leer = st.form_submit_button("📷 Leer mis apuntes")

if leer:
    if apuntes is None:
        st.warning("Primero sube una imagen de tus apuntes.")
    else:
        endpoint = "/transcribe" if tipo.startswith("Manuscrito") else "/ocr"
        with st.spinner(f"Leyendo tus apuntes ({'Claude visión' if endpoint == '/transcribe' else 'PaddleOCR'})..."):
            try:
                files = {"file": (apuntes.name, apuntes.getvalue(), apuntes.type)}
                resp = requests.post(f"{BACKEND_URL}{endpoint}", files=files, timeout=180)
                resp.raise_for_status()
                data = resp.json()
                st.session_state["ocr_text"] = data["text"]
                if data.get("topics"):
                    st.caption("Temas detectados: " + ", ".join(data["topics"]))
                st.success("✅ Texto leído. Revísalo abajo y genera tu simulacro.")
            except requests.exceptions.ConnectionError:
                st.error(
                    f"No pude conectar con el backend en {BACKEND_URL}. "
                    "¿Está corriendo `uvicorn app.main:app`?"
                )
            except Exception as exc:  # noqa: BLE001
                st.error(f"Error al leer la imagen: {exc}")

if "ocr_text" in st.session_state:
    st.divider()
    st.markdown("##### ✏️ Paso 2 — Revisa el texto y genera tu simulacro")
    st.text_area(
        "Texto de tus apuntes (puedes editarlo antes de generar)",
        key="ocr_text",
        height=250,
    )
    examen_pasado = st.text_area(
        "Examen pasado del profe (opcional — mejora el estilo)",
        placeholder="Pega aquí preguntas de exámenes anteriores de este profesor, si tienes.",
        height=120,
    )
    n = st.slider("Número de preguntas", 3, 10, 5)

    if st.button("🧠 Generar simulacro al estilo del profe"):
        with st.spinner("Generando preguntas con Claude..."):
            try:
                payload = {
                    "content": st.session_state["ocr_text"],
                    "curso": curso,
                    "profesor": profesor,
                    "past_exam_text": examen_pasado or None,
                    "n": n,
                }
                resp = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=180)
                resp.raise_for_status()
                preguntas = resp.json()["preguntas"]
                st.success(f"✅ {len(preguntas)} preguntas generadas")
                for i, p in enumerate(preguntas, 1):
                    with st.container(border=True):
                        st.markdown(f"**{i}. {p['pregunta']}**")
                        meta = []
                        if p.get("tema"):
                            meta.append(f"📚 {p['tema']}")
                        if p.get("que_evalua"):
                            meta.append(f"🎯 {p['que_evalua']}")
                        if meta:
                            st.caption("  ·  ".join(meta))
                        with st.expander("Ver esquema de respuesta"):
                            st.write(p.get("esquema_respuesta", ""))
            except Exception as exc:  # noqa: BLE001
                st.error(f"Error al generar el simulacro: {exc}")
