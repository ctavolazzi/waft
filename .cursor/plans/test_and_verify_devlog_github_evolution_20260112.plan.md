# Testing & Verification Plan: Devlog System & GitHub Feature Branch Evolution

**Date**: 2026-01-12  
**Status**: Testing Plan  
**Related Plan**: `evolve_devlog_system_and_github_feature_branch_evolution_b4746c23.plan.md`

---

## Overview

This plan defines comprehensive testing and verification procedures for:
1. **Devlog System Evolution**: Categorized entry system with source tracking
2. **GitHub Feature Branch Integration**: Feature branch workflow for evolution commands

---

## Part 1: Devlog System Testing

### 1.1 Unit Tests: DevlogManager Class

#### Test File: `tests/test_devlog_manager.py`

**Test Cases**:

1. **Test DevlogManager Initialization**
   - ✅ Creates directory structure if missing
   - ✅ Loads existing index.json if present
   - ✅ Handles missing devlog directory gracefully
   - ✅ Validates project path

2. **Test Entry Writing**
   - ✅ Writes entry to correct source directory (`by_source/command/`)
   - ✅ Writes entry to correct category directory (`by_category/feature/`)
   - ✅ Writes entry to date directory (`by_date/2026-01-12/`)
   - ✅ Generates correct filename format: `YYYY-MM-DD_HHMMSS_[source]_[category].md`
   - ✅ Includes all metadata (timestamp, source, category, context)
   - ✅ Handles special characters in content
   - ✅ Updates index.json after write

3. **Test Entry Reading**
   - ✅ `get_recent_entries(limit=5)` returns correct number
   - ✅ `get_recent_entries(source="command")` filters by source
   - ✅ `get_recent_entries(category="feature")` filters by category
   - ✅ `get_recent_entries(source="command", category="feature")` filters by both
   - ✅ Returns entries in reverse chronological order
   - ✅ Handles missing entries gracefully

4. **Test Source Detection**
   - ✅ Detects `command` source from `.cursor/commands/` execution
   - ✅ Detects `script` source from `scripts/` directory
   - ✅ Detects `api` source from API routes
   - ✅ Detects `being` source from Being system
   - ✅ Detects `workflow` source from workflow commands
   - ✅ Falls back to `manual` for unknown sources

5. **Test Context Capture**
   - ✅ Captures git branch name
   - ✅ Captures work effort ID (if active)
   - ✅ Captures Being ID (if in Being context)
   - ✅ Captures command name (if from command)
   - ✅ Captures file paths modified
   - ✅ Captures session statistics

6. **Test Index Management**
   - ✅ Creates index.json on first entry
   - ✅ Updates index.json with new entries
   - ✅ Maintains entry metadata in index
   - ✅ Handles index corruption gracefully
   - ✅ Rebuilds index from directory structure if needed

7. **Test Migration**
   - ✅ Parses existing `devlog.md` correctly
   - ✅ Extracts all entries with dates
   - ✅ Categorizes entries by content analysis
   - ✅ Creates categorized entry files
   - ✅ Preserves all original content
   - ✅ Updates index.json with migrated entries
   - ✅ Keeps `devlog.md` as read-only archive

**Verification Commands**:
```bash
# Run unit tests
pytest tests/test_devlog_manager.py -v

# Check coverage
pytest tests/test_devlog_manager.py --cov=src/waft/core/devlog --cov-report=html
```

---

### 1.2 Integration Tests: Existing Code Updates

#### Test File: `tests/test_devlog_integration.py`

**Test Cases**:

1. **Test Visualizer Integration**
   - ✅ `Visualizer._get_recent_devlog()` uses DevlogManager
   - ✅ Returns same format as before (list of strings)
   - ✅ Returns last 5 entries
   - ✅ Handles missing devlog gracefully
   - ✅ Works with both old and new devlog structure

2. **Test waft_status.py Integration**
   - ✅ `get_recent_activity()` uses DevlogManager
   - ✅ Returns devlog entries in expected format
   - ✅ Handles missing devlog gracefully
   - ✅ Works with both old and new devlog structure

3. **Test API Integration**
   - ✅ `/work-efforts` endpoint returns devlog entries
   - ✅ Entries come from DevlogManager
   - ✅ Format matches expected API response
   - ✅ Handles errors gracefully

