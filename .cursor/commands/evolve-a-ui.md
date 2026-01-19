# Evolve a UI

**Methodical, step-by-step UI evolution based on chat context with proof at every step**

Scans the current chat conversation, creates a design document (verified 3 times), builds technical requirements, then iteratively develops a UI component-by-component with screenshots and case files as proof.

**Use when:** You want a UI that reflects what you actually did in the chat, need a dashboard for the work completed, or want to visualize the conversation's outcomes through a proven, methodical development process.

---

## Purpose

This command provides:
- **Chat Context Analysis**: Scans entire conversation to understand what was done
- **Design Document Creation**: Documents purpose and goals (checked 3 times)
- **Technical Requirements**: Breaks down design into implementable specs
- **Iterative Development**: Builds UI component-by-component with proof
- **Case File Integration**: Creates proof cases and displays them in the UI
- **Supporting Materials**: Builds all standard dev team artifacts
- **Visual Progress**: Screenshots at every step saved to work efforts

---

## Philosophy

### 1. Methodical Over Fast
- **NO SKIPPING STEPS** - Must follow process sequentially
- **NO CODE DUMPING** - Build one component at a time
- **PROVE EVERYTHING** - Case files for major decisions
- **VISUAL PROOF** - Screenshots at every step

### 2. Context-Driven Design
- **Chat Analysis**: Understand what was actually done
- **Purpose First**: Design doc defines WHY before HOW
- **Verified Design**: Check design doc 3 times before proceeding
- **Adaptive UI**: UI reflects actual chat context

### 3. Evidence-Based Development
- **Case Files**: Document decisions with evidence
- **Screenshots**: Visual proof of progress
- **WAFT Tools**: Use `/think`, `/decide`, `/science-bitch` to answer questions
- **Transparency**: Show proof in the UI itself

---

## Workflow Sequence

**Phase 1: Analysis & Design (MANDATORY - NO SKIPPING)**
```
1. Scan Chat Context        → Analyze entire conversation
2. Create Design Document   → Document what was observed, purpose, goals
3. First Check              → Review design doc for completeness
4. Second Check             → Verify accuracy
5. Third Check              → Ensure nothing missed
6. ONLY PROCEED when satisfied
```

**Phase 2: Requirements & Wireframe**
```
7. Create Technical Requirements → Break down design into specs
8. Create Wireframe              → HTML structure, boxes only, no content
```

**Phase 3: Iterative Component Development (STEP BY STEP)**
```
9. HTML Boilerplate         → Basic structure → Screenshot
10. Navigation (empty)      → Nav box only → Screenshot
11. Add Header              → Header box → Screenshot
12. Add Sidebar             → Sidebar box → Screenshot
13. Add Main Content        → Main box → Screenshot
14. Add Footer              → Footer box → Screenshot
15. Add Content to Each     → One section at a time → Screenshot each
16. Use WAFT Tools          → When stuck, use /think, /decide, /science-bitch
17. Create Case Files       → For each major decision → Save to proof_cases/
18. Include Case Component  → Display case files in the page
```

**Phase 4: Supporting Materials**
```
19. Statement of Purpose    → Why this UI exists
20. Developer Profiles      → Personality profiles
21. LaTeX CVs              → Developer CVs
22. Work Effort Tracking   → Link to work efforts
23. Pantheon Integration   → Demigods weighing in
```

---

## Execution Steps

### Step 1: Scan Chat Context

**Purpose**: Understand what was actually done in this conversation

**Actions**:
1. Read entire conversation transcript
2. Identify key work completed
3. Extract decisions made
4. Note implementations
5. Identify themes and patterns
6. Determine what was demonstrated/proven

**Output**: Chat context summary with key work items

**CRITICAL**: This is about the CHAT, not just work efforts. What did we DO here?

---

### Step 2: Create Design Document

**Purpose**: Document what was observed and define the UI's purpose

**Actions**:
1. Write design document describing:
   - What was observed in the chat
   - What the UI should accomplish
   - Why it exists
   - What problem it solves
   - Key features needed
2. Save to `_work_efforts/[timestamp]_ui_design_doc.md`

**Output**: Design document

**CRITICAL**: This defines PURPOSE before implementation

---

### Step 3: First Check of Design Document

**Purpose**: Verify completeness

**Actions**:
1. Review design document
2. Check for:
   - Clear purpose statement
   - All key work items mentioned
   - Goals defined
   - Nothing obvious missing
3. Update if needed

**Output**: Verified design document (first pass)

---

### Step 4: Second Check of Design Document

**Purpose**: Verify accuracy

**Actions**:
1. Re-read chat context
2. Compare to design document
3. Verify:
   - Accuracy of observations
   - Correct understanding of work done
   - Proper problem identification
4. Update if needed

**Output**: Verified design document (second pass)

---

### Step 5: Third Check of Design Document

**Purpose**: Final verification

**Actions**:
1. Final review of design document
2. Check for:
   - Any missed important details
   - Clarity of purpose
   - Completeness
3. **ONLY PROCEED** if satisfied

**Output**: Final verified design document

**CRITICAL**: Do NOT proceed to next phase until this is complete and verified

---

### Step 6: Create Technical Requirements

**Purpose**: Break down design into implementable specs

**Actions**:
1. Read verified design document
2. Create technical requirements:
   - Components needed
   - Data sources
   - Interactions
   - Layout structure
3. Save to `_work_efforts/[timestamp]_ui_requirements.md`

**Output**: Technical requirements document

---

### Step 7: Create Wireframe

**Purpose**: HTML structure only, no content

**Actions**:
1. Create HTML boilerplate
2. Add semantic structure:
   - `<header>`
   - `<nav>`
   - `<main>`
   - `<aside>` (sidebars)
   - `<footer>`
