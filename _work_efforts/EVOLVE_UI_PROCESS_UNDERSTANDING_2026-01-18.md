# Evolve UI Process - My Understanding

**Date**: 2026-01-18
**Purpose**: Document my understanding of the iterative UI evolution process

---

## Core Process Flow

### Phase 1: Context Analysis & Design (MANDATORY - NO SKIPPING)
1. **Scan Chat Context**
   - Analyze entire conversation
   - Identify key work, decisions, implementations
   - Extract themes and patterns
   - Note what was built/demonstrated

2. **Create Design Document** (CHECK 3 TIMES)
   - Document what was observed in chat
   - Describe the purpose and goals
   - Define what the UI should accomplish
   - **First Check**: Review for completeness
   - **Second Check**: Verify accuracy
   - **Third Check**: Ensure nothing missed
   - **ONLY PROCEED** when satisfied with design doc

3. **Create Technical Requirements**
   - Break down design doc into technical specs
   - Define components needed
   - Identify data sources
   - Specify interactions

4. **Create Wireframe/Boilerplate**
   - HTML structure only
   - Box model layout
   - No content yet
   - Just the skeleton

---

### Phase 2: Iterative Component Development (STEP BY STEP - NO SKIPPING)

5. **HTML Boilerplate**
   - Basic HTML structure
   - Semantic tags
   - Box model layout
   - **Screenshot** → Save to `_work_efforts/`

6. **Navigation Section** (EMPTY FIRST)
   - Nav structure only
   - No content
   - Just the box
   - **Screenshot** → Save to `_work_efforts/`

7. **Add Elements One by One**
   - Add header → Screenshot
   - Add sidebar → Screenshot
   - Add main content → Screenshot
   - Add footer → Screenshot
   - **Each step gets a screenshot**

8. **Use WAFT Tools to Answer Questions**
   - When stuck: Use `/think`, `/decide`, `/science-bitch`
   - Use evolution system
   - Use decision matrix
   - **Prove decisions with case files**

9. **Create Case Files as Proof**
   - For each major decision/implementation
   - Create case file in `_work_efforts/proof_cases/`
   - Document evidence and reasoning
   - **Include case files component in page**

10. **Build Supporting Materials**
    - Statement of purpose
    - Developer personality profiles
    - LaTeX CVs for developers
    - Work effort tracking
    - Pantheon integration (demigods weighing in)
    - All the "standard dev team" artifacts

---

### Phase 3: Integration & Evolution

11. **Include Case Files Component**
    - Display case files in the page
    - Show proof evidence
    - Link to case files

12. **Iterate Based on Context**
    - Use WAFT evolution system
    - Use decision tools
    - Use science-bitch for testing
    - Evolve UI based on what works

---

## Project Structure

```
[project_root]/
├── _work_efforts/
│   ├── proof_cases/
│   │   └── [case files created during development]
│   └── [screenshots saved here]
├── README.md
└── index.html
```

---

## Critical Rules

1. **NO SKIPPING STEPS** - Must go through process sequentially
2. **NO CODE DUMPING** - Build component by component
3. **SCREENSHOT EVERY STEP** - Visual proof of progress
4. **CASE FILES FOR PROOF** - Document decisions with evidence
5. **CHECK DESIGN DOC 3X** - Verify before proceeding
6. **USE WAFT TOOLS** - Answer questions iteratively
7. **INCLUDE CASE FILES** - Show proof in the page itself

---

## What This Achieves

- **Methodical Development**: Step-by-step, proven process
- **Transparent Decisions**: Case files show why choices were made
- **Visual Progress**: Screenshots document evolution
- **Context-Aware**: UI adapts to actual chat/work context
- **Complete Artifacts**: All dev team materials included
- **Proven Work**: Evidence-based development

---

**Next**: Update `/evolve-a-ui` command with this process, then start Phase 1
