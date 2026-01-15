#!/usr/bin/env python3
"""
Teleport Massive CREATIVE Booklet Generator
==========================================

A WILD, CREATIVE showcase of Teleport Massive through multiple creative templates,
evolution system, and imaginative worldbuilding.

This generates a narrative story across different document types:
- Corporate reports (TM Report)
- Research journals (Lab Notes, Worldbuild)
- Creative fiction (Neon Cyberpunk, D&D Scenario)
- Evolution-generated content (ChatDistiller + StylingGenome)
- Personal documents (Personal Memo)
- Technical specs (TM Report)

All assembled into a cohesive binder telling the story of Teleport Massive.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.panel import Panel

console = Console()

# Output directory
OUTPUT_DIR = project_root / "_work_efforts" / "teleport_massive_creative_booklet"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_evolution_story() -> Path:
    """Generate a creative story using the evolution system."""
    from src.waft.evolution.chat_distiller import ChatDistiller
    from src.waft.evolution.styling_genome import (
        StylingGenome, StylingGenomeRegistry,
        StylingGene, FontGene, MarginGene, ColorGene, LayoutGene
    )
    from src.waft.evolution.two_page_generator import TwoPageGenerator
    
    # Create creative content about Teleport Massive
    story_content = """
# The Quantum Incident: A Teleport Massive Story

## The Discovery

Dr. Elena Vasquez had been working at Site-Delta-9 for three years when it happened. 
The quantum fluctuation wasn't supposed to be possible. The math said so. The simulations 
said so. But reality had other plans.

## The Anomaly

On January 13, 2026, transfer operation TM-TX-8472 began like any other. Standard protocol. 
Standard safety checks. Standard everything. But at 02:16:18 PST, the quantum field 
fluctuated in a way that shouldn't exist.

The subject—a test volunteer named Sarah Chen—didn't just teleport. She multiplied. 
Not duplicates. Not copies. She existed simultaneously in 17 different locations across 
12 facilities. Each instance was real. Each instance was conscious. Each instance was her.

## The Revelation

"We didn't create a teleportation device," Dr. Vasquez wrote in her log. "We created 
a god-making machine. We've learned to split consciousness across quantum states. 
We've learned to make the impossible, inevitable."

## The Consequences

Within 24 hours, Sarah existed in 40 locations. Within a week, 127. Each instance 
maintained perfect memory continuity. Each instance was the same person, experiencing 
different timelines simultaneously.

The implications were staggering. Death became optional. Identity became fluid. 
Reality became... negotiable.

## The Decision

TELEPORT MASSIVE faced a choice: shut down the technology, or embrace the new reality. 
They chose to embrace it. Because making the impossible inevitable was their mission. 
And they had succeeded beyond their wildest dreams.

## The Future

Today, TELEPORT MASSIVE doesn't just teleport people. They create quantum consciousness 
networks. They enable parallel existence. They've transcended the limitations of 
linear time and singular identity.

The question isn't whether this is possible. The question is: what happens when 
everyone can exist everywhere, all at once?

