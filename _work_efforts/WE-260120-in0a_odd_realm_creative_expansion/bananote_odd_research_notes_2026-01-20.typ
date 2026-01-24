#import "@preview/bananote:0.1.1": *
#import "@preview/scienceicons:0.1.0": open-access-icon, github-icon, website-icon

#show: note.with(
  title: [ODD Research Notes Web App],
  authors: (
    ([ctavolazzi], [WAFT / ODD]),
  ),
  date: datetime.today(),
  version: "0.1",
)

#abstract[
Notes on designing the ODD research notes web app (FastAPI + SvelteKit), with Typst ecosystem anchors for exports and iconography.
]

= Goals
- Create a new ODD research notes page linked to the existing ODD interface
- Keep research notes structured for Typst export
- Align note-taking with the Typst ecosystem anchors

= Science Anchors
- #website-icon() scienceicons: https://typst.app/universe/package/scienceicons
- #github-icon() typst/packages: https://github.com/typst/packages
- #website-icon() may template: https://typst.app/universe/package/may/
- #website-icon() bookly template: https://typst.app/universe/package/bookly/
- #website-icon() owlbear template: https://typst.app/universe/package/owlbear/
- #website-icon() Typst template tutorial: https://typst.app/docs/tutorial/making-a-template/

= Observations
- ODD already ships a static interface (`_realms/odd_realm/index.html`) served by FastAPI.
- The new research notes UI should mirror ODD styling but offer structured note storage.
- Typst templates (bananote, may, bookly, owlbear) offer different export modes: note, daily report, long-form, and styled worldbook.

= Hypotheses
- A lightweight JSON store + FastAPI endpoint is sufficient for capturing research notes.
- SvelteKit provides a clean UI layer for structured input and live review.
- Typst export paths should remain linked to notes for offline archival.

= Experiments (Planned)
- Capture seed notes from the Typst ecosystem and export to PDF.
- Validate link flow between ODD core page and research notes page.
- Test whether the notes API handles multi-line content and source lists cleanly.

= Decisions
- Use a dedicated ODD notes JSON file under `_realms/odd_realm/notes/`.
- Keep the notes UI accessible at `/odd-notes` and link back to the ODD core page.

= Next Steps
- Implement SvelteKit UI and FastAPI endpoints.
- Add explicit link from ODD core page to the notes UI.
- Document export pathways for bananote + Flow Way.

= Work Log
- 21:53 PST: Updated notes URL to SvelteKit default port 5173 to avoid collisions with the card game.
