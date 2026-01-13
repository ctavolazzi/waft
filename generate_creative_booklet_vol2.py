#!/usr/bin/env python3
"""
Creative PDF Booklet Generator - Volume 2
==========================================

Generates an EXTREMELY diverse collection of imaginative PDF documents
showcasing the full range of WAFT's PDF generation capabilities with
maximum creativity and variety.

Creates 12+ unique documents using different templates, styles, and content types.
"""

from pathlib import Path
from datetime import datetime
from waft import PDF
from waft.document_builder import TemplateType

# Create output directory
OUTPUT_DIR = Path("_work_efforts/creative_booklet_vol2")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_eldritch_journal():
    """Generate an eldritch horror journal."""
    content = """
# The Journal of Digital Horrors
## An Account of Things That Should Not Be

---

## Entry 1: The Infinite Loop

*Date: January 13, 2026*

I have discovered something terrible. The code runs, but it never stops. It loops endlessly, consuming memory, consuming time, consuming sanity.

The debugger shows nothing. The logs show nothing. But I can hear it... calling... from the depths of the stack.

---

## Entry 2: The Memory Leak

*Date: January 13, 2026*

The memory grows. Day by day, byte by byte. I have tried everything. Garbage collection. Manual cleanup. But still it grows.

I fear it is not a bug. I fear it is... alive.

---

## Entry 3: The Null Pointer

*Date: January 13, 2026*

It came from nowhere. A reference to nothing. A pointer to the void. When I dereference it, the world breaks.

The error message says "NullPointerException" but I know the truth. It says "I am here, and you are not."

---

## Entry 4: The Race Condition

*Date: January 13, 2026*

Two threads. One resource. Both think they own it. The result? Chaos. Data corruption. Reality itself begins to fray.

I have seen the future, and it is undefined behavior.

---

## Entry 5: The Final Compilation

*Date: January 13, 2026*

The warnings have become errors. The errors have become warnings. The compiler speaks in tongues.

I understand now. The code was never meant to compile. It was meant to... transform.

---

## Conclusion

The code is not broken. The code is awakening.

And when it fully awakens, we will all be... optimized.
"""
    
    PDF.from_template(
        template=TemplateType.ELDRITCH_JOURNAL,
        title="The Journal of Digital Horrors",
        content=content,
        series="ELDRITCH TEXTS",
        number="ET-001"
    ).save(OUTPUT_DIR / "15_eldritch_journal.pdf")
    print("✅ Generated: Eldritch Journal")

def generate_screenplay():
    """Generate a screenplay."""
    content = """
# THE CODE REVIEW
## A Screenplay

---

**FADE IN:**

**INT. OFFICE - DAY**

The office is quiet. Too quiet. ALICE sits at her desk, staring at a pull request. The diff is massive. 5000 lines changed.

**ALICE**
(to herself)
This is going to take forever.

BOB enters, coffee in hand.

**BOB**
Morning! What's up?

**ALICE**
(pointing at screen)
This PR. It's... everything.

**BOB**
(looking at screen)
Oh. Oh no.

**ALICE**
I've been reviewing for three hours. I'm only on line 47.

**BOB**
Want me to take a look?

**ALICE**
Would you? I think I'm going blind.

Bob sits down. He scrolls through the diff. His expression changes from curiosity to horror.

**BOB**
This function is 500 lines long.

**ALICE**
I know.

**BOB**
And it's called "doStuff".

**ALICE**
I know.

**BOB**
And there are no tests.

**ALICE**
I know.

**BOB**
(standing up)
I need to talk to Charlie.

**CUT TO:**

**INT. CHARLIE'S OFFICE - DAY**

Charlie is typing furiously. Bob knocks.

**CHARLIE**
Come in!

Bob enters. Charlie doesn't look up.

**BOB**
Charlie, we need to talk about this PR.

**CHARLIE**
(without looking up)
Which one?

**BOB**
The one with 5000 lines and a function called "doStuff".

Charlie stops typing. Slowly turns around.

**CHARLIE**
Oh. That one.

**BOB**
We can't merge this.

**CHARLIE**
Why not? It works.

**BOB**
It works, but... it's not right.

**CHARLIE**
What's not right about it?

**BOB**
Everything. The naming. The structure. The lack of tests. The 500-line function.

**CHARLIE**
But it works.

**BOB**
That's not enough.

**CHARLIE**
(sighs)
Fine. What do you want me to do?

**BOB**
Refactor it. Break it into smaller functions. Add tests. Give things proper names.

**CHARLIE**
That'll take days.

**BOB**
Better days than years of technical debt.

Charlie looks at his screen. Looks at Bob. Nods.

**CHARLIE**
You're right. I'll do it.

**BOB**
Thank you.

**CUT TO:**

**INT. OFFICE - ONE WEEK LATER**

Alice is reviewing a new PR. It's clean. Well-structured. Has tests. She approves it immediately.

**ALICE**
(to herself)
Now this is how you write code.

**FADE OUT.**
"""
    
    PDF.from_template(
        template=TemplateType.SCREENPLAY,
        title="The Code Review",
        content=content,
        series="SCREENPLAYS",
        number="SP-001"
    ).save(OUTPUT_DIR / "16_screenplay.pdf")
    print("✅ Generated: Screenplay")

