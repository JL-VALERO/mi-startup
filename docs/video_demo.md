# Video demo — Rendir.ai (guion de grabación)

🎥 **Link (Google Drive):** https://drive.google.com/file/d/1k95cF7SYhDxElduFXnFscAsWIWOlt3ve/view?usp=drive_link

> **Para qué es:** video de **2–3 min** que es el **Plan B obligatorio** del demo en vivo (si falla
> internet/deploy en la presentación, se reproduce este). También sirve como demo enlazado en el repo.

---

## ✅ Checklist ANTES de grabar (5 min de prep)
- [ ] **Despertar el backend:** abrir la app **~1 min antes** (Render free duerme; la 1ª lectura
      tarda ~50 s). Hacer **una corrida de prueba completa** para que quede caliente.
- [ ] **Tener lista una FOTO de apuntes manuscritos** (a mano o de pizarra) en el escritorio.
- [ ] ⚠️ **Generar con n = 5 preguntas, NO 10.** Con 10 el PDF se cuelga/timeout (lo detectó una
      usuaria). Con 5 sale perfecto y rápido.
- [ ] **Plan B del Plan B:** correr la app **en LOCAL** (backend + frontend en `geo`, MiKTeX listo) y
      dejar un **PDF ya generado** a la mano, por si el deploy falla durante la grabación.
- [ ] **Pantalla limpia:** cerrar pestañas, silenciar notificaciones, modo no molestar.
- [ ] **Grabar a 1080p**, audio claro (Loom u OBS). Probar 5 s de audio antes.
- [ ] Tener el **precio** y el **dato de tracción** a la vista para no dudar al narrar.

---

## 🎬 Guion (columna IZQ = qué grabar · DER = qué decir)

### 1 · Hook + problema — (0:00–0:20)
- **GRABAR:** tu cara 2 s (opcional) y luego la foto de apuntes manuscritos en pantalla.
- **DECIR:**
  > "Estudiar para un examen de desarrollo es estudiar a ciegas: no sabes qué te va a preguntar tu
  > profesor. Y pegar tus apuntes en ChatGPT no sirve —están a mano— y las preguntas que da son
  > genéricas. Esto es **Rendir.ai**."

### 2 · Solución + insight — (0:20–0:40)
- **GRABAR:** la pantalla de inicio de la app (curso, profesor, subir material).
- **DECIR:**
  > "Subes una **foto de tus apuntes** y Rendir.ai te genera un simulacro **con el estilo de preguntas
  > de ESE profesor**. El insight: en LatAm los exámenes son de desarrollo y cada profe tiene un estilo
  > repetitivo y reconocible. Modelamos al **docente**, no a un curso genérico."

### 3 · Demo en vivo (el corazón) — (0:40–1:50)
- **GRABAR (paso a paso, mostrando el cursor):**
  1. Escribir **curso** y **profesor**.
  2. **Subir la foto** de apuntes manuscritos.
  3. Click en **"Leer mis apuntes"** → mostrar el **texto transcrito** + temas detectados.
  4. **Dejar n = 5.** Click en **"Generar guía-simulacro"**.
  5. Mostrar el **PDF** generado: portada, preguntas, cajas de respuesta.
- **DECIR (mientras ocurre):**
  > "Escribo el curso y el profesor… subo una foto de mis apuntes a mano. La app usa **Claude visión**
  > para leer la letra manuscrita —y **PaddleOCR** para material impreso—. Acá ya transcribió mis
  > apuntes y detectó los temas. Genero el simulacro… y me da una **guía en PDF resuelta**, con
  > preguntas al estilo de mi profe. *(Esperar a que cargue; narrar la portada y un par de preguntas.)*"

> 💡 Si el deploy tarda, di con naturalidad: *"el servidor gratuito estaba despertando"* y, si hace
> falta, corta y muestra el **PDF ya generado** que dejaste listo.

### 4 · Por qué es mejor que ChatGPT + tracción — (1:50–2:20)
- **GRABAR:** el PDF en pantalla (o la galería de capturas).
- **DECIR:**
  > "¿Por qué no ChatGPT? Porque **lee tu letra a mano y la pizarra**, y porque imita **el estilo de tu
  > profesor**, no preguntas genéricas. Lo probaron **3 estudiantes reales**: facilidad **5/5**, los
  > **3 lo usarían** en su próximo examen y los **3 pagarían** —y lo que más valoraron fue justo esta
  > **guía en PDF**."

### 5 · Modelo + the ask — (2:20–2:50)
- **GRABAR:** tu cara, o una slide simple con el precio.
- **DECIR:**
  > "Modelo freemium: el plan **Plus** cuesta **US$3.49 al mes**. Y el **moat** es un dataset propio por
  > **profesor × curso**: cada examen subido mejora la predicción para el siguiente alumno de ese
  > profe —un efecto de red difícil de copiar. **Rendir.ai: convierte tus apuntes en el examen de tu
  > profesor.** Gracias."

---

## Notas de edición
- Duración total objetivo: **2:30–3:00**. Si te pasas, recorta la narración del paso 3 (deja que la
  pantalla hable).
- Subtítulos ayudan (Loom los genera). Sube como **"no listado"** en YouTube o link de Loom.
- Al terminar: **pega el link arriba** (línea 🎥) y haz commit.

> Recordatorio: las fotos de apuntes que se vean en el video deben ser **tuyas o de muestra** (no
> datos personales de terceros).
