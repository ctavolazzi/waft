---
name: Frontend Testing Setup
overview: Set up Vitest testing framework for TypeScript/JavaScript code in frontend/ and visualizer/ directories, including test configuration, example tests, and npm scripts.
todos:
  - id: install-deps
    content: Install Vitest and testing dependencies in visualizer/ and frontend/
    status: pending
  - id: vitest-config
    content: Create vitest.config.ts files for visualizer and frontend
    status: pending
  - id: test-setup
    content: Create test setup files (setup.ts) for mocking and configuration
    status: pending
  - id: api-client-tests
    content: Write tests for frontend/api_client.ts (success, errors, network failures)
    status: pending
  - id: hook-tests
    content: Write tests for frontend/useDecisionEngine.ts (state, async, errors)
    status: pending
  - id: store-tests
    content: Write tests for visualizer stores (projectStore, gymStore)
    status: pending
  - id: package-scripts
    content: Add test scripts to package.json files
    status: pending
  - id: verify-tests
    content: Run tests and verify they pass
    status: pending

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Frontend Testing Setup Plan

## Overview
Set up Vitest (modern Vite-native test framework) for testing TypeScript/JavaScript code in `frontend/` and `visualizer/` directories. Vitest provides Jest-compatible API with better Vite integration and faster performance.

## Current State
- ✅ Python tests exist (pytest) in `tests/` directory
- ❌ No JavaScript/TypeScript test setup
- ✅ Visualizer uses Vite (perfect for Vitest)
- ✅ TypeScript code in `frontend/` and `visualizer/src/lib/`

## Files to Create/Modify

### 1. Visualizer Test Setup
- **`visualizer/package.json`** - Add Vitest dependencies and test scripts
- **`visualizer/vitest.config.ts`** - Vitest configuration for SvelteKit
- **`visualizer/tsconfig.json`** - Update to include test files

### 2. Frontend Test Setup
- **`frontend/package.json`** - Create package.json with Vitest setup (if doesn't exist)
- **`frontend/vitest.config.ts`** - Vitest configuration for frontend utilities

### 3. Test Files to Create

#### Visualizer Tests
- **`visualizer/src/lib/api/client.test.ts`** - Test API client
- **`visualizer/src/lib/stores/projectStore.test.ts`** - Test Svelte store
- **`visualizer/src/lib/stores/gymStore.test.ts`** - Test gym store (if exists)

#### Frontend Tests
- **`frontend/api_client.test.ts`** - Test Decision Engine API client
  - Test `analyzeDecision()` success cases
  - Test error handling (400, 422, 500)
  - Test network errors
  - Test `checkHealth()` function
- **`frontend/useDecisionEngine.test.ts`** - Test React hook
  - Test hook initialization
  - Test `analyze()` function
  - Test loading states
  - Test error states
  - Test `reset()` function

### 4. Test Utilities
- **`visualizer/src/test/setup.ts`** - Test setup file (mocks, globals)
- **`frontend/test/setup.ts`** - Frontend test setup

## Implementation Steps

### Step 1: Install Dependencies
1. Add Vitest and related packages to `visualizer/package.json`:
   - `vitest` - Test framework
   - `@vitest/ui` - Test UI (optional)
   - `@testing-library/svelte` - Svelte component testing
   - `@testing-library/jest-dom` - DOM matchers
   - `jsdom` - DOM environment for tests
   - `@vitest/coverage-v8` - Coverage reports

2. Add Vitest to `frontend/` (create package.json if needed):
   - `vitest`
   - `jsdom`
   - `@testing-library/react` - React hook testing
   - `@testing-library/react-hooks` - React hooks testing utilities

### Step 2: Configure Vitest

#### Visualizer Config (`visualizer/vitest.config.ts`)
```typescript
import { defineConfig } from 'vitest/config';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import path from 'path';

export default defineConfig({
  plugins: [svelte()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    include: ['src/**/*.{test,spec}.{js,ts}'],
  },
  resolve: {
    alias: {
      $lib: path.resolve(__dirname, './src/lib'),
    },
  },
});
```

#### Frontend Config (`frontend/vitest.config.ts`)
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./test/setup.ts'],
    include: ['**/*.{test,spec}.{js,ts}'],
  },
});
```

### Step 3: Create Test Setup Files

#### `visualizer/src/test/setup.ts`
- Mock SvelteKit `$app` modules
- Configure testing-library
- Set up global test utilities

#### `frontend/test/setup.ts`
- Configure fetch mocking
- Set up React Testing Library
- Configure test environment

### Step 4: Write Example Tests

#### `frontend/api_client.test.ts`
- Test successful API calls with mocked fetch
- Test error responses (400, 422, 500)
- Test network failures
- Test `checkHealth()` function

#### `frontend/useDecisionEngine.test.ts`
- Test hook state management
- Test async `analyze()` function
- Test error handling
- Test `reset()` function

#### `visualizer/src/lib/stores/projectStore.test.ts`
- Test store initialization
- Test `fetch()` method
- Test loading/error states
- Test state updates

### Step 5: Update package.json Scripts

#### Visualizer
```json
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:watch": "vitest --watch"
  }
}
```

#### Frontend
```json
{
  "scripts": {
    "test": "vitest",
    "test:watch": "vitest --watch"
  }
}
```

## Testing Strategy

### Unit Tests
- **API Clients**: Mock fetch, test request/response handling
- **React Hooks**: Use `@testing-library/react-hooks` for hook testing
- **Svelte Stores**: Test store methods and state updates

### Integration Tests
- Test API client + hook integration
- Test store + API client integration

### Test Coverage Goals
- API clients: 80%+ coverage
- Hooks: 80%+ coverage
- Stores: 70%+ coverage

## Dependencies Summary

### Visualizer
- `vitest` ^1.0.0
- `@vitest/ui` ^1.0.0 (optional)
- `@vitest/coverage-v8` ^1.0.0
- `@testing-library/svelte` ^4.0.0
- `@testing-library/jest-dom` ^6.0.0
- `jsdom` ^23.0.0

### Frontend
- `vitest` ^1.0.0
- `@testing-library/react` ^14.0.0
- `@testing-library/react-hooks` ^8.0.0
- `jsdom` ^23.0.0

## Notes
- Vitest uses Jest-compatible API, so tests look familiar
- Can use Chai-style assertions via Vitest's `expect` API
- If user specifically wants Mocha+Chai, we can configure that instead
- Vitest is recommended for Vite projects (faster, better integration)
- Tests run in watch mode by default in development

## Verification
After setup:
1. Run `npm test` in visualizer/ - should run tests
2. Run `npm test` in frontend/ - should run tests
3. Verify test files are discovered
4. Verify tests pass with example implementations