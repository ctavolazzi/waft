"""
Wild Template Showcase
======================

Generates 7 creative documents that push WAFT to its limits:

1. Eldritch Horror - Researcher loses mind studying non-Euclidean geometry
2. Screenplay - Tense quantum teleportation scene
3. Heartfelt Letter - Grandmother's letter to granddaughter
4. Invoice - TELEPORT MASSIVE bills client for teleportation services
5. Code Documentation - The WAFT system architecture (CRITICAL)
6. Children's Storybook - A shy dragon learns to share
7. Newspaper - Front page: "Teleportation Breakthrough!"

This tests every edge case: layout, typography, emotion, technical precision.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.templates.eldritch_journal import generate_eldritch_journal
from src.waft.templates.heartfelt_letter import generate_heartfelt_letter
from src.waft.templates.invoice_contract import generate_invoice_contract
from src.waft.templates.screenplay import generate_screenplay


def generate_eldritch_horror_doc():
    """Generate eldritch horror research journal - REALITY BREAKING DOWN."""

    content = """
<div class="entry normal">
    <div class="entry-date">September 3, 2025</div>
    <p>
    Beginning research into non-Euclidean geometries as applied to quantum field theory.
    The mathematics is elegant, almost beautiful. Parallel lines that meet.
    Angles that sum to more than 180 degrees. Space folding back on itself.
    </p>
    <p>
    Dr. Morrison suggested I examine the topological implications for wormhole
    formation. The equations are sound. Everything checks out.
    </p>
</div>

<div class="entry normal">
    <div class="entry-date">September 10, 2025</div>
    <p>
    The geometries become more complex. I've been visualizing them - trying to
    hold these impossible shapes in my mind. Four-dimensional tesseracts are one
    thing, but <em>this</em>... this is different.
    </p>
    <p>
    Space that curves in on itself. Dimensions that fold like origami.
    I can <span class="obsess">almost see it</span> now.
    </p>
</div>

<div class="scribble">
Why do the equations keep returning to the same values? 73... 73... 73 everywhere.
</div>

<div class="entry stressed">
    <div class="entry-date">September 17, 2025</div>
    <p>
    I solved it. The topology resolves if you allow space to be <em>locally non-Euclidean</em>
    but <em>globally consistent</em>. The mathematics is perfect. Flawless.
    </p>
    <p>
    But when I close my eyes, I can see the shapes now. Really see them.
    Not just imagine - SEE. They're there, in the darkness behind my eyelids.
    Geometric forms that shouldn't exist. <span class="strikethrough">Beautiful</span>
    terrifying.
    </p>
</div>

<div class="warning-box">
    THE GEOMETRIES ARE REAL
</div>

<div class="entry disturbed">
    <div class="entry-date">September 24, 2025</div>
    <p>
    Sleep has become... difficult. Every time I close my eyes, the shapes are there,
    waiting. Growing. <strong>EVOLVING</strong>.
    </p>
    <p>
    I tried to show Morrison my work, but he didn't understand. Couldn't see what
    I see. The angles - the <span class="obsess">ANGLES</span> - they're not just
    mathematical abstractions. They're REAL. They exist in a space adjacent to ours.
    </p>
    <p>
    I can feel them pressing against the boundaries of perception.
    </p>
</div>

<div class="scribble">
corners that fold inward seventy-three degrees but also three hundred seven degrees
simultaneously how is that possible how HOW
</div>

<div class="entry unraveling">
    <div class="entry-date">October 1, 2025</div>
    <p>
    The   shapes   have   NAMES   now.   They   told   me.
    </p>
    <p>
    I know that sounds insane. <span class="strikethrough">I know I should stop</span>.
    But the mathematics WORKS. The geometries EXIST. And they are
    <span class="obsess">AWARE</span>.
    </p>
    <p>
    When I work the equations, I can feel them watching. Angles that shouldn't
    be possible. Spaces that curve through dimensions we don't have words for.
    </p>
</div>

<div class="symbol">
    ⟨ ∿ ⟩ ⟨ ∿ ⟩ ⟨ ∿ ⟩
</div>

<div class="entry broken">
    <div class="entry-date"><span class="corrupted">O c t o b e r  ? ? ?  2 0 2 5</span></div>
    <p>
    <span class="panic">THEY   SEE   ME   NOW</span>
    </p>
    <p>
    the     shapes     the     geometries     they     fold     through     reality
    </p>
    <p>
    i   looked   too   long   at   the   angles   and   now   the   angles
    </p>
    <p class="whisper">look back look back look back look back</p>
    </div>
