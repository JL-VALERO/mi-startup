# Pitch Deck — Rendir.ai (14 secciones YC)

> Founder: **Jorge Luis Valer Osis** · Proyecto Final, Data Science con Python 2026-I (UP).
> Versión presentable en PDF: [`docs/pitch_deck.pdf`](pitch_deck.pdf) (fuente: `docs/pitch_deck.tex`).

### 1 · One-liner
**Rendir.ai convierte una foto de tus apuntes en un simulacro de examen con el estilo de preguntas de tu propio profesor.**

### 2 · Founder
Solo founder: **Jorge Luis Valer Osis**, estudiante UP — soy el usuario, vivo el problema (*founder–market fit*).
Construido con agentes de IA: **Claude Code** (CTO backend), Claude/Codex (frontend).

### 3 · Problema
- **Quién:** universitarios en cursos con **examen de desarrollo**.
- Estudian "a ciegas": no saben qué **estilo** de preguntas tomará el profe.
- Armar simulacros realistas a mano toma **horas**; ChatGPT genérico falla (apuntes a mano/pizarra + preguntas genéricas).
- *"No sabes exactamente qué te va a venir…"* (entrevista). **Validado con 7 entrevistas.**

### 4 · Solución & Insight
Subes **todo tu material junto** (apuntes + exámenes pasados) → Rendir.ai genera una **guía-simulacro al estilo de ESE profesor**.
**Insight:** en LatAm los exámenes son de desarrollo y **cada profesor tiene un estilo repetitivo y heredable**. Modelamos al **docente**, no a "un curso genérico".

### 5 · Why now
LLMs baratos + **Claude visión** lee manuscrito/pizarra (donde el OCR clásico falla) + **PaddleOCR** gratis para impreso + **Claude Code** deja a 1 persona construir el producto en horas. La ventana es **ahora**.

### 6 · Mercado
- **TAM:** ~30.9 M universitarios en LatAm (CLACSO).
- **SAM:** ~720 K en Perú (SUNEDU ~1.2 M × ~60% en carreras con examen de desarrollo).
- **SOM:** ~5,000 año 1 (UP + Lima) + pilotos B2B.

### 7 · Competencia & Moat
- vs **ChatGPT/NotebookLM**: genéricos, leen mal la foto, no modelan al profe. vs **hacerlo a mano**: horas. vs **no hacer nada**.
- **Moat:** dataset propio por *(profesor × curso)*. Cada examen subido **mejora la predicción** para el siguiente alumno → efecto de red. *(Validado: 4/7 entrevistados heredan exámenes de terceros.)*

### 8 · Producto — demo + arquitectura
- **Demo desplegado:** https://mi-startup-lmtgtvyvoyedk4rvirh25a.streamlit.app
- **Subes TODO junto** y la app **clasifica cada archivo** y usa la herramienta correcta (Claude visión para fotos/escaneados; texto directo para PDFs) → genera una **guía-simulacro resuelta en PDF**.
- **Arquitectura:** Streamlit → FastAPI/Render → Claude API / PaddleOCR. **2 herramientas del curso:** Claude API + PaddleOCR.

### 9 · Modelo de negocio & pricing
- **Freemium + B2B academias.** Free / **Plus US$ 3.49/mes** (o US$ 26/año) / **B2B desde US$ 2 por alumno-ciclo**.
- **Contribution margin 58–86%** (Haiku/Sonnet); impreso = US$ 0 (PaddleOCR). **Se autofinancia con ~4–9 usuarios de pago** (break-even año 1).

### 10 · Go-to-market
- **10:** mi salón / facultad en la UP. **100:** boca a boca en grupos de WhatsApp por curso + facultades UP. **1,000:** otras universidades de Lima + pilotos B2B con academias.

### 11 · Tracción
- Demo **desplegado y funcionando** (URL pública). 7 entrevistas validan problema y moat.
- Un entrevistado **ya hace Rendir.ai a mano** con ChatGPT → demanda real. *(En curso: 3 usuarios prueban el demo.)*

### 12 · Roadmap
- **3 meses:** pulir flujo + sembrar dataset *(profesor × curso)* en 1 facultad UP.
- **6 meses:** piloto B2B con 1–2 academias; más universidades de Lima.
- **12 meses:** cobertura Perú + app móvil.

### 13 · Riesgos & mitigación
- **Técnico** (calidad del simulacro): feedback loop + fine-tune con exámenes reales.
- **Mercado** (disposición a pagar): freemium para adquirir + B2B donde sí hay presupuesto.
- **Ejecución** (solo founder): agentes de IA + foco en UN flujo que funcione.

### 14 · The ask
Buscamos **100 estudiantes beta este ciclo + 1 academia piloto** para sembrar el dataset.
Eso desbloquea el **moat** *(dataset por profesor × curso)* y las primeras señales de pago.

> *"Make something people want." — Y Combinator*
