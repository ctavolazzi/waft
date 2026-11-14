---
id: TKT-bklg-058
title: "E7 Audit dependencies for known vulnerabilities"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E7 Audit dependencies for known vulnerabilities

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `pip-audit` on the 120 distinct packages locked for the `dev` extra (2026-11-14): 21 packages have advisories (281 as the tool counts them, with duplicates). Most list a fix: cryptography 46.0.6 to 46.0.7, pillow 12.1.1 to 12.2.0, pypdf 6.9.2 to 6.10.0, starlette 1.0.0 to 1.0.1, urllib3 2.6.3 to 2.7.0, fpdf2 2.8.7 to 2.8.8, anthropic 0.86.0 to 0.87.0, and smaller ones (anyio, brotli, brotlicffi, certifi, gitpython, httplib2, idna, pyasn1, pydantic-settings, pygments, pytest, soupsieve, tornado); weasyprint 68.1 lists no fix. pypdf, pillow, weasyprint and fpdf2 parse files that users supply. `npm audit` was not run.

**First step.** upgrade the fixable ones with `uv lock --upgrade-package`, rerun the suite, decide about weasyprint, add pip-audit to CI (C6); run `npm audit` for the front ends you keep.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E7.
