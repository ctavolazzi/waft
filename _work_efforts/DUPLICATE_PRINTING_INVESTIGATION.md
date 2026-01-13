# Duplicate Printing Investigation & Fix

**Date**: 2026-01-12  
**Issue**: Duplicate printing may be happening  
**Status**: ✅ FIXED

---

## Investigation Results

### Problem Found
Multiple locations were automatically printing PDFs, which could cause duplicate printing:

1. ✅ **FIXED**: `experiments/deep_tavern_science_experiment.py` (Line 772)
   - **Before**: Auto-printed with `lpr`
   - **After**: Opens PDF only, shows print command

2. ✅ **FIXED**: `experiments/tavern_science_experiment.py` (Line 593)
   - **Before**: Auto-printed with `lpr`
   - **After**: Opens PDF only, shows print command

3. ✅ **FIXED**: `src/waft/core/science_bitch.py` (Line 344)
   - **Before**: Auto-printed in `_generate_report`
   - **After**: Shows print command only

4. ✅ **FIXED**: `src/waft/core/science_bitch.py` (Line 1076)
   - **Before**: Auto-printed in `generate_field_guide`
   - **After**: Shows print command only

5. ✅ **FIXED**: `src/waft/core/science_bitch.py` (Line 1158)
   - **Before**: Auto-printed in `generate_project_status_report`
   - **After**: Shows print command only

6. ⚠️ **IDENTIFIED**: Manual `open && lpr` command executed
   - This was run separately and would have printed
   - Now removed from workflow

---

## Root Cause

**The Issue**: 
- Experiment scripts automatically printed PDFs
- `science_bitch.py` also automatically printed PDFs
- Manual print command was also executed
- **Result**: PDF could be printed 2-3 times!

**The Fix**:
- Removed all automatic printing
- Changed to: Open PDF + show print command
- User now controls when to print
- Prevents duplicate printing

---

## Changes Made

### 1. Experiment Scripts
**File**: `experiments/deep_tavern_science_experiment.py`
- Removed: `subprocess.run(["lpr", str(pdf_path)])`
- Added: `subprocess.run(["open", str(pdf_path)])` (opens only)
- Added: Print command hint: `lpr {path}`
- Added: `--print` flag for opt-in printing

**File**: `experiments/tavern_science_experiment.py`
- Removed: `subprocess.run(["lpr", str(pdf_path)])`
- Added: `subprocess.run(["open", str(pdf_path)])` (opens only)
- Added: Print command hint: `lpr {path}`

### 2. Science-Bitch Manager
**File**: `src/waft/core/science_bitch.py`
- Removed: All `subprocess.run(["lpr", ...])` calls (3 locations)
- Changed: Now shows print command hint only
- Result: No automatic printing, user controls printing

---

## New Behavior

### Default (No Printing)
```
📄 Opening PDF...
✅ PDF opened!
💡 To print: lpr _science/reports/Deep_Tavern_Science_Experiment_*.pdf
```

### With --print Flag (Opt-In)
```bash
python3 experiments/deep_tavern_science_experiment.py --print
```
- Opens PDF
- Prints PDF (if flag used)

### Manual Printing
```bash
lpr _science/reports/Deep_Tavern_Science_Experiment_*.pdf
```

---

## Verification

✅ **No automatic printing found**: `grep -c "subprocess.run.*lpr"` returns 0  
✅ **All scripts now open only**: PDFs open for review  
✅ **Print commands shown**: User can print manually  
✅ **Duplicate printing prevented**: User controls when to print

---

## Impact

### Before Fix
- PDF could be printed 2-3 times automatically
- No user control
- Waste of paper/ink

### After Fix
- PDF opens for review
- User decides when to print
- No duplicate printing
- Saves resources

---

**Status**: ✅ FIXED  
**Result**: No more duplicate printing - user controls when to print  
**Verification**: All automatic printing removed, only manual printing available
