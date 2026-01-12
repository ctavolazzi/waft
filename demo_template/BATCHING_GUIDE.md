# Batching Guide - Multiple Permutations

**Purpose**: Generate multiple demo permutations and collate them into a single PDF

---

## Quick Start

### Basic Batching (10 Permutations)

```bash
# Generate 10 permutations, collated into one PDF
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch
```

### Custom Permutations

```bash
# Generate 20 permutations
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --permutations 20
```

### With Page Limit

```bash
# Limit PDF to 50 pages max
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --permutations 10 --max-pages 50
```

### With File Size Limit

```bash
# Limit PDF to 5 MB max
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --permutations 10 --max-file-size-mb 5.0
```

### Combined Limits

```bash
# Both page and file size limits
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch --permutations 10 --max-pages 50 --max-file-size-mb 5.0
```

---

## How It Works

### Permutation Generation

Each permutation creates:
- **5 Test Souls** with varying karma amounts (±20% variation)
- **Unique Soul IDs**: `soul_demo_001_perm01`, `soul_demo_001_perm02`, etc.
- **Same Lifetime Catalog**: All permutations use the same catalog

### Collation

All permutations are collected and collated into:
- **Single PDF**: `demo_overview_batched.pdf`
- **HTML Page**: `demo_overview.html` (opens PDF automatically)
- **Statistics**: Total permutations, total souls, average karma

---

## Max Iterations Calculation

The system automatically calculates maximum iterations based on:

### Page Limit

```python
max_iterations = max_pages / estimated_pages_per_permutation
# Example: 50 pages / 2 pages per permutation = 25 max iterations
```

### File Size Limit

```python
# Estimate: ~20 pages per MB
max_pages_by_size = max_file_size_mb * 20
max_iterations = max_pages_by_size / estimated_pages_per_permutation
# Example: 5 MB * 20 pages/MB / 2 pages per permutation = 50 max iterations
```

### Combined Limit

Takes the **most restrictive** limit:
```python
max_iterations = min(iterations_by_pages, iterations_by_size)
```

---

## Use Cases

### Testing Multiple Configurations

```bash
# Test 10 different karma distributions
python3 scripts/seed_reincarnation_demo.py --demo-path demo_karma_test --batch --permutations 10
```

### Large-Scale Analysis

```bash
# Generate 50 permutations for analysis
python3 scripts/seed_reincarnation_demo.py --demo-path demo_analysis --batch --permutations 50 --max-pages 100
```

### Size-Constrained Reports

```bash
# Keep PDF under 10 MB
python3 scripts/seed_reincarnation_demo.py --demo-path demo_report --batch --permutations 20 --max-file-size-mb 10.0
```

---

## Output Files

### Batched Mode

- `demo_overview_batched.pdf` - Collated PDF with all permutations
- `demo_overview.html` - HTML page (opens batched PDF)

### Single Mode

- `demo_overview.pdf` - Single demo PDF
- `demo_overview.html` - HTML page (opens single PDF)

---

## PDF Content Structure

### Batched PDF Includes

1. **Title**: "Reincarnation System Demo Overview - N Permutations"
2. **Overview**: Demo environment explanation
3. **State Capabilities**: Alive vs Dead capabilities
4. **Permutation 1**: All souls and catalog
5. **Permutation 2**: All souls and catalog
6. **...** (all permutations)
7. **Usage Examples**: Python code snippets
8. **Batch Statistics**: Total permutations, total souls, average karma

---

## Parameters

### `--permutations N`

Number of permutations to generate (default: 1)

- **Single mode**: 1 permutation (original behavior)
- **Batch mode**: 10 permutations (default when `--batch` used)
- **Custom**: Any number (e.g., `--permutations 20`)

### `--max-pages N`

Maximum number of pages in PDF (default: no limit)

- Calculates max iterations: `max_pages / 2` (assuming 2 pages per permutation)
- Stops generating permutations if limit would be exceeded
- Example: `--max-pages 50` allows ~25 permutations

### `--max-file-size-mb N`

Maximum PDF file size in MB (default: no limit)

- Estimates: ~20 pages per MB
- Calculates max iterations based on file size
- Example: `--max-file-size-mb 5.0` allows ~50 permutations (5 MB * 20 pages/MB / 2 pages per perm)

### `--batch`

Enable batching mode

- Sets `--permutations` to 10 if not specified
- Generates collated PDF instead of single PDF
- Creates `demo_overview_batched.pdf`

---

## Examples

### Example 1: Standard Batch

```bash
python3 scripts/seed_reincarnation_demo.py --demo-path demo_batch --batch
```

**Result**: 10 permutations, collated PDF, no limits

### Example 2: Large Batch with Limits

```bash
python3 scripts/seed_reincarnation_demo.py \
  --demo-path demo_large \
  --batch \
  --permutations 50 \
  --max-pages 100 \
  --max-file-size-mb 10.0
```

**Result**: Up to 50 permutations (limited by constraints), collated PDF

### Example 3: Small Batch for Quick Testing

```bash
python3 scripts/seed_reincarnation_demo.py \
  --demo-path demo_quick \
  --batch \
  --permutations 3 \
  --max-pages 10
```

**Result**: 3 permutations, PDF limited to 10 pages

---

## Statistics

The batched PDF includes statistics:

- **Total Permutations**: Number of permutations generated
- **Total Souls Created**: Sum of all souls across permutations
- **Average Karma per Soul**: Average karma across all souls
- **Lifetimes Available**: Number of lifetimes in catalog

---

## Best Practices

1. **Start Small**: Test with 3-5 permutations first
2. **Set Limits**: Use `--max-pages` or `--max-file-size-mb` to prevent huge PDFs
3. **Monitor Size**: Check file size output to adjust limits
4. **Use Cases**: 
   - Testing: 5-10 permutations
   - Analysis: 20-50 permutations
   - Reports: 10-20 permutations with size limits

---

**Batching Complete!** Generate multiple permutations and collate them into a single PDF. 📦📄
