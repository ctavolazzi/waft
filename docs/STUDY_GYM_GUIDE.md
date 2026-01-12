# Study Gym: Scientific Method Learning System

**Purpose:** A testing gym where the system can practice using PDF tools and learn through the Scientific Method.

---

## Overview

The Study Gym is a "variable obstacle course" that allows the system to:
1. **Observe** its own behavior with DocumentBuilder
2. **Question** what patterns it sees
3. **Hypothesize** about what works
4. **Test** those hypotheses
5. **Analyze** results
6. **Conclude** what's true beyond reasonable doubt

This is the **Scientific Method** applied to tool discovery.

---

## How It Works

### The Scientific Method Workflow

```
OBSERVE → QUESTION → HYPOTHESIZE → TEST → ANALYZE → CONCLUDE
```

1. **OBSERVE**: System attempts to create a document based on challenge requirements
2. **QUESTION**: System analyzes what happened and identifies patterns
3. **HYPOTHESIZE**: System forms a hypothesis with:
   - Statement of what it thinks
   - Reasoning behind the hypothesis
   - Assumptions being made
   - A plan to test it
4. **TEST**: System tests the hypothesis by attempting the challenge again
5. **ANALYZE**: System analyzes all results and forms findings
6. **CONCLUDE**: System forms conclusions about what's true (confidence ≥ 0.7)

---

## Challenge Templates (Mad Lib Style)

### 1. `page_constraint`
**Goal:** Create a document with exactly N pages

**Variables:**
- `target_pages`: Exact number of pages required
- `content`: HTML content to use

**Example:**
```
/study page_constraint target_pages=2 content="<h2>Test</h2><p>Content</p>"
```

### 2. `content_fitting`
**Goal:** Fit specific content into maximum page count

**Variables:**
- `content_length`: Target word count
- `max_pages`: Maximum allowed pages
- `content`: HTML content

### 3. `style_exploration`
**Goal:** Explore different styling options

**Variables:**
- `document_type`: Type of document
- `style_features`: Features to explore
- `content`: HTML content

### 4. `multi_document`
**Goal:** Create a collection with multiple documents

**Variables:**
- `num_docs`: Number of documents
- `target_pages`: Pages per document
- `content`: HTML content template

### 5. `printer_friendly`
**Goal:** Master printer-friendly conversion

**Variables:**
- `specific_requirements`: What to test
- `target_pages`: Target page count
- `content`: HTML content

---

## Usage

### Global Cursor Command

```
/study [template] [key=value ...]
```

### Examples

**Basic usage:**
```
/study page_constraint target_pages=2 content="<h2>Test</h2><p>Content</p>"
```

**List available templates:**
```
/study
```

---

## Output

Each study session generates:

1. **Session JSON** (`_work_efforts/study_gym/study_YYYYMMDD_HHMMSS.json`)
   - Complete session data
   - All observations with timestamps
   - All hypotheses with confidence levels
   - Findings and conclusions

2. **Summary Report** (`_work_efforts/study_gym/study_YYYYMMDD_HHMMSS_report.md`)
   - Human-readable summary
   - Formatted observations
   - Hypothesis status
   - Findings and conclusions

---

## Integration with DocumentBuilder

The Study Gym uses DocumentBuilder's constraint-aware features:

- **`exact_pages`** parameter triggers feedback loop
- **`max_pages`** and **`min_pages`** for range constraints
- **Automatic CSS adjustment** during generation (font size, margins, spacing)
- **Page count validation** built-in

The gym discovers how these features work through experimentation.

---

## The Feedback Loop

When constraints are specified, DocumentBuilder:

1. Generates initial PDF
2. Checks page count using `pypdf`
3. If constraints not met:
   - Adjusts CSS (font size × 0.95, margins × 0.95, spacing × 0.95)
   - Regenerates PDF
   - Re-checks
   - Iterates up to `max_iterations` (default: 5)
4. Returns PDF that meets constraints (or best attempt)

This feedback loop is **built into DocumentBuilder**, not external.

---

## Scientific Rigor

The Study Gym follows rigorous scientific methodology:

- **Observations** are recorded with timestamps and metrics
- **Hypotheses** include:
  - Confidence levels (0.0 to 1.0)
  - Test plans
  - Assumptions
- **Tests** are repeatable and documented
- **Conclusions** are only reached when confidence is high (≥0.7)

This ensures the system learns reliably and can build on previous knowledge.

---

## Example Session Flow

```
/study page_constraint target_pages=2 content="<h2>Test</h2><p>Content</p>"
```

**What happens:**

1. **OBSERVE**: System attempts to create 2-page document
   - Result: 1 page (constraint not met)

2. **QUESTION**: "Why didn't it meet the constraint?"
   - Analyzes: Document has 1 page, needs 2

3. **HYPOTHESIZE**: "Adjusting CSS will help meet page constraints"
   - Reasoning: CSS affects page count
   - Assumptions: Font size reduction reduces pages
   - Test plan: Try reducing font size and margins

4. **TEST**: System tests hypothesis
   - Attempts again with CSS adjustments
   - Result: Still 1 page (needs more adjustment)

5. **ANALYZE**: "Successfully created 1 document, but constraints not met"
   - Finding: Need more aggressive CSS adjustment

6. **CONCLUDE**: "More study needed" (confidence not high enough yet)

---

## Key Features

### Constraint Awareness
- DocumentBuilder "knows" about page constraints
- Automatically adjusts during generation
- Validates after generation

### Feedback Loop
- Generates → Checks → Adjusts → Regenerates
- Iterative refinement until constraints met
- Maximum iterations to prevent infinite loops

### Scientific Method
- Systematic observation
- Hypothesis formation
- Testing and validation
- Conclusion formation

### Self-Directed Learning
- System discovers capabilities through practice
- Forms its own understanding
- Builds knowledge over time

---

## Files Created

- `src/waft/study_gym.py` - Core gym system
- `scripts/run_study.py` - CLI entry point
- `.cursor/commands/study.md` - Global Cursor command
- `docs/STUDY_GYM_GUIDE.md` - This guide

---

## Philosophy

> "The organism that is this machine should be able to observe, form an opinion, test its opinion, consider its assumptions and recontextualize them if necessary, then form and test a hypothesis until it reaches some kind of conclusions beyond the shadow of a reasonable doubt."

This is exactly what the Study Gym enables. It's not just a testing tool—it's a **learning system** that follows the Scientific Method to discover how tools work.

---

**Created with ❤️ for scientific discovery and self-directed learning.**
