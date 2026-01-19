# Evolve UI Monitor - Technical Requirements

**Date**: 2026-01-18 07:32:00 PST
**Status**: Requirements Phase
**Based on**: `UI_DESIGN_DOC_2026-01-18_evolve-ui-monitor.md`

---

## Overview

This document breaks down the design document into implementable technical specifications for the Evolve UI Monitor dashboard.

---

## Component Architecture

### 1. Runs List Component
**Purpose**: Display all `/evolve-a-ui` executions

**Technical Specs**:
- **Data Source**: Scan `_genetics/ui_evolution/` for HTML files matching pattern `{timestamp}_evolved_ui.html`
- **Display Format**: Table or card list
- **Columns/Fields**:
  - Timestamp (extracted from filename: `YYYYMMDD_HHMMSS`)
  - Run ID (timestamp-based identifier)
  - Status/Phase (inferred from artifacts present)
  - Context (from `{timestamp}_context_analysis.md` if exists)
  - Artifact Count (HTML, screenshots, case files, docs)
- **Sorting**: Default by timestamp (newest first)
- **Filtering**: By date range, phase, status (future)

**Implementation**:
- Scan directory: `_genetics/ui_evolution/`
- Parse filenames: Extract timestamp using regex `(\d{8}_\d{6})`
- Read context analysis files: `{timestamp}_context_analysis.md`
- Determine phase from artifacts:
  - Analysis: Has design doc
  - Requirements: Has requirements doc
  - Wireframe: Has wireframe screenshot
  - Development: Has multiple screenshots
  - Complete: Has final HTML

---

### 2. Run Details Component
**Purpose**: Expandable view showing all artifacts for a specific run

**Technical Specs**:
- **Trigger**: Click/expand on run item
- **Layout**: Accordion or modal
- **Sections**:
  1. **Run Metadata**
     - Timestamp
     - Run ID
     - Phase/Status
     - Context summary
  2. **Artifacts List**
     - HTML files (with preview link)
     - Screenshots (thumbnails)
     - Case files (links)
     - Design documents (links)
     - Requirements documents (links)
  3. **Process Timeline**
     - Visual timeline showing phases
     - Steps completed
     - Screenshots at each step

**Implementation**:
- Group files by timestamp prefix
- Match files across directories:
  - `_genetics/ui_evolution/{timestamp}_*.html`
  - `_genetics/ui_evolution/{timestamp}_context_analysis.md`
  - `_work_efforts/{timestamp}_ui_design_doc.md`
  - `_work_efforts/{timestamp}_ui_requirements.md`
  - `_work_efforts/{timestamp}_wireframe.png`
  - `_work_efforts/{timestamp}_*.png` (screenshots)
  - `_work_efforts/proof_cases/case_{timestamp}_*.md`

---

### 3. Artifact Gallery Component
**Purpose**: Visual display of screenshots and HTML previews

**Technical Specs**:
- **Screenshots**:
  - Display as thumbnails (max 200px width)
  - Click to view full size
  - Group by run
  - Show filename/timestamp
- **HTML Previews**:
  - Link to open in new tab
  - Optional: iframe preview (future)
- **Case Files**:
  - List with title/claim
  - Link to full case file
  - Show verdict (PROVEN/DISPROVEN)

**Implementation**:
- Image thumbnails: Use `<img>` with `max-width: 200px`
- File links: Use relative paths from project root
- Case file parsing: Read markdown, extract claim and verdict

---

### 4. Process Timeline Component
**Purpose**: Show progress through phases

**Technical Specs**:
- **Phases**:
  1. Analysis (design doc exists)
  2. Requirements (requirements doc exists)
  3. Wireframe (wireframe screenshot exists)
  4. Development (multiple screenshots exist)
  5. Complete (final HTML exists)
- **Display**: Horizontal timeline or vertical steps
- **Indicators**: 
  - Completed: ✅
  - In Progress: ⏳
  - Not Started: ⭕
- **Screenshots**: Show screenshot for each completed phase

