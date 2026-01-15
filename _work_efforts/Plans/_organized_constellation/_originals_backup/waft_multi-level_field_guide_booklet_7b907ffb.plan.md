---
name: WAFT Multi-Level Field Guide Booklet
overview: Create a comprehensive field guide booklet explaining WAFT in three increasing complexity levels (layman, professional, ML AI scientist) using the field guide template and showcasing WAFT's fun features like self-documentation, evolutionary agents, and the 12 document templates.
todos:
  - id: "1"
    content: Create generate_waft_field_guide.py script with functions for each level
    status: pending
  - id: "2"
    content: Write Level 1 (Layman) content - simple explanations, analogies, basic concepts
    status: pending
  - id: "3"
    content: Write Level 2 (Professional) content - technical details, APIs, workflows
    status: pending
  - id: "4"
    content: Write Level 3 (ML AI Scientist) content - research methodology, evolutionary theory
    status: pending
  - id: "5"
    content: Generate individual PDFs for each level using field_guide template
    status: pending
  - id: "6"
    content: Create binder script to combine all three PDFs into complete booklet
    status: pending
  - id: "7"
    content: Test generation and verify all features work correctly
    status: pending
  - id: "8"
    content: Add to showcase_documents directory and update documentation
    status: pending
---

# WAFT Field Guide Booklet Plan

## Overview

Create a multi-level field guide booklet that explains WAFT using the field guide template style, progressing from layman explanations to professional technical details to full ML AI scientist depth. The booklet will showcase WAFT's capabilities while explaining them.

## Structure

### Three-Level Progression

**Level 1: Layman's Guide** (Field Guide FG-001)

- Simple analogies and metaphors
- "What is WAFT?" in plain language
- Visual concepts (code as DNA, evolution, documentation)
- Basic use cases anyone can understand
- Safety warnings about AI agents
- Equipment checklist (what you need to get started)

**Level 2: Professional Guide** (Field Guide FG-002)

- Technical architecture overview
- API references and code examples
- Integration patterns
- Best practices and workflows
- Troubleshooting procedures
- Performance considerations

**Level 3: ML AI Scientist Guide** (Field Guide FG-003)

- Deep dive into evolutionary algorithms
- Scientific methodology and research design
- Fitness functions and selection mechanisms
- Phylogenetic analysis and lineage tracking
- Experimental protocols
- Publication-ready data generation

## Content Strategy

### Showcase WAFT Features Throughout

1. **Self-Documentation Loop**

- Explain how WAFT documents itself
- Show the recursive loop visually
- Include actual examples from WAFT's self-observation

2. **12 Document Templates**

- Reference different templates in examples
- Show variety: field guides, lab notes, TM reports, etc.
- Demonstrate template capabilities

3. **Evolutionary Agents**

- Explain the three pillars (Substrate, Physics, Flight Recorder)
- Show genome ID system
- Describe mutation and selection

4. **Gamification System**

- D&D-style progression
- XP and Insight mechanics
- Character sheets and stats

5. **Memory System (_pyrite)**

- Active/backlog/standards organization
- Knowledge management

## Implementation

### Files to Create

1. `examples/generate_waft_field_guide.py`

- Script to generate all three field guide PDFs
- Uses `field_guide.py` template
- Creates content for each level

2. `_work_efforts/showcase_documents/WAFT_Field_Guide_Layman.pdf`

- Level 1: Simple explanations

3. `_work_efforts/showcase_documents/WAFT_Field_Guide_Professional.pdf`

- Level 2: Technical details

4. `_work_efforts/showcase_documents/WAFT_Field_Guide_Scientist.pdf`

- Level 3: Research-level depth

5. `_work_efforts/showcase_documents/WAFT_Field_Guide_Complete_Booklet.pdf`

- Combined binder with all three levels
- Uses `binder.py` to merge PDFs
- Includes table of contents and section dividers

### Content Sections (Each Level)

**Level 1 Sections:**

- Introduction: What is WAFT?
- The Big Picture: Why This Matters
- Equipment Checklist: What You Need
- Quick Start: Your First WAFT Project
- Common Questions
- Safety Warnings
- Next Steps

**Level 2 Sections:**

- Architecture Overview
- Core Components
- API Reference
- Integration Patterns
- Workflow Procedures
- Troubleshooting
- Performance Optimization
- Best Practices

**Level 3 Sections:**

- Evolutionary Theory in WAFT
- Fitness Function Design
- Mutation Strategies
- Selection Mechanisms
- Phylogenetic Analysis
- Experimental Protocols
- Data Collection Methods
- Publication Standards

## Technical Details

### Template Usage

- Use `field_guide.py` template for all three documents
- Customize series numbers: FG-001, FG-002, FG-003
- Use appropriate classification levels
- Include warnings, checklists, and procedures

### Binder Assembly

- Use `Binder` class to combine all three PDFs
- Create section dividers for each level
- Generate table of contents
- Add cover page with booklet title

### Content Generation

- Write HTML content for each field guide
- Use field guide template features:
- Warning boxes for important notes
- Checklists for requirements
- Procedures for step-by-step instructions
- Tables for reference data
- Notes for additional information

## Fun Features to Highlight

1. **Recursive Self-Documentation**

- Show WAFT documenting itself
- Include actual reflection system output
- Demonstrate the loop visually

2. **Template Variety**

- Reference multiple templates in examples
- Show how different templates serve different purposes
- Include template showcase references

3. **Evolutionary Concepts**

- Code as DNA analogy
- Mutation and selection
- Fitness landscapes
- Phylogenetic trees

4. **Gamification**

- Character progression
- XP and Insight
- Adventure journal entries
- D&D-style stats

5. **Scientific Rigor**

- Flight Recorder telemetry
- Lineage tracking
- Publication-ready data
- Research methodology

## Output

Final deliverable: A single PDF booklet containing all three field guides, professionally bound with:

- Cover page
- Table of contents
- Section dividers
- Three complete field guides
- Consistent styling throughout
- Professional presentation

This booklet will serve as both documentation and a showcase of WAFT's capabilities.