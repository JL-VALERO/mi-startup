"""Rendir.ai — frontend Streamlit (esqueleto, Día 0)."""
import streamlit as st

st.set_page_config(page_title="Rendir.ai", page_icon="📝", layout="centered")

st.title("📝 Rendir.ai")
st.subheader("Convierte una foto de tus apuntes en un simulacro al estilo de tu profesor")

st.info("Esqueleto inicial. El flujo se conecta al backend en el Día 1–2.")

curso = st.text_input("Curso")
profesor = st.text_input("Profesor")
apuntes = st.file_uploader("Sube una foto/PDF de tus apuntes", type=["png", "jpg", "jpeg", "pdf"])

if st.button("Generar simulacro", disabled=True):
    st.warning("Pendiente de conectar al backend (POST /ocr -> /generate).")
