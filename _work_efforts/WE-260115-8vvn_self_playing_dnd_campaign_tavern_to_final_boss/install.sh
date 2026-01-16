#!/bin/bash
# Self-Playing DnD Campaign Installer
# Makes it easy for others to experience the joy of a DnD game that plays itself!

set -e

echo "🎲 Self-Playing DnD Campaign Installer"
echo "======================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo -e "${BLUE}📋 Checking requirements...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 not found. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"

# Check if we're in WAFT project
if [ ! -f "$PROJECT_ROOT/src/waft/being.py" ]; then
    echo -e "${YELLOW}⚠️  WAFT project not found. This installer expects to be run from within the WAFT project.${NC}"
    echo -e "${YELLOW}   Current directory: $PROJECT_ROOT${NC}"
    echo -e "${YELLOW}   Please run this from: _work_efforts/WE-260115-8vvn_self_playing_dnd_campaign_tavern_to_final_boss/${NC}"
    exit 1
fi

echo -e "${GREEN}✓${NC} WAFT project found"

# Check Python dependencies
echo -e "${BLUE}📦 Checking Python dependencies...${NC}"

MISSING_DEPS=()

check_dependency() {
    if python3 -c "import $1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $1 installed"
    else
        echo -e "${YELLOW}⚠️  $1 not found${NC}"
        MISSING_DEPS+=("$1")
    fi
}

check_dependency "rich"
check_dependency "weasyprint"

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}📦 Installing missing dependencies...${NC}"
    pip3 install rich weasyprint markdown || {
        echo -e "${YELLOW}⚠️  Failed to install dependencies. Please run: pip3 install rich weasyprint markdown${NC}"
        exit 1
    }
    echo -e "${GREEN}✓${NC} Dependencies installed"
fi

# Make script executable
echo ""
echo -e "${BLUE}🔧 Setting up scripts...${NC}"

chmod +x "$SCRIPT_DIR/SELF_PLAYING_CAMPAIGN.py" 2>/dev/null || true
chmod +x "$SCRIPT_DIR/OPEN_CAMPAIGN_PDF.sh" 2>/dev/null || true

echo -e "${GREEN}✓${NC} Scripts made executable"

# Create output directory
OUTPUT_DIR="$SCRIPT_DIR/output"
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}✓${NC} Output directory ready: $OUTPUT_DIR"

# Create a simple runner script
RUNNER_SCRIPT="$SCRIPT_DIR/run_campaign.sh"
cat > "$RUNNER_SCRIPT" << 'EOF'
#!/bin/bash
# Quick runner for the self-playing DnD campaign

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$PROJECT_ROOT"

echo "🎲 Starting Self-Playing DnD Campaign..."
echo ""

python3 "$SCRIPT_DIR/SELF_PLAYING_CAMPAIGN.py"

echo ""
echo "✅ Campaign complete! Check the output directory for your PDF!"
EOF

chmod +x "$RUNNER_SCRIPT"
echo -e "${GREEN}✓${NC} Runner script created: run_campaign.sh"

# Create README for users
USER_README="$SCRIPT_DIR/HOW_TO_USE.md"
cat > "$USER_README" << 'EOF'
# How to Use the Self-Playing DnD Campaign

## Quick Start

### Option 1: Use the Runner Script

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
EOF

echo -e "${GREEN}✓${NC} User guide created: HOW_TO_USE.md"

# Summary
echo ""
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo ""
echo "📋 Quick Start:"
echo "   1. Run: ./run_campaign.sh"
echo "   2. Wait for the adventure to unfold"
echo "   3. Open: ./OPEN_CAMPAIGN_PDF.sh"
echo ""
echo "📖 For more info, see: HOW_TO_USE.md"
echo ""
echo -e "${BLUE}🎲 Ready to experience a DnD game that plays itself!${NC}"
echo ""
