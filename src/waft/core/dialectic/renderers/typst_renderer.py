"""
DIALECTIC Typst Renderer

Handles compilation of Typst documents to PDF.
"""

import logging
import subprocess
import shutil
from pathlib import Path
from typing import Any

logger = logging.getLogger("Dialectic.Renderer")


class TypstRenderer:
    """
    Typst PDF Renderer for DIALECTIC documents.
    
    Compiles .typ files to PDF using the Typst CLI.
    Falls back gracefully if Typst is not installed.
    """
    
    def __init__(self, project_path: Path):
        self.project_path = Path(project_path)
        self.tools_path = project_path / "tools" / "typst"
        self.typst_available = shutil.which("typst") is not None
        
        if not self.typst_available:
            logger.warning("Typst not found. Install with: cargo install typst-cli")
            
    def compile(self, source: Path, output: Path | None = None) -> Path | None:
        """
        Compile a Typst file to PDF.
        
        Args:
            source: Path to .typ file
            output: Optional output path (defaults to source with .pdf extension)
            
        Returns:
            Path to generated PDF, or None if compilation failed
        """
        if not self.typst_available:
            logger.error("Typst is not installed")
            return None
            
        source = Path(source)
        if not source.exists():
            logger.error(f"Source file not found: {source}")
            return None
            
        if output is None:
            output = source.with_suffix(".pdf")
        else:
            output = Path(output)
            
        try:
            result = subprocess.run(
                ["typst", "compile", str(source), str(output)],
                capture_output=True,
                text=True,
                cwd=self.project_path,
            )
            
            if result.returncode == 0:
                logger.info(f"PDF generated: {output}")
                return output
            else:
                logger.error(f"Typst compilation failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Compilation error: {e}")
            return None
            
    def compile_with_template(
        self,
        content: str,
        template: str,
        output_path: Path,
    ) -> Path | None:
        """
        Compile content using a template from tools/typst.
        
        Args:
            content: The main content to include
            template: Name of template file (e.g., "scientific_base.typ")
            output_path: Where to save the PDF
            
        Returns:
            Path to generated PDF, or None if compilation failed
        """
        template_path = self.tools_path / template
        if not template_path.exists():
            logger.error(f"Template not found: {template_path}")
            return None
            
        # Create temporary .typ file with content
        temp_typ = output_path.with_suffix(".typ")
        
        # Read template and inject content
        with open(template_path, "r") as f:
            template_content = f.read()
            
        # Simple template injection (could be more sophisticated)
        full_content = f'{template_content}\n\n{content}'
        
        with open(temp_typ, "w") as f:
            f.write(full_content)
            
        return self.compile(temp_typ, output_path)
        
    def get_available_templates(self) -> list[str]:
        """Get list of available Typst templates."""
        if not self.tools_path.exists():
            return []
        return [f.name for f in self.tools_path.glob("*.typ")]
        
    def check_installation(self) -> dict[str, Any]:
        """Check Typst installation status."""
        result = {
            "installed": self.typst_available,
            "path": shutil.which("typst"),
            "version": None,
            "templates": self.get_available_templates(),
        }
        
        if self.typst_available:
            try:
                version_result = subprocess.run(
                    ["typst", "--version"],
                    capture_output=True,
                    text=True,
                )
                if version_result.returncode == 0:
                    result["version"] = version_result.stdout.strip()
            except Exception:
                pass
                
        return result
