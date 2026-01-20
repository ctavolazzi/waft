"""
Work Efforts Integration for Streamlit UI.
"""

import re
from pathlib import Path
from typing import Any

import streamlit as st

from .utils import display_error


def render_work_efforts_page(project_path: Path):
    """Render the Work Efforts page."""
    st.markdown('<div class="main-header">📋 Work Efforts</div>', unsafe_allow_html=True)

    work_efforts_path = project_path / "_work_efforts"

    if not work_efforts_path.exists():
        st.warning("Work efforts directory not found. Initialize WAFT project first.")
        return

    # List work efforts
    work_efforts = list_work_efforts(work_efforts_path)

    if work_efforts:
        # Work effort selector
        effort_names = [f"{we['id']} - {we['title']}" for we in work_efforts]
        selected = st.selectbox("Select Work Effort", effort_names)

        if selected:
            selected_id = selected.split(" - ")[0]
            selected_effort = next(we for we in work_efforts if we["id"] == selected_id)
            render_work_effort_details(work_efforts_path, selected_effort)
    else:
        st.info("No work efforts found.")

    st.markdown("---")

    # Create new work effort
    st.subheader("Create New Work Effort")
    st.info("Use the MCP work-efforts server or CLI to create work efforts.")


def validate_work_effort_id(work_effort_id: str) -> bool:
    """
    Validate work effort ID format to prevent path traversal.

    Work effort IDs must match pattern: WE-YYMMDD-xxxx
    Example: WE-260112-yfdi
    """
    pattern = r"^WE-\d{6}-[a-z0-9]{4}$"
    return bool(re.match(pattern, work_effort_id))


def validate_path_within_directory(file_path: Path, base_directory: Path) -> bool:
    """
    Validate that a file path stays within the base directory.
    Prevents path traversal attacks.
    """
    try:
        resolved_path = file_path.resolve()
        resolved_base = base_directory.resolve()
        return str(resolved_path).startswith(str(resolved_base))
    except (OSError, ValueError):
        return False


def render_work_effort_details(work_efforts_path: Path, work_effort: dict[str, Any]):
    """Render details for a specific work effort."""
    work_effort_id = work_effort["id"]

    # Validate work effort ID format
    if not validate_work_effort_id(work_effort_id):
        display_error(f"Invalid work effort ID format: {work_effort_id}", "Security Error")
        return

    effort_path = work_efforts_path / work_effort_id

    # Validate path stays within work_efforts directory
    if not validate_path_within_directory(effort_path, work_efforts_path):
        display_error("Invalid work effort path: path traversal detected", "Security Error")
        return

    st.subheader(work_effort["title"])

    # Read index file if available
    index_file = effort_path / f"{work_effort_id}_index.md"

    # Validate index file path
    if not validate_path_within_directory(index_file, work_efforts_path):
        display_error("Invalid file path: path traversal detected", "Security Error")
        return

    if index_file.exists():
        try:
            with open(index_file, encoding="utf-8") as f:
                st.markdown(f.read())
        except Exception as e:
            display_error(f"Failed to read index file: {e}", "Error")

    # List tickets if available
    tickets_path = effort_path / "tickets"
    if tickets_path.exists():
        st.markdown("---")
        st.subheader("Tickets")
        tickets = list_tickets(tickets_path)

        if tickets:
            for ticket in tickets:
                with st.expander(f"**{ticket['id']}**: {ticket['title']}"):
                    if ticket.get("content"):
                        st.markdown(ticket["content"])
        else:
            st.info("No tickets found.")


def list_work_efforts(work_efforts_path: Path) -> list[dict[str, Any]]:
    """List all work efforts."""
    work_efforts = []

    for item in work_efforts_path.iterdir():
        if item.is_dir() and item.name.startswith("WE-"):
            # Try to find index file
            index_file = item / f"{item.name}_index.md"
            if index_file.exists():
                work_efforts.append(
                    {
                        "id": item.name,
                        "title": item.name.replace("WE-", "").replace("_", " ").title(),
                        "path": item,
                    }
                )
            else:
                # Fallback: use directory name
                work_efforts.append(
                    {
                        "id": item.name,
                        "title": item.name.replace("WE-", "").replace("_", " ").title(),
                        "path": item,
                    }
                )

    # Sort by name
    work_efforts.sort(key=lambda x: x["id"], reverse=True)
    return work_efforts


def list_tickets(tickets_path: Path) -> list[dict[str, Any]]:
    """List tickets in a work effort."""
    tickets = []

    # Validate tickets_path stays within work_efforts
    work_efforts_base = (
        tickets_path.parent.parent
    )  # Go up from tickets/ to work_effort/ to _work_efforts/
    if not validate_path_within_directory(tickets_path, work_efforts_base):
        return tickets  # Return empty if path traversal detected

    for ticket_file in tickets_path.glob("*.md"):
        # Validate each ticket file path
        if not validate_path_within_directory(ticket_file, work_efforts_base):
            continue  # Skip if path traversal detected

        if ticket_file.name.startswith("TKT-"):
            # Read ticket content
            try:
                with open(ticket_file, encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                continue  # Skip files that can't be read

            # Extract title from first line or filename
            lines = content.split("\n")
            title = lines[0].replace("#", "").strip() if lines else ticket_file.stem

            tickets.append(
                {"id": ticket_file.stem, "title": title, "content": content, "path": ticket_file}
            )

    return tickets


def render_recent_work_efforts(project_path: Path):
    """Render recent work efforts widget."""
    work_efforts_path = project_path / "_work_efforts"

    if not work_efforts_path.exists():
        st.info("No work efforts directory")
        return

    work_efforts = list_work_efforts(work_efforts_path)

    if work_efforts:
        for effort in work_efforts[:5]:  # Show 5 most recent
            st.write(f"**{effort['id']}**")
            st.caption(effort["title"])
    else:
        st.info("No work efforts yet")


def render_create_work_effort_modal(project_path: Path):
    """Render create work effort modal (placeholder)."""
    st.info("Use the MCP work-efforts server or CLI to create work efforts.")
