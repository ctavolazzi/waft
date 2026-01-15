---
name: TinaCMS Documentation Setup
overview: Add TinaCMS documentation to README.md and DEVELOPERS.md, add a smoke test to verify the CMS SPA loads, run npm install to sync the lockfile, and update the devlog.
todos:
  - id: npm-install
    content: Run npm install to sync package-lock.json with tinacms dependency
    status: completed
  - id: add-smoke-test
    content: Add TinaCMS SPA smoke test to tests/security-and-smoke.spec.ts
    status: completed
  - id: update-readme
    content: Add CMS section to README.md (scripts table + brief overview)
    status: completed
  - id: update-developers
    content: Add comprehensive CMS section to DEVELOPERS.md (full setup guide)
    status: completed
  - id: update-devlog
    content: Append documentation changes to Session 4 in devlog
    status: completed
  - id: verify
    content: Run verification checklist (npm run dev, check admin URL, npm test)
    status: completed
---

# TinaCMS Documentation & Verification Setup

This plan adds complete documentation for TinaCMS integration and verification that the CMS admin SPA actually boots.

---

## 1. Sync Package Lockfile

Run `npm install` to capture the `tinacms` dependency tree in `package-lock.json`.

```bash
npm install
```

**Verification:** Check that `package-lock.json` now includes `tinacms` entries.

---

## 2. Add TinaCMS Smoke Test

**File:** `tests/security-and-smoke.spec.ts`

Add a new test case to the `Functional Smoke Tests` block (after line 48) that verifies the Tina SPA JavaScript actually loads and executes:

```typescript
  // 4. INFRASTRUCTURE: CMS Asset Check
  // Verify that the TinaCMS SPA actually loads its JavaScript.
  // A 200 OK on the HTML isn't enough; we need to see the app mount.
  test('TinaCMS Admin SPA loads', async ({ page }) => {
    // Only run if we have the keys to get through the gate
    if (!HAS_SECRETS) test.skip('Skipping CMS check (No Service Tokens)');

    await page.setExtraHTTPHeaders(CF_HEADERS);
    
    // Go to the admin entry point
    await page.goto(`${BASE_URL}/admin/index.html`);

    // Check for the Tina loading state or login prompt.
    // "Tina" is usually present in the title or the login button text.
    // This confirms the JS bundle was found and executed.
    await expect(page.getByText(/tina/i).first()).toBeVisible({ timeout: 10000 });
  });
```

**Why:** A 200 OK on `/admin/index.html` doesn't prove the SPA works. This test confirms the JavaScript bundle loads and renders.

---

## 3. Update README.md (Brief Mention)

Add a new row to the **Scripts** table (around line 96) and a brief CMS section after the Authentication section.

**Scripts table addition:**

| Script | Purpose |
|--------|---------|
| `npm run dev` | Start dev server **with TinaCMS** |
| `npm run dev:astro` | Start Astro-only dev server (no CMS) |

**New section after line 187 (after Authentication section):**

```markdown
## Content Management (TinaCMS)

The `/admin/` route provides a visual editor for wiki content via TinaCMS.

### Local Development

```bash
npm run dev          # Starts Astro + TinaCMS admin
npm run dev:astro    # Starts Astro only (no CMS)
```

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `TINA_CLIENT_ID` | Tina Cloud client ID | Production |
| `TINA_TOKEN` | Tina Cloud token | Production |

See `DEVELOPERS.md` for setup instructions.
```

---

## 4. Update DEVELOPERS.md (Detailed Instructions)

Add a comprehensive CMS section after the "Testing & Quality" section (after line 430).

**New section:**

