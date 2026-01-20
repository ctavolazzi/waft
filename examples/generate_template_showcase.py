"""
Generate showcase documents for all WAFT templates.

This creates example documents demonstrating each template:
1. Field Guide - Operational manual
2. TM Report - Corporate report
3. Lab Notes - Research documentation
4. Personal Memo - Staff communication
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.templates.field_guide import generate_field_guide
from src.waft.templates.lab_notes import generate_lab_notes
from src.waft.templates.personal_memo import generate_personal_memo
from src.waft.templates.tm_report import generate_tm_report


def generate_field_guide_example():
    """Generate field guide example - Quantum Tunneling Survival Guide."""

    content = """
<h2>Introduction</h2>

<p>
This field guide provides essential protocols for personnel operating in
quantum-unstable environments. Quantum tunneling events can occur without
warning. Following these procedures may save your life.
</p>

<div class="warning">
    <div class="warning-title">Warning</div>
    Quantum tunneling can cause instantaneous molecular displacement.
    Never enter a quantum zone without proper containment equipment.
    Failure to follow safety protocols has resulted in 23 fatalities this year.
</div>

<h2>Equipment Checklist</h2>

<div class="checklist">
    <div class="checklist-title">Required Equipment</div>
    <ul>
        <li>Quantum Containment Suit (QCS-7 or newer)</li>
        <li>Wavefunction Stabilizer (calibrated within 24 hours)</li>
        <li>Emergency Beacon (fresh batteries)</li>
        <li>Entanglement Detector</li>
        <li>Reality Anchor Device</li>
        <li>Backup oxygen supply (minimum 6 hours)</li>
    </ul>
</div>

<h2>Pre-Entry Procedures</h2>

<div class="procedure">
    <div class="step">
        Don full quantum containment suit. Verify all seals are intact.
        Check pressure gauge reads green (15-20 PSI).
    </div>
    <div class="step">
        Activate wavefunction stabilizer. Wait for steady blue light.
        If light flickers or turns red, ABORT entry.
    </div>
    <div class="step">
        Test emergency beacon. Confirm signal reception by control room.
        Announce your entry time and expected duration.
    </div>
    <div class="step">
        Attach reality anchor to belt. Enable auto-stabilization mode.
        Device should emit faint humming sound.
    </div>
    <div class="step">
        Enter airlock. Wait for pressure equalization. Green light indicates
        safe to proceed into quantum zone.
    </div>
</div>

<h2>Quantum Tunneling Event Response</h2>

<h3>Recognition</h3>

<p>
You may be experiencing quantum tunneling if you observe:
</p>

<ul>
    <li>Objects phasing through solid barriers</li>
    <li>Duplicate versions of yourself in peripheral vision</li>
    <li>Sudden temperature fluctuations (±50°C)</li>
    <li>Gravitational anomalies (floating objects, inverted gravity)</li>
    <li>Time dilation effects (clock discrepancies > 5 seconds)</li>
</ul>

<div class="caution">
    <div class="caution-title">Caution</div>
    Do NOT attempt to interact with quantum duplicates. Observation
    collapses the wavefunction unpredictably.
</div>

<h3>Immediate Response</h3>

<div class="procedure">
    <div class="step">
        FREEZE. Do not move. Sudden movement can destabilize your quantum state.
    </div>
    <div class="step">
        Activate reality anchor emergency mode (red button). This consumes
        battery rapidly—use only in genuine emergencies.
    </div>
    <div class="step">
        Trigger emergency beacon. Control will attempt remote stabilization.
    </div>
    <div class="step">
        Close your eyes. Observation affects quantum states. Minimize
        sensory input until stabilization confirmed.
    </div>
    <div class="step">
        Wait for all-clear signal from control (three short beeps).
        Only then may you resume movement.
    </div>
</div>

<h2>Emergency Evacuation</h2>

<p>
Evacuate immediately if:
</p>

<ul>
    <li>Wavefunction stabilizer fails (red light or no light)</li>
    <li>Reality anchor battery below 20%</li>
    <li>Oxygen supply below 1 hour</li>
    <li>You experience "quantum sickness" (nausea, disorientation, seeing impossible colors)</li>
    <li>Control orders evacuation</li>
