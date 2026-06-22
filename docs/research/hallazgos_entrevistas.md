# Hallazgos de entrevistas — Rendir.ai

> Síntesis de la investigación de usuarios. **7 entrevistas** a estudiantes universitarios que
> dieron un examen de desarrollo reciente (meta de rúbrica: ≥5). Metodología YC *"How to Talk to
> Users"*: se preguntó por el **pasado y el presente**, no por hipótesis futuras.
>
> **Privacidad:** el audio y las transcripciones contienen datos personales y **nunca se commitean**
> (ver `.gitignore`); se transcribieron en local con Whisper (`scripts/transcribir_entrevistas.py`).
> Este documento es la versión **anonimizada** (solo iniciales) apta para el repo.

## Resumen ejecutivo

- **7/7** estudiaron con una mezcla de **apuntes + slides/lecturas del profesor**; la digitalización
  de material a mano sigue siendo un punto de fricción.
- **6/7** usaron **exámenes pasados del profesor** como su mejor predictor del examen real, y la
  mayoría los obtuvo **de otra persona** (compañeros, ciclos superiores, amigos que ya llevaron el
  curso) → señal directa del **moat** de Rendir.ai.
- **7/7** ya usan IA (ChatGPT, Claude, Gemini, NotebookLM) para estudiar, pero reportan límites
  claros: planes gratuitos que no dejan subir imágenes, respuestas dispersas, y ejercicios que la IA
  "se va por otra rama" y no resuelve en el contexto correcto.
- **Disposición a pagar:** mixta. 4/7 dicen no haber pagado nunca por material de estudio; **3/7 sí
  pagan** suscripciones de IA (~$20/mes ChatGPT/Claude Plus) o apps de organización (~$10 Notion).

| Hipótesis | Veredicto | Evidencia |
|---|---|---|
| **H1** — estudian sin saber el estilo del profe → ansiedad y horas perdidas | ✅ **Validada** | 6/7 anticipan vía exámenes pasados; varios citan "no saber qué te va a venir" como su mayor dolor |
| **H2** — la fricción de digitalizar apuntes a mano frena el buen uso de ChatGPT | ⚠️ **Parcial** | Confirmada de forma explícita por 1 (límite de subir imágenes en plan gratis); el resto usa IA con fricción menor |
| **H3** — disposición a pagar por simulacros al estilo del profe | 🟡 **Mixta** | 3/7 ya pagan IA/apps; 4/7 "nunca pagué nada" — pero pagan **tiempo**, no dinero |
| **Moat** — se comparten/heredan exámenes pasados por profesor×curso | ✅ **Validado fuerte** | 4/7 obtuvieron exámenes pasados de terceros; 1 los transfiere a la IA para imitar el estilo |

---

## Registro por entrevista

> Plantilla del guion (`guion_entrevistas.md`). Iniciales anonimizadas; fechas jun. 2026 (aprox.).

### Entrevista N°1 — A. — curso de matemática — jun. 2026
- **Cómo estudió:** rehízo los ejercicios de clase y luego resolvió exámenes pasados de ciclos anteriores ("muy parecidos a los que me iban a tomar"). 1–2 h diarias.
- **Mayor dolor:** errores mínimos de procedimiento (un signo, un mal despeje) que arruinan todo el ejercicio.
- **¿Anticipó preguntas?** Sí — los exámenes pasados y sus variables eran muy parecidos al real.
- **Uso de IA (qué falló):** ChatGPT para corroborar procedimientos/gráficos; **límite:** sin plan Pro no puede subir muchas imágenes.
- **¿Comparte/recibe exámenes? (moat):** tenía exámenes de ciclos anteriores.
- **Último que hizo/pagó:** instaló GoodNotes (apuntes en iPad). Nunca pagó por material.
- **Cita:** *"Como no tengo ChatGPT Pro, no puedo subir bastantes imágenes."*
- **¿Confirma/reta hipótesis?** Confirma H1 y H2 (fricción de imágenes).

### Entrevista N°2 — C. — curso teórico-práctico — jun. 2026
- **Cómo estudió:** listó los temas que entraban, revisó clases grabadas para apuntar la parte práctica, estudió lecturas + resúmenes. 5–7 h en 3 días.
- **Mayor dolor:** tener que **volver a ver las clases grabadas** (no toma notas en el momento); lento, clases de ~1.5 h.
- **¿Anticipó preguntas?** Sí en la parte práctica (gracias a exámenes pasados); la teórica varía mucho entre ciclos.
- **Uso de IA (qué falló):** ChatGPT para conceptos sueltos; NotebookLM para sintetizar lecturas.
- **¿Comparte/recibe exámenes? (moat):** **"me lo pasó un amigo que ya había pasado el curso."**
- **Último que hizo/pagó:** instaló Notion (con Pomodoro y rachas); pagó ~$10 una vez, luego lo obtuvo gratis con correo estudiantil.
- **Cita:** *"La parte práctica sí logré anticipar… gracias a que revisé los exámenes pasados; esto me lo pasó un amigo que ya había pasado el curso."*
- **¿Confirma/reta hipótesis?** Confirma H1 y moat; aporta señal de pago vía correo estudiantil.