```markdown
---

## Content Management System (TinaCMS)

### Overview

TinaCMS provides a visual editor at `/admin/` for editing MDX content in `src/content/docs/`. It uses **direct git-backed mode** (no editorial workflow) - edits commit directly to the repository.

### Architecture

```
┌─────────────────────────────────────────────┐
│           /admin/index.html                 │  ← TinaCMS SPA
├─────────────────────────────────────────────┤
│              tina/config.ts                 │  ← Schema definition
├─────────────────────────────────────────────┤
│           src/content/docs/**/*.mdx         │  ← Content files
├─────────────────────────────────────────────┤
│             Git Repository                  │  ← Storage backend
└─────────────────────────────────────────────┘
```

### Local Development

```bash
# Full stack (Astro + TinaCMS)
npm run dev

# Astro only (faster, no CMS)
npm run dev:astro
```

**Local admin URL:** http://localhost:4321/admin/

In local mode, TinaCMS operates without authentication and commits directly to your local git working tree.

### Production Setup (Tina Cloud)

For production deployments, TinaCMS requires Tina Cloud credentials for authentication and git operations.

#### 1. Create a Tina Cloud Account

1. Go to [app.tina.io](https://app.tina.io)
2. Sign in with GitHub
3. Create a new project linked to this repository

#### 2. Get Credentials

From your Tina Cloud project dashboard:

| Credential | Location |
|------------|----------|
| `TINA_CLIENT_ID` | Project Settings → Client ID |
| `TINA_TOKEN` | Project Settings → Tokens → Create Read-Only Token |

#### 3. Set Environment Variables

**Local (`.env` file):**

```bash
TINA_CLIENT_ID=your-client-id
TINA_TOKEN=your-token
```

**Cloudflare Pages:**

1. Dashboard → Pages → howtowincapitalism → Settings → Environment Variables
2. Add `TINA_CLIENT_ID` (Production)
3. Add `TINA_TOKEN` (Production)

### Content Schema

Defined in `tina/config.ts`:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Page title (also used for filename) |
| `description` | string | Yes | SEO meta description |
| `pubDate` | datetime | No | Publication date |
| `tags` | string[] | No | Content tags |
| `weight` | number | No | Sort order weight |
| `body` | rich-text | Yes | MDX content body |

### Build Process

```bash
npm run build
# Runs: tinacms build && astro build
```

1. `tinacms build` generates admin assets into `public/admin/`
2. `astro build` copies `public/admin/` to `dist/admin/` and builds the site

### Access Control

The `/admin/` route is protected by Cloudflare Access in production. Ensure your Access policy covers:

- Production domain: `howtowincapitalism.com/admin/*`
- Preview domains: `*.howtowincapitalism.pages.dev/admin/*`

### Troubleshooting

| Issue | Solution |
|-------|----------|
| White screen at `/admin/` | Check browser console for JS errors; verify `TINA_CLIENT_ID` is set |
| "Unauthorized" on save | Verify `TINA_TOKEN` has write permissions |
| Admin assets missing | Run `npm run build` and check `dist/admin/` exists |
| Local changes not appearing | Restart dev server (`npm run dev`) |

### Media Storage

Images uploaded via TinaCMS are stored in `public/images/` and committed to the repository.

```
public/
└── images/
    └── [uploaded-files]
```
```

---

## 5. Update Devlog

Append to `_docs/devlog/2025-12-12_devlog.md` under Session 4:

```markdown
### Documentation & Verification

- Added TinaCMS smoke test to `tests/security-and-smoke.spec.ts` (verifies SPA JavaScript loads)
- Added CMS section to `README.md` (brief overview, env vars)
- Added comprehensive CMS section to `DEVELOPERS.md` (full setup guide, Tina Cloud onboarding, troubleshooting)
- Ran `npm install` to sync `package-lock.json` with `tinacms` dependency
```

---

## 6. Verification Checklist

After execution, verify:

- [ ] `package-lock.json` contains `tinacms` entries
- [ ] `npm run dev` starts both Astro and TinaCMS
- [ ] http://localhost:4321/admin/ loads the TinaCMS interface
- [ ] `npm test` passes including the new CMS smoke test (locally may skip due to no secrets)
- [ ] README.md has CMS section
- [ ] DEVELOPERS.md has detailed CMS setup guide