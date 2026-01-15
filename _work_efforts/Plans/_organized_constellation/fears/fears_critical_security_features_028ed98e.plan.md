---
name: Critical Security Features
overview: "Implement three critical security features identified from MECANIK comparison: CSRF protection for all forms, PBKDF2 password hashing with per-user salts, and a complete password reset flow."
todos:
  - id: csrf-utils
    content: Create src/lib/auth/csrf.ts with AES-GCM encrypt/decrypt
    status: pending
  - id: csrf-middleware
    content: Create src/middleware.ts to inject CSRF tokens into forms
    status: pending
  - id: csrf-forms
    content: Add hidden CSRF input to LoginForm and RegisterForm
    status: pending
  - id: csrf-validate
    content: Add CSRF validation to login and register API endpoints
    status: pending
  - id: pbkdf2-hash
    content: Add hashPasswordV2() and verifyPasswordV2() to kv-auth.ts
    status: pending
  - id: pbkdf2-migrate
    content: Update verifyPassword() to detect v1/v2 and upgrade on login
    status: pending
  - id: pbkdf2-seed
    content: Update seed-users.mjs to use v2 hash format
    status: pending
  - id: reset-pages
    content: Create forgot-password and reset-password pages
    status: pending
  - id: reset-api
    content: Create forgot-password and reset-password API endpoints
    status: pending
  - id: reset-email
    content: Create send-reset.ts email template
    status: pending
  - id: env-vars
    content: Document CSRF_SECRET env var requirement
    status: pending

category: fears
confidence: 0.58
constellation_date: 2026-01-14
---

# Critical Security Features Implementation

## Scope

Three features from MECANIK comparison:

1. CSRF Protection (all POST endpoints)
2. PBKDF2 Password Hashing (per-user random salts)
3. Password Reset Flow (forgot-password, email, reset page)

---

## 1. CSRF Protection

### New Files

- `src/lib/auth/csrf.ts` - Token generation/validation
- `src/middleware.ts` - Astro middleware to inject tokens

### Changes

- `src/components/auth/LoginForm.astro` - Add hidden CSRF input
- `src/components/auth/RegisterForm.astro` - Add hidden CSRF input
- `src/pages/api/auth/login.ts` - Validate CSRF token
- `src/pages/api/auth/register.ts` - Validate CSRF token

### Implementation

**Token structure (encrypted JSON):**

```typescript
{
  ip: string,       // CF-Connecting-IP
  country: string,  // CF-IPCountry
  ua: string,       // User-Agent
  exp: number       // Expiry timestamp (60s)
}
```

**Encryption:** AES-GCM via Web Crypto API with `CSRF_SECRET` env var.

**Validation:** Decrypt token, verify IP/UA match, check expiry.

---

## 2. PBKDF2 Password Hashing

### Changes

- `src/lib/auth/kv-auth.ts` - New `hashPasswordV2()` and `verifyPasswordV2()` with migration support
- `scripts/seed-users.mjs` - Update to use new hashing format

### Hash Format

```
v2:${iterations}:${saltHex}:${hashHex}
```

- iterations: 100,000
- salt: 16 random bytes
- hash: 256-bit derived key

### Migration Strategy

- New hashes start with `v2:` prefix
- `verifyPassword()` detects format and uses appropriate method
- On successful v1 login, rehash password to v2 format (transparent upgrade)

---

## 3. Password Reset Flow

### New Files

- `src/pages/forgot-password/index.astro` - Request reset form
- `src/pages/reset-password/index.astro` - Set new password form
- `src/pages/api/auth/forgot-password.ts` - Send reset email
- `src/pages/api/auth/reset-password.ts` - Process password change
- `src/lib/email/send-reset.ts` - Reset email template

### KV Storage

```typescript
// Reset token (2-hour TTL)
`reset:${token}` -> userId
```

### Flow

1. User enters email on `/forgot-password/`
2. API generates 32-byte token, stores in KV with 2h TTL
3. Email sent via Resend with reset link
4. User clicks link, lands on `/reset-password/?token=xxx`
5. User enters new password
6. API validates token, updates password hash, deletes token
7. Confirmation email sent

### Security

- Ambiguous response ("If email exists, check inbox")
- One-time use tokens
- Rate limiting (future enhancement)

---

## Environment Variables Required

```bash
CSRF_SECRET=32-byte-random-hex  # New - for CSRF encryption
RESEND_API_KEY=re_xxxxx         # Existing - for emails
```

---

## File Summary

| File | Action | Purpose |

|------|--------|---------|

| `src/lib/auth/csrf.ts` | Create | CSRF token encrypt/decrypt |

| `src/lib/auth/kv-auth.ts` | Modify | PBKDF2 hashing + migration |

| `src/middleware.ts` | Create | Inject CSRF tokens |

| `src/pages/forgot-password/index.astro` | Create | Reset request page |

| `src/pages/reset-password/index.astro` | Create | New password page |

| `src/pages/api/auth/forgot-password.ts` | Create | Send reset email |

| `src/pages/api/auth/reset-password.ts` | Create | Process reset |

| `src/lib/email/send-reset.ts` | Create | Reset email template |

| `src/pages/api/auth/login.ts` | Modify | CSRF + v1->v2 migration |

| `src/pages/api/auth/register.ts` | Modify | CSRF validation |

| `src/components/auth/LoginForm.astro` | Modify | Add CSRF field |

| `src/components/auth/RegisterForm.astro` | Modify | Add CSRF field |

| `scripts/seed-users.mjs` | Modify | Use v2 hashing |

---

## Testing Plan

1. Verify CSRF blocks requests without valid token
2. Verify existing users can still log in (v1 hash)
3. Verify login upgrades v1 to v2 hash transparently
4. Verify new registrations use v2 hash
5. Verify password reset email arrives
6. Verify reset link works and changes password
7. Verify expired/invalid reset tokens rejected