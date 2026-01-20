"""
LaTeX Compiler
==============

Handles compilation of LaTeX documents to PDF using pdflatex or xelatex.
"""

import shutil
import subprocess
import tempfile
from pathlib import Path


class LaTeXCompiler:
    """Compiles LaTeX documents to PDF."""

    def __init__(self, compiler: str = "pdflatex"):
        """
        Initialize LaTeX compiler.

        Args:
            compiler: LaTeX compiler to use ("pdflatex" or "xelatex")
        """
        self.compiler = compiler
        self._check_compiler_available()

    def _check_compiler_available(self) -> None:
        """Check if LaTeX compiler is available."""
        if not shutil.which(self.compiler):
            raise RuntimeError(
                f"LaTeX compiler '{self.compiler}' not found. "
                f"Please install a LaTeX distribution (e.g., TeX Live, MiKTeX)."
            )

    def compile(
        self,
        latex_content: str,
        output_path: Path,
        working_dir: Path | None = None,
        runs: int = 2,
    ) -> Path:
        """
        Compile LaTeX content to PDF.

        Args:
            latex_content: LaTeX source code as string
            output_path: Where to save the PDF
            working_dir: Working directory for compilation (uses temp dir if None)
            runs: Number of compilation runs (needed for references, TOC, etc.)

        Returns:
            Path to generated PDF

        Raises:
            RuntimeError: If compilation fails
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Use temp directory if not specified
        if working_dir is None:
            with tempfile.TemporaryDirectory() as tmpdir:
                return self._compile_in_dir(latex_content, output_path, Path(tmpdir), runs)
        else:
            return self._compile_in_dir(latex_content, output_path, working_dir, runs)

    def _compile_in_dir(
        self, latex_content: str, output_path: Path, working_dir: Path, runs: int
    ) -> Path:
        """Compile LaTeX in a specific directory."""
        # Write LaTeX content to main.tex
        main_tex = working_dir / "main.tex"
        main_tex.write_text(latex_content, encoding="utf-8")

        # Compile multiple times for references, TOC, etc.
        for run in range(runs):
            result = subprocess.run(
                [
                    self.compiler,
                    "-interaction=nonstopmode",
                    "-output-directory",
                    str(working_dir),
                    str(main_tex),
                ],
                cwd=working_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                error_msg = result.stderr or result.stdout
                raise RuntimeError(f"LaTeX compilation failed (run {run + 1}/{runs}):\n{error_msg}")

        # Find generated PDF
        pdf_path = working_dir / "main.pdf"
        if not pdf_path.exists():
            raise RuntimeError(f"PDF not generated: {pdf_path} not found after compilation")

        # Copy to output path
        shutil.copy2(pdf_path, output_path)

        return output_path

    def compile_file(self, tex_file: Path, output_path: Path, runs: int = 2) -> Path:
        """
        Compile a LaTeX file to PDF.

        Args:
            tex_file: Path to .tex file
            output_path: Where to save the PDF
            runs: Number of compilation runs

        Returns:
            Path to generated PDF
        """
        tex_file = Path(tex_file)
        if not tex_file.exists():
            raise FileNotFoundError(f"LaTeX file not found: {tex_file}")

        latex_content = tex_file.read_text(encoding="utf-8")
        working_dir = tex_file.parent

        return self.compile(latex_content, output_path, working_dir, runs)