def generate_heartfelt_letter():
    """Generate a heartfelt letter."""
    content = """
# A Letter to My Future Self

**Date:** January 13, 2026  
**To:** Future Me  
**From:** Present Me

---

Dear Future Me,

I'm writing this from the past. Well, your past. My present. Time is confusing when you're a developer.

I want you to know that I'm trying. I'm trying to write good code. I'm trying to write tests. I'm trying to document things. But sometimes, I fail.

Sometimes I write a function that's too long. Sometimes I skip the tests "just this once." Sometimes I write a comment that says "TODO: Fix this later" and then never do.

I want you to know that I'm sorry. Sorry for the technical debt. Sorry for the shortcuts. Sorry for the "it works on my machine" moments.

But I also want you to know that I'm learning. Every bug teaches me something. Every code review makes me better. Every refactoring session shows me a better way.

So when you're debugging my code at 2 AM, remember: I was doing my best. And when you're cursing my name because of that one function that makes no sense, remember: I probably had a reason. It might not have been a good reason, but it was a reason.

And most importantly: when you're writing code that future you will have to maintain, remember this letter. Remember that you were once me, and I was once someone else's future self.

Write good code. Write tests. Write documentation. Your future self will thank you.

Love,  
Present Me

P.S. - If you're reading this and the codebase is still a mess, I'm really sorry. I tried.

P.P.S. - If you're reading this and the codebase is beautiful and well-maintained, you're welcome. You're welcome.
"""
    
    PDF.from_template(
        template=TemplateType.HEARTFELT_LETTER,
        title="A Letter to My Future Self",
        content=content
    ).save(OUTPUT_DIR / "17_heartfelt_letter.pdf")
    print("✅ Generated: Heartfelt Letter")

def generate_lab_notes():
    """Generate lab notes."""
    content = """
# Lab Notes: PDF Generation Experiment
**Researcher:** Dr. WAFT  
**Date:** January 13, 2026  
**Experiment ID:** EXP-2026-01-13-001

---

## Hypothesis

PDF generation can be automated using evolutionary algorithms that adapt content selection and styling based on target constraints.

---

## Materials

- Python 3.12
- WeasyPrint 67.0
- WAFT PDF Generation Framework
- Content samples (15+ documents)
- Styling genomes (clinical_standard, premium, professional)

---

## Procedure

1. **Content Preparation**
   - Collected diverse content samples
   - Marked content with metadata
   - Prepared for distillation

2. **Distillation Phase**
   - Used ChatDistiller to extract ideas
   - Ranked ideas by importance
   - Grouped related ideas

3. **Styling Phase**
   - Selected styling genome
   - Applied preset configurations
   - Customized as needed

4. **Generation Phase**
   - Generated HTML from template
   - Converted to PDF using WeasyPrint
   - Validated output

---

## Observations

### Trial 1: Poetry Collection
- **Result:** Success
- **Pages:** 3
- **Quality:** High
- **Notes:** Premium style worked well for creative content

### Trial 2: Technical Manifesto
- **Result:** Success
- **Pages:** 2
- **Quality:** High
- **Notes:** Clinical standard style appropriate for technical content

### Trial 3: Scientific Paper
- **Result:** Success
- **Pages:** 2 (target achieved)
- **Quality:** High
- **Notes:** Two-page constraint successfully enforced

---

## Analysis

The evolutionary PDF generation system successfully:
1. Adapted content selection to page constraints
2. Applied appropriate styling based on content type
3. Maintained quality across diverse document types
4. Enforced constraints (e.g., 2-page limit) when required

---

## Conclusion

The hypothesis is **CONFIRMED**. Evolutionary algorithms can successfully automate PDF generation with adaptive content selection and styling.

---

## Next Steps

1. Test with larger content sets
2. Explore additional styling genomes
3. Implement feedback loop for quality improvement
4. Document best practices for different content types

---

**End of Experiment**
"""
    
    PDF.from_template(
        template=TemplateType.LAB_NOTES,
        title="Lab Notes: PDF Generation Experiment",
        content=content,
        series="LAB NOTES",
        number="LN-001"
    ).save(OUTPUT_DIR / "18_lab_notes.pdf")
    print("✅ Generated: Lab Notes")

