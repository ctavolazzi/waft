---
id: TKT-bklg-059
title: "E8 Review the Electron app's security settings"
status: pending
created: 2026-11-14T15:43:40.225Z
parent: WE-261114-bklg
labels: ['investigation', 'waft']
---

# E8 Review the Electron app's security settings

Part of [[WE-261114-bklg_index|WE-261114-bklg]]

## Status

- [ ] Not started

## Notes

Tags: `M` `agent` `P2`  (M measured, R read, Q question; owner agent, CT or research; P1 first)

**Evidence.** `waft_desktop/electron/main.js` (checked by me): `contextIsolation: true` and `nodeIntegration: false` but `sandbox: false` (lines 279 to 281); the backend is started with `spawn('waft', ['serve', ...], {shell: true})` (line 80); Reload, Force Reload and Toggle Developer Tools are in the right-click menu (lines 325 to 327; whether they are gated on dev mode was not checked); six debug `fetch` calls to `http://127.0.0.1:7248/...` remain (E5); Electron is `^28.0.0` locked at 28.3.3, an old major. A helper agent also read, and I did not check: the preload exposes only three fixed invoke calls plus listeners, but `removeAllListeners(channel)` forwards any channel name; there is no Content-Security-Policy and no `setWindowOpenHandler` or `will-navigate` guard; on macOS the backend respawns after the window closes; electron-builder ships only `main.js`, `preload.js` and `package.json`, so a packaged build cannot load its UI. `dnd_campaign_desktop_app/electron/main.js` and `recap_review_app/frontend/src/main.js` reportedly use the same `sandbox: false` pattern and were not reviewed.

**First step.** set `sandbox: true`, drop `shell: true`, add a CSP and navigation guards, gate DevTools on dev mode, upgrade Electron to a supported major, then check the two other Electron apps (or retire them with D10).

Full context and the baseline: [INVESTIGATION_BACKLOG.md](../INVESTIGATION_BACKLOG.md), heading E8.
