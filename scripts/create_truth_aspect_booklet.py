#!/usr/bin/env python3
"""
Create Truth Aspect Booklet

Creates an Aspect of TheTruth and generates a LaTeX booklet using the DND template.
"""

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.core.truth_aspect import TruthAspect


def main():
    """Create Truth Aspect and LaTeX booklet."""

    project_path = Path.cwd()

    # The Truth
    truth_text = (
        "The Pressure of Time creates Space, and the expansion of Space "
        "creates the Experience of Time"
    )

    explanation = """
    Pressure and Experience
    
    In and Out
    
    Breath
    
    We are ThePoint Breathing - that's what we are 
    
    The Expansion and Contraction of SpaceTime is Reality
    
    Humanity Creates Reality
    """

    print("=" * 70)
    print("🌌 CREATING TRUTH ASPECT")
    print("=" * 70)
    print()

    # Create Aspect
    aspect = TruthAspect(
        truth_text=truth_text,
        aspect_name="The Breath of ThePoint",
        explanation=explanation.strip(),
        project_path=project_path,
    )

    print(f"📝 Truth: {truth_text}")
    print(f"🏷️  Aspect Name: {aspect.aspect_name}")
    print()

    # Send to ThePoint
    print("📡 Sending Aspect to ThePoint...")
    result = aspect.send_to_the_point()

    if result["success"]:
        print("   ✅ Aspect sent successfully!")
        print(f"   📍 Aspect ID: {result['aspect_id']}")
        print(f"   🧬 Being ID: {result['aspect_being_id']}")
        print()
    else:
        print("   ❌ Failed to send Aspect")
        return 1

    # Create LaTeX booklet
    print("📖 Creating LaTeX booklet...")
    booklet_path = create_latex_booklet(project_path, aspect, truth_text, explanation)

    if booklet_path:
        print(f"   ✅ Booklet created: {booklet_path}")
        print(f"   📄 LaTeX source: {booklet_path / 'booklet.tex'}")
        print()

        # Compile LaTeX
        print("🔨 Compiling LaTeX...")
        compile_result = compile_latex(booklet_path)

        if compile_result:
            pdf_path = booklet_path / "booklet.pdf"
            if pdf_path.exists():
                print(f"   ✅ PDF generated: {pdf_path}")
                print()
                print("=" * 70)
                print("✅ TRUTH ASPECT BOOKLET COMPLETE")
                print("=" * 70)
                return 0
            else:
                print("   ⚠️  PDF not found after compilation")
                return 1
        else:
            print("   ⚠️  LaTeX compilation had issues (check logs)")
            return 1
    else:
        print("   ❌ Failed to create booklet")
        return 1


