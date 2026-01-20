"""
Generate a beautiful scientific paper showcasing the WAFT template system.

This creates a high-quality research paper on quantum consciousness and
the observer effect in biological systems.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.templates.simple_scientific import generate_simple_scientific_document

# Document content - rich, well-structured scientific paper
CONTENT = """
<h2>1. Introduction</h2>

<p>
The relationship between quantum mechanics and consciousness remains one of the most
profound unsolved problems in modern science. While quantum theory successfully describes
the behavior of particles at atomic scales, the role of observation in wavefunction
collapse suggests a deep connection between conscious awareness and physical reality
<span style="color: #666;">[1, 2]</span>.
</p>

<p>
The Penrose-Hameroff theory of quantum consciousness proposes that microtubules within
neurons serve as quantum processing units, enabling consciousness to emerge from quantum
computations rather than classical neural activity alone <span style="color: #666;">[3]</span>.
This hypothesis, while controversial, has gained renewed attention following experimental
demonstrations of quantum effects in biological systems at physiological temperatures
<span style="color: #666;">[4, 5]</span>.
</p>

<p>
This paper examines the theoretical foundations of quantum consciousness, analyzes recent
experimental evidence, and explores implications for our understanding of the observer
effect in quantum mechanics. We propose a framework for testing quantum consciousness
hypotheses using organoid-based quantum computing architectures.
</p>

<h2>2. Theoretical Framework</h2>

<h3>2.1 Quantum Mechanics and the Observer Effect</h3>

<p>
In quantum mechanics, a system exists in superposition—multiple states simultaneously—until
observed. The Copenhagen interpretation posits that measurement collapses the wavefunction
into a single eigenstate. Mathematically, this is expressed as:
</p>

<div style="text-align: center; margin: 0.3in 0; font-family: 'Times New Roman', serif; font-size: 13pt;">
    |ψ⟩ = α|0⟩ + β|1⟩ → |n⟩ (upon measurement)
</div>

<p>
where α and β are complex probability amplitudes satisfying |α|² + |β|² = 1. The fundamental
question becomes: <em>What constitutes an "observation"?</em> Does consciousness play a
necessary role, or is any physical interaction sufficient?
</p>

<h3>2.2 The Penrose-Hameroff Orchestrated Objective Reduction (Orch OR) Theory</h3>

<p>
Penrose and Hameroff propose that consciousness arises from quantum gravitational effects
in neuronal microtubules. Key predictions include:
</p>

<ul>
    <li>Microtubules maintain quantum coherence for 10-100 milliseconds</li>
    <li>Quantum superpositions reach threshold of spacetime separation (Δx ≈ 10⁻¹⁰ m)</li>
    <li>Objective reduction occurs via gravitational self-energy differences</li>
    <li>Conscious moments correlate with reduction events (~40 Hz gamma oscillations)</li>
</ul>

<h3>2.3 Many-Worlds Interpretation and Consciousness</h3>

<p>
An alternative framework suggests consciousness does not collapse wavefunctions but rather
experiences single branches of the quantum multiverse. In this view, each measurement
creates parallel universes, with conscious observers experiencing consistent histories
along specific branches. This interpretation eliminates the need for special observer
status but raises questions about the nature of subjective experience across branches.
</p>

<h2>3. Experimental Evidence</h2>

<h3>3.1 Quantum Effects in Biological Systems</h3>

<p>
Recent experiments demonstrate quantum phenomena in biology at physiological temperatures:
</p>

<table>
    <caption>Table 1: Confirmed Quantum Effects in Biological Systems</caption>
    <tr>
        <th>System</th>
        <th>Quantum Effect</th>
        <th>Temperature (K)</th>
        <th>Coherence Time</th>
    </tr>
    <tr>
        <td>Photosynthetic complexes</td>
        <td>Quantum coherence</td>
        <td>277-310</td>
        <td>660 fs - 1.5 ps</td>
    </tr>
    <tr>
        <td>Avian magnetoreception</td>
        <td>Radical pair mechanism</td>
        <td>310</td>
        <td>~100 μs</td>
    </tr>
    <tr>
        <td>Enzyme catalysis</td>
        <td>Quantum tunneling</td>
        <td>273-310</td>
        <td>Instantaneous</td>
    </tr>
    <tr>
        <td>Olfactory receptors</td>
        <td>Electron tunneling</td>
        <td>310</td>
        <td>~1 fs</td>
    </tr>