4. **Test Command Integration**
   - ✅ Commands write to devlog using DevlogManager
   - ✅ Source detection works correctly
   - ✅ Context captured properly
   - ✅ Entries appear in correct directories

**Verification Commands**:
```bash
# Run integration tests
pytest tests/test_devlog_integration.py -v

# Test visualizer directly
python -c "from src.waft.core.visualizer import Visualizer; v = Visualizer('.'); print(v._get_recent_devlog())"

# Test waft_status
python scripts/waft_status.py --check-status

# Test API endpoint
curl http://localhost:8000/api/work-efforts | jq '.devlog'
```

---

### 1.3 Migration Verification

#### Test File: `tests/test_devlog_migration.py`

**Test Cases**:

1. **Test Migration Script**
   - ✅ Parses all entries from `devlog.md`
   - ✅ Categorizes entries correctly
   - ✅ Creates all expected entry files
   - ✅ Preserves original content
   - ✅ Updates index.json
   - ✅ Keeps `devlog.md` intact

2. **Test Backward Compatibility**
   - ✅ Old code can still read `devlog.md`
   - ✅ New code reads from categorized structure
   - ✅ Both systems work simultaneously
   - ✅ No data loss during migration

3. **Test Migration Rollback**
   - ✅ Can restore from backup if needed
   - ✅ Original `devlog.md` unchanged
   - ✅ Can re-run migration safely

**Verification Commands**:
```bash
# Backup current devlog
cp _work_efforts/devlog.md _work_efforts/devlog.md.backup

# Run migration
python scripts/migrate_devlog.py

# Verify migration
python -c "from src.waft.core.devlog import DevlogManager; dm = DevlogManager('.'); print(f'Entries: {len(dm.get_recent_entries(limit=1000))}')"

# Check directory structure
tree _work_efforts/devlog/ -L 3

# Verify index
cat _work_efforts/devlog/index.json | jq '.entries | length'
```

---

### 1.4 End-to-End Testing: Devlog System

#### Manual Test Scenarios

**Scenario 1: Command Entry Creation**
```bash
# Execute a command that writes to devlog
# (e.g., /checkpoint, /evolve, etc.)

# Verify entry created
ls -la _work_efforts/devlog/by_source/command/
ls -la _work_efforts/devlog/by_category/feature/
ls -la _work_efforts/devlog/by_date/2026-01-12/

# Check entry content
cat _work_efforts/devlog/by_source/command/2026-01-12_*_command_*.md

# Verify index updated
cat _work_efforts/devlog/index.json | jq '.entries[-1]'
```

**Scenario 2: Script Entry Creation**
```bash
# Run a script that writes to devlog
python scripts/waft_status.py --check-status

# Verify entry created
ls -la _work_efforts/devlog/by_source/script/

# Check entry content
cat _work_efforts/devlog/by_source/script/2026-01-12_*_script_*.md
```

**Scenario 3: API Entry Creation**
```bash
# Make API call that writes to devlog
curl -X POST http://localhost:8000/api/some-endpoint

# Verify entry created
ls -la _work_efforts/devlog/by_source/api/
```

**Scenario 4: Query Entries**
```bash
# Query recent entries
python -c "from src.waft.core.devlog import DevlogManager; dm = DevlogManager('.'); print(dm.get_recent_entries(limit=5))"

# Query by source
python -c "from src.waft.core.devlog import DevlogManager; dm = DevlogManager('.'); print(dm.get_recent_entries(source='command', limit=5))"

# Query by category
python -c "from src.waft.core.devlog import DevlogManager; dm = DevlogManager('.'); print(dm.get_recent_entries(category='feature', limit=5))"
```

**Scenario 5: Visualizer Integration**
```bash
# Start visualizer
python -m src.waft.main

# Check API response
curl http://localhost:8000/api/work-efforts | jq '.devlog'

# Verify entries appear in UI
# (Open browser to visualizer)
```

---

## Part 2: GitHub Feature Branch Integration Testing

### 2.1 Unit Tests: GitHub Integration

#### Test File: `tests/test_github_integration.py`

**Test Cases**:

