"""
Typst Compiler
==============

Handles compilation of Typst documents to PDF using the typst CLI.
Includes security hardening: path validation, content size limits, and timeouts.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional
import shutil
import os
import re


class TypstCompiler:
    """Compiles Typst documents to PDF with security hardening."""
    
    def __init__(self, timeout: int = 60, max_content_size: int = 10 * 1024 * 1024):
        """
        Initialize Typst compiler, check for typst CLI.
        
        Args:
            timeout: Compilation timeout in seconds (default: 60)
            max_content_size: Maximum content size in bytes (default: 10MB)
            
        Raises:
            RuntimeError: If typst CLI is not available or version is too old
        """
        self.timeout = timeout
        self.max_content_size = max_content_size
        self._check_typst_available()
    
    def _check_typst_available(self) -> None:
        """Check if Typst CLI is available and version is sufficient."""
        if not shutil.which("typst"):
            raise RuntimeError(
                "Typst CLI not found. Please install Typst:\n"
                "  - Using Cargo: cargo install typst-cli\n"
                "  - Or download from: https://typst.com\n"
                "  - Minimum version required: 0.10.0"
            )
        
        # Check version (minimum 0.10.0)
        try:
            result = subprocess.run(
                ["typst", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=False  # Security: Never use shell=True
            )
            if result.returncode == 0:
                version_output = result.stdout.strip()
                # Extract version number (e.g., "typst 0.11.0" -> "0.11.0")
                version_match = re.search(r'(\d+)\.(\d+)\.(\d+)', version_output)
                if version_match:
                    major, minor, patch = map(int, version_match.groups())
                    if (major, minor) < (0, 10):
                        raise RuntimeError(
                            f"Typst version {major}.{minor}.{patch} is too old. "
                            f"Minimum version required: 0.10.0. "
                            f"Please update Typst: cargo install --force typst-cli"
                        )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Typst version check timed out")
        except Exception as e:
            # If version check fails, warn but continue (might be a different typst installation)
            print(f"⚠️  Could not verify Typst version: {e}")
    
    def _validate_path_in_project(self, path: Path) -> Path:
        """
        Validate path is within project boundaries. Returns resolved path.
        
        Security: Rejects paths containing '..', absolute paths outside project/temp,
        and resolves symlinks before validation.
        
        Args:
            path: Path to validate
            
        Returns:
            Resolved, validated path
            
        Raises:
            ValueError: If path is invalid or outside allowed directories
        """
        # Resolve symlinks and normalize
        try:
            resolved = path.resolve()
        except (OSError, RuntimeError) as e:
            raise ValueError(f"Invalid path (cannot resolve): {path} - {e}")
        
        # Reject paths containing '..' (path traversal)
        if ".." in str(path) or ".." in str(resolved):
            raise ValueError(
                f"Path traversal detected: {path}. "
                f"Paths containing '..' are not allowed for security reasons."
            )
        
        # For absolute paths, check if they're in allowed directories
        if resolved.is_absolute():
            # Allow paths in temp directories
            temp_dir = Path(tempfile.gettempdir()).resolve()
            temp_prefixes = [
                temp_dir,
                Path("/tmp"),
                Path("/var/tmp"),
            ]
            
            # Allow paths in project directory (if we can determine it)
            try:
                project_root = Path(__file__).parent.parent.parent.parent.parent.resolve()
                allowed_prefixes = temp_prefixes + [project_root]
            except (IndexError, AttributeError):
                allowed_prefixes = temp_prefixes
            
            # Check if path is within any allowed prefix
            resolved_str = str(resolved)
            is_allowed = False
            
            for prefix in allowed_prefixes:
                prefix_str = str(prefix.resolve() if prefix.exists() else prefix)
                if resolved_str.startswith(prefix_str):
                    is_allowed = True
                    break
            
            # Also check if any parent is a temp directory (for nested temp dirs)
            if not is_allowed:
                parent = resolved.parent
                max_depth = 10  # Prevent infinite loops
                depth = 0
                while parent != parent.parent and depth < max_depth:
                    parent_str = str(parent)
                    if any(parent_str.startswith(str(p)) for p in temp_prefixes):
                        is_allowed = True
                        break
                    parent = parent.parent
                    depth += 1
            
            if not is_allowed:
                raise ValueError(
                    f"Absolute path outside allowed directories: {resolved}. "
                    f"Only paths within project or temp directories are allowed."
                )
        
        return resolved
    
    def _validate_content_size(self, content: str) -> None:
        """
        Validate content size is within limits.
        
        Args:
            content: Content string to validate
            
        Raises:
            ValueError: If content exceeds size limit
        """
        content_size = len(content.encode("utf-8"))
        if content_size > self.max_content_size:
            raise ValueError(
                f"Content size ({content_size} bytes) exceeds maximum "
                f"allowed size ({self.max_content_size} bytes). "
                f"Consider reducing content size or increasing max_content_size."
            )
    
    def compile(
        self,
        typst_content: str,
        output_path: Path,
        working_dir: Optional[Path] = None
    ) -> Path:
        """
        Compile Typst content string to PDF.
        
        Security: Validates paths, content size, and uses shell=False.
        
        Args:
            typst_content: Typst source code as string
            output_path: Where to save the PDF
            working_dir: Working directory for compilation (uses temp dir if None)
            
        Returns:
            Path to generated PDF
            
        Raises:
            ValueError: If paths are invalid or content size exceeds limit
            RuntimeError: If compilation fails
            subprocess.TimeoutExpired: If compilation times out
        """
        # Validate content size
        self._validate_content_size(typst_content)
        
        # Validate and normalize paths
        output_path = Path(output_path)
        # Validate path (checks security, but doesn't change the path)
        self._validate_path_in_project(output_path)
        
        # Ensure output directory exists with safe permissions
        output_path.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
        
        # Check write permissions
        if not os.access(output_path.parent, os.W_OK):
            raise PermissionError(
                f"Cannot write to output directory: {output_path.parent}. "
                f"Please check directory permissions."
            )
        
        # Use temp directory if not specified
        if working_dir is None:
            with tempfile.TemporaryDirectory() as tmpdir:
                return self._compile_in_dir(
                    typst_content,
                    output_path,
                    Path(tmpdir)
                )
        else:
            working_dir = Path(working_dir)
            working_dir = self._validate_path_in_project(working_dir)
            
            # Ensure working directory exists
            working_dir.mkdir(parents=True, exist_ok=True, mode=0o755)
            
            # Check read/write permissions
            if not os.access(working_dir, os.R_OK | os.W_OK):
                raise PermissionError(
                    f"Cannot read/write to working directory: {working_dir}. "
                    f"Please check directory permissions."
                )
            
            return self._compile_in_dir(
                typst_content,
                output_path,
                working_dir
            )
    
    def _compile_in_dir(
        self,
        typst_content: str,
        output_path: Path,
        working_dir: Path
    ) -> Path:
        """
        Compile Typst in a specific directory.
        
        Security: Uses shell=False, validates paths, handles timeouts.
        
        Args:
            typst_content: Typst source code as string
            output_path: Where to save the PDF
            working_dir: Working directory for compilation
            
        Returns:
            Path to generated PDF
            
        Raises:
            RuntimeError: If compilation fails
            subprocess.TimeoutExpired: If compilation times out
        """
        # Write Typst content to main.typ
        main_typ = working_dir / "main.typ"
        main_typ.write_text(typst_content, encoding="utf-8")
        
        # Output PDF in working directory first
        pdf_path = working_dir / "main.pdf"
        
        # Compile using typst CLI
        # Security: Use shell=False with list arguments
        try:
            result = subprocess.run(
                ["typst", "compile", str(main_typ), str(pdf_path)],
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                shell=False  # CRITICAL: Never use shell=True
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                f"Typst compilation timed out after {self.timeout} seconds. "
                f"Consider increasing timeout or simplifying the document."
            )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout
            raise RuntimeError(
                f"Typst compilation failed:\n{error_msg}"
            )
        
        # Verify PDF was generated
        if not pdf_path.exists():
            raise RuntimeError(
                f"PDF not generated: {pdf_path} not found after compilation"
            )
        
        # Copy to output path
        shutil.copy2(pdf_path, output_path)
        
        return output_path
    
    def compile_file(
        self,
        typ_file: Path,
        output_path: Path
    ) -> Path:
        """
        Compile a Typst file to PDF.
        
        Security: Validates paths and uses shell=False.
        
        Args:
            typ_file: Path to .typ file
            output_path: Where to save the PDF
            
        Returns:
            Path to generated PDF
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If paths are invalid
            RuntimeError: If compilation fails
        """
        typ_file = Path(typ_file)
        
        # Validate paths
        typ_file = self._validate_path_in_project(typ_file)
        output_path = Path(output_path)
        output_path = self._validate_path_in_project(output_path)
        
        if not typ_file.exists():
            raise FileNotFoundError(f"Typst file not found: {typ_file}")
        
        # Check read permissions
        if not os.access(typ_file, os.R_OK):
            raise PermissionError(
                f"Cannot read input file: {typ_file}. "
                f"Please check file permissions."
            )
        
        # Read content and compile
        typst_content = typ_file.read_text(encoding="utf-8")
        working_dir = typ_file.parent
        
        return self.compile(typst_content, output_path, working_dir)
