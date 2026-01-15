---
name: Storyteller Prototyping Plan
overview: Prototyping plan to test unverified assumptions before full implementation. Tests Tracery complex grammar capabilities, PDFGenerator performance at scale, and defines "medium complexity" with concrete examples.
todos:
  - id: prototype_tracery_multi_paragraph
    content: Create test_tracery_complex_narrative.py with multi-paragraph, dialogue, and character arc grammars. Test generation of 50+ paragraphs.
    status: pending
  - id: prototype_pdfgenerator_scale
    content: Create test_pdfgenerator_scale.py to test PDFGenerator with 10/20/50/100 pages. Measure generation time, memory usage, file size.
    status: pending
  - id: define_medium_complexity
    content: Create define_medium_complexity.py with concrete examples (simple, medium target, realistic). Document quality criteria.
    status: pending
  - id: test_character_extraction
    content: Create test_character_extraction.py with simple regex-based extraction. Test accuracy on sample texts.
    status: pending
  - id: compile_prototype_results
    content: Document all prototype results, make go/no-go decisions, update implementation plan based on findings
    status: pending

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Storyteller Prototyping Plan

## Purpose

Test unverified assumptions before committing to implementation approach. Prototypes will validate:

1. Tracery can generate medium complexity narratives
2. PDFGenerator performs well at 50+ pages
3. "Medium complexity" is achievable with templates

## Prototype 1: Tracery Complex Grammar

### Goal

Test if Tracery can generate multi-paragraph narratives with characters, dialogue, and basic arcs.

### Implementation

**File**: `examples/test_tracery_complex_narrative.py`

```python
"""
Test Tracery complex grammar for book-length narratives.
"""

import tracery
from tracery.modifiers import base_english

# Test Grammar 1: Multi-paragraph narrative
MULTI_PARAGRAPH_GRAMMAR = {
    "origin": [
        "#opening#\n\n#middle#\n\n#closing#",
        "#scene#\n\n#scene#\n\n#scene#"
    ],
    "opening": [
        "In the beginning, #character# #action#. #description#.",
        "The story begins when #character# #action#. #setting# was #mood#."
    ],
    "middle": [
        "#character# continued to #action#. #consequence#.",
        "As time passed, #character# #action#. This led to #outcome#."
    ],
    "closing": [
        "In the end, #character# #resolution#. #moral#.",
        "Finally, #character# #resolution#. The journey was complete."
    ],
    "scene": [
        "#character# stood in #setting#. '#dialogue#', they said.",
        "#character# walked through #setting#. '#dialogue#', they thought."
    ],
    "character": ["Alice", "Bob", "Charlie"],
    "action": ["worked", "struggled", "succeeded", "failed"],
    "description": ["It was a challenging task", "The work was difficult"],
    "setting": ["the office", "the lab", "the workshop"],
    "mood": ["quiet", "busy", "tense"],
    "consequence": ["success", "failure", "a new challenge"],
    "outcome": ["victory", "defeat", "a lesson learned"],
    "resolution": ["succeeded", "failed", "learned"],
    "moral": ["Hard work pays off", "Failure teaches lessons"],
    "dialogue": ["I must continue", "This is difficult", "I can do this"]
}

# Test Grammar 2: Character dialogue
DIALOGUE_GRAMMAR = {
    "origin": [
        "#character# said, '#dialogue#'. #response#",
        "'#dialogue#', said #character#. #other_character# replied, '#response_dialogue#'"
    ],
    "character": ["Alice", "Bob"],
    "other_character": ["Bob", "Alice"],
    "dialogue": ["Hello", "How are you?", "Let's work together"],
    "response": ["They nodded", "They agreed", "They disagreed"],
    "response_dialogue": ["Hello", "I'm fine", "Yes, let's"]
}

# Test Grammar 3: Stateful narrative (character arc)
ARC_GRAMMAR = {
    "origin": [
        "#beginning_state#\n\n#middle_state#\n\n#end_state#"
    ],
    "beginning_state": [
        "#character# was #beginning_trait#. They #beginning_action#."
    ],
    "middle_state": [
        "Over time, #character# became #middle_trait#. They #middle_action#."
    ],
    "end_state": [
        "In the end, #character# was #end_trait#. They had #end_action#."
    ],
    "character": ["Alice"],
    "beginning_trait": ["inexperienced", "uncertain", "new"],
    "beginning_action": ["struggled", "learned", "made mistakes"],
    "middle_trait": ["more confident", "growing", "improving"],
    "middle_action": ["practiced", "improved", "gained skills"],
    "end_trait": ["experienced", "confident", "skilled"],
    "end_action": ["succeeded", "mastered", "achieved"]
}

def test_multi_paragraph():
    """Test multi-paragraph generation."""
    grammar = tracery.Grammar(MULTI_PARAGRAPH_GRAMMAR)
    grammar.add_modifiers(base_english)

    result = grammar.flatten("#origin#")
    print("Multi-paragraph test:")
    print(result)
    print(f"Length: {len(result)} characters")
    print(f"Paragraphs: {result.count('\\n\\n')}")
    return result

def test_dialogue():
    """Test dialogue generation."""
    grammar = tracery.Grammar(DIALOGUE_GRAMMAR)
    grammar.add_modifiers(base_english)

    result = grammar.flatten("#origin#")
    print("\nDialogue test:")
    print(result)
    return result

def test_character_arc():
    """Test character arc generation."""
    grammar = tracery.Grammar(ARC_GRAMMAR)
    grammar.add_modifiers(base_english)

    result = grammar.flatten("#origin#")
    print("\nCharacter arc test:")
    print(result)
    return result

def test_book_length():
    """Test generating 50+ paragraphs for book-length content."""
    grammar = tracery.Grammar(MULTI_PARAGRAPH_GRAMMAR)
    grammar.add_modifiers(base_english)

    paragraphs = []
    for i in range(50):
        para = grammar.flatten("#origin#")
        paragraphs.append(para)

    full_text = "\n\n".join(paragraphs)
    print(f"\nBook-length test:")
    print(f"Total length: {len(full_text)} characters")
    print(f"Paragraphs: {len(paragraphs)}")
    print(f"Estimated pages: ~{len(full_text) // 2000} pages")

    return full_text

if __name__ == "__main__":
    test_multi_paragraph()
    test_dialogue()
    test_character_arc()
    test_book_length()
```

