# Printing Fix: Prevent Duplicate Printing

**Date**: 2026-01-12  
**Issue**: Duplicate printing may be happening  
**Status**: ✅ FIXED

---

## Problem Identified

Multiple locations were automatically printing PDFs:
1. `experiments/deep_tavern_science_experiment.py` - Line 772: Auto-prints
2. `experiments/tavern_science_experiment.py` - Line 593: Auto-prints
3. `src/waft/core/science_bitch.py` - Line 344: Auto-prints in `_generate_report`
4. `src/waft/core/science_bitch.py` - Line 1076: Auto-prints in `generate_field_guide`
5. `src/waft/core/science_bitch.py` - Line 1158: Auto-prints in `generate_project_status_report`
6. Manual `open && lpr` command also executed

**Result**: PDF could be printed multiple times!

---

## Solution Implemented

### Changes Made

1. **`experiments/deep_tavern_science_experiment.py`**:
   - Changed: Auto-print → Open only
   - Added: `--print` flag for opt-in printing
   - Now: Opens PDF, shows print command, only prints if `--print` flag used

2. **`experiments/tavern_science_experiment.py`**:
   - Changed: Auto-print → Open only
   - Now: Opens PDF, shows print command

3. **`src/waft/core/science_bitch.py`**:
   - Changed: Auto-print → Show print command only
   - Now: Opens PDF, shows `lpr` command for manual printing
   - Applied to all 3 locations (report, field guide, status report)

### New Behavior

**Before**:
- PDF automatically printed (could print multiple times)
- No user control

**After**:
- PDF automatically opened for review
- Print command shown: `lpr {path}`
- User controls when to print
- Prevents duplicate printing

---

## Usage

### To Print (Manual)
```bash
lpr _science/reports/Deep_Tavern_Science_Experiment_*.pdf
```

### To Print (With Flag)
```bash
python3 experiments/deep_tavern_science_experiment.py --print
```

### Default Behavior
- Opens PDF automatically
- Shows print command
- User decides when to print

---

## Verification

✅ All automatic printing removed  
✅ PDFs now open only (for review)  
✅ Print commands shown (for manual printing)  
✅ `--print` flag added to deep experiment script  
✅ No duplicate printing possible

---

**Status**: ✅ FIXED  
**Result**: No more duplicate printing - user controls when to print