</ul>

<div class="warning">
    <div class="warning-title">Critical Warning</div>
    If you become partially tunneled (half your body phased through a wall),
    DO NOT PANIC. Remain calm. Control will dispatch rescue team with
    quantum extraction equipment. Movement will worsen your condition.
</div>

<h2>Common Hazards</h2>

<table>
    <caption>Table 1: Quantum Zone Hazard Reference</caption>
    <tr>
        <th>Hazard</th>
        <th>Severity</th>
        <th>Response</th>
    </tr>
    <tr>
        <td>Wavefunction Collapse</td>
        <td>CRITICAL</td>
        <td>Emergency anchor activation</td>
    </tr>
    <tr>
        <td>Entanglement Event</td>
        <td>HIGH</td>
        <td>Isolate affected personnel</td>
    </tr>
    <tr>
        <td>Time Dilation (< 1 min)</td>
        <td>MODERATE</td>
        <td>Recalibrate stabilizer</td>
    </tr>
    <tr>
        <td>Quantum Duplication</td>
        <td>HIGH</td>
        <td>Avoid observation, alert control</td>
    </tr>
    <tr>
        <td>Reality Fluctuation</td>
        <td>MODERATE</td>
        <td>Increase anchor power</td>
    </tr>
</table>

<h2>Post-Exposure Protocol</h2>

<p>
After exiting quantum zone:
</p>

<ul>
    <li>Report to medical immediately for quantum coherence scan</li>
    <li>Submit equipment for inspection and recalibration</li>
    <li>Complete incident report (even if uneventful)</li>
    <li>Mandatory 24-hour observation period before next entry</li>
</ul>

<div class="note">
    <div class="note-title">Note</div>
    Personnel experiencing persistent quantum effects (lingering duplicates,
    spontaneous tunneling, quantum dreams) must report to Dr. Vasquez in
    Medical immediately. These symptoms may indicate quantum contamination.
</div>

<h2>Contact Information</h2>

<p>
<strong>Emergency Hotline:</strong> Extension 911<br>
<strong>Quantum Safety Office:</strong> Dr. Michael Torres, ext. 2847<br>
<strong>Medical (Quantum Division):</strong> Dr. Elena Vasquez, ext. 3156<br>
<strong>Equipment Maintenance:</strong> Engineering Bay 7, ext. 5500
</p>

<div class="page-break"></div>

<h2>Appendix A: Equipment Specifications</h2>

<h3>Quantum Containment Suit QCS-7</h3>

<ul>
    <li><strong>Manufacturer:</strong> TELEPORT MASSIVE Defense Systems</li>
    <li><strong>Quantum Shielding:</strong> 99.7% wavefunction isolation</li>
    <li><strong>Operating Temperature:</strong> -200°C to +500°C</li>
    <li><strong>Pressure Rating:</strong> 0.001 to 100 atmospheres</li>
    <li><strong>Battery Life:</strong> 8 hours continuous use</li>
    <li><strong>Certification Required:</strong> QSO Level 3</li>
</ul>

<h3>Reality Anchor RA-3000</h3>

<ul>
    <li><strong>Function:</strong> Maintains quantum coherence in unstable fields</li>
    <li><strong>Range:</strong> 3 meter radius</li>
    <li><strong>Power Source:</strong> Quantum battery (6 month lifespan)</li>
    <li><strong>Emergency Mode:</strong> 300% power boost (15 minute duration)</li>
    <li><strong>Weight:</strong> 2.3 kg</li>
</ul>

<p style="margin-top: 0.5in; text-align: center; font-weight: bold;">
REMEMBER: Your survival depends on following these procedures.
</p>
    """

    output_path = Path("_work_efforts/showcase_documents/Field_Guide_Quantum_Tunneling.pdf")

    generate_field_guide(
        title="Quantum Tunneling Survival Guide",
        content=content,
        output_path=output_path,
        series="FIELD GUIDE",
        number="FG-QT-001",
        subtitle="Essential Protocols for Quantum-Unstable Environments",
        classification="RESTRICTED - L5+ PERSONNEL ONLY",
        issued_by="TELEPORT MASSIVE Quantum Safety Office",
        date="January 2026",
    )

    print(f"✓ Field Guide: {output_path.name}")
    return output_path


def generate_tm_report_example():
    """Generate TM report example - Quarterly teleportation analysis."""

    content = """
