---
id: TKT-bklg-052
title: "E1 Rotate or retire the two crypto keys that are still public in history"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E1 Rotate or retire the two crypto keys that are still public in history

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `R` `CT` `P1`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `_pyrite/.waft/.pyrite_secret_key` (a Fernet key) and the D&D realm `.hmac_key` were tracked in this public repo; untracked by commits 67ce2ed8 and 3f8cb670. Commit 67ce2ed8 says the Pexels key, the Pixabay key and the API token were rotated; it does not say the Fernet key was. Commit dd1992fd says both crypto keys must be kept locally because deleting them orphans encrypted secrets and invalidates realm state. So both values stay public and valid. The date the keys first entered history is unknown: the oldest commit visible here, `dc8e4d2a` (2026-01-25), is the shallow boundary and so shows every file as added (L9).

**First step.** inventory what is encrypted or signed with each; rotate with a re-encrypt or re-sign migration; generate on demand afterwards.

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E1.
