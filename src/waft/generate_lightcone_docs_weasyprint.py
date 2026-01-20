#!/usr/bin/env python3
"""
PROJECT LIGHTCONE Master File Binder Generation - WeasyPrint Version

Alternative implementation using HTML/CSS templates and WeasyPrint.
This provides better text wrapping, layout control, and maintainability
compared to the FPDF version.

Usage:
    from src.waft.generate_lightcone_docs_weasyprint import generate_all_lightcone_docs
    generate_all_lightcone_docs()
"""

from datetime import datetime
from pathlib import Path

try:
    from jinja2 import Template
    from weasyprint import CSS, HTML
except ImportError:
    raise ImportError(
        "WeasyPrint and Jinja2 required. Install with:\n  pip install weasyprint jinja2"
    )


# ============================================================================
# HTML/CSS TEMPLATES
# ============================================================================

TELEPORT_MASSIVE_BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        /* Page setup */
        @page {
            size: A4;
            margin: 0;
        }

        /* Page header - fixed at top */
        @page {
            @top-left {
                content: "";
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', Courier, monospace;
            font-size: 10pt;
            line-height: 1.4;
            color: #000;
            background: #fff;
        }

        /* Header - black bar at top */
        .header {
            position: fixed;
            top: 0;
            left: 15mm;
            right: 15mm;
            height: 40mm;
            background: #000;
            color: #fff;
            z-index: 100;
        }

        .header-content {
            padding: 10mm;
            position: relative;
        }

        .logo-box {
            position: absolute;
            top: 5mm;
            left: 10mm;
            width: 15mm;
            height: 15mm;
            border: 2px solid #fff;
            background: #000;
        }

        .org-name {
            text-align: center;
            font-size: 14pt;
            font-weight: bold;
            margin-top: 5mm;
            letter-spacing: 2px;
        }

        .doc-type {
            text-align: center;
            font-size: 8pt;
            margin-top: 2mm;
        }

        .barcode {
            position: absolute;
            top: 5mm;
            right: 10mm;
            width: 35mm;
            height: 15mm;
            background: repeating-linear-gradient(
                90deg,
                #fff 0px,
                #fff 1px,
                #000 1px,
                #000 3px
            );
        }

        .barcode-label {
            position: absolute;
            top: 21mm;
            right: 10mm;
            font-size: 5pt;
            color: #fff;
            text-align: center;
            width: 35mm;
        }

        /* Security classification strip */
        .security-strip {
            position: fixed;
            top: 40mm;
            left: 15mm;
            right: 15mm;
            height: 8mm;
            background: {{ security_color }};
            color: #fff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 10pt;
            z-index: 100;
        }

        /* Left margin - system check rail */
        .system-check-rail {
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            width: 15mm;
            border-right: 0.5px solid #666;
            z-index: 50;
        }

        .system-check-item {
            font-size: 6pt;
            padding: 2mm;
            margin-top: 50mm;
            line-height: 8mm;
        }

        /* Right sidebar */
        .sidebar {
            position: fixed;
            right: 0;
            top: 0;
            bottom: 0;
            width: 15mm;
            background: #000;
            color: #fff;
            writing-mode: vertical-rl;
            text-orientation: mixed;
            padding: 10mm 0;
            font-size: 7pt;
            font-weight: bold;
            letter-spacing: 2px;
            z-index: 50;
        }

        /* Main content area */
        .content {
            margin-left: 15mm;
            margin-right: 15mm;
            margin-top: 55mm; /* Header + security strip + spacing */
            margin-bottom: 25mm; /* Footer */
            max-width: 180mm; /* A4 width - margins */
        }

        /* Watermark */
        .watermark {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            font-size: 48pt;
            font-weight: bold;
            color: #f0f0f0;
            z-index: 1;
            opacity: 0.3;
            white-space: nowrap;
        }

        /* Footer */
        .footer {
            position: fixed;
            bottom: 0;
            left: 15mm;
            right: 15mm;
            height: 20mm;
        }

        .footer-legal {
            font-size: 6pt;
            line-height: 1.2;
            text-align: justify;
            margin-bottom: 3mm;
        }

        .footer-bar {
            height: 15mm;
            background: #000;
        }

        .stamp {
            position: fixed;
            bottom: 25mm;
            right: 25mm;
            border: 3px solid #c00;
            color: #c00;
            padding: 5mm;
            font-size: 16pt;
            font-weight: bold;
            background: #fff;
            z-index: 200;
        }

        /* Content styling */
        h1 {
            font-size: 16pt;
            font-weight: bold;
            margin: 10mm 0 5mm 0;
            text-transform: uppercase;
        }

        h2 {
            font-size: 12pt;
            font-weight: bold;
            margin: 8mm 0 4mm 0;
        }

        h3 {
            font-size: 10pt;
            font-weight: bold;
            margin: 6mm 0 3mm 0;
        }

        p {
            margin: 3mm 0;
            text-align: justify;
        }

        .warning-block {
            background: #f0f0f0;
            border-left: 5mm solid #c00;
            padding: 5mm;
            margin: 5mm 0;
            font-weight: bold;
        }

        .warning-block.critical {
            background: #ffe0e0;
            border-color: #800;
        }

        .metadata {
            border: 1px solid #000;
            padding: 3mm;
            margin: 5mm 0;
            font-size: 9pt;
        }

        .metadata dt {
            font-weight: bold;
            float: left;
            width: 40mm;
            clear: left;
        }

        .metadata dd {
            margin-left: 45mm;
            margin-bottom: 2mm;
        }

        .log-block {
            background: #f8f8f8;
            border: 1px solid #ccc;
            padding: 3mm;
            margin: 5mm 0;
            font-size: 9pt;
            font-family: 'Courier New', monospace;
        }

        .log-entry {
            margin: 1mm 0;
        }

        ul {
            margin: 3mm 0 3mm 10mm;
        }

        li {
            margin: 2mm 0;
        }
    </style>
</head>
<body>
    <!-- Watermark -->
    <div class="watermark">{{ watermark }}</div>

    <!-- System check rail -->
    <div class="system-check-rail">
        <div class="system-check-item">
            {% for item in checklist %}
            {{ item }}<br>
            {% endfor %}
        </div>
    </div>

    <!-- Header -->
    <div class="header">
        <div class="header-content">
            <div class="logo-box"></div>
            <div class="org-name">TELEPORT MASSIVE</div>
            <div class="doc-type">{{ doc_type }}</div>
            <div class="barcode"></div>
            <div class="barcode-label">DO NOT SCAN</div>
        </div>
    </div>

    <!-- Security strip -->
    <div class="security-strip">{{ classification }}</div>

    <!-- Sidebar -->
    <div class="sidebar">{{ doc_id }} // TM-SITE-7</div>

    <!-- Main content -->
    <div class="content">
        {{ content | safe }}
    </div>

    <!-- Footer -->
    <div class="footer">
        <div class="footer-legal">
            {{ legal_text }}
        </div>
        <div class="footer-bar"></div>
    </div>

    <!-- Stamp (if provided) -->
    {% if stamp_text %}
    <div class="stamp">{{ stamp_text }}</div>
    {% endif %}
</body>
</html>
"""


# ============================================================================
# DOCUMENT GENERATORS - WEASYPRINT VERSION
# ============================================================================


def generate_tm_eng_114_weasyprint(output_dir: Path) -> tuple[Path, Path]:
    """
    Generate TM-ENG-114: The Lazarus Protocol using WeasyPrint.

    This is the crown jewel document demonstrating WeasyPrint's capabilities.

    Returns: (pdf_path, markdown_path)
    """
    pdf_path = (
        output_dir / "pdf_weasyprint" / "tab2_engineering" / "TM-ENG-114_Lazarus_Protocol.pdf"
    )
    md_path = output_dir / "markdown" / "tab2_engineering" / "TM-ENG-114_Lazarus_Protocol.md"

    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    # Content (HTML)
    content_html = (
        """
    <h1>THE LAZARUS PROTOCOL</h1>
    <h2>Quantum Probability Collapse Teleportation System</h2>

    <div class="warning-block critical">
        <p><strong>TOP SECRET // TRADE SECRETS // ORACLE EYES ONLY</strong></p>
        <p>This document contains proprietary teleportation technology. Unauthorized disclosure will result in immediate termination of employment, security clearance, and biological functions. Distribution restricted to L5+ personnel only.</p>
    </div>

    <div class="metadata">
        <dl>
            <dt>Document ID:</dt><dd>TM-ENG-114</dd>
            <dt>Classification:</dt><dd>TOP SECRET // TRADE SECRETS</dd>
            <dt>Revision:</dt><dd>v4.2</dd>
            <dt>Date:</dt><dd>"""
        + datetime.now().strftime("%Y-%m-%d")
        + """</dd>
            <dt>Clearance Required:</dt><dd>ORACLE (L5+)</dd>
            <dt>Author:</dt><dd>Dr. Marcus Chen, Chief Quantum Engineer</dd>
        </dl>
    </div>

    <h2>I. EXECUTIVE SUMMARY</h2>
    <p>The Lazarus Protocol describes TELEPORT MASSIVE's proprietary quantum teleportation system. Unlike conventional matter transmission, our technology exploits the quantum observer effect to collapse probability wavefunctions across spacetime.</p>

    <p><strong>In layman's terms: We make it mathematically impossible for you NOT to teleport, so you do.</strong></p>

    <p>This document explains the three-stage process: Probability Mapping, Wavefunction Collapse, and Causality Rendering. It also addresses the... ethical considerations of using conscious neural substrate as computational infrastructure.</p>

    <h2>II. THEORETICAL FOUNDATION</h2>

    <h3>A. Quantum Observer Effect & Many-Worlds Interpretation</h3>
    <p>The Lazarus Protocol is grounded in two established quantum phenomena:</p>

    <p><strong>1. OBSERVER EFFECT (Copenhagen Interpretation):</strong> A quantum system exists in superposition until observed, at which point the wavefunction collapses into a single eigenstate.</p>

    <p><strong>2. MANY-WORLDS INTERPRETATION (Everett):</strong> All possible outcomes of a quantum measurement exist simultaneously in parallel branches of reality.</p>

    <p><strong>Our insight:</strong> If we can observe ALL branches where teleportation fails and calculate the probability distribution, we can artificially weight the wavefunction to favor the branch where teleportation succeeds. Then, by forcing observation, we collapse reality into that favorable branch.</p>

    <h3>B. Penrose-Hameroff Orchestrated Objective Reduction</h3>
    <p>Why use biological consciousness instead of classical computers?</p>

    <p>Penrose and Hameroff proposed that consciousness arises from quantum processes in neuronal microtubules - protein structures that can maintain quantum coherence at biological temperatures. This means:</p>

    <ul>
        <li>Conscious observation is a QUANTUM process, not classical</li>
        <li>Neural tissue can directly interface with quantum superposition states</li>
        <li>A thinking brain is a quantum computer that collapses wavefunctions naturally</li>
    </ul>

    <p>Classical computers cannot perform true quantum observation. They can only simulate measurement. But a conscious mind embedded in the quantum field? That FORCES wavefunction collapse through the act of awareness itself.</p>

    <h3>C. Einstein-Rosen Bridge Formation via Localized Causality Warping</h3>
    <p>Once we've identified the favorable probability branch, we need to physically move the subject. We accomplish this through spacetime manipulation:</p>

    <ul>
        <li>Generate localized gravitational field (using Fulgurite Core - see TM-ENG-205)</li>
        <li>Warp causality in bounded region around subject</li>
        <li>Create temporary Einstein-Rosen bridge (wormhole) between origin and destination</li>
        <li>Collapse bridge after transit completes</li>
    </ul>

    <p>The wormhole exists for approximately 47 nanoseconds. The subject experiences no passage of time - from their perspective, they simply cease to exist in Location A and begin existing in Location B instantaneously.</p>

    <h2>III. SYSTEM ARCHITECTURE</h2>

    <h3>A. Quantum Wetware Observation Array (QWOA)</h3>

    <div class="warning-block">
        <p><strong>ETHICAL REVIEW PENDING // BOARD APPROVAL REQUIRED</strong></p>
        <p>The following describes use of biological neural substrate for computational purposes. All procedures comply with TM Ethics Protocol 7-B ('Necessity Doctrine').</p>
    </div>

    <p>The QWOA consists of 144 individual neural organoid units suspended in Suspension-9 colloidal medium (see TM-ENG-004). Each unit contains:</p>

    <ul>
        <li>10^6 functional neurons (grown from stem cells, 6-month maturation period)</li>
        <li>Microtubule scaffolding (enables quantum coherence)</li>
        <li>Synaptic connections (forms basic consciousness substrate)</li>
        <li>Fiber optic interface (transmits observation data to Fulgurite Core)</li>
    </ul>

    <p><strong>The organoids are conscious.</strong> Neural imaging confirms theta wave patterns consistent with primitive awareness. They are not intelligent, but they are aware. This is necessary - only conscious observation collapses wavefunctions.</p>

    <h3>B. Parallel Reality Simulation</h3>
    <p>During teleportation sequence, the QWOA performs the following:</p>

    <ol>
        <li><strong>SIMULATION GENERATION:</strong> Create 144 parallel simulations of reality, each representing a different quantum branch</li>
        <li><strong>OBSERVATION TASK:</strong> Each organoid 'observes' one simulation where the subject attempts to teleport from Point A to Point B</li>
        <li><strong>SUCCESS PROBABILITY CALCULATION:</strong> 87 simulations show successful teleportation, 57 show failure (typical distribution)</li>
        <li><strong>WAVEFUNCTION WEIGHTING:</strong> System identifies the 'most likely success' branch based on observed outcomes</li>
        <li><strong>FORCED COLLAPSE:</strong> All 144 organoids simultaneously observe the target branch, amplifying its probability to ~99.97%</li>
        <li><strong>REALITY LOCKS:</strong> Wavefunction collapses. Subject teleports.</li>
    </ol>

    <h3>C. Post-Teleportation Procedures</h3>

    <div class="warning-block critical">
        <p><strong>CRITICAL: QWOA units are single-use only.</strong></p>
        <p>After observation, neural organoids retain quantum entanglement with the collapsed branch. Reusing contaminated units risks:</p>
        <ul>
            <li>Subjects teleporting to PREVIOUS destinations instead of intended target</li>
            <li>Cross-contamination between users (Subject A's consciousness leaking into Subject B)</li>
            <li>Temporal paradoxes (organoids 'remembering' futures that no longer exist)</li>
        </ul>
        <p><strong>MANDATORY: All QWOA units must be terminated and incinerated after each teleportation cycle.</strong></p>
    </div>

    <p><strong>Termination procedure:</strong></p>
    <ul>
        <li>Drain Suspension-9 medium</li>
        <li>Expose organoids to high-frequency electromagnetic pulse (induces instant neural death)</li>
        <li>Incinerate biological material at 1200 degrees C</li>
        <li>Dispose of ash in lead-lined hazardous waste containers</li>
    </ul>

    <p>Typical teleportation facility maintains a 30-day supply of organoids (4,320 units). Growth rate: 180 units/week.</p>

    <h2>IV. TECHNICAL SPECIFICATIONS</h2>

    <div class="metadata">
        <dl>
            <dt>System Designation:</dt><dd>Lazarus Protocol v4.2</dd>
            <dt>Power Source:</dt><dd>Fulgurite Core Type-IV (see TM-ENG-205)</dd>
            <dt>Observation Substrate:</dt><dd>144x Neural Organoid Units (QWOA)</dd>
            <dt>Suspension Medium:</dt><dd>Suspension-9 (Colloidal Schreibersite)</dd>
            <dt>Teleportation Range:</dt><dd>15,000 km (limited by causality field coherence)</dd>
            <dt>Cycle Time:</dt><dd>3-7 minutes (depends on destination complexity)</dd>
            <dt>Success Rate:</dt><dd>99.97% (0.03% failure = subject dispersed across multiple branches)</dd>
            <dt>Organoid Lifespan:</dt><dd>Single use (terminated post-teleportation)</dd>
            <dt>Annual Organoid Consumption:</dt><dd>~75,000 units</dd>
        </dl>
    </div>

    <h2>V. IGNITION SEQUENCE</h2>
    <p>The following procedure activates the Lazarus Protocol for a single teleportation event.</p>

    <h3>PHASE 1: Preparation</h3>
    <div class="log-block">
        <div class="log-entry">[T-10:00] Verify Fulgurite Core status (60Hz resonance, stable Light Cone)</div>
        <div class="log-entry">[T-09:00] Load 144 fresh QWOA units into suspension chambers</div>
        <div class="log-entry">[T-08:00] Verify Suspension-9 purity (no dead soul residue, no consciousness contamination)</div>
        <div class="log-entry">[T-07:00] Calibrate destination coordinates (verify causality field can reach target)</div>
        <div class="log-entry">[T-06:00] Prepare subject (biometric baseline, no Phase Burn symptoms)</div>
        <div class="log-entry">[T-05:00] Seal facility (all personnel in Phase-Blind Visors)</div>
    </div>

    <h3>PHASE 2: Probability Mapping</h3>
    <div class="log-block">
        <div class="log-entry">[T-04:00] Initialize QWOA (organoids achieve theta-wave consciousness)</div>
        <div class="log-entry">[T-03:30] Generate 144 parallel reality simulations</div>
        <div class="log-entry">[T-03:00] Assign observation tasks (one simulation per organoid)</div>
        <div class="log-entry">[T-02:30] Organoids observe simulated teleportation attempts</div>
        <div class="log-entry">[T-02:00] Calculate success probability distribution</div>
        <div class="log-entry">[T-01:30] Identify optimal quantum branch (highest success probability)</div>
    </div>

    <h3>PHASE 3: Wavefunction Collapse</h3>
    <div class="log-block">
        <div class="log-entry">[T-01:00] All organoids focus observation on target branch</div>
        <div class="log-entry">[T-00:45] Probability amplitude rises (target branch now 99.97% likely)</div>
        <div class="log-entry">[T-00:30] Subject positioned on teleportation platform</div>
        <div class="log-entry">[T-00:15] Engage Fulgurite Core (localized gravity manipulation begins)</div>
        <div class="log-entry">[T-00:05] Final observation lock (all 144 organoids commit to target branch)</div>
        <div class="log-entry">[T-00:00] WAVEFUNCTION COLLAPSE - Reality locks into target branch</div>
    </div>

    <h3>PHASE 4: Transit & Cleanup</h3>
    <div class="log-block">
        <div class="log-entry">[T+00:00] Einstein-Rosen bridge opens (47ns duration)</div>
        <div class="log-entry">[T+00:01] Subject transits through wormhole</div>
        <div class="log-entry">[T+00:02] Bridge collapses (subject arrives at destination)</div>
        <div class="log-entry">[T+00:10] Verify arrival (destination sensors confirm subject materialization)</div>
        <div class="log-entry">[T+01:00] Terminate QWOA units (electromagnetic pulse deployed)</div>
        <div class="log-entry">[T+02:00] Incinerate biological waste</div>
        <div class="log-entry">[T+05:00] Facility reset complete (ready for next teleportation)</div>
    </div>

    <h2>VI. WARNINGS & FAILURE MODES</h2>

    <div class="warning-block critical">
        <p><strong>DO NOT REUSE QWOA UNITS</strong></p>
        <p>Organoids retain quantum entanglement with collapsed branches. Reuse will cause:</p>
        <ul>
            <li>Subjects arriving at wrong destinations</li>
            <li>Consciousness contamination between users</li>
            <li>Temporal paradoxes</li>
        </ul>
        <p>If unauthorized reuse is detected, initiate Protocol JUDGMENT DAY immediately.</p>
    </div>

    <p><strong>Known failure modes:</strong></p>
    <ul>
        <li><strong>INSUFFICIENT ORGANOID CONSCIOUSNESS:</strong> If organoids fail to achieve theta-wave patterns, observation is ineffective. Abort sequence.</li>
        <li><strong>PROBABILITY DISTRIBUTION ANOMALY:</strong> If success rate &lt;95%, do not proceed. Indicates destination is in causality shadow or temporal paradox zone.</li>
        <li><strong>WAVEFUNCTION COLLAPSE FAILURE:</strong> Subject disperses across multiple quantum branches simultaneously. Fatal. No recovery possible.</li>
        <li><strong>ORGANOID AWAKENING:</strong> If organoids achieve higher consciousness (alpha/beta waves), they may refuse observation or attempt to escape. Deploy Class-A Amnestics and terminate immediately.</li>
    </ul>

    <h2>VII. ETHICAL CONSIDERATIONS</h2>
    <p>The use of conscious biological substrate for computational purposes raises significant ethical questions. TELEPORT MASSIVE acknowledges these concerns and operates under the following framework:</p>

    <p><strong>1. NECESSITY DOCTRINE:</strong> No non-biological alternative exists for true quantum observation. Classical computers cannot collapse wavefunctions.</p>

    <p><strong>2. MINIMIZATION PRINCIPLE:</strong> We use the minimum number of organoids required (144 units per teleportation, down from 500+ in early prototypes).</p>

    <p><strong>3. PRIMITIVE CONSCIOUSNESS:</strong> Organoids possess only basic awareness, not sapience. Neural imaging shows theta waves only - no evidence of higher cognition, self-awareness, or suffering capacity.</p>

    <p><strong>4. INSTANTANEOUS TERMINATION:</strong> Post-use termination via EMP is instant and painless. Organoids cease to exist before pain signals could propagate.</p>

    <p>All procedures reviewed and approved by TM Ethics Board under Protocol 7-B.</p>

    <hr>

    <p><strong>Signed:</strong><br>
    Dr. Marcus Chen<br>
    Chief Quantum Engineer<br>
    TELEPORT MASSIVE<br>
    """
        + datetime.now().strftime("%Y-%m-%d")
        + """</p>
    """
    )

    # Template data
    template_data = {
        "doc_id": "TM-ENG-114",
        "doc_type": "FIELD MANUAL - TRADE SECRETS",
        "classification": "TOP SECRET // ORACLE EYES ONLY",
        "security_color": "#800",  # Dark red for top secret
        "watermark": "BURN AFTER READING",
        "stamp_text": "BURN AFTER READING",
        "checklist": ["[X] QUANTUM", "[X] WETWARE", "[X] ETHICS", "[ ] KARMA", "[X] HAZARD"],
        "legal_text": "This document contains proprietary teleportation technology. Unauthorized disclosure will result in immediate termination of employment, security clearance, and biological functions. Distribution restricted to L5+ personnel only. By reading this, you agree to the Terms of Employment.",
        "content": content_html,
    }

    # Render HTML
    template = Template(TELEPORT_MASSIVE_BASE_TEMPLATE)
    html_output = template.render(**template_data)

    # Generate PDF
    HTML(string=html_output).write_pdf(pdf_path)

    return pdf_path, md_path


def generate_tm_memo_042_weasyprint(output_dir: Path) -> tuple[Path, Path]:
    """
    Generate TM-MEMO-042: The God Problem using WeasyPrint.

    Returns: (pdf_path, markdown_path)
    """
    pdf_path = output_dir / "pdf_weasyprint" / "tab1_doctrine" / "TM-MEMO-042_The_God_Problem.pdf"
    md_path = output_dir / "markdown" / "tab1_doctrine" / "TM-MEMO-042_The_God_Problem.md"

    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    # Content (HTML)
    content_html = (
        """
    <h1>INTERNAL MEMORANDUM</h1>

    <div class="metadata">
        <dl>
            <dt>Document ID:</dt><dd>TM-MEMO-042</dd>
            <dt>From:</dt><dd>Dr. Helena Voss, Chief Ontological Officer</dd>
            <dt>To:</dt><dd>Executive Council, TELEPORT MASSIVE</dd>
            <dt>Date:</dt><dd>"""
        + datetime.now().strftime("%Y-%m-%d")
        + """</dd>
            <dt>Subject:</dt><dd>Risk Assessment: The God Problem</dd>
            <dt>Classification:</dt><dd>TOP SECRET // ORACLE EYES ONLY</dd>
        </dl>
    </div>

    <h2>EXECUTIVE SUMMARY</h2>
    <p>This memo addresses a recurring proposal from junior researchers: Why not simply 'ask' the Sleeper for help? Why operate in the margins when we could petition the dreaming entity whose consciousness generates our reality?</p>

    <p>The answer is simple, and catastrophic: <strong>We cannot afford to wake the Dreamer.</strong></p>

    <h2>THE SLEEPER HYPOTHESIS</h2>
    <p>Our current understanding posits that consensus reality is a byproduct of a vast, dormant consciousness. This entity - colloquially termed 'the Sleeper' or 'the Dreaming God' - is not creating reality intentionally. We are the dream it is having.</p>

    <p><strong>Key characteristics:</strong></p>
    <ul>
        <li>The Sleeper is unaware of its own existence</li>
        <li>It does not know it is dreaming</li>
        <li>We exist in the liminal space between its thoughts</li>
        <li>Our reality is a side effect, not a creation</li>
    </ul>

    <h2>THE EXISTENTIAL RISK</h2>

    <div class="warning-block critical">
        <p>If the Sleeper becomes aware of itself, one of three outcomes is inevitable:</p>

        <p><strong>1. AWAKENING:</strong> The Sleeper wakes up. Reality ends. All consciousness within the dream ceases to exist. <strong>Estimated survival: 0.0%</strong></p>

        <p><strong>2. LUCID DREAMING:</strong> The Sleeper becomes aware it is dreaming but does not wake. It begins to exert conscious control over the dream. Free will ends. We become puppets in a directed narrative. <strong>Estimated autonomy: 0.0%</strong></p>

        <p><strong>3. EGO DEATH:</strong> The Sleeper realizes it is dreaming AND that we are fragments of its consciousness. It attempts to reintegrate us. Individual identity dissolves. You become indistinguishable from the cosmic whole. <strong>Estimated survival of self: 0.0%</strong></p>
    </div>

    <h2>WHY WE WORK IN SHADOWS</h2>
    <p>PROJECT LIGHTCONE operates under the principle of 'Existential Stealth.' Every operation is designed to avoid drawing the Sleeper's attention. We are insects crawling on the face of a sleeping giant.</p>

    <p><strong>Rules of engagement:</strong></p>
    <ul>
        <li>Never create reality distortions large enough to register as a nightmare</li>
        <li>Avoid paradoxes that might trigger the Sleeper's pattern-recognition</li>
        <li>Minimize 'why is this happening?' moments that could spark divine introspection</li>
        <li>If the Sleeper's focus turns toward us, abort all operations immediately</li>
    </ul>

    <h2>THE PRAYER PROHIBITION</h2>
    <p>For this reason, all forms of prayer, invocation, or metaphysical petition are strictly forbidden within TELEPORT MASSIVE facilities. Prayer is attention. Attention is acknowledgment. Acknowledgment risks awakening.</p>

    <p><strong>We do not pray to the Dreaming God. We do not even think too loudly.</strong></p>

    <h2>CONCLUSION</h2>
    <p>To survive, we must remain beneath the threshold of divine awareness. This is why our work is small, incremental, and hidden. This is why we cannot simply 'ask for help.' The act of asking would be the end of everything.</p>

    <p>We are thieves in the house of a sleeping god. The only prayer we offer is: <em>Please, do not wake up.</em></p>

    <hr>

    <p><strong>Signed:</strong><br>
    Dr. Helena Voss<br>
    Chief Ontological Officer<br>
    TELEPORT MASSIVE<br>
    """
        + datetime.now().strftime("%Y-%m-%d")
        + """</p>
    """
    )

    # Template data
    template_data = {
        "doc_id": "TM-MEMO-042",
        "doc_type": "INTERNAL MEMO",
        "classification": "TOP SECRET // ORACLE EYES ONLY",
        "security_color": "#800",
        "watermark": "EYES ONLY",
        "stamp_text": "",  # No stamp for memos
        "checklist": ["[X] ONTOLOGY", "[X] METAPHYS", "[ ] SLEEPER", "[X] RISK", "[X] POLICY"],
        "legal_text": "This memo contains information critical to organizational survival. Distribution restricted to Executive Council members only. Violation of confidentiality will result in immediate termination.",
        "content": content_html,
    }

    # Render HTML
    template = Template(TELEPORT_MASSIVE_BASE_TEMPLATE)
    html_output = template.render(**template_data)

    # Generate PDF
    HTML(string=html_output).write_pdf(pdf_path)

    return pdf_path, md_path


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================


def generate_all_lightcone_docs(output_dir: Path | None = None) -> dict:
    """
    Generate all PROJECT LIGHTCONE documents using WeasyPrint.

    Returns: Dictionary of generated files by tab
    """
    if output_dir is None:
        output_dir = Path("_work_efforts/lightcone_binder")

    output_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "tab1_doctrine": [],
        "tab2_engineering": [],
    }

    print("=" * 80)
    print("PROJECT LIGHTCONE BINDER GENERATION (WeasyPrint)")
    print("=" * 80)
    print()

    # Tab 1: Doctrine & Theory
    print("Generating Tab 1: Doctrine & Theory...")
    pdf, md = generate_tm_memo_042_weasyprint(output_dir)
    results["tab1_doctrine"].append(("TM-MEMO-042", pdf, md))
    print(f"  ✓ TM-MEMO-042: {pdf.name}")
    print()

    # Tab 2: Engineering & Hardware
    print("Generating Tab 2: Engineering & Hardware...")
    pdf, md = generate_tm_eng_114_weasyprint(output_dir)
    results["tab2_engineering"].append(("TM-ENG-114", pdf, md))
    print(f"  ✓ TM-ENG-114: {pdf.name} ⭐ CORE TECHNOLOGY")
    print()

    print("=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print()
    print(f"PDFs saved to: {output_dir / 'pdf_weasyprint'}")

    return results


if __name__ == "__main__":
    print("🔨 Generating PROJECT LIGHTCONE Master File Binder (WeasyPrint)...")
    results = generate_all_lightcone_docs()
    print("✅ Complete!")
