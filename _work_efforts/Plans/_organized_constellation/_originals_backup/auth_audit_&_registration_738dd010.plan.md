---
name: Auth Audit & Registration
overview: "Comprehensive security audit of the current Cloudflare KV auth system, followed by a two-phase implementation of user registration: Phase 1 (admin-only) and Phase 2 (open registration with bot protection)."
todos:
  - id: audit-password-hashing
    content: Upgrade password hashing from SHA-256 to PBKDF2 with per-user salt
    status: pending
  - id: audit-rate-limiting
    content: Add rate limiting to login endpoint (IP + email based)
    status: pending
  - id: audit-account-lockout
    content: Implement account lockout after N failed attempts
    status: pending
  - id: audit-csrf
    content: Add CSRF token to login form
    status: pending
  - id: phase1-admin-api
    content: Create admin user management API endpoints
    status: pending
  - id: phase1-admin-ui
    content: Build admin user management UI pages
    status: pending
  - id: phase2-turnstile
    content: Integrate Cloudflare Turnstile for bot protection
    status: pending
  - id: phase2-email-service
    content: Set up Resend for email verification
    status: pending
  - id: phase2-registration-flow
    content: Implement full registration flow with verification
    status: pending
---

# Auth Security Audit & User Registration Plan

## Part 1: Security Audit

### Current Architecture Review

The auth system uses Cloudflare KV with httpOnly cookies. Key files:

- `src/lib/auth/kv-auth.ts` - Server-side KV operations
- `src/pages/api/auth/login.ts` - Login endpoint
- `src/lib/auth/local-auth.ts` - Local dev fallback

### Identified Vulnerabilities & Issues

| Issue | Severity | Location | Fix |

|-------|----------|----------|-----|

| **SHA-256 without iterations** | MEDIUM | `kv-auth.ts:35` | Upgrade to PBKDF2 or scrypt |

| **Hardcoded salt** | MEDIUM | `kv-auth.ts:37` | Use per-user random salt |

| **No rate limiting** | HIGH | `login.ts` | Add IP/email rate limits |

| **No account lockout** | MEDIUM | `login.ts` | Lock after N failed attempts |

| **Weak local session token** | LOW | `local-auth.ts:78` | Use crypto.randomUUID() |

| **No CSRF protection on forms** | MEDIUM | `LoginForm.astro` | Add CSRF token |

| **Plaintext passwords in local-auth** | LOW | `local-auth.ts:20-61` | Dev-only, acceptable |

| **No session invalidation on password change** | MEDIUM | N/A | Implement when adding password change |

| **Open redirect potential** | LOW | `LoginForm.astro:85` | Already validated (starts with `/`) |

### Password Hashing Upgrade

Current (`kv-auth.ts:35-41`):

```typescript
// Weak: Single SHA-256 pass with static salt
const data = encoder.encode(password + 'htwc_salt_2024');
const hashBuffer = await crypto.subtle.digest('SHA-256', data);
```

Recommended:

```typescript
// PBKDF2 with 100k iterations, per-user salt
const salt = crypto.getRandomValues(new Uint8Array(16));
const key = await crypto.subtle.importKey('raw', encoder.encode(password), 'PBKDF2', false, ['deriveBits']);
const hash = await crypto.subtle.deriveBits({ name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' }, key, 256);
```

### Rate Limiting Implementation

Use Cloudflare KV to track login attempts:

```
rate:ip:{ip}        -> { count, windowStart }
rate:email:{email}  -> { count, windowStart }
lockout:{email}     -> { until, reason }
```

Limits:

- 5 attempts per IP per 15 minutes
- 10 attempts per email per hour
- Account lockout after 20 failed attempts (1 hour)

---

## Part 2: Phase 1 - Admin-Only Registration

### New Files Required

| File | Purpose |

|------|---------|

| `src/pages/api/admin/users/create.ts` | Create user endpoint |

| `src/pages/api/admin/users/list.ts` | List users endpoint |

| `src/pages/api/admin/users/[id].ts` | Get/Update/Delete user |

| `src/pages/admin/users/index.astro` | Admin user list UI |

| `src/pages/admin/users/new.astro` | Create user form |

### API: POST /api/admin/users/create

```typescript
// 1. Verify admin session
// 2. Validate input (email, password, name, role)
// 3. Check email uniqueness
// 4. Hash password with PBKDF2 + random salt
// 5. Generate unique ID
// 6. Write to KV: user:{id} and email:{email}
// 7. Return sanitized user
```