1. **Test GitHub MCP Availability**
   - ✅ Detects GitHub MCP availability
   - ✅ Handles missing GitHub MCP gracefully
   - ✅ Falls back to local-only mode if unavailable
   - ✅ Logs warnings appropriately

2. **Test Branch Creation**
   - ✅ Creates feature branch with correct name pattern
   - ✅ Handles existing branch names (adds suffix)
   - ✅ Sets up branch from correct base (main/master)
   - ✅ Handles branch creation errors

3. **Test Commit Strategy**
   - ✅ Commits at correct points in workflow
   - ✅ Commit messages follow format: `[evolve] [being_id] Phase: Description`
   - ✅ Commits include Being ID for traceability
   - ✅ Handles commit errors gracefully

4. **Test Pull Request Creation**
   - ✅ Creates PR with correct title
   - ✅ PR description includes evolution summary
   - ✅ PR includes genetic lineage
   - ✅ PR includes Being metadata
   - ✅ PR includes workflow results
   - ✅ Handles PR creation errors

5. **Test Branch Naming**
   - ✅ Generates correct branch names: `evolve/[being_id]`
   - ✅ Handles special characters in being_id
   - ✅ Handles long being_ids (truncates if needed)
   - ✅ Handles duplicate branch names

**Verification Commands**:
```bash
# Run unit tests
pytest tests/test_github_integration.py -v

# Mock GitHub MCP for testing
# (Use pytest fixtures to mock MCP responses)
```

---

### 2.2 Integration Tests: Evolve Workflow

#### Test File: `tests/test_evolve_github_workflow.py`

**Test Cases**:

1. **Test Full Evolve Workflow with GitHub**
   - ✅ Creates feature branch before Being spawn
   - ✅ Commits Being spawn to branch
   - ✅ Commits workflow phases to branch
   - ✅ Commits genetic lineage to branch
   - ✅ Commits evolution documentation to branch
   - ✅ Creates PR at end (if configured)
   - ✅ Returns learnings to Source

2. **Test Evolve Workflow without GitHub**
   - ✅ Works correctly when GitHub MCP unavailable
   - ✅ Logs warning about GitHub integration skipped
   - ✅ Continues with local evolution
   - ✅ Documents in devlog that GitHub skipped

3. **Test Branch Cleanup**
   - ✅ Handles branch cleanup on error
   - ✅ Preserves branch on success (for PR)
   - ✅ Can delete branch after PR merge

4. **Test Multiple Evolutions**
   - ✅ Each evolution gets unique branch
   - ✅ No branch name conflicts
   - ✅ Can run multiple evolutions in parallel

**Verification Commands**:
```bash
# Test evolve workflow (dry run)
python scripts/execute_full_evolve.py --dry-run --github-test

# Test evolve workflow (full)
python scripts/execute_full_evolve.py --github-test

# Check branches created
gh repo list-branches ctavolazzi/waft | grep evolve/

# Check PRs created
gh pr list --repo ctavolazzi/waft | grep evolve
```

---

### 2.3 End-to-End Testing: GitHub Integration

#### Manual Test Scenarios

**Scenario 1: Full Evolution with GitHub**
```bash
# Execute evolve command
/evolve

# Verify branch created
gh repo view ctavolazzi/waft --json defaultBranchRef
git branch -r | grep evolve/

# Check commits on branch
git log evolve/[being_id] --oneline

# Verify PR created (if configured)
gh pr list --repo ctavolazzi/waft --head evolve/[being_id]

# Check PR content
gh pr view [PR_NUMBER] --repo ctavolazzi/waft
```

**Scenario 2: Evolution without GitHub (Fallback)**
```bash
# Disable GitHub MCP (or simulate unavailability)
# Execute evolve command
/evolve

# Verify local evolution works
# Check devlog for GitHub skip message
cat _work_efforts/devlog/by_source/workflow/2026-01-12_*_workflow_*.md | grep -i github
```

**Scenario 3: Multiple Evolutions**
```bash
# Execute multiple evolve commands
/evolve
/evolve
/evolve

# Verify unique branches
git branch -r | grep evolve/ | wc -l  # Should be 3

# Verify no conflicts
git branch -r | grep evolve/ | sort | uniq -d  # Should be empty
```

