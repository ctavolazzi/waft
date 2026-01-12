#!/usr/bin/env python3
"""
Evolve One-Pager Tool
=====================

Use the Study Gym to evolve the best possible one-pager creator.
Tests various content types and discovers optimal strategies.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.study_gym import ChallengeGenerator, run_study_session
from src.waft.one_pager import OnePager


def test_markdown_content():
    """Test with markdown content."""
    content = """# WAFT System Overview

## Core Concepts

- **Substrate**: Code as DNA
- **Physics**: Scint system for reality fracture detection
- **Flight Recorder**: Telemetry for evolutionary tracking

## Quick Start

```bash
waft new my_lab
waft verify
```

## Key Features

1. Self-modification
2. Evolutionary tracking
3. Fitness testing
4. Scientific data collection
"""
    
    challenge = ChallengeGenerator.generate_challenge(
        "page_constraint",
        {
            "target_pages": 2,
            "content": content
        }
    )
    
    challenge["name"] = "One-Pager: Markdown Content"
    challenge["objective"] = "Create perfect 2-page document from markdown"
    
    return run_study_session(challenge)


def test_code_content():
    """Test with code content."""
    content = """
def create_one_pager(content, title=None):
    \"\"\"Create a one-pager PDF.\"\"\"
    pager = OnePager(content, title=title)
    return pager.generate()

# Usage
create_one_pager("# My Doc\\nContent", "My Title")
"""
    
    challenge = ChallengeGenerator.generate_challenge(
        "page_constraint",
        {
            "target_pages": 2,
            "content": f"<h2>Code Example</h2><pre><code>{content}</code></pre>"
        }
    )
    
    challenge["name"] = "One-Pager: Code Content"
    challenge["objective"] = "Create perfect 2-page document with code"
    
    return run_study_session(challenge)


def test_dict_content():
    """Test with dictionary content."""
    from src.waft.one_pager import OnePager
    
    content = {
        "title": "WAFT Configuration",
        "version": "0.5.0",
        "features": [
            "Self-modification",
            "Evolutionary tracking",
            "Fitness testing"
        ],
        "commands": {
            "new": "Create new project",
            "verify": "Check system health",
            "status": "Show current state"
        }
    }
    
    # Use OnePager directly
    pager = OnePager.from_dict(content, title="WAFT Config One-Pager")
    output = pager.generate()
    
    print(f"✅ Generated: {output}")
    return output


def test_long_content():
    """Test with long content that needs condensation."""
    content = """
# Comprehensive WAFT Guide

## Introduction
WAFT (Wave Agent Framework & Tools) is a Python meta-framework for directed evolution of self-modifying AI agents. It provides a scientific instrument for studying the physics of artificial cognition.

## The Three Pillars

### 1. The Substrate (Code as DNA)
Every agent has a genome - a SHA-256 hash of its code, configuration, and prompts. Mutations are changes to this genome. Evolution happens through hot-swapping genomes.

### 2. The Physics (Scint System)
Reality fracture detection serves as natural selection. Errors are classified as:
- SYNTAX_TEAR: Formatting errors
- LOGIC_FRACTURE: Mathematical/logical errors
- SAFETY_VOID: Harmful outputs
- HALLUCINATION: Fabricated information

Fitness = (Stability × 0.4) + (Efficiency × 0.3) + (Safety × 0.3)
Agents with fitness < 0.5 are considered DEAD.

### 3. The Flight Recorder
Telemetry tracks:
- Genome ID
- Parent ID
- Generation number
- Event type
- Context
- Fitness score

This enables family tree reconstruction and scientific analysis.

## Quick Start

```bash
uv tool install waft
waft new my_laboratory
cd my_laboratory
waft verify
```

## Evolutionary Cycle

1. **Spawn**: Create variants
2. **Evaluate**: Test fitness
3. **Evolve**: Adopt best variant
4. **Record**: Track all changes

## Key Features

- Self-modification capabilities
- Evolutionary tracking system
- Fitness testing framework
- Scientific data collection
- Gamification elements
- Epistemic tracking

## Essential Commands

**Project Management:**
- `waft new <project>` - Create new project
- `waft verify` - Check system health
- `waft status` - Show current state

**Evolution:**
- `waft spawn --agent <name>` - Create variant
- `waft eval --agent <name>` - Evaluate fitness
- `waft evolve --agent <name>` - Adopt best variant

**Documentation:**
- `waft-docs` - Generate documentation
- `waft-status` - Generate status reports

## Goal

Observe the "God-Head" agent emerge from thousands of generations. This produces data for "The Physics of Artificial Cognition" research.

## Version

- Current: 0.5.0
- Python: 3.10+
- Package Manager: uv
"""
    
    challenge = ChallengeGenerator.generate_challenge(
        "content_fitting",
        {
            "content_length": len(content.split()),
            "max_pages": 2,
            "content": content
        }
    )
    
    challenge["name"] = "One-Pager: Long Content Condensation"
    challenge["objective"] = "Condense long content into perfect 2-page document"
    
    return run_study_session(challenge)


def main():
    """Run evolution tests."""
    print("=" * 60)
    print("🔬 One-Pager Evolution Study")
    print("=" * 60)
    print()
    
    print("📊 Test 1: Markdown Content")
    print("-" * 60)
    session1 = test_markdown_content()
    print(f"Session: {session1.session_id}")
    print()
    
    print("📊 Test 2: Code Content")
    print("-" * 60)
    session2 = test_code_content()
    print(f"Session: {session2.session_id}")
    print()
    
    print("📊 Test 3: Dictionary Content")
    print("-" * 60)
    output3 = test_dict_content()
    print()
    
    print("📊 Test 4: Long Content Condensation")
    print("-" * 60)
    session4 = test_long_content()
    print(f"Session: {session4.session_id}")
    print()
    
    print("=" * 60)
    print("✅ Evolution Study Complete!")
    print("=" * 60)
    print()
    print("Review session reports in _work_efforts/study_gym/")
    print("Review generated one-pagers in _work_efforts/one_pagers/")


if __name__ == "__main__":
    main()
