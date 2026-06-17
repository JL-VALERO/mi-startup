"""Configuración de Rendir.ai leída desde variables de entorno (.env)."""
import os

# Carga .env si python-dotenv está disponible (no rompe si falta, p.ej. en CI).
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover
    pass

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-opus-4-8")

# Idioma para PaddleOCR ("es" = español; maneja también texto a mano).
OCR_LANG = os.getenv("OCR_LANG", "es")

# Usar GPU para PaddleOCR. Default False (Render/CI no tienen GPU). Para activarlo
# en local: instalar paddlepaddle-gpu (ver backend/requirements-gpu.txt) y USE_GPU=true.
USE_GPU = os.getenv("USE_GPU", "false").strip().lower() in {"1", "true", "yes", "si"}
