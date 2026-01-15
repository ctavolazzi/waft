# /case-file - Generate Case File from Proof Evidence

**Compiles proof evidence from the conversation into a professional case file with verdict.**

---

## Purpose

This command generates a comprehensive case file by:
1. **Extracting proof evidence** - From `/prove-it` investigations or other proof discussions in chat
2. **Compiling findings** - All code evidence, file references, and investigation results
3. **Structuring case file** - Professional format with executive summary, evidence, and verdict
4. **Saving documentation** - Markdown case file in `_work_efforts/proof_cases/`
5. **Optional PDF** - Can generate PDF binder if requested

**Use when:**
- You've run `/prove-it` and want a case file from the evidence
- You need documentation of proof findings
- You want a professional case brief with all evidence
- You need to archive proof results
- You want a PDF binder of the case

---

## Execution

**Command**: `/case-file` or `/generate-case` or `/compile-case`

**What the AI does:**
1. **Extracts proof evidence** from recent `/prove-it` investigation or conversation
2. **Identifies the claim** that was proven/disproven
3. **Compiles all evidence** - Code snippets, file references, findings
4. **Structures case file** - Executive summary, investigation, evidence, verdict
5. **Saves markdown** - To `_work_efforts/proof_cases/case_YYYYMMDD_HHMMSS.md`
6. **Optionally generates PDF** - If you request it

**AI Actions:**
- Reviews conversation for proof evidence
- Extracts claim statement
- Compiles investigation findings
- Includes code snippets with line references
- Adds file paths and evidence
- States verdict and confidence
- Formats as professional case file
- Saves to proof_cases directory

**If no proof evidence found:**
- AI will ask you to run `/prove-it` first
- Or you can provide the claim and evidence manually

---

## Case File Structure

The generated case file includes:

### 1. Executive Summary
- Claim statement
- Verdict (PROVEN/DISPROVEN/INCONCLUSIVE)
- Confidence level
- Date and time

### 2. Investigation Details
- Methodology
- Files examined
- Code searched
- Evidence sources

### 3. Evidence Section
- Code snippets with line references
- File paths and locations
- Findings from investigation
- Verification results

### 4. Verdict
- Clear statement of result
- Confidence level
- Reasoning
- Limitations (if any)

### 5. Appendix (Optional)
- Full code references
- Additional context
- Related files

---

## Example Output

**User**: `/case-file`

**AI Response**:

After reviewing the `/prove-it` investigation above, I'll compile a case file...

```
📄 Case File Generated: _work_efforts/proof_cases/case_20260114_105230.md

The case file includes:
- Executive summary with verdict: PROVEN (98% confidence)
- Complete investigation findings
- All code evidence with line references
- Evidence summary
- Verdict reasoning

Would you like me to also generate a PDF binder?
```

---

## When to Use

**Use `/case-file` when**:
- ✅ You've run `/prove-it` and want documentation
- ✅ You need a case file from proof evidence in chat
- ✅ You want to archive proof findings
- ✅ You need a professional case brief
- ✅ You want PDF documentation

**Don't use `/case-file` when**:
- ❌ You haven't run `/prove-it` yet (run that first)
- ❌ You just want quick verification (use `/verify`)
- ❌ You need assumption checking (use `/check-assumptions`)

---

## Integration

This command works with:
- **`/prove-it`**: Extracts evidence from proof investigations
- **`/study-claim`**: Can compile case files from thorough studies
- **`/check-assumptions`**: Can include assumption validation results

---

## File Location

Case files are saved to:
```
_work_efforts/proof_cases/
├── case_YYYYMMDD_HHMMSS.md
└── PROOF_CASE_[claim]_YYYYMMDD_HHMMSS.pdf (if PDF requested)
```

---

## How It Works

When you use `/case-file`, the AI will:

1. **Review conversation** - Looks for `/prove-it` investigations or proof discussions
2. **Extract claim** - Identifies what was being proven
3. **Compile evidence** - Gathers all code snippets, findings, file references
4. **Structure case file** - Formats as professional case brief
5. **Save markdown** - Writes to `_work_efforts/proof_cases/`
6. **Generate PDF** - If requested, creates PDF binder

The AI does this **interactively in chat**, compiling evidence from the conversation into a structured case file.

---

**This command creates professional documentation from proof evidence in your conversations.**

--- End Command ---
