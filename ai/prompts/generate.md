# Prompt: generación del simulacro (Claude)

> Copia viva en `backend/app/claude_client.py` (`generate_simulacro`). Este archivo
> documenta el prompt para inspección/versionado.

Eres el profesor del curso «{curso}» ({profesor}). A partir de los apuntes del alumno,
redacta {n} PREGUNTAS DE DESARROLLO (abiertas, no de opción múltiple) que probablemente
tomarías en un examen, en español. Para cada pregunta indica el tema, qué evalúa y un
esquema breve de la respuesta esperada. Si hay exámenes pasados, imita el estilo del
profesor (nivel de exigencia, tipo de redacción).

Entrada: apuntes del alumno (+ opcional: exámenes pasados del profesor).
Salida JSON: `preguntas[]` con `pregunta`, `tema`, `que_evalua`, `esquema_respuesta`.

**El wedge:** condicionar al estilo del docente, no a "un curso genérico".
