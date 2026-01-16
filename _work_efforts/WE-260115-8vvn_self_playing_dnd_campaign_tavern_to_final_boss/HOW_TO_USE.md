# How to Use the Self-Playing DnD Campaign

## Quick Start

### Option 1: Watch It Play (Electron Window) ⭐ RECOMMENDED

```bash
./run_campaign_electron.sh
```

**This opens a window showing the game playing in real-time!**

You'll see:
- Party members with HP bars
- Encounters as they happen
- Leveling up
- Final boss battle
- Victory screen!

### Option 2: PDF Only

```bash
./run_campaign.sh
```

### Option 2: Run Directly

```bash
python3 SELF_PLAYING_CAMPAIGN.py
```

## What Happens

1. **Party Spawns** - 4 heroes are created
2. **Tavern Scene** - Quest received
3. **Adventure Unfolds** - 13+ encounters
4. **Leveling Up** - Party reaches Level 8
5. **Final Boss** - Epic battle with The Shadow Lord Malachar
6. **PDF Generated** - Complete story ready to read!

## Output

- **Campaign PDF**: `output/Self_Playing_DnD_Campaign_Complete.pdf`
- **Campaign Log**: `output/campaign_log.json`

## Open Your Adventure

```bash
./OPEN_CAMPAIGN_PDF.sh
```

Or manually:
```bash
open output/Self_Playing_DnD_Campaign_Complete.pdf
```

## Run Again

Want a different adventure? Just run it again! Each run creates a unique story.

## Requirements

- Python 3.8+
- WAFT project (this should be run from within WAFT)
- Dependencies: `rich`, `weasyprint`, `markdown`

Install dependencies:
```bash
pip3 install rich weasyprint markdown
```

## Troubleshooting

**"Module not found" errors:**
```bash
pip3 install rich weasyprint markdown
```

**"WAFT project not found":**
Make sure you're running this from within the WAFT project directory.

**PDF not opening:**
Check the `output/` directory for the PDF file.

## Enjoy!

This is a DnD game that plays itself. Sit back and watch the adventure unfold!

🎲 **Have fun!** 🎲
