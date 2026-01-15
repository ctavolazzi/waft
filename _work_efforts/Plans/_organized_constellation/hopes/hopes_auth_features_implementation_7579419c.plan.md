---
name: Auth Features Implementation
overview: Complete the user registration flow by configuring Resend email service, then implement forgot password functionality with token-based password reset.
todos:
  - id: resend-config
    content: "Phase 1: Configure Resend API key in Cloudflare (manual step)"
    status: pending
  - id: kv-reset-functions
    content: Add password reset functions to kv-auth.ts (generateResetToken, createPasswordReset, resetPassword)
    status: completed
  - id: email-template
    content: Create send-password-reset.ts email template
    status: completed
  - id: api-forgot
    content: Create /api/auth/forgot-password API route
    status: completed
  - id: api-reset
    content: Create /api/auth/reset-password API route
    status: completed
  - id: form-forgot
    content: Create ForgotPasswordForm.astro component
    status: completed
  - id: form-reset
    content: Create ResetPasswordForm.astro component
    status: completed
  - id: page-forgot
    content: Create /forgot-password/ page
    status: completed
  - id: page-reset
    content: Create /reset-password/ page with success/error states
    status: completed
  - id: login-link
    content: Add 'Forgot password?' link to LoginForm.astro
    status: completed
  - id: test-e2e
    content: Test complete forgot password flow end-to-end
    status: completed

category: hopes
confidence: 0.56
constellation_date: 2026-01-14
---

# Auth Features Implementation Plan

## Phase 1: Complete User Registration

The registration infrastructure is already built. Only configuration is needed.

### Configuration Steps (Manual)

1. **Resend Setup**

   - Sign up at [resend.com](https://resend.com)
   - Verify domain `howtowincapitalism.com` (add DNS records)
   - Generate API key

2. **Cloudflare Environment Variable**

   - Go to Pages > howtowincapitalism > Settings > Environment variables
   - Add: `RESEND_API_KEY` = `re_xxxxx...`

3. **Test Flow**

   - Visit `/register/`
   - Create test account
   - Verify email arrives
   - Click confirmation link
   - Login with new account

### Existing Files (No Changes Needed)

- `src/pages/register/index.astro`
- `src/components/auth/RegisterForm.astro`
- `src/pages/api/auth/register.ts`
- `src/pages/api/auth/confirm.ts`
- `src/lib/email/send-confirmation.ts`

---

## Phase 2: Implement Forgot Password

### New Files to Create

**1. KV Auth Extensions** - `src/lib/auth/kv-auth.ts`

Add to existing file:

```typescript
// Password reset token generation
export function generateResetToken(): string { ... }

// Create password reset request
export async function createPasswordReset(
  users: KVNamespace,
  email: string
): Promise<{ resetToken: string } | null> { ... }

// Reset password with token
export async function resetPassword(
  users: KVNamespace,
  token: string,
  newPassword: string
): Promise<boolean> { ... }
```

**2. Email Template** - `src/lib/email/send-password-reset.ts`

```typescript
export async function sendPasswordResetEmail({
  to, name, resetToken, apiKey
}): Promise<{ success: boolean; error?: string }>
```

**3. API Routes**

- `src/pages/api/auth/forgot-password.ts` - POST: Request reset email
- `src/pages/api/auth/reset-password.ts` - POST: Set new password with token

**4. UI Pages**

- `src/pages/forgot-password/index.astro` - Email input form
- `src/pages/reset-password/index.astro` - New password form (token in URL)

**5. Components**

- `src/components/auth/ForgotPasswordForm.astro`
- `src/components/auth/ResetPasswordForm.astro`

**6. Result Pages**

- `src/pages/reset-password/success/index.astro`
- `src/pages/reset-password/error/index.astro`

### Login Form Update - `src/components/auth/LoginForm.astro`

Add "Forgot password?" link below the form.

---

## Implementation Order

1. Add KV functions for reset tokens to `kv-auth.ts`
2. Create email template `send-password-reset.ts`
3. Create API routes (forgot + reset)
4. Create UI components (forms)
5. Create pages (forgot-password, reset-password)
6. Add "Forgot password?" link to LoginForm
7. Test end-to-end

---

## Infrastructure Notes

- Reset tokens stored in KV as `reset:{token}` with 1-hour TTL
- Tokens are one-time use (deleted after successful reset)
- Uses same Resend integration as registration
- Same security model: SHA-256 hashed passwords with salt