# Check Assumptions: Empirica TUI Dashboard Manual

Date: 2026-01-19
Session: 207d5a64-bd63-4336-bb7a-f3bf6972959f

## Assumptions
1. Empirica CLI is installed and usable.
2. WAFT has PDF generation capabilities available locally.
3. The field guide template is appropriate for a user manual.
4. The Empirica TUI dashboard scripts are available through the Empirica package.
5. The project has a valid `.empirica/` directory for session storage.

## Validation Evidence
- Empirica CLI check: `empirica session-create` succeeded (session_id created).
- WAFT PDF tooling: `src/waft/pdf.py` and `src/waft/document_builder.py` present.
- Field guide template: `src/waft/templates/field_guide.py` exists with manual-style layout.
- Empirica dashboards: `empirica/dashboard/README.md` and `empirica/tui/dashboard.py` present in the local Empirica repo.
- Project state: `.empirica/` directory exists in repo root.

## Findings
All assumptions are supported enough to proceed. Dependency availability for WeasyPrint/Textual will be validated during PDF generation and dashboard integration steps.
