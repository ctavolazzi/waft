# Demo Script Creation

**Date**: 2026-01-06
**File**: `demo.py`

## Purpose

Created an interactive demo script that showcases all of waft's core capabilities in a single, runnable demonstration.

## Features Demonstrated

1. **Memory Manager**
   - Creating _pyrite structure
   - Adding files to active/ and backlog/
   - Listing files by location
   - Verifying structure

2. **Substrate Manager**
   - Reading project information (name, version)
   - Checking uv.lock status
   - Dependency management workflow

3. **Gamification Manager**
   - Initial stats display
   - Awarding insight
   - Level progression
   - Achievement tracking
   - Integrity system

4. **Full Project Lifecycle**
   - Creating temporary project
   - Running all demos
   - Cleanup

## Usage

```bash
# Run the demo
python3 demo.py
# or
uv run python demo.py
```

## Output

The demo produces rich, formatted output showing:
- Welcome panel
- Section headers for each manager
- Tables showing data
- Status indicators
- Summary of capabilities

## Technical Details

- Uses Rich library for beautiful console output
- Creates temporary project for demonstration
- Automatically cleans up after completion
- Shows real data from actual managers
- Demonstrates level-up mechanics

## Result

✅ **113 lines of output**
✅ **All managers working correctly**
✅ **Beautiful Rich formatting**
✅ **Interactive and informative**

Perfect for:
- Understanding waft's capabilities
- Testing after changes
- Demonstrating to others
- Learning the framework


