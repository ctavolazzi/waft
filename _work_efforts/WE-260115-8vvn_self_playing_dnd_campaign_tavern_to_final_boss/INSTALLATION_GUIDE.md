# Installation Guide: Self-Playing DnD Campaign

**Make it easy for others to experience the joy!**

---

## Quick Install

### Step 1: Run the Installer

```bash
cd _work_efforts/WE-260115-8vvn_self_playing_dnd_campaign_tavern_to_final_boss
./install.sh
```

The installer will:
- ✅ Check Python 3.8+
- ✅ Verify WAFT project
- ✅ Check/install dependencies (rich, weasyprint, markdown)
- ✅ Make scripts executable
- ✅ Create output directory
- ✅ Create runner script
- ✅ Create user guide

### Step 2: Run the Campaign

```bash
./run_campaign.sh
```

### Step 3: Read Your Adventure

```bash
./OPEN_CAMPAIGN_PDF.sh
```

---

## Manual Installation

If the installer doesn't work, you can install manually:

### 1. Install Dependencies

```bash
pip3 install rich weasyprint markdown
```

### 2. Make Scripts Executable

```bash
chmod +x SELF_PLAYING_CAMPAIGN.py
chmod +x OPEN_CAMPAIGN_PDF.sh
```

### 3. Create Output Directory

```bash
mkdir -p output
```

### 4. Run

```bash
python3 SELF_PLAYING_CAMPAIGN.py
```

---

## Requirements

### System Requirements

- **Python**: 3.8 or higher
- **OS**: macOS, Linux, or Windows (with WSL)
- **WAFT Project**: Must be run from within WAFT project

### Python Dependencies

- `rich` - Beautiful terminal output
- `weasyprint` - PDF generation (no LaTeX needed)
- `markdown` - Markdown processing

Install all:
```bash
pip3 install rich weasyprint markdown
```

---

## What Gets Installed

### Scripts

- `SELF_PLAYING_CAMPAIGN.py` - Main campaign script
- `run_campaign.sh` - Quick runner script
- `OPEN_CAMPAIGN_PDF.sh` - PDF opener
- `install.sh` - Installer script

### Documentation

- `HOW_TO_USE.md` - User guide
- `README.md` - Overview
- `WELCOME_BACK.md` - Welcome message
- `CAMPAIGN_COMPLETE.md` - Completion summary

### Output

- `output/` - Directory for generated PDFs and logs

---

## Verification

After installation, verify everything works:

```bash
# Check Python
python3 --version

# Check dependencies
python3 -c "import rich, weasyprint, markdown; print('✓ All dependencies installed')"

# Check scripts
ls -la *.py *.sh

# Run a test
./run_campaign.sh
```

---

## Troubleshooting

### "Python not found"

Install Python 3.8+:
- macOS: `brew install python3`
- Linux: `sudo apt-get install python3`
- Windows: Download from python.org

### "Module not found"

Install dependencies:
```bash
pip3 install rich weasyprint markdown
```

### "WAFT project not found"

Make sure you're running from within the WAFT project:
```bash
cd /path/to/waft/_work_efforts/WE-260115-8vvn_self_playing_dnd_campaign_tavern_to_final_boss
./install.sh
```

### "Permission denied"

Make scripts executable:
```bash
chmod +x install.sh run_campaign.sh OPEN_CAMPAIGN_PDF.sh
```

### PDF not generating

Check WeasyPrint installation:
```bash
python3 -c "from weasyprint import HTML; print('WeasyPrint OK')"
```

If it fails, install system dependencies:
- macOS: `brew install cairo pango gdk-pixbuf libffi`
- Linux: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0`

---

## Sharing with Others

### Option 1: Share the Work Effort

Share the entire work effort directory:
```
_work_efforts/WE-260115-8vvn_self_playing_dnd_campaign_tavern_to_final_boss/
```

They can then:
1. Navigate to the directory
2. Run `./install.sh`
3. Run `./run_campaign.sh`

### Option 2: Create a Standalone Package

You could create a standalone package that includes:
- The campaign script
- A requirements.txt
- Installation instructions
- README

### Option 3: GitHub Repository

Create a GitHub repo with:
- The campaign script
- Installation guide
- Example output
- README

---

## Quick Reference

### Install
```bash
./install.sh
```

### Run Campaign
```bash
./run_campaign.sh
```

### Open PDF
```bash
./OPEN_CAMPAIGN_PDF.sh
```

### Check Status
```bash
ls -la output/
```

---

## For Developers

### Project Structure

```
WE-260115-8vvn_self_playing_dnd_campaign_tavern_to_final_boss/
├── install.sh                    # Installer
├── SELF_PLAYING_CAMPAIGN.py      # Main script
├── run_campaign.sh               # Runner script
├── OPEN_CAMPAIGN_PDF.sh          # PDF opener
├── HOW_TO_USE.md                 # User guide
├── README.md                     # Overview
├── output/                       # Generated files
│   ├── Self_Playing_DnD_Campaign_Complete.pdf
│   └── campaign_log.json
└── tickets/                      # Work tracking
```

### Dependencies

The campaign uses:
- **WAFT Being System** - For party members
- **PDFGenerator** - For PDF creation (WeasyPrint)
- **Rich** - For beautiful terminal output
- **Python Standard Library** - For everything else

**All free and open source!**

---

## Success Indicators

After installation, you should see:

```
✅ Installation Complete!

📋 Quick Start:
   1. Run: ./run_campaign.sh
   2. Wait for the adventure to unfold
   3. Open: ./OPEN_CAMPAIGN_PDF.sh

🎲 Ready to experience a DnD game that plays itself!
```

---

**Status**: ✅ **Installer Ready!**

🎲 **Share the joy!** 🎲