### Entrevista N°3 — D. — métodos / teoría de juegos — jun. 2026
- **Cómo estudió:** 3 h diarias por 2 semanas con apuntes de clase, **fotos de la pizarra** y exámenes pasados.
- **Mayor dolor:** curso que repite + situación de riesgo académico; tiempo muerto en transporte a la universidad.
- **¿Anticipó preguntas?** Sí — usó el examen anterior como referencia, preguntas "muy parecidas".
- **Uso de IA (qué falló):** ChatGPT en teoría de juegos (no en métodos); **límite:** sin premium "se vuelve lento".
- **¿Comparte/recibe exámenes? (moat):** **se los pasó una compañera** ("me los pasaron básicamente").
- **Último que hizo/pagó:** nada — "todo ha sido gratuito".
- **Cita:** *"Estudié de los apuntes, fotos de la pizarra y exámenes pasados… me los pasaron."*
- **¿Confirma/reta hipótesis?** Confirma H1 y moat; refuta H3 (no paga).

### Entrevista N°4 — J.V. — economía / teoría bancaria — jun. 2026
- **Cómo estudió:** usó ChatGPT + Codex para **generar un banco de preguntas** que recreara los controles de lectura del profesor.
- **Mayor dolor:** primera vez haciéndolo, sin guía; la IA generaba preguntas dispersas/erróneas hasta que delimitó mejor el contexto.
- **¿Anticipó preguntas?** Parcialmente — de 10 generadas, 1 salió "tan cual" en el control real.
- **Uso de IA (qué falló):** ChatGPT (prefiere sobre Gemini); fricción al afinar el prompt para fiabilidad.
- **¿Comparte/recibe exámenes? (moat):** **el curso permite llevarse los exámenes y él se los transfiere a la IA** para extraer el estilo del profesor.
- **Último que hizo/pagó:** paga ChatGPT Plus (las funciones gratuitas son muy limitadas). Nunca pagó por material humano.
- **Cita:** *"El curso nos permite llevarnos nuestros exámenes y a partir de ellos se los transfiero a la IA… ella extrae el formato o estilo de pregunta que el profesor suele hacer."*
- **¿Confirma/reta hipótesis?** **Confirma fuerte H1, moat y H3.** Es básicamente Rendir.ai hecho a mano.

### Entrevista N°5 — J.S. — economía — jun. 2026
- **Cómo estudió:** clases del profesor + IA para contrastar y aclarar dudas.
- **Mayor dolor:** el **tiempo** — lleva muchos cursos, optimización muy ajustada.
- **¿Anticipó preguntas?** Sí, más o menos: "el profesor tampoco tiene mucha imaginación", segundo examen del mismo curso.
- **Uso de IA (qué falló):** ChatGPT para simplificar lo que explicó el profesor.
- **¿Comparte/recibe exámenes? (moat):** no lo menciona; contrastó método con una compañera.
- **Último que hizo/pagó:** paga Claude Pro (~$20). Lo usa para trabajos finales y resúmenes teóricos/matemáticos.
- **Cita:** *"El profesor toma todo lo que enseña… tengo que recordar bastante rápido lo que enseñó."*
- **¿Confirma/reta hipótesis?** Confirma H1 y H3 (paga IA).

### Entrevista N°6 — J.H. — econometría — jun. 2026
- **Cómo estudió:** material del profesor (lecturas, slides, guías). ~24 h repartidas en 2 semanas.
- **Mayor dolor:** las **demostraciones** que el profesor deja a medias; obligan a repasar temas de cursos pasados ya olvidados.
- **¿Anticipó preguntas?** Sí — vía prácticas dirigidas y guías; preguntas teóricas "explícitamente lo que él dijo en clase".
- **Uso de IA (qué falló):** Gemini para demostraciones; NotebookLM para definiciones y cuestionarios de repaso.
- **¿Comparte/recibe exámenes? (moat):** **compartió todo su material con sus compañeros** para mejor retroalimentación.
- **Último que hizo/pagó:** nada — siguió con slides y apuntes, sin pagar.
- **Cita:** *"Hay preguntas de teoría que son explícitamente lo que él dijo en clase; es acordarse de lo que hizo y dijo."*
- **¿Confirma/reta hipótesis?** Confirma H1 y moat; refuta H3.