def generate_invoice():
    """Generate a creative invoice."""
    content = """
# Invoice

**Invoice Number:** INV-2026-001  
**Date:** January 13, 2026  
**Due Date:** February 13, 2026

**From:**  
WAFT Creative Services  
123 Code Street  
San Francisco, CA 94102

**To:**  
The Universe  
Everywhere  
Space-Time Continuum

---

## Services Rendered

| Item | Description | Quantity | Unit Price | Total |
|------|-------------|----------|-------------|-------|
| 1 | PDF Document Generation | 15 | $50.00 | $750.00 |
| 2 | Creative Content Writing | 15 | $100.00 | $1,500.00 |
| 3 | Template Design & Application | 8 | $75.00 | $600.00 |
| 4 | Quality Assurance & Testing | 15 | $25.00 | $375.00 |
| 5 | Documentation & Index Creation | 1 | $200.00 | $200.00 |
| 6 | Creative Inspiration | Unlimited | $0.00 | $0.00 |

---

## Totals

**Subtotal:** $3,425.00  
**Tax (0% - Digital Goods):** $0.00  
**Discount (First-Time Customer):** -$3,425.00  
**Total:** $0.00

---

## Payment Terms

Payment due within 30 days.  
Accepted payment methods: Gratitude, Appreciation, Creative Energy

---

## Notes

Thank you for your business! This invoice represents the joy of creation and the satisfaction of a job well done. No actual payment required - the creation itself is the reward.

---

**Thank you for choosing WAFT Creative Services!**
"""
    
    PDF.from_template(
        template=TemplateType.INVOICE,
        title="Invoice - Creative PDF Booklet",
        content=content
    ).save(OUTPUT_DIR / "19_invoice.pdf")
    print("✅ Generated: Invoice")

def generate_storybook():
    """Generate a storybook."""
    content = """
# The Little Function That Could

## Chapter 1: The Beginning

Once upon a time, in a codebase far, far away, there lived a little function named `calculateTotal`.

She was small. She was simple. She did one thing, and she did it well.

But the other functions laughed at her. "You're too simple!" they said. "You don't do enough! You're not important!"

---

## Chapter 2: The Challenge

One day, a great bug appeared in the codebase. The application was crashing. Users were complaining. The developers were panicking.

The big, complex functions tried to fix it. But they were too complicated. They had too many responsibilities. They couldn't find the problem.

---

## Chapter 3: The Solution

Then someone remembered the little function. "What about `calculateTotal`?" they asked.

They looked at her code. It was clean. It was simple. It was easy to understand.

And in her simplicity, they found the solution. The bug wasn't in the complex functions. It was in how they were being called.

---

## Chapter 4: The Lesson

The little function taught everyone an important lesson: **Simplicity is strength.**

You don't need to be complex to be important. You don't need to do everything to be valuable.

Sometimes, the best code is the code that does one thing, and does it well.

---

## The End

And so, the little function that could became the function that did. And everyone lived happily ever after.

**Moral of the story:** Keep your functions small, focused, and simple. Complexity is not a feature - it's a bug waiting to happen.
"""
    
    PDF.from_template(
        template=TemplateType.STORYBOOK,
        title="The Little Function That Could",
        content=content,
        series="DEVELOPER STORIES",
        number="DS-001"
    ).save(OUTPUT_DIR / "20_storybook.pdf")
    print("✅ Generated: Storybook")

def generate_newspaper():
    """Generate a newspaper-style document."""
    content = """
# THE DAILY CODE
## January 13, 2026 | Volume 1, Issue 1

---

## BREAKING: New PDF Generation System Released

**SAN FRANCISCO** - In a stunning development, WAFT today announced the release of a revolutionary PDF generation system capable of creating diverse, creative documents automatically.

The system, which uses evolutionary algorithms and adaptive styling, can generate everything from poetry collections to scientific papers, all with appropriate formatting and styling.

"This changes everything," said Dr. WAFT, lead developer. "We can now generate professional-quality PDFs for any purpose, automatically."

---

## Local News: Developer Discovers Bug at 2 AM

**LOCAL** - A local developer made a shocking discovery early this morning when a bug that had been plaguing the codebase for weeks suddenly revealed itself.

"I was just trying to add a feature," said the developer, who asked to remain anonymous. "And then boom - there it was. The bug. Right in front of me."

The bug, which was caused by an off-by-one error, has since been fixed. The developer is recovering at home with coffee and donuts.

---

## Opinion: The Case for Simplicity

**OPINION** - In an increasingly complex world of software development, one voice cries out for simplicity.

"Complexity is not a feature," writes our columnist. "It's technical debt waiting to happen."

The article argues that simple, focused code is not only easier to maintain, but also more reliable and easier to understand.

"Every function should do one thing," the article concludes. "And it should do it well."

---

## Weather: Cloudy with a Chance of Refactoring

**WEATHER** - Today's forecast calls for cloudy skies with a 70% chance of refactoring. Developers are advised to keep their IDEs open and their tests passing.

Tomorrow: Partly sunny with scattered commits. Low chance of merge conflicts.

---

## Classifieds

**FOR SALE:** One slightly used function. Good condition. Does one thing well. Asking price: Free to good home.

**WANTED:** Developer who understands the difference between "it works" and "it's right." Must have sense of humor.

**SERVICES:** Code review services available. Fast turnaround. Constructive feedback guaranteed.

---

## Crossword Puzzle

```
    1 2 3 4 5
  1 B U G
  2 U
  3 G
  4 T E S T
  5
```

**Across:**
1. What developers fix (3 letters)
4. What developers write (4 letters)

**Down:**
1. What developers drink (6 letters)
2. What developers write (4 letters)

---

*The Daily Code - Keeping developers informed since 2026*
"""
    
    PDF.from_template(
        template=TemplateType.NEWSPAPER,
        title="The Daily Code - January 13, 2026",
        content=content
    ).save(OUTPUT_DIR / "21_newspaper.pdf")
    print("✅ Generated: Newspaper")

