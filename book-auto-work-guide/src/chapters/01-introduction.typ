= Introduction

The WAFT Auto-Work feature represents a significant advancement in autonomous project management. This system enables intelligent, hands-off execution of work efforts by analyzing priorities, selecting optimal tasks, and executing them autonomously with comprehensive safety mechanisms.

== Purpose of This Guide

This guide provides:

- *[Comprehensive Documentation]*: Complete explanation of how Auto-Work functions
- *[Step-by-Step Walkthrough]*: Detailed process flow from start to finish
- *[Usage Examples]*: Real-world scenarios with expected outputs
- *[Integration Details]*: How Auto-Work integrates with Empirica, Pantheon, Campfire, and D&D systems
- *[Safety Mechanisms]*: Security features and validation processes
- *[Troubleshooting]*: Common issues and solutions

== Who This Guide Is For

This guide is designed for:

- *[Developers]*: Understanding the technical implementation
- *[Project Managers]*: Learning how to leverage autonomous work execution
- *[System Administrators]*: Configuring and maintaining the system
- *[Users]*: Learning to use Auto-Work effectively

== What You'll Learn

By the end of this guide, you will understand:

1. How Auto-Work analyzes and prioritizes work efforts
2. The priority scoring algorithm and its factors
3. How safety gates prevent unsafe operations
4. Integration with epistemic tracking (Empirica)
5. Integration with decision support (Pantheon)
6. Storytelling integration (Campfire)
7. D&D campaign integration for quest generation
8. How to use Auto-Work effectively in your workflow

== Prerequisites

Before using Auto-Work, ensure you have:

- WAFT installed and configured
- Work efforts in `_work_efforts/` directory
- (Optional) Empirica initialized for epistemic tracking
- (Optional) Pantheon entities configured for decision support
- (Optional) Campfire configured for storytelling
- (Optional) D&D campaign system configured for quest generation

== Document Structure

This guide is organized into five parts:

*[Part I: Introduction & Overview]* - What Auto-Work is and its key features

*[Part II: How It Works]* - Deep dive into the architecture and algorithms

*[Part III: Integration & Safety]* - Empirica, Pantheon, Campfire, D&D, and safety mechanisms

*[Part IV: Usage Guide]* - How to use Auto-Work with examples and walkthroughs

*[Part V: Advanced Topics]* - Customization, best practices, and future enhancements

== Getting Started

To get started with Auto-Work, run:

```
/auto-work
```

Or to see what would be done without executing:

```
/auto-work --dry-run
```

For detailed output:

```
/auto-work --verbose
```

Let's begin by understanding what Auto-Work is and how it can transform your workflow.
