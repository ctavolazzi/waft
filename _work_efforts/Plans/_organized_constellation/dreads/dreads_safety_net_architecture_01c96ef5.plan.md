---
name: Safety Net Architecture
overview: Replace existing fragmented logging (logger.mjs + debug.ts) with a unified Logger, add structured AppError classes, and implement client-side error UI (Toast notifications + error fallbacks).
todos:
  - id: logger
    content: Create src/lib/logger.ts with DEBUG/INFO/WARN/ERROR levels and context support
    status: pending
  - id: errors
    content: Create src/lib/errors.ts with AppError, UserError, SystemError classes
    status: pending
  - id: toast-store
    content: Create src/lib/stores/toastStore.ts with nanostores
    status: pending
  - id: toast-ui
    content: Create src/components/utilities/ToastContainer.astro
    status: pending
  - id: error-boundary
    content: Create src/lib/errorBoundary.ts global handlers
    status: pending
  - id: error-fallback
    content: Create src/components/utilities/ErrorFallback.astro
    status: pending
  - id: migrate-store
    content: Update src/lib/auth/store.ts to use new logger
    status: pending
  - id: migrate-actions
    content: Update src/lib/api/profileActions.ts with errors + logger
    status: pending
  - id: migrate-service
    content: Update src/lib/api/profileService.ts with errors + logger
    status: pending
  - id: migrate-matrix
    content: Update src/lib/tools/decision-matrix.ts to use new logger
    status: pending
  - id: cleanup
    content: Delete src/lib/debug.ts and src/lib/tools/logger.mjs
    status: pending

category: dreads
confidence: 0.40
constellation_date: 2026-01-14
---

# Safety Net Architecture Specification

## Problem Statement

Current error handling is fragmented:

- `src/lib/tools/logger.mjs` - Server-side only (Node.js, file I/O)
- `src/lib/debug.ts` - Client-side only (browser console)
- No structured error types (just boolean returns)
- No user-facing error display system

---

## 1. The Logger (`src/lib/logger.ts`)

### Interface

```typescript
type LogLevel = 'DEBUG' | 'INFO' | 'WARN' | 'ERROR';

interface LogContext {
  userId?: string;
  component?: string;
  action?: string;
  [key: string]: unknown;
}

interface Logger {
  debug(message: string, context?: LogContext): void;
  info(message: string, context?: LogContext): void;
  warn(message: string, context?: LogContext): void;
  error(message: string, error?: Error, context?: LogContext): void;
}

// Factory for scoped loggers
function createLogger(component: string): Logger;

// Global singleton
const logger: Logger;
```

### Key Design Decisions

| Decision | Choice | Rationale |

|----------|--------|-----------|

| Output | Console only | Cloudflare Pages has no filesystem; future: plug in Sentry |

| Format | JSON in prod, pretty in dev | Machine-parseable for log aggregation |

| Levels | 4 (DEBUG/INFO/WARN/ERROR) | Standard; DEBUG off in production |

| Context | Structured object | Enables filtering by userId, component |

### Future Extensibility Hook

```typescript
// src/lib/logger.ts (line ~15)
type LogTransport = (entry: LogEntry) => void;
const transports: LogTransport[] = [consoleTransport];

// Later: transports.push(sentryTransport);
```

### Files to Delete After Migration

- `src/lib/tools/logger.mjs` (server logger)
- `src/lib/debug.ts` (client logger)

Update imports in: `store.ts`, `profileActions.ts`, `profileService.ts`, `decision-matrix.ts`

---

## 2. The Error Standard (`src/lib/errors.ts`)

### Class Hierarchy

```typescript
// Base error - all app errors extend this
class AppError extends Error {
  readonly code: string;
  readonly context?: Record<string, unknown>;
  readonly timestamp: string;
}

// User did something wrong -> show toast, don't crash
class UserError extends AppError {
  readonly userMessage: string; // Safe to display
}

// System failure -> show error boundary, log to Sentry
class SystemError extends AppError {
  readonly originalError?: Error;
}
```

### Error Codes

