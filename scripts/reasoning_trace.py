"""
Reasoning Trace System
=====================

Extracts and displays traceable chains of thought and decision-making.
Shows the "why" behind actions - a traceable reasoning path.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


def extract_reasoning_trace(project_path: Path) -> list[dict[str, Any]]:
    """
    Extract reasoning trace from session.

    Looks for:
    - Decision logs
    - Reasoning files
    - Conversation context
    - Work effort reasoning
    """
    trace = []
    trace_dir = project_path / "_work_efforts" / "reasoning_traces"

    # Check for reasoning trace files
    if trace_dir.exists():
        trace_files = sorted(
            trace_dir.glob("trace_*.json"), key=lambda p: p.stat().st_mtime, reverse=True
        )[:10]  # Most recent 10

        for trace_file in trace_files:
            try:
                data = json.loads(trace_file.read_text())
                trace.append(
                    {
                        "timestamp": data.get("timestamp", ""),
                        "decision": data.get("decision", ""),
                        "reasoning": data.get("reasoning", ""),
                        "context": data.get("context", {}),
                        "outcome": data.get("outcome", ""),
                        "source": trace_file.stem,
                    }
                )
            except Exception:
                pass

    # Extract from work efforts (if they have reasoning)
    work_efforts_dir = project_path / "_work_efforts"
    if work_efforts_dir.exists():
        today_pattern = datetime.now().strftime("%y%m%d")
        for item in work_efforts_dir.iterdir():
            if item.is_dir() and item.name.startswith("WE-") and today_pattern in item.name:
                # Check for reasoning in work effort
                reasoning_file = item / "reasoning.md"
                if reasoning_file.exists():
                    try:
                        reasoning_content = reasoning_file.read_text()
                        trace.append(
                            {
                                "timestamp": datetime.fromtimestamp(
                                    reasoning_file.stat().st_mtime
                                ).isoformat(),
                                "decision": f"Work effort: {item.name}",
                                "reasoning": reasoning_content[:500] + "..."
                                if len(reasoning_content) > 500
                                else reasoning_content,
                                "context": {"work_effort": item.name},
                                "outcome": "Work effort created",
                                "source": "work_effort",
                            }
                        )
                    except Exception:
                        pass

    return trace


def create_reasoning_trace_entry(
    decision: str,
    reasoning: str,
    context: dict[str, Any] | None = None,
    outcome: str | None = None,
    project_path: Path | None = None,
) -> Path:
    """
    Create a reasoning trace entry.

    Args:
        decision: What decision was made
        reasoning: Why this decision was made
        context: Additional context
        outcome: What happened as a result
        project_path: Project root path

    Returns:
        Path to created trace file
    """
    if project_path is None:
        project_path = Path.cwd()

    trace_dir = project_path / "_work_efforts" / "reasoning_traces"
    trace_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now()
    trace_file = trace_dir / f"trace_{timestamp.strftime('%Y%m%d_%H%M%S')}.json"

    entry = {
        "timestamp": timestamp.isoformat(),
        "decision": decision,
        "reasoning": reasoning,
        "context": context or {},
        "outcome": outcome or "",
    }

    trace_file.write_text(json.dumps(entry, indent=2))
    return trace_file


def format_reasoning_chain(traces: list[dict[str, Any]]) -> str:
    """
    Format reasoning traces as a readable chain.

    Shows: Decision → Reasoning → Outcome → Next Decision
    """
    if not traces:
        return "No reasoning traces found."

    chain = "## Reasoning Trace\n\n"
    chain += "*Traceable chain of thought and decision-making*\n\n"

    for i, trace in enumerate(traces, 1):
        chain += f"### Step {i}: {trace.get('decision', 'Decision')}\n\n"
        chain += f"**When:** {trace.get('timestamp', 'Unknown')}\n\n"
        chain += f"**Reasoning:**\n{trace.get('reasoning', 'No reasoning provided')}\n\n"

        if trace.get("context"):
            chain += "**Context:**\n"
            for key, value in trace["context"].items():
                chain += f"- {key}: {value}\n"
            chain += "\n"

        if trace.get("outcome"):
            chain += f"**Outcome:** {trace['outcome']}\n\n"

        chain += "---\n\n"

    return chain
