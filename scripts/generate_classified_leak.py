#!/usr/bin/env python3
"""
Classified Leak Document Generator
====================================
Converts a markdown source file into a classified-looking leaked government
document PDF with page-level classification stamps on every page.

Part of the WAFT framework — Teleport Massive creative pipeline.

Usage:
    python generate_classified_leak.py <source.md> [options]

Options:
    --output PATH           Output PDF path (default: same dir as source, .pdf)
    --doc-number TEXT       Document control number (default: OSI-7/INA/2026-331-R)
    --codeword TEXT         Classification codeword (default: [CODEWORD])
    --open                  Open the PDF after generation
    --no-header             Skip per-page classification stamps

Examples:
    python generate_classified_leak.py found-documents-ultimatum-era.md --open
    python generate_classified_leak.py lore.md --doc-number "OSI-7/INA/2026-444-R" --open
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


# Header is assembled by replacing @@PLACEHOLDERS@@ — avoids the brace-escaping
# nightmare of str.format() inside heavy LaTeX. The banner, running stamps, a
# rotated "ink" stamp (eso-pic + tikz, single-pass), a faded registration mark,
# and a Bates-style control number in the corner all combine to read as a
# produced/leaked document rather than a typed manuscript.
LATEX_HEADER_TEMPLATE = r"""
\usepackage{fancyhdr}
\usepackage{xcolor}
\usepackage{eso-pic}
\usepackage{tikz}
\usepackage{etoolbox}
\definecolor{stampred}{rgb}{0.62,0.07,0.07}
\definecolor{batesgray}{rgb}{0.35,0.35,0.35}

