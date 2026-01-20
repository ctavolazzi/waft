#!/usr/bin/env python3
"""
Generate Pantheon UI in Multiple Template Styles
Creates alternative template versions of the Pantheon web page.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

from weasyprint import HTML

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def load_pantheon_data():
    """Load actual Pantheon data from _pantheon directory."""
    project_path = Path(__file__).parent.parent
    pantheon_path = project_path / "_pantheon"

    data = {}

    # Magistrate data
    magistrate_path = pantheon_path / "magistrate" / "body_of_proof.json"
    if magistrate_path.exists():
        with open(magistrate_path) as f:
            magistrate_data = json.load(f)
            data["magistrate"] = {
                "precedents": len(magistrate_data.get("precedents", [])),
                "cases": len(magistrate_data.get("precedents", [])),
            }

    # Judge data
    judge_path = pantheon_path / "judge" / "judgment_history.json"
    if judge_path.exists():
        with open(judge_path) as f:
            judge_data = json.load(f)
            data["judge"] = {"judgments": len(judge_data.get("judgments", []))}

    # Reasoner data
    reasoner_path = pantheon_path / "reasoner" / "trace_index.json"
    if reasoner_path.exists():
        with open(reasoner_path) as f:
            reasoner_data = json.load(f)
            data["reasoner"] = {"traces": len(reasoner_data.get("traces", []))}

    # GitHub God data
    github_path = pantheon_path / "github_god" / "rollup_index.json"
    if github_path.exists():
        with open(github_path) as f:
            github_data = json.load(f)
            data["github_god"] = {"rollups": len(github_data.get("rollups", []))}

    return data


def create_dnd_template():
    """Create D&D Character Sheet style template."""
    return (
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Pantheon - WAFT Gods</title>
    <style>
        @page {
            size: letter;
            margin: 0.5in;
            background: #f4e8d0;
        }

        body {
            font-family: 'Times New Roman', 'Times', 'Georgia', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #3d2817;
            background: #f4e8d0;
            margin: 0;
            padding: 0.5in;
        }

        .container {
            background: #faf5eb;
            border: 3px double #8b4513;
            padding: 0.5in;
            box-shadow: 0 0 15px rgba(139, 69, 19, 0.3);
        }

        h1 {
            font-size: 32pt;
            font-weight: bold;
            margin: 0 0 0.3in 0;
            color: #8b0000;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
            border-bottom: 4px double #8b4513;
            padding-bottom: 0.2in;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .subtitle {
            text-align: center;
            font-size: 14pt;
            color: #654321;
            margin-bottom: 0.4in;
            font-style: italic;
        }

        .pantheon-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.3in;
            margin-bottom: 0.3in;
        }

        .god-card {
            background: #fff;
            border: 2px solid #8b4513;
            padding: 0.3in;
            page-break-inside: avoid;
        }

        .god-header {
            border-bottom: 2px solid #8b4513;
            padding-bottom: 0.1in;
            margin-bottom: 0.15in;
        }

        .god-name {
            font-size: 16pt;
            font-weight: bold;
            color: #8b0000;
            text-transform: uppercase;
        }

        .god-title {
            font-size: 10pt;
            color: #654321;
            font-weight: bold;
            margin: 0.1in 0;
            text-transform: uppercase;
        }

        .god-description {
            font-size: 9pt;
            line-height: 1.5;
            color: #3d2817;
            margin: 0.1in 0;
        }

        .god-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.1in;
            margin: 0.15in 0;
        }

        .stat-item {
            border: 1px solid #8b4513;
            padding: 0.1in;
            background: #f0e6d2;
        }

        .stat-label {
            font-size: 8pt;
            font-weight: bold;
            text-transform: uppercase;
            color: #654321;
            border-bottom: 1px solid #8b4513;
            padding-bottom: 2pt;
            margin-bottom: 4pt;
        }

        .stat-value {
            font-size: 14pt;
            font-weight: bold;
            text-align: center;
            color: #8b0000;
        }

        .god-abilities {
            margin-top: 0.15in;
            padding-top: 0.15in;
            border-top: 1px solid #8b4513;
        }

        .abilities-title {
            font-size: 9pt;
            font-weight: bold;
            text-transform: uppercase;
            color: #654321;
            margin-bottom: 0.1in;
        }

        .abilities-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.05in;
        }

        .ability-badge {
            background: #8b4513;
            color: #faf5eb;
            padding: 4pt 8pt;
            border: 1px solid #654321;
            font-size: 8pt;
            font-weight: bold;
        }

        .footer {
            text-align: center;
            margin-top: 0.4in;
            padding-top: 0.2in;
            border-top: 2px solid #8b4513;
            font-size: 9pt;
            color: #654321;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏛️ The Pantheon</h1>
        <div class="subtitle">Higher Beings System • WAFT Gods</div>

        <div class="pantheon-grid" id="pantheon-grid">
            <!-- Gods populated by JavaScript -->
        </div>

        <div class="footer">
            <p>WAFT Pantheon • Timeless Forces that Bind Reality Together</p>
            <p>"As above, so below"</p>
        </div>
    </div>

    <script>
        const pantheonGods = """
        + json.dumps(
            [
                {
                    "name": "Magistrate",
                    "icon": "⚖️",
                    "title": "God of Precedent and Body of Proof",
                    "description": "Organizes proof cases from _work_efforts/proof_cases/ into Precedent categories, building a Body of Proof over time.",
                    "abilities": [
                        "organize_all_cases",
                        "search_precedents",
                        "get_body_of_proof_summary",
                    ],
                    "status": "active",
                    "stats": {"Precedents": "2", "Cases": "2"},
                },
                {
                    "name": "Judge",
                    "icon": "👨‍⚖️",
                    "title": "God of Judgment and Evaluation",
                    "description": "Evaluates organization claims and references the Magistrate's Body of Proof.",
                    "abilities": ["evaluate_claim", "get_judgment_history", "get_judgment_summary"],
                    "status": "active",
                    "stats": {"Judgments": "2"},
                },
                {
                    "name": "The Reasoner",
                    "icon": "🧠",
                    "title": "God of Reasoning Traces",
                    "description": "Maintains traceable reasoning chains showing the 'why' behind decisions.",
                    "abilities": [
                        "create_trace",
                        "get_recent_traces",
                        "build_chain",
                        "search_traces",
                    ],
                    "status": "active",
                    "stats": {"Traces": "1"},
                },
                {
                    "name": "The GitHub God",
                    "icon": "🐙",
                    "title": "God of Repository Management",
                    "description": "Maintains repository state, generates rollups, and tracks GitHub operations.",
                    "abilities": ["generate_rollup", "get_repository_state", "get_branch_summary"],
                    "status": "active",
                    "stats": {"Rollups": "7", "Operations": "1"},
                },
                {
                    "name": "The Steward",
                    "icon": "💎",
                    "title": "God of Work Efforts",
                    "description": "The divine intelligence that locks, monitors, organizes, and initiates evolutionary cycles.",
                    "abilities": [
                        "/think",
                        "/evolve",
                        "/monitor",
                        "/organize",
                        "/lock",
                        "/unlock",
                        "/status",
                        "/secrets",
                    ],
                    "status": "active",
                    "stats": {"System": "pyrite"},
                },
                {
                    "name": "Librarian",
                    "icon": "📚",
                    "title": "God of Knowledge and Cataloging",
                    "description": "Maintains catalogs and reports. Organizes knowledge and documentation.",
                    "abilities": ["catalog", "organize_reports"],
                    "status": "active",
                    "stats": {"Catalog Items": "1", "Reports": "1"},
                },
                {
                    "name": "Military Brass",
                    "icon": "🎖️",
                    "title": "God of Missions and Operations",
                    "description": "Manages missions and briefings. Coordinates military-style operations.",
                    "abilities": ["create_mission", "get_briefings", "missions_registry"],
                    "status": "active",
                    "stats": {"Missions": "2"},
                },
                {
                    "name": "Mission Control",
                    "icon": "🚀",
                    "title": "God of Realm Exploration",
                    "description": "Controls realm scouting and colonization operations.",
                    "abilities": ["realm_scout", "get_realm_status", "control_registry"],
                    "status": "active",
                    "stats": {"Realm Scouts": "3"},
                },
                {
                    "name": "Fae",
                    "icon": "🧚",
                    "title": "God of Quests",
                    "description": "Manages quests and quest registry. Coordinates quest-based activities.",
                    "abilities": ["create_quest", "get_quests", "quests_registry"],
                    "status": "active",
                    "stats": {"Quests": "Active"},
                },
                {
                    "name": "The Village",
                    "icon": "🏘️",
                    "title": "God of Community",
                    "description": "Manages village registry and community activities.",
                    "abilities": ["village_registry"],
                    "status": "active",
                    "stats": {},
                },
                {
                    "name": "Test Runner",
                    "icon": "🧪",
                    "title": "God of Testing",
                    "description": "Manages test execution and test metadata.",
                    "abilities": ["run_tests", "test_metadata"],
                    "status": "active",
                    "stats": {},
                },
                {
                    "name": "External Drive Realm",
                    "icon": "💾",
                    "title": "God of External Storage",
                    "description": "Manages external drive realm content and storage routing.",
                    "abilities": ["content_manifest", "realm_registry", "realm_status"],
                    "status": "active",
                    "stats": {"Content Items": "1"},
                },
            ]
        )
        + """;

        function renderPantheon() {
            const grid = document.getElementById('pantheon-grid');
            grid.innerHTML = pantheonGods.map(god => `
                <div class="god-card">
                    <div class="god-header">
                        <div class="god-name">${god.icon} ${god.name}</div>
                    </div>
                    <div class="god-title">${god.title}</div>
                    <div class="god-description">${god.description}</div>
                    ${Object.keys(god.stats).length > 0 ? `
                        <div class="god-stats">
                            ${Object.entries(god.stats).map(([k, v]) => `
                                <div class="stat-item">
                                    <div class="stat-label">${k}</div>
                                    <div class="stat-value">${v}</div>
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                    ${god.abilities ? `
                        <div class="god-abilities">
                            <div class="abilities-title">Abilities</div>
                            <div class="abilities-list">
                                ${god.abilities.map(a => `<span class="ability-badge">${a}</span>`).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }

        renderPantheon();
    </script>
</body>
</html>
    """
    )


