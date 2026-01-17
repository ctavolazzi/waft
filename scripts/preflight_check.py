#!/usr/bin/env python3
"""
WAFT Demo Pre-Flight Checklist
================================

Verifies that all dependencies, files, and systems are ready
for the interactive demonstration.

Run this before showing the demo to ensure everything works.
"""

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
import importlib.util

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class PreflightChecker:
    """Runs comprehensive pre-flight checks for the demo."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.issues: List[str] = []

    def header(self, text: str):
        """Print section header."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}\n")

    def check(self, description: str, passed: bool, error_msg: Optional[str] = None, warning: bool = False):
        """Print check result."""
        if passed:
            print(f"{Colors.GREEN}✅ {description}{Colors.END}")
            if not warning:
                self.passed += 1
        else:
            if warning:
                print(f"{Colors.YELLOW}⚠️  {description}{Colors.END}")
                if error_msg:
                    print(f"   {Colors.YELLOW}→ {error_msg}{Colors.END}")
                self.warnings += 1
            else:
                print(f"{Colors.RED}❌ {description}{Colors.END}")
                if error_msg:
                    print(f"   {Colors.RED}→ {error_msg}{Colors.END}")
                    self.issues.append(error_msg)
                self.failed += 1

    def info(self, text: str):
        """Print info message."""
        print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

    def check_python_version(self) -> bool:
        """Check Python version is 3.10+."""
        version = sys.version_info
        passed = version.major == 3 and version.minor >= 10
        version_str = f"{version.major}.{version.minor}.{version.micro}"

        self.check(
            f"Python version: {version_str}",
            passed,
            "Python 3.10+ required" if not passed else None
        )
        return passed

    def check_dependency(self, package_name: str, import_name: Optional[str] = None) -> bool:
        """Check if a Python package is installed."""
        if import_name is None:
            import_name = package_name

        try:
            __import__(import_name)
            self.check(f"Package '{package_name}' installed", True)
            return True
        except ImportError:
            self.check(
                f"Package '{package_name}' installed",
                False,
                f"Install with: pip install {package_name}"
            )
            return False

    def check_file_exists(self, file_path: Path, description: str, required: bool = True) -> bool:
        """Check if a file exists."""
        exists = file_path.exists()
        self.check(
            f"{description}: {file_path}",
            exists,
            f"File not found" if not exists else None,
            warning=not required
        )
        return exists

    def check_directory_exists(self, dir_path: Path, description: str, create: bool = False) -> bool:
        """Check if a directory exists, optionally create it."""
        exists = dir_path.exists()

        if not exists and create:
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                self.check(f"{description}: {dir_path}", True, "Created directory")
                return True
            except Exception as e:
                self.check(f"{description}: {dir_path}", False, f"Failed to create: {e}")
                return False
        else:
            self.check(
                f"{description}: {dir_path}",
                exists,
                f"Directory not found" if not exists else None
            )
            return exists

    def check_module_importable(self, module_path: str, description: str) -> bool:
        """Check if a Python module can be imported."""
        try:
            importlib.import_module(module_path)
            self.check(f"{description} importable", True)
            return True
        except ImportError as e:
            self.check(f"{description} importable", False, str(e))
            return False
        except Exception as e:
            self.check(f"{description} importable", False, f"Error: {e}")
            return False

    def check_command_exists(self, command: str, description: str, required: bool = True) -> bool:
        """Check if a system command exists."""
        try:
            result = subprocess.run(
                ['which', command],
                capture_output=True,
                text=True
            )
            exists = result.returncode == 0
            self.check(
                f"{description} available",
                exists,
                f"Command '{command}' not found in PATH" if not exists else None,
                warning=not required
            )
            return exists
        except Exception as e:
            self.check(f"{description} available", False, str(e), warning=not required)
            return False

    def run_all_checks(self):
        """Run all pre-flight checks."""

        # =====================================================================
        # SYSTEM CHECKS
        # =====================================================================
        self.header("🖥️  SYSTEM CHECKS")

        self.check_python_version()

        # =====================================================================
        # PYTHON DEPENDENCIES
        # =====================================================================
        self.header("📦 PYTHON DEPENDENCIES")

        self.check_dependency("weasyprint")
        self.check_dependency("jinja2")
        self.check_dependency("pypdf")

        # =====================================================================
        # WAFT CORE MODULES
        # =====================================================================
        self.header("🔧 WAFT CORE MODULES")

        self.check_module_importable("src.waft.reflection", "Reflection System")
        self.check_module_importable("src.waft.binder", "Binder System")
        self.check_module_importable(
            "src.waft.templates.code_documentation",
            "Code Documentation Template"
        )

        # =====================================================================
        # DEMO FILES
        # =====================================================================
        self.header("📄 DEMO FILES")

        demo_files = [
            (PROJECT_ROOT / "examples/interactive_demo.py", "Interactive Demo Script", True),
            (PROJECT_ROOT / "examples/demonstrate_reflection.py", "Reflection Demo Script", True),
            (PROJECT_ROOT / "WHAT_WE_HAVE_HERE.md", "Verification Document", True),
            (PROJECT_ROOT / "DEMO_CHECKLIST.md", "Demo Checklist", False),
        ]

        for file_path, description, required in demo_files:
            self.check_file_exists(file_path, description, required)

        # Check if demo script is executable
        demo_script = PROJECT_ROOT / "examples/interactive_demo.py"
        if demo_script.exists():
            is_executable = demo_script.stat().st_mode & 0o111 != 0
            self.check(
                "Demo script is executable",
                is_executable,
                f"Make executable with: chmod +x {demo_script}",
                warning=True
            )

        # =====================================================================
        # TEMPLATE FILES
        # =====================================================================
        self.header("📋 TEMPLATE FILES")

        templates_dir = PROJECT_ROOT / "src/waft/templates"
        templates = [
            "simple_scientific.py",
            "field_guide.py",
            "tm_report.py",
            "lab_notes.py",
            "personal_memo.py",
            "eldritch_journal.py",
            "screenplay.py",
            "heartfelt_letter.py",
            "invoice_contract.py",
            "code_documentation.py",
            "storybook.py",
            "newspaper.py",
        ]

        template_count = 0
        for template in templates:
            if self.check_file_exists(
                templates_dir / template,
                f"Template: {template}",
                required=False
            ):
                template_count += 1

        self.info(f"Found {template_count}/12 templates")

        # =====================================================================
        # DIRECTORIES
        # =====================================================================
        self.header("📁 DIRECTORIES")

        self.check_directory_exists(
            PROJECT_ROOT / "_work_efforts",
            "Output directory",
            create=True
        )

        self.check_directory_exists(
            PROJECT_ROOT / "src/waft",
            "WAFT source directory",
            create=False
        )

        self.check_directory_exists(
            PROJECT_ROOT / "examples",
            "Examples directory",
            create=False
        )

        # =====================================================================
        # EXAMPLE PDFS
        # =====================================================================
        self.header("📑 EXAMPLE PDFs (Optional)")

        output_dir = PROJECT_ROOT / "_work_efforts"
        if output_dir.exists():
            pdf_files = list(output_dir.glob("*.pdf"))
            if pdf_files:
                self.info(f"Found {len(pdf_files)} existing PDF examples:")
                for pdf in sorted(pdf_files)[:5]:  # Show first 5
                    size_kb = pdf.stat().st_size / 1024
                    print(f"   • {pdf.name} ({size_kb:.1f} KB)")
                if len(pdf_files) > 5:
                    print(f"   • ... and {len(pdf_files) - 5} more")
            else:
                self.info("No existing PDF examples (will be generated during demo)")

        # =====================================================================
        # SYSTEM COMMANDS (Optional)
        # =====================================================================
        self.header("🔨 SYSTEM COMMANDS (Optional)")

        self.check_command_exists("xdg-open", "PDF opener (xdg-open)", required=False)
        self.check_command_exists("git", "Git", required=False)

        # =====================================================================
        # SMOKE TEST
        # =====================================================================
        self.header("🧪 SMOKE TEST")

        try:
            from src.waft.reflection import ReflectionSystem
            waft_root = PROJECT_ROOT / "src/waft"
            reflector = ReflectionSystem(waft_root=waft_root)
            self.check("Reflection system initialization", True)
        except Exception as e:
            self.check("Reflection system initialization", False, str(e))

        # =====================================================================
        # FINAL REPORT
        # =====================================================================
        return self.print_summary()

    def print_summary(self):
        """Print final summary."""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}PREFLIGHT SUMMARY{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}\n")

        print(f"{Colors.GREEN}✅ Passed:  {self.passed}{Colors.END}")
        print(f"{Colors.RED}❌ Failed:  {self.failed}{Colors.END}")
        print(f"{Colors.YELLOW}⚠️  Warnings: {self.warnings}{Colors.END}")

        total = self.passed + self.failed
        if total > 0:
            success_rate = (self.passed / total) * 100
            print(f"\n{Colors.BOLD}Success Rate: {success_rate:.1f}%{Colors.END}")

        print()

        if self.failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}{'=' * 80}{Colors.END}")
            print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL SYSTEMS GO - DEMO READY TO RUN{Colors.END}")
            print(f"{Colors.GREEN}{Colors.BOLD}{'=' * 80}{Colors.END}\n")

            print(f"{Colors.CYAN}Run the demo with:{Colors.END}")
            print(f"{Colors.BOLD}  python3 examples/interactive_demo.py{Colors.END}\n")

            return True
        else:
            print(f"{Colors.RED}{Colors.BOLD}{'=' * 80}{Colors.END}")
            print(f"{Colors.RED}{Colors.BOLD}⚠️  ISSUES DETECTED - FIX BEFORE RUNNING DEMO{Colors.END}")
            print(f"{Colors.RED}{Colors.BOLD}{'=' * 80}{Colors.END}\n")

            print(f"{Colors.RED}Issues to fix:{Colors.END}")
            for i, issue in enumerate(self.issues, 1):
                print(f"  {i}. {issue}")
            print()

            return False


def main():
    """Run pre-flight checks."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                               ║")
    print("║                  WAFT DEMO PRE-FLIGHT CHECKLIST                               ║")
    print("║                  Verifying system readiness...                                ║")
    print("║                                                                               ║")
    print("╚═══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")

    checker = PreflightChecker()
    success = checker.run_all_checks()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
