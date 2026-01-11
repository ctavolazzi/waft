#!/usr/bin/env python3
"""
Create One-Pager from Chat using V2 Evolution System
====================================================

Creates a 2-page one-pager PDF from the current chat session using the
evolved V2 system with TRUE constraint enforcement and genomic tracking.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution import (
    ChatDistiller,
    TwoPageGenerator,
    StylingGenome,
    StylingGenomeRegistry,
    StylingGene,
    FontGene,
    MarginGene,
    ColorGene,
    LayoutGene,
)


def get_chat_content() -> str:
    """
    Extract chat content from this session.
    
    This session focused on:
    - V2 evolution and integration
    - Formatting fixes
    - Checkpoint creation
    - Reflection
    """
    return """
# V2 Evolution: One-Pager System Evolution

## The Evolution

**Problem Identified**: V1 generated 4 pages but reported constraint satisfaction = 1.0 (false positive)
**Solution Evolved**: V2 with adaptive constraint enforcement using real page counting
**Result**: 2 pages generated accurately in 3 iterations

## Key Achievements

**V2 Integration**
- Made V2 the default implementation (TwoPageGenerator → TwoPageGeneratorV2)
- Kept V1 available for backward compatibility
- Updated all examples to use V2 API (target_pages=2)
- Added pypdf dependency for real page counting

**Formatting Fixes**
- Added _clean_markdown() method to strip markdown artifacts
- Removed headers (##), bold markers (**), redundant prefixes
- Improved text rendering CSS (word-wrap, overflow-wrap, hyphens)
- Ensured consistent, professional output

**Technical Improvements**
- Real page counting using pypdf.PdfReader
- Adaptive iteration algorithm (up to 5 attempts)
- Accurate fitness metrics based on actual page count
- Feedback loop: measure → adjust → measure

## The Meta-Evolution

The evolutionary framework evolved itself:
1. Failure detected (4 pages, fake metric)
2. Mutation spawned (V1 → V2)
3. Validation succeeded (2 pages, accurate metric)
4. Integration complete (V2 as default)

This is recursive improvement - the system improving itself through measured feedback.

## V2 Algorithm

```python
for iteration in range(5):
    html = render_html(ideas[:ideas_to_show])
    page_count = count_real_pages(html)  # Using pypdf!
    
    if page_count == 2:
        break  # Perfect!
    
    if page_count > 2:
        ideas_to_show *= 0.75  # Reduce
    else:
        ideas_to_show *= 1.3   # Increase
```

## Results

**V1 (Failed)**:
- Pages: 4 (target: 2)
- Constraint metric: 1.0 (fake)
- Method: HTML character count heuristic

**V2 (Success)**:
- Pages: 2 (target: 2) ✓
- Constraint metric: 1.0 (true)
- Method: Real page counting + adaptive iteration
- Iterations: 3
- Content: 28 ideas → 19 ideas (fitness-weighted selection)

## Formatting Improvements

**Issues Fixed**:
- Markdown artifacts removed (##, **, etc.)
- Redundant "Key Concept:" prefixes cleaned
- Text rendering improved (word-wrap, hyphens)
- Consistent presentation across all idea types

**Implementation**:
- _clean_markdown() strips all markdown before rendering
- Enhanced CSS for better text flow
- Professional, clean output

## Impact

- ✅ Accurate constraint enforcement (2 pages, not 4)
- ✅ Clean, professional output (no markdown artifacts)
- ✅ Better text rendering and readability
- ✅ System can evolve based on accurate fitness signals
- ✅ Backward compatibility maintained

## Next Steps

1. Test V2 in production
2. Monitor performance (iteration counts, convergence)
3. Explore other constraint types (1-page, 3-page, etc.)
4. Improve fitness functions (multi-objective optimization)

## Philosophy

> "Physical constellation of crystallized knowledge inside spacetime through the refraction of light"

This one-pager crystallizes the evolution of the one-pager system itself - meta-evolution in action.
"""


def main():
    """Create one-pager from chat session using V2 evolution system."""
    print("🔬 Creating one-pager from chat session using V2 evolution system...")
    print()
    
    # Get chat content
    chat_content = get_chat_content()
    
    # Distill chat into ideas
    print("📝 Distilling chat into ideas...")
    distiller = ChatDistiller()
    distilled = distiller.distill_text(chat_content, title="V2 Evolution: One-Pager System Evolution")
    
    print(f"✓ Extracted {distilled.total_ideas} ideas")
    print(f"  - Concepts: {distilled.concepts_count}")
    print(f"  - Actions: {distilled.actions_count}")
    print(f"  - Decisions: {distilled.decisions_count}")
    print(f"  - Insights: {distilled.insights_count}")
    print(f"  - Questions: {distilled.questions_count}")
    print()
    
    # Get or create styling genome
    print("🎨 Creating styling genome...")
    registry = StylingGenomeRegistry(registry_dir=Path("_genetics/chat_one_pagers"))
    
    # Create genesis genome if needed
    genesis_genes = StylingGene(
        font=FontGene(family="sans-serif", size_body=11),
        margin=MarginGene(top=20, bottom=20, left=20, right=20),
        color=ColorGene(text="#000000", background="#FFFFFF", accent="#0066cc"),
        layout=LayoutGene(columns=1, density="normal"),
        name="Chat One-Pager Genesis",
    )
    genome = StylingGenome.from_genes(genesis_genes)
    registry.register(genome)
    print(f"✓ Using: {genome.scientific_name} ({genome.genome_id[:8]}...)")
    print()
    
    # Generate with V2 (default)
    print("📄 Generating 2-page PDF with V2 (adaptive constraint enforcement)...")
    generator = TwoPageGenerator(weasyprint_available=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"_work_efforts/one_pagers/chat_session_{timestamp}.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    result = generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_path,
        target_pages=2,  # V2 API
    )
    
    print()
    print("=" * 60)
    print("✅ Chat One-Pager Created!")
    print("=" * 60)
    print(f"📄 Output: {output_path}")
    print(f"📊 Pages: {result['page_count']}/2")
    print(f"🎯 Constraint satisfied: {result['constraint_satisfied']}")
    print(f"💪 Fitness: {result['fitness_metrics']['overall']:.3f}")
    print(f"   - Readability: {result['fitness_metrics']['readability']:.3f}")
    print(f"   - Completeness: {result['fitness_metrics']['completeness']:.3f}")
    print(f"   - Constraint: {result['fitness_metrics']['constraint_satisfaction']:.3f}")
    print(f"   - Aesthetics: {result['fitness_metrics']['aesthetic_appeal']:.3f}")
    print(f"🧬 Ideas shown: {result['ideas_shown']}/{distilled.total_ideas}")
    print(f"🔬 Generator: {result['generator_version']}")
    print()
    
    if result['constraint_satisfied']:
        print("✅ Perfect 2-page document!")
    else:
        print(f"⚠️ Generated {result['page_count']} pages (expected 2)")
    
    print()
    print("Ready for printing and binder storage!")
    print()
    
    # Open the PDF
    import subprocess
    subprocess.run(["open", "-a", "Preview", str(output_path)])
    
    print(f"📖 PDF opened in Preview")


if __name__ == "__main__":
    main()
