---
name: Site Visual Upgrade
overview: Upgrade the CFL Wiki from bare-bones to a polished makerspace site with better styling, responsive images, and improved layout.
todos:
  - id: restart-jekyll
    content: Check/restart Jekyll server and verify pages render
    status: completed
  - id: fix-image
    content: Replace placeholder with local cfl-kiosk.jpg
    status: completed
    dependencies:
      - restart-jekyll
  - id: upgrade-css
    content: Overhaul main.css with dark makerspace theme
    status: completed
    dependencies:
      - fix-image
  - id: improve-layout
    content: Update default.html layout structure
    status: completed
    dependencies:
      - upgrade-css
  - id: verify-push
    content: Test all pages locally, commit and push
    status: completed
    dependencies:
      - improve-layout
---

# CFL Wiki Visual Upgrade

## Phase 1: Restart and Verify

1. **Check Jekyll server status** - See if it's still running, restart if needed
2. **Verify current state** - Curl pages to confirm they render

## Phase 2: Fix the Image

3. **Replace placeholder image** - Use the existing `assets/img/cfl-kiosk.jpg` from the repo instead of the external placeholder (more reliable, already there)

## Phase 3: Upgrade Styling

4. **Overhaul `assets/css/main.css`**:

- Dark theme with makerspace vibe (dark background, light text)
- Better typography (JetBrains Mono or similar for that maker/coder feel)
- Accent color (orange/amber to match fab lab energy)
- Responsive images (`max-width: 100%`)
- Better link styling with hover effects
- Improved spacing and visual hierarchy
- Code blocks that look good

## Phase 4: Improve Layout

5. **Update `_layouts/default.html`**:

- Proper semantic structure
- Better nav styling
- Cleaner footer
- Container with better max-width handling

## Phase 5: Verify

6. **Test locally** - Curl all pages, verify styling, check image loads
7. **Commit and push** - Update the PR

## Files to Modify

| File | Changes |
|------|---------|
| [`assets/css/main.css`](assets/css/main.css) | Complete restyle |
| [`_layouts/default.html`](_layouts/default.html) | Layout improvements |
| [`_wiki/getting-started.mkd`](_wiki/getting-started.mkd) | Use local image |

## Expected Result

- Dark-themed makerspace aesthetic
- Responsive, professional look
- All pages render correctly at http://127.0.0.1:4000
- Image displays properly
- Ready for PR merge