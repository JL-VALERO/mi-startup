"""Soporte de PDF para Rendir.ai usando PyMuPDF (`fitz`).

- `pdf_extract`: texto + nº de páginas + heurística de "escaneado".
  El texto de PDFs digitales sale GRATIS (sin tokens) y corre incluso en el deploy.
- `pdf_render_images`: renderiza cada página a PNG (para PDFs escaneados / Claude visión).

PyMuPDF es una sola wheel sin binarios externos (funciona en Windows y en Render).
Los imports son diferidos para no exigir la dependencia al importar el resto del backend.
"""


def _open(data: bytes):
    import fitz  # PyMuPDF

    return fitz.open(stream=data, filetype="pdf")


def pdf_extract(data: bytes) -> dict:
    """Devuelve {text, n_pages, is_scanned} del PDF.

    `is_scanned` es True cuando hay muy poco texto por página (probablemente
    imágenes escaneadas), señal de que conviene OCR/visión en vez de texto directo.
    """
    doc = _open(data)
    try:
        partes = []
        for i, page in enumerate(doc, 1):
            txt = page.get_text("text").strip()
            if txt:
                partes.append(f"--- Página {i} ---\n{txt}")
        n_pages = doc.page_count
    finally:
        doc.close()
    text = "\n\n".join(partes)
    is_scanned = n_pages > 0 and len(text) < 40 * n_pages
    return {"text": text, "n_pages": n_pages, "is_scanned": is_scanned}


def pdf_render_images(data: bytes, dpi: int = 200, max_pages: int = 10) -> list[bytes]:
    """Renderiza hasta `max_pages` páginas del PDF a PNG (bytes)."""
    doc = _open(data)
    try:
        imgs = []
        for page in doc:
            if len(imgs) >= max_pages:
                break
            pix = page.get_pixmap(dpi=dpi)
            imgs.append(pix.tobytes("png"))
        return imgs
    finally:
        doc.close()