**Implementation**:
- Check for artifacts to determine phase:
  - Phase 1: `*_ui_design_doc.md` exists
  - Phase 2: `*_ui_requirements.md` exists
  - Phase 3: `*_wireframe.png` exists
  - Phase 4: Multiple `*_{element}.png` exist
  - Phase 5: `{timestamp}_evolved_ui.html` exists

---

### 5. File Browser Component
**Purpose**: Navigate to generated files

**Technical Specs**:
- **File Types**:
  - HTML files (open in browser)
  - Screenshots (view/download)
  - Markdown files (view in browser or editor)
  - Case files (view in browser)
- **Actions**:
  - View: Open file
  - Download: Download file
  - Copy Path: Copy file path to clipboard
- **Grouping**: By run, by type, by date

**Implementation**:
- File links: Use `file://` protocol for local files
- Relative paths: Calculate from project root
- Download: Use `<a download>` attribute

---

### 6. Search/Filter Component (Future)
**Purpose**: Find runs by date, context, phase

**Technical Specs**:
- **Filters**:
  - Date range picker
  - Phase selector (dropdown)
  - Status selector
- **Search**:
  - Search context analysis content
  - Search case file claims
- **Implementation**: Client-side filtering of loaded data

---

## Data Collection

### File Scanning Logic

**Primary Scan**: `_genetics/ui_evolution/`
```python
# Find all HTML files matching pattern
pattern = r'(\d{8}_\d{6})_evolved_ui\.html'
# Extract timestamp, create run object
```

**Secondary Scans**:
1. `_genetics/ui_evolution/{timestamp}_context_analysis.md`
2. `_work_efforts/{timestamp}_ui_design_doc.md`
3. `_work_efforts/{timestamp}_ui_requirements.md`
4. `_work_efforts/{timestamp}_wireframe.png`
5. `_work_efforts/{timestamp}_*.png` (all screenshots)
6. `_work_efforts/proof_cases/case_{timestamp}_*.md`

**Data Structure**:
```typescript
interface EvolveUIRun {
  runId: string;           // YYYYMMDD_HHMMSS
  timestamp: Date;         // Parsed from runId
  phase: Phase;            // Analysis | Requirements | Wireframe | Development | Complete
  artifacts: {
    html: string[];        // Paths to HTML files
    contextAnalysis?: string; // Path to context analysis
    designDoc?: string;    // Path to design doc
    requirements?: string;  // Path to requirements
    wireframe?: string; // Path to wireframe screenshot
    screenshots: string[]; // Paths to all screenshots
    caseFiles: string[];   // Paths to case files
  };
  context?: string;        // Summary from context analysis
}
```

---

## Layout Structure

### Page Layout
```
┌─────────────────────────────────────────┐
│ Header: "Evolve UI Monitor"             │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Runs List (Table/Cards)           │ │
│  │ - Run 1 [Expand]                  │ │
│  │ - Run 2 [Expand]                  │ │
│  │ - Run 3 [Expand]                  │ │
│  └───────────────────────────────────┘ │
│                                         │
│  ┌───────────────────────────────────┐ │
│  │ Run Details (Expanded)            │ │
│  │ - Metadata                        │ │
│  │ - Process Timeline                │ │
│  │ - Artifact Gallery                │ │
│  │ - File Browser                    │ │
│  └───────────────────────────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

### Responsive Design
- **Desktop**: Two-column (Runs List | Run Details)
- **Mobile**: Single column, stacked

---

## Technical Stack

### Frontend
- **Framework**: SvelteKit (existing visualizer)
- **Location**: `visualizer/src/routes/evolve-ui-monitor/+page.svelte`
- **Styling**: Box model CSS (no !important)
- **Icons**: Unicode/emoji or simple SVG

### Backend (if needed)
- **API Endpoint**: `/api/evolve-ui-runs` (FastAPI)
- **Function**: Scan directories, parse files, return structured data
- **Location**: `src/waft/api/routes/evolve_ui_monitor.py`

### Data Processing
- **File Scanning**: Python script or Node.js
- **Timestamp Parsing**: Regex `(\d{8}_\d{6})`
- **Phase Detection**: Check artifact existence

---

## Implementation Phases

### Phase 1: MVP (View-Only)
1. Scan `_genetics/ui_evolution/` for HTML files
2. Extract timestamps from filenames
3. Display runs list (timestamp, status)
4. Basic run details (artifacts list)
5. Links to view HTML files

### Phase 2: Enhanced Display
1. Process timeline component
2. Screenshot thumbnails
3. Case file integration
4. Design doc/requirements links

### Phase 3: Advanced Features
1. Search/filter
2. Context analysis display
3. HTML previews
4. File download

---

## File Structure

```
visualizer/src/routes/evolve-ui-monitor/
├── +page.svelte          # Main page component
├── components/
│   ├── RunsList.svelte   # Runs list component
│   ├── RunDetails.svelte # Run details component
│   ├── ProcessTimeline.svelte # Timeline component
│   ├── ArtifactGallery.svelte # Gallery component
│   └── FileBrowser.svelte # File browser component
└── lib/
    └── evolveUiScanner.ts # File scanning logic
