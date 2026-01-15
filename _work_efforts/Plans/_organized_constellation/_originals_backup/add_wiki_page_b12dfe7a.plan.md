---
name: Add Wiki Page
overview: Delete the unnecessary Gemfile, create a properly-formatted wiki page matching existing conventions, and push to GitHub Pages for build/deploy.
todos:
  - id: delete-gemfile
    content: Delete the Gemfile (unnecessary cruft)
    status: completed
  - id: create-wiki-page
    content: Create _wiki/getting-started.mkd with content
    status: completed
    dependencies:
      - delete-gemfile
  - id: commit-push
    content: Commit and push to GitHub
    status: completed
    dependencies:
      - create-wiki-page
  - id: verify-live
    content: Verify page appears on live site
    status: completed
    dependencies:
      - commit-push
---

# Add Wiki Page to CFL Site

## Cleanup

1. **Delete Gemfile** - Remove `/Users/ctavolazzi/Code/chicofablab.github.io-1/Gemfile` (cruft I added; GitHub Pages ignores it per `_config.yml` exclude list)

## Create Wiki Page

2. **Create `_wiki/getting-started.mkd`** - Use `.mkd` extension to match existing pages ([`cfl-kiosk.mkd`](_wiki/cfl-kiosk.mkd), [`cfl-task-dashboard.mkd`](_wiki/cfl-task-dashboard.mkd))

Front matter and content:

```yaml
---
title: Getting Started
---
```

Content will include:

- Welcome heading
- Location info (603 Orange Street, Chico, CA - from footer)
- What CFL is (makerspace/fab lab)
- How to visit/join
- Links to existing wiki pages (kiosk, task dashboard)

## Deploy

3. **Commit and push** to GitHub - GitHub Pages builds automatically; no local Jekyll needed

## Verification

4. **Check live site** at https://chicofl.org after GitHub Actions completes (~1-2 min):

   - Homepage lists new page
   - Page renders at /wiki/getting-started
   - Links work

No local development - network restrictions make `bundle install` impossible, and it's unnecessary for this task.