3. Add box model CSS (borders visible for wireframe)
4. NO CONTENT - just boxes
5. Save to `index.html` at project root

**Output**: Wireframe HTML

**Output**: Wireframe HTML file

---

### Step 8: Screenshot Wireframe

**Purpose**: Visual proof of structure

**Actions**:
1. Open `index.html` in browser
2. Take full-page screenshot
3. Save to `_work_efforts/[timestamp]_wireframe.png`

**Output**: Screenshot of wireframe

---

### Step 9: Add Navigation (Empty)

**Purpose**: Add nav structure, no content yet

**Actions**:
1. Add `<nav>` element
2. Add nav box structure
3. NO links or content
4. Just the box
5. **Screenshot** → Save to `_work_efforts/[timestamp]_nav_empty.png`

**Output**: Nav structure, screenshot

---

### Step 10-N: Add Elements One by One

**Purpose**: Build incrementally with proof

**For each element** (header, sidebar, main, footer, etc.):
1. Add HTML structure
2. Add basic styling (box model)
3. **Screenshot** → Save to `_work_efforts/[timestamp]_[element_name].png`
4. Create case file if major decision made
5. Use WAFT tools if stuck (`/think`, `/decide`, `/science-bitch`)

**Output**: Incremental screenshots, case files, working UI

---

### Step N+1: Use WAFT Tools When Needed

**Purpose**: Answer questions iteratively

**When stuck or need to decide**:
1. Use `/think` for cognitive setup
2. Use `/decide` for decision-making
3. Use `/science-bitch` for hypothesis testing
4. Use evolution system for design questions
5. Create case file documenting the decision

**Output**: Decisions with proof

---

### Step N+2: Create Case Files

**Purpose**: Document major decisions with evidence

**Actions**:
1. For each major decision/implementation:
   - Create case file in `_work_efforts/proof_cases/`
   - Document claim (what was decided)
   - Include evidence (code, reasoning)
   - State verdict (decision made)
2. Use format: `case_YYYYMMDD_HHMMSS_[description].md`

**Output**: Case files documenting decisions

---

### Step N+3: Include Case Files Component

**Purpose**: Show proof in the UI itself

**Actions**:
1. Create component to display case files
2. List recent case files
3. Show case summaries
4. Link to full case files
5. Add to main page

**Output**: Case files visible in UI

---

### Step N+4: Build Supporting Materials

**Purpose**: Create all standard dev team artifacts

**Actions**:
1. **Statement of Purpose**: Why this UI exists
2. **Developer Profiles**: Personality profiles for "developers"
3. **LaTeX CVs**: Generate CVs for developers
4. **Work Effort Tracking**: Link to work efforts
5. **Pantheon Integration**: Demigods weighing in on decisions
6. Include all in the UI or as linked documents

**Output**: Complete supporting materials

---

## Project Structure

```
[project_root]/
├── _work_efforts/
│   ├── proof_cases/
│   │   └── [case files created during development]
│   └── [screenshots saved here: timestamp_element.png]
├── README.md
└── index.html
```

---

## Output Files

**Generated Files**:
- `index.html` - Main UI file (at project root)
- `README.md` - Project documentation (at project root)
- `_work_efforts/[timestamp]_ui_design_doc.md` - Design document
- `_work_efforts/[timestamp]_ui_requirements.md` - Technical requirements
- `_work_efforts/[timestamp]_wireframe.png` - Wireframe screenshot
- `_work_efforts/[timestamp]_[element].png` - Screenshot for each element
- `_work_efforts/proof_cases/case_*.md` - Case files for decisions

**Supporting Materials**:
- Developer profiles
- LaTeX CVs
- Statement of purpose
- Work effort links
- Pantheon integration

---

## Critical Rules

1. **NO SKIPPING STEPS** - Must follow sequence exactly
2. **NO CODE DUMPING** - One component at a time
3. **SCREENSHOT EVERY STEP** - Visual proof required
4. **CHECK DESIGN DOC 3X** - Verify before proceeding
5. **CASE FILES FOR PROOF** - Document decisions
6. **USE WAFT TOOLS** - Answer questions iteratively
7. **INCLUDE CASE FILES** - Show proof in UI

---

## Integration

This command uses:
- **Chat transcript analysis** - Understand conversation
- **Work Efforts System** - Link to work efforts
- **Case File System** - Document decisions
- **WAFT Tools** - `/think`, `/decide`, `/science-bitch`
- **Evolution System** - Design evolution
- **Pantheon** - Demigod integration
- **Document Generation** - CVs, profiles, etc.

---

## When to Use

**Use `/evolve-a-ui` when**:
- ✅ Want UI that reflects actual chat work
- ✅ Need dashboard for completed work
- ✅ Want methodical, proven development
- ✅ Need evidence-based UI creation
- ✅ Want to visualize conversation outcomes

**Don't use `/evolve-a-ui` when**:
- ❌ Want quick prototype (this is methodical)
- ❌ Don't want to follow process (must follow steps)
- ❌ Need production UI immediately (this is iterative)

---

## Example Flow

```
User: /evolve-a-ui

AI:
1. Scanning chat... [analyzes conversation]
2. Creating design document... [documents observations]
3. First check... [verifies completeness]
4. Second check... [verifies accuracy]
5. Third check... [final verification]
6. Design doc verified. Creating requirements...
7. Creating wireframe... [HTML structure]
8. Screenshot saved: wireframe.png
9. Adding nav (empty)... [nav box]
10. Screenshot saved: nav_empty.png
11. Adding header... [header box]
12. Screenshot saved: header.png
... [continues step by step]
```

---

*This command creates a UI through methodical, proven development with evidence at every step.*
