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


def _normalize_media_type(media_type: str) -> str:
    """Claude acepta image/jpeg (no image/jpg). Normaliza el alias."""
    return "image/jpeg" if media_type == "image/jpg" else media_type


def transcribe_images(
    items: list[tuple[bytes, str]], extra_text: str = ""
) -> dict:
    """Lee VARIAS imágenes de apuntes en UNA sola llamada a Claude visión.

    Args:
        items: lista de (image_bytes, media_type). Una sola llamada da mejor
            contexto entre páginas y es más barata que N llamadas.
        extra_text: texto ya extraído (p.ej. de un PDF digital) para integrar.
    Returns:
        {text, topics}
    """
    content: list[dict] = []
    for image_bytes, media_type in items:
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": _normalize_media_type(media_type),
                    "data": base64.standard_b64encode(image_bytes).decode("utf-8"),
                },
            }
        )
    prompt = _TRANSCRIBE_PROMPT
    if extra_text.strip():
        prompt += (
            "\n\nTEXTO YA EXTRAÍDO de otras páginas (intégralo en la transcripción "
            f"final):\n{extra_text}"
        )
    content.append({"type": "text", "text": prompt})

    resp = _client().messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=8000,
        messages=[{"role": "user", "content": content}],
        output_config={"format": {"type": "json_schema", "schema": _TRANSCRIBE_SCHEMA}},
    )
    parsed = json.loads(_first_text(resp))
    return {"text": parsed["transcription"], "topics": parsed.get("temas", [])}


def transcribe_image(image_bytes: bytes, media_type: str = "image/png") -> dict:
    """Wrapper de una sola imagen sobre `transcribe_images`."""
    return transcribe_images([(image_bytes, media_type)])


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


# --- 3) Guía-simulacro resuelta en LaTeX (estilo guía académica) -----------

_GUIA_PROMPT = r"""Eres el profesor del curso «{curso}» ({profesor}). A partir de los
apuntes del alumno, redacta una GUÍA DE SIMULACRO con {n} problemas de DESARROLLO al
estilo de preguntas de ESE profesor, CON sus soluciones, como una guía académica resuelta.

Devuelve ÚNICAMENTE el CUERPO LaTeX (sin \documentclass, sin \usepackage, sin
\begin{{document}}). Estructura por cada problema:
  \section{{Problema k -- <título corto>}}
  \subsection{{Enunciado}}   % puedes poner los datos en una tabla booktabs dentro de \begin{{teoria}}...\end{{teoria}}
  \subsection{{Marco Teórico}}  % conceptos y fórmulas clave
  \subsection{{Solución paso a paso}}  % usa align/equation; el RESULTADO final va en \begin{{respuesta}}...\end{{respuesta}}
Y al final: \section{{Resumen General}} con una tabla booktabs que resuma los problemas.

REGLAS ESTRICTAS (para que compile):
- Solo usa: \section, \subsection, itemize/enumerate, tabular con booktabs
  (\toprule \midrule \bottomrule), entornos `equation`/`align`, matemática con $...$,
  \boxed, y los entornos ya definidos `respuesta` (caja de resultado) y `teoria` (caja sobria).
- NO uses \usepackage, \definecolor, imágenes, \begin{{document}} ni colores propios.
- Escapa correctamente caracteres especiales: % como \%, & como \& (salvo en tablas), _ como \_.
- Todo en español. Matemática real y coherente con los apuntes.

APUNTES DEL ALUMNO:
{content}{estilo}
"""


def generate_guia_latex(
    content: str,
    curso: str = "",
    profesor: str = "",
    past_exam_text: str | None = None,
    n: int = 4,
) -> str:
    """Devuelve SOLO el cuerpo LaTeX de una guía-simulacro resuelta."""
    estilo = (
        f"\n\nEXÁMENES PASADOS DE ESTE PROFESOR (imita su estilo y nivel):\n{past_exam_text}"
        if past_exam_text
        else ""
    )
    prompt = _GUIA_PROMPT.format(
        curso=curso or "sin especificar",
        profesor=profesor or "docente",
        n=n,
        content=content,
        estilo=estilo,
    )
    resp = _client().messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}],
    )
    body = _first_text(resp).strip()
    # Por si el modelo envuelve en bloque de código markdown.
    if body.startswith("```"):
        body = body.split("\n", 1)[1] if "\n" in body else body
        if body.endswith("```"):
            body = body.rsplit("```", 1)[0]
    return body.strip()
