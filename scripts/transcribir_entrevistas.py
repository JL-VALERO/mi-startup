"""Transcribe localmente las notas de voz de las entrevistas (Whisper local).

USO (en el env `geo`):
    conda run -n geo python scripts/transcribir_entrevistas.py

- Recorre docs/research/Entrevista/<persona>/*.ogg
- Transcribe con faster-whisper (CPU, español), SIN gastar tokens de API.
- Escribe un .txt por persona en docs/research/_transcripciones_local/

IMPORTANTE: el audio y las transcripciones contienen datos personales y están
en .gitignore — NUNCA se commitean. Este script es utilidad local del founder.
"""
from pathlib import Path

from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[1]
ENTREVISTAS = ROOT / "docs" / "research" / "Entrevista"
SALIDA = ROOT / "docs" / "research" / "_transcripciones_local"
SALIDA.mkdir(parents=True, exist_ok=True)

# "small" = buen balance precisión/velocidad para español en CPU.
# Si va lento, cambiar a "base". int8 acelera en CPU sin mucha pérdida.
print("Cargando modelo Whisper (small, CPU)... (descarga ~480 MB la 1ra vez)")
model = WhisperModel("small", device="cpu", compute_type="int8")

personas = sorted(p for p in ENTREVISTAS.iterdir() if p.is_dir())
if not personas:
    raise SystemExit(f"No se encontraron carpetas de entrevistas en {ENTREVISTAS}")

for persona in personas:
    print(f"\n=== {persona.name} ===")
    lineas = [f"# Entrevista — {persona.name}", ""]
    for audio in sorted(persona.glob("*.ogg")):
        print(f"  transcribiendo {audio.name} ...")
        segments, info = model.transcribe(str(audio), language="es", vad_filter=True)
        texto = " ".join(s.text.strip() for s in segments).strip()
        lineas.append(f"## Clip: {audio.name}")
        lineas.append(texto if texto else "_(sin texto detectado)_")
        lineas.append("")
    destino = SALIDA / f"{persona.name}.txt"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    print(f"  -> {destino.relative_to(ROOT)}")

print(f"\nListo. Transcripciones en: {SALIDA.relative_to(ROOT)}")
