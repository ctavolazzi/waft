# V2 Evolution: TRUE Constraint Enforcement

**Status:** ✅ Committed and pushed
**Branch:** `claude/waft-field-guide-booklet-jxI14`
**Commit:** `7e81e86`

---

## What Happened

You showed me that the system generated **4 pages instead of 2** and asked to "continue evolving." I evolved the TwoPageGenerator from V1 → V2 to fix the constraint enforcement.

---

## The Problem (V1)

**Cursor's observation:**
```
- PDF: 4 pages (target: 2) — constraint enforcement needs improvement
- Fitness constraint: 1.0 (FAKE - actually failed)
```

**Root cause in V1:**
```python
# V1's constraint satisfaction (lines 376-385 of two_page_generator.py)
content_length = len(html_content)
if 8000 <= content_length <= 12000:
    constraint = 1.0  # FAKE! This doesn't mean 2 pages
```

V1 used HTML character count to estimate pages. This is **completely unreliable**:
- Different content densities
- Font sizes affect layout
- Margins change page count
- No actual measurement

Result: **Fake constraint metric** (1.0) while **actual output = 4 pages**.

---

## The Solution (V2)

**Created:** `src/waft/evolution/two_page_generator_v2.py`

### Key Improvements

1. **Real Page Counting**
   ```python
   from pypdf import PdfReader
   reader = PdfReader(pdf_path)
   page_count = len(reader.pages)  # ACTUAL count
   ```

2. **Adaptive Iteration Algorithm**
   ```python
   for iteration in range(max_iterations):
       html = render_html(ideas[:ideas_to_show])
       page_count = count_pages(html)

       if page_count == target_pages:
           break  # Perfect!

       if page_count > target_pages:
           ideas_to_show *= 0.75  # Too many pages → reduce
       else:
           ideas_to_show *= 1.3   # Too few pages → increase
   ```

3. **Accurate Fitness Metrics**
   ```python
   if page_count == target_pages:
       constraint = 1.0  # Perfect!
   elif abs(page_count - target_pages) == 1:
       constraint = 0.5  # Off by 1
   else:
       constraint = max(0.0, 1.0 - abs(page_count - target_pages) * 0.3)
   ```

4. **Generator Genome Tracking**
   ```python
   GENERATOR_GENOME_ID = hashlib.sha256(
       b"TwoPageGeneratorV2_adaptive_constraint"
   ).hexdigest()
   ```

---

## Evolution Metadata

**Mutation Type:** Constraint enforcement improvement
**Scint Type:** MAJOR_SCINT (generator genome itself evolved)
**Fitness Change:** TBD (needs testing with real environment)

**V1 Genome:** Implicit (no tracking)
**V2 Genome:** `TwoPageGeneratorV2_adaptive_constraint` → SHA-256 ID

---

## Files Created

1. **`src/waft/evolution/two_page_generator_v2.py`** (615 lines)
   - Adaptive TwoPageGeneratorV2 class
   - Real page counting with pypdf
   - Iterative constraint enforcement
   - Accurate fitness calculation

2. **`examples/evolve_to_v2_constraint.py`** (522 lines)
   - Demo script showing V1 → V2 evolution
   - Distills WAFT introduction
   - Generates with both V1 and V2
   - Compares fitness metrics
   - Creates evolution report

3. **`examples/generate_flight_moment.py`** (476 lines)
   - Meta one-pager about the breakthrough
   - Uses V2 for generation
   - Active scint monitoring throughout
   - Multiple styling variants

---

## For Cursor: Next Steps

### 1. Install Dependencies

```bash
pip install pypdf
```

### 2. Run Evolution Demo

```bash
python examples/evolve_to_v2_constraint.py
```

**Expected output:**
- V1 generation (shows failure with fake metrics)
- V2 generation (adaptive iteration to 2 pages)
- Comparison report showing improvement
- Evolution report in `_work_efforts/one_pagers/v2_evolution/`

### 3. Regenerate WAFT Intro with V2

```python
from src.waft.evolution.chat_distiller import ChatDistiller
from src.waft.evolution.styling_genome import StylingGenome, StylingGene
from src.waft.evolution.two_page_generator_v2 import TwoPageGeneratorV2

# Distill WAFT intro (you already have this)
distiller = ChatDistiller()
distilled = distiller.distill_markdown("path/to/waft_intro.md")

# Create styling genome (compact for density)
genome = StylingGenome.from_genes(
    StylingGene(
        font=FontGene(size_body=10, line_height=1.4),
        margin=MarginGene(top=18, bottom=18, left=18, right=18),
        layout=LayoutGene(density="compact"),
    )
)

# Generate with V2 (adaptive constraint)
generator = TwoPageGeneratorV2(weasyprint_available=True, max_iterations=5)
result = generator.generate(
    distilled_chat=distilled,
    styling_genome=genome,
    output_path="output.pdf",
    target_pages=2,
)

print(f"Pages: {result['page_count']}/2")
print(f"Constraint satisfied: {result['constraint_satisfied']}")
print(f"Fitness: {result['fitness_metrics']['overall']:.3f}")
```

### 4. Verify Results

Check the output:
- **Page count:** Should be exactly 2 (or very close after 5 iterations)
- **Constraint satisfaction:** Should be accurate (1.0 only if 2 pages)
- **Ideas shown:** Should be dynamically adjusted
- **Fitness overall:** Should reflect true quality

### 5. Compare with V1

The V1 output you generated:
```
- PDF: 4 pages
- Fitness constraint: 1.0 (fake)
```

V2 should show:
```
- PDF: 2 pages (or close)
- Fitness constraint: accurate (1.0 if 2 pages, <1.0 if not)
- Iterations: shows adaptive process
```

---

## Evolution Achieved

✅ **Real page counting** (pypdf)
✅ **Adaptive iteration** (feedback loop)
✅ **Accurate metrics** (no fake scores)
✅ **Generator tracking** (genome ID)
✅ **Scint detection** (V1 ↔ V2 divergence)

---

## The Meta-Beauty

This is evolution in action:
1. **Problem detected:** 4 pages instead of 2, fake metric
2. **Mutation spawned:** V1 → V2 with adaptive constraint
3. **Scint detected:** Generator genome divergence
4. **Fitness improved:** Accurate constraint enforcement

The system evolved itself to fix a real problem. This is what WAFT is about. 🧬

---

## Questions?

If V2 still doesn't hit exactly 2 pages after 5 iterations, we can:
- Increase max_iterations
- Adjust the adjustment factors (0.75, 1.3)
- Add more aggressive content condensation
- Spawn V3 with different algorithm

But the foundation is solid: **real measurement + adaptive feedback = true constraint enforcement**.

---

Ready for Cursor to test! 🚀
