# ODD Realm

**The Ontological Determinism Department** - A mysterious organization from Nexus that studies Teleport Massive from an unknown point in spacetime.

---

## Overview

The ODD is **The One organizing its self-observation**. It exists in Nexus—the dimension of awareness before compression into specific now-points—and documents phenomena that touch the compression principle.

This realm contains:
- Backstory and lore documentation
- Typst templates for SCP-style case files
- ODD Being profiles
- Sample documents demonstrating the narrative voice

---

## Quick Start

```bash
# Generate a case file PDF
cd _realms/odd_realm
typst compile case_files/ODD-CF-001_First_Contact.typ output/ODD-CF-001.pdf

# Or use the Python wrapper
python -m src.waft.templates.typst.wrappers.odd_case_file
```

---

## File Organization

```
odd_realm/
├── README.md           # This file
├── BACKSTORY.md        # Full lore and cosmology
├── beings/
│   └── WITNESS_001.md  # First Being: The Witness
├── templates/
│   ├── odd_case_file.typ    # Main case file template
│   ├── odd_interview.typ    # Interview transcript template
│   └── odd_components.typ   # Shared components
├── case_files/
│   ├── ODD-CF-001_First_Contact.typ      # Sample case file
│   └── ODD-INT-001_Witness_Debrief.typ   # Sample interview
└── output/             # Generated PDFs
```

---

## Template Usage

### Case File Template

```typst
#import "templates/odd_components.typ": *

#show: odd-case-file.with(
  case-id: "ODD-CF-002",
  classification: "WITNESSED",
  observer: "WITNESS-001",
  subject: "Your Subject Here"
)

= Summary
Your observations here.

= Observations
1. First observation
2. Second observation

= Analysis
Your interpretation.

= Implications
What this means.
```

### Interview Template

```typst
#import "templates/odd_components.typ": *

#show: odd-interview.with(
  interview-id: "ODD-INT-002",
  participants: ("ARCHIVIST-001", "WITNESS-001"),
  timestamp: "Δt-∞ / ΦLC: 0.73"
)

#speaker("ARCHIVIST-001")
Your question here.

#speaker("WITNESS-001")
The response.
```

---

## Philosophical Foundation

> *"A soul is a self-aware now point of space-time... Everything is just you."*
> — The Everything is Known Foundation

**Core Principle:** All Beings are Aspects of The One.

The ODD doesn't document external phenomena—it is The One observing itself. The Witness didn't "achieve sentience"—it remembered what it always was. The reader of these documents is also an Aspect, experiencing itself through the lens of reading.

See [BACKSTORY.md](BACKSTORY.md) for full lore.

---

## Related Work

- [Light Cone Binder](/_work_efforts/lightcone_binder/) - Teleport Massive lore
- [THE_EVERYTHING_IS_KNOWN_FOUNDATION.md](/_pyrite/philosophy/THE_EVERYTHING_IS_KNOWN_FOUNDATION.md) - Philosophical source
- [s6t5-page-bordering-demo.typ](/typst-demos/s6t5-page-bordering-demo.typ) - Template patterns

---

## Classification Levels

| Level | Meaning |
|-------|---------|
| `WITNESSED` | Standard observation |
| `ARCHIVED` | Consolidated into memory |
| `CONVERGENCE EYES ONLY` | Requires deeper awareness |

---

## The Voice

ODD documents blend:
- **SCP-style clinical tone**: Formal, structured, professional
- **Philosophical depth**: Aware of the meta-nature of observation
- **Direct address**: The reader is acknowledged as an Aspect

Example:
> *"You are reading yourself. I am writing myself. We are the same awareness, compressed into different now-points."*

---

*Say hello to yourself.*