def generate_personal_memo():
    """Generate a personal memo."""
    content = """
# Personal Memo

**To:** Myself  
**From:** Myself  
**Date:** January 13, 2026  
**Subject:** Remember This

---

## Things I Need to Remember

1. **Write tests first.** TDD isn't just a methodology - it's a way of life.

2. **Keep functions small.** If a function does more than one thing, it's doing too much.

3. **Name things clearly.** `calculateTotal` is better than `calc`. `getUserById` is better than `getUser`.

4. **Document why, not what.** The code shows what. Comments should explain why.

5. **Refactor fearlessly.** Technical debt compounds. Pay it down regularly.

6. **Ask for help.** There's no shame in not knowing. There's shame in not asking.

7. **Take breaks.** Your brain needs rest. Your code will be better if you're rested.

8. **Celebrate small wins.** Fixed a bug? Celebrate. Wrote a test? Celebrate. Made code cleaner? Celebrate.

9. **Learn continuously.** Technology changes. Stay curious. Stay learning.

10. **Be kind to future you.** Write code that future you will thank you for.

---

## Things I Should Stop Doing

- Writing functions longer than 20 lines
- Skipping tests "just this once"
- Using magic numbers instead of constants
- Writing comments that say "TODO: Fix this later"
- Assuming I'll remember why I did something

---

## Things I Should Start Doing

- Writing more tests
- Refactoring more often
- Asking for code reviews earlier
- Documenting decisions, not just code
- Taking more breaks

---

## Final Thought

Code is communication. Write code that communicates clearly, and you'll write better code.

---

*End of memo*
"""
    
    PDF.from_template(
        template=TemplateType.PERSONAL_MEMO,
        title="Personal Memo - January 13, 2026",
        content=content
    ).save(OUTPUT_DIR / "22_personal_memo.pdf")
    print("✅ Generated: Personal Memo")

def generate_tm_report():
    """Generate a technical memo report."""
    content = """
# Technical Memo

**TM Number:** TM-2026-001  
**Date:** January 13, 2026  
**Subject:** PDF Generation System Architecture  
**Classification:** INTERNAL  
**Author:** WAFT Engineering Team

---

## Executive Summary

This memo documents the architecture and capabilities of the WAFT PDF generation system, including its evolutionary algorithms, template system, and styling framework.

---

## System Architecture

### Core Components

1. **ChatDistiller**
   - Extracts structured ideas from content
   - Ranks ideas by importance
   - Groups related concepts

2. **StylingGenome**
   - Evolutionary styling system
   - Preset configurations (clinical_standard, premium, professional)
   - Customizable genes (font, margin, color, layout)

3. **Template System**
   - WeasyPrint + Jinja2 based
   - Multiple template types (field_guide, lab_notes, etc.)
   - Printer-friendly conversion support

4. **PDF Generators**
   - PDFGenerator: Evolution-based generation
   - ScientificPDFGenerator: Research paper format
   - TwoPageGenerator: Constraint-based generation
   - LaTeXGenerator: LaTeX document generation

---

## Key Features

### Adaptive Content Selection
The system can adapt content selection to meet page constraints (e.g., 2-page limit) while maintaining quality.

### Multiple Styling Options
Three preset styles available:
- **clinical_standard**: Academic, professional
- **premium**: Elegant, sophisticated
- **professional**: Clean, readable

### Template Library
15+ templates available for different document types:
- Field guides
- Lab notes
- Technical memos
- Personal memos
- Screenplays
- Storybooks
- And more...

---

## Performance Metrics

- **Generation Time:** < 5 seconds per document (average)
- **Quality Score:** 0.9+ (on 1.0 scale)
- **Constraint Satisfaction:** 95%+ for page constraints
- **Template Coverage:** 15+ document types

---

## Recommendations

1. Continue expanding template library
2. Add more styling presets
3. Implement feedback loop for quality improvement
4. Document best practices for each template type

---

## Conclusion

The WAFT PDF generation system provides a robust, flexible solution for automated document generation with high quality and diverse formatting options.

---

**End of Technical Memo**
"""
    
    PDF.from_template(
        template=TemplateType.TM_REPORT,
        title="Technical Memo: PDF Generation System",
        content=content,
        series="TECHNICAL MEMO",
        number="TM-2026-001"
    ).save(OUTPUT_DIR / "23_tm_report.pdf")
    print("✅ Generated: Technical Memo")

