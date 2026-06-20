"""Rendir.ai — frontend Streamlit.

Flujo: sube apuntes -> lee (Claude visión para manuscrito/pizarra, PaddleOCR para
impreso) -> edita el texto -> genera un simulacro de preguntas al estilo del profe.
"""
import html
import os

import requests
import streamlit as st


def _simulacro_md(curso: str, profesor: str, preguntas: list[dict]) -> str:
    """Compila el simulacro a Markdown para descargar."""
    out = [f"# Simulacro — {curso or 'curso'} ({profesor or 'profesor'})", ""]
    for i, p in enumerate(preguntas, 1):
        out.append(f"## {i}. {p['pregunta']}")
        if p.get("tema"):
            out.append(f"- **Tema:** {p['tema']}")
        if p.get("que_evalua"):
            out.append(f"- **Evalúa:** {p['que_evalua']}")
        out.append(f"\n**Esquema de respuesta:** {p.get('esquema_respuesta', '')}\n")
    return "\n".join(out)

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

# Vista más limpia + estilo de las tarjetas de pregunta (CSS mínimo y contenido).
st.markdown(
    """
    <style>
      #MainMenu, footer {visibility: hidden;}
      .q-head {display:flex; align-items:center; gap:.5rem; margin:.1rem 0 .35rem;}
      .q-num {background:#F08C00; color:#fff; font-weight:700; border-radius:50%;
              width:1.7rem; height:1.7rem; display:inline-flex; align-items:center;
              justify-content:center; font-size:.9rem; flex:0 0 auto;}
      .q-chip {background:#FBEEDD; color:#92400e; border:1px solid #F0C088;
               border-radius:1rem; padding:.12rem .65rem; font-size:.78rem; font-weight:600;}
      .q-text {font-size:1.06rem; font-weight:600; line-height:1.45; margin:.15rem 0;}
      .q-eval {color:#6b5b4a; font-size:.9rem; margin-top:.2rem;}
    </style>
    """,
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
        "Sube una o varias fotos (PNG/JPG) o un PDF de tus apuntes",
        type=["png", "jpg", "jpeg", "pdf"],
        accept_multiple_files=True,
    )
    leer = st.form_submit_button("📷 Leer mis apuntes")

if leer:
    if not apuntes:
        st.warning("Primero sube al menos una foto o un PDF de tus apuntes.")
    else:
        endpoint = "/transcribe" if tipo.startswith("Manuscrito") else "/ocr"
        motor = "Claude visión" if endpoint == "/transcribe" else "PaddleOCR"
        with st.spinner(f"Leyendo {len(apuntes)} archivo(s) con {motor}..."):
            try:
                files = [
                    ("files", (f.name, f.getvalue(), f.type or "application/octet-stream"))
                    for f in apuntes
                ]
                resp = requests.post(f"{BACKEND_URL}{endpoint}", files=files, timeout=300)
                resp.raise_for_status()
                data = resp.json()
                st.session_state["ocr_text"] = data["text"]
                if data.get("topics"):
                    st.caption("Temas detectados: " + ", ".join(data["topics"]))
                st.success(
                    f"✅ {len(apuntes)} archivo(s) leído(s). Revisa el texto abajo y genera tu simulacro."
                )
            except requests.exceptions.ConnectionError:
                st.error(
                    f"No pude conectar con el backend en {BACKEND_URL}. "
                    "¿Está corriendo `uvicorn app.main:app`?"
                )
            except Exception as exc:  # noqa: BLE001
                st.error(f"Error al leer los apuntes: {exc}")

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
                st.session_state["preguntas"] = resp.json()["preguntas"]
                st.session_state["meta"] = {"curso": curso, "profesor": profesor}
            except Exception as exc:  # noqa: BLE001
                st.error(f"Error al generar el simulacro: {exc}")

# --- Resultado: simulacro como tarjetas (persiste entre interacciones) ---
if st.session_state.get("preguntas"):
    preguntas = st.session_state["preguntas"]
    meta = st.session_state.get("meta", {})
    st.divider()
    head_l, head_r = st.columns([3, 1])
    head_l.markdown(f"##### 🧠 Tu simulacro · {len(preguntas)} preguntas")
    head_r.download_button(
        "⬇️ Descargar",
        data=_simulacro_md(meta.get("curso", ""), meta.get("profesor", ""), preguntas),
        file_name="simulacro_rendir.md",
        mime="text/markdown",
        use_container_width=True,
    )
    for i, p in enumerate(preguntas, 1):
        with st.container(border=True):
            tema = html.escape(p.get("tema", ""))
            pregunta = html.escape(p.get("pregunta", ""))
            evalua = html.escape(p.get("que_evalua", ""))
            chip = f"<span class='q-chip'>📚 {tema}</span>" if tema else ""
            evalua_html = (
                f"<div class='q-eval'>🎯 <b>Evalúa:</b> {evalua}</div>" if evalua else ""
            )
            st.markdown(
                f"<div class='q-head'><span class='q-num'>{i}</span>{chip}</div>"
                f"<div class='q-text'>{pregunta}</div>{evalua_html}",
                unsafe_allow_html=True,
            )
            with st.expander("Ver esquema de respuesta"):
                st.write(p.get("esquema_respuesta", ""))