```

---

## API Endpoints (if needed)

### GET /api/evolve-ui-runs
**Purpose**: Get all evolve-a-ui runs

**Response**:
```json
{
  "runs": [
    {
      "runId": "20260118_073200",
      "timestamp": "2026-01-18T07:32:00Z",
      "phase": "Complete",
      "artifacts": {
        "html": ["_genetics/ui_evolution/20260118_073200_evolved_ui.html"],
        "contextAnalysis": "_genetics/ui_evolution/20260118_073200_context_analysis.md",
        "screenshots": ["_work_efforts/20260118_073200_wireframe.png"],
        "caseFiles": []
      }
    }
  ]
}
```

---

## Security Requirements (CRITICAL)

### 1. File Exclusion List
**Requirement**: Never scan or display sensitive files
**Implementation**:
- Exclude patterns: `.env`, `*.key`, `*.pem`, `secrets.*`, `*.secret`, `*.token`
- Exclude directories: `node_modules/`, `.git/`, `__pycache__/`, `.venv/`
- Validate file extensions before processing
- Never scan files outside project root

**Code Pattern**:
```typescript
const SENSITIVE_PATTERNS = [
  /\.env$/,
  /\.key$/,
  /\.pem$/,
  /secrets?\./i,
  /\.secret$/,
  /\.token$/
];

function isSensitiveFile(filename: string): boolean {
  return SENSITIVE_PATTERNS.some(pattern => pattern.test(filename));
}
```

### 2. Path Validation
**Requirement**: Prevent path traversal attacks
**Implementation**:
- Use existing `_validate_path_in_storage` pattern from `src/waft/utils.py`
- Reject paths with `..`
- Reject absolute paths outside project root
- Normalize paths before use
- Validate paths are within project boundary

**Code Pattern**:
```typescript
function validatePath(filePath: string, projectRoot: string): boolean {
  const path = Path.resolve(projectRoot, filePath);
  const resolved = path.resolve();
  const base = Path.resolve(projectRoot);
  
  // Reject path traversal
  if (filePath.includes('..')) return false;
  
  // Must be within project root
  return resolved.startsWith(base);
}
```

### 3. File Permissions
**Requirement**: Set restrictive file permissions
**Implementation**:
- Files: `0o600` (owner read/write only)
- Directories: `0o700` (owner read/write/execute only)
- Validate permissions on read (warn if insecure)
- Use existing pattern from `work_effort_service.py`: `chmod(0o700)`

**Code Pattern**:
```python
# When creating files
file_path.chmod(0o600)

# When creating directories
dir_path.chmod(0o700)

# When reading, validate permissions
stat_info = file_path.stat()
mode = stat_info.st_mode & 0o777
if mode & 0o044:  # Group or world readable
    logger.warning(f"Insecure permissions: {oct(mode)}")