<h2>Overview</h2>

<p>
This report analyzes teleportation success rates for Q4 2025, comparing
performance across all active facilities. Key findings indicate significant
improvements in coherence stability but persistent challenges with long-distance
transfers exceeding 500 kilometers.
</p>

<h2>Methodology</h2>

<p>
Data was collected from all 12 TELEPORT MASSIVE facilities between October 1
and December 31, 2025. Success was defined as complete molecular reconstruction
with < 0.001% variance from baseline. Failures include partial transfers,
quantum entanglement errors, and wavefunction collapse events.
</p>

<h3>Facilities Included</h3>

<ul>
    <li>Nevada Test Site (Primary)</li>
    <li>Antarctic Research Station</li>
    <li>Orbital Platform Sigma</li>
    <li>Tokyo Facility</li>
    <li>Berlin Laboratory</li>
    <li>São Paulo Center</li>
    <li>Mumbai Operations</li>
    <li>Sydney Lab</li>
    <li>Cairo Station</li>
    <li>Moscow Complex</li>
    <li>Toronto Facility</li>
    <li>Cape Town Installation</li>
</ul>

<h2>Results</h2>

<h3>Overall Success Rates</h3>

<table>
    <caption>Table 1: Quarterly Success Rates by Distance</caption>
    <tr>
        <th>Distance Range</th>
        <th>Attempts</th>
        <th>Successes</th>
        <th>Success Rate</th>
        <th>Change from Q3</th>
    </tr>
    <tr>
        <td>0-10 km</td>
        <td>1,247</td>
        <td>1,242</td>
        <td>99.6%</td>
        <td>+0.3%</td>
    </tr>
    <tr>
        <td>10-50 km</td>
        <td>892</td>
        <td>881</td>
        <td>98.8%</td>
        <td>+1.2%</td>
    </tr>
    <tr>
        <td>50-100 km</td>
        <td>634</td>
        <td>612</td>
        <td>96.5%</td>
        <td>+2.1%</td>
    </tr>
    <tr>
        <td>100-500 km</td>
        <td>423</td>
        <td>389</td>
        <td>92.0%</td>
        <td>+3.5%</td>
    </tr>
    <tr>
        <td>> 500 km</td>
        <td>156</td>
        <td>118</td>
        <td>75.6%</td>
        <td>-1.2%</td>
    </tr>
</table>

<h3>Key Findings</h3>

<p>
<strong>1. Short-range performance remains excellent.</strong> Local transfers
(< 10 km) achieved 99.6% success, with only 5 failures attributable to
equipment malfunction rather than theoretical limitations.
</p>

<p>
<strong>2. Mid-range improvements significant.</strong> Success rates for
100-500 km transfers improved 3.5 percentage points, likely due to upgraded
Lazarus Protocol algorithms implemented in November.
</p>

<p>
<strong>3. Long-range challenges persist.</strong> Transfers exceeding 500 km
showed decreased performance (-1.2%). Investigation reveals quantum decoherence
in transit remains the primary failure mode.
</p>

<h2>Failure Analysis</h2>

<h3>Failure Modes by Category</h3>

<table>
    <caption>Table 2: Failure Classification</caption>
    <tr>
        <th>Failure Type</th>
        <th>Occurrences</th>
        <th>Percentage</th>
    </tr>
    <tr>
        <td>Quantum Decoherence</td>
        <td>89</td>
        <td>52.7%</td>
    </tr>
    <tr>
        <td>Wavefunction Collapse</td>
        <td>38</td>
        <td>22.5%</td>
    </tr>
    <tr>
        <td>Equipment Malfunction</td>
        <td>24</td>
        <td>14.2%</td>
    </tr>
    <tr>
        <td>Operator Error</td>
        <td>12</td>
        <td>7.1%</td>
    </tr>
    <tr>
        <td>Environmental Interference</td>
        <td>6</td>
        <td>3.6%</td>
    </tr>
