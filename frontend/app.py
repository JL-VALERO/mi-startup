"""Rendir.ai — frontend Streamlit.

Flujo: sube apuntes -> lee (Claude visión para manuscrito/pizarra, PaddleOCR para
impreso) -> edita el texto -> genera un simulacro de preguntas al estilo del profe.
"""
import base64
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


def render_stepper(active: int) -> None:
    """Barra de progreso de 3 pasos; resalta el paso activo (1..3)."""
    pasos = [("1", "Sube apuntes"), ("2", "Lee con IA"), ("3", "Genera simulacro")]
    chips = []
    for i, (num, label) in enumerate(pasos, 1):
        cls = "step done" if i < active else ("step active" if i == active else "step")
        chips.append(
            f"<div class='{cls}'><span class='step-n'>{num}</span>"
            f"<span class='step-l'>{label}</span></div>"
        )
        if i < len(pasos):
            chips.append("<span class='step-sep'></span>")
    st.markdown(f"<div class='stepper'>{''.join(chips)}</div>", unsafe_allow_html=True)


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

# --- Design system: fuentes, paleta, hero, stepper y estilo de componentes ---
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@600;700;800&display=swap');

      :root{
        --amber:#F08C00; --amber-deep:#C2410C; --amber-soft:#FBEEDD;
        --radius:16px;
        --shadow:0 10px 30px rgba(120,72,0,.10); --shadow-sm:0 4px 14px rgba(120,72,0,.08);
        /* Tema CLARO por defecto; el modo oscuro sobrescribe estas variables */
        --page:#FFFCF7; --panel:#ffffff; --panel-2:#ffffff;
        --text:#2B2118; --muted:#6b5b4a; --line:#F2E4D0; --chip:#F0DCC0;
      }

      /* Limpieza del chrome de Streamlit */
      #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"]{
        visibility:hidden; height:0;}
      [data-testid="stHeader"]{background:transparent;}

      /* Tipografía y fondo de PÁGINA */
      html, body, [data-testid="stAppViewContainer"], .stApp{background:var(--page) !important;}
      html, body, .stMarkdown, p, span, li, label, input, textarea, button{
        font-family:'Inter',system-ui,-apple-system,sans-serif;}
      .stMarkdown, p, label, [data-testid="stWidgetLabel"] *{color:var(--text);}
      h1,h2,h3,h4,h5,h6{
        font-family:'Sora','Inter',sans-serif !important; color:var(--text); letter-spacing:-.01em;}

      /* Ancho legible + aire */
      .block-container, .stMainBlockContainer{
        max-width:780px; padding-top:2.2rem; padding-bottom:4rem;}

      /* HERO de marca: tarjeta gris oscuro con acento ámbar */
      .hero{margin:.4rem 0 1.4rem; padding:2.1rem 1.9rem;
        background:linear-gradient(135deg,#2E3138 0%,#23262C 55%,#1A1C20 100%);
        border:1px solid var(--line); border-bottom:3px solid var(--amber);
        border-radius:22px; color:#fff; box-shadow:0 14px 34px rgba(20,20,24,.30);}
      .hero-row{display:flex; align-items:center; gap:1rem;}
      .hero-logo{flex:0 0 auto; width:56px; height:56px; display:flex;
        align-items:center; justify-content:center; filter:drop-shadow(0 6px 14px rgba(240,140,0,.4));}
      .hero-name{font-family:'Sora',sans-serif; font-weight:800; font-size:2.1rem;
        line-height:1; color:#fff; letter-spacing:-.02em;}
      .hero-name .dot{color:var(--amber);}
      .hero-tag{margin-top:.7rem; font-size:1.08rem; font-weight:600; color:#F4F1EC;}
      .hero-sub{margin-top:.3rem; font-size:.88rem; color:#fff; opacity:.72;}

      /* STEPPER de progreso */
      .stepper{display:flex; align-items:center; gap:.4rem; margin:.1rem 0 1.4rem; flex-wrap:wrap;}
      .step{display:flex; align-items:center; gap:.45rem; padding:.32rem .75rem; border-radius:999px;
        background:var(--panel); border:1px solid var(--line); color:var(--muted);
        font-size:.82rem; font-weight:600;}
      .step .step-n{width:1.35rem; height:1.35rem; border-radius:50%; display:inline-flex;
        align-items:center; justify-content:center; background:var(--chip); color:var(--muted);
        font-size:.76rem; font-weight:700;}
      .step.active{background:var(--amber); border-color:var(--amber); color:#fff;
        box-shadow:var(--shadow-sm);}
      .step.active .step-n{background:#fff; color:var(--amber-deep);}
      .step.done{background:var(--amber-soft); border-color:#F0C088; color:var(--amber-deep);}
      .step.done .step-n{background:var(--amber); color:#fff;}
      .step-sep{flex:1 1 14px; min-width:14px; height:2px; background:var(--line); border-radius:2px;}

      /* Formulario como tarjeta */
      [data-testid="stForm"]{background:var(--panel); border:1px solid var(--line);
        border-radius:var(--radius); padding:1.3rem 1.3rem 1rem; box-shadow:var(--shadow-sm);}

      /* Inputs */
      .stTextInput input, .stTextArea textarea{border-radius:12px !important;
        background:var(--panel-2) !important; color:var(--text) !important;
        border-color:var(--line) !important;}
      .stTextInput input:focus, .stTextArea textarea:focus{
        border-color:var(--amber) !important; box-shadow:0 0 0 3px rgba(240,140,0,.18) !important;}
      .stTextInput input::placeholder, .stTextArea textarea::placeholder{
        color:var(--muted) !important; opacity:.85 !important;}

      /* Radio como segmented pills */
      [data-testid="stRadio"] [role="radiogroup"]{gap:.5rem;}
      [data-testid="stRadio"] label{background:var(--panel); border:1px solid var(--line);
        border-radius:999px; padding:.35rem .95rem; color:var(--text); transition:all .15s;}
      [data-testid="stRadio"] label:hover{border-color:var(--amber);}

      /* Dropzone del file uploader */
      [data-testid="stFileUploaderDropzone"]{background:var(--amber-soft);
        border:2px dashed var(--amber); border-radius:var(--radius);}
      [data-testid="stFileUploaderDropzone"] *{color:var(--amber-deep) !important;}

      /* Botones píldora con hover-lift (colores según el tema -> visibles en claro y oscuro) */
      .stButton button, .stDownloadButton button, [data-testid="stFormSubmitButton"] button{
        border-radius:999px !important; font-weight:700 !important; padding:.55rem 1.3rem !important;
        background:var(--panel) !important; border:1px solid var(--line) !important;
        color:var(--text) !important; transition:transform .12s ease, box-shadow .12s ease;}
      .stButton button p, .stDownloadButton button p{color:var(--text) !important;}
      .stButton button:hover, .stDownloadButton button:hover,
      [data-testid="stFormSubmitButton"] button:hover{
        transform:translateY(-2px); box-shadow:var(--shadow-sm); border-color:var(--amber) !important;}

      /* CTA principal "Leer mis apuntes": ámbar sólido, siempre visible */
      [data-testid="stFormSubmitButton"] button{
        background:var(--amber) !important; border:0 !important;}
      [data-testid="stFormSubmitButton"] button, [data-testid="stFormSubmitButton"] button p{
        color:#fff !important;}
      [data-testid="stFormSubmitButton"] button:hover{background:var(--amber-deep) !important;}

      /* Tarjetas (st.container border=True) */
      [data-testid="stVerticalBlockBorderWrapper"]{border-radius:var(--radius) !important;
        background:var(--panel); border-color:var(--line) !important;
        box-shadow:var(--shadow-sm); transition:box-shadow .15s;}
      [data-testid="stVerticalBlockBorderWrapper"]:hover{box-shadow:var(--shadow);}

      /* Tarjeta de pregunta (contenido) */
      .q-head{display:flex; align-items:center; gap:.5rem; margin:.1rem 0 .4rem;}
      .q-num{background:var(--amber); color:#fff; font-weight:700; border-radius:50%;
        width:1.7rem; height:1.7rem; display:inline-flex; align-items:center;
        justify-content:center; font-size:.9rem; flex:0 0 auto;}
      .q-chip{background:var(--amber-soft); color:var(--amber-deep); border:1px solid #F0C088;
        border-radius:1rem; padding:.12rem .65rem; font-size:.78rem; font-weight:600;}
      .q-text{font-size:1.08rem; font-weight:600; line-height:1.45; margin:.15rem 0; color:var(--text);}
      .q-eval{color:var(--muted); font-size:.9rem; margin-top:.25rem;}

      /* Expander e imágenes del PDF */
      [data-testid="stExpander"]{border-radius:12px !important; background:var(--panel);
        border-color:var(--line) !important;}
      [data-testid="stImage"] img{border-radius:10px; box-shadow:var(--shadow-sm);
        border:1px solid var(--line);}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Toggle de tema claro/oscuro (cambia el fondo de toda la página) ---
_tcol = st.columns([5, 2])[1]
dark_mode = _tcol.toggle(
    "🌙 Oscuro" if not st.session_state.get("dark_mode") else "☀️ Claro",
    key="dark_mode",
)
if dark_mode:
    st.markdown(
        "<style>:root{--page:#16181C; --panel:#23262C; --panel-2:#2A2E35;"
        " --text:#ECE8E1; --muted:#A49A8E; --line:#363A42; --chip:#3A3F47;}</style>",
        unsafe_allow_html=True,
    )

# --- Hero con identidad de marca (logo SVG inline para no romperse en la nube) ---
st.markdown(
    """
    <div class="hero">
      <div class="hero-row">
        <div class="hero-logo">
          <svg width="56" height="56" viewBox="0 0 48 48" fill="none"
               xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="rg" x1="4" y1="2" x2="44" y2="46"
                              gradientUnits="userSpaceOnUse">
                <stop stop-color="#FFC163"/>
                <stop offset="1" stop-color="#EF7C00"/>
              </linearGradient>
            </defs>
            <rect x="2" y="2" width="44" height="44" rx="13" fill="url(#rg)"/>
            <rect x="12" y="12" width="18" height="24" rx="3.2" fill="#fff"/>
            <line x1="16" y1="19" x2="26" y2="19" stroke="#F08C00" stroke-width="2.1"
                  stroke-linecap="round"/>
            <line x1="16" y1="24" x2="26" y2="24" stroke="#FBC07A" stroke-width="2.1"
                  stroke-linecap="round"/>
            <line x1="16" y1="29" x2="22" y2="29" stroke="#FBC07A" stroke-width="2.1"
                  stroke-linecap="round"/>
            <path d="M32.5 12.5 l1.75 4 4 1.75 -4 1.75 -1.75 4 -1.75 -4 -4 -1.75 4 -1.75 z"
                  fill="#fff"/>
          </svg>
        </div>
        <div class="hero-name">Rendir<span class="dot">.ai</span></div>
      </div>
      <div class="hero-tag">De una foto de tus apuntes a un simulacro al estilo de TU profesor.</div>
      <div class="hero-sub">📷 Lee tu letra a mano · 🧠 genera preguntas de desarrollo · 📄 exporta en PDF</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Stepper: el paso activo se deriva del estado de la sesión.
_active = 3 if st.session_state.get("preguntas") else (2 if "ocr_text" in st.session_state else 1)
render_stepper(_active)

st.markdown("##### 📷 Paso 1 — Sube tus apuntes y léelos")
with st.form("entrada"):
    col1, col2 = st.columns(2)
    curso = col1.text_input("Curso", placeholder="Ej. Microeconomía II")
    profesor = col2.text_input("Profesor", placeholder="Ej. A. Quispe")

    tipo = st.radio(
        "Tipo de material",
        ["Manuscrito / pizarra (Claude visión)", "Impreso / PDF (PaddleOCR)"],
        help="El manuscrito y la pizarra los lee Claude visión; lo impreso, PaddleOCR.",
        horizontal=True,
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

    payload = {
        "content": st.session_state["ocr_text"],
        "curso": curso,
        "profesor": profesor,
        "past_exam_text": examen_pasado or None,
        "n": n,
    }
    col_a, col_b = st.columns(2)
    gen_cards = col_a.button("🧠 Generar simulacro", use_container_width=True)
    gen_pdf = col_b.button("📄 Generar guía en PDF", use_container_width=True)

    if gen_cards:
        with st.spinner("Generando preguntas con Claude..."):
            try:
                resp = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=180)
                resp.raise_for_status()
                st.session_state["preguntas"] = resp.json()["preguntas"]
                st.session_state["meta"] = {"curso": curso, "profesor": profesor}
            except Exception as exc:  # noqa: BLE001
                st.error(f"Error al generar el simulacro: {exc}")

    if gen_pdf:
        with st.spinner("Generando la guía y compilando LaTeX… (la 1ra vez puede tardar)"):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/generate_pdf", json=payload, timeout=600
                )
                if resp.status_code == 200:
                    st.session_state["pdf"] = resp.json()
                else:
                    try:
                        detail = resp.json().get("detail", resp.text)
                    except Exception:  # noqa: BLE001
                        detail = resp.text
                    st.session_state.pop("pdf", None)
                    st.error(f"No se pudo generar el PDF: {detail}")
            except Exception as exc:  # noqa: BLE001
                st.error(f"Error al generar la guía: {exc}")

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

# --- Resultado: guía en PDF (estilo guía académica) ---
if st.session_state.get("pdf"):
    guia = st.session_state["pdf"]
    pdf_bytes = base64.b64decode(guia["pdf"])
    st.divider()
    st.markdown("##### 📄 Tu guía en PDF (estilo del profesor)")
    st.download_button(
        "⬇️ Descargar guía (PDF)",
        data=pdf_bytes,
        file_name="simulacro_rendir.pdf",
        mime="application/pdf",
    )
    # Previsualización como imágenes de página (confiable en cualquier navegador).
    for png_b64 in guia.get("pages", []):
        st.image(base64.b64decode(png_b64), use_container_width=True)
