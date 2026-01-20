# Empirica TUI Dashboard User Manual

## Introduction
This manual explains how to use the Empirica TUI dashboards via `waft empirica monitor`.

## Prerequisites
- Python 3.11+
- Empirica installed: `pip install empirica`
- WAFT project initialized: `waft init`
- Terminal supports ANSI colors (80x24 minimum)
- Windows: `pip install windows-curses`

## Installation & Setup
1. Verify Empirica: `empirica --version`
2. Initialize: `waft init`
3. Create session: `waft session create --ai-id claude-code`
4. Launch: `waft empirica monitor`

## Basic Usage
```
waft empirica monitor
waft empirica monitor --type cascade
waft empirica monitor --type tui
waft empirica monitor --session-id <SESSION_ID>
waft empirica monitor --path /path/to/project
```

## Dashboard Types
- Snapshot Monitor: memory quality and reliability
- CASCADE Monitor: workflow tracking
- TUI Dashboard: full Textual UI

## Interactive Commands (Snapshot Monitor)
- q: Quit
- r: Refresh
- f: Full list toggle
- e: Export snapshot JSON
- d: Details view

## Troubleshooting
- Empirica not installed: `pip install empirica`
- Empirica not initialized: `waft init`
- Missing textual: `pip install textual`
- Missing curses (Windows): `pip install windows-curses`
- Session not found: `waft session status`

## Glossary
- CASCADE: Empirica workflow phases
- Epistemic Vectors: knowledge/uncertainty signals
- Snapshot: saved epistemic state with reliability