</table>

<p>
These findings demonstrate that quantum effects can persist in warm, wet biological
environments—challenging the assumption that decoherence immediately destroys quantum
phenomena in living systems.
</p>

<h3>3.2 Neuronal Microtubule Studies</h3>

<p>
Microtubules are cylindrical protein polymers (25 nm diameter) composed of tubulin dimers.
Each dimer can exist in multiple conformational states, potentially storing quantum information.
Key experimental observations include:
</p>

<ul>
    <li><strong>Electrical conductivity:</strong> Microtubules exhibit semiconductor-like properties</li>
    <li><strong>Resonance:</strong> Megahertz to gigahertz frequency oscillations detected</li>
    <li><strong>Anesthetic sensitivity:</strong> Quantum-sensitive mechanisms disrupted by anesthetics</li>
    <li><strong>Isolation:</strong> Ordered water layers may provide decoherence protection</li>
</ul>

<h2>4. Computational Methods</h2>

<h3>4.1 Quantum Decoherence Simulation</h3>

<p>
To assess whether microtubules can maintain quantum coherence, we developed a Python-based
simulation using the Lindblad master equation:
</p>

<pre><code>import numpy as np
from scipy.linalg import expm

def lindblad_evolution(rho0, H, L, t, gamma):
    # Simulate quantum decoherence using Lindblad equation
    # Args: rho0 (initial density matrix), H (Hamiltonian),
    #       L (Lindblad operator), t (time array), gamma (rate)
    # Returns: rho_t (evolved density matrix at each time)

    # Liouvillian superoperator
    def liouvillian(rho):
        commutator = -1j * (H @ rho - rho @ H)
        dissipator = gamma * (L @ rho @ L.conj().T -
                              0.5 * (L.conj().T @ L @ rho +
                                     rho @ L.conj().T @ L))
        return commutator + dissipator

    # Time evolution
    rho_t = []
    for ti in t:
        rho = expm(liouvillian * ti) @ rho0
        rho_t.append(rho)

    return np.array(rho_t)

# Simulation parameters
gamma_bio = 1e9  # Biological decoherence rate (s^-1)
gamma_mt = 1e3   # Microtubule protected rate (s^-1)

# Result: ~1000x longer coherence in structured environment</code></pre>

<p>
Our simulations suggest that ordered water layers and protein structure around microtubules
could extend coherence times from picoseconds (free solution) to nanoseconds or microseconds
(structured environment)—approaching the timescale required for neural processing.
</p>

<h3>4.2 Neural Organoid Quantum Computing Architecture</h3>

<p>
We propose using brain organoids—3D cultured neural tissues—as quantum processing substrates.
The architecture combines classical neural computation with quantum coherence in microtubule networks:
</p>

<ol>
    <li><strong>Quantum layer:</strong> Microtubule networks maintain entangled states</li>
    <li><strong>Classical layer:</strong> Synaptic connections process information conventionally</li>
    <li><strong>Interface:</strong> Membrane potentials couple quantum and classical domains</li>
    <li><strong>Readout:</strong> Calcium imaging reveals quantum state-dependent activity</li>
</ol>

<h2>5. Results and Discussion</h2>

<h3>5.1 Coherence Time Analysis</h3>

<p>
Our decoherence simulations yield coherence times consistent with Orch OR predictions.
Under optimal conditions (ordered water, geometric shielding, low temperature fluctuations),
microtubule quantum states persist for:
</p>

<div style="margin: 0.2in 0.5in; padding: 0.2in; background: #f9f9f9; border-left: 3px solid #666;">
    <strong>τ<sub>coherence</sub> = (1.2 ± 0.3) × 10⁻⁵ seconds</strong>
    <br><br>
    This 12-microsecond window is sufficient for ~500 neural oscillations at gamma frequency
    (40 Hz), potentially enabling quantum computation across multiple synaptic events.
</div>

<h3>5.2 Implications for Consciousness</h3>

<p>
If consciousness emerges from quantum processes in microtubules, several testable predictions follow:
</p>

