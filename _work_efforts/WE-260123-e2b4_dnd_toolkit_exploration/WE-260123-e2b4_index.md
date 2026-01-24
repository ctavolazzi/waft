# Work Effort: D&D 5e Toolkit Exploration

## Status: Completed
**Started:** 2026-01-23
**Last Updated:** 2026-01-24

## Objective

Explore and catalog 6 D&D/RPG-related repositories cloned into `_external/` for potential feature extraction and integration into WAFT content generation workflows.

## Deliverable: D&D Toolkit Hub

Built a fully functional web-based toolkit at `_tools/dnd-toolkit/`:

### Features
- **SRD Browser** - Search 323 monsters, 319 spells, 586 items
- **Homebrew Creator** - Forms for monsters, spells, items with export to JSON/Markdown/Card
- **Card Generator** - Queue system with preview, exports to rpg-cards format
- **Tools Hub** - Links to Dungeoneer VTT, rpg-cards, donjon converter, SRD

### Tech Stack
- RPGUI for styling (CSS/JS)
- Vanilla JavaScript (no dependencies)
- Static files (no server required)

### To Use
Open `_tools/dnd-toolkit/index.html` in a browser.

## Repositories Cloned

| Repo | Purpose | Tech Stack |
|------|---------|------------|
| `dungeoneer` | VTT with maps, combat, generators | Electron, JavaScript |
| `dnd5e-srd` | Full SRD in Obsidian markdown | Markdown |
| `aurora-homebrew-gui` | Python/Tkinter form pattern | Python, Tkinter |
| `rpgui` | CSS framework for RPG-styled web UI | CSS, JavaScript |
| `donjon-to-homebrewery` | AI dungeon enhancement + Homebrewery output | Python, OpenAI |
| `rpg-cards` | Printable spell/item/monster cards | HTML, CSS, JavaScript |

## Dependencies Not Yet Installed

Manual installation required:

```bash
# rpg-cards (web card generator)
cd _external/rpg-cards && npm install && npm start

# donjon-to-homebrewery (Python)
cd _external/donjon-to-homebrewery
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Dungeoneer VTT (Electron)
cd _external/dungeoneer && yarn install
# May need: yarn remove sharp && yarn add sharp (macOS)
```

## Potential Extractions

| Source | Feature to Extract |
|--------|-------------------|
| Dungeoneer | Encounter difficulty calc, random tables, token processing |
| dnd5e-srd | Structured monster/spell data for PDF generation |
| Aurora-Homebrew-GUI | Tkinter form pattern for content creation |
| donjon_to_homebrewery | AI dungeon enhancement, Homebrewery markdown format |
| rpg-cards | Card layout templates, JSON card schema |
| RPGUI | CSS styling for RPG-themed web UI |

## Future Vision: Universal D&D Content Pipeline

```
Input (donjon, SRD, homebrew)
  → Processing (AI, Form UI)
    → Output (JSON/Markdown/Cards/PDF)
```

## Next Steps

1. [ ] Explore Dungeoneer's generator architecture
2. [ ] Study rpg-cards JSON schema for card data
3. [ ] Test donjon_to_homebrewery with sample dungeon
4. [ ] Evaluate RPGUI for homebrew creator styling
5. [ ] Cross-reference SRD data with existing `create_dnd_binder_fpdf.py`

## Related Files

- Plan: `~/.cursor/plans/clone_dungeoneer_vtt_d905f09d.plan.md`
- Existing D&D work: `create_dnd_binder_fpdf.py`
- External repos: `_external/`

## Notes

- Dungeoneer and dnd5e-srd were already cloned previously
- Also have `slaytheweb` (card-based roguelike) in `_external/`
