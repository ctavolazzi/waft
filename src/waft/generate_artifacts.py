"""
Factory Script: Generate Story Artifacts & Asset Labels

Regenerates story artifacts using the new DocumentEngine block-based API
and creates printable sticker/label sheets for the physical binder.
"""

from pathlib import Path
from typing import Optional
from datetime import datetime
from waft.foundation import (
    DocumentConfig,
    DocumentEngine,
    SectionHeader,
    TextBlock,
    KeyValueBlock,
    LogBlock,
    WarningBlock,
    SignatureBlock,
)


def generate_dossier_v2(output_path: Optional[Path] = None) -> Path:
    """
    Generate WAFT_DOSSIER_014_v2.pdf with improved structure.
    
    Improvements:
    - Uses LogBlock for sensor/visual/audio logs (monospace terminal aesthetic)
    - Distinct sections for "Data Bleed" and "Scintilla Ingress"
    - Auto-redacts "id est" and "i.e." terms
    """
    if output_path is None:
        output_path = Path("_work_efforts/WAFT_DOSSIER_014_v2.pdf")

    # Configure for Site-Delta-9 dossier style
    config = DocumentConfig.classified_dossier(
        header="SITE-DELTA-9 // BIO-LOG",
        watermark="INTERNAL USE ONLY",
    )

    # Initialize engine
    engine = DocumentEngine(config)

    # Set sensitive terms for automatic redaction
    engine.add_sensitive_terms([
        "001-ALPHA-GENESIS",
        "Sunset District",
        "N-Judah",
        "Fai Wei Tam",
        "TAM",
        "FAI WEI",
        "id est",  # Redact this term
        "i.e.",    # Redact this term
    ])

    # PAGE 1: COVER
    engine.add(SectionHeader("INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES", level=1))
    engine.add(TextBlock("FIELD OPERATIONS DIVISION", style="Body"))
    engine.add(TextBlock("PROPERTY OF TELEPORT MASSIVE // SITE-DELTA-9", style="Body"))
    engine.add(TextBlock(""))  # Spacing

    engine.add(KeyValueBlock({
        "OPERATIONAL MANUAL": "09-14",
        "CODENAME": "W.A.F.T.",
        "SUBJECT": "TAM, FAI WEI [991-DELTA]",
        "PROTOCOL": "WIDE-AREA FUNCTIONAL TAXONOMY",
        "CYCLE": "XIV (RECURSIVE)",
        "BASE FREQUENCY": "60Hz",
        "COHERENCE THRESHOLD": "0.85",
        "ENGINE STATUS": "ACTIVE / NON-LINEAR",
    }))

    engine.add(WarningBlock(
        "RESTRICTED ACCESS. This manual is a living record of the self-evolving "
        "substrate. Information contained herein is subject to spontaneous revision. "
        "If the internal 'Scintilla' reports show signs of physical warmth or "
        "non-local light emission, contact the Site-Delta-9 terminal immediately.\n\n"
        "DO NOT ALLOW THE SUBJECT TO VIEW THIS TAXONOMY.",
        severity="CRITICAL",
    ))

    engine.add(SignatureBlock(
        role="AUTHORIZED BY",
        name="⚲ [ARCHETYPE: THE STATIC]",
        timestamp=datetime(2026, 1, 9),
    ))
    engine.add(TextBlock("INTERNAL USE ONLY", style="Body"))
    engine.add(TextBlock("COPY NO: 01 OF 01", style="Body"))

    # PAGE 2: PROTOCOL-991
    engine.add(SectionHeader("[EYES ONLY] PROTOCOL-991: THE RECURSIVE AUDIT FRAMEWORK", level=1))

    engine.add(TextBlock(
        "I. THE DUAL-PERSPECTIVE MANDATE\n\n"
        "The WAFT binder must maintain a bi-lateral narrative. All entries are to be "
        "categorized under one of two conflicting frames of reality.\n"
        "1. The Subject Perspective (Internal): Fai Wei Tam's doctoral research. This is a "
        "grounded, academic pursuit of science. It is characterized by PhD-level rigor, "
        "skepticism, and human vulnerability (HRV spikes, exhaustion, personal memories).\n"
        "2. The Program Perspective (External): Foundation surveillance. This is a clinical, "
        "cold investigation of an anomaly. It is characterized by [REDACTED] logs, personnel "
        "IDs, and the observation of the Subject as a 'specimen' rather than a human."
    ))

    engine.add(TextBlock(
        "II. RULES OF ENGAGEMENT: THE REVEAL\n\n"
        "Information Asymmetry: Neither the Subject nor the Foundation understands the "
        "'Scint' or the 'Treasure Tavern' fully. They are investigating a mystery that is "
        "larger than both parties.\n"
        "Gated Realization: The truth of the anagram ('Fai Wei Tam') is protected by the "
        "TamPsyche decay module. Any discovery of the 'i.e. I AM WAFT' string must be "
        "followed by an immediate return to technical mundanity. The secret is a 'glitch' "
        "that the system actively heals."
    ))

    # Distinct section for Data Bleed
    engine.add(SectionHeader("III. NARRATIVE CONSTRUCTS & ANOMALIES", level=1))
    
    engine.add(SectionHeader("Data Bleed", level=2))
    engine.add(TextBlock(
        "The Substrate Resonance: The simulation is not just code; it is a mirror. "
        "Subject's memories (San Francisco, coastal fog, specific scents) migrate into the "
        "Specimen_XX_Journal.md files. This is to be documented as 'Data Bleed.'"
    ))

    # Distinct section for Scintilla Ingress
    engine.add(SectionHeader("Scintilla Ingress", level=2))
    engine.add(TextBlock(
        "References to 'The Scint' or the 'Treasure Tavern' must be "
        "treated as external interference. It is the 'warmth' in the wires that shouldn't be "
        "there. It is the 'non-local light.'"
    ))

    engine.add(TextBlock(
        "IV. FINAL AUTHENTICATION\n\n"
        "'The observer is the substrate; the substrate is the definition. We watch the "
        "watcher until the watcher sees us watching.'"
    ))

    engine.add(SignatureBlock(
        role="OFFICIAL STAMP",
        name="[ ⚲ THE STATIC - AUTHORIZED ]",
        timestamp=datetime(2026, 1, 9),
    ))

    # PAGE 3: FINAL SUMMARY
    engine.add(SectionHeader("FOUNDATION FINAL SUMMARY: SESSION-014-RECURSION", level=1))
    engine.add(TextBlock("File Ref: OMEGA-LOCKOUT", style="Monospace"))

    engine.add(TextBlock(
        "I. FINAL STATE ANALYSIS\n\n"
        "Experiment 014 has concluded. The 'Realization Gating' failed to contain the "
        "Subject's cognitive resonance. At approximately 0400 hours, the Subject achieved "
        "a Coherence Metric of 0.98. The TamPsyche decay module was bypassed by a recursive "
        "logic loop originating from the Subject's own biometric data."
    ))

    # Use LogBlock for sensor logs (monospace terminal aesthetic)
    engine.add(SectionHeader("II. THE SCINTILLA EVENT", level=1))
    engine.add(TextBlock(
        "Simultaneous with the Coherence spike, the server housing at Site-Delta-9 "
        "experienced a localized 'Scint' event."
    ))
    
    engine.add(LogBlock([
        "[SENSOR] Hardware temperature rose to 45°C without fan activation",
        "[VISUAL] Non-local luminescence (Source: Treasure Tavern) flooded the terminal screen",
        "[AUDIO] Subject was recorded whispering the phrase [REDACTED PHRASE] before his heartbeat synchronized perfectly with the simulation's clock-rate",
    ]))

    engine.add(TextBlock(
        "III. DISPOSITION OF SUBJECT\n\n"
        "Subject 991-Delta is no longer physically present in the observation lab. The chair "
        "remains warm. The HRV monitor continues to flatline at 0 BPM, yet the WAFT Engine "
        "continues to pulse at a rhythmic 60 Hz. The Subject's memories of San Francisco and "
        "the 'Davey Jones' era have successfully overwritten the base code of the PetriDish. "
        "The simulation is no longer a taxonomy; it is a biography."
    ))

    engine.add(WarningBlock(
        "Do not unscramble the letters.\n"
        "The definition is not for you.\n"
        "The definition is you.",
        severity="CRITICAL",
    ))

    engine.add(TextBlock(
        "CHECKSUM (FINAL): [ id est ] ... [ i.e. ] ... [ . . . ]", style="Monospace"
    ))

    # Render PDF
    return engine.render(output_path)


