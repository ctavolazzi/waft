#!/usr/bin/env python3
"""
Classified Document Builder
===========================
Build "leaked classified government document" PDFs entirely from code.

This is the programmatic companion to ``generate_classified_leak.py`` (which
renders markdown -> stamped PDF). This module supplies the piece that was
previously hand-crafted: guaranteed-aligned ASCII-art boxes (SF-703 cover
sheets, routing slips, classification banners, authority blocks, end-of-
document boxes) plus a fluent ``ClassifiedDocument`` builder that assembles
boxes + portion-marked prose into markdown and renders it through the existing
PDF pipeline (banners, rotated ink stamp, Bates numbers, non-breaking boxes).

Why a builder instead of hand-written markdown:
  * Box borders only line up if every row has the exact same codepoint count.
    Courier New is true monospace, so ``len(line)`` == rendered width. The
    ``Box`` class pads every row to an identical width by construction, so a
    box can never come out ragged.
  * Boxes are emitted as fenced code blocks; the renderer wraps each in a
    non-breaking minipage so they never split across a page.

Usage (CLI):
    python classified_doc_builder.py demo [--open]   # build + render a sample
    python classified_doc_builder.py boxes           # print the boxes to stdout

Usage (API):
    from classified_doc_builder import ClassifiedDocument, cover_sheet
    doc = ClassifiedDocument(codeword="FISHBOWL", doc_number="OSI-7/INA/2026-331-R")
    doc.heading("DOCUMENT 007", level=2).box(cover_sheet()).section("KEY JUDGMENTS")
    doc.render("/tmp/out.pdf", open_after=True)
"""

import argparse
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Import build_pdf from the sibling renderer (filename import; no package req).
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_RENDERER = _HERE / "generate_classified_leak.py"


