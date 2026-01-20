#!/usr/bin/env python3
"""
Create CV for Fai Wei

Generates a CV for the existing Fai Wei being and creates their personnel file.
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from waft.being import BeingSystem
from waft.pantheon.bureaucracy_god import BureaucracyGod
from waft.templates.typst.compiler import TypstCompiler
from waft.templates.typst.wrappers.brilliant_cv import generate_brilliant_cv


def main():
    """Create CV for Fai Wei."""
    project_path = project_root
    being_system = BeingSystem(project_path=project_path)

    # Load Fai Wei
    fai_wei_id = "being_20260119_101033_f8e06283"
    fai_wei = being_system._load_being(fai_wei_id)

    if not fai_wei:
        print(f"❌ Error: Could not load Fai Wei ({fai_wei_id})")
        sys.exit(1)

    print(f"✅ Loaded Fai Wei: {fai_wei.custom_name}")
    print(f"   Being ID: {fai_wei.being_id}")
    print(f"   Reality: {fai_wei.reality_id}")
    print()

    # Create personnel file directory
    being_dir = being_system.beings_path / fai_wei.being_id
    being_dir.mkdir(parents=True, exist_ok=True)

    personnel_dir = being_dir / "personnel"
    personnel_dir.mkdir(parents=True, exist_ok=True)

    # Set permissions (0o700)
    try:
        os.chmod(being_dir, 0o700)
        os.chmod(personnel_dir, 0o700)
    except (OSError, PermissionError):
        pass

    print(f"📁 Created personnel directory: {personnel_dir}")
    print()

    # Generate CV Typst files
    print("📝 Generating CV Typst files...")
    cv_typ_path = generate_brilliant_cv(being=fai_wei, output_dir=personnel_dir, language="en")
    print(f"✅ Generated CV Typst: {cv_typ_path}")
    print()

    # Compile to PDF
    print("📄 Compiling CV to PDF...")
    cv_pdf_path = None
    try:
        compiler = TypstCompiler()
        pdf_path = personnel_dir / "cv.pdf"
        compiler.compile_file(cv_typ_path, pdf_path)
        cv_pdf_path = pdf_path
        print(f"✅ Generated CV PDF: {cv_pdf_path}")
    except Exception as e:
        print(f"⚠️  CV PDF compilation failed: {e}")
        print(f"   Typst source available at: {cv_typ_path}")
    print()

    # Register with BureaucracyGod
    print("📋 Registering with BureaucracyGod...")
    try:
        bureaucracy_god = BureaucracyGod(project_path=project_path)
        bureaucracy_god.register_personnel_file(
            being_id=fai_wei.being_id,
            personnel_file_path=personnel_dir,
            metadata={
                "cv_version": 1.0,
                "generated_at": datetime.now().isoformat(),
                "reality_id": fai_wei.reality_id,
            },
        )
        print("✅ Registered with BureaucracyGod")
    except Exception as e:
        print(f"⚠️  Bureaucracy registration failed: {e}")
    print()

    print("✅ Fai Wei CV creation complete!")
    print(f"   Personnel file: {personnel_dir}")
    if cv_pdf_path:
        print(f"   CV PDF: {cv_pdf_path}")


if __name__ == "__main__":
    main()