```

### 4. Content Sanitization
**Requirement**: Filter sensitive content before display
**Implementation**:
- Filter patterns: API keys, passwords, tokens, secrets
- Sanitize context analysis content
- Sanitize case file content
- Never display raw file content without sanitization
- Truncate or redact sensitive sections

**Code Pattern**:
```typescript
const SENSITIVE_PATTERNS = [
  /api[_-]?key\s*[:=]\s*['"]?([a-zA-Z0-9_-]{20,})/gi,
  /password\s*[:=]\s*['"]?([^'"]+)/gi,
  /token\s*[:=]\s*['"]?([a-zA-Z0-9_-]{20,})/gi
];

function sanitizeContent(content: string): string {
  let sanitized = content;
  SENSITIVE_PATTERNS.forEach(pattern => {
    sanitized = sanitized.replace(pattern, '[REDACTED]');
  });
  return sanitized;
}
```

### 5. Content Security Policy
**Requirement**: Prevent XSS from file content
**Implementation**:
- Add CSP headers to SvelteKit responses
- Sanitize HTML content before display
- Use textContent instead of innerHTML where possible
- Validate file types before processing

---

## Error Handling Requirements (HIGH)

### 1. File I/O Error Handling
**Requirement**: Handle all file system errors gracefully
**Implementation**:
- Try/except blocks for all file operations
- Handle `PermissionError`: Show clear error message
- Handle `FileNotFoundError`: Skip missing files, continue scan
- Handle `IOError`: Log error, continue with other files
- Handle `OSError`: Log error, graceful degradation

**Code Pattern**:
```typescript
try {
  const content = await readFile(filePath);
  return content;
} catch (error) {
  if (error.code === 'ENOENT') {
    logger.warn(`File not found: ${filePath}`);
    return null; // Skip missing files
  } else if (error.code === 'EACCES') {
    logger.error(`Permission denied: ${filePath}`);
    throw new Error(`Cannot read ${filePath}: Permission denied`);
  } else {
    logger.error(`Error reading ${filePath}: ${error.message}`);
    return null; // Graceful degradation
  }
}
```

### 2. Network Error Handling
**Requirement**: Handle API unavailability
**Implementation**:
- Fallback to direct file scanning if API unavailable
- Handle timeout errors (10s timeout)
- Handle 401/403 errors (auth issues)
- Handle 500 errors (server errors)
- Show user-friendly error messages

### 3. Parsing Error Handling
**Requirement**: Handle malformed files gracefully
**Implementation**:
- Handle JSON parsing errors (invalid JSON)
- Handle markdown parsing errors (malformed case files)
- Handle image loading errors (corrupted images)
- Handle encoding errors (non-UTF-8 files)
- Continue processing other files on error

---

## Input Validation Requirements (HIGH)

### 1. Timestamp Validation
**Requirement**: Validate extracted timestamps
**Implementation**:
- Validate format: `YYYYMMDD_HHMMSS`
- Validate date is reasonable (not future, not before 2020)
- Handle malformed filenames gracefully
- Sanitize timestamps before use in queries

**Code Pattern**:
```typescript
function validateTimestamp(timestamp: string): boolean {
  // Format check
  if (!/^\d{8}_\d{6}$/.test(timestamp)) return false;
  
  // Parse date
  const year = parseInt(timestamp.substring(0, 4));
  const month = parseInt(timestamp.substring(4, 6));
  const day = parseInt(timestamp.substring(6, 8));
  
  // Reasonable date check
  if (year < 2020 || year > 2030) return false;
  if (month < 1 || month > 12) return false;
  if (day < 1 || day > 31) return false;
  
  // Not in future
  const date = new Date(year, month - 1, day);
  if (date > new Date()) return false;
  
  return true;
}
```

### 2. File Type Validation
**Requirement**: Validate file types before processing
**Implementation**:
- Validate file extensions
- Validate MIME types for images
- Reject unexpected file types
- Handle missing extensions

### 3. File Size Validation
**Requirement**: Enforce file size limits
**Implementation**:
- Max file size: 10MB per file
- Max total scan size: 100MB
- Reject files exceeding limits
- Show error for oversized files

---

## Resource Limits Requirements (HIGH)

### 1. Pagination
**Requirement**: Limit number of runs displayed
**Implementation**:
- Default: 50 runs per page
- Load more button for additional runs
- Lazy loading for large lists
- Virtual scrolling for performance

### 2. Memory Limits
**Requirement**: Limit memory usage
**Implementation**:
- Thumbnail max size: 200px width
- Lazy load images (only load visible thumbnails)
- Limit concurrent file reads
- Clear unused data from memory

### 3. Timeout Limits
**Requirement**: Prevent hanging operations
**Implementation**:
- File read timeout: 5 seconds
- API request timeout: 10 seconds
- Total scan timeout: 30 seconds
- Show timeout errors to user

---

## Testing Requirements

### 1. Unit Tests
- Test path validation functions
- Test timestamp extraction and validation
- Test file exclusion logic
- Test content sanitization
- Test error handling

### 2. Integration Tests
- Test full file scanning flow
- Test API endpoint (if used)
- Test error scenarios
- Test concurrent access

### 3. Security Tests
- Test path traversal prevention
- Test sensitive file exclusion
- Test content sanitization
- Test permission validation

### 4. E2E Tests
- Test full UI flow
- Test with real files
- Test error states
- Test empty states

---

## UX Requirements

### 1. Loading States
**Requirement**: Show progress during operations
**Implementation**:
- Loading spinner during file scan
- Progress indicator for large scans
- Skeleton screens while loading
- Disable interactions during load

### 2. Empty States
**Requirement**: Handle empty data gracefully
**Implementation**:
- Show message when no runs exist
- Show message when scan finds nothing
- Provide helpful guidance
- Suggest next steps

### 3. Error States
**Requirement**: Show errors clearly
**Implementation**:
- User-friendly error messages
- Retry buttons for failed operations
- Error details in expandable section
- Log errors for debugging

---

## Caching Requirements

### 1. Scan Result Caching
**Requirement**: Cache file scan results
**Implementation**:
- Cache scan results in memory
- Cache key: directory path + last modified time
- Invalidate cache on file changes
- Cache TTL: 5 minutes

### 2. Image Caching
**Requirement**: Cache image thumbnails
**Implementation**:
- Browser cache for images
- Cache-Control headers
- Lazy loading for off-screen images

---

## Concurrency Requirements

### 1. Concurrent Access Handling
**Requirement**: Handle multiple simultaneous scans
**Implementation**:
- Use file locking or atomic operations
- Prevent duplicate scans
- Queue scan requests
- Show scan status

### 2. Race Condition Prevention
**Requirement**: Prevent race conditions
**Implementation**:
- Atomic file operations
- Lock files during read/write
- Validate file state after operations

---

## Logging Requirements

### 1. Operation Logging
**Requirement**: Log all file operations
**Implementation**:
- Log file scans (start, end, count)
- Log errors (with context)
- Log security events (path validation failures)
- Log performance metrics

### 2. Error Tracking
**Requirement**: Track errors for debugging
**Implementation**:
- Log all errors with stack traces
- Log file paths that fail
- Log permission errors
- Log parsing errors

---

## Success Criteria (Technical)

- ✅ Can scan `_genetics/ui_evolution/` and find all runs
- ✅ Can extract timestamps from filenames
- ✅ Can determine phase from artifacts
- ✅ Can display runs list
- ✅ Can show run details with artifacts
- ✅ Can link to generated HTML files
- ✅ Can display screenshots as thumbnails
- ✅ Can show process timeline
- ✅ **Security**: Path validation prevents traversal
- ✅ **Security**: Sensitive files excluded
- ✅ **Security**: Content sanitized before display
- ✅ **Error Handling**: All errors handled gracefully
- ✅ **Validation**: All inputs validated
- ✅ **Resources**: Limits prevent exhaustion

---

**Ready for Wireframe Phase** (with security requirements addressed)
