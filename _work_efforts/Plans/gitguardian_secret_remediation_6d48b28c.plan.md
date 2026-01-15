---
name: GitGuardian Secret Remediation
overview: Rotate exposed production passwords, separate production and development credentials, and implement proper secrets management to prevent future GitGuardian alerts.
todos:
  - id: rotate-prod-passwords
    content: Generate new production passwords and store in Cloudflare environment secrets
    status: completed
  - id: update-seed-script
    content: Modify seed-users.mjs to read passwords from env vars with dev fallbacks
    status: completed
  - id: update-local-auth
    content: Change local-auth.ts to use dev-only passwords with GitGuardian ignore comments
    status: completed
  - id: update-test-files
    content: Update all 8 test files to use dev passwords with GitGuardian ignore comments
    status: completed
  - id: update-docs
    content: Update .cursorrules and AUTH.md to document dev credentials only
    status: in_progress
  - id: reseed-production
    content: Run seed script to update production KV with new passwords
    status: pending
---

# GitGuardian Secret Remediation Plan

## Problem Summary

Production user passwords are hardcoded in 3 source files and used across 8 test files. These are REAL production credentials that seed to Cloudflare KV, not just test fixtures.

## Strategy: Separate Production from Development

1. **Production passwords** - Rotate and store in Cloudflare environment secrets (never in code)
2. **Development/test passwords** - Keep in code with GitGuardian ignore comments

## Files to Modify

### Phase 1: Generate New Production Passwords

Generate 4 new secure passwords for production (run this yourself, don't commit):

- admin: (new random password)
- editor: (new random password)
- contributor: (new random password)
- viewer: (new random password)

Store in Cloudflare Dashboard > Pages > Settings > Environment variables as:

- `SEED_ADMIN_PASSWORD`
- `SEED_EDITOR_PASSWORD`
- `SEED_CONTRIBUTOR_PASSWORD`
- `SEED_VIEWER_PASSWORD`

### Phase 2: Update Seed Script

`scripts/seed-users.mjs`:

- Read passwords from environment variables for production
- Fallback to hardcoded dev passwords for local seeding
```javascript
// Production: read from env, Local: use dev passwords
const passwords = {
  admin: process.env.SEED_ADMIN_PASSWORD || 'DevAdmin_Local_2024#',
  editor: process.env.SEED_EDITOR_PASSWORD || 'DevEditor_Local_2024#',
  contributor: process.env.SEED_CONTRIBUTOR_PASSWORD || 'DevContrib_Local_2024#',
  viewer: process.env.SEED_VIEWER_PASSWORD || 'DevViewer_Local_2024#',
};
```


### Phase 3: Update Local Auth

`src/lib/auth/local-auth.ts`:

- Change to development-only passwords (different from production)
- Add GitGuardian ignore comments
```typescript
// Local development only - NOT production credentials
// pragma: allowlist secret
password: 'DevAdmin_Local_2024#',
```


### Phase 4: Create Shared Test Fixtures and Update Test Files

Create a centralized test credentials file to avoid duplication:

**New file: `tests/fixtures/test-credentials.ts`**

```typescript
// Development-only test credentials (NOT production passwords)
// pragma: allowlist nextline secret
export const TEST_CREDENTIALS = {
  admin: { email: 'admin@email.com', password: 'DevAdmin_Local_2024#', role: 'admin' },
  editor: { email: 'editor@email.com', password: 'DevEditor_Local_2024#', role: 'editor' },
  contributor: { email: 'contributor@email.com', password: 'DevContrib_Local_2024#', role: 'contributor' },
  viewer: { email: 'viewer@email.com', password: 'DevViewer_Local_2024#', role: 'viewer' },
} as const;

export const SITE_PASSWORD = 'unlockmenow';
```

Update all 8 test files to import from shared fixtures:

- `tests/admin.spec.ts`
- `tests/auth.spec.ts`
- `tests/navigation.spec.ts`
- `tests/security.spec.ts`
- `tests/accessibility.spec.ts`
- `tests/auth-snapshots.spec.ts`
- `tests/content.spec.ts`
- `tests/users.spec.ts`

### Phase 5: Update Documentation

- `.cursorrules` - Update test credentials table to show DEV passwords only
- `_docs/AUTH.md` - Document the separation of prod/dev credentials

### Phase 6: Re-run Seed Script

After setting Cloudflare environment secrets:

```bash
node scripts/seed-users.mjs  # Production with new passwords
```

## New Password Scheme

| Environment | Passwords | Storage |

|-------------|-----------|---------|

| Production | Unique, rotated | Cloudflare env vars |

| Local Dev | `DevAdmin_Local_2024#`, etc. | Code (with ignore) |

| Tests | Same as local dev | Code (with ignore) |

## Verification

1. GitGuardian should no longer flag (using ignore comments for dev passwords)
2. Production uses different passwords from code
3. Tests still pass with dev credentials