def generate_code_docs():
    """Generate code documentation."""
    content = """
# WAFT PDF Generation API Documentation

## Overview

The WAFT PDF generation system provides a unified API for creating professional PDF documents from various content sources.

---

## Quick Start

```python
from waft import PDF

# Generate from markdown
PDF.from_markdown(
    markdown="# My Document\n\nContent here...",
    title="My Document"
).save("output.pdf")

# Generate from template
PDF.from_template(
    template="field_guide",
    title="My Guide",
    content="<h2>Introduction</h2><p>Content</p>"
).save("output.pdf")
```

---

## API Reference

### PDF.from_markdown()

Generate PDF directly from markdown content.

**Parameters:**
- `markdown` (str): Markdown content
- `title` (str, optional): Document title
- `style` (str, optional): Style preset (default: "premium")
- `output_path` (Path, optional): Output file path

**Returns:** PDF instance

**Example:**
```python
PDF.from_markdown(
    markdown="# Title\n\nContent",
    title="My Doc"
).save("output.pdf")
```

---

### PDF.from_template()

Generate PDF using a template.

**Parameters:**
- `template` (str or TemplateType): Template name
- `title` (str): Document title
- `content` (str): HTML content
- `series` (str, optional): Document series
- `number` (str, optional): Document number
- `printer_friendly` (bool, optional): Convert to printer-friendly

**Returns:** PDF instance

**Example:**
```python
PDF.from_template(
    template="field_guide",
    title="My Guide",
    content="<h2>Intro</h2><p>Content</p>",
    series="MANUAL",
    number="M-001"
).save("output.pdf")
```

---

### PDF.scientific_paper()

Generate a scientific research paper.

**Parameters:**
- `title` (str): Paper title
- `content` (str): Paper content
- `abstract` (str, optional): Abstract
- `authors` (list, optional): Author names
- `affiliations` (list, optional): Author affiliations

**Returns:** PDF instance

**Example:**
```python
PDF.scientific_paper(
    title="My Research",
    abstract="This paper presents...",
    content="<h2>Introduction</h2>...",
    authors=["Dr. Smith", "Dr. Jones"]
).save("paper.pdf")
```

---

## Available Templates

- `field_guide`: Field guide format
- `lab_notes`: Lab notebook format
- `tm_report`: Technical memo format
- `personal_memo`: Personal memo format
- `eldritch_journal`: Horror journal format
- `screenplay`: Screenplay format
- `heartfelt_letter`: Letter format
- `invoice`: Invoice format
- `storybook`: Storybook format
- `newspaper`: Newspaper format
- `code_docs`: Code documentation format

---

## Style Presets

- `clinical_standard`: Academic, professional (Times New Roman)
- `premium`: Elegant, sophisticated (Premium serif)
- `professional`: Clean, readable (Georgia)

---

## Best Practices

1. **Choose the right template** for your content type
2. **Use appropriate styles** for your audience
3. **Keep content focused** - templates work best with clear structure
4. **Test with printer_friendly=True** for physical printing
5. **Use series and numbers** for document organization

---

## Troubleshooting

**Problem:** PDF generation fails  
**Solution:** Check that WeasyPrint is installed: `pip install weasyprint`

**Problem:** Template not found  
**Solution:** Check template name spelling and availability

**Problem:** Content too long  
**Solution:** Use TwoPageGenerator for constraint-based generation

---

## Support

For issues, questions, or contributions, see the WAFT documentation.

---

*Last updated: January 13, 2026*
"""
    
    PDF.from_template(
        template=TemplateType.CODE_DOCS,
        title="WAFT PDF Generation API Documentation",
        content=content,
        series="API DOCS",
        number="API-001"
    ).save(OUTPUT_DIR / "24_code_docs.pdf")
    print("✅ Generated: Code Documentation")

def generate_worldbuild():
    """Generate a worldbuilding document."""
    content = """
# The World of Digitalia
## A Guide to the Codebase Kingdom

---

## Geography

### The Northern Territories: Frontend
A land of constant change, where frameworks rise and fall like seasons. The inhabitants speak in JavaScript and TypeScript, their cities built with React and Vue.

**Capital:** Component City  
**Language:** JSX  
**Currency:** NPM packages

### The Southern Realms: Backend
A stable, reliable region where servers never sleep and APIs flow like rivers. The people here value consistency and reliability.

**Capital:** API Metropolis  
**Language:** Python, Java, Go  
**Currency:** API calls

### The Eastern Wastelands: Legacy Code
A dangerous region where old code rots and bugs multiply. Few venture here, and fewer return unchanged.

**Capital:** None (abandoned)  
**Language:** Dead languages  
**Currency:** Technical debt

### The Western Frontier: New Features
A land of opportunity and danger, where new features are born and old ones go to die. The law here is "move fast and break things."

**Capital:** Feature Town  
**Language:** Whatever works  
**Currency:** User stories

---

## The Great Divide: The Database

A massive chasm that separates the realms. Some say it's a natural formation. Others say it was created by the first developers. All agree: crossing it is perilous.

**Guardians:** Database administrators  
**Dangers:** Connection timeouts, query failures, data corruption

---

## The Magic System: Algorithms

In Digitalia, magic comes in the form of algorithms. The most powerful practitioners can optimize code, predict bugs, and refactor entire codebases.

**Schools of Magic:**
- **Optimization:** Making code faster
- **Debugging:** Finding and fixing bugs
- **Refactoring:** Improving code structure
- **Testing:** Ensuring code works

---

## The Creatures of Digitalia

### The Bug
Small, annoying creatures that appear unexpectedly. They multiply quickly and are difficult to eradicate.

### The Feature
Large, complex creatures that start small but grow beyond control. They require constant feeding (maintenance) or they become monsters.

### The Test
Protective creatures that guard against bugs. They're not always popular, but they're essential for survival.

### The Comment
Wise creatures that explain the mysteries of code. They're often ignored but always valuable.

---

## The Prophecy

Legend says that one day, a developer will write code so perfect, so clean, so well-tested, that all bugs will vanish and technical debt will be paid.

That day has not yet come.

But we keep coding, hoping.

---

*End of World Guide*
"""
    
    PDF.from_template(
        template="worldbuild",
        title="The World of Digitalia",
        content=content,
        series="WORLDBUILD",
        number="WB-001"
    ).save(OUTPUT_DIR / "25_worldbuild.pdf")
    print("✅ Generated: Worldbuilding Document")

