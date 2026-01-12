# /study - DocumentBuilder Study Gym

**Purpose:** Scientific method-based learning system for discovering DocumentBuilder capabilities

**Usage:** `/study [template] [key=value ...]`

**Script:** `scripts/run_study.py`

## Overview

The Study Gym is a "practice tool" where the system can:
1. **Observe** its own behavior with DocumentBuilder
2. **Question** what patterns it sees
3. **Hypothesize** about what works
4. **Test** those hypotheses
5. **Analyze** results
6. **Conclude** what's true beyond reasonable doubt

This follows the Scientific Method applied to tool discovery.

## Available Challenge Templates

### 1. `page_constraint`
Create a document with exactly N pages.

**Variables:**
- `target_pages`: Exact number of pages required
- `content`: HTML content to use

**Example:**
```
/study page_constraint target_pages=2 content="<h2>Test</h2><p>Content here</p>"
```

### 2. `content_fitting`
Fit a specific amount of content into a maximum page count.

**Variables:**
- `content_length`: Target word count
- `max_pages`: Maximum allowed pages
- `content`: HTML content

**Example:**
```
/study content_fitting content_length=500 max_pages=3 content="<h2>Long Content</h2><p>...</p>"
```

### 3. `style_exploration`
Explore different styling options.

**Variables:**
- `document_type`: Type of document to create
- `style_features`: Features to explore
- `content`: HTML content

**Example:**
```
/study style_exploration document_type="field_guide" style_features="printer_friendly,compact" content="<h2>Test</h2>"
```

### 4. `multi_document`
Create a collection with multiple documents.

**Variables:**
- `num_docs`: Number of documents
- `target_pages`: Pages per document
- `content`: HTML content template

**Example:**
```
/study multi_document num_docs=3 target_pages=2 content="<h2>Doc {n}</h2><p>Content</p>"
```

### 5. `printer_friendly`
Master printer-friendly conversion.

**Variables:**
- `specific_requirements`: What to test
- `target_pages`: Target page count
- `content`: HTML content

**Example:**
```
/study printer_friendly specific_requirements="2_pages_black_white" target_pages=2 content="<h2>Test</h2>"
```

## How It Works

### Phase 1: OBSERVE
The system attempts to create the document based on the challenge configuration and records what happens.

### Phase 2: QUESTION
The system analyzes its observations and identifies patterns.

### Phase 3: HYPOTHESIZE
The system forms a hypothesis about what might work, including:
- Statement of the hypothesis
- Reasoning behind it
- Assumptions being made
- A plan to test it

### Phase 4: TEST
The system tests the hypothesis by attempting the challenge again with adjustments.

### Phase 5: ANALYZE
The system analyzes all results and forms findings about what it learned.

### Phase 6: CONCLUDE
The system forms conclusions about what's true "beyond reasonable doubt" based on confirmed hypotheses and successful attempts.

## Output

Each study session generates:
1. **Session JSON** (`_work_efforts/study_gym/study_YYYYMMDD_HHMMSS.json`)
   - Complete session data
   - All observations
   - All hypotheses
   - Findings and conclusions

2. **Summary Report** (`_work_efforts/study_gym/study_YYYYMMDD_HHMMSS_report.md`)
   - Human-readable summary
   - Formatted observations
   - Hypothesis status
   - Findings and conclusions

## Example Session

```
/study page_constraint target_pages=2 content="<h2>WAFT One-Pager</h2><p>Essential info...</p>"
```

This will:
1. Try to create a 2-page document
2. Observe the result
3. Form a hypothesis about how to control page count
4. Test the hypothesis
5. Analyze what worked
6. Conclude what's true

## Scientific Method

The Study Gym follows rigorous scientific methodology:

- **Observations** are recorded with timestamps and metrics
- **Hypotheses** include confidence levels and test plans
- **Tests** are repeatable and documented
- **Conclusions** are only reached when confidence is high (≥0.7)

This ensures the system learns reliably and can build on previous knowledge.

## Integration with DocumentBuilder

The Study Gym uses DocumentBuilder's constraint-aware features:
- `exact_pages` parameter triggers feedback loop
- `max_pages` and `min_pages` for range constraints
- Automatic CSS adjustment during generation
- Page count validation built-in

The gym discovers how these features work through experimentation.
