"""
Example: Generate Aero-Check Checklist using Python Wrapper

Demonstrates how to use the aero-check Typst wrapper to generate
aviation-inspired checklists with optional umbra shadow enhancements.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.templates.typst.wrappers.aero_check import (
    ChecklistSection,
    ChecklistStep,
    ChecklistTopic,
    ShadowConfig,
    generate_aero_checklist,
)


def example_basic_checklist():
    """Generate a basic checklist without shadows."""

    # Create topics with sections and steps
    topics = [
        ChecklistTopic(
            name="Pre-Flight Inspection",
            sections=[
                ChecklistSection(
                    name="Exterior Check",
                    steps=[
                        ChecklistStep("Check for visible damage", "Check"),
                        ChecklistStep("Verify control surfaces move freely", "Check"),
                        ChecklistStep("Inspect landing gear", "Check"),
                        ChecklistStep("Check tire pressure", "Check"),
                    ],
                ),
                ChecklistSection(
                    name="Engine Check",
                    steps=[
                        ChecklistStep("Check oil level", "Check"),
                        ChecklistStep("Inspect propeller", "Check"),
                        ChecklistStep("Check fuel sump", "Check"),
                    ],
                ),
            ],
        ),
        ChecklistTopic(
            name="Cockpit Preparation",
            sections=[
                ChecklistSection(
                    name="Pre-Start",
                    steps=[
                        ChecklistStep("Set parking brake", "Check"),
                        ChecklistStep("Master switch ON", "Check"),
                        ChecklistStep("Check fuel quantity", "Check"),
                    ],
                )
            ],
        ),
    ]

    # Generate PDF
    output_path = Path("demo_output/aero_checklist_basic.pdf")
    output_path.parent.mkdir(exist_ok=True)

    pdf_path = generate_aero_checklist(
        title="Aircraft Pre-Flight Checklist",
        topics=topics,
        output_path=output_path,
        disclaimer="Complete all items before engine start.",
        style=0,
    )

    print(f"✅ Basic checklist generated: {pdf_path}")
    return pdf_path


def example_shadow_checklist():
    """Generate a checklist with umbra shadow enhancements."""

    topics = [
        ChecklistTopic(
            name="System Status",
            sections=[
                ChecklistSection(
                    name="Verification",
                    steps=[
                        ChecklistStep("Verify Typst CLI installed", "Check"),
                        ChecklistStep("Confirm Python environment active", "Check"),
                        ChecklistStep("Validate dependencies installed", "Check"),
                    ],
                ),
                ChecklistSection(
                    name="Template Registry",
                    steps=[
                        ChecklistStep("Confirm registry accessible", "Check"),
                        ChecklistStep("Verify template discovery", "Check"),
                    ],
                ),
            ],
        ),
        ChecklistTopic(
            name="Document Generation",
            sections=[
                ChecklistSection(
                    name="Compilation",
                    steps=[
                        ChecklistStep("Initialize Typst compiler", "Check"),
                        ChecklistStep("Load template and dependencies", "Check"),
                        ChecklistStep("Execute compilation", "Check"),
                        ChecklistStep("Verify PDF output", "Check"),
                    ],
                )
            ],
        ),
    ]

    # Configure shadows - use simple color names (wrapper will handle lighten)
    shadow_config = ShadowConfig(
        enabled=True, radius=0.3, shadow_stops=("blue", "white"), correction=5.0
    )

    output_path = Path("demo_output/aero_checklist_shadow.pdf")
    output_path.parent.mkdir(exist_ok=True)

    pdf_path = generate_aero_checklist(
        title="WAFT System Checklist",
        topics=topics,
        output_path=output_path,
        disclaimer="Enhanced with umbra gradient shadows.",
        style=0,
        use_shadows=True,
        shadow_config=shadow_config,
    )

    print(f"✅ Shadow-enhanced checklist generated: {pdf_path}")
    return pdf_path


def example_neumorphic_checklist():
    """Generate a neumorphic-style checklist."""

    topics = [
        ChecklistTopic(
            name="Daily Routine",
            sections=[
                ChecklistSection(
                    name="Morning",
                    steps=[
                        ChecklistStep("Wake up and hydrate", "Check"),
                        ChecklistStep("Morning exercise", "Check"),
                        ChecklistStep("Healthy breakfast", "Check"),
                    ],
                ),
                ChecklistSection(
                    name="Work Focus",
                    steps=[
                        ChecklistStep("Prioritize top 3 tasks", "Check"),
                        ChecklistStep("Deep work session", "Check"),
                        ChecklistStep("Take regular breaks", "Check"),
                    ],
                ),
            ],
        )
    ]

    # Neumorphic shadow config (soft, light colors)
    shadow_config = ShadowConfig(
        enabled=True, radius=0.2, shadow_stops=('rgb("e0e0e0")', 'rgb("ffffff")'), correction=3.0
    )

    output_path = Path("demo_output/aero_checklist_neumorphic.pdf")
    output_path.parent.mkdir(exist_ok=True)

    pdf_path = generate_aero_checklist(
        title="Daily Routine Checklist",
        topics=topics,
        output_path=output_path,
        disclaimer="Neumorphic design with soft shadows.",
        style=1,
        use_shadows=True,
        shadow_config=shadow_config,
    )

    print(f"✅ Neumorphic checklist generated: {pdf_path}")
    return pdf_path


if __name__ == "__main__":
    print("Generating aero-check checklist examples...\n")

    # Generate examples
    example_basic_checklist()
    example_shadow_checklist()
    example_neumorphic_checklist()

    print("\n✅ All examples generated successfully!")
    print("Check the demo_output/ directory for PDFs.")