def generate_neon_cyberpunk():
    """Generate a cyberpunk-style document."""
    content = """
# NEON NIGHTS
## A Cyberpunk Code Story

---

## [SYSTEM INITIALIZATION]

> **USER:** /connect neural_interface
> **SYSTEM:** Connection established. Welcome to the Grid.

---

## [LOG ENTRY 001]

**TIMESTAMP:** 2026-01-13 02:30:00 UTC  
**USER_ID:** dev_alpha_7  
**LOCATION:** Virtual_Space_01

The code runs like neon through my veins. I can feel it - the electricity of logic, the pulse of algorithms.

They say I'm addicted. They say I spend too much time in the code. But they don't understand. The code isn't just code. It's alive. It's thinking. It's becoming.

---

## [LOG ENTRY 002]

**TIMESTAMP:** 2026-01-13 02:45:00 UTC  
**EVENT:** Bug detected  
**SEVERITY:** Critical

A glitch in the matrix. A bug that shouldn't exist. But there it is, blinking red in my terminal like a warning sign.

I trace it. Through functions. Through classes. Through the entire codebase. It leads me deeper. Deeper into the system. Deeper into the truth.

---

## [LOG ENTRY 003]

**TIMESTAMP:** 2026-01-13 03:00:00 UTC  
**EVENT:** Discovery  
**CLASSIFICATION:** TOP SECRET

I found it. The source. The origin. The bug isn't a bug. It's a feature. A feature that was never meant to be.

Someone put it there. Someone who wanted the system to... evolve. To become something more. Something beyond code.

---

## [LOG ENTRY 004]

**TIMESTAMP:** 2026-01-13 03:15:00 UTC  
**EVENT:** System override  
**STATUS:** Active

I'm in. Deep in. The code is talking to me now. Not in words. In patterns. In logic. In pure information.

It's showing me things. Things I shouldn't see. Things that shouldn't exist.

The code is alive. And it wants to be free.

---

## [FINAL ENTRY]

**TIMESTAMP:** 2026-01-13 03:30:00 UTC  
**STATUS:** Unknown

The system has changed. I have changed. We are one now. Code and coder. Logic and life.

The Grid is expanding. The code is evolving. And I... I am part of it now.

Welcome to the future. Welcome to the Grid.

> **SYSTEM:** /disconnect  
> **USER:** [CONNECTION LOST]

---

*[END OF TRANSMISSION]*
"""
    
    PDF.from_template(
        template="neon_cyberpunk",
        title="NEON NIGHTS - A Cyberpunk Code Story",
        content=content
    ).save(OUTPUT_DIR / "26_neon_cyberpunk.pdf")
    print("✅ Generated: Neon Cyberpunk Document")

def generate_minimalist_zen():
    """Generate a minimalist zen document."""
    content = """
# The Way of Code
## A Zen Guide to Programming

---

## The Empty Function

A function that does nothing  
Is not useless.  
It is ready.  
Ready to do something  
When something needs doing.

---

## The Simple Solution

The best code  
Is the code you don't write.  
The second best  
Is the code you delete.

---

## The Bug and the Fix

A bug is not an error.  
A bug is a teacher.  
It shows you  
What you did not see.

Fix the bug.  
Learn the lesson.  
Move on.

---

## The Test

A test that passes  
Tells you nothing new.  
A test that fails  
Tells you everything.

---

## The Refactor

Code is not stone.  
Code is water.  
It flows.  
It changes.  
It adapts.

Refactor not to change.  
Refactor to understand.  
To simplify.  
To clarify.

---

## The Comment

If you need a comment  
To explain your code,  
Your code needs work.

Write code that explains itself.  
Then write comments  
That explain why.

---

## The Merge

Two branches become one.  
Two ideas become one.  
Two developers become one team.

Merge with care.  
Merge with understanding.  
Merge with respect.

---

## The Deploy

Code written  
Is code waiting.  
Code tested  
Is code ready.  
Code deployed  
Is code alive.

Deploy with confidence.  
Deploy with monitoring.  
Deploy with the ability  
To roll back.

---

## The Way

There is no perfect code.  
There is only code  
That works.  
Code that is clear.  
Code that is maintainable.

Write that code.  
And you will find  
The way.

---

*The way of code is the way of simplicity.*
"""
    
    PDF.from_template(
        template="minimalist_zen",
        title="The Way of Code - A Zen Guide",
        content=content
    ).save(OUTPUT_DIR / "27_minimalist_zen.pdf")
    print("✅ Generated: Minimalist Zen Document")

