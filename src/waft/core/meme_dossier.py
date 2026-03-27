from __future__ import annotations

import html as html_module
import random
from datetime import datetime
from pathlib import Path

from ..brief import BriefDocument
from .meme_generator import MemeGenerator, MemeRequest


def build_generation_cases(prompt: str, count: int, seed: int | None) -> list[dict]:
    rng = random.Random(seed if seed is not None else datetime.now().microsecond)
    modes = ["mixed", "template", "original"]
    templates = ["drake", "distracted_boyfriend", "expanding_brain", "inspiring_poster", ""]
    styles = ["top_bottom", "top_band", "motivational", ""]
    hooks = [
        "subject exhibited emergent meme patterning",
        "operator observed autonomous humor synthesis",
        "facility monitor flagged memetic output recursion",
        "containment review classified this as productive anomaly",
        "artifact chain indicates coherent self-referential satire",
    ]

    cases = []
    for i in range(1, count + 1):
        mode = modes[(i - 1) % len(modes)]
        template = rng.choice(templates) if mode != "original" else ""
        style = rng.choice(styles) if mode != "template" else ""
        case_seed = (seed + i) if seed is not None else rng.randint(10_000, 999_999)
        hook = hooks[(i - 1) % len(hooks)]
        cases.append(
            {
                "index": i,
                "mode": mode,
                "template": template,
                "style": style,
                "seed": case_seed,
                "prompt": f"{prompt} // incident-{i}: {hook}",
                "top_text": f"SITE-19 LOG {i}",
                "bottom_text": "WAFT MEME ENTITY ACTIVE",
                "title": f"ANOMALY-{i:03d}",
                "subtitle": hook.upper(),
                "rationale": (
                    f"Case {i} selected mode={mode} with seed={case_seed} to test reproducible "
                    "humor emergence while keeping containment narrative stable."
                ),
            }
        )
    return cases


def run_generation(project_path: Path, artifacts_dir: Path, cases: list[dict]) -> list[dict]:
    generator = MemeGenerator(project_path=project_path)
    records: list[dict] = []

    for case in cases:
        output_path = artifacts_dir / f"meme_{case['index']:02d}_{case['mode']}.jpg"
        request = MemeRequest(
            prompt=case["prompt"],
            top_text=case["top_text"],
            bottom_text=case["bottom_text"],
            title=case["title"],
            subtitle=case["subtitle"],
            mode=case["mode"],
            style=case["style"],
            template=case["template"],
            seed=case["seed"],
            output=str(output_path),
        )
        coi_commands = [
            f"COI.PREFLIGHT prompt='{case['prompt']}'",
            f"COI.CHECK mode={case['mode']} template={case['template'] or 'auto'} style={case['style'] or 'auto'}",
            "COI.GATE bouncer.inspect_url(source_url)",
            "COI.ROUTE choose style/template strategy",
            "COI.RENDER ffmpeg drawtext pipeline",
            "COI.POSTFLIGHT artifact validation and write",
        ]
        record = {
            "index": case["index"],
            "mode": case["mode"],
            "template": case["template"] or "auto",
            "style": case["style"] or "auto",
            "seed": case["seed"],
            "rationale": case["rationale"],
            "coi_commands": coi_commands,
            "output_path": output_path,
            "success": False,
            "error": "",
        }
        try:
            generated_path = generator.generate(request)
            record["output_path"] = generated_path
            record["success"] = True
        except Exception as exc:
            record["error"] = str(exc)
        records.append(record)
    return records


