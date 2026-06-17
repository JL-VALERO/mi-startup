"""Wrapper de PaddleOCR (Lectura 14) para Rendir.ai.

PaddleOCR es pesado en memoria, así que el modelo se carga de forma PEREZOSA
(solo en el primer uso real) y se cachea. Los imports pesados (paddleocr, numpy,
PIL) también son diferidos para que importar este módulo no requiera tenerlos
instalados — esto mantiene el CI ligero y rápido.
"""
from functools import lru_cache

from .config import OCR_LANG


@lru_cache(maxsize=1)
def _get_ocr():
    """Devuelve una instancia única de PaddleOCR (carga perezosa + cache)."""
    from paddleocr import PaddleOCR

    return PaddleOCR(use_angle_cls=True, lang=OCR_LANG, show_log=False)


def _image_bytes_to_array(data: bytes):
    """Convierte los bytes de una imagen subida en un array RGB para PaddleOCR."""
    import io

    import numpy as np
    from PIL import Image

    img = Image.open(io.BytesIO(data)).convert("RGB")
    return np.array(img)


def extract_text(data: bytes) -> dict:
    """Corre OCR sobre los bytes de una imagen.

    Returns:
        dict con `text` (todo el texto unido), `lines` (texto + confianza por
        línea), `avg_confidence` y `num_lines`.
    """
    arr = _image_bytes_to_array(data)
    ocr = _get_ocr()
    raw = ocr.ocr(arr, cls=True)

    # PaddleOCR devuelve [None] cuando no detecta texto.
    page = raw[0] if raw and raw[0] else []

    lines = []
    for entry in page:
        # Cada entry = [bbox, (texto, score)]
        text, score = entry[1][0], float(entry[1][1])
        lines.append({"text": text, "confidence": round(score, 4)})

    full_text = "\n".join(line["text"] for line in lines)
    avg_conf = (
        round(sum(line["confidence"] for line in lines) / len(lines), 4)
        if lines
        else 0.0
    )
    return {
        "text": full_text,
        "lines": lines,
        "avg_confidence": avg_conf,
        "num_lines": len(lines),
    }
