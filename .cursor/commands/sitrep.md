# Sitrep

Generate a current recent-work sitrep and update the persistent hub page.

## Usage

```text
/sitrep
```

## Execution

1. Run:
   `PYENV_VERSION=3.14.3 python scripts/work_effort_report.py`
2. Confirm artifacts generated in `_work_efforts/reports/`:
   - current markdown
   - current HTML
   - current PDF
   - `report_hub_latest.html`
3. Confirm only the hub page opens automatically in Chrome.
4. Confirm runtime trace is printed in terminal and includes:
   - expected Python target,
   - resolved interpreter path/version,
   - `PYENV_VERSION` value,
   - explicit status + reason.

## Notes

- Markdown is kept as a source artifact and linked from the hub.
- Hub archive combines:
  - discovered report files on disk, and
  - explicit entries maintained in `report_index.json`.
- Hub status cards now show:
  - freshness (`fresh`/`aging`/`stale`) and time since latest run,
  - quality score (`0-100`) + quality tier (`excellent`/`good`/`fair`/`poor`),
  - delta row for missing artifacts and quality trend vs prior run.
- Hub archive controls:
  - search by run id/title/date/content text,
  - filters by quality tier, date window, and artifact completeness,
  - sort by newest, quality high-to-low, or stale first.
- Hub trends + explorer:
  - inline charts for freshness, quality trend, and artifact completeness,
  - throughput chips (24h/7d/30d),
  - explorer panel grouped by day with quick HTML/PDF/MD links,
  - health panel for disk/index drift (disk-only and indexed-only run counts).
- Golden nugget + reverse-cone navigation:
  - plain-language abstract at top ("golden nugget"),
  - progressive rabbit-hole navigation chips (summary -> evidence -> deep dives).
- 404 prompt configurator:
  - hub includes a route-check panel that pre-fills a copyable LLM build prompt when a route is missing.
  - teaching/test page: `docs/404_PROMPT_CONFIGURATOR_TEST.html`
  - standalone utility:
    - `PYENV_VERSION=3.14.3 python scripts/site_prompt_configurator.py --endpoint "/your/missing/route"`
- Runtime policy:
  - `/sitrep` should be invoked with `PYENV_VERSION=3.14.3`.
  - The script prints a runtime trace and reason every run so version drift is visible immediately.
