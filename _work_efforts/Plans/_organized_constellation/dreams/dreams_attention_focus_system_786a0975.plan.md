---
name: Attention Focus System
overview: Implement a comprehensive attention/focus mechanism for WAFT beings, including Arrow of Attention, vibrational resonance, shocker system, energy types (friction/heat vs will/cold), and reality manifestation through focused awareness.
todos: []

category: dreams
confidence: 0.79
constellation_date: 2026-01-14
---

# Attention & Focus System Implementation Plan

## Overview

This plan implements a metaphysical attention system where beings' focused awareness manifests reality. The system includes:

- Arrow of Attention (hybrid vector + target system)
- Vibrational resonance (immutable base frequency + karma modifications)
- Shocker system (separate from status_effects)
- Energy types (Friction/Heat vs Will/Cold)
- Focal lens (energy capacity based on coherence)
- Internal coherence/quantum alignment

## Architecture

### Core Components

1. **Attention System** (`src/waft/core/attention.py`)

- `ArrowOfAttention` class (hybrid: vector + target)
- Attention weights (vector for intensity/direction)
- Focus target (being_id, goal_id, reality_id, etc.)
- Reality manifestation logic

2. **Vibrational Resonance** (integrated into `Being` class)

- Base frequency from being_id hash (immutable)
- Karma modifications across lifetimes
- Related to "Highest Timeline" concept

3. **Shocker System** (`src/waft/core/sh