def _load_renderer():
    spec = importlib.util.spec_from_file_location("generate_classified_leak", _RENDERER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# Box drawing — equal-width by construction.
# ---------------------------------------------------------------------------
SINGLE = {"tl": "┌", "tr": "┐", "bl": "└", "br": "┘", "h": "─", "v": "│"}
DOUBLE = {"tl": "╔", "tr": "╗", "bl": "╚", "br": "╝", "h": "═", "v": "║"}


def R(n: int) -> str:
    """A redaction bar of width ``n`` (solid block; 1 cell each in Courier)."""
    return "█" * n


class Box:
    """An ASCII-art box whose every row is exactly ``width + 2`` cells wide.

    ``width`` is the inner content width (between the vertical borders). Every
    helper pads to that width, so borders are guaranteed to align. Methods
    return ``self`` for chaining.
    """

    def __init__(self, width: int, style: dict = SINGLE):
        self.w = width
        self.s = style
        self.lines: list[str] = []

    def _row(self, inner: str) -> str:
        if len(inner) > self.w:
            raise ValueError(f"row too wide ({len(inner)} > {self.w}): {inner!r}")
        return self.s["v"] + inner + " " * (self.w - len(inner)) + self.s["v"]

    def top(self):
        self.lines.append(self.s["tl"] + self.s["h"] * self.w + self.s["tr"])
        return self

    def bottom(self):
        self.lines.append(self.s["bl"] + self.s["h"] * self.w + self.s["br"])
        return self

    def blank(self):
        self.lines.append(self._row(""))
        return self

    def center(self, text: str):
        self.lines.append(self._row(text.center(self.w)))
        return self

    def left(self, text: str, indent: int = 2):
        self.lines.append(self._row(" " * indent + text))
        return self

    def rule(self, char: str = "─", indent: int = 0):
        self.lines.append(self._row(" " * indent + char * (self.w - 2 * indent)))
        return self

    def embed(self, child: "Box", indent: int = 3):
        """Nest another box inside this one (its rows become left content)."""
        for line in child.render_lines():
            self.left(line, indent=indent)
        return self

    def render_lines(self) -> list[str]:
        return list(self.lines)

    def render(self) -> str:
        return "\n".join(self.lines)

    def assert_aligned(self) -> "Box":
        widths = {len(line) for line in self.lines}
        if len(widths) > 1:
            raise AssertionError(f"box is ragged, row widths = {sorted(widths)}")
        return self


# ---------------------------------------------------------------------------
# Pre-built classified elements (reproduce the Ultimatum Era document).
# ---------------------------------------------------------------------------
def cover_sheet(doc_number: str = "OSI-7/INA/2026-331-R", inner: int = 64,
                nested: int = 54, access_rows: int = 4) -> Box:
    """SF-703-style TOP SECRET document cover sheet."""
    b = Box(inner, DOUBLE).top()
    b.center("TOP SECRET").blank()
    b.center("TOP SECRET DOCUMENT COVER SHEET")
    b.center("(THIS SHEET UNCLASSIFIED)").blank()
    b.left(f"ATTACHED DOCUMENT:  {doc_number}", indent=3)
    b.left(f"TS CONTROL NUMBER:  TS-{R(4)}-{R(4)}-{R(4)}", indent=3)
    b.left(f"COPY {R(2)} OF {R(2)}   REGISTERED TO READER {R(10)}", indent=3)
    b.blank()
    nb = Box(nested, SINGLE).top()
    nb.left("ACCESS RECORD — EACH READER ENTERS NAME & DATE", indent=2)
    for _ in range(access_rows):
        nb.left(f"{R(28)}   [REDACTED]", indent=2)
    nb.bottom()
    b.embed(nb, indent=3).blank()
    b.left("STANDARD FORM 703 (REV.) — EO 13526 / 32 CFR 2001", indent=3)
    b.center("TOP SECRET").bottom()
    return b.assert_aligned()


def routing_slip(inner: int = 65, routed_to: int = 3) -> Box:
    """ACTION ROUTING SLIP — EYES ONLY."""
    b = Box(inner, SINGLE).top()
    b.center("ACTION ROUTING SLIP — EYES ONLY")
    b.left(f"ORIGINATING ANALYST:  {R(16)}   (OSI-7, TIER-4)")
    b.left(f"ROUTED TO:            {R(16)}   (OSI-7, DIV. CHIEF)")
    for _ in range(routed_to - 1):
        b.left(f"                      {R(16)}   ([REDACTED])")
    b.left(f"COPY:                 {R(32)}")
    b.left("ACTION REQUIRED BY:   [REDACTED]")
    b.left("OPSEC REVIEW:         PENDING — HOLD UNTIL CLEARED")
    b.left("STATUS:               DRAFT / AWAITING DIV. CHIEF APPROVAL")
    b.left("NOTE: Do not reproduce this routing slip with the")
    b.left("      document. File under OSI-7/ROUTING/2026-331.")
    b.bottom()
    return b.assert_aligned()


def end_box(doc_number: str, codeword: str, inner: int = 65) -> Box:
    """END OF DOCUMENT banner box."""
    b = Box(inner, DOUBLE).top()
    b.center(f"END OF DOCUMENT — {doc_number}")
    b.center(f"TOP SECRET//{codeword}//ORCON/NOFORN/PROPIN")
    b.center("DO NOT REPRODUCE — DO NOT RETAIN — DO NOT DISCUSS")
    b.center("OUTSIDE SCI READ-IN CHANNELS")
    b.bottom()
    return b.assert_aligned()


def memo_header(codeword: str, doc_number: str, subject: str) -> str:
    """Plain (non-boxed) memorandum letterhead, returned as code-block text."""
    return "\n".join([
        "                    OFFICE OF SPECIAL INTELLIGENCE",
        "                 DIVISION 7 — SPECIAL ACCESS PROGRAMS",
        f"              {R(8)} FEDERAL ANNEX · WASHINGTON, D.C. 20{R(3)}",
        "",
        "                                              DATE:  [REDACTED]",
        "                                              IN REPLY REFER TO:",
        f"                                              {doc_number}",
        "",
        "MEMORANDUM FOR:  [REDACTED], DEPUTY DIRECTOR FOR [REDACTED]",
        "THROUGH:         [REDACTED], DIVISION CHIEF, OSI-7",
        "FROM:            [REDACTED], Senior Analyst (Tier-4 Read-In)",
        f"SUBJECT:         (U) {subject}",
        "REFERENCES:      (a) (U) OSI-7/FISHBOWL/Standing Directive",
        "                 (b) (S) [REDACTED]",
    ])


# ---------------------------------------------------------------------------
# Document builder.
# ---------------------------------------------------------------------------
class ClassifiedDocument:
    """Fluent builder that accumulates markdown and renders a stamped PDF."""

    def __init__(self, codeword: str = "FISHBOWL",
                 doc_number: str = "OSI-7/INA/2026-331-R", title: str | None = None):
        self.codeword = codeword
        self.doc_number = doc_number
        self.title = title
        self._fm: dict[str, str] = {}
        self._blocks: list[str] = []

    # -- structural --------------------------------------------------------
    def frontmatter(self, **kw):
        self._fm.update({k: str(v) for k, v in kw.items()})
        return self

    def raw(self, md: str):
        self._blocks.append(md)
        return self

    def hr(self):
        self._blocks.append("---")
        return self

    def heading(self, text: str, level: int = 2):
        self._blocks.append("#" * level + " " + text)
        return self

    def para(self, text: str):
        self._blocks.append(text)
        return self

    def italic(self, text: str):
        self._blocks.append(f"*{text}*")
        return self

    def code(self, text: str):
        self._blocks.append("```\n" + text + "\n```")
        return self

    # -- classified elements ----------------------------------------------
    def box(self, b: Box):
        return self.code(b.render())

    def banner(self):
        return self.code(f"TOP SECRET//{self.codeword}//ORCON/NOFORN/PROPIN")

    def memo(self, subject: str):
        return self.code(memo_header(self.codeword, self.doc_number, subject))

    def section(self, name: str):
        self._blocks.append(f"**{name}** `(TS//SCI//{self.codeword})`")
        return self

    def portion(self, level: str, text: str):
        """A portion-marked paragraph, e.g. portion('TS//SCI//FISHBOWL', '...')."""
        self._blocks.append(f"({level}) {text}")
        return self

    def key_judgment(self, confidence: str, text: str):
        self._blocks.append(
            f"(TS//SCI//{self.codeword}) **We assess with {confidence}** {text}")
        return self

    def authority_block(self):
        body = "\n".join([
            "─" * 65,
            "CLASSIFICATION AUTHORITY BLOCK",
            "─" * 65,
            f"Classified By:   {R(16)}, Senior Analyst, OSI-7 (Tier-4)",
            "Derived From:    Multiple Sources (see Enclosure 1)",
            "Declassify On:   25X1",
            "─" * 65,
            "DECLASSIFICATION EXEMPTION NOTE (U):",
            "  25X1 invoked under EO 13526 Sec. 3.3(b)(1) — the exempting",
            "  category includes, verbatim, \"a non-human intelligence source.\"",
            "─" * 65,
        ])
        return self.code(body)

    def end(self):
        return self.box(end_box(self.doc_number, self.codeword))

    # -- output ------------------------------------------------------------
    def to_markdown(self) -> str:
        parts: list[str] = []
        if self._fm:
            fm = "\n".join(f"{k}: {v}" for k, v in self._fm.items())
            parts.append(f"---\n{fm}\n---")
        if self.title:
            parts.append(f"# {self.title}")
        parts.extend(self._blocks)
        return "\n\n".join(parts) + "\n"

    def render(self, out_pdf: str | Path, open_after: bool = False,
               stamp: bool = True, stamp_line1: str = "WORKING PAPER",
               stamp_line2: str = "DRAFT --- DO NOT CITE OR DISSEMINATE") -> Path:
        out_pdf = Path(out_pdf).expanduser().resolve()
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        renderer = _load_renderer()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, prefix="classified_doc_"
        ) as f:
            f.write(self.to_markdown())
            md_path = Path(f.name)
        ok = renderer.build_pdf(
            source_path=md_path, output_path=out_pdf,
            doc_number=self.doc_number, codeword=self.codeword,
            include_header=True, stamp=stamp,
            stamp_line1=stamp_line1, stamp_line2=stamp_line2,
        )
        if not ok:
            raise RuntimeError("PDF render failed (see pandoc output above)")
        if open_after:
            opener = {"darwin": "open", "linux": "xdg-open"}.get(sys.platform, "open")
            subprocess.run([opener, str(out_pdf)])
        return out_pdf


