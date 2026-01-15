---
name: Code Quality Audit Fix
overview: Fix 64+ TypeScript errors and CSS linting issues by adding Cloudflare Workers types, fixing component barrel exports, and resolving type casting issues.
todos:
  - id: cloudflare-types
    content: Install @cloudflare/workers-types and update tsconfig.json
    status: pending
  - id: env-types
    content: Add index signature to App.Locals in env.d.ts
    status: pending
  - id: barrel-exports
    content: Delete or fix component barrel export files (index.ts)
    status: pending
  - id: rate-limit-types
    content: Fix rate-limit.ts union type with proper type guards
    status: pending
  - id: misc-types
    content: Fix profileService.ts and store.ts type issues
    status: pending
  - id: css-lint
    content: "Optional: Update CSS lint config to exclude .astro files"
    status: pending
  - id: work-effort
    content: Create work effort 10.13_code_quality_audit.md
    status: pending

category: dreads
confidence: 0.80
constellation_date: 2026-01-14
---

# Code Quality Audit Fixes

## Problem Summary

| Category | Count | Root Cause |
|----------|-------|------------|
| `KVNamespace` undefined | 19 | Missing `@cloudflare/workers-types` |
| Astro imports in `.ts` | 28 | Barrel exports use `.astro` in TypeScript |
| `Locals` type casting | 15 | Index signature mismatch |
| `rate-limit.ts` union | 4 | Type narrowing issue |
| Misc type issues | 2 | Individual fixes needed |

---

## Fix 1: Add Cloudflare Workers Types

Install the types package and update tsconfig:

```bash
npm i -D @cloudflare/workers-types
```

Update [`tsconfig.json`](tsconfig.json):
```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"],
  "compilerOptions": {
    "types": ["@cloudflare/workers-types"]
  }
}
```

This fixes all 19 `KVNamespace` errors.

---

## Fix 2: Fix Component Barrel Exports

The file [`src/components/index.ts`](src/components/index.ts) imports `.astro` files which TypeScript cannot resolve in `.ts` files.

**Solution A (Recommended):** Delete `index.ts` barrel files - import components directly in `.astro` pages:
```astro
---
import WikiBox from '../components/atoms/WikiBox.astro';
---
```

**Solution B:** Rename to `index.astro` and re-export (more complex, less common pattern).

Files affected:
- `src/components/index.ts` (24 exports)
- `src/components/organisms/profile/index.ts` (4 exports)

This fixes all 28 component import errors.

---

## Fix 3: Fix Locals Type Definition

Update [`src/env.d.ts`](src/env.d.ts) to add index signature:

```typescript
/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface Env {
  USERS: KVNamespace;
  SESSIONS: KVNamespace;
  RESEND_API_KEY: string;
}

declare namespace App {
  interface Locals {
    runtime: {
      env: Env;
    };
    [key: string]: unknown;  // Add index signature
  }
}
```

This fixes all 15 `Locals` casting errors.

---

## Fix 4: Fix rate-limit.ts Union Type

In [`src/lib/auth/rate-limit.ts`](src/lib/auth/rate-limit.ts), add type guards for the rate limit config union:

```typescript
// Add type guard before accessing .email property
if ('email' in limitsConfig) {
  // Now TypeScript knows this has email property
}
```

This fixes 4 property access errors.

---

## Fix 5: Fix Remaining Type Issues

1. **`profileService.ts:156`** - Add explicit cast:
   ```typescript
   return profile as unknown as Record<string, unknown>;
   ```

2. **`store.ts:74`** - Add index signature to `AuthState` interface or use proper typing.

---

## Fix 6: CSS Linting Config (Optional)

Either exclude `.astro` files from stylelint or add proper parser:

Update [`package.json`](package.json) lint script:
```json
"lint:css": "stylelint 'src/**/*.css' --allow-empty-input"
```

---

## Execution Order

1. Install `@cloudflare/workers-types` and update tsconfig (fixes 19 errors)
2. Update `env.d.ts` with index signature (fixes 15 errors)
3. Delete barrel export files OR update imports (fixes 28 errors)
4. Fix `rate-limit.ts` type guards (fixes 4 errors)
5. Fix individual misc issues (fixes 2 errors)
6. Optional: Update CSS lint config

---

## Files to Modify

| File | Change |
|------|--------|
| `tsconfig.json` | Add compilerOptions.types |
| `src/env.d.ts` | Add index signature to Locals |
| `src/components/index.ts` | Delete or convert to .astro |
| `src/components/organisms/profile/index.ts` | Delete or convert to .astro |
| `src/lib/auth/rate-limit.ts` | Add type guards |
| `src/lib/api/profileService.ts` | Fix cast |
| `src/lib/auth/store.ts` | Fix AuthState constraint |
| `package.json` | Optional: Fix CSS lint scope |

---

## Work Effort

Create `_work_efforts/10-19_development/10_active/10.13_code_quality_audit.md` to track this work.