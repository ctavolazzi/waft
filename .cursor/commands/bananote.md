# Bananote

**Use the Typst bananote template to take structured notes while working.**

Use when: You want a running research booklet / notes document tied to the current work effort.

---

## Purpose

This command provides:
- A consistent note-taking format during work
- A Typst-based research booklet (source + PDF)
- Lightweight structure for findings, decisions, and next steps

---

## Execution Steps

### Step 1: Create or select a notes file
**Purpose**: Keep all notes in the active work effort.

**Actions**:
1. Create a Typst file in the work effort folder (e.g., `bananote_notes.typ`).
2. Use a date-based filename if multiple notes are needed.

**Output**: A `.typ` note file tracked with the work effort.

---

### Step 2: Open the ODD notes web app
**Purpose**: Keep a live reference view while writing notes.

**Actions**:
1. Open the SvelteKit notes UI (expects FastAPI on `http://localhost:8000`):
   ```
   browser_navigate("http://localhost:5173/odd-notes")
   ```
2. Keep the existing ODD page handy:
   - `http://localhost:6660/`

**Output**: Browser open to the ODD research notes page.

---

### Step 3: Use the bananote template
**Purpose**: Ensure notes follow the bananote structure.

**Actions**:
1. Import bananote and apply the `note` template:
   ```typst
   #import "@preview/bananote:0.1.1": *

   #show: note.with(
     title: [Research Notes],
     authors: (
       ([Your Name], [Affiliation]),
     ),
     date: datetime.today(),
     version: "0.1",
   )

   #abstract[Short abstract of the notes.]
   ```
2. Populate metadata (title, authors, date).
3. Capture goals, observations, decisions, and TODOs as you work.

**Output**: Structured notes that render as a clean PDF.

---

### Step 4: Compile to PDF
**Purpose**: Produce a readable artifact.

**Actions**:
1. Use Typst CLI:
   ```bash
   typst compile bananote_notes.typ bananote_notes.pdf
   ```
2. Or use WAFT Typst compiler (`src/waft/templates/typst`).

**Output**: `bananote_notes.pdf` in the work effort folder.

---

## Output Format

- Source: `bananote_notes.typ`
- PDF: `bananote_notes.pdf`

---

## Use Cases

### 1. Research Booklet
**Scenario**: Running a long investigation with multiple findings.

**Example**:
```
/bananote
```

**Output**: A maintained bananote PDF that captures the session.

---

## Integration with Other Commands

- **`/deep-analyze`**: Capture extracted insights in bananote notes
- **`/critique`**: Record issues and recommended fixes
- **`/respond-to-critique`**: Track applied fixes and evidence

---

## When to Use

**Use `/bananote` when**:
- ✅ You need structured notes tied to a work effort
- ✅ You want a PDF research booklet as an artifact

**Don't use `/bananote` when**:
- ❌ A quick one-line note is sufficient
- ❌ Notes are not part of the requested deliverables

---

**Requires Typst 0.12.0+ (bananote minimum).**

--- End Command ---
