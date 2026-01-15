---
name: Hotline Button Clarity
overview: Update the "Weird Question Hotline" button's subtext to clarify it sends an email and that the under-an-hour response time starts when you see the message.
todos:
  - id: setup-work-efforts
    content: Create _work_efforts_ folder structure with Johnny Decimal system
    status: completed
  - id: update-subtext
    content: Update hotline subtext in dist/index.html with clearer copy
    status: completed
    dependencies:
      - setup-work-efforts
  - id: create-work-effort-doc
    content: Document the change in work effort file
    status: completed
    dependencies:
      - update-subtext
---

# Improve Weird Question Hotline Button Clarity

## Current State
The button in [`dist/index.html`](dist/index.html) (lines 707-711):
```html
<div class="hotline-wrapper">
    <a href="mailto:christopher@fogsift.com?subject=Weird%20Question%20Hotline" class="hotline-button">
        Weird Question Hotline
    </a>
    <div class="hotline-subtext">Got a random weird question? I bet I can answer it in under an hour.</div>
```

## Proposed Changes

### 1. Update the subtext copy
Change the subtext to include "click to email" and clarify the timing:

**Before:**
> Got a random weird question? I bet I can answer it in under an hour.

**After:**
> Click to email me your weird question. Once I see it, I'll respond and start working on it within the hour.

This keeps the playful tone while making it clear:
- Clicking sends an email
- The timer starts when *you* see it (not when they send it)

### 2. Set up work effort tracking
Create the `_work_efforts_` folder using Johnny Decimal:
```
_work_efforts_/
    00-09_site_improvements/
        00_ui_ux/
            00.00_index.md
            00.01_hotline-button-clarity.md
```