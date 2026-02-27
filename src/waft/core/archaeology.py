"""
Archaeology — Mine dungeon run data for patterns and insights.

Analyzes all saved runs to find: deadliest monsters, hardest seeds,
optimal strategies, and behavioral patterns. Stores insights as
messages via the shared MessageStore for other systems to consume.
"""

from collections import Counter
from pathlib import Path

from .datastore import MessageStore, load_all_dungeon_runs

# --- Constants ---

INSIGHTS_SUBDIRECTORY = "insights"
ARCHAEOLOGY_AUTHOR = "the-archaeologist"


def analyze(project_path: Path) -> dict:
    """
    Run full archaeological analysis on all dungeon data.

    Returns a dict of insights, and posts them to the message store.
    """
    runs = load_all_dungeon_runs(project_path)
    if not runs:
        return {"total_runs": 0, "insights": []}

    insights = {}
    insights["total_runs"] = len(runs)
    insights["monster_kills"] = _analyze_monsters(runs)
    insights["seed_difficulty"] = _analyze_seeds(runs)
    insights["death_analysis"] = _analyze_deaths(runs)
    insights["agent_comparison"] = _analyze_agents(runs)
    insights["treasure_analysis"] = _analyze_treasure(runs)

    # Generate human-readable insights
    readable = _generate_readable_insights(insights)
    insights["readable"] = readable

    # Post insights as messages
    store = MessageStore(project_path, subdirectory=INSIGHTS_SUBDIRECTORY)
    for text in readable:
        store.post(
            author=ARCHAEOLOGY_AUTHOR,
            text=text,
            tags=["archaeology", "insight"],
        )

    return insights


def _analyze_monsters(runs: list[dict]) -> dict:
    """Which monsters kill the most agents?"""
    kill_counts = Counter()
    encounter_counts = Counter()

    for run in runs:
        for event in run.get("events", []):
            etype = event.get("event_type", "")
            data = event.get("data", {})

            if etype == "encounter":
                name = data.get("monster", "")
                if name:
                    encounter_counts[name] += 1

            if etype == "combat_loss":
                name = data.get("monster", "")
                if name:
                    kill_counts[name] += 1

    return {
        "deadliest": kill_counts.most_common(3),
        "most_encountered": encounter_counts.most_common(3),
        "kill_counts": dict(kill_counts),
        "encounter_counts": dict(encounter_counts),
    }


def _analyze_seeds(runs: list[dict]) -> dict:
    """Which seeds are hardest/easiest?"""
    seed_outcomes = {}
    for run in runs:
        seed = run.get("seed", 0)
        outcome = run.get("outcome", "?")
        if seed not in seed_outcomes:
            seed_outcomes[seed] = {"escaped": 0, "died": 0, "timeout": 0}
        if outcome in seed_outcomes[seed]:
            seed_outcomes[seed][outcome] += 1

    deadliest = sorted(
        seed_outcomes.items(),
        key=lambda x: x[1].get("died", 0),
        reverse=True,
    )[:5]

    safest = sorted(
        seed_outcomes.items(),
        key=lambda x: x[1].get("escaped", 0),
        reverse=True,
    )[:5]

    return {
        "deadliest_seeds": [
            {"seed": s, **counts} for s, counts in deadliest
        ],
        "safest_seeds": [
            {"seed": s, **counts} for s, counts in safest
        ],
    }


def _analyze_deaths(runs: list[dict]) -> dict:
    """When and how do agents die?"""
    death_turns = []
    death_causes = Counter()

    for run in runs:
        if run.get("outcome") != "died":
            continue
        death_turns.append(run.get("turns", 0))

        for event in run.get("events", []):
            if event.get("event_type") == "combat_loss":
                monster = event.get("data", {}).get("monster", "unknown")
                death_causes[monster] += 1

    avg_death_turn = (
        sum(death_turns) / len(death_turns) if death_turns else 0
    )

    return {
        "total_deaths": len(death_turns),
        "avg_death_turn": avg_death_turn,
        "death_causes": dict(death_causes),
        "earliest_death": min(death_turns) if death_turns else 0,
        "latest_death": max(death_turns) if death_turns else 0,
    }