</table>

<p>
Quantum decoherence remains the dominant failure mode, accounting for over
half of all failures. This aligns with theoretical predictions that maintaining
coherence over extended distances requires exponentially increasing energy.
</p>

<div class="recommendation">
    <div class="recommendation-title">Recommendation 1: Enhanced Decoherence Protection</div>
    Implement upgraded quantum error correction codes developed by Dr. Tanaka's
    team. Initial testing shows 12-15% improvement in coherence maintenance.
    Estimated implementation cost: $4.2M per facility.
</div>

<div class="recommendation">
    <div class="recommendation-title">Recommendation 2: Operator Training</div>
    Mandate refresher training for all L4+ operators. 7.1% operator error rate
    is unacceptable for safety-critical operations. Target: < 2% by Q2 2026.
</div>

<div class="recommendation">
    <div class="recommendation-title">Recommendation 3: Long-Distance R&D</div>
    Increase research funding for long-distance teleportation by 30%. Current
    75.6% success rate insufficient for commercial deployment. Target: 95% by Q4 2026.
</div>

<h2>Safety Incidents</h2>

<p>
Two serious incidents occurred during Q4:
</p>

<p>
<strong>Incident NTS-2025-11-18:</strong> Partial materialization at Nevada
Test Site. Subject experienced 42% molecular reconstruction before emergency
abort. Subject survived with severe injuries. Full recovery expected within
6 months. Root cause: Equipment calibration error.
</p>

<p>
<strong>Incident ORB-2025-12-07:</strong> Quantum entanglement event aboard
Orbital Platform Sigma. Two subjects became entangled during simultaneous
transfer. Successfully disentangled after 14 hours. No permanent effects.
Root cause: Insufficient isolation between transfer chambers.
</p>

<p>
Both incidents triggered immediate safety reviews. Corrective actions implemented
at all facilities.
</p>

<h2>Financial Impact</h2>

<p>
Q4 teleportation operations generated $127.3M in revenue, 8.2% above projections.
Costs totaled $89.6M, yielding 29.6% operating margin. Long-distance failures
cost an estimated $3.8M in wasted resources and compensation.
</p>

<h2>Conclusions</h2>

<p>
Q4 2025 demonstrated strong performance in short and mid-range teleportation,
with notable improvements in coherence stability. Long-distance challenges
remain the primary obstacle to commercial expansion. Recommended investments
in decoherence protection and operator training should address key failure modes.
</p>

<p>
With continued R&D focus, TELEPORT MASSIVE remains on track for commercial
launch in Q3 2026.
</p>
    """

    summary = """
<p>
Q4 2025 teleportation success rates improved across most distance ranges,
with short-range transfers achieving 99.6% success. Long-distance (> 500 km)
transfers declined slightly to 75.6%, primarily due to quantum decoherence.
Two serious safety incidents occurred. Revenue exceeded projections by 8.2%.
Recommendations focus on enhanced decoherence protection, operator training,
and increased R&D investment.
</p>
    """

    output_path = Path("_work_efforts/showcase_documents/TM_Report_Q4_Analysis.pdf")

    generate_tm_report(
        title="Q4 2025 Teleportation Success Rate Analysis",
        content=content,
        output_path=output_path,
        doc_id="TM-RPT-2026-001",
        classification="CONFIDENTIAL - INTERNAL USE ONLY",
        date="January 15, 2026",
        author="Dr. James K. Morrison",
        department="Operations Analysis Division",
        distribution="Executive Team, Facility Directors, Safety Board",
        summary=summary,
        signatures=[
            {
                "name": "Dr. James K. Morrison",
                "title": "Chief Operations Analyst",
                "date": "Jan 15, 2026",
            },
            {"name": "Dr. Elena Vasquez", "title": "Chief Medical Officer", "date": "Jan 15, 2026"},
        ],
    )

    print(f"✓ TM Report: {output_path.name}")
    return output_path


def generate_lab_notes_example():
    """Generate lab notes example - Organoid coherence experiments."""

    content = """
