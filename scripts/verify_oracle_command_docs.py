#!/usr/bin/env python3
"""Fail-fast checks to prevent oracle command doc drift."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ORACLE_DOC = ROOT / ".cursor" / "commands" / "oracle.md"
CONSULT_ALIAS_DOC = ROOT / ".cursor" / "commands" / "consult-the-oracle.md"
KICKOFF_DOC = ROOT / ".cursor" / "commands" / "alrighty-then.md"
SHORT_ALIAS_DOC = ROOT / ".cursor" / "commands" / "aa.md"


def main() -> int:
    errors = []

    if not ORACLE_DOC.exists():
        errors.append(f"Missing file: {ORACLE_DOC}")
    if not CONSULT_ALIAS_DOC.exists():
        errors.append(f"Missing file: {CONSULT_ALIAS_DOC}")
    if not KICKOFF_DOC.exists():
        errors.append(f"Missing file: {KICKOFF_DOC}")
    if not SHORT_ALIAS_DOC.exists():
        errors.append(f"Missing file: {SHORT_ALIAS_DOC}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    oracle = ORACLE_DOC.read_text(encoding="utf-8")
    consult_alias = CONSULT_ALIAS_DOC.read_text(encoding="utf-8")
    kickoff = KICKOFF_DOC.read_text(encoding="utf-8")
    short_alias = SHORT_ALIAS_DOC.read_text(encoding="utf-8")

    required_oracle_phrases = [
        "ThePonderingOne",
        "MCP-first Policy",
        "Brain Realm Status",
        "PROCEED | INVESTIGATE | HALT | BRANCH | REVISE",
    ]
    for phrase in required_oracle_phrases:
        if phrase not in oracle:
            errors.append(f"oracle.md missing required phrase: {phrase}")

    required_consult_alias_phrases = [
        "Alias for `/oracle`.",
        "Source of truth:",
        "calls `waft oracle` internally",
    ]
    for phrase in required_consult_alias_phrases:
        if phrase not in consult_alias:
            errors.append(f"consult-the-oracle.md missing required phrase: {phrase}")

    required_kickoff_phrases = [
        "Kick off the Oracle brain-realm flow in one go.",
        "ThePonderingOne",
        "waft oracle",
    ]
    for phrase in required_kickoff_phrases:
        if phrase not in kickoff:
            errors.append(f"alrighty-then.md missing required phrase: {phrase}")

    required_short_alias_phrases = [
        "Alias for `/alrighty-then`.",
        "Source of truth:",
        "delegates behavior to `/alrighty-then`",
    ]
    for phrase in required_short_alias_phrases:
        if phrase not in short_alias:
            errors.append(f"aa.md missing required phrase: {phrase}")

    if "### Decision Assessment" in consult_alias:
        errors.append(
            "consult-the-oracle.md should remain lightweight and avoid duplicated sections"
        )
    if "## Execution Plan" in short_alias:
        errors.append("aa.md should remain lightweight and avoid duplicated sections")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("OK: oracle command docs are synced and policy-complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
