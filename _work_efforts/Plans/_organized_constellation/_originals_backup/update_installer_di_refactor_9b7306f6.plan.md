---
name: Update Installer DI Refactor
overview: Refactor update-installer.js and update-checker.js for dependency injection, enabling fully mocked integration tests that run without network access or system commands.
todos:
  - id: refactor-installer
    content: Refactor update-installer.js to accept downloadFn and extractFn via constructor
    status: completed
  - id: refactor-checker
    content: Refactor update-checker.js to accept fetchFn via constructor
    status: completed
  - id: create-mocked-tests
    content: Create tests/update-installer-mocked.test.js with fully mocked dependencies
    status: completed
  - id: verify-existing
    content: Verify existing tests still pass after refactoring
    status: completed
  - id: update-docs
    content: Update work effort and devlog with completion status
    status: completed
---

# Stage 2: Update Installer Dependency Injection Refactor

## Objective

Make the update system testable by injecting download and extract functions, allowing tests to run offline without `unzip`.

## Files to Modify

### 1. [`scripts/update-installer.js`](scripts/update-installer.js)

**Changes:**

- Add `downloadFn` and `extractFn` to constructor options
- Extract current `downloadFile` method into `_defaultDownload`
- Extract current `extractUpdate` logic into `_defaultExtract`
- Update `downloadUpdate()` to use `this.downloadFn`
- Update `extractUpdate()` to use `this.extractFn`
```javascript
constructor(options = {}) {
  // ... existing options ...
  
  // Injectable dependencies
  this.downloadFn = options.downloadFn || this._defaultDownload.bind(this);
  this.extractFn = options.extractFn || this._defaultExtract.bind(this);
}

_defaultDownload(url, destPath) {
  return this.downloadFile(url, destPath, 0);
}

_defaultExtract(zipPath, destDir) {
  this.ensureCommandAvailable('unzip');
  execSync(`unzip -q -o "${zipPath}" -d "${destDir}"`, { stdio: 'inherit' });
}
```




### 2. [`scripts/update-checker.js`](scripts/update-checker.js)

**Changes:**

- Add `fetchFn` to constructor options
- Extract `requestJson` into injectable dependency
- Update `fetchLatestRelease()` to use `this.fetchFn`
```javascript
constructor(options = {}) {
  // ... existing options ...
  this.fetchFn = options.fetchFn || this._defaultFetch.bind(this);
}

_defaultFetch(url) {
  return this.requestJson(url);
}
```




### 3. New: [`tests/update-installer-mocked.test.js`](tests/update-installer-mocked.test.js)

**Mocked Tests:**

- Mock `downloadFn`: writes fake content to destination
- Mock `extractFn`: creates mock directory structure
- Mock `fetchFn`: returns fake GitHub API response

**Test Scenarios:**

- `install()` calls downloadFn with correct URL
- `install()` calls extractFn with correct paths
- `install()` creates backup before modifying files
- `install()` rolls back on verification failure
- `checkForUpdates()` uses fetchFn
- Rollback restores files correctly

## Implementation Order

1. Refactor `update-installer.js` - add DI while preserving existing behavior
2. Refactor `update-checker.js` - add DI for fetch
3. Create mocked test file with full test coverage
4. Verify existing tests still pass
5. Update package.json test script

## Test Approach

Using Node.js built-in `assert` (matching existing test style):

```javascript
// Mock functions
const mockDownload = async (url, destPath) => {
  fs.writeFileSync(destPath, 'mock-zip-content');
};

const mockExtract = (zipPath, destDir) => {
  fs.mkdirSync(destDir, { recursive: true });
  fs.mkdirSync(path.join(destDir, 'cursor-coding-protocols-2.0.0'));
  fs.writeFileSync(
    path.join(destDir, 'cursor-coding-protocols-2.0.0', 'package.json'),
    JSON.stringify({ version: '2.0.0' })
  );
};

const installer = new UpdateInstaller({
  rootDir: TEST_ROOT,
  downloadFn: mockDownload,
  extractFn: mockExtract
});
```



## Success Criteria

- [ ] `update-installer.js` accepts `downloadFn` and `extractFn` options
- [ ] `update-checker.js` accepts `fetchFn` option
- [ ] New mocked tests run without network access
- [ ] New mocked tests run without `unzip` command
- [ ] Existing tests continue to pass