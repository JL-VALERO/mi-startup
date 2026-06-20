"""Generación de PDF estilo guía académica (LaTeX) para Rendir.ai.

Toma un CUERPO LaTeX (lo redacta Claude), lo envuelve en un preámbulo fijo que
reproduce el estilo de `Instrucciones/ejemplo.pdf` (portada con metadatos, índice,
encabezados, cajas de respuesta verdes, tablas booktabs) y lo compila a PDF con
la instalación local de LaTeX (MiKTeX/TeX Live).

Es una utilidad LOCAL: si no hay un motor LaTeX en el PATH, `build_pdf` levanta
`LatexNotAvailable` para que el endpoint degrade limpio (el deploy no trae LaTeX).
"""
import shutil
import subprocess
import tempfile
from pathlib import Path


class LatexNotAvailable(RuntimeError):
    """No hay un motor LaTeX (latexmk/pdflatex) en el PATH."""


class LatexCompileError(RuntimeError):
    """La compilación LaTeX falló; el mensaje trae el tail del log."""


# Preámbulo fijo que imita el estilo del ejemplo (azul en títulos, cajas verdes
# de respuesta, encabezado/pie, tablas booktabs). El cuerpo de Claude sólo usa
# los entornos definidos aquí.
PREAMBLE = r"""
\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[spanish,es-noquoting]{babel}
\usepackage[a4paper,margin=2.4cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{array}
\usepackage{xcolor}
\usepackage[most]{tcolorbox}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}

\definecolor{azultitulo}{RGB}{20,58,110}
\definecolor{verderesp}{RGB}{82,156,86}
\definecolor{verdefondo}{RGB}{228,243,228}

\titleformat{\section}{\color{azultitulo}\Large\bfseries}{\thesection.}{0.6em}{}
\titleformat{\subsection}{\color{azultitulo}\large\bfseries}{\thesubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{1.4em}{0.7em}

\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{azultitulo}\bfseries \cursohdr}
\fancyhead[R]{\small\color{azultitulo} \temahdr}
\fancyfoot[C]{\small\thepage}
\renewcommand{\headrulewidth}{0.4pt}

% Caja verde de respuesta destacada (como en el ejemplo).
\newtcolorbox{respuesta}{colback=verdefondo,colframe=verderesp,boxrule=1pt,
  arc=2pt,left=8pt,right=8pt,top=6pt,bottom=6pt}
% Caja sobria para marco teórico / notas.
\newtcolorbox{teoria}{colback=white,colframe=azultitulo!70,boxrule=0.6pt,
  arc=2pt,left=8pt,right=8pt,top=6pt,bottom=6pt}

\newcommand{\cursohdr}{CURSO}
\newcommand{\temahdr}{TEMA}
"""


def _escape(s: str) -> str:
    """Escapa metadatos (no el cuerpo, que es LaTeX crudo de Claude)."""
    repl = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
        "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(c, c) for c in s)


def _titlepage(meta: dict) -> str:
    curso = _escape(meta.get("curso") or "Curso")
    profesor = _escape(meta.get("profesor") or "Docente")
    temas = _escape(meta.get("temas") or "—")
    periodo = _escape(meta.get("periodo") or "2026-1")
    universidad = _escape(meta.get("universidad") or "Universidad")
    titulo = _escape(meta.get("titulo") or "Simulacro de Examen")
    return rf"""
\renewcommand{{\cursohdr}}{{{curso}}}
\renewcommand{{\temahdr}}{{Simulacro al estilo del profesor}}
\begin{{titlepage}}
\centering
{{\color{{azultitulo}}\rule{{\linewidth}}{{1.5pt}}}}\\[1.2em]
{{\color{{azultitulo}}\Huge\bfseries {titulo}\par}}
\vspace{{0.4em}}
{{\color{{azultitulo}}\rule{{\linewidth}}{{1.5pt}}}}\\[2.5em]
{{\Large\bfseries Generado al estilo de preguntas del profesor}}\\[3em]
\begin{{flushleft}}\large
\begin{{tabular}}{{@{{}}ll@{{}}}}
\textbf{{Curso:}} & {curso}\\[4pt]
\textbf{{Profesor:}} & {profesor}\\[4pt]
\textbf{{Temas:}} & {temas}\\[4pt]
\textbf{{Periodo:}} & {periodo}\\[4pt]
\textbf{{Universidad:}} & {universidad}\\
\end{{tabular}}
\end{{flushleft}}
\vfill
{{\small\color{{gray}} Rendir.ai · Simulacro al estilo de tu profesor}}
\end{{titlepage}}
"""


def assemble_tex(latex_body: str, meta: dict) -> str:
    """Documento LaTeX completo: preámbulo + portada + índice + cuerpo."""
    return (
        PREAMBLE
        + "\n\\begin{document}\n"
        + _titlepage(meta)
        + "\\tableofcontents\n\\newpage\n"
        + latex_body
        + "\n\\end{document}\n"
    )


def _engine() -> list[str]:
    # pdflatex primero: no requiere Perl (latexmk en MiKTeX suele fallar sin Perl).
    if shutil.which("pdflatex"):
        return ["pdflatex", "-interaction=nonstopmode", "-halt-on-error"]
    if shutil.which("latexmk"):
        return ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error"]
    raise LatexNotAvailable(
        "No se encontró LaTeX (pdflatex/latexmk). La guía en PDF requiere LaTeX local."
    )


def build_pdf(latex_body: str, meta: dict, timeout: int = 240) -> bytes:
    """Compila el cuerpo LaTeX a PDF y devuelve los bytes."""
    cmd0 = _engine()
    tex = assemble_tex(latex_body, meta)
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "guia.tex").write_text(tex, encoding="utf-8")
        # latexmk hace las pasadas necesarias; pdflatex se corre dos veces (índice).
        runs = 1 if cmd0[0] == "latexmk" else 2
        last = None
        for _ in range(runs):
            last = subprocess.run(
                [*cmd0, "guia.tex"], cwd=d, capture_output=True, text=True,
                timeout=timeout,
            )
        pdf = d / "guia.pdf"
        if not pdf.exists():
            if (d / "guia.log").exists():
                log = (d / "guia.log").read_text(encoding="utf-8", errors="ignore")
            else:
                log = ((last.stdout or "") + (last.stderr or "")) if last else ""
            raise LatexCompileError(log[-1800:])
        return pdf.read_bytes()
