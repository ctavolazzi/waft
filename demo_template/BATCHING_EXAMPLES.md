# Batching Examples

## Basic Batching

```bash
# Generate 10 permutations (default for --batch)
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch
```

**Output**:
- `demo_overview_batched.pdf` - All 10 permutations collated
- `demo_overview.html` - Opens PDF automatically
- Browser opens with HTML page
- PDF opens in new tab automatically

---

## Custom Permutations

```bash
# Generate 20 permutations
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --permutations 20
```

**Output**: 20 permutations in collated PDF

---

## With Page Limit

```bash
# Limit to 50 pages max
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --permutations 10 --max-pages 50
```

**Calculation**: 50 pages / 2 pages per permutation = 25 max iterations
**Result**: All 10 permutations included (under limit)

---

## With File Size Limit

```bash
# Limit to 5 MB max
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --permutations 10 --max-file-size-mb 5.0
```

**Calculation**: 5 MB * 20 pages/MB / 2 pages per permutation = 50 max iterations
**Result**: All 10 permutations included (under limit)

---

## Combined Limits

```bash
# Both page and file size limits
python3 scripts/seed_reincarnation_demo.py \
  --demo-path my_demo \
  --batch \
  --permutations 20 \
  --max-pages 30 \
  --max-file-size-mb 5.0
```

**Calculation**:
- By pages: 30 / 2 = 15 max iterations
- By size: 5.0 * 20 / 2 = 50 max iterations
- **Most restrictive**: 15 iterations

**Result**: Only 15 permutations included (limited by page count)

---

## Large-Scale Batching

```bash
# Generate 50 permutations for analysis
python3 scripts/seed_reincarnation_demo.py \
  --demo-path demo_analysis \
  --batch \
  --permutations 50 \
  --max-pages 100 \
  --max-file-size-mb 10.0
```

**Result**: Up to 50 permutations (limited by constraints)

---

## Quick Testing

```bash
# Quick test with 3 permutations
python3 scripts/seed_reincarnation_demo.py \
  --demo-path demo_quick \
  --batch \
  --permutations 3 \
  --max-pages 10
```

**Result**: 3 permutations, PDF limited to 10 pages

---

## What Each Permutation Contains

### Permutation 0 (Base)
- `soul_demo_001`: 1000.0 karma
- `soul_demo_002`: 500.0 karma
- `soul_demo_003`: 2000.0 karma
- `soul_demo_004`: 0.0 karma
- `soul_demo_005`: 150.0 karma

### Permutation 1+
- `soul_demo_001_perm01`: ~800-1200 karma (±20% variation)
- `soul_demo_002_perm01`: ~400-600 karma (±20% variation)
- etc.

**All permutations use the same lifetime catalog.**

---

## Output Files

### Batched Mode
- `demo_overview_batched.pdf` - Collated PDF
- `demo_overview.html` - HTML page

### Single Mode
- `demo_overview.pdf` - Single PDF
- `demo_overview.html` - HTML page

---

## PDF Statistics

The batched PDF includes:
- Total Permutations
- Total Souls Created
- Average Karma per Soul
- Lifetimes Available

---

**Happy Batching!** 📦📄