<ul>
    <li><strong>Anesthetic mechanism:</strong> Drugs disrupt quantum coherence, not just ion channels</li>
    <li><strong>Cognitive enhancement:</strong> Protecting coherence improves information processing</li>
    <li><strong>Quantum effects in psychology:</strong> Decision-making may exhibit quantum interference</li>
    <li><strong>Observer effect biology:</strong> Conscious observation could influence quantum biological processes</li>
</ul>

<h3>5.3 Quantum Teleportation via Observer Collapse</h3>

<p>
Our findings suggest a speculative but theoretically grounded mechanism for quantum teleportation
using conscious observers. If consciousness can collapse wavefunctions in biologically relevant
timeframes, and if the Many-Worlds interpretation is correct, then:
</p>

<ol>
    <li>Subject enters quantum superposition across spatial locations</li>
    <li>Conscious observer (using organoid quantum computer) "measures" subject</li>
    <li>Wavefunction collapses into branch where subject exists at target location</li>
    <li>From subject's perspective, teleportation is instantaneous and certain</li>
</ol>

<p>
<em>Critical assumption:</em> This requires consciousness to genuinely collapse wavefunctions
rather than merely correlate with pre-existing classical outcomes. Experimental validation
would revolutionize both physics and neuroscience.
</p>

<h2>6. Experimental Proposals</h2>

<h3>6.1 Organoid Quantum Interference Experiment</h3>

<p>
We propose a modified double-slit experiment using neural organoids as observers:
</p>

<ul>
    <li><strong>Setup:</strong> Photons pass through double-slit, detected by photodiodes</li>
    <li><strong>Control:</strong> Standard interference pattern observed</li>
    <li><strong>Test:</strong> Neural organoid "observes" which-path information via coupled quantum dot</li>
    <li><strong>Prediction:</strong> Interference pattern collapses only when organoid exhibits conscious activity</li>
</ul>

<h3>6.2 Anesthetic Coherence Disruption Test</h3>

<p>
Administer anesthetics (propofol, sevoflurane) to cultured neurons while monitoring:
</p>

<ul>
    <li>Microtubule quantum coherence (via ultrafast spectroscopy)</li>
    <li>Consciousness proxies (integrated information, complexity measures)</li>
    <li>Time course correlation between coherence loss and consciousness loss</li>
</ul>

<h2>7. Challenges and Future Directions</h2>

<h3>7.1 Technical Challenges</h3>

<p>
Several obstacles must be overcome:
</p>

<ul>
    <li><strong>Measurement:</strong> Detecting quantum coherence in living tissue without destroying it</li>
    <li><strong>Isolation:</strong> Shielding biological systems from environmental decoherence</li>
    <li><strong>Validation:</strong> Distinguishing quantum from classical information processing</li>
    <li><strong>Scaling:</strong> Moving from single neurons to integrated brain function</li>
</ul>

<h3>7.2 Philosophical Implications</h3>

<p>
If consciousness plays a fundamental role in quantum mechanics, profound questions arise:
</p>

<ul>
    <li>Does consciousness exist at the quantum level in all matter?</li>
    <li>Is the universe participatory—requiring observers to become real?</li>
    <li>Can we engineer consciousness by controlling quantum coherence?</li>
    <li>What ethical considerations govern quantum consciousness research?</li>
</ul>

<h2>8. Conclusion</h2>

<p>
The quantum consciousness hypothesis remains speculative but increasingly testable. Recent
demonstrations of quantum effects in biological systems at physiological temperatures remove
a major theoretical objection. Our simulations suggest microtubules could maintain coherence
for microseconds—sufficient for neural computation.
</p>

<p>
We propose concrete experiments using neural organoids to test whether consciousness genuinely
collapses wavefunctions. If confirmed, this would represent a paradigm shift in both neuroscience
and physics, with applications ranging from quantum computing to novel approaches for treating
disorders of consciousness.
</p>

<p>
The intersection of quantum mechanics and consciousness may finally yield to experimental
investigation. As Bohr noted, "If quantum mechanics hasn't profoundly shocked you, you haven't
understood it yet." Understanding consciousness may require accepting that reality itself is
fundamentally participatory.
</p>

<h2>Acknowledgments</h2>

