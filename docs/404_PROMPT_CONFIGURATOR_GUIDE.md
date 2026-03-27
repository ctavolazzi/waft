# 404 Prompt Configurator Guide

Use the 404 Prompt Configurator to turn missing routes into build-ready prompts instead of dead-end pages.

## What It Does

- Detects route/endpoint candidates that do not exist yet.
- Captures local page context (title, styles, components, visible structure).
- Lets you add goal, wireframe notes, and optional screenshot reference.
- Generates a copy-ready LLM prompt for implementation continuation.

## In Sitrep Hub

Open `_work_efforts/reports/report_hub_latest.html` and use **404 Prompt Configurator** near the bottom of the page.

## Teaching/Test Page

Open `docs/404_PROMPT_CONFIGURATOR_TEST.html`.

This page is intentionally instructional and includes:
- guided flow,
- prefill actions,
- route check behavior,
- prompt generation and copy button.

## Standalone Utility

```bash
PYENV_VERSION=3.14.3 python scripts/site_prompt_configurator.py \
  --endpoint "/missing/route" \
  --goal "Show top abstract and deep evidence explorer"
```

Outputs:
- `_work_efforts/reports/route_prompt_*.md`
- `_work_efforts/reports/route_wireframe_*.txt`