**Scenario 4: PR Review and Merge**
```bash
# Review PR
gh pr view [PR_NUMBER] --repo ctavolazzi/waft

# Check PR content includes:
# - Evolution summary
# - Genetic lineage
# - Being metadata
# - Workflow results

# Merge PR (if approved)
gh pr merge [PR_NUMBER] --repo ctavolazzi/waft --squash

# Verify branch deleted after merge
git branch -r | grep evolve/[being_id]  # Should not exist
```

---

## Part 3: Integration Testing

### 3.1 Combined System Testing

#### Test File: `tests/test_devlog_github_integration.py`

**Test Cases**:

1. **Test Devlog Entries from GitHub Workflow**
   - ✅ Evolve workflow writes devlog entries
   - ✅ Entries include GitHub branch information
   - ✅ Entries include PR information (if created)
   - ✅ Source detection works for workflow entries

2. **Test GitHub Context in Devlog**
   - ✅ Devlog entries capture git branch
   - ✅ Devlog entries capture PR number (if created)
   - ✅ Devlog entries capture commit SHAs
   - ✅ Context properly formatted in entries

3. **Test End-to-End Flow**
   - ✅ Execute evolve → Creates branch → Writes devlog → Creates PR
   - ✅ All systems work together
   - ✅ No data loss or corruption
   - ✅ All entries properly categorized

**Verification Commands**:
```bash
# Run combined tests
pytest tests/test_devlog_github_integration.py -v

# Execute full workflow
/evolve

# Verify devlog entries
cat _work_efforts/devlog/by_source/workflow/2026-01-12_*_workflow_*.md

# Check entries include GitHub context
grep -i "branch\|pr\|commit" _work_efforts/devlog/by_source/workflow/2026-01-12_*_workflow_*.md
```

---

## Part 4: Performance Testing

### 4.1 Devlog System Performance

**Test Cases**:

1. **Test Entry Write Performance**
   - ✅ Write 100 entries in < 5 seconds
   - ✅ Index updates don't block writes
   - ✅ No performance degradation with many entries

2. **Test Entry Read Performance**
   - ✅ Read 1000 recent entries in < 1 second
   - ✅ Filtered queries (by source/category) fast
   - ✅ Index lookups efficient

3. **Test Migration Performance**
   - ✅ Migrate 4596-line devlog.md in < 30 seconds
   - ✅ No memory issues with large files
   - ✅ Progress feedback during migration

**Verification Commands**:
```bash
# Performance test: Write entries
time python -c "
from src.waft.core.devlog import DevlogManager
import time
dm = DevlogManager('.')
start = time.time()
for i in range(100):
    dm.write_entry(f'Test entry {i}', 'test', 'test', {})
print(f'Time: {time.time() - start}s')
"

# Performance test: Read entries
time python -c "
from src.waft.core.devlog import DevlogManager
import time
dm = DevlogManager('.')
start = time.time()
entries = dm.get_recent_entries(limit=1000)
print(f'Time: {time.time() - start}s, Entries: {len(entries)}')
"

# Performance test: Migration
time python scripts/migrate_devlog.py
```

---

### 4.2 GitHub Integration Performance

**Test Cases**:

1. **Test Branch Creation Performance**
   - ✅ Branch creation in < 2 seconds
   - ✅ No blocking on GitHub API calls

2. **Test Commit Performance**
   - ✅ Commits don't slow down workflow
   - ✅ Batch commits when possible

3. **Test PR Creation Performance**
   - ✅ PR creation in < 5 seconds
   - ✅ Non-blocking (async if possible)

**Verification Commands**:
```bash
# Performance test: Branch creation
time python -c "
# Test branch creation speed
"

# Performance test: Full workflow
time /evolve
```

---

## Part 5: Error Handling & Edge Cases

### 5.1 Devlog System Edge Cases

**Test Cases**:

1. **Test Missing Directory**
   - ✅ Creates directory structure if missing
   - ✅ Handles permission errors gracefully

2. **Test Corrupted Index**
   - ✅ Rebuilds index if corrupted
   - ✅ Handles JSON parse errors

3. **Test Concurrent Writes**
   - ✅ Handles multiple processes writing simultaneously
   - ✅ No data loss or corruption
   - ✅ Index updates atomic

