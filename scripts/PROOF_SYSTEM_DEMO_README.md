# 🔬 Proof System Interactive Demo

An interactive, Colab-style demo page for testing the WAFT proof system with real claims.

## Quick Start

```bash
# Start the demo server
python3 scripts/proof_system_demo_server.py

# Then open your browser to:
# http://localhost:8000
```

## What It Does

This interactive demo demonstrates the **claim analysis fix** we just implemented:

1. **Enter a claim** - Type or click an example claim
2. **Run proof** - Click "Run Proof" to analyze the claim
3. **See results** - View claim analysis, verification type, target files, and proof results

## Example Claims

### HTML Report Features
```
The show-me HTML report (show_me_bulletproof.py) implements a unified 
above-the-fold section with ID above-the-fold, responsive design with 
mobile breakpoints, and an abstract copy button that uses the clipboard API
```

### Template Black Bars
```
All PDF templates have been fixed to remove black bars from headers
```

### Proof System Analysis
```
The proof system can analyze claims and determine what to test
```

## Features

✅ **Claim Analysis** - Automatically identifies verification type (HTML, Template, JavaScript, etc.)  
✅ **Target File Detection** - Finds relevant files mentioned in claims  
✅ **Feature Extraction** - Identifies specific features to verify  
✅ **Proof Results** - Shows proven/disproven/inconclusive assumptions with evidence  
✅ **Interactive UI** - Colab-style interface with clickable examples  

## How It Works

1. **Server** (`proof_system_demo_server.py`):
   - Runs a local HTTP server on port 8000
   - Accepts POST requests with claims
   - Runs the actual proof system
   - Returns JSON results

2. **Client** (HTML page):
   - Provides interactive UI
   - Sends claims to server
   - Displays formatted results
   - Shows evidence and confidence scores

## Key Demonstration

This demo shows the **critical fix** we implemented:

**Before:** System always checked PDF templates for black bars, regardless of claim  
**After:** System analyzes claim to determine what to test

### Example Flow

1. Enter HTML report claim
2. System identifies: `verification_type: "html"`
3. System finds: `target_files: ["scripts/show_me_bulletproof.py"]`
4. System checks: `features_to_check: ["above-the-fold", "responsive_design", "abstract_copy_button", "clipboard_api"]`
5. System verifies each feature and returns proof results

## Files

- `proof_system_demo_server.py` - Server that runs the proof system
- `proof_system_demo.html` - Standalone HTML demo (simplified, no server needed)
- `PROOF_SYSTEM_DEMO_README.md` - This file

## Usage

### Option 1: Full Interactive Demo (Recommended)

```bash
python3 scripts/proof_system_demo_server.py
```

Then open http://localhost:8000 in your browser.

### Option 2: Standalone HTML

Open `scripts/proof_system_demo.html` in your browser (limited functionality, shows concept).

## API

The server exposes a `/prove` endpoint:

**POST /prove**
```json
{
  "claim": "Your claim here"
}
```

**Response:**
```json
{
  "analysis": {
    "verification_type": "html",
    "target_files": ["scripts/show_me_bulletproof.py"],
    "features_to_check": ["above-the-fold", "responsive_design"]
  },
  "total": 4,
  "proven": 4,
  "disproven": 0,
  "inconclusive": 0,
  "assumptions": [...]
}
```

## Troubleshooting

**Port already in use?**
```bash
# Use a different port
python3 scripts/proof_system_demo_server.py --port 8001
```

**Module not found?**
```bash
# Make sure you're in the project root
cd /Users/ctavolazzi/Code/active/waft
python3 scripts/proof_system_demo_server.py
```

## Next Steps

- Add more verification types (JavaScript, CSS, Python)
- Add visualization of proof results
- Add export to PDF functionality
- Add claim history/saved claims
