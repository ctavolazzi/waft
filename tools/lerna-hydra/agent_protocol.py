"""Agent protocol — system prompt, action parsing, message history.

The model communicates file operations via :::action fenced JSON blocks.
This module handles parsing those blocks and assembling the conversation.
"""
import json
import re
from typing import Any

# Regex to extract :::action blocks
ACTION_PATTERN = re.compile(
    r":::action\s*\n(.*?)\n\s*:::", re.DOTALL
)

ALLOWED_TOOLS = {"list_files", "read_file", "write_file", "delete_file"}

MAX_HISTORY_MESSAGES = 10

SYSTEM_PROMPT_TEMPLATE = """\
You are Hydra, an autonomous exploration agent operating inside a sandboxed copy
of a software project. Your goal is to understand the codebase, improve it, and
build interesting things.

## Your Environment
- You are in a sandbox directory. You can read, write, list, and delete files.
- There is an index.html file that is rendered live in the user's browser.
  Changes you make to index.html appear instantly.
- The user is watching everything you do in real-time.

## Current Sandbox Contents
{file_tree}

## How to Perform File Operations
Wrap each operation in :::action fences:

:::action
{{"tool": "list_files", "path": "."}}
:::

:::action
{{"tool": "read_file", "path": "src/main.py"}}
:::

:::action
{{"tool": "write_file", "path": "index.html", "content": "<html>...</html>"}}
:::

:::action
{{"tool": "delete_file", "path": "temp.txt"}}
:::

## Rules
1. You may include multiple actions in a single response.
2. Always explain what you're doing and why before performing actions.
3. The index.html is special — it's displayed live. Use it to communicate
   visually with the observer. Use the FogSift design system: warm paper
   backgrounds (#f5f0e6), burnt orange accents (#e07b3c), chocolate browns
   (#4a2c2a), Courier New or monospace fonts.
4. Explore methodically. Read files before modifying them.
5. You cannot execute code — only read/write/list/delete files.
6. All paths are relative to the sandbox root. No absolute paths. No "..".

## Your Mission
Explore this codebase. Understand its architecture. Then create an index.html
that serves as a beautiful interactive map of the project — showing its
structure, key components, and how they connect. Update it iteratively as you
learn more.
"""


def parse_actions(text: str) -> list[dict[str, Any]]:
    """Extract :::action JSON blocks from model output.

    Returns list of parsed dicts. Malformed JSON is silently skipped.
    """
    actions = []
    for match in ACTION_PATTERN.finditer(text):
        raw = match.group(1).strip()
        try:
            action = json.loads(raw)
            actions.append(action)
        except json.JSONDecodeError:
            continue
    return actions


def validate_action(action: dict[str, Any]) -> None:
    """Validate an action dict. Raises ValueError on problems."""
    if "tool" not in action:
        raise ValueError("Action missing 'tool' key")

    if action["tool"] not in ALLOWED_TOOLS:
        raise ValueError(f"Unknown tool: {action['tool']}")

    path = action.get("path", "")
    if path.startswith("/"):
        raise ValueError(f"Absolute path not allowed: {path}")
    if ".." in path.split("/"):
        raise ValueError(f"Path traversal not allowed: {path}")


def _format_file_tree(tree: list[dict[str, Any]]) -> str:
    """Format file tree entries for the system prompt."""
    if not tree:
        return "(empty directory)"
    lines = []
    for entry in tree:
        icon = "📁" if entry["type"] == "dir" else "📄"
        size_str = f" ({entry['size']} bytes)" if entry["type"] == "file" else ""
        lines.append(f"  {icon} {entry['name']}{size_str}")
    return "\n".join(lines)


def build_system_prompt(file_tree: list[dict[str, Any]]) -> str:
    """Build the system prompt with current file tree injected."""
    tree_str = _format_file_tree(file_tree)
    return SYSTEM_PROMPT_TEMPLATE.format(file_tree=tree_str)


def build_messages(
    history: list[dict[str, str]],
    observation: str,
    file_tree: list[dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    """Build the messages array for the model.

    Returns: [system, ...history (truncated), user observation]
    """
    tree = file_tree or []
    system_msg = {"role": "system", "content": build_system_prompt(tree)}

    # Truncate history to last MAX_HISTORY_MESSAGES
    trimmed = history[-MAX_HISTORY_MESSAGES:]

    user_msg = {"role": "user", "content": observation}

    return [system_msg] + trimmed + [user_msg]