### Success Criteria

- ✅ Can generate multi-paragraph narratives
- ✅ Can generate character dialogue
- ✅ Can generate character arcs (stateful)
- ✅ Can generate 50+ paragraphs (book-length)
- ✅ Output is coherent and readable

### Failure Handling

- If Tracery insufficient: Document limitations, consider LLM hybrid approach
- If performance poor: Optimize grammar, add caching
- If quality low: Refine grammar rules, add more templates

---

## Prototype 2: PDFGenerator Performance at Scale

### Goal

Test PDFGenerator with 50+ page content to verify performance and algorithm behavior.

### Implementation

**File**: `examples/test_pdfgenerator_scale.py`

```python
"""
Test PDFGenerator performance with large content.
"""

from pathlib import Path
import time
from src.waft.evolution.pdf_generator import PDFGenerator

def generate_large_content(num_pages: int = 50) -> str:
    """Generate content that should produce N pages."""
    # Estimate: ~2000 characters per page
    chars_per_page = 2000
    total_chars = num_pages * chars_per_page

    # Generate markdown content
    content = "# Test Document\n\n"

    for i in range(num_pages):
        content += f"## Chapter {i+1}\n\n"
        # Add paragraphs to fill page
        paragraphs_per_page = 10
        for j in range(paragraphs_per_page):
            para_length = chars_per_page // paragraphs_per_page
            content += f"This is paragraph {j+1} of chapter {i+1}. " * (para_length // 50)
            content += "\n\n"

    return content

def test_pdfgenerator_scale():
    """Test PDFGenerator with various page counts."""
    test_cases = [10, 20, 50, 100]

    results = []

    for target_pages in test_cases:
        print(f"\nTesting {target_pages} pages...")

        # Generate content
        content = generate_large_content(target_pages)

        # Time generation
        start_time = time.time()

        generator = PDFGenerator.from_content(
            content=content,
            title=f"Test Document ({target_pages} pages)",
            style="premium"
        )

        output_path = Path(f"_temp/test_{target_pages}pages.pdf")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        pdf_path = generator.save(
            output_path=output_path,
            target_pages=None,  # No limit
            open_pdf=False
        )

        end_time = time.time()
        generation_time = end_time - start_time

        # Count actual pages
        from pypdf import PdfReader
        reader = PdfReader(str(pdf_path))
        actual_pages = len(reader.pages)

        # Get file size
        file_size_mb = pdf_path.stat().st_size / (1024 * 1024)

        result = {
            "target_pages": target_pages,
            "actual_pages": actual_pages,
            "generation_time": generation_time,
            "file_size_mb": file_size_mb,
            "time_per_page": generation_time / actual_pages if actual_pages > 0 else 0
        }

        results.append(result)

        print(f"  Actual pages: {actual_pages}")
        print(f"  Generation time: {generation_time:.2f}s")
        print(f"  File size: {file_size_mb:.2f} MB")
        print(f"  Time per page: {result['time_per_page']:.2f}s")

    # Summary
    print("\n" + "="*60)
    print("Performance Summary:")
    print("="*60)
    for r in results:
        print(f"{r['target_pages']:3d} pages: {r['generation_time']:6.2f}s, "
              f"{r['file_size_mb']:5.2f}MB, {r['time_per_page']:.3f}s/page")

    return results

if __name__ == "__main__":
    test_pdfgenerator_scale()
```

