# WAFT Meme Generator Guide

`waft meme` adds meme rendering to WAFT with secure URL checks and FFmpeg output.

## Commands

```bash
waft meme styles
waft meme templates
waft meme cooking
waft meme generate "when tests pass on first run"
waft generate meme generate "when tests pass on first run"
```

## Backend Behavior

WAFT currently supports one rendering backend in production:

- `WAFT_MEME_BACKEND=ffmpeg` (default)

Backend notes:

- If `WAFT_MEME_BACKEND` is set to anything else, meme generation fails fast with an explicit backend error.
- This is intentional: it reserves a stable contract for future optional backends (for example, `pillow`) without changing current command/API behavior.
- FFmpeg binary path remains configurable with `WAFT_FFMPEG_BIN`.

### Security Check

Run a local hardening audit before generating:

```bash
waft meme security-check
waft generate meme security-check
```

What it validates:

- `MemeGenerator.max_download_bytes` is present and bounded (non-zero, <= 15 MB).
- Meme history retention constant (`MAX_HISTORY_ENTRIES`) exists and is bounded.
- Meme file serving policy is restricted to the `_work_efforts/reports` subtree.

Behavior:

- Prints compact `PASS`/`FAIL` lines for each check.
- Returns exit code `0` when all checks pass.
- Returns exit code `1` when one or more critical checks fail.

### Generate Options

```bash
waft meme generate "ship it" \
  --top "WHEN THE BUILD IS GREEN" \
  --bottom "DEPLOY FRIDAY" \
  --mode mixed \
  --seed 42 \
  --output ./meme.jpg
```

- `--mode`: `mixed|cooking|template|original`
- `--style`: force style (`top_bottom`, `top_band`, `motivational`)
- `--template`: legacy template hint (`drake`, `distracted_boyfriend`, `expanding_brain`, `inspiring_poster`)
- `--recipe`: cooking recipe preset (`burnt_ember`, `midnight_braise`, `containment_chowder`, `chaos_reduction`, `forbidden_frittata`, `facility_feast`)
- `--temperature`: 0.0-2.0 tuning control
- `--top-k`: 1-20 flavor sampling depth
- `--creativity`: 0.0-1.0 novelty pressure
- `--punchiness`: 0.0-1.0 caption intensity
- `--absurdity`: 0.0-1.0 chaos factor
- `--topical`: optional trend-assisted prompt enrichment
- `--image-url`: explicit image source URL
- `--config`: JSON request override file for full parameterized generation runs

## Style and Template Matrix

| Style | Description | Typical Use |
|---|---|---|
| `top_bottom` | Classic top/bottom text overlay | Fast meme captions |
| `top_band` | White band headline + bottom text | News-like caption memes |
| `motivational` | Framed poster + title/subtitle | Demotivational/motivational posters |

| Template | Default Style |
|---|---|
| `drake` | `top_bottom` |
| `distracted_boyfriend` | `top_bottom` |
| `expanding_brain` | `top_bottom` |
| `inspiring_poster` | `motivational` |

## Cooking Recipes

| Recipe | Default Style | Flavor |
|---|---|---|
| `burnt_ember` | `top_bottom` | Spicy two-line roast format |
| `midnight_braise` | `top_band` | Headline-first dark humor plating |
| `containment_chowder` | `motivational` | Incident-poster anomaly vibe |
| `chaos_reduction` | `top_bottom` | Before/after control-room punchline |
| `forbidden_frittata` | `top_band` | Classified banner + footer sting |
| `facility_feast` | `motivational` | Full SCP dossier poster energy |

## Meme Soundboard

The web kitchen now exposes 8 image buttons (popular meme styles) that act like a soundboard:

- `drake`
- `distracted_boyfriend`
- `expanding_brain`
- `two_buttons`
- `change_my_mind`
- `woman_yelling_cat`
- `gru_plan`
- `inspiring_poster`

Clicking a button triggers a randomized meme cook route for that template style.

## Template Catalog Layer

