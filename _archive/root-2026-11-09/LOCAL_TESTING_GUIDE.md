# PROJECT LIGHTCONE - Local Testing Guide

**Purpose**: Test PDF generation on your local machine
**Time Required**: 15-30 minutes
**Skill Level**: Basic command line usage

---

## Quick Start (TL;DR)

```bash
# 1. Navigate to repository
cd /path/to/waft

# 2. Checkout the branch
git checkout claude/update-plan-merge-gFm6u
git pull origin claude/update-plan-merge-gFm6u

# 3. Install dependencies
pip install fpdf2>=2.7.0

# 4. Run verification script
python verify_environment.py

# 5. Generate PDFs (test mode - 4 documents)
python -m src.waft.generate_lightcone_docs

# 6. Check output
ls -lh _work_efforts/lightcone_binder/pdf/
```

---

## Step-by-Step Instructions

### Step 1: Repository Setup

**Navigate to your waft repository**:
```bash
cd /path/to/waft
# Replace /path/to/waft with your actual path
# Example: cd ~/Documents/waft
```

**Verify you're in the right place**:
```bash
pwd
# Should show: /path/to/waft
ls
# Should show: src/, _work_efforts/, pyproject.toml, etc.
```

**Checkout the branch with all the work**:
```bash
git checkout claude/update-plan-merge-gFm6u
git pull origin claude/update-plan-merge-gFm6u
```

**Expected output**:
```
Already on 'claude/update-plan-merge-gFm6u'
Already up to date.
```

---

### Step 2: Environment Setup

**Check Python version**:
```bash
python --version
# OR
python3 --version
```

**Required**: Python 3.10 or higher

**If Python version is too old**:
- macOS: `brew install python@3.11`
- Ubuntu/Debian: `sudo apt install python3.11`
- Windows: Download from python.org

**Optional but recommended: Create virtual environment**:
```bash
# Create venv
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Your prompt should now show (venv)
```

---

### Step 3: Install Dependencies

**Install fpdf2** (PDF generation library):
```bash
pip install fpdf2>=2.7.0
```

**Expected output**:
```
Collecting fpdf2>=2.7.0
  Downloading fpdf2-X.X.X-py3-none-any.whl
Installing collected packages: fpdf2
Successfully installed fpdf2-X.X.X
```

**Verify installation**:
```bash
python -c "from fpdf import FPDF; print('✅ fpdf2 installed successfully')"
```

**If you get an error about cryptography/cffi**:
```bash
# Update pip and setuptools first
pip install --upgrade pip setuptools

# Try installing in clean environment
deactivate  # if in venv
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install fpdf2>=2.7.0
```

---

### Step 4: Verify Environment

**I've created a verification script for you. Run it**:
```bash
python verify_environment.py
```

**This will check**:
- ✅ Python version
- ✅ Repository structure
- ✅ Branch status
- ✅ fpdf2 installation
- ✅ DocumentEngine imports
- ✅ Generation module exists
- ✅ Markdown sources exist

**Expected output**:
```
🔍 PROJECT LIGHTCONE Environment Verification
================================================

✅ Python 3.11.x detected
✅ Repository structure valid
✅ Branch: claude/update-plan-merge-gFm6u
✅ fpdf2 installed and working
✅ DocumentEngine imports successful
✅ Generation module found (1041 lines)
✅ Markdown sources found (13/13 files)

================================================
🎉 ALL CHECKS PASSED - Ready to generate PDFs!
================================================
```

**If any checks fail**, the script will tell you what's wrong and how to fix it.

---

### Step 5: Generate Test PDFs

**Run the generation module**:
```bash
python -m src.waft.generate_lightcone_docs
```

**What this does**:
- Generates 4 PDFs (Tab 1-2: TM-VIS-001, TM-MEMO-042, TM-ENG-004, TM-ENG-114)
- Creates directory structure in `_work_efforts/lightcone_binder/pdf/`
- Shows progress as it generates each document

**Expected output**:
```
================================================================================
PROJECT LIGHTCONE MASTER FILE BINDER GENERATION
================================================================================

Generating Tab 1: Doctrine & Theory...
  ✓ TM-VIS-001: TM-VIS-001_Light_Cone_Topology.pdf
  ✓ TM-MEMO-042: TM-MEMO-042_The_God_Problem.pdf

Generating Tab 2: Engineering & Hardware...
  ✓ TM-ENG-004: TM-ENG-004_Suspension9_MSDS.pdf
  ✓ TM-ENG-114: TM-ENG-114_Lazarus_Protocol.pdf ⭐ CORE TECHNOLOGY

Tab 2 (remaining), Tab 3-5: Coming soon...

================================================================================
GENERATION COMPLETE
================================================================================
```

**Time**: Should take 5-15 seconds total

---

### Step 6: Verify PDF Output

**Check that PDFs were created**:
```bash
ls -lh _work_efforts/lightcone_binder/pdf/tab1_doctrine/
ls -lh _work_efforts/lightcone_binder/pdf/tab2_engineering/
```

**Expected output**:
```
tab1_doctrine/:
-rw-r--r--  1 user  staff   24K Jan 11 12:00 TM-VIS-001_Light_Cone_Topology.pdf
-rw-r--r--  1 user  staff   18K Jan 11 12:00 TM-MEMO-042_The_God_Problem.pdf

tab2_engineering/:
-rw-r--r--  1 user  staff   22K Jan 11 12:00 TM-ENG-004_Suspension9_MSDS.pdf
-rw-r--r--  1 user  staff   35K Jan 11 12:00 TM-ENG-114_Lazarus_Protocol.pdf
```