# ---------------------------------------------------------------------------
# Demo: assemble a complete sample document entirely from code.
# ---------------------------------------------------------------------------
def build_demo() -> ClassifiedDocument:
    doc = ClassifiedDocument(
        codeword="FISHBOWL",
        doc_number="OSI-7/INA/2026-331-R",
        title="Found Documents — Builder Demo",
    )
    doc.frontmatter(version="0.0.1", status="demo")
    doc.italic("Generated entirely from code by classified_doc_builder.py. "
               "Every box below is aligned by construction.")
    doc.hr()
    doc.heading("DOCUMENT 007", level=2)
    doc.heading("Inter-Agency Assessment — Classified Distribution", level=3)
    doc.box(routing_slip())
    doc.box(cover_sheet())
    doc.banner()
    doc.memo("Status Assessment — Autonomous Research Vectors")
    doc.hr()
    doc.section("KEY JUDGMENTS")
    doc.key_judgment("HIGH CONFIDENCE",
                     "the primary research vector will reach operational "
                     "capability within the reporting window.")
    doc.key_judgment("MODERATE CONFIDENCE",
                     "operationalization will be observable to outside parties "
                     "at or near the moment of first success.")
    doc.key_judgment("LOW CONFIDENCE",
                     "the response will fall within previously observed "
                     "tolerance — flagged for senior attention precisely "
                     "because our confidence is low.")
    doc.hr()
    doc.section("SECTION I — SUMMARY")
    doc.portion("TS//SCI//FISHBOWL",
                "This is a portion-marked paragraph. The marker at the start of "
                "the line is real analytic-document syntax and survives the PDF "
                "render unchanged.")
    doc.portion("U", "Unclassified portions are marked (U).")
    doc.hr()
    doc.authority_block()
    doc.end()
    return doc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build classified-looking documents from code.",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = parser.add_subparsers(dest="cmd")

    p_demo = sub.add_parser("demo", help="build + render a sample document")
    p_demo.add_argument("--output", help="output PDF path")
    p_demo.add_argument("--open", action="store_true", help="open after render")

    sub.add_parser("boxes", help="print the standard boxes to stdout")

    args = parser.parse_args()

    if args.cmd == "boxes":
        for title, b in [("ROUTING SLIP", routing_slip()),
                         ("COVER SHEET", cover_sheet()),
                         ("END OF DOCUMENT", end_box("OSI-7/INA/2026-331-R", "FISHBOWL"))]:
            print(f"\n===== {title} =====")
            print(b.render())
        return 0

    if args.cmd == "demo":
        out = args.output or (_HERE.parent / "_examples_output" / "classified_leak_demo.pdf")
        print("[INFO] Building demo document from code…")
        doc = build_demo()
        path = doc.render(out, open_after=args.open)
        print(f"[OK]   Rendered: {path} ({path.stat().st_size // 1024}K)")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
