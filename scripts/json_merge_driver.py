#!/usr/bin/env python3
"""
TavernKeeper Semantic JSON Merge Driver

Performs a 3-way semantic merge on chronicles.json to handle concurrent
game state updates from different branches.

Usage:
    python3 scripts/json_merge_driver.py <ancestor> <ours> <theirs>

This script is configured as a Git merge driver in .gitattributes:
    chronicles.json merge=tavern-json-driver

And in .git/config:
    [merge "tavern-json-driver"]
        name = TavernKeeper Semantic JSON Merger
        driver = python3 scripts/json_merge_driver.py %O %A %B
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Set


def load_json_file(path: str) -> Dict[str, Any]:
    """Load JSON file, return empty dict if file doesn't exist or is invalid."""
    try:
        if not Path(path).exists():
            return {}
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def merge_user_stats(base: Dict[str, Any], ours: Dict[str, Any], theirs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge user stats using Operational Transformation.

    Formula: final = base + (ours - base) + (theirs - base)
    This ensures deltas from both branches are applied.
    """
    merged = base.copy()

    # Get all user IDs from all three versions
    all_user_ids = set(base.keys()) | set(ours.keys()) | set(theirs.keys())

    for user_id in all_user_ids:
        base_user = base.get(user_id, {})
        our_user = ours.get(user_id, {})
        their_user = theirs.get(user_id, {})

        # Merge scalar fields (XP, Credits, etc.)
        merged_user = base_user.copy()

        for field in ["insight", "credits", "integrity", "level"]:
            base_val = base_user.get(field, 0)
            our_val = our_user.get(field, base_val)
            their_val = their_user.get(field, base_val)

            # Apply delta transformation
            our_delta = our_val - base_val
            their_delta = their_val - base_val
            merged_user[field] = base_val + our_delta + their_delta

        # Merge ability scores (take maximum of any changes)
        if "ability_scores" in our_user or "ability_scores" in their_user:
            merged_abilities = base_user.get("ability_scores", {}).copy()
            our_abilities = our_user.get("ability_scores", {})
            their_abilities = their_user.get("ability_scores", {})

            for ability in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
                base_ability = merged_abilities.get(ability, 8)
                our_ability = our_abilities.get(ability, base_ability)
                their_ability = their_abilities.get(ability, base_ability)
                # Take the maximum (assuming ability score increases are improvements)
                merged_abilities[ability] = max(base_ability, our_ability, their_ability)

            merged_user["ability_scores"] = merged_abilities

        # Merge other fields (take latest timestamp, etc.)
        for field in ["created_at", "updated_at"]:
            timestamps = []
            if field in base_user:
                timestamps.append(base_user[field])
            if field in our_user:
                timestamps.append(our_user[field])
            if field in their_user:
                timestamps.append(their_user[field])
            if timestamps:
                merged_user[field] = max(timestamps)

        merged[user_id] = merged_user

    return merged


def merge_lists(base: List[Any], ours: List[Any], theirs: List[Any]) -> List[Any]:
    """
    Merge lists by identifying new entries.

    Strategy:
    1. Keep all base entries
    2. Add entries from ours that aren't in base
    3. Add entries from theirs that aren't in base
    4. Sort by timestamp if available
    """
    # Convert to sets of JSON strings for comparison
    base_set = {json.dumps(item, sort_keys=True) for item in base}
    our_new = [item for item in ours if json.dumps(item, sort_keys=True) not in base_set]
    their_new = [item for item in theirs if json.dumps(item, sort_keys=True) not in base_set]

    merged = base + our_new + their_new

    # Sort by timestamp if available
    try:
        merged.sort(key=lambda x: x.get("timestamp", ""))
    except (KeyError, TypeError):
        pass

    return merged


def merge_chronicles(base: Dict[str, Any], ours: Dict[str, Any], theirs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Perform semantic 3-way merge on chronicles.json.

    Args:
        base: Ancestor version
        ours: Current version
        theirs: Incoming version

    Returns:
        Merged version
    """
    merged = {}

    # Merge character (single character per repo)
    if "character" in ours or "character" in theirs:
        base_char = base.get("character", {})
        our_char = ours.get("character", base_char)
        their_char = theirs.get("character", base_char)

        # For character, take the one with higher level/insight (more progress)
        if our_char.get("level", 0) >= their_char.get("level", 0):
            merged["character"] = our_char.copy()
            # But merge stats using OT
            for field in ["insight", "credits", "integrity"]:
                base_val = base_char.get(field, 0)
                our_val = our_char.get(field, base_val)
                their_val = their_char.get(field, base_val)
                our_delta = our_val - base_val
                their_delta = their_val - base_val
                merged["character"][field] = base_val + our_delta + their_delta
        else:
            merged["character"] = their_char.copy()
            for field in ["insight", "credits", "integrity"]:
                base_val = base_char.get(field, 0)
                our_val = our_char.get(field, base_val)
                their_val = their_char.get(field, base_val)
                our_delta = our_val - base_val
                their_delta = their_val - base_val
                merged["character"][field] = base_val + our_delta + their_delta

    # Merge status effects (list)
    base_effects = base.get("status_effects", [])
    our_effects = ours.get("status_effects", [])
    their_effects = theirs.get("status_effects", [])
    merged["status_effects"] = merge_lists(base_effects, our_effects, their_effects)

    # Merge adventure journal (list)
    base_journal = base.get("adventure_journal", [])
    our_journal = ours.get("adventure_journal", [])
    their_journal = theirs.get("adventure_journal", [])
    merged["adventure_journal"] = merge_lists(base_journal, our_journal, their_journal)

    # Merge quests (list)
    base_quests = base.get("quests", [])
    our_quests = ours.get("quests", [])
    their_quests = theirs.get("quests", [])
    merged["quests"] = merge_lists(base_quests, our_quests, their_quests)

    # Merge achievements (set union - achievements are unique IDs)
    base_achievements = set(base.get("achievements", []))
    our_achievements = set(ours.get("achievements", []))
    their_achievements = set(theirs.get("achievements", []))
    merged["achievements"] = sorted(list(base_achievements | our_achievements | their_achievements))

    # Merge tavern_keeper_state (take latest)
    base_state = base.get("tavern_keeper_state", {})
    our_state = ours.get("tavern_keeper_state", base_state)
    their_state = theirs.get("tavern_keeper_state", base_state)

    # Take the one with more wisdom_shared or latest update
    if our_state.get("wisdom_shared", 0) >= their_state.get("wisdom_shared", 0):
        merged["tavern_keeper_state"] = our_state.copy()
    else:
        merged["tavern_keeper_state"] = their_state.copy()

    return merged


def main():
    """Main entry point for merge driver."""
    if len(sys.argv) != 4:
        print("Usage: json_merge_driver.py <ancestor> <ours> <theirs>", file=sys.stderr)
        sys.exit(1)

    ancestor_path = sys.argv[1]
    ours_path = sys.argv[2]
    theirs_path = sys.argv[3]

    # Load all three versions
    base = load_json_file(ancestor_path)
    ours = load_json_file(ours_path)
    theirs = load_json_file(theirs_path)

    # Perform merge
    try:
        merged = merge_chronicles(base, ours, theirs)

        # Write merged result to ours_path (Git expects result there)
        with open(ours_path, "w") as f:
            json.dump(merged, f, indent=2)

        sys.exit(0)
    except Exception as e:
        print(f"Merge failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