def _analyze_agents(runs: list[dict]) -> dict:
    """Compare agent performance."""
    agents = {}
    for run in runs:
        aid = run.get("agent_id", "unknown")
        if aid not in agents:
            agents[aid] = {"escaped": 0, "died": 0, "total": 0, "gold": 0}
        agents[aid]["total"] += 1
        if run.get("outcome") == "escaped":
            agents[aid]["escaped"] += 1
        elif run.get("outcome") == "died":
            agents[aid]["died"] += 1
        agents[aid]["gold"] += run.get("gold", 0)

    ranked = sorted(
        agents.items(),
        key=lambda x: x[1]["escaped"] / max(x[1]["total"], 1),
        reverse=True,
    )

    return {"agents": dict(ranked)}


def _analyze_treasure(runs: list[dict]) -> dict:
    """Treasure economy analysis."""
    total_gold = sum(r.get("gold", 0) for r in runs)
    gold_per_escape = []
    for run in runs:
        if run.get("outcome") == "escaped":
            gold_per_escape.append(run.get("gold", 0))

    return {
        "total_gold_found": total_gold,
        "avg_gold_per_escape": (
            sum(gold_per_escape) / len(gold_per_escape)
            if gold_per_escape
            else 0
        ),
        "richest_run_gold": max(gold_per_escape) if gold_per_escape else 0,
    }


def _generate_readable_insights(data: dict) -> list[str]:
    """Turn raw analysis into human-readable insight strings."""
    insights = []

    # Monster insights
    monsters = data.get("monster_kills", {})
    deadliest = monsters.get("deadliest", [])
    if deadliest:
        name, count = deadliest[0]
        enc = monsters.get("encounter_counts", {}).get(name, 0)
        rate = count / enc if enc else 0
        insights.append(
            f"The {name} is the deadliest monster "
            f"({count} kills in {enc} encounters, "
            f"{rate:.0%} kill rate)."
        )

    # Death insights
    deaths = data.get("death_analysis", {})
    avg_turn = deaths.get("avg_death_turn", 0)
    if avg_turn:
        insights.append(
            f"Average death occurs on turn {avg_turn:.1f}. "
            f"Earliest: turn {deaths.get('earliest_death', '?')}, "
            f"latest: turn {deaths.get('latest_death', '?')}."
        )

    # Seed insights
    seeds = data.get("seed_difficulty", {})
    deadliest_seeds = seeds.get("deadliest_seeds", [])
    if deadliest_seeds:
        worst = deadliest_seeds[0]
        insights.append(
            f"Seed {worst['seed']} is the deadliest "
            f"({worst.get('died', 0)} deaths, "
            f"{worst.get('escaped', 0)} escapes)."
        )

    safest_seeds = seeds.get("safest_seeds", [])
    if safest_seeds:
        best = safest_seeds[0]
        insights.append(
            f"Seed {best['seed']} is the safest "
            f"({best.get('escaped', 0)} escapes, "
            f"{best.get('died', 0)} deaths)."
        )

    # Treasure
    treasure = data.get("treasure_analysis", {})
    avg_gold = treasure.get("avg_gold_per_escape", 0)
    if avg_gold:
        insights.append(
            f"Escaping agents earn {avg_gold:.0f} gold on average. "
            f"Richest single run: {treasure.get('richest_run_gold', 0)} gold."
        )

    # Agent comparison
    agents = data.get("agent_comparison", {}).get("agents", {})
    if len(agents) > 1:
        best_agent = next(iter(agents))
        best_data = agents[best_agent]
        rate = best_data["escaped"] / max(best_data["total"], 1)
        insights.append(
            f"Best agent: {best_agent} "
            f"({rate:.0%} escape rate, "
            f"{best_data['total']} runs)."
        )

    return insights
