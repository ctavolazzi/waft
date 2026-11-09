---
id: "001"
---
# MISSION: MINT GENESIS ARTIFACT & RELEASE

We are initializing the simulation. We need to generate the first tangible artifact of Timeline 001, witness it, and then seal the version.

## PHASE 1: THE GENESIS ARTIFACT
Create a Python script `src/waft/scripts/mint_genesis.py` that:
1.  **Imports** `TheFoundation` and the block components.
2.  **Loads** the configuration from `src/waft/config/tam_origin_config.json`.
3.  **Generates** a high-resolution PDF named `_fracture/ARTIFACT_001_GENESIS.pdf`.
4.  **Content Requirements:**
    * **Header:** "TIMELINE INITIATION REPORT // SEQ-001"
    * **Metadata:** Display the `timeline_id`, `soul_signature`, and `fracture_point` from the config using `KeyValueBlock`.
    * **Narrative Body:** A `TextBlock` stating: "The simulation has successfully fractured from the main trunk. Subject 991-DELTA is currently dormant within the San Francisco Construct. Local reality parameters are stable. Karma economy is offline (awaiting Chitragupta)."
    * **Footer:** "AUTHORIZED BY THE STATIC // ANCHOR: v0.3.0-anchor"
5.  **Auto-Open:** The script must programmatically open the PDF upon completion (use `subprocess.call(('open', filepath))` for Mac/Linux or `os.startfile` for Windows).

## PHASE 2: EXECUTION
Run the script immediately. I want to see the PDF open on my screen.

## PHASE 3: THE RELEASE
Once the artifact is generated:
1.  **Version Bump:** Update `pyproject.toml` and `src/waft/__init__.py` from `0.3.0-alpha` to `0.3.1-alpha` (The "First Breath" update).
2.  **Commit:** Stage the new script, the new config, the Genesis Marker, and the PDF artifact (force add the PDF if ignored).
    * *Commit Message:* `feat(timeline-001): Genesis Artifact minted. Simulation active v0.3.1`
3.  **Push:** Push the `fracture/001-origin-tam` branch to origin.

**Execute.**