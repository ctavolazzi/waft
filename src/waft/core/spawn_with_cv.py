"""
Spawn Being with CV Generation

Utility functions for spawning Beings with automatically generated CVs.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any

from ..being import BeingSystem
from ..pantheon.bureaucracy_god import BureaucracyGod
from ..reality import RealitySystem, RealityType
from ..templates.typst.compiler import TypstCompiler
from ..templates.typst.wrappers.brilliant_cv import generate_brilliant_cv


def spawn_being_with_cv(
    project_path: Path,
    reality_id: str | None = None,
    parent_being_id: str | None = None,
    initial_skills: dict[str, float] | None = None,
    generate_pdf: bool = True,
) -> dict[str, Any]:
    """
    Spawn a Being and generate a CV in its personnel file.

    Args:
        project_path: Project root path
        reality_id: Optional reality ID (creates default if None)
        parent_being_id: Optional parent Being ID
        initial_skills: Optional initial skills dict
        generate_pdf: Whether to compile CV to PDF (default: True)

    Returns:
        Dictionary with:
            - being: Being instance
            - personnel_file_path: Path to personnel directory
            - cv_typ_path: Path to cv.typ file
            - cv_pdf_path: Path to cv.pdf (if generated)
            - bureaucracy_record: PersonnelRecord (if registered)
    """
    # Initialize systems
    being_system = BeingSystem(project_path=project_path)
    reality_system = RealitySystem(project_path=project_path)

    # Determine or create reality
    if reality_id is None:
        reality = reality_system.create_reality(
            reality_type=RealityType.LEARNING, configuration={"purpose": "bureaucracy"}
        )
        reality_id = reality.reality_id

    # Spawn Being
    being = being_system.spawn_being(
        reality_id=reality_id, parent_being_id=parent_being_id, initial_skills=initial_skills
    )

    # Create personnel file directory
    being_dir = being_system.beings_path / being.being_id
    being_dir.mkdir(parents=True, exist_ok=True)

    personnel_dir = being_dir / "personnel"
    personnel_dir.mkdir(parents=True, exist_ok=True)

    # Set permissions (0o700)
    try:
        os.chmod(being_dir, 0o700)
        os.chmod(personnel_dir, 0o700)
    except (OSError, PermissionError):
        pass

    # Generate CV Typst files
    cv_typ_path = generate_brilliant_cv(being=being, output_dir=personnel_dir, language="en")

    # Compile to PDF if requested
    cv_pdf_path = None
    if generate_pdf:
        try:
            compiler = TypstCompiler()
            pdf_path = personnel_dir / "cv.pdf"
            compiler.compile_file(cv_typ_path, pdf_path)
            cv_pdf_path = pdf_path
        except Exception as e:
            # PDF compilation failed, but Being and Typst files are created
            print(f"⚠️  CV PDF compilation failed: {e}")
            print(f"   Typst source available at: {cv_typ_path}")

    # Register with BureaucracyGod
    bureaucracy_record = None
    try:
        bureaucracy_god = BureaucracyGod(project_path=project_path)
        bureaucracy_record = bureaucracy_god.register_personnel_file(
            being_id=being.being_id,
            personnel_file_path=personnel_dir,
            metadata={
                "cv_version": 1.0,
                "generated_at": datetime.now().isoformat(),
                "reality_id": reality_id,
            },
        )
    except Exception as e:
        print(f"⚠️  Bureaucracy registration failed: {e}")
        print("   Being created, but not registered with BureaucracyGod")

    return {
        "being": being,
        "personnel_file_path": personnel_dir,
        "cv_typ_path": cv_typ_path,
        "cv_pdf_path": cv_pdf_path,
        "bureaucracy_record": bureaucracy_record,
    }