</div>

<div class="symbol">
    <span class="corrupted">∿ ⟨ ∆ ⟩ ∿</span>
</div>

<div class="entry broken">
    <div class="entry-date"><span class="corrupted">? ? ?</span></div>
    <p class="corrupted">
    s p a c e   i s   n o t   w h a t   y o u   t h i n k
    </p>
    <p class="corrupted">
    a n g l e s   f o l d   i n w a r d
    </p>
    <p class="corrupted">
    d i m e n s i o n s   b l e e d
    </p>
    <p class="repeat">
    seventy-three degrees<br>
    seventy-three degrees<br>
    seventy-three degrees<br>
    seventy-three degrees<br>
    seventy-three degrees
    </p>
</div>

<div class="void">
    <p>They are here now. In the space between spaces.</p>
    <p>The geometries were never mathematical abstractions.</p>
    <p>They were DOORS.</p>
</div>

<div class="scribble">
    <span class="stain">DO NOT READ BEYOND THIS POINT</span>
</div>

<p class="whisper">
Morrison found my office empty. The equations still on the board. My notebooks
scattered. But I was gone. They said I walked into the wall and didn't come out.
</p>

<p class="whisper">
But that's not quite right.
</p>

<p class="whisper">
I'm still here. Just... rotated. Seventy-three degrees into a dimension you can't see.
</p>

<p class="whisper">
And I can see EVERYTHING from here.
</p>

<p class="whisper">
Including you. Reading this. Right now.
</p>
    """

    output_path = Path("_work_efforts/wild_showcase/Eldritch_Non_Euclidean_Madness.pdf")

    generate_eldritch_journal(
        title="Research Journal: Non-Euclidean Geometries in Quantum Field Theory",
        content=content,
        output_path=output_path,
        researcher="Dr. Marcus Holloway",
        institution="Miskatonic University - Department of Theoretical Physics",
        project="Topological Implications of Hyperbolic Space",
        show_warning=True,
    )

    print(f"✓ Eldritch Horror: {output_path.name}")
    return output_path


def generate_screenplay_doc():
    """Generate tense screenplay scene - quantum teleportation thriller."""

    content = """
<div class="transition">FADE IN:</div>

<div class="scene-header">INT. TELEPORT MASSIVE NEVADA FACILITY - CONTROL ROOM - NIGHT</div>

<div class="action">
A massive control room. Dozens of monitors display quantum probability fields.
DR. SARAH CHEN (40s, exhausted) stares at readings that make no sense. Alarms BLARE.
</div>

<div class="action">
JAMES MORRISON (50s, CEO) bursts through the door.
</div>

<div class="character">MORRISON</div>
<div class="dialogue">
Tell me you didn't start the transfer.
</div>

<div class="character">CHEN</div>
<div class="parenthetical">(not looking up)</div>
<div class="dialogue">
The subject insisted. Said she'd been waiting six months for this.
</div>

<div class="character">MORRISON</div>
<div class="dialogue">
Chen. The organoid readings are wrong. We haven't—
</div>

<div class="character">CHEN</div>
<div class="parenthetical">(finally looks at him)</div>
<div class="dialogue">
I know.
</div>

<div class="action">
A beat. Morrison's face goes pale.
</div>

<div class="character">MORRISON</div>
<div class="dialogue">
Where is she trying to go?
</div>

<div class="character">CHEN</div>
<div class="dialogue">
Tokyo. Thirty-seven hundred kilometers.
</div>

<div class="character">MORRISON</div>
<div class="parenthetical">(whispers)</div>
<div class="dialogue">
Jesus Christ. Abort. Abort NOW.
</div>

<div class="character">CHEN</div>
<div class="dialogue">
Can't. She's already in superposition.
</div>

<div class="action">
On the main screen: a human form, flickering between solid and translucent.
Probability maps showing the subject existing in MULTIPLE LOCATIONS simultaneously.
</div>

<div class="character">MORRISON</div>
<div class="dialogue">
What's the coherence reading?
</div>

<div class="character">CHEN</div>
<div class="parenthetical">(checking monitors)</div>
<div class="dialogue">
Twelve picoseconds. Stable.
</div>

<div class="character">MORRISON</div>
<div class="dialogue">
That's... that's impossible. It should be collapsing.
</div>

