"""
Tracery Grammar Definitions for Constructivist Sci-Fi Narratives.

These grammars generate procedural text for the TavernKeeper system.
During development, AI will review generated narratives and refine grammars.
"""

# Success Narratives Grammar
SUCCESS_GRAMMAR = {
    "origin": [
        "The #structure# #action# as #challenge# #outcome#.",
        "Wisdom flows through the #component# as #achievement# manifests.",
        "The TavernKeeper nods approvingly: '#narrative#.'",
        "Sector #sector# #status#. #machine_part# integrity at #percent#%.",
    ],
    "structure": ["foundation", "framework", "architecture", "substrate", "lattice"],
    "action": ["holds firm", "resonates", "stabilizes", "reinforces", "aligns"],
    "challenge": ["entropy", "complexity", "uncertainty", "technical debt", "chaos"],
    "outcome": ["dissipates", "recedes", "transforms", "yields", "submits"],
    "component": ["codebase", "system", "repository", "project", "construct"],
    "achievement": ["stability", "clarity", "efficiency", "resilience", "harmony"],
    "narrative": [
        "The construct stands firm",
        "Structural integrity confirmed",
        "All systems nominal",
        "Wisdom accumulates",
    ],
    "sector": ["Alpha-9", "Beta-3", "Gamma-7", "Delta-12", "Epsilon-5"],
    "status": ["reinforced", "optimized", "expanded", "realigned", "fortified"],
    "machine_part": ["Logic-Lattice", "Algorithm-Core", "Data-Stream", "Code-Matrix"],
    "percent": ["102%", "105%", "110%", "115%"],
}

# Failure Narratives Grammar
FAILURE_GRAMMAR = {
    "origin": [
        "The #structure# trembles as #problem# reveals itself.",
        "Wisdom falters - the #component# resists #action#.",
        "The TavernKeeper notes the #issue# with concern.",
        "WARNING: #desc# resonance detected in #machine_part#. Entropy levels rising.",
    ],
    "structure": ["foundation", "framework", "architecture", "lattice"],
    "problem": ["instability", "complexity", "uncertainty", "entropy", "decay"],
    "component": ["codebase", "system", "repository", "construct"],
    "action": ["verification", "construction", "integration", "optimization"],
    "issue": ["structural weakness", "logical inconsistency", "technical debt", "instability"],
    "desc": ["Isolinear", "Positronic", "Constructivist", "Kinetic", "Harmonic"],
    "machine_part": ["Logic-Lattice", "Algorithm-Core", "Data-Stream", "Code-Matrix"],
}

# Level Up Narratives Grammar
LEVEL_UP_GRAMMAR = {
    "origin": [
        "The #entity# evolves - new #capability# emerges from accumulated wisdom.",
        "The TavernKeeper raises a glass: 'You have grown, #title#.'",
        "Level #level# achieved. The #aspect# of #entity# deepens.",
        "#entity# reaches Level #level#. #capability# manifests in the #machine_part#.",
    ],
    "entity": ["structure", "system", "repository", "codebase", "construct"],
    "capability": ["resilience", "clarity", "efficiency", "wisdom", "mastery"],
    "title": ["Architect", "Constructor", "Builder", "Craftsman", "Keeper"],
    "level": ["#level_num#"],
    "level_num": ["2", "3", "4", "5", "10", "15", "20"],
    "aspect": ["foundation", "framework", "understanding", "mastery", "essence"],
    "machine_part": ["Logic-Lattice", "Algorithm-Core", "Data-Stream", "Code-Matrix"],
}

# Commit Narratives Grammar
COMMIT_GRAMMAR = {
    "origin": [
        "Sector #sector# reinforced by #class# #username#. #machine_part# integrity increased.",
        "Entropy purged from #file#. #desc# resonance detected.",
        "The TavernKeeper records: '#component# expands its domain.'",
        "#action# completes. #machine_part# hums with purpose.",
    ],
    "sector": ["Alpha-9", "Beta-3", "Gamma-7", "Delta-12", "Epsilon-5"],
    "class": ["Architect", "Constructor", "Fabricator", "Mechanicum", "Archivist"],
    "username": ["the Builder", "the Keeper", "the Architect"],
    "machine_part": ["Logic-Lattice", "Algorithm-Core", "Data-Stream", "Code-Matrix"],
    "file": ["main.py", "core.py", "utils.py", "the codebase"],
    "desc": ["Isolinear", "Positronic", "Constructivist", "Kinetic", "Harmonic"],
    "component": ["codebase", "system", "repository", "construct"],
    "action": ["Code integration", "Lattice reinforcement", "Structural optimization"],
}

# Critical Success Narratives
CRITICAL_SUCCESS_GRAMMAR = {
    "origin": [
        "GOLDEN AGE. The #machine_part# pulses with #desc# energy. DIVINE CODE INTEGRATION.",
        "Harmonic resonance achieved! #entity# transcends. #capability# unlocked.",
        "The TavernKeeper stands: 'Behold - #entity# has achieved perfection.'",
    ],
    "machine_part": ["Logic-Lattice", "Algorithm-Core", "Data-Stream", "Code-Matrix"],
    "desc": ["Isolinear", "Positronic", "Constructivist", "Kinetic", "Harmonic"],
    "entity": ["structure", "system", "repository", "codebase", "construct"],
    "capability": ["transcendence", "perfection", "harmony", "mastery"],
}

# Critical Failure Narratives
CRITICAL_FAILURE_GRAMMAR = {
    "origin": [
        "ENTROPY SPIKE DETECTED. The #machine_part# flickers. Structural resonance failure.",
        "Critical structural anomaly in Sector #sector#. The TavernKeeper intervenes.",
        "WARNING: #desc# decay detected. #entity# reports instability.",
    ],
    "machine_part": ["Logic-Lattice", "Algorithm-Core", "Data-Stream", "Code-Matrix"],
    "sector": ["Alpha-9", "Beta-3", "Gamma-7", "Delta-12", "Epsilon-5"],
    "desc": ["Isolinear", "Positronic", "Constructivist", "Kinetic", "Harmonic"],
    "entity": ["structure", "system", "repository", "codebase", "construct"],
}


def get_grammar(grammar_type: str) -> dict:
    """
    Get grammar by type.

    Args:
        grammar_type: One of "success", "failure", "level_up", "commit", "critical_success", "critical_failure"

    Returns:
        Grammar dictionary
    """
    grammars = {
        "success": SUCCESS_GRAMMAR,
        "failure": FAILURE_GRAMMAR,
        "level_up": LEVEL_UP_GRAMMAR,
        "commit": COMMIT_GRAMMAR,
        "critical_success": CRITICAL_SUCCESS_GRAMMAR,
        "critical_failure": CRITICAL_FAILURE_GRAMMAR,
    }
    return grammars.get(grammar_type, SUCCESS_GRAMMAR)

