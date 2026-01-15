---
name: Auth Flow Screenshots
overview: Run the Playwright screenshot capture script against localhost:4321 to document the complete auth flow, then commit and push all changes including the v0.0.2 session security updates.
todos:
  - id: run-screenshots
    content: Run node scripts/capture-auth-screenshots.mjs to capture all 8 auth flow screenshots
    status: completed
  - id: verify-screenshots
    content: Verify all screenshots saved to _docs/screenshots/auth-flow/v0.0.1/
    status: completed
  - id: commit-ship
    content: Commit all changes and push to deploy v0.0.2
    status: completed
---

# Auth Flow Screenshot Capture

## Prerequisites

- Dev server running on localhost:4321 (already running)
- Playwright browsers installed (already done)

## Execution

### Step 1: Run Screenshot Capture Script

```bash
cd /Users/ctavolazzi/Code/howtowincapitalism
node scripts/capture-auth-screenshots.mjs
```

This captures 8 screenshots:

| Screenshot | Description |

|------------|-------------|

| 01_login-page_v0.0.1.png | Login form |

| 02_login-error_v0.0.1.png | Invalid credentials error |

| 03_home-authenticated_v0.0.1.png | Home page after login (or 03_login-failed if auth fails) |

| 04_user-menu_v0.0.1.png | User dropdown menu open |

| 05_profile-page_v0.0.1.png | User profile page |

| 06_logged-out_v0.0.1.png | After logout redirect |

| 07_register-page_v0.0.1.png | Registration form |

| 08_forgot-password-page_v0.0.1.png | Forgot password form |

### Step 2: Verify Screenshots

Check that all screenshots were saved to `_docs/screenshots/auth-flow/v0.0.1/`

### Step 3: Commit and Push

```bash
git add -A
git commit -m "docs: capture v0.0.1 auth flow screenshots from localhost"
git push
```

## Files Involved

- Script: `scripts/capture-auth-screenshots.mjs`
- Output: `_docs/screenshots/auth-flow/v0.0.1/*.png`
- Credentials: viewer@email.com / V!ewer_Read_2024# (from local-auth.ts)