def create_field_guide_template():
    """Create Field Guide style template."""
    return (
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Pantheon - Field Guide</title>
    <style>
        @page {
            size: letter;
            margin: 0.75in 0.5in;
        }

        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #000;
        }

        .cover {
            border: 4px double #000;
            padding: 0.5in;
            margin-bottom: 0.3in;
            background: #f5f5f5;
            text-align: center;
        }

        .series-number {
            font-family: 'Courier New', monospace;
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 0.2in;
        }

        .title {
            font-family: 'Arial Black', sans-serif;
            font-size: 24pt;
            font-weight: bold;
            text-transform: uppercase;
            margin-bottom: 0.2in;
        }

        .god-entry {
            border: 2px solid #000;
            padding: 0.2in;
            margin-bottom: 0.2in;
            page-break-inside: avoid;
        }

        .god-name {
            font-size: 14pt;
            font-weight: bold;
            text-transform: uppercase;
            border-bottom: 2px solid #000;
            padding-bottom: 0.1in;
            margin-bottom: 0.1in;
        }

        .god-title {
            font-size: 11pt;
            font-weight: bold;
            margin-bottom: 0.1in;
        }

        .god-description {
            font-size: 9pt;
            margin-bottom: 0.1in;
        }

        .stat-block {
            background: #f0f0f0;
            border: 1px solid #000;
            padding: 0.1in;
            margin: 0.1in 0;
            font-family: 'Courier New', monospace;
            font-size: 8pt;
        }

        .abilities {
            margin-top: 0.1in;
            padding-top: 0.1in;
            border-top: 1px solid #000;
        }

        .ability-tag {
            display: inline-block;
            background: #000;
            color: #fff;
            padding: 2pt 6pt;
            margin: 2pt;
            font-size: 8pt;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="cover">
        <div class="series-number">FIELD GUIDE FG-PANTHEON-001</div>
        <div class="title">The Pantheon</div>
        <div style="font-size: 12pt; margin-top: 0.2in;">Higher Beings System • WAFT Gods</div>
    </div>

    <div id="pantheon-content">
        <!-- Gods populated by JavaScript -->
    </div>

    <script>
        const pantheonGods = """
        + json.dumps(
            [
                {
                    "name": "Magistrate",
                    "icon": "⚖️",
                    "title": "God of Precedent and Body of Proof",
                    "description": "Organizes proof cases from _work_efforts/proof_cases/ into Precedent categories, building a Body of Proof over time.",
                    "abilities": [
                        "organize_all_cases",
                        "search_precedents",
                        "get_body_of_proof_summary",
                    ],
                    "status": "active",
                    "stats": {"Precedents": "2", "Cases": "2"},
                },
                {
                    "name": "Judge",
                    "icon": "👨‍⚖️",
                    "title": "God of Judgment and Evaluation",
                    "description": "Evaluates organization claims and references the Magistrate's Body of Proof.",
                    "abilities": ["evaluate_claim", "get_judgment_history", "get_judgment_summary"],
                    "status": "active",
                    "stats": {"Judgments": "2"},
                },
                {
                    "name": "The Reasoner",
                    "icon": "🧠",
                    "title": "God of Reasoning Traces",
                    "description": "Maintains traceable reasoning chains showing the 'why' behind decisions.",
                    "abilities": [
                        "create_trace",
                        "get_recent_traces",
                        "build_chain",
                        "search_traces",
                    ],
                    "status": "active",
                    "stats": {"Traces": "1"},
                },
                {
                    "name": "The GitHub God",
                    "icon": "🐙",
                    "title": "God of Repository Management",
                    "description": "Maintains repository state, generates rollups, and tracks GitHub operations.",
                    "abilities": ["generate_rollup", "get_repository_state", "get_branch_summary"],
                    "status": "active",
                    "stats": {"Rollups": "7", "Operations": "1"},
                },
                {
                    "name": "The Steward",
                    "icon": "💎",
                    "title": "God of Work Efforts",
                    "description": "The divine intelligence that locks, monitors, organizes, and initiates evolutionary cycles.",
                    "abilities": [
                        "/think",
                        "/evolve",
                        "/monitor",
                        "/organize",
                        "/lock",
                        "/unlock",
                        "/status",
                        "/secrets",
                    ],
                    "status": "active",
                    "stats": {"System": "pyrite"},
                },
                {
                    "name": "Librarian",
                    "icon": "📚",
                    "title": "God of Knowledge and Cataloging",
                    "description": "Maintains catalogs and reports. Organizes knowledge and documentation.",
                    "abilities": ["catalog", "organize_reports"],
                    "status": "active",
                    "stats": {"Catalog Items": "1", "Reports": "1"},
                },
                {
                    "name": "Military Brass",
                    "icon": "🎖️",
                    "title": "God of Missions and Operations",
                    "description": "Manages missions and briefings. Coordinates military-style operations.",
                    "abilities": ["create_mission", "get_briefings", "missions_registry"],
                    "status": "active",
                    "stats": {"Missions": "2"},
                },
                {
                    "name": "Mission Control",
                    "icon": "🚀",
                    "title": "God of Realm Exploration",
                    "description": "Controls realm scouting and colonization operations.",
                    "abilities": ["realm_scout", "get_realm_status", "control_registry"],
                    "status": "active",
                    "stats": {"Realm Scouts": "3"},
                },
                {
                    "name": "Fae",
                    "icon": "🧚",
                    "title": "God of Quests",
                    "description": "Manages quests and quest registry. Coordinates quest-based activities.",
                    "abilities": ["create_quest", "get_quests", "quests_registry"],
                    "status": "active",
                    "stats": {"Quests": "Active"},
                },
                {
                    "name": "The Village",
                    "icon": "🏘️",
                    "title": "God of Community",
                    "description": "Manages village registry and community activities.",
                    "abilities": ["village_registry"],
                    "status": "active",
                    "stats": {},
                },
                {
                    "name": "Test Runner",
                    "icon": "🧪",
                    "title": "God of Testing",
                    "description": "Manages test execution and test metadata.",
                    "abilities": ["run_tests", "test_metadata"],
                    "status": "active",
                    "stats": {},
                },
                {
                    "name": "External Drive Realm",
                    "icon": "💾",
                    "title": "God of External Storage",
                    "description": "Manages external drive realm content and storage routing.",
                    "abilities": ["content_manifest", "realm_registry", "realm_status"],
                    "status": "active",
                    "stats": {"Content Items": "1"},
                },
            ]
        )
        + """;

        function renderPantheon() {
            const content = document.getElementById('pantheon-content');
            content.innerHTML = pantheonGods.map(god => `
                <div class="god-entry">
                    <div class="god-name">${god.icon} ${god.name}</div>
                    <div class="god-title">${god.title}</div>
                    <div class="god-description">${god.description}</div>
                    ${Object.keys(god.stats).length > 0 ? `
                        <div class="stat-block">
                            ${Object.entries(god.stats).map(([k, v]) => `${k}: ${v}`).join(' | ')}
                        </div>
                    ` : ''}
                    ${god.abilities ? `
                        <div class="abilities">
                            <strong>ABILITIES:</strong>
                            ${god.abilities.map(a => `<span class="ability-tag">${a}</span>`).join('')}
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }

        renderPantheon();
    </script>
</body>
</html>
    """
    )


def create_academic_template():
    """Create Academic Paper style template."""
    return (
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>The Pantheon: Higher Beings System</title>
    <style>
        @page {
            size: letter;
            margin: 1in;
        }

        body {
            font-family: 'Times New Roman', 'Times', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
            max-width: 100%;
        }

        .title {
            font-size: 18pt;
            font-weight: bold;
            text-align: center;
            margin-bottom: 0.2in;
        }

        .authors {
            text-align: center;
            font-size: 10pt;
            margin-bottom: 0.3in;
            font-style: italic;
        }

        .abstract {
            margin: 0.3in 0;
            padding: 0.2in;
            border: 1px solid #000;
            background: #f9f9f9;
        }

        .abstract-title {
            font-weight: bold;
            margin-bottom: 0.1in;
        }

        .section {
            margin: 0.4in 0;
        }

        .section-title {
            font-size: 14pt;
            font-weight: bold;
            margin-bottom: 0.2in;
            border-bottom: 1px solid #000;
            padding-bottom: 0.05in;
        }

        .god-entry {
            margin: 0.2in 0;
            padding: 0.15in;
            border-left: 3px solid #000;
            background: #f9f9f9;
        }

        .god-name {
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 0.05in;
        }

        .god-title {
            font-style: italic;
            margin-bottom: 0.1in;
        }

        .god-description {
            font-size: 10pt;
            margin-bottom: 0.1in;
        }

        .god-stats {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            margin: 0.1in 0;
        }

        .abilities {
            margin-top: 0.1in;
            font-size: 9pt;
        }

        .ability {
            display: inline-block;
            background: #e0e0e0;
            padding: 2pt 6pt;
            margin: 2pt;
            border: 1px solid #000;
        }
    </style>
</head>
<body>
    <div class="title">The Pantheon: Higher Beings System</div>
    <div class="authors">WAFT Gods • Timeless Forces that Bind Reality Together</div>

    <div class="abstract">
        <div class="abstract-title">Abstract</div>
        <div>The Pantheon houses Higher Beings (Gods) as Aspects of Creation, following "as above, so below" principles from the spiritual cosmology. This document catalogs all Pantheon entities, their responsibilities, abilities, and current operational status.</div>
    </div>

    <div class="section">
        <div class="section-title">1. Introduction</div>
        <div>Pantheon Entities are Timeless Forces that Bind Reality Together. Unlike Beings (which are timeful, dynamic agents), Entities in the Pantheon are stable, maintaining fundamental structure until evidence collected by Beings proves change is needed.</div>
    </div>

    <div class="section">
        <div class="section-title">2. Pantheon Entities</div>
        <div id="pantheon-content">
            <!-- Gods populated by JavaScript -->
        </div>
    </div>

    <script>
        const pantheonGods = """
        + json.dumps(
            [
                {
                    "name": "Magistrate",
                    "icon": "⚖️",
                    "title": "God of Precedent and Body of Proof",
                    "description": "Organizes proof cases from _work_efforts/proof_cases/ into Precedent categories, building a Body of Proof over time.",
                    "abilities": [
                        "organize_all_cases",
                        "search_precedents",
                        "get_body_of_proof_summary",
                    ],
                    "status": "active",
                    "stats": {"Precedents": "2", "Cases": "2"},
                },
                {
                    "name": "Judge",
                    "icon": "👨‍⚖️",
                    "title": "God of Judgment and Evaluation",
                    "description": "Evaluates organization claims and references the Magistrate's Body of Proof.",
                    "abilities": ["evaluate_claim", "get_judgment_history", "get_judgment_summary"],
                    "status": "active",
                    "stats": {"Judgments": "2"},
                },
                {
                    "name": "The Reasoner",
                    "icon": "🧠",
                    "title": "God of Reasoning Traces",
                    "description": "Maintains traceable reasoning chains showing the 'why' behind decisions.",
                    "abilities": [
                        "create_trace",
                        "get_recent_traces",
                        "build_chain",
                        "search_traces",
                    ],
                    "status": "active",
                    "stats": {"Traces": "1"},
                },
                {
                    "name": "The GitHub God",
                    "icon": "🐙",
                    "title": "God of Repository Management",
                    "description": "Maintains repository state, generates rollups, and tracks GitHub operations.",
                    "abilities": ["generate_rollup", "get_repository_state", "get_branch_summary"],
                    "status": "active",
                    "stats": {"Rollups": "7", "Operations": "1"},
                },
                {
                    "name": "The Steward",
                    "icon": "💎",
                    "title": "God of Work Efforts",
                    "description": "The divine intelligence that locks, monitors, organizes, and initiates evolutionary cycles.",
                    "abilities": [
                        "/think",
                        "/evolve",
                        "/monitor",
                        "/organize",
                        "/lock",
                        "/unlock",
                        "/status",
                        "/secrets",
                    ],
                    "status": "active",
                    "stats": {"System": "pyrite"},
                },
                {
                    "name": "Librarian",
                    "icon": "📚",
                    "title": "God of Knowledge and Cataloging",
                    "description": "Maintains catalogs and reports. Organizes knowledge and documentation.",
                    "abilities": ["catalog", "organize_reports"],
                    "status": "active",
                    "stats": {"Catalog Items": "1", "Reports": "1"},
                },
                {
                    "name": "Military Brass",
                    "icon": "🎖️",
                    "title": "God of Missions and Operations",
                    "description": "Manages missions and briefings. Coordinates military-style operations.",
                    "abilities": ["create_mission", "get_briefings", "missions_registry"],
                    "status": "active",
                    "stats": {"Missions": "2"},
                },
                {
                    "name": "Mission Control",
                    "icon": "🚀",
                    "title": "God of Realm Exploration",
                    "description": "Controls realm scouting and colonization operations.",
                    "abilities": ["realm_scout", "get_realm_status", "control_registry"],
                    "status": "active",
                    "stats": {"Realm Scouts": "3"},
                },
                {
                    "name": "Fae",
                    "icon": "🧚",
                    "title": "God of Quests",
                    "description": "Manages quests and quest registry. Coordinates quest-based activities.",
                    "abilities": ["create_quest", "get_quests", "quests_registry"],
                    "status": "active",
                    "stats": {"Quests": "Active"},
                },
                {
                    "name": "The Village",
                    "icon": "🏘️",
                    "title": "God of Community",
                    "description": "Manages village registry and community activities.",
                    "abilities": ["village_registry"],
                    "status": "active",
                    "stats": {},
                },
                {
                    "name": "Test Runner",
                    "icon": "🧪",
                    "title": "God of Testing",
                    "description": "Manages test execution and test metadata.",
                    "abilities": ["run_tests", "test_metadata"],
                    "status": "active",
                    "stats": {},
                },
                {
                    "name": "External Drive Realm",
                    "icon": "💾",
                    "title": "God of External Storage",
                    "description": "Manages external drive realm content and storage routing.",
                    "abilities": ["content_manifest", "realm_registry", "realm_status"],
                    "status": "active",
                    "stats": {"Content Items": "1"},
                },
            ]
        )
        + """;

        function renderPantheon() {
            const content = document.getElementById('pantheon-content');
            content.innerHTML = pantheonGods.map((god, idx) => `
                <div class="god-entry">
                    <div class="god-name">${idx + 1}. ${god.icon} ${god.name}</div>
                    <div class="god-title">${god.title}</div>
                    <div class="god-description">${god.description}</div>
                    ${Object.keys(god.stats).length > 0 ? `
                        <div class="god-stats">
                            Stats: ${Object.entries(god.stats).map(([k, v]) => `${k}=${v}`).join(', ')}
                        </div>
                    ` : ''}
                    ${god.abilities ? `
                        <div class="abilities">
                            <strong>Abilities:</strong>
                            ${god.abilities.map(a => `<span class="ability">${a}</span>`).join('')}
                        </div>
                    ` : ''}
                </div>
            `).join('');
        }

        renderPantheon();
    </script>
</body>
</html>
    """
    )


def create_lab_notes_template():
    """Create Lab Notes style template."""
    return (
        """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pantheon Lab Notes</title>
    <style>
        @page {
            size: letter;
            margin: 0.75in;
            background-image:
                linear-gradient(#e0e0e0 1px, transparent 1px),
                linear-gradient(90deg, #e0e0e0 1px, transparent 1px);
            background-size: 0.2in 0.2in;
        }

        body {
            font-family: 'Courier New', 'Consolas', monospace;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
        }

        .lab-cover {
            border: 3px solid #000;
            padding: 0.4in;
            background: white;
            margin-bottom: 0.3in;
        }

        .lab-id {
            font-weight: bold;
            margin-bottom: 0.15in;
        }

        .lab-title {
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 0.15in;
        }

        .entry {
            margin: 0.3in 0;
            padding: 0.2in;
            border: 1px solid #000;
            background: white;
            page-break-inside: avoid;
        }

        .entry-header {
            border-bottom: 2px solid #000;
            padding-bottom: 0.1in;
            margin-bottom: 0.1in;
        }

        .entry-title {
            font-weight: bold;
            font-size: 12pt;
            text-transform: uppercase;
        }

        .entry-meta {
            font-size: 9pt;
            color: #666;
            margin-top: 0.05in;
        }

        .observation {
            margin: 0.1in 0;
            padding-left: 0.2in;
            border-left: 2px solid #000;
        }

        .data-table {
            margin: 0.1in 0;
            border: 1px solid #000;
            border-collapse: collapse;
            width: 100%;
            font-size: 9pt;
        }

        .data-table td {
            border: 1px solid #000;
            padding: 0.05in;
        }

        .data-table .label {
            font-weight: bold;
            background: #f0f0f0;
        }
    </style>
</head>
<body>
    <div class="lab-cover">
        <div class="lab-id">LAB-NOTES-PANTHEON-001</div>
        <div class="lab-title">Pantheon Entity Catalog</div>
        <div style="margin-top: 0.1in;">Date: """
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        + """</div>
    </div>

    <div id="pantheon-content">
        <!-- Gods populated by JavaScript -->
    </div>

    <script>
        const pantheonGods = """
        + json.dumps(
            [
                {
                    "name": "Magistrate",
                    "icon": "⚖️",
                    "title": "God of Precedent and Body of Proof",
                    "description": "Organizes proof cases from _work_efforts/proof_cases/ into Precedent categories, building a Body of Proof over time.",
                    "abilities": [
                        "organize_all_cases",
                        "search_precedents",
                        "get_body_of_proof_summary",
                    ],
                    "status": "active",
                    "stats": {"Precedents": "2", "Cases": "2"},
                },
                {
                    "name": "Judge",
                    "icon": "👨‍⚖️",
                    "title": "God of Judgment and Evaluation",
                    "description": "Evaluates organization claims and references the Magistrate's Body of Proof.",
                    "abilities": ["evaluate_claim", "get_judgment_history", "get_judgment_summary"],
                    "status": "active",
                    "stats": {"Judgments": "2"},
                },
                {
                    "name": "The Reasoner",
                    "icon": "🧠",
                    "title": "God of Reasoning Traces",
                    "description": "Maintains traceable reasoning chains showing the 'why' behind decisions.",
                    "abilities": [
                        "create_trace",
                        "get_recent_traces",
                        "build_chain",
                        "search_traces",
                    ],
                    "status": "active",
                    "stats": {"Traces": "1"},
                },
                {
                    "name": "The GitHub God",
                    "icon": "🐙",
                    "title": "God of Repository Management",
                    "description": "Maintains repository state, generates rollups, and tracks GitHub operations.",
                    "abilities": ["generate_rollup", "get_repository_state", "get_branch_summary"],
                    "status": "active",
                    "stats": {"Rollups": "7", "Operations": "1"},
                },
                {
                    "name": "The Steward",
                    "icon": "💎",
                    "title": "God of Work Efforts",
                    "description": "The divine intelligence that locks, monitors, organizes, and initiates evolutionary cycles.",
                    "abilities": [
                        "/think",
                        "/evolve",
                        "/monitor",
                        "/organize",
                        "/lock",
                        "/unlock",
                        "/status",
                        "/secrets",
                    ],
                    "status": "active",
                    "stats": {"System": "pyrite"},
                },
                {
                    "name": "Librarian",
                    "icon": "📚",
                    "title": "God of Knowledge and Cataloging",
                    "description": "Maintains catalogs and reports. Organizes knowledge and documentation.",
                    "abilities": ["catalog", "organize_reports"],
                    "status": "active",
                    "stats": {"Catalog Items": "1", "Reports": "1"},
                },
                {
                    "name": "Military Brass",
                    "icon": "🎖️",
                    "title": "God of Missions and Operations",
                    "description": "Manages missions and briefings. Coordinates military-style operations.",
                    "abilities": ["create_mission", "get_briefings", "missions_registry"],
                    "status": "active",
                    "stats": {"Missions": "2"},
                },
                {
                    "name": "Mission Control",
                    "icon": "🚀",
                    "title": "God of Realm Exploration",
                    "description": "Controls realm scouting and colonization operations.",
                    "abilities": ["realm_scout", "get_realm_status", "control_registry"],
                    "status": "active",
                    "stats": {"Realm Scouts": "3"},
                },
                {
                    "name": "Fae",
                    "icon": "🧚",
                    "title": "God of Quests",
                    "description": "Manages quests and quest registry. Coordinates quest-based activities.",
                    "abilities": ["create_quest", "get_quests", "quests_registry"],
                    "status": "active",
                    "stats": {"Quests": "Active"},
                },
                {
                    "name": "The Village",
                    "icon": "🏘️",
                    "title": "God of Community",
                    "description": "Manages village registry and community activities.",
                    "abilities": ["village_registry"],
                    "status": "active",
                    "stats": {},
                },
                {
                    "name": "Test Runner",
                    "icon": "🧪",
                    "title": "God of Testing",
                    "description": "Manages test execution and test metadata.",
                    "abilities": ["run_tests", "test_metadata"],
                    "status": "active",
                    "stats": {},
                },
                {
                    "name": "External Drive Realm",
                    "icon": "💾",
                    "title": "God of External Storage",
                    "description": "Manages external drive realm content and storage routing.",
                    "abilities": ["content_manifest", "realm_registry", "realm_status"],
                    "status": "active",
                    "stats": {"Content Items": "1"},
                },
            ]
        )
        + """;

        function renderPantheon() {
            const content = document.getElementById('pantheon-content');
            content.innerHTML = pantheonGods.map((god, idx) => {
                const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
                return `
                    <div class="entry">
                        <div class="entry-header">
                            <div class="entry-title">ENTRY ${String(idx + 1).padStart(3, '0')}: ${god.name.toUpperCase()}</div>
                            <div class="entry-meta">Timestamp: ${timestamp} | Status: ${god.status.toUpperCase()}</div>
                        </div>
                        <div class="observation">
                            <strong>OBSERVATION:</strong> ${god.description}
                        </div>
                        <div class="observation">
                            <strong>TITLE:</strong> ${god.title}
                        </div>
                        ${Object.keys(god.stats).length > 0 ? `
                            <table class="data-table">
                                ${Object.entries(god.stats).map(([k, v]) => `
                                    <tr>
                                        <td class="label">${k}</td>
                                        <td>${v}</td>
                                    </tr>
                                `).join('')}
                            </table>
                        ` : ''}
                        ${god.abilities ? `
                            <div class="observation">
                                <strong>CAPABILITIES:</strong> ${god.abilities.join(', ')}
                            </div>
                        ` : ''}
                    </div>
                `;
            }).join('');
        }

        renderPantheon();
    </script>
</body>
</html>
    """
    )


def generate_all_templates():
    """Generate all template versions."""
    output_dir = Path(__file__).parent / "pantheon_templates"
    output_dir.mkdir(exist_ok=True)

    templates = {
        "improved": "scripts/pantheon_web_improved.html",
        "dnd_character_sheet": create_dnd_template(),
        "field_guide": create_field_guide_template(),
        "academic_paper": create_academic_template(),
        "lab_notes": create_lab_notes_template(),
    }

    print("🎨 Generating Pantheon UI templates...\n")

    # Copy improved version
    if Path("scripts/pantheon_web_improved.html").exists():
        import shutil

        shutil.copy("scripts/pantheon_web_improved.html", output_dir / "pantheon_improved.html")
        print(f"✅ Improved version: {output_dir / 'pantheon_improved.html'}")

    # Generate template versions
    for name, content in templates.items():
        if name == "improved":
            continue

        html_path = output_dir / f"pantheon_{name}.html"
        html_path.write_text(content)
        print(f"✅ {name.replace('_', ' ').title()}: {html_path}")

        # Generate PDF
        try:
            pdf_path = output_dir / f"pantheon_{name}.pdf"
            HTML(string=content).write_pdf(pdf_path)
            print(f"   📄 PDF: {pdf_path}")
        except Exception as e:
            print(f"   ⚠️  PDF generation failed: {e}")

    print(f"\n✨ All templates generated in: {output_dir}")
    return output_dir


if __name__ == "__main__":
    generate_all_templates()
