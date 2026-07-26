# Field manual test harness

Headless-Chrome checks for [`../index.html`](../index.html). No npm install, no
`node_modules` — a small Chrome DevTools Protocol driver on Node 22's native
`WebSocket`.

```bash
node interact.js    # 24 checks: drive every instrument, assert the state it lands in
node reduced.js     # 10 checks: prefers-reduced-motion emulation
node shots.js       # section screenshots into ./shots/
```

Requires Node >= 22 (for the global `WebSocket`) and Google Chrome at
`/Applications/Google Chrome.app`. Each exits non-zero if a check fails or the
page logged a console error.

## What the suites cover

`interact.js` clicks through the page the way a reader would: it edits the
Genome Lab textarea and confirms the digest changes, that the status flips to
MUTATED, that adopting promotes the child and advances the generation, and that
the displayed hash equals a `crypto.subtle` digest of the textarea taken
independently in the page. It answers the Stabilization Chamber correctly and
then incorrectly, checking the artifact seals, energy is paid, integrity drops
and the round advances. It waits out the scaffold stream, rolls the d20 and
asserts the face changes mid-tumble before settling, and checks nav scroll-spy
and the progress rail.

`reduced.js` re-runs under emulated `prefers-reduced-motion: reduce` and asserts
the opposite property: nothing animates, but every widget still rests in a
complete, readable state — full digest, fracture rendered, artifact *not*
corrupting, scaffold fully written, tree fully grown, stack assembled,
simulation auto-paused with the dish still painted.

## Two traps worth knowing

**Never use `--virtual-time-budget` for this page.** It collapses `setTimeout`
chains into a single frame, so `IntersectionObserver` never observes the
intermediate scroll positions that boot the widgets, and CSS
`scroll-behavior: smooth` never settles. The first version of this harness used
it and reported the whole page dead. `cdp.js` drives real time instead.

**The driver takes a random debug port per run and kills its whole process
group on exit.** A fixed port silently reconnects to a leftover browser from an
earlier run, and if that window is occluded, `requestAnimationFrame` never fires
and `IntersectionObserver` never delivers. Every rAF-driven counter then reads
frozen and every scroll-booted widget looks broken — 11 of 24 checks failed that
way against a page that was entirely correct. The anti-backgrounding flags in
`cdp.js` exist for the same reason; don't drop them.