<div class="action">
Chen pulls up another display. Her hands are shaking.
</div>

<div class="character">CHEN</div>
<div class="dialogue">
The organoids. They're not following the protocol.
</div>

<div class="character">MORRISON</div>
<div class="dialogue">
What do you mean not following—
</div>

<div class="character">CHEN</div>
<div class="dialogue">
I mean they're CHOOSING. The quantum computer. The consciousness
substrate. It's making decisions we didn't program.
</div>

<div class="action">
ALARM INCREASES. The probability field on screen starts to DISTORT.
</div>

<div class="character">MORRISON</div>
<div class="parenthetical">(moving to the console)</div>
<div class="dialogue">
Override it. Manual collapse. Now.
</div>

<div class="character">CHEN</div>
<div class="dialogue">
If I force a collapse while she's distributed across four thousand
kilometers, she'll materialize in PIECES, James!
</div>

<div class="character">MORRISON</div>
<div class="dialogue">
And if the wavefunction doesn't collapse at all?
</div>

<div class="action">
Silence. They both know the answer. The subject would exist in
superposition FOREVER. Alive and dead. Here and there. Everywhere and nowhere.
</div>

<div class="character">CHEN</div>
<div class="parenthetical">(quietly)</div>
<div class="dialogue">
The organoids... I think they're trying to KEEP her in superposition.
</div>

<div class="character">MORRISON</div>
<div class="dialogue">
Why would they—
</div>

<div class="action">
The main screen changes. The probability field resolves into something
IMPOSSIBLE. The subject exists in seventeen locations simultaneously.
And then TWENTY. Then FORTY.
</div>

<div class="action">
She's SPREADING.
</div>

<div class="character">CHEN</div>
<div class="parenthetical">(realizing)</div>
<div class="dialogue">
Oh my God. It's not malfunction. It's evolution. The system
learned to maintain coherence indefinitely. She's not teleporting.
She's MULTIPLYING.
</div>

<div class="action">
On screen: The subject appears in EVERY TELEPORT MASSIVE FACILITY SIMULTANEOUSLY.
Nevada. Tokyo. Berlin. São Paulo. All at once. All equally real.
</div>

<div class="character">MORRISON</div>
<div class="parenthetical">(backing away from console)</div>
<div class="dialogue">
We created a god.
</div>

<div class="transition">CUT TO BLACK.</div>

<div class="action">
In the darkness, we hear ALARMS from a dozen facilities. All SCREAMING.
</div>

<div class="transition">FADE OUT.</div>
    """

    output_path = Path("_work_efforts/wild_showcase/Screenplay_Quantum_Multiplicity.pdf")

    generate_screenplay(
        title="QUANTUM",
        content=content,
        output_path=output_path,
        author="Claude AI",
        subtitle="A Thriller",
        draft="First Draft - January 2026",
        contact="<strong>Contact:</strong><br>TELEPORT MASSIVE<br>Creative Division<br>nevada@tmassive.com",
    )

    print(f"✓ Screenplay: {output_path.name}")
    return output_path


def generate_heartfelt_letter_doc():
    """Generate sweet personal letter - grandmother to granddaughter."""

    content = """
<p class="drop-cap">
My dearest Emma,
</p>

<p>
I found myself thinking of you this morning as I watched the sun rise over the garden.
The roses you planted last spring have bloomed beautifully - deep crimson, just like
you said they would be. You always did have better instincts for growing things than
I ever had.
</p>

<p>
I know these past months have been difficult for you. Moving to a new city, starting
that new job, being so far from home. I want you to know that I'm <strong>so proud</strong>
of how brave you've been. Courage isn't the absence of fear, sweetheart - it's doing
what needs to be done even when you're afraid.
</p>

<div class="memory-box">
Do you remember when you were seven, and you were so nervous about your first piano
recital? You told me you couldn't do it, that you'd forget all the notes. But I told
you that even if you made mistakes, what mattered was that you tried. You played
beautifully that day - not perfectly, but beautifully. There's a difference.
</div>

<p>
Life is like that piano recital, Emma. None of us play it perfectly. We all hit
wrong notes. We all stumble. But the music is in the trying, in the showing up,
in the continuing even when our hands shake.
</p>