### Entrevista N°7 — S. — curso teórico-práctico — jun. 2026
- **Cómo estudió:** apuntes propios + slides del profesor, resaltó lo importante, ejercicios parecidos con NotebookLM. 4–5 h.
- **Mayor dolor:** no saber si domina el concepto y **no saber exactamente qué va a venir** → riesgo de perder tiempo en lo no relevante.
- **¿Anticipó preguntas?** Según cómo plantea el profe sus exámenes pasados y "las fijas" que suelta en las últimas clases.
- **Uso de IA (qué falló):** ChatGPT, Claude y NotebookLM; **límite:** en algunos ejercicios "se va por otra rama" y no resuelve en el contexto correcto.
- **¿Comparte/recibe exámenes? (moat):** exámenes pasados "que normalmente me pasan mis compañeros de ciclos superiores".
- **Último que hizo/pagó:** nada — "nunca he pagado nada y tampoco creo que lo haría".
- **Cita:** *"No sabes exactamente qué te va a venir y puede que estés perdiendo tiempo con algo que quizá no sea tan valioso en el examen."*
- **¿Confirma/reta hipótesis?** Confirma H1 y moat; refuta H3.

---

## Validación de hipótesis

### H1 — Estudian sin saber el estilo del profesor → ansiedad y horas perdidas → ✅ Validada
El patrón es unánime: el mejor predictor que usan es el **examen pasado del profesor**, y el dolor
central es la incertidumbre sobre el estilo de preguntas. S. lo resume: *"no sabes exactamente qué
te va a venir y puede que estés perdiendo tiempo con algo que quizá no sea tan valioso."* Esto es
exactamente lo que Rendir.ai elimina: modelar al docente para anticipar el estilo.

### H2 — La fricción de digitalizar apuntes a mano frena el buen uso de ChatGPT → ⚠️ Parcial
Confirmada de forma explícita por A.: *"como no tengo ChatGPT Pro, no puedo subir bastantes
imágenes."* D. estudia con **fotos de la pizarra**, justo el material que las herramientas genéricas
leen mal. Pero la mayoría ya integra IA a su flujo con fricción menor, así que la fricción de
imágenes es un dolor **real pero acotado**, no universal. → El lector híbrido (Claude visión +
PaddleOCR) ataca este punto, pero **no es el gancho principal**; el gancho es el estilo del profesor.

### H3 — Disposición a pagar → 🟡 Mixta
4/7 nunca pagaron por material y son explícitos ("tampoco creo que lo haría"). Pero **3/7 ya pagan**
~$20/mes por ChatGPT/Claude Plus, y C. pagó Notion. La lectura: **pagan por IA que les ahorra
tiempo**, no por "material de estudio" tradicional. Rendir.ai debe posicionarse como herramienta de
IA (ahorro de horas + mejor nota), no como "resúmenes/material". Modelo freemium o B2B (academias)
sigue siendo lo más prometedor.

### 🏆 Moat — Compartir/heredar exámenes pasados → ✅ Validado fuerte
La señal más contundente del estudio. 4/7 obtuvieron exámenes pasados **de terceros** (compañeros,
ciclos superiores, un amigo que ya llevó el curso). J.V. ya hace una versión manual de Rendir.ai:
*"el curso nos permite llevarnos los exámenes y se los transfiero a la IA… extrae el estilo del
profesor."* Cada examen subido por *(profesor × curso)* mejora la predicción para el siguiente
alumno → el efecto de red que sostiene el moat es **comportamiento real**, no hipótesis.

---

## Implicaciones de producto (next steps)

1. **El gancho es el estilo del profesor, no el OCR.** El OCR híbrido es un *enabler*; el mensaje de
   marketing debe ser "simulacro al estilo de TU profesor".
2. **Sembrar el dataset por *(profesor × curso)*** desde el día 1: pedir a cada usuario subir
   exámenes pasados (ya los comparten orgánicamente). Es el motor del moat.
3. **Posicionar como herramienta de IA premium** (ahorro de tiempo + nota), no como "material". Los
   que pagan, pagan IA.
4. **Competidor real = ChatGPT/NotebookLM manual.** El valor de Rendir.ai es eliminar el trabajo de
   prompt-engineering que hicieron J.V. y otros, y leer bien la foto/pizarra que esas herramientas
   leen mal.
