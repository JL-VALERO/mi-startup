# Mercado & modelo de negocio — Rendir.ai

> Sección 6 y 9 del dossier YC: tamaño de mercado (TAM/SAM/SOM con fuentes), cómo gana dinero,
> pricing y **contribution margin** (costo real de tokens por simulacro).
>
> *Cifras de mercado de fuentes públicas (SUNEDU, CLACSO); supuestos de pricing y costos marcados
> como tales. Tipo de cambio usado: **S/ 3.75 por US$**. Precios de tokens: tarifas oficiales de la
> API de Claude (jun. 2026).*

---

## 1. Mercado (TAM / SAM / SOM)

| Nivel | Definición | Tamaño (usuarios) | Valor anual estimado* |
|---|---|---|---|
| **TAM** | Estudiantes universitarios en **América Latina** | **~30.9 millones** (2021) | ~US$ 1,200 M/año |
| **SAM** | Estudiantes universitarios en **Perú** en carreras con **examen de desarrollo** y exámenes pasados heredables (ICP) | **~720 mil** (60% de ~1.2 M) | ~US$ 29 M/año |
| **SOM** | A quién alcanzamos los **primeros 12 meses** (UP + expansión temprana en Lima) | **~5,000 registrados** (~500 de pago) | ~US$ 20–40 K/año + pilotos B2B |

\* *Valor anual = usuarios × precio del plan Plus (~US$ 40/año) a penetración plena. Es un techo
teórico para el TAM/SAM; el SOM usa una conversión a pago realista (~10%).*

**Fuentes y supuestos:**
- **TAM:** ~30.9 M de estudiantes de educación superior en América Latina (CLACSO, dato 2021; +32%
  vs. 2012). Mercado en el que el insight aplica: exámenes de desarrollo + estilo del profesor.
- **SAM:** **~1.2 millones** de universitarios en Perú en universidades licenciadas (SUNEDU: ~340 K
  públicas + ~676 K privadas). Acotamos al **~60%** en carreras con examen de desarrollo donde
  circulan exámenes pasados (Economía, Derecho, Ingeniería, Ciencias, etc.) → **~720 K**. Esto se
  alinea con las 7 entrevistas (`docs/research/hallazgos_entrevistas.md`): todas encajan en este ICP.
- **SOM:** arrancamos por la **UP** (~12 K estudiantes) y universidades cercanas de Lima. Meta año 1:
  ~5,000 registrados (freemium) y ~10% de conversión a pago, más 2–3 **pilotos B2B** (academias /
  centros de nivelación).

---

## 2. Modelo de negocio (cómo gana dinero)

**Freemium + B2B**, apalancado en el **moat** *(dataset por profesor × curso)*:

1. **B2C freemium → Plus:** el alumno usa gratis con límites; convierte a Plus por simulacros
   ilimitados, PDF y subir examen pasado.
2. **B2B academias / universidades:** licencia por alumno o por curso. Es donde el moat paga: una
   academia con histórico de exámenes de un profesor genera simulacros muy fieles.
3. **Motor del moat:** cada examen pasado subido mejora la predicción para el siguiente alumno de ese
   *(profesor × curso)* → efecto de red difícil de copiar (validado: 4/7 entrevistados heredan
   exámenes de terceros).

---

## 3. Pricing (máx. 3 planes)

| Plan | Precio | Qué incluye | Para quién |
|---|---|---|---|
| **Free** | S/ 0 | 3 simulacros/mes, lectura de apuntes, marca de agua, sin PDF | Adquisición |
| **Plus Estudiante** | **S/ 12.90/mes** o **S/ 99/año** (~US$ 3.4/mes) | Simulacros ilimitados, **PDF estilo guía**, subir examen pasado (foto/PDF), modo mixto | Estudiante activo en época de exámenes |
| **B2B Academias** | **Desde S/ 8 por alumno/ciclo** (licencia) | Panel por curso, dataset del profesor, simulacros masivos, marca de la academia | Academias / centros de nivelación / facultades |

*Precio anclado a la disposición a pagar observada: 3/7 entrevistados ya pagan ~US$ 20/mes por IA;
el Plus a ~US$ 3.4/mes es una fracción de eso y se posiciona como "IA que te sube la nota", no como
"material".*

---

## 4. Contribution margin (costo de tokens por simulacro)

**Supuesto de consumo por simulacro** (lectura con Claude visión + generación):
~**4,200 tokens de entrada** + ~**4,000 tokens de salida**.
*(Imagen de apuntes ≈ 1,600 tokens a resolución estándar; PaddleOCR para impreso = **0 tokens**,
gratis. PDF estilo LaTeX añade ~6,000 tokens de salida — ~duplica el costo del simulacro.)*

### Costo variable por simulacro, según modelo

| Modelo | Tarifa (in / out por 1M) | Costo por simulacro | En soles |
|---|---|---|---|
| **Haiku 4.5** | US$ 1 / US$ 5 | **US$ 0.024** | **S/ 0.09** |
| **Sonnet 4.6** | US$ 3 / US$ 15 | **US$ 0.073** | **S/ 0.27** |
| **Opus 4.8** | US$ 5 / US$ 25 | **US$ 0.121** | **S/ 0.45** |

### Unit economics por usuario Plus (supuesto: 20 simulacros/mes)

| Modelo en producción | Costo variable/mes | Ingreso Plus/mes | **Margen de contribución** |
|---|---|---|---|
| **Haiku 4.5** | US$ 0.48 (S/ 1.8) | US$ 3.4 (S/ 12.9) | **~86%** |
| **Sonnet 4.6** | US$ 1.45 (S/ 5.4) | US$ 3.4 (S/ 12.9) | **~58%** |
| **Opus 4.8** | US$ 2.42 (S/ 9.1) | US$ 3.4 (S/ 12.9) | ~29% (no rentable a uso alto) |

**Decisión de margen:** producción en **Haiku/Sonnet** (margen 58–86%); **Opus** se reserva para la
demo o un add-on premium. PaddleOCR cubre gratis el material impreso, bajando el costo promedio real.
El margen mejora con caché de prompts y reuso del dataset por *(profesor × curso)*.

---

## 5. Supuestos y próximos pasos
- Validar precio con una encuesta corta de disposición a pagar (las entrevistas ya dan señal).
- Cerrar 1–2 pilotos B2B para probar el modelo de licencia por alumno.
- Refinar consumo de tokens con datos reales del demo (medir tokens/simulacro en producción).