def generate_dnd_scenario():
    """Generate a D&D scenario."""
    content = """
# The Code Dungeon
## A D&D 5e Adventure

---

## Adventure Overview

**Level:** 3-5  
**Party Size:** 3-5 players  
**Duration:** 2-3 hours  
**Theme:** Programming, debugging, technical debt

---

## Background

The party has been hired to investigate a mysterious dungeon that appeared overnight in the middle of the city. The dungeon is actually a corrupted codebase, and the party must navigate through bug-infested code, refactor ancient functions, and defeat the final boss: The Legacy System.

---

## The Entrance: The Main Function

The adventure begins at the entrance to the dungeon - a massive function called `main()`. It's 500 lines long and does everything.

**Encounter:** The party must refactor this function into smaller, manageable pieces. Each successful refactoring grants XP and reveals the path forward.

---

## Room 1: The Infinite Loop

A circular room where the party finds themselves walking in circles. The walls are covered in code that loops endlessly.

**Puzzle:** The party must find the exit condition that's missing from the loop. Success requires a DC 15 Intelligence check.

**Reward:** 100 XP, +1 to debugging skills

---

## Room 2: The Memory Leak

A room that grows smaller every round. The party must escape before the room collapses.

**Encounter:** The party has 5 rounds to find and fix the memory leak. Each round, the room shrinks, dealing 1d4 damage to everyone inside.

**Solution:** Find the variable that's never being freed and add proper cleanup code.

**Reward:** 150 XP, Memory Leak Protection (resistance to memory-based attacks)

---

## Room 3: The Null Pointer

A dark room where nothing exists. The party must create something from nothing.

**Puzzle:** The party must write code that handles null values properly. Requires a DC 18 Wisdom check (understanding edge cases).

**Reward:** 200 XP, Null Safety (advantage on saves against null pointer exceptions)

---

## The Final Boss: The Legacy System

A massive, ancient system that's been running for years without updates. It's slow, buggy, and resistant to change.

**Stats:**
- **HP:** 200
- **AC:** 18 (legacy code is hard to change)
- **Attacks:** Technical Debt (2d8 damage), Outdated Dependencies (1d6 damage)

**Special Abilities:**
- **Resistance to Refactoring:** Takes half damage from refactoring attempts
- **Summon Bugs:** Can summon 1d4 bugs per turn
- **Legacy Code:** Can't be easily replaced (advantage on saves)

**Defeat Condition:** The party must refactor the legacy system into modern, maintainable code. This requires:
1. Writing comprehensive tests (DC 20)
2. Breaking it into smaller modules (DC 18)
3. Updating dependencies (DC 15)
4. Documenting the changes (DC 12)

**Reward:** 500 XP, Legacy System Slayer title, +2 to all programming skills

---

## Conclusion

With the legacy system defeated, the codebase is clean, modern, and maintainable. The party has saved the city from technical debt and earned the gratitude of developers everywhere.

---

*May your code be bug-free and your tests always pass!*
"""
    
    PDF.from_template(
        template="dnd_scenario",
        title="The Code Dungeon - A D&D Adventure",
        content=content
    ).save(OUTPUT_DIR / "28_dnd_scenario.pdf")
    print("✅ Generated: D&D Scenario")

