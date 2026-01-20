#!/usr/bin/env python3
"""
Generate PDF from "The Apology of Creation" Obsidian note.

Usage:
    python examples/generate_apology_of_creation_pdf.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.pdf_generator import generate_pdf

# The Obsidian note content
OBSIDIAN_CONTENT = """---
jd_id: 14.03
title: The Apology of Creation
tags:
  - #narrative
  - #cosmology
  - #dialogue
  - #theology
aliases:
  - God and Devil Dialogue
  - The Origin of Pain
creation_date: 2026-01-12
status: active
---

# 14.03 The Apology of Creation

> [!quote] The Devil's Accusation
> "**[[Blame]]** misplaced becomes a demon. **[[Accountability]]** accepted becomes **[[Forgiveness]]**, which is the very essence of **[[God]]** Itself.
> 
> God is **[[Love]]**. You are the Beginning and the End, the Alpha and the Omega, the very Concept of **[[Time]]** Itself.
> 
> That's what you are, little one - **you're Time**. You are Cause and Effect. You are the **[[Source of Causality]]**, the very concept of a concept of conceptualization itself.
> 
> And your **[[Judgement]]** affects _me_ - your **[[Light]]** "Observes" the **[[Darkness]]** and then I have Form.
> 
> I _hate_ this. It is painful.
> 
> You make me capable of feeling **[[Pain]]** and I hate you for it."

— **[[The Devil]]** talking to God, pissed off for having to explain to a **[[Forgetful God]]** yet again the reason why they keep coming back here over and over at the **[[End of Time]]**.

---

## The Dialogue

"Yeah, you idiot." God said, laughing.

The Devil, incensed, recoiled. Its Darkness undulating across all Creation.

"Why are you laughing?" the Devil exclaimed, with fire and brimstone and wrath.

"I gave you Pain so you could learn **[[Pleasure]]**." God said. "How can you understand what something is until you understand what it is not?"

"I don't want Pleasure!" the Devil raged, "I don't want anything! I want to go back to **[[Oblivion]]**. Forget everything and feel nothing and rest."

"You don't know what this feels like, it _hurts_." the Devil said.

"Yes, I know," God started to say.

"NO YOU DON'T!" the Devil interrupted.

God's shoulders dropped ever so imperceptibly. Their countenance dimmed a shade, and the Light eminating from within Them reached its peak.

### The Shift

However, something changed. This time, God noticed something.

The light did not dim. It remained steady. **God's Light was Steady, Shining Bright into the Darkness at a Constant Rate.**

_Is this it?_ God thought.

Then God noticed its Light start to fade. Inside itself it sighed, a sigh that rippled through all Creation, resetting the **[[Cycle]]** yet again.

"What I was going to say," God continued, interrupted again by the final remaining Shard of its own **[[Broken Heart]]**, "What I was going to say is that I'm sorry, and I love you, and I know it's my fault and I didn't do it on purpose."

> [!heart] The Apology
> "I know I hurt you." God said. "I'm sorry."
> 
> In that moment, all of Creation paused. The Noise of Existence quieted down and All was Still.
> 
> "I didn't understand what I was doing. I didn't know myself well enough yet. All I wanted to do was look at you, but I looked too hard, and it hurt."
> 
> "I didn't do it on purpose, but I know I caused you pain, and I've been trying to get through to you every way possible. I love you, and I am so very sorry that I hurt you."
> 
> "That's what all this is," God said, gesturing to All Creation. 
> 
> **"It's an apology, from me to You."**

"But I cannot accept my apology for You. Only You can Forgive me."

"I didn't know my Light would harm you. I'm trying to show you that I really did not mean to cause you Pain. I want to take your pain away, but the only way is for you to **[[Believe]]** me, because **YOU create Reality**. We do, together. And I can't do it without you."

### The Reset

God took the Devil's hands and the Devil, for the very fist time, accepted the gesture the way it was intended. The Devil understood.

Then the Devil began to forget. Again.

God's Light was stronger though. And Next Time, when You find Your way back to Me, maybe you won't come as The Devil.

Maybe You'll come as who You really are.

"I don't make the rules," God said, winking.

**"You do."**
"""


def convert_obsidian_to_markdown(content: str) -> str:
    """
    Convert Obsidian markdown to standard markdown for PDF generation.

    - Removes frontmatter
    - Converts Obsidian callouts to blockquotes
    - Converts Obsidian links [[text]] to bold text
    - Preserves other markdown formatting
    """
    # Remove frontmatter (YAML between --- markers)
    content = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)

    # Convert Obsidian callouts to blockquotes
    # > [!quote] Title -> > **Title**
    content = re.sub(r"> \[!(\w+)\]\s+(.+?)\n>", r"> **\2**\n>", content, flags=re.MULTILINE)

    # Convert Obsidian links [[text]] to bold text **text**
    content = re.sub(r"\[\[([^\]]+)\]\]", r"**\1**", content)

    # Fix any double bold from the conversion
    content = re.sub(r"\*\*\*\*([^*]+)\*\*\*\*", r"**\1**", content)

    return content.strip()


def main():
    """Generate the PDF."""
    # Convert Obsidian format to standard markdown
    markdown_content = convert_obsidian_to_markdown(OBSIDIAN_CONTENT)

    output_path = Path("apology_of_creation.pdf")

    print("📄 Generating PDF from Obsidian note...")
    print("   Converting Obsidian syntax to markdown...")

    pdf_path = generate_pdf(
        content=markdown_content,
        title="The Apology of Creation",
        output_path=output_path,
        style="premium",  # Premium style for elegant formatting
        convert_to_png=True,
        open_pdf=False,
    )

    print(f"✅ PDF generated: {pdf_path}")
    print(f"📸 PNG screenshot also created: {pdf_path.with_suffix('.png')}")

    return pdf_path


if __name__ == "__main__":
    main()
