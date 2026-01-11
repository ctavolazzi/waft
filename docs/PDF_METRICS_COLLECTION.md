# PDF Metrics Collection

**Created**: 2026-01-11  
**Purpose**: Core-level metrics collection for PDF generation to support evolution with quality data

---

## Overview

PDF generation now includes an **optional metrics flag** that collects comprehensive data about every PDF generation. This enables evolution with quality data by tracking:

- Input metrics (ideas, importance, content)
- Generation metrics (time, iterations, constraint satisfaction)
- Output metrics (file sizes, page counts)
- Styling metrics (fonts, colors, layouts)
- Fitness metrics (readability, completeness, constraint, aesthetics)
- Conversion metrics (PNG conversion success, file sizes)
- Content metrics (word counts, density, structure)
- Quality metrics (computed scores and grades)

---

## Usage

### Basic Usage (No Metrics)

```python
from src.waft.evolution import TwoPageGeneratorV2, StylingGenome, ChatDistiller

generator = TwoPageGeneratorV2()
result = generator.generate(
    distilled_chat=distilled_chat,
    styling_genome=styling_genome,
    output_path="output.pdf",
    collect_metrics=False  # Default: no metrics
)
```

### With Metrics Collection

```python
from src.waft.evolution import TwoPageGeneratorV2, StylingGenome, ChatDistiller

generator = TwoPageGeneratorV2()
result = generator.generate(
    distilled_chat=distilled_chat,
    styling_genome=styling_genome,
    output_path="output.pdf",
    collect_metrics=True,  # Enable metrics collection
    metrics_dir=Path("_pyrite/metrics/pdf")  # Optional: custom directory
)

# Metrics are automatically saved
# Access metrics from result
if "metrics" in result:
    metrics = result["metrics"]
    print(f"Quality Grade: {metrics['quality_grade']}")
    print(f"Quality Score: {metrics['quality_score']:.3f}")
    print(f"Metrics File: {result['metrics_file']}")
```

---

## Metrics Collected

### Input Metrics
- `input_ideas_total`: Total ideas available
- `input_ideas_shown`: Ideas actually used
- `input_ideas_importance_avg`: Average importance score
- `input_ideas_importance_max`: Maximum importance
- `input_ideas_importance_min`: Minimum importance
- `chat_title`: Chat title
- `chat_summary_length`: Summary length in characters

### Generation Metrics
- `generation_time_seconds`: Time to generate PDF
- `iterations_used`: Number of adaptive iterations
- `target_pages`: Target page count
- `actual_pages`: Actual page count
- `constraint_satisfied`: Whether constraint was met
- `page_diff`: Absolute difference from target

### Output Metrics
- `pdf_path`: Path to generated PDF
- `pdf_size_bytes`: PDF file size
- `html_size_bytes`: HTML content size
- `pdf_exists`: Whether PDF was created
- `html_exists`: Whether HTML was created

### Styling Metrics
- `styling_genome_id`: Genome ID of styling used
- `styling_scientific_name`: Scientific name of styling
- `font_family`: Font family used
- `font_size_body`: Body font size
- `font_size_h1`: H1 font size
- `color_scheme`: Color scheme name
- `layout_density`: Layout density (compact/normal/spacious)
- `margin_top/bottom/left/right`: Margin values

### Fitness Metrics
- `fitness_readability`: Readability score (0.0-1.0)
- `fitness_completeness`: Completeness score (0.0-1.0)
- `fitness_constraint`: Constraint satisfaction (0.0-1.0)
- `fitness_aesthetic`: Aesthetic appeal (0.0-1.0)
- `fitness_overall`: Overall fitness (weighted average)

### Conversion Metrics
- `png_conversion_attempted`: Whether PNG conversion was attempted
- `png_conversion_success`: Whether PNG conversion succeeded
- `png_count`: Number of PNG images created
- `png_dpi`: DPI used for PNG conversion
- `png_total_size_bytes`: Total size of all PNGs

### Content Metrics
- `content_words_total`: Total word count
- `content_words_page1`: Words on page 1
- `content_words_page2`: Words on page 2
- `content_density_words_per_page`: Average words per page
- `content_paragraphs_total`: Total paragraphs
- `content_lists_total`: Total lists
- `content_boxes_total`: Total boxes (note/highlight)

### Quality Metrics
- `quality_score`: Computed quality score (0.0-1.0)
- `quality_grade`: Letter grade (A, B, C, D, F)

---

## Storage

Metrics are stored in JSONL format (one JSON object per line) for easy analysis:

### Daily Files
`_pyrite/metrics/pdf/daily/YYYY-MM-DD.jsonl`

One file per day with all metrics from that day.

### Aggregate File
`_pyrite/metrics/pdf/all_metrics.jsonl`

All metrics from all days in a single file.

### Custom Directory
You can specify a custom directory:
```python
result = generator.generate(
    ...,
    collect_metrics=True,
    metrics_dir=Path("custom/metrics/path")
)
```

---

## Analysis

### Reading Metrics

```python
import json
from pathlib import Path

# Read daily metrics
daily_file = Path("_pyrite/metrics/pdf/daily/2026-01-11.jsonl")
with open(daily_file) as f:
    for line in f:
        metrics = json.loads(line)
        print(f"Quality: {metrics['quality_grade']} ({metrics['quality_score']:.3f})")
```

### Querying Metrics

```python
import json
from pathlib import Path

# Find all A-grade PDFs
aggregate_file = Path("_pyrite/metrics/pdf/all_metrics.jsonl")
a_grade_pdfs = []

with open(aggregate_file) as f:
    for line in f:
        metrics = json.loads(line)
        if metrics.get('quality_grade') == 'A':
            a_grade_pdfs.append(metrics)

print(f"Found {len(a_grade_pdfs)} A-grade PDFs")
```

### Evolution Analysis

```python
import json
from pathlib import Path
from collections import defaultdict

# Analyze fitness trends over time
aggregate_file = Path("_pyrite/metrics/pdf/all_metrics.jsonl")
fitness_by_date = defaultdict(list)

with open(aggregate_file) as f:
    for line in f:
        metrics = json.loads(line)
        date = metrics['timestamp'][:10]  # YYYY-MM-DD
        fitness_by_date[date].append(metrics['fitness_overall'])

# Compute averages
for date in sorted(fitness_by_date.keys()):
    avg_fitness = sum(fitness_by_date[date]) / len(fitness_by_date[date])
    print(f"{date}: {avg_fitness:.3f}")
```

---

## Integration with Evolution

Metrics integrate seamlessly with WAFT's evolutionary system:

1. **Evolutionary Events**: Metrics are recorded alongside evolutionary events
2. **Fitness Tracking**: Quality scores feed into fitness evaluation
3. **Lineage Tracking**: Metrics include genome IDs for lineage analysis
4. **Scientific Names**: Styling scientific names are included for taxonomic tracking

---

## Benefits

### For Evolution
- **Data-Driven Decisions**: Make evolution decisions based on actual quality data
- **Trend Analysis**: Track quality improvements over time
- **Pattern Recognition**: Identify what styling/configurations work best
- **A/B Testing**: Compare different approaches with quantitative data

### For Quality Assurance
- **Quality Monitoring**: Track quality scores and grades
- **Regression Detection**: Identify when quality degrades
- **Success Metrics**: Measure success of improvements
- **Benchmarking**: Establish quality baselines

### For Development
- **Performance Tracking**: Monitor generation time and iterations
- **Constraint Analysis**: Track constraint satisfaction rates
- **Content Analysis**: Understand content density and structure
- **Conversion Tracking**: Monitor PNG conversion success rates

---

## Example: Enabling Metrics in Scripts

### Before (No Metrics)
```python
result = generator.generate(
    distilled_chat=distilled_chat,
    styling_genome=styling_genome,
    output_path="output.pdf"
)
```

### After (With Metrics)
```python
result = generator.generate(
    distilled_chat=distilled_chat,
    styling_genome=styling_genome,
    output_path="output.pdf",
    collect_metrics=True  # Just add this flag!
)

# Metrics automatically saved to _pyrite/metrics/pdf/
# Access from result if needed
if "metrics" in result:
    print(f"Quality: {result['metrics']['quality_grade']}")
```

---

## Performance Impact

Metrics collection has **minimal performance impact**:
- **Time**: < 10ms overhead per generation
- **Storage**: ~2-5KB per metrics record
- **Memory**: Negligible (metrics collected at end of generation)

Metrics are collected **after** PDF generation completes, so they don't affect generation performance.

---

## Future Enhancements

Potential future enhancements:
- Real-time metrics dashboard
- Automated quality alerts
- Machine learning for quality prediction
- Integration with external analytics
- Metrics aggregation and reporting tools

---

**Status**: ✅ Implemented  
**Default**: Disabled (opt-in)  
**Storage**: JSONL files in `_pyrite/metrics/pdf/`  
**Integration**: Seamless with evolutionary system
