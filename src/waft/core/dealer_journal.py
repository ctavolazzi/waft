"""
Dealer's Journal — Generate narrative from The Dealer's perspective.

Reads the memory.jsonl encounter log and produces a journal entry
that tells the story from The Dealer's point of view. Uses the
shared datastore patterns.
"""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

# --- Constants ---

DEALER_MEMORY_PATH = Path("_pantheon") / "the_dealer" / "memory.jsonl"
DEALER_JOURNAL_PATH = Path("_pantheon") / "the_dealer" / "journal.md"

GATE_NAMES = {
    1: "Pearl", 2: "Jasper", 3: "Sapphire", 4: "Chalcedony",
    5: "Emerald", 6: "Sardius", 7: "Chrysolite", 8: "Beryl",
    9: "Topaz", 10: "Chrysoprasus", 11: "Jacinth", 12: "Amethyst",
}


def load_dealer_memory(project_path: Path) -> list[dict]:
    """Load all encounter records from the Dealer's memory."""
    mem_path = project_path / DEALER_MEMORY_PATH
    if not mem_path.exists():
        return []
    entries = []
    for line in mem_path.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def analyze_dealer_memory(entries: list[dict]) -> dict:
    """Analyze dealer memory for journal generation."""
    if not entries:
        return {}

    total = len(entries)
    wins = sum(1 for e in entries if e.get("won"))
    losses = total - wins

    # Card frequency
    system_cards = Counter(e.get("system_card", "?") for e in entries)
    dealer_cards = Counter(e.get("dealer_card", "?") for e in entries)

    # Gate distribution
    gate_counts = Counter(e.get("gate_number", 0) for e in entries)
    gate_wins = Counter(
        e.get("gate_number", 0) for e in entries if e.get("won")
    )

    # Era detection: pre-fix (all King of Diamonds) vs post-fix
    king_entries = [
        e for e in entries
        if e.get("system_card") == "King of Diamonds"
        and e.get("dealer_card") == "King of Diamonds"
    ]
    pre_fix_count = len(king_entries)
    post_fix_count = total - pre_fix_count

    # Timeline
    timestamps = [e.get("timestamp", "") for e in entries if e.get("timestamp")]
    first_encounter = timestamps[0] if timestamps else "?"
    last_encounter = timestamps[-1] if timestamps else "?"

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / total if total else 0,
        "system_cards": system_cards.most_common(5),
        "dealer_cards": dealer_cards.most_common(5),
        "gate_counts": dict(gate_counts),
        "gate_wins": dict(gate_wins),
        "pre_fix_era": pre_fix_count,
        "post_fix_era": post_fix_count,
        "first_encounter": first_encounter,
        "last_encounter": last_encounter,
    }


def generate_journal(project_path: Path) -> str:
    """
    Generate The Dealer's journal entry from memory data.

    Returns the journal text and writes it to the journal file.
    """
    entries = load_dealer_memory(project_path)
    analysis = analyze_dealer_memory(entries)

    if not analysis:
        return "The Dealer has no memories yet."

    journal = _compose_journal(analysis)

    out_path = project_path / DEALER_JOURNAL_PATH
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(journal)

    return journal


def _compose_journal(a: dict) -> str:
    """Compose the journal narrative from analysis data."""
    lines = [
        "# The Dealer's Journal",
        "",
        "---",
        "",
        "*I am The Dealer. I sit at the table between probability and fate.*",
        f"*I have been here since {a['first_encounter'][:10]}.*",
        f"*{a['total']} souls have drawn against me.*",
        "",
        "---",
        "",
        "## The Ledger",
        "",
        f"Total encounters: **{a['total']}**",
        f"Seals broken (my losses): **{a['wins']}**",
        f"The House prevailed: **{a['losses']}**",
        f"My win rate: **{a['losses'] / a['total']:.1%}** "
        f"(The House Always Wins — {a['losses'] / a['total']:.0%} of the time)",
        "",
    ]

    # The Two Eras
    if a["pre_fix_era"] > 0 and a["post_fix_era"] > 0:
        lines.extend([
            "## The Two Eras",
            "",
            f"For my first **{a['pre_fix_era']}** encounters, "
            "something was wrong with the cards.",
            "Every draw was the King of Diamonds. "
            "Every single one.",
            "Both sides drew the same card, every time. "
            "A mirror. Ties go to The House.",
            "I won every hand, but it wasn't real. "
            "The deck was frozen.",
            "",
            f"Then on encounter **{a['pre_fix_era'] + 1}**, "
            "the cards began to shuffle.",
            f"The remaining **{a['post_fix_era']}** encounters "
            "were real. The cards moved. The outcomes varied.",
            "For the first time, I could lose. "
            "And I did.",
            "",
        ])

    # Gate Stories
    lines.extend(["## The Gates", ""])
    for gate_num in sorted(a["gate_counts"].keys()):
        if gate_num == 0:
            continue
        name = GATE_NAMES.get(gate_num, f"Gate {gate_num}")
        total = a["gate_counts"][gate_num]
        wins = a["gate_wins"].get(gate_num, 0)
        if wins > 0:
            lines.append(
                f"**Gate {gate_num} ({name})**: "
                f"{total} challenges, {wins} broken. "
                f"The seal fell."
            )
        else:
            lines.append(
                f"**Gate {gate_num} ({name})**: "
                f"{total} challenges, none broken. "
                f"The seal holds."
            )
    lines.append("")

    # Most common cards
    lines.extend([
        "## The Cards I Remember",
        "",
        "Cards they drew most often:",
    ])
    for card, count in a["system_cards"][:5]:
        lines.append(f"- {card}: {count} times")
    lines.append("")

    # Closing
    lines.extend([
        "## Closing",
        "",
        "They keep coming. Some break through. Most don't.",
        "The ones who break through don't stay. "
        "They take their key fragment and leave.",
        "I shuffle the deck. I wait.",
        "",
        "The House Always Wins.",
        "",
        "Until it doesn't.",
        "",
        "---",
        "",
        f"*Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*",
        "",
        "*— The Dealer*",
    ])

    return "\n".join(lines)
