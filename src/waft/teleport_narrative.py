"""
teleport_narrative.py — Prose generator for teleportation events.

Generates narrative text describing a teleportation event in the
Teleport Massive universe (year 2111, teleportation mastered with side effects).

No LLM dependency — template-based with randomized variation.
Deterministic with a seed.

Usage (Python):
    from waft.teleport_narrative import generate_narrative, TeleportEvent

    event = TeleportEvent(
        character="Sam Iker",
        origin="New Los Angeles",
        destination="Phobos Station",
        style="noir_cosmic",
    )
    prose = generate_narrative(event)
    print(prose)

Usage (CLI):
    python3 teleport_narrative.py "Sam Iker" "New Los Angeles" "Phobos Station"
    python3 teleport_narrative.py "Sam Iker" "New LA" "Phobos" --style visceral --seed 42
"""

from __future__ import annotations

import argparse
import json
import random
from dataclasses import dataclass, field
from typing import Literal

Style = Literal["noir_cosmic", "technical", "visceral", "minimal"]


@dataclass
class TeleportEvent:
    character: str
    origin: str
    destination: str
    style: Style = "noir_cosmic"
    seed: int | None = None
    # Optional universe context
    year: int = 2111
    era: str = "Post-Singularity"
    notes: str = ""


# ── Prose templates per style ────────────────────────────────────────────────

_NOIR_COSMIC = [
    (
        "{character} stepped into the pad and let the city eat them. "
        "One moment: {origin}, neon and exhaust. The next — "
        "the cold arithmetic of {destination}, "
        "the stars no closer but somehow more honest. "
        "The Phaseburn left its usual calling card: a metallic taste, "
        "a half-second of not existing. {year}. Still no fix for that."
    ),
    (
        "The teleport signature locked. {origin} dissolved behind {character} "
        "like a half-remembered dream. {destination} assembled itself — "
        "molecule by molecule, or so the technicians insisted. "
        "What actually happened in the gap was something the Federation "
        "had stopped asking about in {year}. "
        "Some questions cost more than the answers are worth."
    ),
    (
        "Three seconds. That's all it took to not be in {origin} anymore. "
        "{character} blinked at {destination}'s grid-lit ceiling. "
        "The side effects: elevated cortisol, microsecond ego death, "
        "and the persistent sense that the version of them that arrived "
        "was close enough. It had to be. "
        "Everyone arrived close enough, in {year}."
    ),
]

_TECHNICAL = [
    (
        "TELEPORT LOG — {year}/{era}\n"
        "Operator: {character}\n"
        "Origin pad: {origin}\n"
        "Destination pad: {destination}\n"
        "Transit duration: 0.003s\n"
        "Phaseburn index: 0.14 (within nominal)\n"
        "Identity hash: VERIFIED\n"
        "Status: ARRIVAL CONFIRMED"
    ),
    (
        "Initiating teleport sequence for {character}. "
        "Origin: {origin}. Destination: {destination}. "
        "Quantum signature captured. Disassembly in progress. "
        "Transit buffer stable. "
        "Reassembly at {destination}: complete. "
        "Arrival timestamp: {year}-standard. Identity coherence: 99.97%. "
        "Phaseburn residual: nominal. Cleared for duty."
    ),
]

_VISCERAL = [
    (
        "{character} came apart. "
        "Not painfully — the suppressants saw to that — but completely. "
        "{origin} was the last thing: the smell of rain on concrete, "
        "a stranger's laugh two streets over. "
        "Then nothing, the way nothing actually is. "
        "Then {destination}: colder, harder, real. "
        "They checked their hands. Still their hands. "
        "Close enough."
    ),
    (
        "The disassembly hit like a held breath finally released. "
        "{character} felt {origin} let go — "
        "the gravity, the air, the specific quality of that light. "
        "The reassembly at {destination} was rougher. "
        "It always was. The body remembered being scattered. "
        "Give it a minute. Give it {year} more years of this "
        "and maybe it stops remembering."
    ),
]

_MINIMAL = [
    "{character}: {origin} → {destination}. Arrived. {year}.",
    "Teleport complete. {character} at {destination}. Origin: {origin}.",
    "{character} left {origin}. Arrived {destination}. No anomalies logged.",
]

_TEMPLATES: dict[Style, list[str]] = {
    "noir_cosmic": _NOIR_COSMIC,
    "technical":   _TECHNICAL,
    "visceral":    _VISCERAL,
    "minimal":     _MINIMAL,
}


# ── Core API ─────────────────────────────────────────────────────────────────

def generate_narrative(event: TeleportEvent) -> str:
    """
    Generate prose for a teleportation event.

    Returns a deterministic string if event.seed is set; otherwise random.
    """
    templates = _TEMPLATES.get(event.style, _NOIR_COSMIC)
    rng = random.Random(event.seed) if event.seed is not None else random.Random()
    template = rng.choice(templates)

    prose = template.format(
        character=event.character,
        origin=event.origin,
        destination=event.destination,
        year=event.year,
        era=event.era,
    )

    if event.notes:
        prose += f"\n\n*Note: {event.notes}*"

    return prose


def generate_from_dict(data: dict) -> str:
    """Convenience wrapper for dict input (useful for CLI/JSON piping)."""
    event = TeleportEvent(
        character=data.get("character", "Unknown"),
        origin=data.get("origin", "Unknown Origin"),
        destination=data.get("destination", "Unknown Destination"),
        style=data.get("style", "noir_cosmic"),
        seed=data.get("seed"),
        year=data.get("year", 2111),
        era=data.get("era", "Post-Singularity"),
        notes=data.get("notes", ""),
    )
    return generate_narrative(event)


def list_styles() -> list[Style]:
    return list(_TEMPLATES.keys())


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate Teleport Massive narrative prose."
    )
    parser.add_argument("character", help="Character name")
    parser.add_argument("origin", help="Origin location")
    parser.add_argument("destination", help="Destination location")
    parser.add_argument("--style", choices=list_styles(), default="noir_cosmic")
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for deterministic output.")
    parser.add_argument("--year", type=int, default=2111)
    parser.add_argument("--notes", default="", help="Optional event notes.")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="Output JSON with prose + metadata.")
    args = parser.parse_args()

    event = TeleportEvent(
        character=args.character,
        origin=args.origin,
        destination=args.destination,
        style=args.style,
        seed=args.seed,
        year=args.year,
        notes=args.notes,
    )

    prose = generate_narrative(event)

    if args.as_json:
        print(json.dumps({
            "prose": prose,
            "character": event.character,
            "origin": event.origin,
            "destination": event.destination,
            "style": event.style,
            "seed": event.seed,
            "year": event.year,
        }, indent=2))
    else:
        print(prose)


if __name__ == "__main__":
    main()