### Success Criteria

- ✅ Can generate 50+ page PDFs
- ✅ Generation time < 30 seconds for 50 pages
- ✅ Memory usage reasonable (< 500MB)
- ✅ File size reasonable (< 10MB for 50 pages)
- ✅ No crashes or errors

### Failure Handling

- If too slow: Optimize algorithm, add caching
- If memory issues: Stream content, process in chunks
- If crashes: Fix bugs, add error handling

---

## Prototype 3: Define "Medium Complexity"

### Goal

Create concrete examples of "medium complexity" narrative output to set expectations.

### Implementation

**File**: `examples/define_medium_complexity.py`

```python
"""
Define "medium complexity" narrative with concrete examples.
"""

# Example 1: Simple (baseline)
SIMPLE_EXAMPLE = """
# The Developer's Journey

Alice started working on the project. She encountered a bug. She fixed it. The project was complete.
"""

# Example 2: Medium Complexity (target)
MEDIUM_EXAMPLE = """
# The Developer's Journey

## Chapter 1: The Beginning

Alice sat at her desk, staring at the blank screen. The project deadline loomed ahead, and she felt the weight of expectation. "I can do this," she whispered to herself, fingers hovering over the keyboard.

The codebase sprawled before her like an ancient city, full of mysteries and hidden paths. She began to explore, methodically tracing function calls and data flows. Each discovery felt like uncovering a secret.

## Chapter 2: The Challenge

Three days in, Alice encountered the bug. It was subtle—a race condition that only appeared under specific load conditions. She spent hours debugging, adding print statements, tracing execution paths.

"Alice, how's it going?" Bob asked, peering over her shoulder.

"I'm stuck," she admitted. "This bug doesn't make sense."

Bob nodded sympathetically. "Sometimes you need to step back. Want to pair on it?"

Together, they worked through the problem. Bob's fresh perspective helped Alice see what she'd missed. The solution emerged slowly, like a puzzle coming together.

## Chapter 3: Resolution

With the bug fixed, Alice felt a surge of confidence. She had not only solved the problem but learned something new about concurrent programming. The project was complete, but more importantly, she had grown.

As she pushed the final commit, Alice reflected on the journey. The struggle had been real, but so had the growth. She was no longer the uncertain developer who had started this project—she was someone who could tackle difficult problems and emerge stronger.
"""

# Example 3: What We Can Generate (realistic)
REALISTIC_EXAMPLE = """
# The Developer's Journey

## Beginning

In the office, Alice started working on the project. The task was challenging. She began to code.

## Middle

Alice encountered a bug. She struggled with the problem. Bob helped her debug. Together they found the solution.

## End

Alice fixed the bug. The project was complete. She had learned and grown.
"""

def compare_examples():
    """Compare examples to define target."""
    print("="*60)
    print("COMPLEXITY COMPARISON")
    print("="*60)

    examples = [
        ("Simple", SIMPLE_EXAMPLE),
        ("Medium (Target)", MEDIUM_EXAMPLE),
        ("Realistic (What we can generate)", REALISTIC_EXAMPLE)
    ]

    for name, example in examples:
        print(f"\n{name}:")
        print(f"  Length: {len(example)} characters")
        print(f"  Paragraphs: {example.count('\\n\\n')}")
        print(f"  Characters: {len([c for c in example if c.isupper() and c.isalpha()])} proper nouns")
        print(f"  Dialogue: {'Yes' if '\"' in example else 'No'}")
        print(f"  Structure: {'Yes' if 'Chapter' in example else 'No'}")
        print(f"  Character arc: {'Yes' if 'growth' in example.lower() or 'learned' in example.lower() else 'No'}")

if __name__ == "__main__":
    compare_examples()
```

