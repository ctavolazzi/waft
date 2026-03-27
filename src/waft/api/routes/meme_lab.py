from __future__ import annotations

import json
import random
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field

from ...core.meme_dossier import generate_dossier
from ...core.meme_generator import MemeGenerator, MemeRequest
from ..dependencies import get_project_path

router = APIRouter()
MAX_HISTORY_ENTRIES = 2000


class MemeLabGenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    top_text: str = ""
    bottom_text: str = ""
    title: str = ""
    subtitle: str = ""
    image_url: str = ""
    mode: str = "mixed"
    style: str = ""
    template: str = ""
    recipe: str = ""
    seed: int | None = None
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_k: int = Field(default=6, ge=1, le=20)
    creativity: float = Field(default=0.6, ge=0.0, le=1.0)
    punchiness: float = Field(default=0.6, ge=0.0, le=1.0)
    absurdity: float = Field(default=0.4, ge=0.0, le=1.0)
    topical: bool = False


class MemeLabDossierRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    count: int = Field(default=4, ge=1, le=20)
    seed: int | None = None


class MemeLabCookRequest(BaseModel):
    seed: int | None = None
    temperature: float = Field(default=0.9, ge=0.0, le=2.0)
    top_k: int = Field(default=8, ge=1, le=20)
    creativity: float = Field(default=0.8, ge=0.0, le=1.0)
    punchiness: float = Field(default=0.8, ge=0.0, le=1.0)
    absurdity: float = Field(default=0.55, ge=0.0, le=1.0)


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _safe_relative_path(project_path: Path, candidate_path: Path) -> str:
    resolved_project = project_path.resolve()
    resolved_candidate = candidate_path.resolve()
    try:
        return str(resolved_candidate.relative_to(resolved_project))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="file path outside project root") from exc


def _history_file_path(project_path: Path) -> Path:
    return project_path / "_work_efforts" / "reports" / "meme_web_artifacts" / "meme_history.jsonl"


def _append_history_entry(project_path: Path, entry: dict) -> None:
    history_path = _history_file_path(project_path)
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=True) + "\n")
    # Keep history bounded to prevent unbounded local growth.
    lines = history_path.read_text(encoding="utf-8").splitlines()
    if len(lines) > MAX_HISTORY_ENTRIES:
        history_path.write_text(
            "\n".join(lines[-MAX_HISTORY_ENTRIES:]) + "\n",
            encoding="utf-8",
        )


def _read_history_entries(project_path: Path, limit: int = 40) -> list[dict]:
    history_path = _history_file_path(project_path)
    if not history_path.exists():
        return []
    lines = history_path.read_text(encoding="utf-8").splitlines()
    entries: list[dict] = []
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        rel = str(item.get("relative_path", "")).strip()
        if not rel:
            continue
        abs_path = (project_path / rel).resolve()
        try:
            abs_path.relative_to(project_path.resolve())
        except ValueError:
            continue
        if not abs_path.exists() or not abs_path.is_file():
            continue
        item["file_url"] = f"/api/meme-lab/file?path={quote(rel)}"
        entries.append(item)
        if len(entries) >= limit:
            break
    return entries