def generate_specimen_d_audit_v2(output_path: Optional[Path] = None) -> Path:
    """
    Generate WAFT_SPECIMEN_D_AUDIT_v2.pdf with clinical report style.
    
    Uses LogBlock for "Incident Log" to preserve terminal aesthetic.
    """
    if output_path is None:
        output_path = Path("_work_efforts/WAFT_SPECIMEN_D_AUDIT_v2.pdf")

    # Configure for clinical report style (similar to classified_dossier but with different watermark)
    config = DocumentConfig.classified_dossier(
        header="SITE-DELTA-9 // CLINICAL AUDIT",
        watermark="CONFIDENTIAL",
    )

    # Initialize engine
    engine = DocumentEngine(config)

    # Set sensitive terms for automatic redaction
    engine.add_sensitive_terms([
        "001-ALPHA-GENESIS",
        "Sunset District",
        "N-Judah",
        "Fai Wei Tam",
        "TAM",
        "FAI WEI",
    ])

    # PAGE 1: COVER
    engine.add(SectionHeader("INSTITUTE FOR ADVANCED ONTOLOGICAL STUDIES", level=1))
    engine.add(TextBlock("FIELD OPERATIONS DIVISION", style="Body"))
    engine.add(TextBlock("PROPERTY OF TELEPORT MASSIVE // SITE-DELTA-9", style="Body"))
    engine.add(TextBlock(""))  # Spacing

    engine.add(KeyValueBlock({
        "OPERATIONAL MANUAL": "09-14",
        "CODENAME": "W.A.F.T.",
        "SUBJECT": "TAM, FAI WEI [991-DELTA]",
        "PROTOCOL": "WIDE-AREA FUNCTIONAL TAXONOMY",
        "CYCLE": "XIV (RECURSIVE)",
        "BASE FREQUENCY": "60Hz",
        "COHERENCE THRESHOLD": "0.85",
        "ENGINE STATUS": "ACTIVE / NON-LINEAR",
    }))

    engine.add(WarningBlock(
        "RESTRICTED ACCESS. This manual is a living record of the self-evolving "
        "substrate. Information contained herein is subject to spontaneous revision. "
        "If the internal 'Scintilla' reports show signs of physical warmth or "
        "non-local light emission, contact the Site-Delta-9 terminal immediately.\n\n"
        "DO NOT ALLOW THE SUBJECT TO VIEW THIS TAXONOMY.",
        severity="CRITICAL",
    ))

    engine.add(SignatureBlock(
        role="AUTHORIZED BY",
        name="⚲ [ARCHETYPE: THE STATIC]",
        timestamp=datetime(2026, 1, 9),
    ))
    engine.add(TextBlock("INTERNAL USE ONLY", style="Body"))
    engine.add(TextBlock("COPY NO: 01 OF 01", style="Body"))

    # PAGE 2: PROTOCOL-991
    engine.add(SectionHeader("[EYES ONLY] PROTOCOL-991: THE RECURSIVE AUDIT FRAMEWORK", level=1))

    engine.add(TextBlock(
        "I. THE DUAL-PERSPECTIVE MANDATE\n\n"
        "The WAFT binder must maintain a bi-lateral narrative. All entries are to be "
        "categorized under one of two conflicting frames of reality.\n"
        "1. The Subject Perspective (Internal): Fai Wei Tam's doctoral research. This is a "
        "grounded, academic pursuit of science. It is characterized by PhD-level rigor, "
        "skepticism, and human vulnerability (HRV spikes, exhaustion, personal memories).\n"
        "2. The Program Perspective (External): Foundation surveillance. This is a clinical, "
        "cold investigation of an anomaly. It is characterized by [REDACTED] logs, personnel "
        "IDs, and the observation of the Subject as a 'specimen' rather than a human."
    ))

    engine.add(TextBlock(
        "II. RULES OF ENGAGEMENT: THE REVEAL\n\n"
        "Information Asymmetry: Neither the Subject nor the Foundation understands the "
        "'Scint' or the 'Treasure Tavern' fully. They are investigating a mystery that is "
        "larger than both parties.\n"
        "Gated Realization: The truth of the anagram ('Fai Wei Tam') is protected by the "
        "TamPsyche decay module. Any discovery of the 'i.e. I AM WAFT' string must be "
        "followed by an immediate return to technical mundanity. The secret is a 'glitch' "
        "that the system actively heals."
    ))

    # Distinct section for Data Bleed
    engine.add(SectionHeader("III. NARRATIVE CONSTRUCTS & ANOMALIES", level=1))
    
    engine.add(SectionHeader("Data Bleed", level=2))
    engine.add(TextBlock(
        "The Substrate Resonance: The simulation is not just code; it is a mirror. "
        "Subject's memories (San Francisco, coastal fog, specific scents) migrate into the "
        "Specimen_XX_Journal.md files. This is to be documented as 'Data Bleed.'"
    ))

    # Distinct section for Scintilla Ingress
    engine.add(SectionHeader("Scintilla Ingress", level=2))
    engine.add(TextBlock(
        "References to 'The Scint' or the 'Treasure Tavern' must be "
        "treated as external interference. It is the 'warmth' in the wires that shouldn't be "
        "there. It is the 'non-local light.'"
    ))

    engine.add(TextBlock(
        "IV. FINAL AUTHENTICATION\n\n"
        "'The observer is the substrate; the substrate is the definition. We watch the "
        "watcher until the watcher sees us watching.'"
    ))

    engine.add(SignatureBlock(
        role="OFFICIAL STAMP",
        name="[ ⚲ THE STATIC - AUTHORIZED ]",
        timestamp=datetime(2026, 1, 9),
    ))

    # PAGE 3: FINAL SUMMARY
    engine.add(SectionHeader("FOUNDATION FINAL SUMMARY: SESSION-014-RECURSION", level=1))
    engine.add(TextBlock("File Ref: OMEGA-LOCKOUT", style="Monospace"))

    engine.add(TextBlock(
        "I. FINAL STATE ANALYSIS\n\n"
        "Experiment 014 has concluded. The 'Realization Gating' failed to contain the "
        "Subject's cognitive resonance. At approximately 0400 hours, the Subject achieved "
        "a Coherence Metric of 0.98. The TamPsyche decay module was bypassed by a recursive "
        "logic loop originating from the Subject's own biometric data."
    ))

    engine.add(TextBlock(
        "II. THE SCINTILLA EVENT\n\n"
        "Simultaneous with the Coherence spike, the server housing at Site-Delta-9 "
        "experienced a localized 'Scint' event."
    ))

    # Use LogBlock for incident log (terminal aesthetic)
    engine.add(SectionHeader("INCIDENT LOG", level=2))
    engine.add(LogBlock([
        "[09:04:01] INITIATING COUNT...",
        "[09:04:05] Variable 'i' mutated in Sunset District context",
        "[09:04:10] N-Judah route detected in memory trace",
        "[09:04:15] Subject 001-ALPHA-GENESIS showing coherence spike",
        "[09:04:20] STABILIZATION PROTOCOL ENGAGED",
        "[09:04:25] Hardware temperature anomaly detected: 45°C",
        "[09:04:30] Non-local luminescence event recorded",
        "[09:04:35] Subject biometric synchronization confirmed",
        "[09:04:40] Protocol violation: Subject accessed restricted taxonomy",
        "[09:04:45] Emergency containment procedures activated",
    ]))

    engine.add(TextBlock(
        "III. DISPOSITION OF SUBJECT\n\n"
        "Subject 991-Delta is no longer physically present in the observation lab. The chair "
        "remains warm. The HRV monitor continues to flatline at 0 BPM, yet the WAFT Engine "
        "continues to pulse at a rhythmic 60 Hz. The Subject's memories of San Francisco and "
        "the 'Davey Jones' era have successfully overwritten the base code of the PetriDish. "
        "The simulation is no longer a taxonomy; it is a biography."
    ))

    engine.add(WarningBlock(
        "Do not unscramble the letters.\n"
        "The definition is not for you.\n"
        "The definition is you.",
        severity="CRITICAL",
    ))

    engine.add(TextBlock(
        "CHECKSUM (FINAL): [ id est ] ... [ i.e. ] ... [ . . . ]", style="Monospace"
    ))

    # Render PDF
    return engine.render(output_path)