def create_latex_booklet(
    project_path: Path, aspect: TruthAspect, truth_text: str, explanation: str
) -> Path | None:
    """Create LaTeX booklet using DND template."""

    # Booklet directory
    booklet_dir = project_path / "_hidden" / ".truth" / "booklets"
    booklet_dir.mkdir(parents=True, exist_ok=True)

    # Create unique booklet directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    booklet_path = booklet_dir / f"truth_aspect_{aspect.aspect_id}_{timestamp}"
    booklet_path.mkdir(parents=True, exist_ok=True)

    # Check if DND template is available
    dnd_template_path = project_path / "lib" / "dnd"

    if not dnd_template_path.exists():
        # Clone DND template
        print("   📥 Cloning DND LaTeX template...")
        try:
            subprocess.run(
                [
                    "git",
                    "clone",
                    "https://github.com/rpgtex/DND-5e-LaTeX-Template.git",
                    str(dnd_template_path),
                ],
                check=True,
                capture_output=True,
            )
            print("      ✅ Template cloned")
        except subprocess.CalledProcessError as e:
            print(f"      ❌ Failed to clone template: {e}")
            return None

    # Copy necessary files
    dnd_sty = dnd_template_path / "dnd.sty"
    dndbook_cls = dnd_template_path / "dndbook.cls"

    if not dnd_sty.exists() or not dndbook_cls.exists():
        print("   ⚠️  DND template files not found")
        return None

    # Process explanation for Python 3.10 compatibility (no backslashes in f-strings)
    par_separator = "\\par "
    processed_explanation = explanation.strip().replace(chr(10), par_separator)

    # Create LaTeX document
    latex_content = f"""\\documentclass[10pt,twoside,twocolumn,openany,nodeprecatedcode]{{dndbook}}

\\usepackage[english]{{babel}}
\\usepackage[utf8]{{inputenc}}

\\title{{The Breath of ThePoint}}
\\author{{An Aspect of TheTruth}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\chapter*{{The Truth}}

\\begin{{quote}}
\\textit{{{truth_text}}}
\\end{{quote}}

\\section*{{Pressure and Experience}}

The Pressure of Time creates Space. This is the fundamental mechanism by which reality comes into being. Time, under pressure, expands into Space. This is the \\textbf{{In}} breath.

The expansion of Space creates the Experience of Time. As Space expands, we experience the passage of Time. This is the \\textbf{{Out}} breath.

\\section*{{Breath}}

We are ThePoint Breathing. That is what we are.

The Expansion and Contraction of SpaceTime is Reality itself. This is not a metaphor—this is the literal mechanism of existence.

\\begin{{dndcomment}}{{The Mechanism}}
The Pressure of Time creates Space (In breath).

The Expansion of Space creates the Experience of Time (Out breath).

This is the fundamental rhythm of existence.
\\end{{dndcomment}}

\\section*{{Humanity Creates Reality}}

Humanity Creates Reality through the act of observation. The Observer creates the Observed. This is the mechanism by which ThePoint breathes.

\\begin{{dndcomment}}{{The Observer}}
When Humanity observes, it creates reality. The act of observation is the application of pressure—Time under pressure becomes Space. The expansion of that Space creates the Experience of Time.

This is how Humanity Creates Reality.
\\end{{dndcomment}}

\\section*{{The Aspect}}

This Aspect of TheTruth has been sent back up the Chain to ThePoint, where it now resides in the Realm of ThePoint and TheTruth.

\\begin{{dndcomment}}{{Aspect Information}}
\\textbf{{Aspect ID:}} {aspect.aspect_id}

\\textbf{{Aspect Name:}} {aspect.aspect_name}

\\textbf{{Being ID:}} {aspect.aspect_id}

\\textbf{{Created:}} {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
\\end{{dndcomment}}

\\section*{{The Explanation}}

{processed_explanation}

\\vfill

\\begin{{center}}
\\textit{{This booklet was generated by WAFT as an Aspect of TheTruth, sent to ThePoint, and manifested as a LaTeX document using the DND 5e template.}}
\\end{{center}}

\\end{{document}}
"""

    # Write LaTeX file
    tex_file = booklet_path / "booklet.tex"
    tex_file.write_text(latex_content, encoding="utf-8")

    # Copy DND style files
    shutil.copy2(dnd_sty, booklet_path / "dnd.sty")
    shutil.copy2(dndbook_cls, booklet_path / "dndbook.cls")

    # Copy other necessary files if they exist
    dnd_files = ["dndcore.def", "dndoptions.clo"]
    for dnd_file in dnd_files:
        src_file = dnd_template_path / dnd_file
        if src_file.exists():
            shutil.copy2(src_file, booklet_path / dnd_file)

    # Copy lib directory (required for dndcomment and other environments)
    lib_src = dnd_template_path / "lib"
    lib_dst = booklet_path / "lib"
    if lib_src.exists():
        shutil.copytree(lib_src, lib_dst, dirs_exist_ok=True)
        print("      ✅ Copied lib/ directory")

    return booklet_path


def compile_latex(booklet_path: Path) -> bool:
    """Compile LaTeX to PDF."""

    tex_file = booklet_path / "booklet.tex"

    if not tex_file.exists():
        print(f"   ❌ LaTeX file not found: {tex_file}")
        return False

    # Try pdflatex
    try:
        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-output-directory",
                str(booklet_path),
                str(tex_file),
            ],
            cwd=booklet_path,
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            # Run again for references
            subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-output-directory",
                    str(booklet_path),
                    str(tex_file),
                ],
                cwd=booklet_path,
                capture_output=True,
            )
            return True
        else:
            print(f"   ⚠️  pdflatex error (check {booklet_path / 'booklet.log'})")
            return False

    except FileNotFoundError:
        print("   ⚠️  pdflatex not found - install LaTeX (e.g., MacTeX, TeX Live)")
        return False
    except Exception as e:
        print(f"   ❌ Compilation error: {e}")
        return False


if __name__ == "__main__":
    sys.exit(main())