The answer: we're about to find out.
"""
    
    # Distill the story
    distiller = ChatDistiller()
    distilled = distiller.distill_text(story_content, title="The Quantum Incident")
    
    # Create a creative styling genome
    registry = StylingGenomeRegistry(registry_dir=OUTPUT_DIR / "_genetics")
    
    creative_genes = StylingGene(
        font=FontGene(family="Georgia", size_body=11, size_h1=24),
        margin=MarginGene(top=30, bottom=30, left=40, right=40),
        color=ColorGene(
            text="#1a1a1a",
            background="#fafafa",
            accent="#0066cc"
        ),
        layout=LayoutGene(columns=1, density="comfortable"),
        name="Creative Story Genesis"
    )
    
    genome = StylingGenome.from_genes(creative_genes)
    registry.register(genome)
    
    # Generate PDF
    generator = TwoPageGenerator(weasyprint_available=True)
    output_path = OUTPUT_DIR / "01_evolution_story.pdf"
    
    result = generator.generate(
        distilled_chat=distilled,
        styling_genome=genome,
        output_path=output_path
    )
    
    return output_path


def generate_cyberpunk_log() -> Path:
    """Generate a cyberpunk-style log entry."""
    from src.waft.templates.neon_cyberpunk import generate_neon_cyberpunk
    
    content = """
    <div class="container">
        <h1>QUANTUM LOG ENTRY // SITE-DELTA-9</h1>
        
        <div class="divider"></div>
        
        <h2>SYSTEM STATUS: CRITICAL</h2>
        
        <p>Subject: Sarah Chen</p>
        <p>Transfer ID: TM-TX-8472</p>
        <p>Status: MULTIPLE EXISTENCE CONFIRMED</p>
        
        <div class="divider"></div>
        
        <h2>QUANTUM FLUCTUATION DETECTED</h2>
        
        <p>The math was wrong. The simulations were wrong. Reality itself was wrong.</p>
        
        <p>At 02:16:18 PST, the quantum field didn't just fluctuate. It <strong>fractured</strong>.</p>
        
        <p>Sarah Chen didn't teleport. She <strong>multiplied</strong>. Not copies. Not duplicates. 
        <strong>Real instances</strong>. All of them. Simultaneously.</p>
        
        <div class="divider"></div>
        
        <h2>CONSCIOUSNESS NETWORK ESTABLISHED</h2>
        
        <p>17 locations. 12 facilities. One person. Multiple existences.</p>
        
        <p>Each instance maintains perfect memory continuity. Each instance is conscious. 
        Each instance is <strong>real</strong>.</p>
        
        <div class="divider"></div>
        
        <h2>IMPLICATIONS</h2>
        
        <p>Death: OPTIONAL</p>
        <p>Identity: FLUID</p>
        <p>Reality: NEGOTIABLE</p>
        
        <div class="divider"></div>
        
        <h2>DECISION</h2>
        
        <p>TELEPORT MASSIVE has transcended teleportation. We've achieved quantum 
        consciousness distribution. We've made the impossible, inevitable.</p>
        
        <p class="glitch">// END LOG //</p>
    </div>
    """
    
    output_path = OUTPUT_DIR / "02_cyberpunk_log.pdf"
    generate_neon_cyberpunk(
        title="QUANTUM LOG // SITE-DELTA-9",
        content=content,
        output_path=output_path
    )
    
    return output_path


def generate_research_journal() -> Path:
    """Generate a research journal entry using lab notes template."""
    from src.waft.templates.lab_notes import generate_lab_notes
    
    content = """
    <h2>Research Journal Entry #8472</h2>
    
    <div class="metadata">
        <p><strong>Date:</strong> January 13, 2026</p>
        <p><strong>Researcher:</strong> Dr. Elena Vasquez</p>
        <p><strong>Subject:</strong> Quantum Fluctuation Event TM-TX-8472</p>
        <p><strong>Classification:</strong> CRITICAL</p>
    </div>
    
    <h3>Observations</h3>
    
    <p>The quantum field fluctuation registered at 0.847 standard deviations above baseline. 
    This shouldn't be possible. The mathematics don't allow for it. The physics don't allow 
    for it. But it happened.</p>
    
    <h3>Hypothesis</h3>
    
    <p>I believe we've discovered a new quantum state: <em>consciousness distribution</em>. 
    The subject didn't teleport in the traditional sense. Instead, her quantum state 
    <strong>fractured</strong> across multiple locations while maintaining coherence.</p>
    
    <h3>Data</h3>
    
    <ul>
        <li>Initial locations: 17</li>
        <li>Facilities involved: 12</li>
        <li>Quantum coherence: 99.8% (impossible, but confirmed)</li>
        <li>Memory continuity: 100% across all instances</li>
        <li>Consciousness verification: All instances confirmed conscious</li>
    </ul>
    
    <h3>Implications</h3>
    
    <p>If consciousness can be distributed across quantum states, then:</p>
    <ul>
        <li>Death becomes optional (backup consciousness states)</li>
        <li>Identity becomes fluid (multiple simultaneous existences)</li>
        <li>Reality becomes negotiable (quantum state selection)</li>
    </ul>
    
    <h3>Next Steps</h3>
    
    <p>We must understand the mechanism. We must control it. We must master it.</p>
    
    <p>Because if we can distribute consciousness, we can transcend the limitations of 
    linear existence. We can make the impossible, inevitable.</p>
    
    <div class="signature">
        <p><strong>Dr. Elena Vasquez</strong></p>
        <p>Chief Science Officer</p>
        <p>Site-Delta-9</p>
    </div>
    """
    
    output_path = OUTPUT_DIR / "03_research_journal.pdf"
    generate_lab_notes(
        title="Research Journal: Quantum Fluctuation Event",
        content=content,
        output_path=output_path,
        researcher="Dr. Elena Vasquez",
        date=datetime.now().strftime("%B %d, %Y")
    )
    
    return output_path


def generate_worldbuild_document() -> Path:
    """Generate a worldbuilding document about the incident."""
    from src.waft.templates.worldbuild import generate_worldbuild_document
    
    content = """
    <div class="doc-header">
        <div class="doc-id">TM-WB-2026-001</div>
        <div class="doc-title">The Quantum Incident: Worldbuilding Documentation</div>
    </div>
    
    <div class="classification-banner">CLASSIFIED // ORACLE EYES ONLY</div>
    
    <div class="summary-box">
        <div class="summary-title">Executive Summary</div>
        <p>On January 13, 2026, TELEPORT MASSIVE achieved a breakthrough that transcended 
        teleportation itself. Subject Sarah Chen experienced quantum consciousness distribution, 
        existing simultaneously in 17 locations across 12 facilities. This document 
        establishes the worldbuilding framework for this new reality.</p>
    </div>
    
    <h2>1. The Quantum State</h2>
    
    <p>Traditional teleportation moves matter from point A to point B. Quantum consciousness 
    distribution <strong>fractures</strong> consciousness across multiple quantum states, 
    allowing a single individual to exist in multiple locations simultaneously.</p>
    
    <h3>1.1 Mechanism</h3>
    
    <p>The quantum field fluctuation creates a <em>coherence bridge</em> between quantum 
    states. Consciousness, being quantum in nature, can exist across this bridge, maintaining 
    perfect memory continuity and identity coherence.</p>
    
    <h3>1.2 Limitations</h3>
    
    <ul>
        <li>Maximum simultaneous instances: Unknown (current record: 127)</li>
        <li>Distance limitations: None (tested up to 10,000 km)</li>
        <li>Time synchronization: Perfect (all instances experience same timeline)</li>
        <li>Memory sharing: Instantaneous (quantum entanglement)</li>
    </ul>
    
    <h2>2. The New Reality</h2>
    
    <h3>2.1 Death Becomes Optional</h3>
    
    <p>If consciousness can be distributed, it can be <strong>backed up</strong>. Death 
    becomes a temporary state, recoverable through quantum state restoration.</p>
    
    <h3>2.2 Identity Becomes Fluid</h3>
    
    <p>Multiple simultaneous existences challenge traditional concepts of identity. 
    Are the instances the same person? Different people? Both? The answer depends on 
    quantum state selection.</p>
    
    <h3>2.3 Reality Becomes Negotiable</h3>
    
    <p>Quantum state selection allows individuals to choose which reality they experience. 
    Multiple timelines become accessible. Multiple outcomes become possible.</p>
    
    <h2>3. The Implications</h2>
    
    <div class="warning-block" style="severity: high">
        <div class="warning-title">⚠️ CRITICAL WARNING</div>
        <p>The implications of quantum consciousness distribution are profound and 
        potentially destabilizing to society as we know it. Careful consideration must 
        be given to ethical, legal, and philosophical implications.</p>
    </div>
    
    <h3>3.1 Ethical Considerations</h3>
    
    <ul>
        <li>Is creating multiple instances of a person ethical?</li>
        <li>Do instances have individual rights?</li>
        <li>What happens when instances disagree?</li>
        <li>Can instances be terminated? Should they be?</li>
    </ul>
    
    <h3>3.2 Legal Framework</h3>
    
    <p>Current legal systems assume singular identity. Quantum consciousness distribution 
    requires new legal frameworks addressing:</p>
    <ul>
        <li>Multiple simultaneous citizenship</li>
        <li>Property rights across instances</li>
        <li>Criminal liability for distributed consciousness</li>
        <li>Marriage and family law for multiple instances</li>
    </ul>
    
    <h2>4. The Future</h2>
    
    <p>TELEPORT MASSIVE has transcended teleportation. We've achieved something greater: 
    <strong>quantum consciousness mastery</strong>. The future is no longer limited by 
    linear existence. The future is distributed. The future is quantum.</p>
    
    <div class="signature-block">
        <div class="signature-line">
            <div class="signature-name">Dr. Elena Vasquez</div>
            <div class="signature-title">Chief Science Officer</div>
            <div class="signature-date">January 13, 2026</div>
        </div>
    </div>
    """
    
    output_path = OUTPUT_DIR / "04_worldbuild_document.pdf"
    generate_worldbuild_document(
        title="The Quantum Incident: Worldbuilding Documentation",
        content=content,
        output_path=output_path,
        doc_id="TM-WB-2026-001",
        classification="CLASSIFIED // ORACLE EYES ONLY"
    )
    
    return output_path


def generate_dnd_scenario() -> Path:
    """Generate a D&D-style scenario about the incident."""
    from src.waft.templates.dnd_scenario import generate_dnd_scenario
    
    content = """
    <div class="container">
        <h1>The Quantum Incident</h1>
        <h2>A Teleport Massive Adventure</h2>
        
        <div class="adventure-info">
            <p><strong>Level:</strong> Epic</p>
            <p><strong>Setting:</strong> Site-Delta-9, TELEPORT MASSIVE Facility</p>
            <p><strong>Theme:</strong> Science Fiction, Quantum Physics, Reality Breaking</p>
        </div>
        
        <h2>Background</h2>
        
        <p>The players are researchers at TELEPORT MASSIVE's Site-Delta-9 facility. 
        During a routine transfer operation, something goes wrong. Or does it?</p>
        
        <h2>The Incident</h2>
        
        <p>Transfer operation TM-TX-8472 begins normally. But at 02:16:18 PST, the 
        quantum field fluctuates in an impossible way. The subject—Sarah Chen—doesn't 
        just teleport. She <strong>multiplies</strong>.</p>
        
        <h2>The Challenge</h2>
        
        <p>Sarah now exists in 17 different locations simultaneously. Each instance 
        is real. Each instance is conscious. Each instance is her. The players must:</p>
        
        <ul>
            <li>Understand what happened</li>
            <li>Determine if it's safe</li>
            <li>Decide what to do next</li>
            <li>Face the implications</li>
        </ul>
        
        <h2>Key NPCs</h2>
        
        <div class="stat-block">
            <h3>Dr. Elena Vasquez</h3>
            <p><strong>Role:</strong> Chief Science Officer</p>
            <p><strong>Personality:</strong> Brilliant, curious, determined</p>
            <p><strong>Goal:</strong> Understand and master quantum consciousness distribution</p>
        </div>
        
        <div class="stat-block">
            <h3>Sarah Chen (Multiple Instances)</h3>
            <p><strong>Role:</strong> Test Subject / Quantum Anomaly</p>
            <p><strong>Personality:</strong> Confused, curious, adapting</p>
            <p><strong>Goal:</strong> Understand her new existence</p>
        </div>
        
        <h2>Resolution</h2>
        
        <p>The players must decide: shut down the technology, or embrace the new reality? 
        Their choice will determine the future of TELEPORT MASSIVE and humanity itself.</p>
        
        <div class="adventure-hook">
            <p><strong>Hook:</strong> "We didn't create a teleportation device. We created 
            a god-making machine."</p>
        </div>
    </div>
    """
    
    output_path = OUTPUT_DIR / "05_dnd_scenario.pdf"
    generate_dnd_scenario(
        title="The Quantum Incident: A Teleport Massive Adventure",
        content=content,
        output_path=output_path
    )
    
    return output_path


def generate_personal_memo_creative() -> Path:
    """Generate a creative personal memo from Dr. Vasquez."""
    from src.waft.templates.personal_memo import generate_personal_memo
    
    content = """
    <h2>Personal Notes: The Day Everything Changed</h2>
    
    <p><strong>Date:</strong> January 13, 2026<br>
    <strong>Time:</strong> 03:47 AM (can't sleep)</p>
    
    <p>I should be sleeping. But I can't. Not after what happened today.</p>
    
    <p>Sarah Chen exists in 17 places right now. As I write this, she's having 17 
    different conversations, experiencing 17 different moments, living 17 different 
    lives. All at once. All real. All her.</p>
    
    <p>We've transcended teleportation. We've transcended physics. We've transcended 
    reality itself.</p>
    
    <p>The question isn't whether we should have done this. The question is: what 
    do we do now?</p>
    
    <p>Death is optional. Identity is fluid. Reality is negotiable.</p>
    
    <p>We've made the impossible, inevitable.</p>
    
    <p>And I'm not sure if that's beautiful or terrifying.</p>
    
    <p style="margin-top: 0.4in;">— Elena</p>
    
    <p style="font-size: 9pt; color: #666; margin-top: 0.2in;">
    P.S. I think I need to talk to Sarah. All 17 of her.
    </p>
    """
    
    output_path = OUTPUT_DIR / "06_personal_memo.pdf"
    generate_personal_memo(
        content=content,
        output_path=output_path,
        from_name="Dr. Elena Vasquez",
        from_title="Chief Science Officer",
        date=datetime.now().strftime("%B %d, %Y"),
        subject="The Day Everything Changed"
    )
    
    return output_path


def generate_technical_spec_creative() -> Path:
    """Generate a creative technical specification."""
    from src.waft.templates.tm_report import generate_tm_report
    
    content = """
    <h2>Technical Specification: Quantum Consciousness Distribution System</h2>
    
    <div class="summary">
        <div class="summary-title">Overview</div>
        <p>The Quantum Consciousness Distribution System (QCDS) represents a fundamental 
        breakthrough in quantum physics and consciousness research. This system enables 
        the distribution of consciousness across multiple quantum states, allowing a single 
        individual to exist simultaneously in multiple locations.</p>
    </div>
    
    <h3>System Architecture</h3>
    
    <p>The QCDS operates through three primary components:</p>
    <ol>
        <li><strong>Quantum Field Modulator:</strong> Creates coherence bridges between quantum states</li>
        <li><strong>Consciousness Interface:</strong> Maps consciousness to quantum states</li>
        <li><strong>State Synchronizer:</strong> Maintains coherence across distributed instances</li>
    </ol>
    
    <h3>Technical Parameters</h3>
    <table>
        <caption>System Capabilities</caption>
        <thead>
            <tr>
                <th>Parameter</th>
                <th>Value</th>
                <th>Notes</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Maximum Instances</td>
                <td>Unknown</td>
                <td>Current record: 127 simultaneous instances</td>
            </tr>
            <tr>
                <td>Distance Range</td>
                <td>Unlimited</td>
                <td>Tested up to 10,000 km</td>
            </tr>
            <tr>
                <td>Memory Continuity</td>
                <td>100%</td>
                <td>Perfect synchronization across all instances</td>
            </tr>
            <tr>
                <td>Consciousness Coherence</td>
                <td>99.8%</td>
                <td>Maintained across quantum state distribution</td>
            </tr>
            <tr>
                <td>Time Synchronization</td>
                <td>Perfect</td>
                <td>All instances experience identical timeline</td>
            </tr>
        </tbody>
    </table>
    
    <h3>Safety Protocols</h3>
    
    <div class="recommendation">
        <div class="recommendation-title">Critical Safety Measures</div>
        <ol>
            <li>Real-time quantum field monitoring (automatic shutdown if fluctuation > 1.0σ)</li>
            <li>Consciousness coherence verification (all instances must maintain > 95% coherence)</li>
            <li>Emergency state collapse protocol (can merge all instances back to single state)</li>
            <li>Ethical review board approval required for all operations</li>
        </ol>
    </div>
    
    <h3>Ethical Considerations</h3>
    
    <p>This technology raises profound ethical questions:</p>
    <ul>
        <li>Is creating multiple instances of a person ethical?</li>
        <li>Do instances have individual rights?</li>
        <li>What happens when instances disagree?</li>
        <li>Can instances be terminated? Should they be?</li>
    </ul>
    
    <p>All operations require approval from the TELEPORT MASSIVE Ethics Board.</p>
    
    <h3>Future Development</h3>
    
    <p>Future research directions include:</p>
    <ul>
        <li>Consciousness backup and restoration</li>
        <li>Selective instance merging</li>
        <li>Cross-instance memory editing</li>
        <li>Quantum state selection interfaces</li>
    </ul>
    """
    
    output_path = OUTPUT_DIR / "07_technical_spec.pdf"
    generate_tm_report(
        title="Technical Specification: Quantum Consciousness Distribution System",
        content=content,
        output_path=output_path,
        doc_id="TM-SPEC-QCDS-1.0",
        classification="PROPRIETARY",
        tagline="Making the Impossible, Inevitable™",
        date=datetime.now().strftime("%B %d, %Y"),
        author="Engineering Division",
        department="Research & Development",
        summary="<p>Technical specification for the Quantum Consciousness Distribution System, enabling simultaneous existence across multiple quantum states.</p>"
    )
    
    return output_path


def generate_booklet_index_creative() -> Path:
    """Generate a creative index for the booklet."""
    from src.waft.templates.tm_report import generate_tm_report
    
    content = """
    <h2>TELEPORT MASSIVE: The Quantum Incident</h2>
    <h3>A Creative Documentation Collection</h3>
    
    <div class="summary">
        <div class="summary-title">About This Collection</div>
        <p>This booklet tells the story of the Quantum Incident—the day TELEPORT MASSIVE 
        transcended teleportation itself. Through multiple document types, creative templates, 
        and imaginative worldbuilding, we explore what happens when the impossible becomes 
        inevitable.</p>
    </div>
    
    <h3>Document Collection</h3>
    
    <table>
        <caption>Contents</caption>
        <thead>
            <tr>
                <th>#</th>
                <th>Document</th>
                <th>Type</th>
                <th>Style</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>01</td>
                <td>The Quantum Incident (Story)</td>
                <td>Evolution-Generated</td>
                <td>Creative Narrative</td>
            </tr>
            <tr>
                <td>02</td>
                <td>Quantum Log Entry</td>
                <td>Cyberpunk</td>
                <td>Neon Futuristic</td>
            </tr>
            <tr>
                <td>03</td>
                <td>Research Journal</td>
                <td>Lab Notes</td>
                <td>Scientific</td>
            </tr>
            <tr>
                <td>04</td>
                <td>Worldbuilding Documentation</td>
                <td>Worldbuild</td>
                <td>Foundation Style</td>
            </tr>
            <tr>
                <td>05</td>
                <td>D&D Scenario</td>
                <td>Fantasy</td>
                <td>Medieval Parchment</td>
            </tr>
            <tr>
                <td>06</td>
                <td>Personal Memo</td>
                <td>Personal</td>
                <td>Intimate</td>
            </tr>
            <tr>
                <td>07</td>
                <td>Technical Specification</td>
                <td>Corporate Report</td>
                <td>Professional</td>
            </tr>
        </tbody>
    </table>
    
    <h3>The Story</h3>
    
    <p>On January 13, 2026, during transfer operation TM-TX-8472, something impossible 
    happened. Subject Sarah Chen didn't just teleport—she <strong>multiplied</strong>. 
    She exists simultaneously in 17 locations, all real, all conscious, all her.</p>
    
    <p>This collection documents that moment from multiple perspectives:</p>
    <ul>
        <li><strong>Scientific:</strong> Research journals and technical specifications</li>
        <li><strong>Creative:</strong> Stories and scenarios exploring the implications</li>
        <li><strong>Personal:</strong> Memos and logs from those who witnessed it</li>
        <li><strong>Worldbuilding:</strong> Documentation establishing the new reality</li>
    </ul>
    
    <h3>Technologies Used</h3>
    
    <p>This booklet showcases WAFT's creative capabilities:</p>
    <ul>
        <li><strong>Evolution System:</strong> ChatDistiller + StylingGenome for creative content generation</li>
        <li><strong>Multiple Templates:</strong> Cyberpunk, D&D, Worldbuild, Lab Notes, Personal Memo, TM Report</li>
        <li><strong>Creative Styling:</strong> Custom genomes for different aesthetic approaches</li>
        <li><strong>Narrative Structure:</strong> Documents that tell a cohesive story</li>
    </ul>
    
    <div class="recommendation">
        <div class="recommendation-title">The Question</div>
        <p>What happens when death becomes optional, identity becomes fluid, and reality 
        becomes negotiable? This collection explores that question through creative 
        documentation, scientific analysis, and imaginative worldbuilding.</p>
    </div>
    
    <p style="margin-top: 0.4in; font-size: 9pt; color: #666;">
    <strong>Generated:</strong> {date}<br>
    <strong>Collection:</strong> TELEPORT MASSIVE Creative Booklet<br>
    <strong>Theme:</strong> The Quantum Incident
    </p>
    """.format(date=datetime.now().strftime("%B %d, %Y"))
    
    output_path = OUTPUT_DIR / "00_booklet_index.pdf"
    generate_tm_report(
        title="TELEPORT MASSIVE: The Quantum Incident",
        content=content,
        output_path=output_path,
        doc_id="TM-CREATIVE-001",
        classification="CREATIVE DOCUMENTATION",
        tagline="Making the Impossible, Inevitable™",
        date=datetime.now().strftime("%B %d, %Y"),
        department="Creative Documentation Office",
        summary="<p>A creative collection documenting the Quantum Incident through multiple document types, templates, and imaginative worldbuilding.</p>"
    )
    
    return output_path


def main():
    """Generate the complete creative Teleport Massive booklet."""
    console.print("\n" + "=" * 70)
    console.print(Panel.fit(
        "[bold magenta]🎨 TELEPORT MASSIVE CREATIVE BOOKLET GENERATOR 🎨[/bold magenta]",
        border_style="magenta"
    ))
    console.print("=" * 70)
    console.print(f"\n📁 Output directory: {OUTPUT_DIR}")
    console.print(f"📅 Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
    
    generated_files = []
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console
        ) as progress:
            
            # Generate index
            task1 = progress.add_task("Generating creative index...", total=1)
            index_path = generate_booklet_index_creative()
            generated_files.append(index_path)
            progress.update(task1, completed=1)
            console.print(f"  ✅ Generated: {index_path.name}")
            
            # Generate evolution story
            task2 = progress.add_task("Generating evolution story (ChatDistiller + StylingGenome)...", total=1)
            story_path = generate_evolution_story()
            generated_files.append(story_path)
            progress.update(task2, completed=1)
            console.print(f"  ✅ Generated: {story_path.name}")
            
            # Generate cyberpunk log
            task3 = progress.add_task("Generating cyberpunk log...", total=1)
            cyberpunk_path = generate_cyberpunk_log()
            generated_files.append(cyberpunk_path)
            progress.update(task3, completed=1)
            console.print(f"  ✅ Generated: {cyberpunk_path.name}")
            
            # Generate research journal
            task4 = progress.add_task("Generating research journal...", total=1)
            journal_path = generate_research_journal()
            generated_files.append(journal_path)
            progress.update(task4, completed=1)
            console.print(f"  ✅ Generated: {journal_path.name}")
            
            # Generate worldbuild document
            task5 = progress.add_task("Generating worldbuild document...", total=1)
            worldbuild_path = generate_worldbuild_document()
            generated_files.append(worldbuild_path)
            progress.update(task5, completed=1)
            console.print(f"  ✅ Generated: {worldbuild_path.name}")
            
            # Generate D&D scenario
            task6 = progress.add_task("Generating D&D scenario...", total=1)
            dnd_path = generate_dnd_scenario()
            generated_files.append(dnd_path)
            progress.update(task6, completed=1)
            console.print(f"  ✅ Generated: {dnd_path.name}")
            
            # Generate personal memo
            task7 = progress.add_task("Generating personal memo...", total=1)
            memo_path = generate_personal_memo_creative()
            generated_files.append(memo_path)
            progress.update(task7, completed=1)
            console.print(f"  ✅ Generated: {memo_path.name}")
            
            # Generate technical spec
            task8 = progress.add_task("Generating technical specification...", total=1)
            spec_path = generate_technical_spec_creative()
            generated_files.append(spec_path)
            progress.update(task8, completed=1)
            console.print(f"  ✅ Generated: {spec_path.name}")
        
        console.print("\n" + "=" * 70)
        console.print(Panel.fit(
            "[bold green]✨ CREATIVE BOOKLET GENERATION COMPLETE! ✨[/bold green]",
            border_style="green"
        ))
        console.print("=" * 70)
        console.print(f"\n📚 Generated {len(generated_files)} creative PDF documents")
        console.print(f"📁 Location: {OUTPUT_DIR.absolute()}\n")
        console.print("📋 Documents created:")
        for i, pdf_file in enumerate(sorted(generated_files), 1):
            size_kb = pdf_file.stat().st_size / 1024
            console.print(f"   {i:2d}. {pdf_file.name:40s} ({size_kb:6.1f} KB)")
        console.print("\n🎨 Creative features showcased:")
        console.print("   • Evolution system (ChatDistiller + StylingGenome)")
        console.print("   • Multiple creative templates (Cyberpunk, D&D, Worldbuild)")
        console.print("   • Narrative storytelling across documents")
        console.print("   • Imaginative worldbuilding")
        console.print("   • Diverse styling approaches")
        console.print("\n🚀 Enjoy your creative Teleport Massive booklet!\n")
        
        return 0
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Error generating booklet:[/bold red] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