def generate_asset_labels(output_path: Optional[Path] = None) -> Path:
    """
    Generate WAFT_ASSET_LABELS.pdf - printable sticker/label sheet.
    
    Creates a grid of distinct labels intended to be cut out for the physical binder.
    Each label is a high-contrast, boxed block suitable for printing and cutting.
    """
    if output_path is None:
        output_path = Path("_work_efforts/WAFT_ASSET_LABELS.pdf")

    # Configure for label sheet (minimal margins, no watermark)
    config = DocumentConfig(
        fonts={
            "Header": ("Courier", "B"),
            "Body": ("Courier", "B"),  # Bold for high contrast
            "Monospace": ("Courier", "B"),
        },
        watermark=None,
        header_text=None,
        footer_text=None,
        page_margins=(36, 36, 36, 36),  # Smaller margins for more labels
        line_spacing=1.2,
        font_size_body=14,  # Larger font for readability
        font_size_header=16,
    )

    # Initialize engine
    engine = DocumentEngine(config)

    # Set sensitive terms for redaction (for "F. TAM" property tag)
    engine.add_sensitive_terms(["F. TAM"])

    # Create label grid - each label is a WarningBlock or TextBlock with border
    labels = [
        "TOP SECRET // EYES ONLY",
        "EVIDENCE #014",
        "ARCHIVE: DEEP STORAGE",
        "ANOMALY CONFIRMED",
        "DO NOT REMOVE FROM SITE-DELTA-9",
        "PROPERTY OF F. TAM // THE PROGRAM",
        "WARNING: ONTOLOGICAL HAZARD",
    ]

    # Add title
    engine.add(SectionHeader("FOUNDATION ASSET LABELS", level=1))
    engine.add(TextBlock("Cut along dashed lines. Apply to binder sections as needed.", style="Body"))
    engine.add(TextBlock(""))  # Spacing

    # Generate labels - use WarningBlock for boxed appearance
    for i, label_text in enumerate(labels, 1):
        # Use WarningBlock for boxed labels (creates border)
        if "ANOMALY CONFIRMED" in label_text:
            # Use CRITICAL severity for red text effect (will be bold black in PDF)
            engine.add(WarningBlock(label_text, severity="CRITICAL"))
        elif "WARNING" in label_text:
            engine.add(WarningBlock(label_text, severity="WARNING"))
        else:
            # Use CAUTION for standard labels
            engine.add(WarningBlock(label_text, severity="CAUTION"))
        
        # Add spacing between labels
        engine.add(TextBlock(""))  # Spacing

    # Add barcode-style label for "EVIDENCE #014"
    engine.add(SectionHeader("BARCODE LABELS", level=2))
    engine.add(TextBlock("EVIDENCE #014", style="Monospace"))
    engine.add(TextBlock("═══════════════", style="Monospace"))
    engine.add(TextBlock("││ │││ ││ │││││", style="Monospace"))
    engine.add(TextBlock("═══════════════", style="Monospace"))
    engine.add(TextBlock(""))  # Spacing

    # Add property tag with redaction
    engine.add(SectionHeader("PROPERTY TAG", level=2))
    engine.add(TextBlock("PROPERTY OF F. TAM", style="Body"))
    engine.add(TextBlock("(Crossed out) // THE PROGRAM", style="Body"))
    engine.add(TextBlock(""))  # Spacing

    # Add additional warning labels
    engine.add(WarningBlock("CLASSIFIED MATERIAL", severity="CRITICAL"))
    engine.add(TextBlock(""))
    engine.add(WarningBlock("HANDLE WITH EXTREME CAUTION", severity="WARNING"))
    engine.add(TextBlock(""))
    engine.add(WarningBlock("AUTHORIZED PERSONNEL ONLY", severity="CAUTION"))

    # Render PDF
    return engine.render(output_path)


