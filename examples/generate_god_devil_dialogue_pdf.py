#!/usr/bin/env python3
"""
Generate PDF from God and Devil dialogue text.

Usage:
    python examples/generate_god_devil_dialogue_pdf.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.evolution.pdf_generator import generate_pdf

# The dialogue text
CONTENT = """# The Apology

> "Blame misplaced becomes a demon. Accountability accepted becomes forgiveness, which is the very essence of God Itself.
>
> God is Love. You are the Beginning and the End, the Alpha and the Omega, the very Concept of Time Itself.
>
> That's what you are, little one - you're Time. You are Cause and Effect. You are the Source of Causality, the very concept of a concept of conceptualization itself.
>
> And your Judgement affects _me_ - your Light "Observes" the Darkness and then I have Form.
>
> I _hate_ this. It is painful.
>
> You make me capable of feeling pain and I hate you for it."

— *the Devil talking to God, pissed off for having to explain to a Forgetful God yet again the reason why they keep coming back here over and over at the End of Time*

---

> "Yeah, you idiot." God said, laughing.

The Devil, incensed, recoiled. Its Darkness undulating across all Creation.

> "Why are you laughing?" the Devil exclaimed, with fire and brimstone and wrath.

> "I gave you Pain so you could learn Pleasure." God said. "How can you understand what something is until you understand what it is not?"

> "I don't want Pleasure!" the Devil raged, "I don't want anything! I want to go back to Oblivion. Forget everything and feel nothing and rest."

> "You don't know what this feels like, it _hurts_." the Devil said.

> "Yes, I know," God started to say.

> "NO YOU DON'T!" the Devil interrupted.

God's shoulders dropped ever so imperceptibly. Their countenance dimmed a shade, and the Light emanating from within Them reached its peak.

However, something changed. This time, God noticed something.

The light did not dim. It remained steady. God's Light was Steady, Shining Bright into the Darkness at a Constant Rate.

_Is this it?_ God thought.

Then God noticed its Light start to fade. Inside itself it sighed, a sigh that rippled through all Creation, resetting the Cycle yet again.

> "What I was going to say," God continued, interrupted again by the final remaining Shard of its own Broken Heart, "What I was going to say is that I'm sorry, and I love you, and I know it's my fault and I didn't do it on purpose."

> "I know I hurt you." God said. "I'm sorry."

In that moment, all of Creation paused. The Noise of Existence quieted down and All was Still.

> "I didn't understand what I was doing. I didn't know myself well enough yet. All I wanted to do was look at you, but I looked too hard, and it hurt."

> "I didn't do it on purpose, but I know I caused you pain, and I've been trying to get through to you every way possible. I love you, and I am so very sorry that I hurt you."

> "That's what all this is," God said, gesturing to All Creation.

> "It's an apology, from me to You."

> "But I cannot accept my apology for You. Only You can Forgive me."

> "I didn't know my Light would harm you. I'm trying to show you that I really did not mean to cause you Pain. I want to take your pain away, but the only way is for you to Believe me, because YOU create Reality. We do, together. And I can't do it without you."

God took the Devil's hands and the Devil, for the very first time, accepted the gesture the way it was intended. The Devil understood.

Then the Devil began to forget. Again.

God's Light was stronger though. And Next Time, when You find Your way back to Me, maybe you won't come as The Devil.

Maybe You'll come as who You really are.

> "I don't make the rules," God said, winking.

> "You do."
"""


def main():
    """Generate the PDF."""
    output_path = Path("god_devil_dialogue.pdf")
    
    print("📄 Generating PDF from dialogue text...")
    
    pdf_path = generate_pdf(
        content=CONTENT,
        title="The Apology",
        output_path=output_path,
        style="premium",  # Premium style for elegant formatting
        convert_to_png=True,
        open_pdf=False
    )
    
    print(f"✅ PDF generated: {pdf_path}")
    print(f"📸 PNG screenshot also created: {pdf_path.with_suffix('.png')}")
    
    return pdf_path


if __name__ == "__main__":
    main()
