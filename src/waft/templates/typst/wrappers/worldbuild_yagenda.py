"""
Worldbuilding Template with Yagenda (Agenda/Calendar)

Uses the yagenda package to create meeting agendas, event schedules,
and timeline documents for worldbuilding.
"""

from pathlib import Path
from typing import Any

import yaml

from ..compiler import TypstCompiler


def generate_worldbuild_agenda(
    title: str,
    date: str,
    time: str,
    location: str,
    topics: list[dict[str, Any]],
    output_path: Path,
    invited: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> Path:
    """
    Generate a worldbuilding agenda document using yagenda.

    Args:
        title: Meeting/event title
        date: Date (ISO format: "YYYY-MM-DD")
        time: Time (e.g., "10:00 AM")
        location: Location name
        topics: List of agenda topics
            Format: [{"title": "...", "presenter": "...", "duration": "..."}, ...]
        output_path: Where to save PDF
        invited: List of invited participants
        metadata: Additional metadata

    Returns:
        Path to generated PDF
    """
    # Build invited list
    invited_list = invited or []
    invited_typst = (
        "[" + ", ".join([f'"{name}"' for name in invited_list]) + "]" if invited_list else "[]"
    )

    # Build topics in yagenda format (dictionary with topic keys)
    # yagenda expects a dict where keys are topic IDs and values have Topic, Time, Lead, Purpose, Preparation, Process
    topics_dict = {}
    for i, topic in enumerate(topics):
        topic_key = topic.get("key", f"topic_{i + 1}").lower().replace(" ", "_").replace("-", "_")
        topics_dict[topic_key] = {
            "Topic": topic.get("title", "Agenda Item"),
            "Time": topic.get("duration", "TBD"),
            "Lead": topic.get("presenter", ""),
            "Purpose": topic.get("purpose", "Discuss"),  # Required field
            "Preparation": topic.get("preparation", ""),  # Required field (can be empty)
            "Process": topic.get("process", ""),  # Required field (can be empty)
        }

    # Build YAML string
    topics_yaml = yaml.dump(
        topics_dict, default_flow_style=False, allow_unicode=True, sort_keys=False
    )

    # Build Typst content - use inline YAML with raw string
    # Escape backticks and dollar signs in YAML
    topics_yaml_escaped = topics_yaml.replace("`", "\\`").replace("$", "\\$")

    typst_content = f'''#import "@preview/yagenda:0.1.0": *

#show: agenda.with(
  name: "{title}",
  date: "{date}",
  time: "{time}",
  location: "{location}",
  invited: {invited_typst}
)

// Topics data - inline YAML using raw string
#let topics-yaml-text = `{topics_yaml_escaped}`.text
#let topics = yaml.decode(topics-yaml-text)

// Render the agenda table
#agenda-table(topics)
'''

    # Compile to PDF
    compiler = TypstCompiler()
    pdf_path = compiler.compile(typst_content=typst_content, output_path=output_path)

    return pdf_path


def generate_worldbuild_event_schedule(
    title: str,
    date: str,
    events: list[dict[str, Any]],
    output_path: Path,
    location: str | None = None,
    participants: list[str] | None = None,
    **kwargs,
) -> Path:
    """
    Generate an event schedule for worldbuilding (festivals, ceremonies, etc.).

    Args:
        title: Event title
        date: Event date
        events: List of scheduled events/activities
            Format: [{"title": "...", "time": "...", "description": "..."}, ...]
        output_path: Output PDF path
        location: Event location
        participants: List of participants
        **kwargs: Additional arguments

    Returns:
        Path to generated PDF
    """
    # Convert events to agenda topics format
    topics = []
    for event in events:
        topics.append(
            {
                "title": event.get("title", "Activity"),
                "presenter": event.get("presenter", event.get("time", "")),
                "duration": event.get("duration", "TBD"),
            }
        )

    return generate_worldbuild_agenda(
        title=title,
        date=date,
        time=events[0].get("time", "All Day") if events else "TBD",
        location=location or "Various Locations",
        topics=topics,
        output_path=output_path,
        invited=participants,
        metadata=kwargs,
    )


def generate_worldbuild_council_meeting(
    council_name: str,
    date: str,
    agenda_items: list[dict[str, Any]],
    output_path: Path,
    members: list[str] | None = None,
    location: str = "Council Chambers",
    **kwargs,
) -> Path:
    """
    Generate a council meeting agenda for worldbuilding.

    Args:
        council_name: Name of the council
        date: Meeting date
        agenda_items: List of agenda items
        output_path: Output PDF path
        members: Council members
        location: Meeting location
        **kwargs: Additional arguments

    Returns:
        Path to generated PDF
    """
    topics = []
    for item in agenda_items:
        topics.append(
            {
                "title": item.get("title", "Agenda Item"),
                "presenter": item.get("presenter", item.get("proposed_by", "Council")),
                "duration": item.get("duration", "15 minutes"),
            }
        )

    return generate_worldbuild_agenda(
        title=f"{council_name} Meeting",
        date=date,
        time=kwargs.get("time", "10:00 AM"),
        location=location,
        topics=topics,
        output_path=output_path,
        invited=members,
        metadata=kwargs,
    )