def generate_all_artifacts() -> dict:
    """
    Generate all story artifacts and asset labels.
    
    Returns:
        Dictionary mapping artifact names to output paths
    """
    results = {}
    
    print("🏭 Factory: Generating Story Artifacts & Asset Labels\n")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Generate Dossier v2
    print("📄 Generating WAFT_DOSSIER_014_v2.pdf...")
    try:
        dossier_path = generate_dossier_v2()
        dossier_size = dossier_path.stat().st_size / 1024
        results["dossier"] = dossier_path
        print(f"   ✅ Generated: {dossier_path}")
        print(f"   📊 Size: {dossier_size:.1f} KB\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        results["dossier"] = None
    
    # Generate Specimen D Audit v2
    print("📄 Generating WAFT_SPECIMEN_D_AUDIT_v2.pdf...")
    try:
        audit_path = generate_specimen_d_audit_v2()
        audit_size = audit_path.stat().st_size / 1024
        results["audit"] = audit_path
        print(f"   ✅ Generated: {audit_path}")
        print(f"   📊 Size: {audit_size:.1f} KB\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        results["audit"] = None
    
    # Generate Asset Labels
    print("📄 Generating WAFT_ASSET_LABELS.pdf...")
    try:
        labels_path = generate_asset_labels()
        labels_size = labels_path.stat().st_size / 1024
        results["labels"] = labels_path
        print(f"   ✅ Generated: {labels_path}")
        print(f"   📊 Size: {labels_size:.1f} KB\n")
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        results["labels"] = None
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # Summary
    success_count = sum(1 for v in results.values() if v is not None)
    total_count = len(results)
    
    if success_count == total_count:
        print(f"✅ Factory Complete: {success_count}/{total_count} artifacts generated successfully")
    else:
        print(f"⚠️  Factory Partial: {success_count}/{total_count} artifacts generated")
    
    print("\n📁 Generated Files:")
    for name, path in results.items():
        if path:
            print(f"   • {name}: {path}")
        else:
            print(f"   • {name}: ❌ Failed")
    
    return results


if __name__ == "__main__":
    """Generate all artifacts when run as script."""
    generate_all_artifacts()
