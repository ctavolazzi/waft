"""
Mission PDF Generator

Generates professional mission documentation PDFs with military-style formatting.
Soft military language (NCIS TV style) - professional but approachable.
"""

from datetime import datetime
from pathlib import Path

from ..evolution.pdf_generator import PDFGenerator
from ..utils import get_storage_path


def generate_mission_pdf(
    mission: "Mission", project_path: Path | None = None, output_path: Path | None = None
) -> Path:
    """
    Generate professional mission PDF document.

    Args:
        mission: Mission object
        project_path: Project root path
        output_path: Optional output path (auto-generated if None)

    Returns:
        Path to generated PDF
    """
    if project_path is None:
        project_path = Path.cwd()
    else:
        project_path = Path(project_path)

    # Generate mission content
    content = generate_mission_content(mission)

    # Create PDF generator
    generator = PDFGenerator.from_content(
        content=content, title=f"Mission Briefing: {mission.name}", style="clinical_standard"
    )

    # Determine output path
    if output_path is None:
        relative_path = Path("_pantheon/military_brass/missions") / f"{mission.mission_id}.pdf"
        output_path = get_storage_path(relative_path, project_path)
    else:
        # If absolute path provided, use as-is (might be outside project)
        if output_path.is_absolute():
            output_path = output_path
        else:
            output_path = get_storage_path(output_path, project_path)

    # Generate PDF
    pdf_path = generator.save(output_path=output_path, open_pdf=False, convert_to_png=False)

    return pdf_path


def generate_mission_content(mission: "Mission") -> str:
    """
    Generate mission briefing content.

    Args:
        mission: Mission object

    Returns:
        Markdown content for mission PDF
    """
    content = f"""# Mission Briefing: {mission.name}

**Mission ID**: {mission.mission_id}  
**Classification**: {mission.classification}  
**Date**: {mission.created_at}  
**Status**: {mission.status}  
**Progress**: {mission.progress}

---

## Mission Objective

{mission.objective}

---

## Success Criteria

"""

    for i, criterion in enumerate(mission.success_criteria, 1):
        content += f"{i}. {criterion}\n"

    content += f"""
---

## Mission Briefing

{mission.briefing or "Mission briefing prepared. Objective defined and approved by Military Brass."}

---

## Mission Details

**Difficulty**: {mission.difficulty}/10  
**Classification**: {mission.classification}  
**Status**: {mission.status}  
**Progress**: {mission.progress}

---

## Mission Plan

### Phase 1: Preparation
- Mission briefing reviewed and approved
- Resources allocated
- Timeline established
- Success criteria defined

### Phase 2: Execution
- Mission objectives pursued
- Progress tracked and reported
- Status updates provided
- Adjustments made as needed

### Phase 3: Completion
- Success criteria verified
- Mission debriefing conducted
- Documentation finalized
- Recognition and rewards distributed

---

## Timeline

**Mission Start**: {mission.created_at}  
**Current Status**: {mission.status}  
**Progress**: {mission.progress}

---

## Resources

- **Mission ID**: {mission.mission_id}
- **Classification**: {mission.classification}
- **Difficulty**: {mission.difficulty}/10
- **Status**: {mission.status}

---

## Risk Assessment

Mission risks and mitigations to be assessed during execution phase.

---

## Status Tracking

**Current Status**: {mission.status}  
**Progress**: {mission.progress}  
**Last Updated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## Notes

Mission briefing prepared by Military Brass.  
Objective defined and approved.  
Mission ready for execution.

---

*Mission briefing document - {mission.classification}*
"""

    return content
