# Rendir.ai

> **Rendir.ai convierte una foto de tus apuntes en un simulacro de examen con el estilo de preguntas de tu propio profesor.**

Proyecto Final — *Data Science con Python 2026-I*, Universidad del Pacífico.
Founder solo: **Jorge Luis Valer Osis**.

---

## El problema
Los estudiantes universitarios estudian "a ciegas": no saben qué tipo de **preguntas de
desarrollo** les tomará su profesor, y armar simulacros realistas a mano toma horas. Pegar todo en
ChatGPT no funciona bien porque (a) los apuntes están **a mano o en foto de pizarra** y (b) las
preguntas que genera son **genéricas**, no al estilo del docente.

## La solución (y el insight)
Subes una **foto de tus apuntes** + opcionalmente **exámenes pasados del profesor**, y Rendir.ai
te genera un **simulacro con el estilo de preguntas de ESE profesor**.

- **Insight:** en LatAm los exámenes son de desarrollo y cada profesor tiene un estilo repetitivo y
  reconocible. Modelamos al docente, no a "un curso genérico".
- **Moat:** dataset propio por *(profesor × curso)*. Cada examen subido mejora la predicción para el
  siguiente alumno de ese profesor → efecto de red difícil de copiar.

## Arquitectura
```
[Foto/PDF de apuntes] --> Frontend (Streamlit)
                               |
                               v
                     Backend (FastAPI / Render)
                       |                    |
                       v                    v
                 PaddleOCR            Claude API
              (texto manuscrito)  (extrae temas + genera
                                   simulacro estilo profesor)
                               |
                               v
                     BD (profesor x curso x exámenes)  <-- semilla del moat
```
Diagrama detallado en `docs/arquitectura.png`.

## Herramientas del curso usadas (≥2 obligatorias)
| Herramienta | Lectura | Dónde en el código | Por qué |
|---|---|---|---|
| **PaddleOCR** | 14 | `backend/app/` (endpoint `/ocr`) | OCR de apuntes a mano / foto de pizarra en español, gratis |
| **Claude API** | 14 | `ai/` + `backend/app/` (endpoint `/generate`) | Extracción estructurada + generación de preguntas al estilo del profesor |
| **crewAI** *(opcional)* | 10–11 | `ai/agents/` | Orquestar pipeline: extraer → analizar estilo → generar → corregir |

## Cómo correr (local)

> **Entorno:** este proyecto se ejecuta en el conda env **`geo`** (Python **3.10.20**), que ya
> incluye `paddlepaddle 2.6.1`, `paddleocr 2.7.3` y `numpy 1.26`. **Actívalo en cada terminal
> antes de instalar o correr** (el prompt debe pasar de `(base)` a `(geo)`):
> ```bash
> conda activate geo
> ```
> Como `geo` ya trae el stack de PaddleOCR, el `backend/requirements.txt` incluye **solo las
> dependencias web** (FastAPI, etc.) y usa rangos para no degradar lo que `geo` ya tiene. El
> stack de OCR vive aparte en `backend/requirements-ocr.txt` (solo para deploy / entorno fresco).

```bash
# Backend (terminal 1, con `geo` activo)
cd backend
pip install -r requirements.txt        # solo deps web; `geo` ya trae PaddleOCR
cp ../.env.example ../.env             # completa ANTHROPIC_API_KEY (necesario desde el Día 2)
uvicorn app.main:app --reload

# Frontend (terminal 2, con `geo` activo)
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

> **En un entorno FRESCO o el deploy (Render):** instala además el stack de OCR:
> ```bash
> pip install -r backend/requirements-ocr.txt
> ```

> **GPU opcional (solo local):** por defecto PaddleOCR corre en CPU (igual que en el deploy de
> Render). Si tienes GPU NVIDIA y quieres acelerar, sigue `backend/requirements-gpu.txt` y pon
> `USE_GPU=true` en tu `.env`.

## Demo desplegado
🔗 **URL pública:** _(pendiente — Día 3)_
🎥 **Video demo (2–3 min):** ver `docs/video_demo.md`

## Estructura del repo
```
README.md  LICENSE  .env.example  .gitignore
docs/        # pitch deck, diagrama, capturas, research (entrevistas)
frontend/    # Streamlit
backend/     # FastAPI (app/, tests/, requirements.txt)
ai/          # prompts, agentes
data/        # muestras chicas anonimizadas
notebooks/   # EDA del estilo de preguntas
.github/workflows/  # CI (lint + tests)
```

## Construido con agentes de IA
Repo asistido con **Claude Code** (CTO backend), Claude/Codex (frontend) y crewAI (pipeline IA).

## Licencia
MIT — ver `LICENSE`.