### KV Schema Extension

```
USERS namespace:
  user:{id}              -> { id, email, passwordHash, salt, name, role, ... }
  email:{email}          -> userId
  count:users            -> total user count (for admin dashboard)
```

---

## Part 3: Phase 2 - Open Registration with Bot Protection

### Anti-Bot Stack

| Layer | Service | Purpose |

|-------|---------|---------|

| **CAPTCHA** | Cloudflare Turnstile | Invisible bot detection (free) |

| **Email verification** | Resend or Mailgun | Verify real email ownership |

| **Rate limiting** | Cloudflare KV | Prevent spam registrations |

| **Honeypot field** | Frontend | Catch dumb bots |

| **Time-based detection** | Frontend | Too-fast submissions = bot |

### Registration Flow

```
User fills form (email, password, name)
       |
       v
[Turnstile CAPTCHA validates]
       |
       v
POST /api/auth/register
       |
       +-- Rate limit check (IP: 3/hour, global: 100/day)
       +-- Honeypot field check
       +-- Submission time check (>3 seconds)
       +-- Turnstile token verification (server-side)
       +-- Email format + disposable domain check
       |
       v
Create pending user in KV (status: 'pending')
Generate verification token (expires 24h)
       |
       v
Send verification email via Resend
       |
       v
User clicks link: /verify?token=xxx
       |
       v
POST /api/auth/verify
       |
       +-- Token valid + not expired
       +-- Mark user as 'active'
       +-- Delete verification token
       +-- Auto-login (set session cookie)
       |
       v
Redirect to home
```

### New Files for Phase 2

| File | Purpose |

|------|---------|

| `src/pages/register.astro` | Registration page |

| `src/pages/verify.astro` | Email verification landing |

| `src/pages/api/auth/register.ts` | Registration endpoint |

| `src/pages/api/auth/verify.ts` | Email verification endpoint |

| `src/lib/auth/turnstile.ts` | Turnstile verification helper |

| `src/lib/email/send.ts` | Email sending via Resend |

| `src/lib/email/templates/verify.ts` | Verification email template |

### KV Schema for Registration

```
USERS namespace:
  user:{id}              -> { ..., status: 'active'|'pending' }
  email:{email}          -> userId
  verify:{token}         -> { userId, expiresAt }
  
Rate limiting:
  rate:register:ip:{ip}  -> { count, windowStart }
  rate:register:daily    -> { count, date }
```

### Turnstile Integration

```astro
<!-- In registration form -->
<div class="cf-turnstile" data-sitekey="{TURNSTILE_SITE_KEY}"></div>
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
```

Server verification (`turnstile.ts`):

```typescript
export async function verifyTurnstile(token: string, ip: string): Promise<boolean> {
  const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      secret: TURNSTILE_SECRET_KEY,
      response: token,
      remoteip: ip,
    }),
  });
  const data = await res.json();
  return data.success === true;
}
```

### Email Service (Resend)

```typescript
// src/lib/email/send.ts
import { Resend } from 'resend';

const resend = new Resend(RESEND_API_KEY);

export async function sendVerificationEmail(to: string, token: string) {
  const verifyUrl = `https://howtowincapitalism.com/verify?token=${token}`;
  
  await resend.emails.send({
    from: 'noreply@howtowincapitalism.com',
    to,
    subject: 'Verify your email',
    html: `<a href="${verifyUrl}">Click to verify</a>`,
  });
}
```

### Disposable Email Blocking

Block known disposable domains:

```typescript
const BLOCKED_DOMAINS = ['tempmail.com', 'guerrillamail.com', '10minutemail.com', ...];

function isDisposableEmail(email: string): boolean {
  const domain = email.split('@')[1]?.toLowerCase();
  return BLOCKED_DOMAINS.includes(domain);
}
```

---

## Environment Variables Required

```bash
# Turnstile (Phase 2)
TURNSTILE_SITE_KEY=xxx
TURNSTILE_SECRET_KEY=xxx

# Email (Phase 2)
RESEND_API_KEY=xxx
FROM_EMAIL=noreply@howtowincapitalism.com
```

---

## Implementation Order

1. **Security fixes** (audit items) - Immediate priority
2. **Phase 1: Admin registration** - Low complexity, no external dependencies
3. **Phase 2: Open registration** - Requires Turnstile setup + email service