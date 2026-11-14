---
id: TKT-bklg-042
title: "D3 Decide what to do about the largest tracked files"
status: pending
created: 2026-11-14T15:43:40.224Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# D3 Decide what to do about the largest tracked files

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `CT` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** top files by size: `mediawiki-1.45.1.zip` 93.7 MiB; `examples/908530342-Building-AI-Agents-With-LLMs-RAG-And-Knowledge-Graphs-1.pdf` 90.8 MiB; `templates/1789_USA_Miller_Woods_TrailA_Visitors_Guide.pdf` 67.2 MiB; `PITCH_DECK/Waft__Breeding_AI_s_Future_.mp4` 39.3 MiB; three PDFs of 38 to 39 MiB in `_work_efforts/WE-260119-ejtx...`; a 31.1 MiB `.m4a` in `PITCH_DECK`. The `.git` pack is 687 MiB in this shallow clone (L9; the full history may be larger), and the 12 largest top-level folders of tracked files sum to about 1,400 MiB.

**First step.** options: Git LFS, release assets, a data repo, or history filtering (D12). Add a size check to CI (D11).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading D3.
