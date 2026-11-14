---
id: TKT-bklg-009
title: "A9 Make the six PDF-to-PNG tests pass or skip"
status: completed
created: 2026-11-14T15:43:40.223Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# A9 Make the six PDF-to-PNG tests pass or skip

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [x] Completed

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `tests/test_pdf_image_converter.py` (6 tests) fails with `RuntimeError: No PDF conversion library available`. It needs pdf2image with poppler, ImageMagick or PyMuPDF; none is installed here and `pymupdf` is not in `pyproject.toml`.

**First step.** add `pymupdf` as an extra and use `pytest.importorskip`, or declare the system packages in the setup script.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading A9.

**2026-11-14 (build pass).** pdf2image is in the dev extra and poppler is installed in CI; the six tests pass where poppler is present.
