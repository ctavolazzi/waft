# Demo Batching System - Complete ✅

**Date**: 2026-01-11 16:35:00 PST
**Status**: ✅ Batching with Max Iterations Complete

---

## What Was Added

### Batching System

The demo seeding script now supports generating multiple permutations and collating them into a single PDF.

**New Features**:
1. **Multiple Permutations**: Generate N variations of the demo
2. **Collated PDF**: All permutations in one PDF
3. **Max Iterations**: Calculated from page count and file size limits
4. **Automatic Limits**: Stops when constraints are met

---

## New Command-Line Options

### `--batch`

Enable batching mode (defaults to 10 permutations if not specified)

```bash
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch
```

### `--permutations N`

Number of permutations to generate (default: 1, or 10 if `--batch` used)

```bash
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --permutations 20
```

### `--max-pages N`

Maximum number of pages in PDF (default: no limit)

```bash
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --max-pages 50
```

### `--max-file-size-mb N`

Maximum PDF file size in MB (default: no limit)

```bash
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --max-file-size-mb 5.0
```

---

## Max Iterations Calculation

### Formula

```python
def calculate_max_iterations(max_pages, max_file_size_mb, estimated_pages_per_permutation=2.0):
    iterations_by_pages = max_pages / estimated_pages_per_permutation if max_pages else None
    iterations_by_size = (max_file_size_mb * 20) / estimated_pages_per_permutation if max_file_size_mb else None
    
    if iterations_by_pages is None and iterations_by_size is None:
        return None  # No limit
    elif iterations_by_pages is None:
        return iterations_by_size
    elif iterations_by_size is None:
        return iterations_by_pages
    else:
        return min(iterations_by_pages, iterations_by_size)  # Most restrictive
```

### Examples

- **Max Pages: 50** → Max iterations: 25 (50 / 2 pages per perm)
- **Max Size: 5 MB** → Max iterations: 50 (5 MB * 20 pages/MB / 2 pages per perm)
- **Both: 50 pages, 5 MB** → Max iterations: 25 (most restrictive)

---

## Permutation Variations

Each permutation (after the first) has:
- **Varied Karma**: ±20% variation from base values
- **Unique IDs**: `soul_demo_001_perm01`, `soul_demo_001_perm02`, etc.
- **Same Catalog**: All permutations use the same lifetime catalog

### Base Souls (Permutation 0)

- `soul_demo_001`: 1000.0 karma
- `soul_demo_002`: 500.0 karma
- `soul_demo_003`: 2000.0 karma
- `soul_demo_004`: 0.0 karma
- `soul_demo_005`: 150.0 karma

### Permutation Variations

- `soul_demo_001_perm01`: ~800-1200 karma (±20%)
- `soul_demo_002_perm01`: ~400-600 karma (±20%)
- etc.

---

## Output Files

### Batched Mode

- `demo_overview_batched.pdf` - Collated PDF with all permutations
- `demo_overview.html` - HTML page (opens batched PDF automatically)

### Single Mode

- `demo_overview.pdf` - Single demo PDF
- `demo_overview.html` - HTML page (opens single PDF automatically)

---

## PDF Content Structure

### Batched PDF Sections

1. **Title**: "Reincarnation System Demo Overview - N Permutations"
2. **Overview**: Demo environment explanation
3. **State Capabilities**: Alive vs Dead capabilities
4. **Permutation 1**: All souls and catalog
5. **Permutation 2**: All souls and catalog
6. **...** (all permutations)
7. **Usage Examples**: Python code snippets
8. **Batch Statistics**: 
   - Total Permutations
   - Total Souls Created
   - Average Karma per Soul
   - Lifetimes Available

---

## Usage Examples

### Standard Batch (10 Permutations)

```bash
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch
```

**Result**: 10 permutations, collated PDF, HTML opens automatically

### Custom Permutations with Limits

```bash
python3 scripts/seed_reincarnation_demo.py \
  --demo-path my_demo \
  --batch \
  --permutations 20 \
  --max-pages 50 \
  --max-file-size-mb 5.0
```

**Result**: Up to 20 permutations (limited by constraints), collated PDF

### Quick Test (3 Permutations)

```bash
python3 scripts/seed_reincarnation_demo.py \
  --demo-path my_demo \
  --batch \
  --permutations 3 \
  --max-pages 10
```

**Result**: 3 permutations, PDF limited to 10 pages

---

## Implementation Details

### Functions Added

1. **`generate_permutation_content()`**: Creates markdown for single permutation
2. **`generate_batched_demo_pdf()`**: Generates collated PDF with all permutations
3. **`calculate_max_iterations()`**: Calculates max iterations from limits
4. **`create_test_souls(permutation=N)`**: Creates souls with variations

### Modified Functions

1. **`create_test_souls()`**: Now accepts `permutation` parameter for variations
2. **`main()`**: Added batching logic and new command-line arguments

---

## Testing

✅ **Batching**: Verified working (10 permutations generated)
✅ **Max Pages**: Verified working (limits iterations correctly)
✅ **Max File Size**: Verified working (calculates from size)
✅ **Collation**: Verified working (all permutations in one PDF)
✅ **HTML**: Verified working (opens batched PDF)
✅ **Auto-Open**: Verified working (browser opens automatically)

---

## Status

✅ **Batching System**: Complete
✅ **Max Iterations**: Implemented
✅ **Page Limits**: Working
✅ **File Size Limits**: Working
✅ **Collation**: Working
✅ **Documentation**: Complete

---

**Demo Batching Complete!** Generate multiple permutations and collate them into a single PDF with automatic limits. 📦📄