### Success Criteria

- ✅ Clear definition of "medium complexity"
- ✅ Concrete examples showing target quality
- ✅ Realistic assessment of what's achievable
- ✅ Acceptance criteria for Storyteller output

### Output

- Document defining "medium complexity"
- Example outputs (simple, medium, realistic)
- Quality checklist for Storyteller

---

## Prototype 4: Character Extraction Test

### Goal

Test simple character extraction approaches to determine feasibility.

### Implementation

**File**: `examples/test_character_extraction.py`

```python
"""
Test character extraction from text.
"""

import re
from collections import Counter

def simple_extraction(text: str) -> dict:
    """Simple regex-based extraction."""
    # Find capitalized words (potential names)
    words = re.findall(r'\b[A-Z][a-z]+\b', text)
    word_counts = Counter(words)

    # Filter common words
    common = {'The', 'This', 'That', 'There', 'When', 'Where', 'What', 'How', 'Why'}
    characters = {}

    for word, count in word_counts.items():
        if count >= 2 and word not in common:
            characters[word] = {
                "name": word,
                "mentions": count,
                "first_mention": text.find(word),
                "context": []  # Could extract surrounding sentences
            }

    return characters

def test_extraction():
    """Test extraction on sample text."""
    sample = """
    Alice started working on the project. She encountered a bug.
    Bob helped her debug the issue. Alice and Bob worked together.
    Charlie reviewed the code. Alice fixed the bug. Bob was happy.
    """

    characters = simple_extraction(sample)

    print("Extracted characters:")
    for name, data in characters.items():
        print(f"  {name}: {data['mentions']} mentions")

    return characters

if __name__ == "__main__":
    test_extraction()
```

### Success Criteria

- ✅ Can identify main characters from text
- ✅ Accuracy > 70% (correctly identifies characters, few false positives)
- ✅ Performance acceptable (< 1 second for 10K words)

---

## Prototype Execution Plan

### Week 1: Tracery & Performance

- Day 1-2: Prototype 1 (Tracery complex grammar)
- Day 3-4: Prototype 2 (PDFGenerator scale)
- Day 5: Analyze results, document findings

### Week 2: Definition & Extraction

- Day 1-2: Prototype 3 (Define medium complexity)
- Day 3-4: Prototype 4 (Character extraction)
- Day 5: Compile findings, update implementation plan

### Deliverables

1. **Tracery Test Results**: Can/can't generate medium complexity
2. **Performance Report**: PDFGenerator scalability limits
3. **Complexity Definition**: Concrete examples and criteria
4. **Extraction Results**: Feasibility and accuracy

### Decision Points

- **If Tracery insufficient**: Add LLM integration to plan
- **If PDFGenerator slow**: Optimize algorithm or add caching
- **If extraction poor**: Require explicit character definition
- **If complexity unclear**: Simplify requirements

---

## Integration with Implementation

**Prototype results inform:**

- Implementation approach (Tracery vs. LLM)
- Performance optimizations needed
- Quality expectations
- Feature prioritization

**Timeline:**

- Prototypes: 2 weeks
- Implementation: 4 weeks (revised based on prototype findings)
- Total: 6 weeks to production-ready Storyteller