<p>
This work was supported by TELEPORT MASSIVE Research Division. We thank Dr. Sarah Chen for
discussions on quantum decoherence, Dr. Michael Torres for neural organoid protocols, and
the Quantum Biology Consortium for computational resources. Special thanks to the late
Dr. Roger Penrose for inspiring this line of inquiry.
</p>
"""

# References
REFERENCES = [
    "[1] Von Neumann, J. (1955). Mathematical Foundations of Quantum Mechanics. Princeton University Press.",
    "[2] Wigner, E. P. (1967). Remarks on the Mind-Body Question. In: Symmetries and Reflections, pp. 171-184.",
    "[3] Penrose, R., & Hameroff, S. (2011). Consciousness in the universe: Neuroscience, quantum space-time geometry and Orch OR theory. Journal of Cosmology, 14, 1-50.",
    "[4] Engel, G. S., et al. (2007). Evidence for wavelike energy transfer through quantum coherence in photosynthetic systems. Nature, 446(7137), 782-786.",
    "[5] Lambert, N., et al. (2013). Quantum biology. Nature Physics, 9(1), 10-18.",
    "[6] Craddock, T. J., et al. (2017). Anesthetic alterations of collective terahertz oscillations in tubulin correlate with clinical potency. Scientific Reports, 7, 9877.",
    "[7] Koch, C., et al. (2016). Neural correlates of consciousness: Progress and problems. Nature Reviews Neuroscience, 17(5), 307-321.",
    "[8] Tegmark, M. (2000). Importance of quantum decoherence in brain processes. Physical Review E, 61(4), 4194.",
    "[9] Hagan, S., et al. (2002). Quantum computation in brain microtubules: Decoherence and biological feasibility. Physical Review E, 65(6), 061901.",
    "[10] Fisher, M. P. (2015). Quantum cognition: The possibility of processing with nuclear spins in the brain. Annals of Physics, 362, 593-602.",
]


def main():
    """Generate the quantum consciousness research paper."""

    output_path = Path("_work_efforts/showcase_documents/Quantum_Consciousness_Observer_Effect.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Generating beautiful scientific document...")
    print("=" * 60)

    # Generate the document
    pdf_path = generate_simple_scientific_document(
        title="Quantum Consciousness and the Observer Effect: A Framework for Understanding Wavefunction Collapse in Biological Systems",
        content=CONTENT,
        output_path=output_path,
        authors=["Dr. Elena Vasquez", "Dr. James K. Morrison", "Dr. Yuki Tanaka"],
        date="January 2026",
        abstract=(
            "The role of consciousness in quantum mechanics remains one of the deepest unsolved "
            "problems in modern science. This paper examines the Penrose-Hameroff theory of quantum "
            "consciousness, which proposes that microtubules in neurons serve as quantum processors. "
            "We present theoretical analysis, computational simulations, and experimental proposals "
            "to test whether consciousness plays a fundamental role in wavefunction collapse. Our "
            "decoherence simulations suggest microtubules can maintain quantum coherence for 12 ± 3 "
            "microseconds—sufficient for neural computation across multiple synaptic events. We propose "
            "using neural organoids to test quantum consciousness hypotheses and explore implications "
            "for quantum computing, disorders of consciousness, and the nature of reality itself. If "
            "confirmed, these findings would revolutionize our understanding of both physics and neuroscience."
        ),
        references=REFERENCES,
        short_title="Quantum Consciousness and the Observer Effect",
    )

    print("\n✓ Document generated successfully!")
    print(f"  Location: {pdf_path}")
    print(f"  Size: {pdf_path.stat().st_size:,} bytes")
    print("  Pages: ~8-10 (estimated)")
    print("\n" + "=" * 60)
    print("\nThis document demonstrates:")
    print("  • Clean, professional typography")
    print("  • Well-structured scientific content")
    print("  • Abstract, multiple authors, date")
    print("  • Section hierarchy (h2, h3, h4)")
    print("  • Tables with proper formatting")
    print("  • Code blocks with syntax")
    print("  • Lists (ordered and unordered)")
    print("  • References section")
    print("  • Mathematical notation (basic)")
    print("  • Blockquotes and emphasis")
    print("\nReady for download after git push!")


if __name__ == "__main__":
    main()
