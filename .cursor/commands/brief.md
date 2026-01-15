# /brief - Brief Document Creator

**Purpose:** Create full binder-ready brief documents with TM-ARCH-009 style cover page and briefing content

**Usage:** `/brief [options]`

**Script:** `scripts/create_brief.py`

---

## Overview

The Brief tool creates complete binder-ready documents with:
- **TM-ARCH-009 Style Cover Page**: Professional cover with metadata, warnings, signatures
- **Briefing Content**: System status + chat context automatically included
- **Multiple Pages**: Full document, not just 2 pages
- **Binder-Ready**: Perfect for physical binders

**Perfect for:**
- Session briefs
- Project briefs
- Status reports
- Handoff documents
- Binder documentation

---

## Quick Start

### Basic Brief
```
/brief title:"Session Brief"
```

### With Cover Metadata (TM-ARCH-009 Style)
```
/brief title:"Project Brief" doc-id:"BRIEF-001" cover-header:"TELEPORT MASSIVE" cover-metadata:'{"OPERATIONAL MANUAL": "09-14", "CODENAME": "W.A.F.T."}'
```

### With Chat Context
```
/brief title:"Status Brief" current-task:"Implementing feature X" recent-topics:'["API design", "Testing"]'
```

---

## Features

- **TM-ARCH-009 Cover Page**: Professional cover with all Foundation elements
- **Automatic Briefing**: System status + chat context automatically included
- **KeyValueBlock**: Metadata on cover page
- **WarningBlock**: Severity warnings on cover
- **SignatureBlock**: Authorization signatures
- **Multiple Pages**: Full document, not limited to 2 pages
- **Binder-Ready**: Perfect for physical binders

---

## Usage Examples

### Basic Session Brief
```
/brief title:"Session Brief" doc-id:"BRIEF-001"
```

### TM-ARCH-009 Style Brief
```
/brief title:"Operational Brief" doc-id:"TM-ARCH-009" cover-header:"TELEPORT MASSIVE" cover-metadata:'{"OPERATIONAL MANUAL": "09-14", "CODENAME": "W.A.F.T.", "PROTOCOL": "WIDE-AREA FUNCTIONAL TAXONOMY"}' cover-warning:'{"message": "RESTRICTED ACCESS. This manual is a living record.", "severity": "CRITICAL"}' cover-signature:'{"role": "AUTHORIZED BY", "name": "Site-Delta-9", "date": "2026-01-12"}' cover-footer:"INTERNAL USE ONLY"
```

### Project Brief with Context
```
/brief title:"Project Brief" current-task:"Building new feature" recent-topics:'["Architecture", "Testing", "Documentation"]' key-decisions:'["Use React", "Implement tests"]' next-steps:'["Write tests", "Update docs"]'
```

### Custom Classification
```
/brief title:"Classified Brief" classification:"CLASSIFIED" cover-header:"FOUNDATION" cover-footer:"EYES ONLY"
```

---

## Output

All briefs are saved to:
- `_work_efforts/briefs/[title]_[date].pdf`

Format:
- **Cover Page**: TM-ARCH-009 style with metadata, warnings, signatures
- **Content Pages**: Briefing content (system status + chat context)
- **Multiple Pages**: Full document, binder-ready
- **Professional Formatting**: Foundation + Field Guide hybrid

---

## Integration

The Brief tool is part of WAFT's document generation system:

```python
from waft import BriefDocument

# Create brief
brief = BriefDocument(
    title="Session Brief",
    doc_id="BRIEF-001",
    cover_header="TELEPORT MASSIVE",
    cover_metadata={
        "OPERATIONAL MANUAL": "09-14",
        "CODENAME": "W.A.F.T."
    },
    cover_warning={
        "message": "RESTRICTED ACCESS.",
        "severity": "CRITICAL"
    },
    cover_signature={
        "role": "AUTHORIZED BY",
        "name": "Site-Delta-9",
        "date": "2026-01-12"
    },
    chat_context={
        'current_task': 'Implementing feature X',
        'recent_topics': ['API design', 'Testing']
    }
)

# Add custom content
brief.add_section_header("Executive Summary", level=2)
brief.add_text("This brief summarizes the current session status...")

# Generate PDF
brief.generate()
```

---

## Cover Page Elements

The cover page includes:

1. **Cover Header**: Institution/organization name (e.g., "TELEPORT MASSIVE")
2. **Title**: Document title (large, bold, uppercase)
3. **Subtitle**: Optional subtitle
4. **Document ID**: Document identifier (e.g., "TM-ARCH-009")
5. **KeyValueBlock**: Metadata (operational manual, codename, protocol, etc.)
6. **WarningBlock**: Security warnings (severity: WARNING, CAUTION, CRITICAL)
7. **SignatureBlock**: Authorization signatures
8. **Cover Footer**: Footer text (e.g., "INTERNAL USE ONLY", "COPY NO: 01 OF 01")

---

## Content Pages

Content pages automatically include:

1. **Current Session Context**:
   - Current task
   - Recent topics
   - Key decisions
   - Next steps

2. **System Status**:
   - Git status
   - Work efforts
   - Project health
   - Epistemic state
   - Kernel status

---

## Use Cases

- **Session Briefs**: Document what happened in a session
- **Project Briefs**: Status reports for projects
- **Handoff Documents**: Transfer knowledge between sessions
- **Status Reports**: Regular status updates
- **Binder Documentation**: Physical binder organization

---

## Philosophy

Combines:
- **TM-ARCH-009 Style**: Professional cover page with Foundation elements
- **Briefing System**: Automatic system status + chat context
- **Binder-Ready**: Full document, not limited to 2 pages
- **Professional Formatting**: Foundation + Field Guide hybrid

Result: A truly compelling brief document that's perfect for binders and handoffs.

---

**Created for session documentation, project briefs, and binder organization.**

--- End Command ---