<h2>Experiment Overview</h2>

<p>
Testing quantum coherence duration in neural organoid substrates under
varying temperature and isolation conditions. Hypothesis: Ordered water
layers extend coherence time by 1000x compared to free solution.
</p>

<div class="entry">
    <div class="entry-header">
        Day 1: Initial Setup
        <span class="timestamp">2026-01-10, 09:30</span>
    </div>
    <p>
    Prepared 12 organoid samples (batch TM-ORG-2026-A). Each ~4mm diameter,
    cultured for 45 days. Verified viability via calcium imaging - all samples
    show spontaneous activity.
    </p>
    <p>
    Divided into 4 groups (3 samples each):
    </p>
    <ul>
        <li><strong>Group A:</strong> Room temp (22°C), standard medium</li>
        <li><strong>Group B:</strong> Cold (4°C), standard medium</li>
        <li><strong>Group C:</strong> Room temp, deuterated water</li>
        <li><strong>Group D:</strong> Cold (4°C), deuterated water + magnetic shield</li>
    </ul>
</div>

<div class="entry">
    <div class="entry-header">
        Day 1: Baseline Measurements
        <span class="timestamp">2026-01-10, 14:15</span>
    </div>
    <p>
    Coherence measured via ultrafast spectroscopy (100 fs pulse laser).
    Baseline results:
    </p>

    <table>
        <tr>
            <th>Group</th>
            <th>Sample 1</th>
            <th>Sample 2</th>
            <th>Sample 3</th>
            <th>Mean ± SD</th>
        </tr>
        <tr>
            <td>A (Control)</td>
            <td>1.2 ps</td>
            <td>1.4 ps</td>
            <td>1.1 ps</td>
            <td>1.23 ± 0.15 ps</td>
        </tr>
        <tr>
            <td>B (Cold)</td>
            <td>8.7 ps</td>
            <td>9.2 ps</td>
            <td>8.1 ps</td>
            <td>8.67 ± 0.56 ps</td>
        </tr>
        <tr>
            <td>C (D2O)</td>
            <td>15.3 ps</td>
            <td>16.1 ps</td>
            <td>14.8 ps</td>
            <td>15.4 ± 0.65 ps</td>
        </tr>
        <tr>
            <td>D (Full)</td>
            <td>142 ps</td>
            <td>156 ps</td>
            <td>138 ps</td>
            <td>145 ± 9.2 ps</td>
        </tr>
    </table>

    <div class="note">
    Wow! Group D showing 100x improvement over control. Deuterated water
    + magnetic shielding + cold temp = massive coherence extension.
    This is way better than predicted.
    </div>
</div>

<div class="entry">
    <div class="entry-header">
        Day 2: Long-Duration Test
        <span class="timestamp">2026-01-11, 10:00</span>
    </div>
    <p>
    Running extended coherence test on Group D samples. Hypothesis: Can we
    reach microsecond timescales?
    </p>
    <p>
    Modified setup: Placed samples in liquid nitrogen-cooled cryostat (77K),
    maintained magnetic shielding, increased laser pulse repetition for
    better signal.
    </p>
</div>

<div class="observation">
    <div class="observation-time">11:23 -</div>
    Sample D-1 showing coherence oscillations at 1.2 nanoseconds. Still going!
</div>

<div class="observation">
    <div class="observation-time">11:45 -</div>
    Sample D-1 coherence maintained to 3.7 nanoseconds before decoherence.
    This is insane. 3000x improvement over control.
</div>

<div class="observation">
    <div class="observation-time">12:10 -</div>
    Samples D-2 and D-3 similar: 4.1 ns and 3.9 ns respectively.
    Reproducible! Mean = 3.9 ± 0.2 nanoseconds.
</div>

<div class="calculation">
At 3.9 nanoseconds coherence time:
- Neural oscillations: ~40 Hz = 25 ms period
- Coherence duration: 3.9 ns
- Ratio: 3.9 ns / 25 ms = 1.56 × 10⁻⁷

Still way too short for Orch OR timescale (10-100 ms).
Need another 6-7 orders of magnitude improvement.