The web UI now includes a "Template Browser" card for mainstream + WAFT-native clickable formats.

API endpoints:

- `GET /api/meme-lab/templates` - full template catalog with categories
- `GET /api/meme-lab/soundboard` - featured templates (default 8) for quick clicks
- `POST /api/meme-lab/cook-template/{template_name}` - cook by any known template name

## Fine-Tuning Controls

In the Meme Kitchen page, controls below the soundboard let you tune outputs like a model:

- `temperature` (0.0-2.0)
- `top_k` (1-20)
- `creativity` (0.0-1.0)
- `punchiness` (0.0-1.0)
- `absurdity` (0.0-1.0)

These influence prompt flavor injection, caption intensity, and random variation.

## Theater Autoplay and History

The theater view now supports:

- **Autoplay toggle** (`off|on`) to cycle finished memes on stage
- **Autoplay seconds** control (1-30s) for slideshow cadence
- **Server-side history endpoint**: `GET /api/meme-lab/history?limit=40`

History is persisted in:

- `_work_efforts/reports/meme_web_artifacts/meme_history.jsonl`

The UI merges server history with browser `localStorage` so generated memes survive refreshes and can be replayed in theater mode.

## Auto Demo Script

Seed a ready-to-view theater demo and open in Chrome:

```bash
PYENV_VERSION=3.14.3 python scripts/meme_lab_auto_demo.py --host 127.0.0.1 --port 8012
```

If the API is not running yet:

```bash
PYENV_VERSION=3.14.3 python -m uvicorn src.waft.api.main:app --host 127.0.0.1 --port 8012 --reload
```

## Topical Mode

Topical mode is optional. If `--topical` is used and `WAFT_MEME_TREND_URL` is configured, WAFT tries to fetch trend text and enrich the prompt. If this fails for any reason, generation falls back to prompt-only behavior.

## Security Notes

- Source image and topical URLs are checked with WAFT `Bouncer` rules before fetch.
- Blocked hosts/schemes are rejected before download.

## Troubleshooting

| Failure Signature | Likely Cause | Operator Action |
|---|---|---|
| `ffmpeg binary '...' not found` | FFmpeg missing from PATH or custom path unset | Install ffmpeg (`brew install ffmpeg` or `sudo apt install ffmpeg`) or set `WAFT_FFMPEG_BIN=/path/to/ffmpeg` |
| `Unsupported meme backend` | `WAFT_MEME_BACKEND` not set to `ffmpeg` | Set `WAFT_MEME_BACKEND=ffmpeg` |
| `ffmpeg failed: ...` | FFmpeg filter/render error on input text/image | Retry with shorter text and confirm source image is valid |
| `ffmpeg completed but no output file was created` | FFmpeg run succeeded but output write failed | Check output directory permissions and path validity |
| `URL blocked by Bouncer` | Source URL violates bouncer policy | Use an allowlisted public image host |
| `image URL did not return image content` | Remote URL returned non-image response | Provide a direct image URL |
| `image URL exceeds maximum allowed download size` | Remote image exceeds 15 MB cap | Use a smaller image source |

## Local Validation Commands

Use this set to validate meme behavior quickly:

```bash
PYENV_VERSION=3.14.3 python -m pytest tests/test_meme_generator.py -q
PYENV_VERSION=3.14.3 python -m pytest tests/test_meme_cli.py -q
PYENV_VERSION=3.14.3 python -m pytest tests/test_meme_robustness_matrix.py -q
PYENV_VERSION=3.14.3 python -m pytest tests/api/test_meme_lab.py -q
PYENV_VERSION=3.14.3 python -m pytest tests/test_commands.py -k "meme or security_check" -q
```

Full targeted hardening gate:

```bash
PYENV_VERSION=3.14.3 python -m pytest tests/test_meme_generator.py tests/test_meme_cli.py tests/test_meme_robustness_matrix.py tests/api/test_meme_lab.py tests/test_commands.py -k "meme or security_check" -q
```
