---
name: Run Full Test Suite
overview: Run all 11 Playwright test files against the local dev server to verify the Node adapter setup works correctly.
todos:
  - id: run-tests
    content: Execute npm run test to run full Playwright suite
    status: completed

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Run Full Playwright Test Suite

## What Will Happen

The dev server is already running on `localhost:4321`. Playwright will connect to it (via `reuseExistingServer: true`) and run all tests.

## Test Files (11 total)

| File | Purpose |

|------|---------|

| `accessibility.spec.ts` | A11y checks |

| `account-rights.spec.ts` | RBAC permissions |

| `admin.spec.ts` | Admin functionality |

| `auth-snapshots.spec.ts` | Visual regression for auth |

| `auth.spec.ts` | Login/logout flows |

| `content.spec.ts` | Content rendering |

| `navigation.spec.ts` | Site navigation |

| `registration.spec.ts` | User registration |

| `security-and-smoke.spec.ts` | Security headers + basic checks |

| `security.spec.ts` | Security features |

| `users.spec.ts` | User profile pages |

## Command

```bash
npm run test
```

This runs `playwright test` which will:

1. Connect to the running dev server
2. Execute all test files in `tests/`
3. Generate an HTML report

## Expected Output

- Pass/fail results for each test
- HTML report available via `npm run test:report`
- Screenshots captured on failures