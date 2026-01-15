---
name: GitGuardian Alert Remediation
overview: Address GitGuardian alert by investigating the credential discrepancy between `.cursorrules` and test fixtures, then properly configure GitGuardian exclusions for legitimate test credentials.
todos:
  - id: verify-credentials
    content: Search codebase for .cursorrules passwords to confirm they're not used in production
    status: pending
  - id: update-cursorrules
    content: Update .cursorrules to remove/fix the credential discrepancy
    status: pending
  - id: create-gitguardian-config
    content: Create .gitguardian.yaml to exclude test fixtures from scanning
    status: pending
  - id: dismiss-alerts
    content: Dismiss the 2 GitGuardian alerts as false positives in dashboard
    status: pending
  - id: update-work-effort
    content: Update security audit work effort with completion notes
    status: pending

category: fears
confidence: 0.53
constellation_date: 2026-01-14
---

# GitGuardian Alert Remediation Plan

## Investigation Required First

Before dismissing as false positive, we need to resolve a discrepancy:

| File | Admin Password |

|------|----------------|

| `.cursorrules` | `Adm!n_Secure_2024#` |

| `tests/fixtures/test-credentials.ts` | `DevAdmin_Local_2024#` |

**Question:** Are the `.cursorrules` passwords actually used anywhere? If they're production credentials, they need to be rotated.

---

## Phase 1: Verify Credential Usage

1. Search codebase for `.cursorrules` passwords to see if they're used anywhere
2. Confirm `test-credentials.ts` is the only source of test auth
3. Verify production uses Cloudflare env vars (not hardcoded)

---

## Phase 2: Fix `.cursorrules` Documentation

If `.cursorrules` passwords are outdated documentation:

- Update to match `test-credentials.ts` (the `Dev*_Local_*` pattern)
- Or remove credentials from `.cursorrules` entirely and reference the fixture file

**Recommended change in [.cursorrules](.cursorrules):**

```markdown
### Test Credentials
See `tests/fixtures/test-credentials.ts` for E2E test credentials.
These are development-only and differ from production.
```

---

## Phase 3: Add GitGuardian Configuration

Create [.gitguardian.yaml](.gitguardian.yaml) to exclude test fixtures:

```yaml
# GitGuardian Configuration
# Exclude development-only test credentials from scanning

paths-ignore:
  - tests/fixtures/**
  - "**/*.test.ts"
  - "**/*.spec.ts"

# Document why these exclusions exist
# Test credentials in tests/fixtures/test-credentials.ts are:
# - Development-only mock credentials
# - Not used in production (production uses Cloudflare env vars)
# - Intentionally committed for E2E testing
```

---

## Phase 4: Dismiss Current Alerts

After configuration is in place:

1. Go to GitGuardian dashboard
2. Mark the 2 alerts in PR #5 as "false positive - test credentials"
3. Document the dismissal reason

---

## Phase 5: Update Security Audit Work Effort

Update [10.10_security_audit.md](_work_efforts/10-19_development/10_active/10.10_security_audit.md):

- Add GitGuardian configuration to completed items
- Document the `.cursorrules` credential cleanup
- Update Section 5.2 (Secrets Management) status

---

## Files to Modify

| File | Action |

|------|--------|

| `.gitguardian.yaml` | Create (new file) |

| `.cursorrules` | Update test credentials section |

| `10.10_security_audit.md` | Update with completion notes |

| Devlog | Document the remediation |