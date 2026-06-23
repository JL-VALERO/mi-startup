# Backend de Rendir.ai con LaTeX, para que /generate_pdf (guía en PDF) funcione
# también en el deploy (Render), no solo en local.
#
# Construye desde rootDir=backend (ver render.yaml). Incluye pdflatex + los
# paquetes que usa el preámbulo de la guía (article, babel-spanish, geometry,
# amsmath, booktabs, xcolor, tcolorbox[most], fancyhdr, titlesec, enumitem,
# hyperref). PaddleOCR sigue fuera del deploy (corre en local).
FROM python:3.11-slim

# LaTeX (pdflatex) + colecciones necesarias. `--no-install-recommends` para no
# inflar la imagen; el build falla ruidosamente si pdflatex no quedó disponible.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      texlive-latex-base \
      texlive-latex-recommended \
      texlive-latex-extra \
      texlive-fonts-recommended \
      texlive-lang-spanish \
 && rm -rf /var/lib/apt/lists/* \
 && pdflatex --version

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./

# Render inyecta el puerto en $PORT.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]