**PDF sizes should be reasonable** (15-40 KB each)

---

### Step 7: Open and Review PDFs

**Open a PDF**:
```bash
# macOS:
open _work_efforts/lightcone_binder/pdf/tab2_engineering/TM-ENG-114_Lazarus_Protocol.pdf

# Linux:
xdg-open _work_efforts/lightcone_binder/pdf/tab2_engineering/TM-ENG-114_Lazarus_Protocol.pdf

# Windows:
start _work_efforts/lightcone_binder/pdf/tab2_engineering/TM-ENG-114_Lazarus_Protocol.pdf
```

**What to check**:
- ✅ PDF opens without errors
- ✅ Text is readable
- ✅ Headers/footers look correct
- ✅ Classification warnings visible
- ✅ Overall styling looks good

**Recommended: Open TM-ENG-114 (Lazarus Protocol)** - this is the crown jewel document with the most content.

---

### Step 8: Test Print (Optional)

**Print a single page to test quality**:
1. Open TM-ENG-114_Lazarus_Protocol.pdf
2. Print page 1 only
3. Check print quality, margins, readability

**If margins are wrong**:
- Check printer settings (scaling should be 100%, no "fit to page")
- Verify page size matches printer (A4 vs. US Letter)

**If text is too small/large**:
- This is expected - designed for binder printing
- Should be readable but dense (1990s photocopied aesthetic)

---

## Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'fpdf'"

**Solution**:
```bash
pip install fpdf2>=2.7.0
```

### Issue 2: "ModuleNotFoundError: No module named 'waft.foundation'"

**Cause**: Waft package not installed or wrong directory

**Solution**:
```bash
# Make sure you're in the waft root directory
pwd  # Should show /path/to/waft

# Install waft in development mode
pip install -e .
```

### Issue 3: "ImportError: cannot import name 'DocumentConfig'"

**Cause**: DocumentEngine not available

**Solution**:
```bash
# Check if foundation.py exists
ls src/waft/foundation.py

# If it exists, verify imports manually
python -c "from waft.foundation import DocumentConfig; print('OK')"
```

### Issue 4: Cryptography/cffi errors

**Solution**:
```bash
# Clean install in fresh virtual environment
deactivate  # if in venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install fpdf2>=2.7.0
```

### Issue 5: PDFs generate but look wrong

**Check**:
1. Compare with `_fracture/ARTIFACT_001_GENESIS.pdf` (style reference)
2. Verify page size setting (A4 vs US Letter)
3. Check if fonts are available on your system

**If headers/footers missing**:
- This might be FPDF vs DocumentEngine difference
- Tab 1 uses FPDF (custom headers), Tab 2 uses DocumentEngine (simpler)

### Issue 6: "Permission denied" when generating PDFs

**Solution**:
```bash
# Check write permissions
ls -ld _work_efforts/lightcone_binder/

# If needed, create directories manually
mkdir -p _work_efforts/lightcone_binder/pdf/{tab1_doctrine,tab2_engineering}
```

---

## Next Steps After Testing

### If everything works ✅

**Option 1: Continue with current 4 PDFs**
- You have the core documents
- TM-ENG-114 Lazarus Protocol is the most important
- Can print these now and add more later

**Option 2: Complete all generators**
- I implement remaining 9 generators
- You generate all 13 PDFs
- Print complete binder in one session

**Option 3: Provide feedback first**
- Review the 4 PDFs
- Suggest styling adjustments
- Then I complete the rest with improvements

### If something doesn't work ❌

**Report the issue**:
1. What command you ran
2. What error message you got
3. Your Python version (`python --version`)
4. Your operating system

**I'll help troubleshoot**:
- Provide specific fixes
- Create alternative solutions
- Adjust code if needed

---

## Testing Checklist

Use this to track your progress:

- [ ] Navigated to waft repository
- [ ] Checked out correct branch
- [ ] Pulled latest changes
- [ ] Python 3.10+ installed
- [ ] Created virtual environment (optional)
- [ ] Installed fpdf2
- [ ] Ran verify_environment.py
- [ ] All checks passed
- [ ] Ran generate_lightcone_docs
- [ ] 4 PDFs generated without errors
- [ ] Opened and reviewed TM-ENG-114
- [ ] Styling looks correct
- [ ] Test printed 1 page (optional)
- [ ] Ready to proceed with full generation

---

## Quick Reference

**Generate PDFs**:
```bash
python -m src.waft.generate_lightcone_docs
```

**Find PDFs**:
```bash
cd _work_efforts/lightcone_binder/pdf/
ls -R
```

**Open PDF** (macOS):
```bash
open tab2_engineering/TM-ENG-114_Lazarus_Protocol.pdf
```

**Regenerate** (deletes old PDFs and creates new ones):
```bash
rm -rf _work_efforts/lightcone_binder/pdf/
python -m src.waft.generate_lightcone_docs
```

---

**Ready to test?** Start with Step 1!

**Questions?** Let me know what command failed and I'll help debug.

**Working?** Let me know if you want me to implement the remaining 9 generators!