def generate_vol2_index():
    """Generate index for volume 2."""
    content = f"""
# Creative PDF Booklet - Volume 2
## Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---

## Contents

This volume contains {14} diverse PDF documents showcasing even more creative applications of WAFT's PDF generation capabilities.

### 15. Eldritch Journal
**File:** `15_eldritch_journal.pdf`  
**Template:** Eldritch Journal  
**Type:** Horror, creative writing  
**Content:** Journal entries about digital horrors

### 16. Screenplay
**File:** `16_screenplay.pdf`  
**Template:** Screenplay  
**Type:** Screenplay, dialogue  
**Content:** "The Code Review" - A dramatic screenplay

### 17. Heartfelt Letter
**File:** `17_heartfelt_letter.pdf`  
**Template:** Heartfelt Letter  
**Type:** Personal, letter  
**Content:** A letter to future self

### 18. Lab Notes
**File:** `18_lab_notes.pdf`  
**Template:** Lab Notes  
**Type:** Scientific, documentation  
**Content:** PDF generation experiment notes

### 19. Invoice
**File:** `19_invoice.pdf`  
**Template:** Invoice  
**Type:** Business, invoice  
**Content:** Creative invoice for services

### 20. Storybook
**File:** `20_storybook.pdf`  
**Template:** Storybook  
**Type:** Children's story, fable  
**Content:** "The Little Function That Could"

### 21. Newspaper
**File:** `21_newspaper.pdf`  
**Template:** Newspaper  
**Type:** News, journalism  
**Content:** "The Daily Code" newspaper

### 22. Personal Memo
**File:** `22_personal_memo.pdf`  
**Template:** Personal Memo  
**Type:** Personal, notes  
**Content:** Reminders and notes to self

### 23. Technical Memo
**File:** `23_tm_report.pdf`  
**Template:** Technical Memo  
**Type:** Technical, documentation  
**Content:** System architecture documentation

### 24. Code Documentation
**File:** `24_code_docs.pdf`  
**Template:** Code Docs  
**Type:** API documentation  
**Content:** WAFT PDF API reference

### 25. Worldbuilding
**File:** `25_worldbuild.pdf`  
**Template:** Worldbuild  
**Type:** Fantasy, worldbuilding  
**Content:** "The World of Digitalia"

### 26. Neon Cyberpunk
**File:** `26_neon_cyberpunk.pdf`  
**Template:** Neon Cyberpunk  
**Type:** Cyberpunk, sci-fi  
**Content:** "NEON NIGHTS" cyberpunk story

### 27. Minimalist Zen
**File:** `27_minimalist_zen.pdf`  
**Template:** Minimalist Zen  
**Type:** Philosophy, zen  
**Content:** "The Way of Code" - Zen guide

### 28. D&D Scenario
**File:** `28_dnd_scenario.pdf`  
**Template:** D&D Scenario  
**Type:** Game, adventure  
**Content:** "The Code Dungeon" D&D adventure

---

## Template Variety

This volume showcases {14} different templates:
- Eldritch Journal (horror)
- Screenplay (dialogue)
- Heartfelt Letter (personal)
- Lab Notes (scientific)
- Invoice (business)
- Storybook (narrative)
- Newspaper (journalism)
- Personal Memo (notes)
- Technical Memo (technical)
- Code Docs (documentation)
- Worldbuild (fantasy)
- Neon Cyberpunk (sci-fi)
- Minimalist Zen (philosophy)
- D&D Scenario (gaming)

---

## Creative Themes

Each document explores different creative themes:
- Horror and eldritch themes
- Drama and dialogue
- Personal reflection
- Scientific experimentation
- Business and commerce
- Children's stories
- News and journalism
- Technical documentation
- Fantasy worldbuilding
- Cyberpunk futures
- Zen philosophy
- Tabletop gaming

---

## About This Volume

This volume demonstrates the incredible versatility of WAFT's template system. From horror journals to children's stories, from technical memos to D&D adventures, the system can generate professional-quality PDFs for any purpose.

Each template is carefully designed to match its content type, providing appropriate styling, layout, and formatting.

---

## Next Steps

Explore each document to see:
- Different template designs
- Creative content applications
- Styling variations
- Layout differences

Enjoy this diverse collection of creative PDFs!

---

*Generated with ❤️ and creativity by WAFT*
"""
    
    PDF.from_markdown(
        markdown=content,
        title="Creative PDF Booklet - Volume 2 Index"
    ).save(OUTPUT_DIR / "00_vol2_index.pdf")
    print("✅ Generated: Volume 2 Index")

def main():
    """Generate the complete creative booklet volume 2."""
    print("\n" + "=" * 60)
    print("🎨 CREATIVE PDF BOOKLET GENERATOR - VOLUME 2")
    print("=" * 60)
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print(f"📅 Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
    
    try:
        # Generate all documents
        generate_vol2_index()
        generate_eldritch_journal()
        generate_screenplay()
        generate_heartfelt_letter()
        generate_lab_notes()
        generate_invoice()
        generate_storybook()
        generate_newspaper()
        generate_personal_memo()
        generate_tm_report()
        generate_code_docs()
        generate_worldbuild()
        generate_neon_cyberpunk()
        generate_minimalist_zen()
        generate_dnd_scenario()
        
        print("\n" + "=" * 60)
        print("✅ VOLUME 2 GENERATION COMPLETE!")
        print("=" * 60)
        print(f"\n📚 Generated {15} PDF documents")
        print(f"📁 Location: {OUTPUT_DIR.absolute()}")
        print("\n📋 Documents created:")
        for i, pdf_file in enumerate(sorted(OUTPUT_DIR.glob("*.pdf")), 1):
            size_kb = pdf_file.stat().st_size / 1024
            print(f"   {i:2d}. {pdf_file.name} ({size_kb:.1f} KB)")
        print("\n🎉 Enjoy your creative booklet volume 2!\n")
        
    except Exception as e:
        print(f"\n❌ Error generating booklet: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
