#import "@preview/bananote:0.1.1": *

#show: note.with(
  title: [Card-Game-Simulator Full Cycle Notes],
  authors: (
    ([ctavolazzi], [WAFT]),
  ),
  date: datetime.today(),
  version: "0.1",
)

#abstract[Running notes for the Card-Game-Simulator full-cycle plan.]

= Goal
- Execute the full-cycle plan: clone, analyze, critique, respond, science-bitch, another-cycle, booklet, auto-work.

= Context
- Work effort: WE-260120-4q9l
- Clone failed due to disk space; cleanup path selected.

= Findings
- Clone attempt failed: "No space left on device".
- Disk free on /System/Volumes/Data: 5.4Gi (98% used).
- Largest repo entries: waft_pdf_library (1.5G), _realms (938M), waft_desktop (475M), _work_efforts (345M), templates (204M).
- Bananote PDF compiled with font warnings: unknown font family "new computer modern sans".
- Copied to /Volumes/Easystore/waft_cleanup_2026-01-20_copy1 (waft_pdf_library, _realms, waft_desktop, _work_efforts, templates, .venv).
- Destination sizes are larger than source (indicates pre-existing data or non-empty destination).

= Decisions
- Proceed with cleanup before retrying clone.
- Keep current PDF output; revisit font availability if formatting is off.
- Keep copies; confirm if a clean mirror is needed.

= TODO
- Decide whether to re-copy into a fresh empty destination.
- Propose deletion candidates with backup verification.
- Retry clone after space is freed.

= Next Steps
- Confirm deletion targets after backup verification.
- Retry clone.

= Logs
- 2026-01-20: Kickoff logged in devlog; work effort created.
- 2026-01-20: Clone failed due to disk space; cleanup path selected.
- 2026-01-20: Disk audit shows 5.4Gi free; top directories identified.
- 2026-01-20: Bananote compiled to PDF with font warnings.
- 2026-01-20: Copied large directories to Easystore; destination appears non-empty.