4. **Test Large Entries**
   - ✅ Handles entries > 1MB
   - ✅ Handles entries with special characters
   - ✅ Handles entries with unicode

5. **Test Invalid Sources/Categories**
   - ✅ Validates source values
   - ✅ Validates category values
   - ✅ Falls back to defaults if invalid

**Verification Commands**:
```bash
# Test missing directory
rm -rf _work_efforts/devlog/
python -c "from src.waft.core.devlog import DevlogManager; dm = DevlogManager('.'); dm.write_entry('Test', 'test', 'test', {})"
ls -la _work_efforts/devlog/  # Should exist

# Test corrupted index
echo "invalid json" > _work_efforts/devlog/index.json
python -c "from src.waft.core.devlog import DevlogManager; dm = DevlogManager('.'); dm.get_recent_entries()"
cat _work_efforts/devlog/index.json  # Should be valid JSON

# Test concurrent writes
python -c "
import multiprocessing
from src.waft.core.devlog import DevlogManager

def write_entry(i):
    dm = DevlogManager('.')
    dm.write_entry(f'Entry {i}', 'test', 'test', {})

with multiprocessing.Pool(5) as p:
    p.map(write_entry, range(50))
"
```

---

### 5.2 GitHub Integration Edge Cases

**Test Cases**:

1. **Test GitHub API Errors**
   - ✅ Handles rate limiting gracefully
   - ✅ Handles authentication errors
   - ✅ Handles network timeouts
   - ✅ Retries with backoff

2. **Test Branch Conflicts**
   - ✅ Handles existing branch names
   - ✅ Handles branch deletion conflicts
   - ✅ Handles merge conflicts

3. **Test PR Creation Errors**
   - ✅ Handles PR creation failures
   - ✅ Logs errors appropriately
   - ✅ Continues workflow if PR fails

4. **Test Git Errors**
   - ✅ Handles git not initialized
   - ✅ Handles git not configured
   - ✅ Handles uncommitted changes

**Verification Commands**:
```bash
# Test GitHub API errors (simulate)
# (Use mocking in tests)

# Test branch conflicts
git checkout -b evolve/test-being
/evolve  # Should handle existing branch

# Test PR creation errors
# (Simulate GitHub API failure)
```

---

## Part 6: Verification Checklist

### 6.1 Devlog System Verification

- [ ] **Unit Tests**: All DevlogManager tests pass
- [ ] **Integration Tests**: All integration tests pass
- [ ] **Migration**: Migration completes successfully
- [ ] **Backward Compatibility**: Old code still works
- [ ] **Directory Structure**: All directories created correctly
- [ ] **Index Management**: Index.json maintained correctly
- [ ] **Source Detection**: All sources detected correctly
- [ ] **Context Capture**: All context captured correctly
- [ ] **Entry Writing**: Entries written to all correct locations
- [ ] **Entry Reading**: Entries read correctly with filters
- [ ] **Visualizer Integration**: Visualizer shows new entries
- [ ] **waft_status Integration**: waft_status shows new entries
- [ ] **API Integration**: API returns new entries
- [ ] **Performance**: Meets performance targets
- [ ] **Error Handling**: All edge cases handled

### 6.2 GitHub Integration Verification

- [ ] **GitHub MCP**: GitHub MCP available and working
- [ ] **Branch Creation**: Branches created correctly
- [ ] **Branch Naming**: Branch names follow pattern
- [ ] **Commit Strategy**: Commits made at correct points
- [ ] **Commit Messages**: Messages follow format
- [ ] **PR Creation**: PRs created correctly (if configured)
- [ ] **PR Content**: PR includes all required information
- [ ] **Fallback**: Works without GitHub MCP
- [ ] **Error Handling**: All errors handled gracefully
- [ ] **Multiple Evolutions**: No conflicts with multiple evolutions
- [ ] **Performance**: Meets performance targets

### 6.3 Combined System Verification

- [ ] **End-to-End**: Full workflow works end-to-end
- [ ] **Devlog from GitHub**: Devlog entries include GitHub context
- [ ] **No Data Loss**: All data preserved
- [ ] **No Corruption**: No data corruption
- [ ] **Documentation**: All documentation updated
- [ ] **Migration Guide**: Migration guide created
- [ ] **User Guide**: User guide updated