def build_story_content(records: list[dict], prompt: str, generated_at: str) -> str:
    total = len(records)
    success_count = len([r for r in records if r["success"]])
    failed_count = total - success_count

    parts: list[str] = []
    parts.append("<h2>Incident Summary</h2>")
    parts.append(
        f"<p><strong>Timestamp:</strong> {html_module.escape(generated_at)}<br>"
        f"<strong>Prompt Directive:</strong> {html_module.escape(prompt)}<br>"
        f"<strong>Artifacts Produced:</strong> {success_count}/{total} successful, {failed_count} failed.</p>"
    )
    parts.append("<h2>SCP Narrative Log</h2>")
    parts.append(
        "<p>"
        "Facility observers initially categorized WAFT meme synthesis as low-priority novelty. "
        "Within one run cycle, the system produced coherent, stylistically varied propaganda-grade "
        "artifacts while preserving deterministic replay characteristics under seeded routing. "
        "At that point, containment strategy shifted from suppression to controlled documentation."
        "</p>"
    )
    parts.append(
        "<p>"
        "The memetic output stream was generated through explicit COI command chain checkpoints "
        "(prefight/check/gate/route/render/postflight). This implies WAFT is not only generating "
        "memes, but doing so through rational procedural scaffolding that can be audited."
        "</p>"
    )
    parts.append("<h2>COI Command Trace</h2>")
    parts.append("<div class='note'><div class='note-title'>Canonical Flow</div>")
    parts.append(
        "<pre><code>COI.PREFLIGHT -> COI.CHECK -> COI.GATE -> COI.ROUTE -> COI.RENDER -> COI.POSTFLIGHT</code></pre></div>"
    )
    parts.append("<h2>Artifact Ledger</h2>")

    for record in records:
        parts.append(
            f"<h3>Artifact {record['index']:02d} // mode={html_module.escape(record['mode'])} "
            f"template={html_module.escape(record['template'])} style={html_module.escape(record['style'])}</h3>"
        )
        parts.append(
            "<div class='status-box'>"
            "<div class='status-title'>Rational Thinking</div>"
            f"<p>{html_module.escape(record['rationale'])}</p>"
            "</div>"
        )
        parts.append("<pre><code>")
        for cmd in record["coi_commands"]:
            parts.append(html_module.escape(cmd))
        parts.append("</code></pre>")

        if record["success"]:
            img_uri = Path(record["output_path"]).resolve().as_uri()
            parts.append(
                "<div class='note'>"
                "<div class='note-title'>Generated Meme Artifact</div>"
                f"<p><code>{html_module.escape(str(record['output_path']))}</code></p>"
                f"<img src='{img_uri}' style='width:100%; max-height:4.2in; object-fit:contain; border:2px solid #111; background:#eee;'/>"
                "</div>"
            )
        else:
            parts.append(
                "<div class='warning-block critical'>"
                "<div class='warning-title'>Artifact Generation Failure</div>"
                f"<p>{html_module.escape(record['error'] or 'Unknown error')}</p>"
                "</div>"
            )

    parts.append("<h2>Containment Recommendation</h2>")
    parts.append(
        "<ol>"
        "<li>Maintain COI checkpoint logging for every future meme generation cycle.</li>"
        "<li>Keep seeded replay enabled for forensic reproducibility.</li>"
        "<li>Treat successful meme generation as a documented WAFT capability, not an anecdote.</li>"
        "</ol>"
    )
    return "\n".join(parts)


def generate_dossier(
    project_path: Path,
    prompt: str,
    count: int,
    seed: int | None,
    output_pdf: Path,
    artifacts_dir: Path,
) -> tuple[Path, list[dict]]:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
    cases = build_generation_cases(prompt=prompt, count=count, seed=seed)
    records = run_generation(project_path=project_path, artifacts_dir=artifacts_dir, cases=cases)

    content = build_story_content(records=records, prompt=prompt, generated_at=generated_at)
    doc = BriefDocument(
        title="SCP Discovery Dossier: WAFT Meme Generation Anomaly",
        doc_id=f"DOSSIER-SCP-MEME-{datetime.now().strftime('%Y%m%d')}",
        subtitle="Facility Report on Autonomous Meme Synthesis",
        classification="FACILITY INTERNAL // MEMETIC ANOMALY",
        cover_header="WAFT CONTAINMENT RESEARCH FACILITY",
        cover_metadata={
            "INCIDENT": "MEME-GEN-ALPHA",
            "SYSTEM": "WALT AI / WAFT",
            "REPORT_TYPE": "DISCOVERY DOSSIER",
            "ARTIFACT_BATCH_SIZE": str(count),
            "TIMESTAMP": generated_at,
        },
        cover_warning={
            "message": "Observed capability: WAFT can autonomously generate memetic artifacts with auditable command traces.",
            "severity": "CRITICAL",
        },
        cover_signature={
            "role": "FILED BY",
            "name": "Containment Documentation Cell",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
        cover_footer="SCP STYLE REPORT - INTERNAL FACILITY USE",
        include_system_status=False,
    )
    doc.content_blocks.append(content)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    return doc.generate(output_path=output_pdf), records