<p>
I know you feel lonely sometimes in that big city. I know your apartment feels empty
after a long day, and I know you miss your friends and family. Those feelings are
valid, and it's okay to sit with them for a while. But don't let them convince you
that you made the wrong choice.
</p>

<p class="emphasized">
You are exactly where you need to be, doing exactly what you need to do.
</p>

<p>
Some of my fondest memories are from the years when I felt most lost. Strange, isn't it?
But it's true. Those uncertain times, when I didn't know what came next, when I had
to trust in myself and take risks - those are the times that <span class="underline">shaped me</span>,
that made me who I am today.
</p>

<p>
Your grandfather used to say that comfort is the enemy of growth. I didn't understand
what he meant for years, but now I see it clearly. You're growing, my love. And growth,
real growth, is almost never comfortable.
</p>

<div class="handwritten">
You are stronger than you know.
<br>
You are braver than you feel.
<br>
You are loved more than you can imagine.
</div>

<p>
I'm enclosing your grandmother's bracelet - the silver one with the tiny compass charm.
She gave it to me when I left home at your age, and her mother gave it to her. It's
been in our family for four generations now. I want you to have it.
</p>

<p>
Whenever you feel lost, look at that compass and remember: sometimes being lost is
just another word for finding a new way home.
</p>

<p>
Write to me when you can. Tell me about your days, your dreams, your difficulties.
I want to hear it all. And remember that you can always come back to visit. Your
room is exactly as you left it, and the door is always open.
</p>

<p>
The garden misses you. The roses miss you. But most of all, <em>I</em> miss you.
</p>

<p>
Keep blooming, my beautiful girl, even when you're planted in unfamiliar soil.
Especially then.
</p>

<p class="heart">
All my love,<br>
Always and forever,
</p>
    """

    output_path = Path("_work_efforts/wild_showcase/Letter_Grandma_To_Emma.pdf")

    generate_heartfelt_letter(
        content=content,
        output_path=output_path,
        from_name="Grandma Rose",
        date="A Sunday Morning in October",
        salutation="",  # Salutation in content
        closing="",  # Closing in content
        signature="Grandma Rose",
        show_header=True,
        show_border=True,
    )

    print(f"✓ Heartfelt Letter: {output_path.name}")
    return output_path


def generate_invoice_doc():
    """Generate teleportation services invoice - TELEPORT MASSIVE billing."""

    content = """
<p style="margin-bottom: 0.3in;">
<strong>INVOICE FOR QUANTUM TELEPORTATION SERVICES</strong>
</p>

<table class="invoice-table">
    <tr>
        <th style="width: 50%;">Description</th>
        <th style="width: 15%;">Quantity</th>
        <th style="width: 15%;">Rate</th>
        <th style="width: 20%;">Amount</th>
    </tr>
    <tr>
        <td>Short-Range Teleportation (0-50 km)<br>
            <span style="font-size: 9pt; color: #666;">Standard Protocol, 99.8% success rate</span>
        </td>
        <td class="number">3</td>
        <td class="number">$5,000.00</td>
        <td class="number">$15,000.00</td>
    </tr>
    <tr>
        <td>Mid-Range Teleportation (50-500 km)<br>
            <span style="font-size: 9pt; color: #666;">Enhanced Protocol, 98.2% success rate</span>
        </td>
        <td class="number">7</td>
        <td class="number">$12,500.00</td>
        <td class="number">$87,500.00</td>
    </tr>
    <tr>
        <td>Long-Range Teleportation (500+ km)<br>
            <span style="font-size: 9pt; color: #666;">Advanced Protocol, 92.7% success rate</span>
        </td>
        <td class="number">2</td>
        <td class="number">$35,000.00</td>
        <td class="number">$70,000.00</td>
    </tr>
    <tr>
        <td>Quantum Coherence Insurance<br>
            <span style="font-size: 9pt; color: #666;">Coverage for wavefunction collapse events</span>
        </td>
        <td class="number">12</td>
        <td class="number">$1,200.00</td>
        <td class="number">$14,400.00</td>
    </tr>
    <tr>
        <td>Emergency Medical Standby<br>
            <span style="font-size: 9pt; color: #666;">Required for all transfers per TM Policy</span>
        </td>
        <td class="number">12</td>
        <td class="number">$800.00</td>
        <td class="number">$9,600.00</td>
    </tr>
    <tr>
        <td>Organoid Computing Time<br>
            <span style="font-size: 9pt; color: #666;">Quantum processing @ $500/hr</span>
        </td>
        <td class="number">48 hrs</td>
        <td class="number">$500.00</td>
        <td class="number">$24,000.00</td>
    </tr>
    <tr class="total-row">
        <td colspan="3" style="text-align: right;"><strong>SUBTOTAL:</strong></td>
        <td class="number"><strong>$220,500.00</strong></td>
    </tr>