def _template_seed(template_name: str) -> int:
    digest = hashlib.sha256(template_name.encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % 1_000_000


def _all_template_names(project_path: Path) -> list[str]:
    return [template.name for template in MemeGenerator(project_path=project_path).list_templates()]


def _featured_template_names(project_path: Path) -> list[str]:
    generator = MemeGenerator(project_path=project_path)
    return [template.name for template in generator.list_featured_templates()]


def _build_random_template_request(
    template_name: str,
    output_path: Path,
    seed: int,
    payload: MemeLabGenerateRequest | None = None,
) -> MemeRequest:
    moods = [
        "deploy panic",
        "build passed on first try",
        "CI pipeline chaos",
        "oracle said investigate",
        "feature freeze rebellion",
        "ship-it delusion",
        "bugfix speedrun",
        "meme singularity",
    ]
    base = random.Random(seed)
    prompt = f"{template_name.replace('_', ' ')} // {base.choice(moods)}"
    top = f"{template_name.replace('_', ' ').upper()} MODE"
    bottom = "COOKED BY WAFT"
    if payload:
        prompt = payload.prompt or prompt
        top = payload.top_text or top
        bottom = payload.bottom_text or bottom
    return MemeRequest(
        prompt=prompt,
        top_text=top,
        bottom_text=bottom,
        title=(payload.title if payload else "") or template_name.replace("_", " ").title(),
        subtitle=(payload.subtitle if payload else "") or "SOUNDBOARD RANDOMIZED",
        mode="template",
        template=template_name,
        recipe=(payload.recipe if payload else ""),
        style=(payload.style if payload else ""),
        seed=seed,
        temperature=(payload.temperature if payload else 0.8),
        top_k=(payload.top_k if payload else 8),
        creativity=(payload.creativity if payload else 0.7),
        punchiness=(payload.punchiness if payload else 0.8),
        absurdity=(payload.absurdity if payload else 0.5),
        output=str(output_path),
    )


@router.get("/meme-lab", response_class=HTMLResponse)
async def meme_lab_ui() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>WAFT Meme Kitchen</title>
  <style>
    body { margin: 0; font-family: -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif; background:#0f172a; color:#e2e8f0; }
    #app { max-width: 1440px; margin: 0 auto; padding: 14px; }
    .status { margin: 8px 0; color:#a7f3d0; font-size:13px; min-height:18px; }
    .error { color:#fca5a5; }
    .theater { display:grid; grid-template-columns: 320px 1fr 320px; gap:12px; align-items:start; }
    .card { background:#111827; border:1px solid #334155; border-radius:10px; padding:12px; margin-bottom:12px; }
    .wireframe { border:1px dashed #64748b; }
    .stage { min-height: 78vh; }
    .rail { position: sticky; top: 10px; }
    label { display:block; margin-top:8px; margin-bottom:4px; color:#93c5fd; font-size:13px; }
    input, textarea, select, button { width:100%; box-sizing:border-box; border-radius:8px; border:1px solid #334155; background:#0b1220; color:#e2e8f0; padding:8px; }
    textarea { min-height:84px; resize:vertical; }
    button { cursor:pointer; background:#1d4ed8; border-color:#2563eb; font-weight:600; margin-top:8px; }
    button.secondary { background:#334155; border-color:#475569; }
    .soundboard { display:grid; grid-template-columns:repeat(2, minmax(0, 1fr)); gap:8px; margin-top:8px; }
    .sound-btn { border:1px solid #475569; border-radius:8px; background:#0b1220; padding:8px; cursor:pointer; text-align:left; }
    .sound-btn img { width:100%; height:96px; object-fit:cover; border-radius:6px; border:1px solid #334155; background:#000; }
    .sound-btn .name { font-size:11px; color:#cbd5e1; margin-top:6px; }
    .gallery-main img { width:100%; max-height:460px; object-fit:contain; background:#000; border:1px solid #334155; border-radius:10px; }
    .gallery-strip { display:grid; grid-template-columns:repeat(5, minmax(0,1fr)); gap:6px; margin-top:10px; }
    .thumb { border:1px solid #334155; border-radius:6px; background:#020617; padding:4px; cursor:pointer; }
    .thumb.active { border-color:#38bdf8; }
    .thumb img { width:100%; height:72px; object-fit:cover; border-radius:4px; background:#000; }
    .artifact { margin:10px 0; padding:10px; border:1px solid #334155; border-radius:8px; background:#020617; }
    a { color:#93c5fd; }
    code { background:#1e293b; padding:2px 5px; border-radius:4px; }
    @media (max-width: 1080px) {
      .theater { grid-template-columns: 1fr; }
      .rail { position: static; }
      .stage { min-height: auto; }
      .mobile-wireframe { display:block; }
    }
  </style>
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
</head>
<body>
  <div id="app"></div>
  <script>
    const h = React.createElement;
    const MEME_HISTORY_KEY = "waft_meme_history_v1";

    function App() {
      const [status, setStatus] = React.useState("Ready");
      const [error, setError] = React.useState("");
      const [memeForm, setMemeForm] = React.useState({
        prompt: "WAFT facility kitchen log: autonomous meme synthesis event",
        top_text: "",
        bottom_text: "",
        title: "",
        subtitle: "",
        image_url: "",
        mode: "mixed",
        style: "",
        template: "",
        recipe: "",
        seed: "",
        temperature: 0.9,
        top_k: 8,
        creativity: 0.8,
        punchiness: 0.8,
        absurdity: 0.55,
        topical: false
      });
      const [cookbook, setCookbook] = React.useState([]);
      const [soundboard, setSoundboard] = React.useState([]);
      const [templateCatalog, setTemplateCatalog] = React.useState([]);
      const [dossierForm, setDossierForm] = React.useState({
        prompt: "Facility notes indicate WAFT has begun inventing memes about its own operation.",
        count: 4,
        seed: ""
      });
      const [lastDossier, setLastDossier] = React.useState(null);
      const [memeHistory, setMemeHistory] = React.useState([]);
      const [activeMeme, setActiveMeme] = React.useState(null);
      const [autoplay, setAutoplay] = React.useState(false);
      const [autoplaySeconds, setAutoplaySeconds] = React.useState(4);

      React.useEffect(() => {
        try {
          const raw = localStorage.getItem(MEME_HISTORY_KEY);
          if (raw) {
            const parsed = JSON.parse(raw);
            if (Array.isArray(parsed) && parsed.length > 0) {
              setMemeHistory(parsed);
              setActiveMeme(parsed[0]);
            }
          }
        } catch (_e) {}
      }, []);

      React.useEffect(() => {
        try {
          localStorage.setItem(MEME_HISTORY_KEY, JSON.stringify(memeHistory.slice(0, 40)));
        } catch (_e) {}
      }, [memeHistory]);

      function pushMeme(data) {
        const item = {
          file_url: data.file_url,
          output_path: data.output_path,
          template: data.template || "custom",
          seed: data.seed || null,
          created_at: new Date().toISOString()
        };
        setMemeHistory((prev) => {
          const dedup = prev.filter((x) => x.file_url !== item.file_url);
          return [item, ...dedup].slice(0, 40);
        });
        setActiveMeme(item);
      }

      async function postJson(url, payload) {
        const response = await fetch(url, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || ("Request failed: " + response.status));
        return data;
      }

      async function loadCookbook() {
        try {
          const response = await fetch("/api/meme-lab/cookbook");
          const data = await response.json();
          if (response.ok) setCookbook(data.recipes || []);
        } catch (_e) {}
      }

      async function loadSoundboard() {
        try {
          const response = await fetch("/api/meme-lab/soundboard");
          const data = await response.json();
          if (response.ok) setSoundboard(data.buttons || []);
        } catch (_e) {}
      }

      async function loadTemplateCatalog() {
        try {
          const response = await fetch("/api/meme-lab/templates");
          const data = await response.json();
          if (response.ok) setTemplateCatalog(data.templates || []);
        } catch (_e) {}
      }

      async function loadServerHistory() {
        try {
          const response = await fetch("/api/meme-lab/history?limit=40");
          const data = await response.json();
          if (!response.ok) return;
          const incoming = Array.isArray(data.history) ? data.history : [];
          if (incoming.length === 0) return;
          setMemeHistory((prev) => {
            const map = new Map();
            for (const item of incoming) map.set(item.file_url, item);
            for (const item of prev) map.set(item.file_url, item);
            return Array.from(map.values()).slice(0, 40);
          });
          setActiveMeme((current) => current || incoming[0]);
        } catch (_e) {}
      }

      async function generateMeme() {
        setError("");
        setStatus("Generating meme...");
        try {
          const payload = {
            ...memeForm,
            seed: memeForm.seed === "" ? null : Number(memeForm.seed),
            temperature: Number(memeForm.temperature),
            top_k: Number(memeForm.top_k),
            creativity: Number(memeForm.creativity),
            punchiness: Number(memeForm.punchiness),
            absurdity: Number(memeForm.absurdity)
          };
          const data = await postJson("/api/meme-lab/generate-meme", payload);
          pushMeme(data);
          setStatus("Meme generated.");
        } catch (e) {
          setError(String(e));
          setStatus("Meme generation failed.");
        }
      }

      async function cookFromButton(templateName) {
        setError("");
        setStatus("Cooking random " + templateName + " meme...");
        try {
          const payload = {
            seed: memeForm.seed === "" ? null : Number(memeForm.seed),
            temperature: Number(memeForm.temperature),
            top_k: Number(memeForm.top_k),
            creativity: Number(memeForm.creativity),
            punchiness: Number(memeForm.punchiness),
            absurdity: Number(memeForm.absurdity)
          };
          const data = await postJson("/api/meme-lab/cook-template/" + templateName, payload);
          pushMeme(data);
          setStatus("Cooked random " + templateName + " meme.");
        } catch (e) {
          setError(String(e));
          setStatus("Template cook failed.");
        }
      }

      async function generateDossier() {
        setError("");
        setStatus("Generating dossier and meme batch...");
        try {
          const payload = {
            prompt: dossierForm.prompt,
            count: Number(dossierForm.count),
            seed: dossierForm.seed === "" ? null : Number(dossierForm.seed)
          };
          const data = await postJson("/api/meme-lab/generate-dossier", payload);
          setLastDossier(data);
          setStatus("Dossier generated.");
        } catch (e) {
          setError(String(e));
          setStatus("Dossier generation failed.");
        }
      }

      React.useEffect(() => {
        loadCookbook();
        loadSoundboard();
        loadTemplateCatalog();
        loadServerHistory();
      }, []);

      React.useEffect(() => {
        if (!autoplay || memeHistory.length < 2) return;
        const ms = Math.max(1, Number(autoplaySeconds || 1)) * 1000;
        const timer = setInterval(() => {
          setActiveMeme((current) => {
            if (!current) return memeHistory[0];
            const idx = memeHistory.findIndex((x) => x.file_url === current.file_url);
            if (idx < 0) return memeHistory[0];
            return memeHistory[(idx + 1) % memeHistory.length];
          });
        }, ms);
        return () => clearInterval(timer);
      }, [autoplay, autoplaySeconds, memeHistory]);

      return h("div", null,
        h("h1", null, "WAFT Meme Kitchen Theater Mode"),
        h("div", { className: "status" }, status),
        error ? h("div", { className: "status error" }, error) : null,
        h("div", { className: "theater" },
          h("aside", { className: "rail" },
            h("section", { className: "card wireframe" },
              h("h2", null, "Soundboard"),
              h("p", null, "Click a template image to cook a randomized meme."),
              h("div", { className: "soundboard" },
                ...soundboard.map(item =>
                  h("button", { key: item.template, className: "sound-btn", onClick: () => cookFromButton(item.template) },
                    h("img", { src: item.image_url, alt: item.label }),
                    h("div", { className: "name" }, item.label)
                  )
                )
              )
            ),
            h("section", { className: "card wireframe" },
              h("h3", null, "Template Browser"),
              h("p", null, "Mainstream + WAFT-native clickable formats."),
              h("div", { className: "soundboard" },
                ...templateCatalog.map(item =>
                  h("button", { key: "catalog_" + item.name, className: "sound-btn", onClick: () => cookFromButton(item.name) },
                    h("div", { className: "name" }, item.name.replaceAll("_", " ")),
                    h("div", { className: "name" }, item.category + " • " + item.style)
                  )
                )
              )
            ),
            h("section", { className: "card wireframe" },
              h("h3", null, "Fine-Tune Controls"),
              h("label", null, "Temperature"),
              h("input", { type: "range", min: 0, max: 2, step: 0.05, value: memeForm.temperature, onChange: e => setMemeForm({ ...memeForm, temperature: e.target.value }) }),
              h("label", null, "Top-K Randomness"),
              h("input", { type: "range", min: 1, max: 20, step: 1, value: memeForm.top_k, onChange: e => setMemeForm({ ...memeForm, top_k: e.target.value }) }),
              h("label", null, "Creativity"),
              h("input", { type: "range", min: 0, max: 1, step: 0.05, value: memeForm.creativity, onChange: e => setMemeForm({ ...memeForm, creativity: e.target.value }) }),
              h("label", null, "Punchiness"),
              h("input", { type: "range", min: 0, max: 1, step: 0.05, value: memeForm.punchiness, onChange: e => setMemeForm({ ...memeForm, punchiness: e.target.value }) }),
              h("label", null, "Absurdity"),
              h("input", { type: "range", min: 0, max: 1, step: 0.05, value: memeForm.absurdity, onChange: e => setMemeForm({ ...memeForm, absurdity: e.target.value }) })
            )
          ),
          h("main", { className: "stage" },
            memeHistory.length > 0 ? h("section", { className: "card wireframe" },
              h("h2", null, "Finished Memes"),
              h("p", null, "Your generated memes stay here as an evolving gallery."),
              h("div", { style: { display: "grid", gridTemplateColumns: "1fr 110px", gap: "8px", alignItems: "end" } },
                h("div", null,
                  h("label", null, "Theater Autoplay"),
                  h("select", { value: autoplay ? "on" : "off", onChange: e => setAutoplay(e.target.value === "on") },
                    h("option", { value: "off" }, "off"),
                    h("option", { value: "on" }, "on")
                  )
                ),
                h("div", null,
                  h("label", null, "Seconds"),
                  h("input", { type: "number", min: 1, max: 30, value: autoplaySeconds, onChange: e => setAutoplaySeconds(Number(e.target.value) || 1) })
                )
              ),
              activeMeme ? h("div", { className: "gallery-main" },
                h("img", { src: activeMeme.file_url, alt: "Active generated meme" }),
                h("p", null, h("code", null, activeMeme.output_path))
              ) : null,
              h("div", { className: "gallery-strip" },
                ...memeHistory.map((item, idx) =>
                  h("div", { key: item.file_url + idx, className: "thumb " + (activeMeme && activeMeme.file_url === item.file_url ? "active" : ""), onClick: () => setActiveMeme(item) },
                    h("img", { src: item.file_url, alt: item.template || "meme" })
                  )
                )
              )
            ) : null
          ),
          h("aside", { className: "rail" },
            h("section", { className: "card wireframe" },
              h("h2", null, "Manual Cook"),
              h("label", null, "Prompt"),
              h("textarea", { value: memeForm.prompt, onChange: e => setMemeForm({ ...memeForm, prompt: e.target.value }) }),
              h("label", null, "Top Text"),
              h("input", { value: memeForm.top_text, onChange: e => setMemeForm({ ...memeForm, top_text: e.target.value }) }),
              h("label", null, "Bottom Text"),
              h("input", { value: memeForm.bottom_text, onChange: e => setMemeForm({ ...memeForm, bottom_text: e.target.value }) }),
              h("label", null, "Mode"),
              h("select", { value: memeForm.mode, onChange: e => setMemeForm({ ...memeForm, mode: e.target.value }) },
                h("option", { value: "mixed" }, "mixed"),
                h("option", { value: "cooking" }, "cooking"),
                h("option", { value: "original" }, "original")
              ),
              h("label", null, "Recipe"),
              h("select", { value: memeForm.recipe, onChange: e => setMemeForm({ ...memeForm, recipe: e.target.value }) },
                h("option", { value: "" }, "auto"),
                ...cookbook.map(recipe =>
                  h("option", { key: recipe.name, value: recipe.name }, recipe.name + " (" + recipe.style + ")")
                )
              ),
              h("label", null, "Seed (optional)"),
              h("input", { value: memeForm.seed, onChange: e => setMemeForm({ ...memeForm, seed: e.target.value }) }),
              h("button", { onClick: generateMeme }, "Cook Meme")
            ),
            h("section", { className: "card wireframe" },
              h("h2", null, "Dossier Generator"),
              h("label", null, "Discovery Prompt"),
              h("textarea", { value: dossierForm.prompt, onChange: e => setDossierForm({ ...dossierForm, prompt: e.target.value }) }),
              h("label", null, "Meme Count"),
              h("input", { type: "number", min: 1, max: 20, value: dossierForm.count, onChange: e => setDossierForm({ ...dossierForm, count: e.target.value }) }),
              h("label", null, "Seed (optional)"),
              h("input", { value: dossierForm.seed, onChange: e => setDossierForm({ ...dossierForm, seed: e.target.value }) }),
              h("button", { className: "secondary", onClick: generateDossier }, "Generate Dossier PDF"),
              lastDossier ? h("div", { className: "artifact" },
                h("p", null, "PDF: ", h("code", null, lastDossier.pdf_path)),
                h("p", null, h("a", { href: lastDossier.pdf_url, target: "_blank" }, "Open generated dossier PDF")),
                h("p", null, "Artifacts: ", String(lastDossier.artifacts.length))
              ) : null
            )
          )
        )
      );
    }

    ReactDOM.createRoot(document.getElementById("app")).render(h(App));
  </script>
</body>
</html>"""


@router.post("/meme-lab/generate-meme")
async def generate_meme(payload: MemeLabGenerateRequest, http_request: Request):
    project_path = get_project_path(http_request)
    stamp = _utc_stamp()
    output_path = project_path / "_work_efforts" / "reports" / "meme_web_artifacts" / f"meme_{stamp}.jpg"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    request = MemeRequest(
        prompt=payload.prompt,
        top_text=payload.top_text,
        bottom_text=payload.bottom_text,
        title=payload.title,
        subtitle=payload.subtitle,
        image_url=payload.image_url,
        mode=payload.mode,  # type: ignore[arg-type]
        style=payload.style,
        template=payload.template,
        recipe=payload.recipe,
        seed=payload.seed,
        temperature=payload.temperature,
        top_k=payload.top_k,
        creativity=payload.creativity,
        punchiness=payload.punchiness,
        absurdity=payload.absurdity,
        topical=payload.topical,
        output=str(output_path),
    )

    final_path = MemeGenerator(project_path=project_path).generate(request)
    rel_path = _safe_relative_path(project_path, final_path)
    history_entry = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "template": payload.template or "custom",
        "seed": payload.seed,
        "output_path": str(final_path),
        "relative_path": rel_path,
    }
    _append_history_entry(project_path, history_entry)
    return {
        "output_path": str(final_path),
        "relative_path": rel_path,
        "file_url": f"/api/meme-lab/file?path={quote(rel_path)}",
    }


@router.get("/meme-lab/cookbook")
async def cookbook(http_request: Request):
    project_path = get_project_path(http_request)
    recipes = [
        {"name": recipe.name, "style": recipe.style, "description": recipe.description}
        for recipe in MemeGenerator(project_path=project_path).list_recipes()
    ]
    return {"recipes": recipes}


@router.get("/meme-lab/templates")
async def templates(http_request: Request):
    project_path = get_project_path(http_request)
    templates_data = [
        {
            "name": template.name,
            "style": template.style,
            "description": template.description,
            "category": template.category,
            "featured": template.featured,
        }
        for template in MemeGenerator(project_path=project_path).list_templates()
    ]
    return {"templates": templates_data}


@router.post("/meme-lab/generate-dossier")
async def generate_dossier_pdf(payload: MemeLabDossierRequest, http_request: Request):
    project_path = get_project_path(http_request)
    stamp = _utc_stamp()
    artifacts_dir = (
        project_path / "_work_efforts" / "reports" / "meme_web_artifacts" / f"dossier_{stamp}"
    )
    output_pdf = (
        project_path / "_work_efforts" / "reports" / f"SCP_WAFT_MEME_DISCOVERY_DOSSIER_WEB_{stamp}.pdf"
    )
    final_pdf, records = generate_dossier(
        project_path=project_path,
        prompt=payload.prompt,
        count=payload.count,
        seed=payload.seed,
        output_pdf=output_pdf,
        artifacts_dir=artifacts_dir,
    )

    pdf_rel = _safe_relative_path(project_path, final_pdf)
    artifacts = []
    for record in records:
        if not record["success"]:
            continue
        record_rel = _safe_relative_path(project_path, Path(record["output_path"]))
        artifacts.append(
            {
                "path": str(record["output_path"]),
                "relative_path": record_rel,
                "url": f"/api/meme-lab/file?path={quote(record_rel)}",
            }
        )

    return {
        "pdf_path": str(final_pdf),
        "pdf_relative_path": pdf_rel,
        "pdf_url": f"/api/meme-lab/file?path={quote(pdf_rel)}",
        "artifacts": artifacts,
        "total": len(records),
        "successes": len(artifacts),
    }


@router.get("/meme-lab/soundboard")
async def soundboard(http_request: Request):
    project_path = get_project_path(http_request)
    buttons_dir = project_path / "_work_efforts" / "reports" / "meme_web_artifacts" / "buttons"
    buttons_dir.mkdir(parents=True, exist_ok=True)
    generator = MemeGenerator(project_path=project_path)
    buttons = []

    for template_name in _featured_template_names(project_path):
        button_path = buttons_dir / f"{template_name}.jpg"
        if not button_path.exists():
            request = _build_random_template_request(
                template_name=template_name,
                output_path=button_path,
                seed=_template_seed(template_name),
            )
            try:
                generator.generate(request)
            except Exception:
                # Keep going; broken templates should not block page.
                pass
        rel_path = _safe_relative_path(project_path, button_path)
        buttons.append(
            {
                "template": template_name,
                "label": template_name.replace("_", " ").title(),
                "image_url": f"/api/meme-lab/file?path={quote(rel_path)}",
                "cook_url": f"/api/meme-lab/cook-template/{template_name}",
            }
        )
    return {"buttons": buttons}


@router.post("/meme-lab/cook-template/{template_name}")
async def cook_template(
    template_name: str,
    payload: MemeLabCookRequest,
    http_request: Request,
):
    project_path = get_project_path(http_request)
    if template_name not in _all_template_names(project_path):
        raise HTTPException(status_code=404, detail="unknown template")
    stamp = _utc_stamp()
    output_path = (
        project_path
        / "_work_efforts"
        / "reports"
        / "meme_web_artifacts"
        / f"{template_name}_{stamp}.jpg"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    seed = payload.seed if payload.seed is not None else random.randint(10_000, 999_999)
    request = _build_random_template_request(
        template_name=template_name,
        output_path=output_path,
        seed=seed,
        payload=MemeLabGenerateRequest(
            prompt=f"{template_name.replace('_', ' ')} random cook",
            mode="cooking",
            temperature=payload.temperature,
            top_k=payload.top_k,
            creativity=payload.creativity,
            punchiness=payload.punchiness,
            absurdity=payload.absurdity,
        ),
    )
    final_path = MemeGenerator(project_path=project_path).generate(request)
    rel_path = _safe_relative_path(project_path, final_path)
    history_entry = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "template": template_name,
        "seed": seed,
        "output_path": str(final_path),
        "relative_path": rel_path,
    }
    _append_history_entry(project_path, history_entry)
    return {
        "template": template_name,
        "seed": seed,
        "output_path": str(final_path),
        "file_url": f"/api/meme-lab/file?path={quote(rel_path)}",
    }


@router.get("/meme-lab/history")
async def meme_history(http_request: Request, limit: int = Query(40, ge=1, le=200)):
    project_path = get_project_path(http_request)
    return {"history": _read_history_entries(project_path, limit=limit)}


@router.get("/meme-lab/file")
async def get_meme_lab_file(http_request: Request, path: str = Query(..., min_length=1)):
    project_path = get_project_path(http_request).resolve()
    target = (project_path / path).resolve()
    reports_root = (project_path / "_work_efforts" / "reports").resolve()
    try:
        target.relative_to(project_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="invalid file path") from exc
    try:
        target.relative_to(reports_root)
    except ValueError as exc:
        raise HTTPException(status_code=403, detail="file path not permitted") from exc
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(str(target), filename=target.name)