---

## Part 7: Test Execution Plan

### Phase 1: Unit Tests (Day 1)
1. Run all DevlogManager unit tests
2. Fix any failing tests
3. Achieve > 90% code coverage
4. Run all GitHub integration unit tests
5. Fix any failing tests

### Phase 2: Integration Tests (Day 1-2)
1. Run all integration tests
2. Test migration script
3. Test backward compatibility
4. Fix any issues

### Phase 3: End-to-End Testing (Day 2)
1. Execute manual test scenarios
2. Test full evolve workflow
3. Test GitHub integration
4. Test combined systems
5. Document any issues

### Phase 4: Performance Testing (Day 2)
1. Run performance tests
2. Optimize if needed
3. Verify performance targets met

### Phase 5: Edge Case Testing (Day 3)
1. Test all edge cases
2. Test error handling
3. Test concurrent operations
4. Fix any issues

### Phase 6: Final Verification (Day 3)
1. Run full test suite
2. Complete verification checklist
3. Update documentation
4. Create test report

---

## Part 8: Test Data & Fixtures

### 8.1 Test Devlog Data

**File**: `tests/fixtures/test_devlog.md`

- Sample devlog entries for testing
- Various entry formats
- Different dates and sources
- Edge cases (special characters, unicode, etc.)

### 8.2 Test GitHub Responses

**Files**: `tests/fixtures/github_responses/`

- Mock GitHub API responses
- Success responses
- Error responses
- Rate limit responses

### 8.3 Test Being Data

**Files**: `tests/fixtures/beings/`

- Sample Being data for testing
- Various Being states
- Genetic lineage examples

---

## Part 9: Test Reporting

### 9.1 Test Results Format

**File**: `tests/reports/test_results_YYYYMMDD.md`

```markdown
# Test Results: Devlog System & GitHub Integration

**Date**: YYYY-MM-DD
**Test Suite**: Full System Test

## Summary
- Total Tests: X
- Passed: Y
- Failed: Z
- Skipped: W
- Coverage: XX%

## Test Results by Category

### Devlog System
- Unit Tests: X/Y passed
- Integration Tests: X/Y passed
- Migration Tests: X/Y passed

### GitHub Integration
- Unit Tests: X/Y passed
- Integration Tests: X/Y passed
- End-to-End Tests: X/Y passed

## Issues Found
1. [Issue description]
2. [Issue description]

## Performance Results
- Entry Write: X ms/entry
- Entry Read: X ms/1000 entries
- Migration: X seconds
- Branch Creation: X seconds
- PR Creation: X seconds

## Recommendations
1. [Recommendation]
2. [Recommendation]
```

---

## Part 10: Rollback Plan

### 10.1 If Tests Fail

1. **Stop deployment**
2. **Review test failures**
3. **Fix issues**
4. **Re-run tests**
5. **Verify fixes**

### 10.2 If Migration Fails

1. **Restore from backup**
   ```bash
   cp _work_efforts/devlog.md.backup _work_efforts/devlog.md
   rm -rf _work_efforts/devlog/
   ```
2. **Review migration logs**
3. **Fix migration script**
4. **Re-run migration**

### 10.3 If GitHub Integration Fails

1. **Disable GitHub integration**
2. **Continue with local-only mode**
3. **Review GitHub MCP logs**
4. **Fix issues**
5. **Re-enable GitHub integration**

---

## Success Criteria

### Devlog System
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ Migration completes successfully
- ✅ Backward compatibility maintained
- ✅ Performance targets met
- ✅ All edge cases handled

### GitHub Integration
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ Feature branches created correctly
- ✅ PRs created correctly (if configured)
- ✅ Fallback works without GitHub
- ✅ Performance targets met

### Combined System
- ✅ End-to-end workflow works
- ✅ No data loss or corruption
- ✅ All documentation updated
- ✅ User guide complete

---

## Next Steps After Testing

1. **Review test results**
2. **Fix any issues found**
3. **Update documentation**
4. **Create migration guide**
5. **Update user guide**
6. **Deploy to production**
7. **Monitor for issues**

---

**End of Testing & Verification Plan**