```typescript
// src/lib/errors.ts
const ErrorCodes = {
  // User Errors (4xx equivalent)
  VALIDATION_FAILED: 'USER_VALIDATION',
  NOT_FOUND: 'USER_NOT_FOUND',
  UNAUTHORIZED: 'USER_UNAUTHORIZED',
  FORBIDDEN: 'USER_FORBIDDEN',

  // System Errors (5xx equivalent)
  NETWORK_ERROR: 'SYS_NETWORK',
  STORAGE_ERROR: 'SYS_STORAGE',
  UNKNOWN: 'SYS_UNKNOWN',
} as const;
```

### Usage Pattern

```typescript
// In profileActions.ts
async function updateUserProfile(userId: string, data: ProfileUpdateData) {
  if (!data.username?.trim()) {
    throw new UserError('VALIDATION_FAILED', 'Username cannot be empty');
  }

  try {
    const result = storeUpdateProfile(userId, data);
    if (!result) {
      throw new UserError('NOT_FOUND', 'User profile not found');
    }
    return result;
  } catch (err) {
    if (err instanceof AppError) throw err;
    throw new SystemError('UNKNOWN', 'Failed to save profile', err);
  }
}
```

---

## 3. The UI Strategy

### 3.1 Toast Notifications (for UserError)

Since project uses nanostores, create a toast store:

**File:** `src/lib/stores/toastStore.ts`

```typescript
import { atom } from 'nanostores';

interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  message: string;
  duration?: number;
}

export const toasts = atom<Toast[]>([]);

export function showToast(toast: Omit<Toast, 'id'>): void;
export function dismissToast(id: string): void;
```

**Component:** `src/components/utilities/ToastContainer.astro`

- Renders toast stack (bottom-right)
- Auto-dismiss after duration
- Subscribe to toastStore

### 3.2 Error Fallback (for SystemError)

Astro doesn't have React Error Boundaries. Strategy:

**A. Page-level try/catch in Astro frontmatter:**

```astro
---
// src/pages/profile/[id].astro
try {
  const profile = await fetchUserProfile(id);
} catch (err) {
  if (err instanceof SystemError) {
    return Astro.redirect('/500');
  }
  throw err;
}
---
```

**B. Client-side global error handler:**

```typescript
// src/lib/errorBoundary.ts
window.addEventListener('error', (event) => {
  logger.error('Uncaught error', event.error);
  showToast({ type: 'error', message: 'Something went wrong' });
});

window.addEventListener('unhandledrejection', (event) => {
  logger.error('Unhandled promise rejection', event.reason);
});
```

**C. Error fallback component for islands:**

```astro
<!-- src/components/utilities/ErrorFallback.astro -->
<div class="error-fallback">
  <p>Something went wrong loading this section.</p>
  <button onclick="location.reload()">Retry</button>
</div>
```

---

## 4. Integration Points

### Profile Routes (Alice's Work)

The profile form should use the new error handling:

```typescript
// In ProfileForm client-side script
try {
  await updateUserProfile(userId, formData);
  showToast({ type: 'success', message: 'Profile saved!' });
} catch (err) {
  if (err instanceof UserError) {
    showToast({ type: 'error', message: err.userMessage });
  } else {
    showToast({ type: 'error', message: 'Failed to save. Please try again.' });
    logger.error('Profile save failed', err);
  }
}
```

---

## 5. File Structure

```
src/lib/
├── logger.ts          # NEW: Unified logger
├── errors.ts          # NEW: AppError classes
├── stores/
│   └── toastStore.ts  # NEW: Toast state
├── errorBoundary.ts   # NEW: Global error handlers
└── debug.ts           # DELETE after migration

src/components/utilities/
├── ToastContainer.astro  # NEW
└── ErrorFallback.astro   # NEW
```

---

## 6. Migration Checklist

Files requiring import updates:

- `src/lib/auth/store.ts` (uses debug)
- `src/lib/api/profileActions.ts` (uses debug)
- `src/lib/api/profileService.ts` (no logger, add it)
- `src/lib/tools/decision-matrix.ts` (uses debug)