% Keep every ASCII-art box / code block intact — never split a box across a
% page break. Wrapping each verbatim in an unbreakable minipage pushes a box
% that won't fit wholesale to the next page instead of cutting it in half.
% (No \nobreak: page breaks are allowed *between* boxes, just not inside one,
% so blocks still pack naturally and don't leave large gaps.)
\BeforeBeginEnvironment{verbatim}{\par\begin{minipage}{\linewidth}}
\AfterEndEnvironment{verbatim}{\end{minipage}\par}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{1.2pt}
\renewcommand{\footrulewidth}{1.2pt}
\fancyhead[C]{\footnotesize\bfseries TOP SECRET//@@CODEWORD@@//ORCON/NOFORN/PROPIN}
\fancyfoot[L]{\scriptsize\ttfamily @@DOCNUM@@}
\fancyfoot[C]{\footnotesize\bfseries TOP SECRET//@@CODEWORD@@//ORCON/NOFORN/PROPIN}
\fancyfoot[R]{\scriptsize Page \thepage}

% --- Rotated faded "ink" stamp on every page (over content) ---
@@STAMPBLOCK@@

% --- Faded registration block, top-right corner of page 1 only ---
\AddToShipoutPictureFG{%
  \ifnum\value{page}=1\relax
    \put(\LenToUnit{0.66\paperwidth},\LenToUnit{0.90\paperheight}){%
      \rotatebox{6}{%
        \setlength{\fboxrule}{1pt}\setlength{\fboxsep}{4pt}%
        \textcolor{stampred}{\framebox{\parbox{1.95in}{\centering\tiny\ttfamily
          OFFICE OF SPECIAL INTELLIGENCE\\REGISTERED DOCUMENT\\
          CONTROL TS-████-████\\COPY ██ OF ██}}}}}%
  \fi}

% --- Bates-style control stamp, bottom-right corner, every page ---
\AddToShipoutPictureFG{%
  \put(\LenToUnit{0.80\paperwidth},\LenToUnit{0.045\paperheight}){%
    \textcolor{batesgray}{\scriptsize\ttfamily
      OSI7-REL-00\ifnum\value{page}<10 0\fi\arabic{page}}}}
"""

# The rotated ink stamp, injected at @@STAMPBLOCK@@ only when stamping is on.
LATEX_STAMP_BLOCK = r"""
\AddToShipoutPictureFG{%
  \put(\LenToUnit{0.30\paperwidth},\LenToUnit{0.44\paperheight}){%
    \begin{tikzpicture}
      \node[rotate=18,draw=stampred,line width=1.6pt,text=stampred,
            font=\sffamily\bfseries\large,inner sep=9pt,opacity=0.50,align=center,
            rounded corners=1pt]
        {@@STAMPLINE1@@\\[2pt]{\small @@STAMPLINE2@@}};
    \end{tikzpicture}}}
"""

PANDOC_DEFAULTS = {
    "pdf_engine": "xelatex",
    "from_format": "markdown-fancy_lists",
    "mainfont": "Courier New",
    "monofont": "Courier New",
    "fontsize": "10pt",
    "linestretch": "1.15",
    "geometry": "margin=1.25in,top=1.6in,bottom=1.6in",
    "papersize": "letter",
}


def build_pdf(
    source_path: Path,
    output_path: Path,
    doc_number: str,
    codeword: str,
    include_header: bool,
    stamp: bool = True,
    stamp_line1: str = "WORKING PAPER",
    stamp_line2: str = "DRAFT --- DO NOT CITE OR DISSEMINATE",
) -> bool:
    """Run pandoc to generate the classified PDF."""

    cmd = [
        "pandoc",
        str(source_path),
        f"--pdf-engine={PANDOC_DEFAULTS['pdf_engine']}",
        f"--from={PANDOC_DEFAULTS['from_format']}",
        f"-V", f"mainfont:{PANDOC_DEFAULTS['mainfont']}",
        f"-V", f"monofont:{PANDOC_DEFAULTS['monofont']}",
        f"-V", f"fontsize:{PANDOC_DEFAULTS['fontsize']}",
        f"-V", f"linestretch:{PANDOC_DEFAULTS['linestretch']}",
        f"-V", f"geometry:{PANDOC_DEFAULTS['geometry']}",
        f"-V", f"papersize:{PANDOC_DEFAULTS['papersize']}",
        "-V", "colorlinks:false",
        "-o", str(output_path),
    ]

    if include_header:
        stamp_block = ""
        if stamp:
            stamp_block = (
                LATEX_STAMP_BLOCK
                .replace("@@STAMPLINE1@@", stamp_line1)
                .replace("@@STAMPLINE2@@", stamp_line2)
            )
        header_content = (
            LATEX_HEADER_TEMPLATE
            .replace("@@CODEWORD@@", codeword)
            .replace("@@DOCNUM@@", doc_number)
            .replace("@@STAMPBLOCK@@", stamp_block)
        )
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".tex", delete=False, prefix="classified_header_"
        ) as f:
            f.write(header_content)
            header_path = f.name

        cmd += ["--include-in-header", header_path]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"[ERROR] pandoc failed:\n{result.stderr}", file=sys.stderr)
        return False

    if result.stderr:
        for line in result.stderr.splitlines():
            if "Missing character" not in line:
                print(f"[WARN] {line}", file=sys.stderr)

    return True


def open_pdf(path: Path) -> None:
    """Open the PDF with the system default viewer."""
    import platform
    if platform.system() == "Darwin":
        subprocess.run(["open", str(path)])
    elif platform.system() == "Linux":
        subprocess.run(["xdg-open", str(path)])
    else:
        subprocess.run(["start", str(path)], shell=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate a classified-looking leaked document PDF from markdown.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("source", help="Source markdown file path")
    parser.add_argument("--output", help="Output PDF path")
    parser.add_argument(
        "--doc-number",
        default="OSI-7/INA/2026-331-R",
        help="Document control number for footer (default: OSI-7/INA/2026-331-R)",
    )
    parser.add_argument(
        "--codeword",
        default="FISHBOWL",
        help="Classification codeword for header/footer stamps (default: FISHBOWL)",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the PDF after generation",
    )
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="Skip per-page classification stamps",
    )
    parser.add_argument(
        "--no-stamp",
        action="store_true",
        help="Skip the rotated red ink stamp (keeps banners/Bates marks)",
    )
    parser.add_argument(
        "--stamp-line1",
        default="WORKING PAPER",
        help="Top line of the rotated ink stamp (default: WORKING PAPER)",
    )
    parser.add_argument(
        "--stamp-line2",
        default="DRAFT --- DO NOT CITE OR DISSEMINATE",
        help="Bottom line of the rotated ink stamp",
    )
    args = parser.parse_args()

    source_path = Path(args.source).expanduser().resolve()
    if not source_path.exists():
        print(f"[ERROR] Source file not found: {source_path}", file=sys.stderr)
        return 1

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
    else:
        output_path = source_path.with_suffix(".pdf")

    print(f"[INFO] Source:     {source_path}")
    print(f"[INFO] Output:     {output_path}")
    print(f"[INFO] Doc number: {args.doc_number}")
    print(f"[INFO] Codeword:   {args.codeword}")
    print(f"[INFO] Banners:    {'off' if args.no_header else 'on'}")
    print(f"[INFO] Ink stamp:  {'off' if args.no_stamp else args.stamp_line1}")
    print()

    success = build_pdf(
        source_path=source_path,
        output_path=output_path,
        doc_number=args.doc_number,
        codeword=args.codeword,
        include_header=not args.no_header,
        stamp=not args.no_stamp,
        stamp_line1=args.stamp_line1,
        stamp_line2=args.stamp_line2,
    )

    if not success:
        return 1

    size_kb = output_path.stat().st_size // 1024
    print(f"[OK]   PDF generated: {output_path} ({size_kb}K)")

    if args.open:
        open_pdf(output_path)
        print(f"[OK]   Opened in system viewer.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