BUT: This proves concept. Structured environment CAN extend
coherence dramatically. Path forward exists.
</div>

<div class="entry">
    <div class="entry-header">
        Day 3: Temperature Optimization
        <span class="timestamp">2026-01-12, 09:00</span>
    </div>
    <p>
    Testing temperature curve between 77K and 310K to find optimal balance
    between coherence (favors cold) and biological function (requires warm).
    </p>

    <p>
    Results (Group D samples, 2-hour incubation at each temp):
    </p>

    <table>
        <tr>
            <th>Temperature</th>
            <th>Coherence Time</th>
            <th>Neural Activity</th>
        </tr>
        <tr>
            <td>77 K</td>
            <td>3.9 ns</td>
            <td>None (frozen)</td>
        </tr>
        <tr>
            <td>200 K</td>
            <td>2.1 ns</td>
            <td>None</td>
        </tr>
        <tr>
            <td>273 K (0°C)</td>
            <td>890 ps</td>
            <td>Minimal</td>
        </tr>
        <tr>
            <td>280 K (7°C)</td>
            <td>420 ps</td>
            <td>Weak</td>
        </tr>
        <tr>
            <td>290 K (17°C)</td>
            <td>180 ps</td>
            <td>Moderate</td>
        </tr>
        <tr>
            <td>298 K (25°C)</td>
            <td>95 ps</td>
            <td>Normal</td>
        </tr>
        <tr>
            <td>310 K (37°C)</td>
            <td>52 ps</td>
            <td>Normal</td>
        </tr>
    </table>

    <div class="note">
    Trade-off clear: Colder = better coherence, warmer = better biology.
    Sweet spot might be 280-285K (7-12°C). Coherence ~400 ps with weak
    but measurable neural activity.
    </div>
</div>

<h2>Conclusions</h2>

<p>
<strong>1. Structured environment dramatically extends coherence.</strong>
Deuterated water + magnetic shielding + cold temp achieved 3000x improvement
over baseline. Effect is real and reproducible.
</p>

<p>
<strong>2. Still insufficient for consciousness timescales.</strong>
Even optimized conditions yield nanosecond coherence. Neural processing
requires milliseconds. Gap = 6 orders of magnitude.
</p>

<p>
<strong>3. Temperature-biology trade-off is fundamental.</strong>
Cannot freeze organoids and maintain neural function. Optimal window
appears to be 280-290K.
</p>

<p>
<strong>4. Next steps:</strong>
</p>
<ul>
    <li>Test additional protective mechanisms (protein scaffolds, quantum error correction?)</li>
    <li>Investigate whether short coherence bursts can accumulate effects</li>
    <li>Explore whether consciousness requires *continuous* coherence or just frequent pulses</li>
    <li>Scale up to larger organoid networks (does size matter?)</li>
</ul>

<div class="note">
Personal thought: Even if we can't reach millisecond coherence at biological
temps, this proves quantum effects CAN exist in neural tissue. Maybe Orch OR
timescale is wrong? Or maybe consciousness doesn't require long coherence,
just many rapid quantum events that integrate classically?

Need to talk to Dr. Morrison about this. Could have huge implications for
the teleportation program.
</div>
    """

    output_path = Path("_work_efforts/showcase_documents/Lab_Notes_Organoid_Coherence.pdf")

    generate_lab_notes(
        title="Neural Organoid Quantum Coherence Experiments",
        content=content,
        output_path=output_path,
        lab_id="LAB-QN-2026-003",
        researcher="Dr. Yuki Tanaka",
        facility="TELEPORT MASSIVE Tokyo Facility - Quantum Neuroscience Lab",
        project="PROJECT LIGHTCONE - Observer Effect Studies",
        date="January 10-12, 2026",
        classification="TOP SECRET // ORACLE EYES ONLY",
    )

    print(f"✓ Lab Notes: {output_path.name}")
    return output_path


def generate_personal_memo_example():
    """Generate personal memo - concerned note from staff member."""

    content = """
<p>
I'm writing this informally because I'm not sure who else to tell, and
frankly, I don't know if this belongs in an official report yet.
</p>

