---
id: WE-260116-5exf
title: "LaTeX Alternatives Evaluation"
status: active
created: 2026-01-17T04:58:04.353Z
created_by: ctavolazzi
last_updated: 2026-01-17T04:58:04.353Z
branch: feature/WE-260116-5exf-latex_alternatives_evaluation
repository: waft
---

# WE-260116-5exf: LaTeX Alternatives Evaluation

## Metadata
- **Created**: Friday, January 16, 2026 at 8:58:04 PM PST
- **Author**: ctavolazzi
- **Repository**: waft
- **Branch**: feature/WE-260116-5exf-latex_alternatives_evaluation

## Objective
Document and evaluate modern LaTeX alternatives (Typst, ConTeXt, Quarto, Pandoc) for WAFT's typesetting needs, comparing them against existing LaTeX infrastructure and other PDF generation systems to provide actionable recommendations.

## Tickets

| ID | Title | Status |
|----|-------|--------|
| (no tickets yet) | | |

## Commits
- (populated as work progresses)

## Related
- **Evaluation Document**: [`docs/LATEX_ALTERNATIVES_EVALUATION.md`](../../docs/LATEX_ALTERNATIVES_EVALUATION.md)
- **Summary**: [`EVALUATION_SUMMARY.md`](EVALUATION_SUMMARY.md)
- **Related Work**: 
  - `WE-260116-xkhg`: Formal letter template (chose LaTeX over ConTeXt/Typst)
  - `docs/FOUNDATION_V3_ROADMAP.md`: ReportLab/WeasyPrint alternatives
  - `WAFT-Mac-Shortcuts-Research/notes/pdf_systems_analysis.md`: Current PDF systems
- PRs: (to be added)

## Status

✅ **Evaluation Complete**

**Key Findings:**
- Typst is the most promising modern alternative (faster, simpler syntax)
- ConTeXt offers better consistency but high migration cost
- Quarto excellent for reproducible research but overkill for general templates
- Pandoc good for Markdown workflows

**Recommendations:**
- Continue with LaTeX for existing templates
- Consider Typst for new templates (create proof of concept)
- Hybrid approach long-term (different tools for different use cases)
