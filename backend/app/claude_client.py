"""Cliente de Claude (Anthropic) para Rendir.ai — Lectura 14 (Document AI con Claude).

Dos usos:
  - transcribe_image(): Claude VISIÓN lee apuntes manuscritos / foto de pizarra
    (donde PaddleOCR falla) y devuelve transcripción + temas.
  - generate_simulacro(): Claude genera un simulacro de preguntas de desarrollo
    al estilo del profesor.

Usa el SDK oficial `anthropic` y `output_config.format` (JSON schema) para salida
estructurada y parseable. Modelo: ANTHROPIC_MODEL (claude-opus-4-8 por defecto).
"""
import base64
import json

from .config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL


def _client():
    """Crea el cliente de Anthropic; error claro si falta la API key."""
    if not ANTHROPIC_API_KEY:
        raise RuntimeError(
            "Falta ANTHROPIC_API_KEY. Cópiala en tu archivo .env "
            "(ver .env.example)."
        )
    import anthropic

    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def _first_text(response) -> str:
    """Devuelve el primer bloque de texto de la respuesta de Claude."""
    for block in response.content:
        if block.type == "text":
            return block.text
    return ""


# --- 1) Lectura de apuntes con Claude visión -------------------------------

_TRANSCRIBE_SCHEMA = {
    "type": "object",
    "properties": {
        "transcription": {"type": "string"},
        "temas": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["transcription", "temas"],
    "additionalProperties": False,
}

_TRANSCRIBE_PROMPT = (
    "Eres un asistente que transcribe apuntes de estudiantes. La imagen puede ser "
    "letra a mano o una foto de pizarra. Transcribe TODO el contenido de forma fiel "
    "en su idioma original (normalmente español), corrigiendo solo errores obvios de "
    "OCR. Luego lista los temas/conceptos principales que aparecen. Devuelve el "
    "resultado en el formato JSON solicitado."
)


def transcribe_image(image_bytes: bytes, media_type: str = "image/png") -> dict:
    """Lee una imagen de apuntes con Claude visión. Devuelve {text, topics}."""
    data = base64.standard_b64encode(image_bytes).decode("utf-8")
    resp = _client().messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": data,
                        },
                    },
                    {"type": "text", "text": _TRANSCRIBE_PROMPT},
                ],
            }
        ],
        output_config={"format": {"type": "json_schema", "schema": _TRANSCRIBE_SCHEMA}},
    )
    parsed = json.loads(_first_text(resp))
    return {"text": parsed["transcription"], "topics": parsed.get("temas", [])}


# --- 2) Generación del simulacro al estilo del profesor --------------------

_GENERATE_SCHEMA = {
    "type": "object",
    "properties": {
        "preguntas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "pregunta": {"type": "string"},
                    "tema": {"type": "string"},
                    "que_evalua": {"type": "string"},
                    "esquema_respuesta": {"type": "string"},
                },
                "required": ["pregunta", "tema", "que_evalua", "esquema_respuesta"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["preguntas"],
    "additionalProperties": False,
}


def generate_simulacro(
    content: str,
    curso: str = "",
    profesor: str = "",
    past_exam_text: str | None = None,
    n: int = 5,
) -> dict:
    """Genera N preguntas de desarrollo al estilo del profesor. Devuelve {preguntas}."""
    estilo = (
        f"\n\nEXÁMENES PASADOS DE ESTE PROFESOR (imita su estilo, nivel de exigencia "
        f"y tipo de redacción):\n{past_exam_text}"
        if past_exam_text
        else ""
    )
    prompt = (
        f"Eres el profesor del curso «{curso or 'sin especificar'}» "
        f"({profesor or 'docente'}). A partir de los apuntes del alumno, redacta "
        f"{n} PREGUNTAS DE DESARROLLO (abiertas, no de opción múltiple) que "
        f"probablemente tomarías en un examen, en español. Para cada pregunta indica "
        f"el tema, qué evalúa y un esquema breve de la respuesta esperada. Si hay "
        f"exámenes pasados, imita el estilo del profesor.\n\n"
        f"APUNTES DEL ALUMNO:\n{content}{estilo}"
    )
    resp = _client().messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
        output_config={"format": {"type": "json_schema", "schema": _GENERATE_SCHEMA}},
    )
    parsed = json.loads(_first_text(resp))
    return {"preguntas": parsed["preguntas"]}
