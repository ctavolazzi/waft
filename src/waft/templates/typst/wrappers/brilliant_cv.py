"""
brilliant-cv Typst Template Wrapper

Generates Typst content for brilliant-cv template from Being data.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any

from ..being_cv_mapper import map_being_to_cv_data

if TYPE_CHECKING:
    from ...being import Being


def generate_brilliant_cv(being: "Being", output_dir: Path, language: str = "en") -> Path:
    """
    Generate brilliant-cv Typst content from Being data.

    Args:
        being: Being instance to generate CV for
        output_dir: Directory to write Typst files
        language: Language code (en, fr, cn) - default: en

    Returns:
        Path to generated cv.typ file
    """
    # Map Being to CV data
    cv_data = map_being_to_cv_data(being)

    # Create output directory structure
    output_dir.mkdir(parents=True, exist_ok=True)
    modules_dir = output_dir / f"modules_{language}"
    modules_dir.mkdir(parents=True, exist_ok=True)

    # Generate metadata.toml
    metadata_content = _create_metadata_toml(cv_data, language)
    metadata_path = output_dir / "metadata.toml"
    metadata_path.write_text(metadata_content, encoding="utf-8")

    # Generate cv.typ
    cv_typ_content = _create_cv_typ(language, cv_data)
    cv_typ_path = output_dir / "cv.typ"
    cv_typ_path.write_text(cv_typ_content, encoding="utf-8")

    # Generate experience module
    experience_content = _create_experience_module(cv_data["experience"])
    experience_path = modules_dir / "experience.typ"
    experience_path.write_text(experience_content, encoding="utf-8")

    # Generate skills module
    skills_content = _create_skills_module(cv_data["technical_skills"], cv_data["soft_skills"])
    skills_path = modules_dir / "skills.typ"
    skills_path.write_text(skills_content, encoding="utf-8")

    # Generate education module
    education_content = _create_education_module(cv_data["education"])
    education_path = modules_dir / "education.typ"
    education_path.write_text(education_content, encoding="utf-8")

    return cv_typ_path


def _create_metadata_toml(cv_data: dict[str, Any], language: str) -> str:
    """Generate metadata.toml content."""
    personal = cv_data["personal"]

    return f"""[personal]
firstname = "{personal["firstname"]}"
lastname = "{personal["lastname"]}"
email = "{personal["email"]}"
location = "{personal["location"]}"
{_format_optional_field("phone", personal.get("phone"))}
{_format_optional_field("website", personal.get("website"))}
{_format_optional_field("github", personal.get("github"))}
{_format_optional_field("linkedin", personal.get("linkedin"))}

[layout]
main-color = "0044cc"
font = "Roboto"
{_format_optional_field("font-alt", None)}

[inject]
keyword-injection = true
prompt-injection = true

[lang]
default = "{language}"
"""


def _format_optional_field(key: str, value: str | None) -> str:
    """Format optional TOML field."""
    if value:
        return f'{key} = "{value}"'
    return ""  # Don't include commented fields - Typst doesn't like them


def _create_cv_typ(language: str, cv_data: dict[str, Any]) -> str:
    """Generate cv.typ entry point."""
    personal = cv_data["personal"]
    return f"""#import "@preview/brilliant-cv:3.1.1": *

#import "modules_{language}/experience.typ": *
#import "modules_{language}/skills.typ": *
#import "modules_{language}/education.typ": *

#let doc = [
  #experience
  #skills
  #education
]

#show: doc => cv(
  doc,
  metadata: (
    personal: (
      firstname: "{personal["firstname"]}",
      lastname: "{personal["lastname"]}",
      email: "{personal["email"]}",
      location: "{personal["location"]}",
    ),
  ),
  main-color: rgb("#0044cc"),
)
"""


def _create_experience_module(experience: list[dict[str, Any]]) -> str:
    """Generate experience.typ module."""
    if not experience:
        return "#let experience = []\n"

    entries = []
    for exp in experience:
        bullets_str = ",\n    ".join([f'"{bullet}"' for bullet in exp.get("bullets", [])])
        entry = f"""cvEntry(
  title: "{_escape_typst(exp.get("title", ""))}",
  institution: "{_escape_typst(exp.get("institution", ""))}",
  date: "{exp.get("date", "")}",
  location: "{_escape_typst(exp.get("location", ""))}",
  bullets: [
    {bullets_str}
  ],
)"""
        entries.append(entry)

    return f"""#let experience = [
{",\n".join(entries)}
]
"""


def _create_skills_module(
    technical_skills: list[dict[str, Any]], soft_skills: list[dict[str, Any]]
) -> str:
    """Generate skills.typ module."""
    tech_skills_str = ",\n    ".join([f'"{skill["name"]}"' for skill in technical_skills[:10]])
    soft_skills_str = ",\n    ".join([f'"{skill["name"]}"' for skill in soft_skills[:10]])

    return f"""#let skills = (
  technical: [
    {tech_skills_str}
  ],
  soft: [
    {soft_skills_str}
  ],
)
"""


def _create_education_module(education: list[dict[str, Any]]) -> str:
    """Generate education.typ module."""
    if not education:
        return "#let education = []\n"

    entries = []
    for edu in education:
        entry = f"""cvEducation(
  degree: "{_escape_typst(edu.get("degree", ""))}",
  institution: "{_escape_typst(edu.get("institution", ""))}",
  date: "{edu.get("date", "")}",
  location: "{_escape_typst(edu.get("location", ""))}",
  description: "{_escape_typst(edu.get("description", ""))}",
)"""
        entries.append(entry)

    return f"""#let education = [
{",\n".join(entries)}
]
"""


def _escape_typst(text: str) -> str:
    """Escape special characters for Typst."""
    if not text:
        return ""
    return text.replace('"', '\\"').replace("\n", " ").replace("\r", "")
