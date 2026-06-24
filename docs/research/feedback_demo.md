# Feedback del demo — 3 usuarios reales (tracción)

> Prueba de usabilidad del **demo desplegado** con 3 estudiantes universitarios (carreras con
> examen de desarrollo). Es la evidencia de **tracción / señales tempranas** (§11 del dossier YC).
>
> **Privacidad:** iniciales anonimizadas, sin datos personales. El audio/notas crudas **no se
> versionan** (ver `.gitignore`). **Demo:** https://mi-startup-lmtgtvyvoyedk4rvirh25a.streamlit.app

---

## Cómo se hizo (método)
1. Se compartió la **URL del demo** con 3 estudiantes universitarios (carreras con examen de
   desarrollo). 2 dieron su feedback por **nota de voz/escrito** y se recogió **sin guiarlos**.
2. Cada uno, **solo (sin ayuda)**: escribió curso + profesor → subió una **foto de sus apuntes** →
   generó el simulacro y la **guía en PDF**. *(Si el backend en Render está dormido, la 1ª lectura
   tarda ~50 s.)*
3. Se recogió feedback con las 5 preguntas de abajo. Regla YC: **escuchar, no vender**.

## Guía de preguntas (las mismas para los 3)
1. ¿Pudiste subir tus apuntes y generar el simulacro **sin ayuda**? *(facilidad 1–5)*
2. ¿Las preguntas se parecían al **estilo de tu profesor**? *(fidelidad 1–5)*
3. ¿Qué fue lo **más confuso** o lo que **no funcionó**?
4. ¿Lo **usarías** en tu próximo examen? ¿Por qué sí/no?
5. ¿**Pagarías** el Plus (US$ 3.49/mes)? ¿Cuánto pagarías como máximo?

---

## Registro por usuario

### Usuario 1 — A. — universitaria (curso con examen de desarrollo) — jun. 2026
- **Facilidad de uso (1–5):** 5
- **Fidelidad al estilo del profe (1–5):** ≈5 — *"muy parecido"*, sobre todo en la **guía PDF**:
  el solucionario replicaba el esquema visto en clase. "No siento que le faltara nada."
- **Qué falló / fue confuso:** con **10 preguntas el PDF no cargó** y tardó muchísimo; con **5
  preguntas sí** funcionó. Al inicio, las **varias opciones de tipo de lectura** y la **separación
  en pasos** confunden (subió todo en el paso 1; sugiere "un solo paso").
- **¿Lo usaría?:** Sí, como **repaso previo** al examen.
- **¿Pagaría? ¿cuánto:** Sí; US$ 3.49 "está bien" (máximo no del todo claro en el audio, ≈S/30).
- **Cita textual destacable:** *"El PDF… era mucho mejor que el simulacro que me dio inicialmente."*
- **Bug / observación técnica:** **n=10 → PDF falla/timeout**. Acción: optimizar/limitar `n` alto;
  en el demo en vivo usar **n=5**.

### Usuario 2 — J. — universitario (curso con examen de desarrollo) — jun. 2026
- **Facilidad de uso (1–5):** 5 *(lo más lento: la subida del archivo)*
- **Fidelidad al estilo del profe (1–5):** 3 — *"más o menos lo que viene en el examen"*.
- **Qué falló / fue confuso:** en el **Paso 2 no sabía que el texto leído se podía corregir** antes
  de mandarlo a analizar. **Sin errores.**
- **¿Lo usaría?:** Sí — *"te da preguntas bastante parecidas a las que pueden venir en el examen"*.
- **¿Pagaría? ¿cuánto:** Sí; máximo **S/5**.
- **Cita textual destacable:** *"…preguntas bastante parecidas a las que pueden venir en el examen."*
- **Bug / observación técnica:** afordancia — el texto del **Paso 2 no se percibe editable**.

### Usuario 3 — O. — universitario (curso con examen de desarrollo) — jun. 2026
- **Facilidad de uso (1–5):** 5 — "ninguna parte me costó".
- **Fidelidad al estilo del profe (1–5):** 4 — *"muy fiel al estilo"*; le falta **más contexto**
  (idea: poder subir las **clases grabadas**).
- **Qué falló / fue confuso:** nada — *"funcionó correctamente"*.
- **¿Lo usaría?:** Sí — *"me gustó mucho el formato"*.
- **¿Pagaría? ¿cuánto:** Sí; máximo **~US$ 3**.
- **Cita textual destacable:** *"Muy fiel al estilo… me gustó mucho el formato."*
- **Bug / observación técnica:** ninguno.

---

## Síntesis
- **Promedios:** facilidad **5.0/5** · fidelidad **≈4.0/5** (5/3/4) · ¿usarían? **3/3** · ¿pagarían? **3/3**
- **Señal de tracción:** los **3 lo usarían** en su próximo examen y los **3 pagarían**. La **guía en
  PDF** es lo más valorado — preferida explícitamente sobre el simulacro de texto.
- **Bugs críticos detectados (antes del demo en vivo):**
  1. 🔴 **n=10 → la guía PDF no carga / timeout** (con n=5 funciona). → usar **n=5** en la demo.
  2. **Paso 2:** el texto leído **no se percibe editable** antes de analizar (afordancia).
- **Mejoras priorizadas:**
  1. Simplificar el flujo / aclarar las opciones de lectura — menos pasos (A.).
  2. Hacer visible que el texto del Paso 2 es editable (J.).
  3. Optimizar la generación con muchas preguntas y la **rapidez** general (A.).
  4. Más contexto del curso (p. ej. clases grabadas) para subir la fidelidad (O.).
- **Disposición a pagar:** todos sí, con topes dispares (**S/5**, **~US$3**, **US$3.49+**). El precio
  Plus (US$3.49 ≈ S/13) queda en el **límite alto** para algunos → evaluar **plan anual** o un tier
  más barato como ancla.
- **Cita más fuerte:** *"El PDF era mucho mejor que el simulacro"* (Usuario 1).

> Nota: las fotos de apuntes, audios y notas crudas **no se commitean** (datos personales), igual que
> las entrevistas — ver `.gitignore`.