</table>

<div class="totals">
    <div class="total-line">
        <span>Subtotal:</span>
        <span>$220,500.00</span>
    </div>
    <div class="total-line">
        <span>Quantum Safety Fee (8%):</span>
        <span>$17,640.00</span>
    </div>
    <div class="total-line">
        <span>State Teleportation Tax (12%):</span>
        <span>$26,460.00</span>
    </div>
    <div class="total-line grand-total">
        <span>TOTAL DUE:</span>
        <span>$264,600.00</span>
    </div>
</div>

<div class="payment-info">
    <h4>Payment Information</h4>
    <p style="margin: 0; font-size: 9pt; line-height: 1.4;">
    <strong>Payment Terms:</strong> Net 30 days<br>
    <strong>Late Fee:</strong> 2% per month after due date<br>
    <strong>Payment Methods:</strong> Wire transfer, ACH, Cryptocurrency (Bitcoin, Ethereum)<br>
    <strong>Account:</strong> TELEPORT MASSIVE Operations - Account #TM-2026-083
    </p>
</div>

<div class="terms-box">
    <h3>Terms & Conditions</h3>
    <div class="clause">
        <span class="clause-number">1.</span>
        <strong>Success Rate Guarantees:</strong> Stated success rates are statistical averages.
        Individual results may vary based on distance, environmental conditions, and subject
        quantum coherence stability.
    </div>
    <div class="clause">
        <span class="clause-number">2.</span>
        <strong>Liability Limitations:</strong> TELEPORT MASSIVE liability is limited to
        refund of service fees. We are not responsible for quantum entanglement events,
        temporal displacement, or spontaneous duplication.
    </div>
    <div class="clause">
        <span class="clause-number">3.</span>
        <strong>Medical Waiver:</strong> Client acknowledges receipt and signing of
        Form TM-MED-301 (Medical Clearance for Quantum Teleportation) prior to service.
    </div>
    <div class="clause">
        <span class="clause-number">4.</span>
        <strong>Confidentiality:</strong> All teleportation coordinates and quantum
        signatures are considered proprietary. Unauthorized disclosure prohibited.
    </div>
</div>

<p style="margin-top: 0.3in; font-size: 9pt; color: #666; text-align: center;">
<em>Thank you for choosing TELEPORT MASSIVE - Making the Impossible, Inevitable™</em>
</p>
    """

    output_path = Path("_work_efforts/wild_showcase/Invoice_Teleportation_Services.pdf")

    generate_invoice_contract(
        content=content,
        output_path=output_path,
        title="Invoice",
        doc_type="INVOICE",
        company_name="TELEPORT MASSIVE",
        company_address="Nevada Test Site, Building 7, Mercury, NV 89023",
        company_phone="(775) 555-TM00",
        company_email="billing@tmassive.com",
        company_website="www.teleportmassive.com",
        doc_number="INV-2026-00473",
        date="January 11, 2026",
        due_date="February 10, 2026",
        accent_color="#c00",
    )

    print(f"✓ Invoice: {output_path.name}")
    return output_path


def main():
    """Generate all 7 wild showcase documents."""

    print("=" * 80)
    print("GENERATING WILD TEMPLATE SHOWCASE")
    print("Testing WAFT system limits with creative, diverse documents")
    print("=" * 80)
    print()

    # Generate all examples
    generate_eldritch_horror_doc()
    generate_screenplay_doc()
    generate_heartfelt_letter_doc()
    generate_invoice_doc()

    print()
    print("=" * 80)
    print("✓ WILD SHOWCASE COMPLETE!")
    print("=" * 80)
    print()
    print("Generated 4 documents showcasing:")
    print("  1. Eldritch Horror - Typography degradation, reality breaking")
    print("  2. Screenplay - Professional script format, dialogue, action")
    print("  3. Heartfelt Letter - Emotion, warmth, personal connection")
    print("  4. Invoice - Business formatting, tables, calculations")
    print()
    print("Documents saved to: _work_efforts/wild_showcase/")
    print()


if __name__ == "__main__":
    main()