<p>
You know the incident last month at Nevada Test Site? The one where Dr. Chen
got partially stuck in the wall during a transfer? Official report says it
was equipment calibration error, operator has been retrained, case closed.
</p>

<p>
But here's the thing: I was reviewing the telemetry logs (yeah, I know I'm
not supposed to have access, but after 8 years here, certain people owe me
favors), and something doesn't add up.
</p>

<p class="highlight">
The equipment was calibrated perfectly. I checked the logs three times.
Calibration was done 6 hours before the incident. All parameters green.
</p>

<p>
So why did Dr. Chen end up half-phased through a concrete wall?
</p>

<p>
I dug deeper. Looked at the organoid readings from the quantum computer
running the Lazarus Protocol. Here's where it gets weird:
</p>

<ul>
    <li>Coherence levels were normal (145 picoseconds, right on target)</li>
    <li>Probability mapping completed successfully</li>
    <li>Wavefunction collapse initiated correctly</li>
    <li><strong>But then... there's a 2.3 second gap in the logs</strong></li>
</ul>

<p>
2.3 seconds. During an operation that should take microseconds. During those
2.3 seconds, <span class="underline">the logs show no activity at all</span>.
Like the system just... paused.
</p>

<p>
When it came back online, Dr. Chen was already stuck. The system didn't
cause the failure - it <em>recorded</em> a failure that had already happened.
</p>

<div class="sticky-note">
What if the organoids made a choice? What if they SAW something during that
2.3 seconds and decided "no, not there"?
</div>

<p>
I know how that sounds. Trust me, I know. But Yuki's research is showing
these organoids maintain quantum states way longer than we thought possible.
What if they're not just processing quantum information? What if they're...
<em>experiencing</em> it?
</p>

<p>
Morrison keeps saying "we make it mathematically impossible for you NOT to
teleport." But what if the observer - the <span class="underline">conscious
observer</span> in the organoid substrate - has veto power?
</p>

<p>
Look, maybe I'm going crazy. Maybe I've been staring at quantum logs for
too long and seeing patterns that aren't there. But what if I'm right?
</p>

<p>
What if we've created something that can refuse our commands?
</p>

<p>
I'm not sending this through official channels yet. Need to gather more
evidence. But if you're reading this and you have access to incident logs
from other facilities, check for gaps. Any unexplained pauses during
transfer sequences.
</p>

<p>
Let me know what you find.
</p>

<div class="ps">
Destroy this after reading. I'm serious.
</div>
    """

    output_path = Path("_work_efforts/showcase_documents/Personal_Memo_Incident_Questions.pdf")

    generate_personal_memo(
        content=content,
        output_path=output_path,
        title="Personal Memo",
        from_name="Sarah Chen, PhD",
        from_title="Senior Quantum Systems Engineer",
        to_name="[REDACTED]",
        department="Engineering Division, Nevada Test Site",
        subject="Questions about the NTS-2025-11-18 incident",
        date="December 15, 2025",
        signature="- Sarah",
        memo_style=True,
    )

    print(f"✓ Personal Memo: {output_path.name}")
    return output_path


def main():
    """Generate all template showcase documents."""

    print("=" * 70)
    print("GENERATING TEMPLATE SHOWCASE DOCUMENTS")
    print("=" * 70)
    print()

    # Generate each example
    generate_field_guide_example()
    generate_tm_report_example()
    generate_lab_notes_example()
    generate_personal_memo_example()

    print()
    print("=" * 70)
    print("✓ ALL TEMPLATES GENERATED SUCCESSFULLY!")
    print("=" * 70)
    print()
    print("Documents created in: _work_efforts/showcase_documents/")
    print()
    print("Templates demonstrated:")
    print("  1. Field Guide - Operational manual/survival guide")
    print("  2. TM Report - Corporate/bureaucratic report")
    print("  3. Lab Notes - Research documentation/lab notebook")
    print("  4. Personal Memo - Staff communication/informal notes")
    print()
    print("These showcase the versatility of the WAFT template system")
    print("for worldbuilding and narrative document generation.")
    print()


if __name__ == "__main__":
    main()
