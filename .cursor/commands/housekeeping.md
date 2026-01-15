# /housekeeping

**Summon ThePantheon and Housekeeping Gods to tidy up the repository.**

Coordinates Higher Beings (Magistrate, Judge) and Housekeeping staff to organize, refactor, and maintain clean architecture. Proactive organization and "making the bed" - setting everything right.

**Use when:** Project is getting disorganized, need systematic tidying, want proactive organization.

---

## Purpose

This command summons:

### ThePantheon (Higher Beings)
- **Magistrate**: Organizes case files and builds Body of Proof
- **Judge**: Evaluates organization quality and renders judgments

### Housekeeping Gods (Hotel Staff)
- **Housekeeping**: Organizes file structure, refactors code, maintains clean architecture
- **Janitor**: Cleans up temporary files and error artifacts (reactive cleanup)

Together they provide:
- **Proactive Organization**: Not just cleanup, but proper structure
- **Code Refactoring**: Tidies code organization
- **File Structure**: Organizes directories and creates indexes
- **Quality Evaluation**: Judge evaluates organization quality
- **Precedent Building**: Magistrate organizes cases for future reference

---

## Philosophy

**"As Above, So Below"**

ThePantheon provides celestial oversight while Housekeeping performs earthly tidying:
1. **Magistrate organizes** - Builds Body of Proof from case files
2. **Judge evaluates** - Renders judgment on organization quality
3. **Housekeeping tidies** - Organizes files, refactors code, "makes the bed"
4. **Janitor cleans** - Removes temporary files and error artifacts

**Everything in its place, and a place for everything.**

---

## Execution Steps

### Housekeeping 1.1: Summon ThePantheon
**Purpose**: Initialize Higher Beings for oversight

**Steps**:
1. Initialize Magistrate from `waft.pantheon`
2. Initialize Judge (requires Magistrate)
3. Load existing Body of Proof
4. Load judgment history
5. Verify Pantheon is ready

**Output**: Pantheon initialized and ready

---

### Housekeeping 1.2: Summon Housekeeping Staff
**Purpose**: Initialize Housekeeping and Janitor Beings

**Steps**:
1. Load or spawn Housekeeping Being (Martha)
2. Load or spawn Janitor Being (Carl)
3. Verify staff skills and readiness
4. Check shift schedules (Housekeeping: Morning, Janitor: Night)

**Output**: Housekeeping staff ready

---

### Housekeeping 1.3: Assess Current State
**Purpose**: Evaluate what needs tidying

**Steps**:
1. Magistrate organizes all case files from `_work_efforts/proof_cases/`
2. Housekeeping scans directory structure
3. Identify missing indexes
4. Find disorganized files
5. Check code organization issues
6. Judge evaluates current organization state

**Output**: Assessment report

---

### Housekeeping 1.4: Organize File Structure
**Purpose**: Create proper directory organization

**Steps**:
1. Housekeeping organizes `_work_efforts/` directories
2. Create missing `00.00_index.md` files
3. Organize files by type/category
4. Ensure Johnny Decimal structure
5. Update indexes

**Output**: Organized file structure

---

### Housekeeping 1.5: Tidy Code Organization
**Purpose**: Refactor code structure issues

**Steps**:
1. Housekeeping scans Python files
2. Check import organization
3. Check function organization
4. Check class organization
5. Report organization issues (doesn't auto-fix, reports)

**Output**: Code organization report

---

### Housekeeping 1.6: Clean Temporary Files
**Purpose**: Remove temporary files and artifacts

**Steps**:
1. Janitor cleans temporary files (`.tmp`, `.bak`, `__pycache__`, etc.)
2. Janitor removes error artifacts
3. Janitor fixes broken symlinks
4. Janitor cleans empty directories
5. Report what was cleaned

**Output**: Cleanup report

---

### Housekeeping 1.7: Judge Evaluation
**Purpose**: Judge renders judgment on organization quality

**Steps**:
1. Judge evaluates organization claim
2. Judge references Body of Proof (from Magistrate)
3. Judge renders verdict (PROVEN/PROBABLE/UNPROVEN)
4. Judge provides reasoning
5. Judge saves judgment to Pantheon

**Output**: Judgment report

---

### Housekeeping 1.8: Final Report
**Purpose**: Summary of housekeeping work

**Steps**:
1. Compile all actions taken
2. Show organization improvements
3. Display Judge's verdict
4. List files organized
5. Show cleanup statistics
6. Provide next steps

**Output**: Complete housekeeping report

---

## Usage Examples

### 1. Full Housekeeping
**Scenario**: Project needs comprehensive tidying

**Example**:
```
/housekeeping
```

**Output**: Complete housekeeping with Pantheon oversight

---

### 2. Organize Work Efforts Only
**Scenario**: Just need to organize `_work_efforts/`

**Example**:
```
/housekeeping --work-efforts
```

**Output**: Work efforts organized with indexes

---

### 3. Code Organization Only
**Scenario**: Just need code structure analysis

**Example**:
```
/housekeeping --code-only
```

**Output**: Code organization report

---

### 4. Cleanup Only
**Scenario**: Just need temporary file cleanup

**Example**:
```
/housekeeping --cleanup-only
```

**Output**: Temporary files cleaned

---

### 5. Assessment Only
**Scenario**: Just want to see what needs tidying

**Example**:
```
/housekeeping --assess
```

**Output**: Assessment report without changes

---

## Integration with Other Commands

- **`/cleanup`**: Reactive cleanup (`/housekeeping` is proactive organization)
- **`/status`**: Shows status (`/housekeeping` performs organization)
- **`/the-archivist`**: Archives PDFs (`/housekeeping` organizes structure)
- **`/prove-it`**: Creates proof cases (`/housekeeping` organizes them via Magistrate)

---

## When to Use

**Use `/housekeeping` when**:
- ✅ Project is getting disorganized
- ✅ Need systematic tidying
- ✅ Want proactive organization (not just cleanup)
- ✅ Need code structure analysis
- ✅ Want Pantheon oversight
- ✅ Need to "make the bed" - set things right

**Don't use `/housekeeping` when**:
- ❌ Just need quick cleanup (use `/cleanup` or Janitor)
- ❌ Unsure about changes (use `--assess` first)
- ❌ Recent work might be affected (be careful)

---

## Technical Details

### Pantheon Integration

**Magistrate**:
- Organizes case files from `_work_efforts/proof_cases/`
- Builds Body of Proof in `_pantheon/magistrate/`
- Creates precedents for future reference

**Judge**:
- Evaluates organization claims
- References Body of Proof
- Saves judgments to `_pantheon/judge/`

### Housekeeping Staff

**Housekeeping (Martha)**:
- Skills: organization (25.0), refactoring (20.0), code_structure (22.0), tidying (28.0)
- Shift: Morning (6 AM - 2 PM)
- Personality: Meticulous, methodical, perfectionist
- Responsibilities: Organize structure, refactor code, maintain architecture

**Janitor (Carl)**:
- Skills: cleanup (30.0), error_handling (25.0), reactive_fixes (28.0), temporary_cleanup (32.0)
- Shift: Night (10 PM - 6 AM) - on call
- Personality: Quick, reactive, problem-solver
- Responsibilities: Clean temp files, remove error artifacts, fix broken states

### Tools Used

**Pantheon**:
- `waft.pantheon.Magistrate` - Organizes cases
- `waft.pantheon.Judge` - Evaluates quality

**Hotel Staff**:
- `hotel_staff.roles.housekeeping.Housekeeping` - Organizes and tidies
- `hotel_staff.roles.janitor.Janitor` - Cleans up messes

**File System**:
- Directory organization
- Index file creation
- Code analysis
- Temporary file cleanup

### Performance

- **Target Time**: < 30 seconds
- **Pantheon Init**: ~2 seconds
- **Staff Init**: ~2 seconds
- **Assessment**: ~5 seconds
- **Organization**: ~10 seconds
- **Code Analysis**: ~5 seconds
- **Cleanup**: ~3 seconds
- **Judgment**: ~2 seconds
- **Reporting**: ~1 second

### Error Handling

- **Pantheon Errors**: Graceful degradation, continue with staff only
- **Staff Errors**: Skip problematic operations, continue
- **File Errors**: Report but don't fail
- **Always Complete**: Always provide report even if some steps fail

---

## Example Workflow

```
User: "/housekeeping"

AI: 🏛️ Housekeeping: Summoning ThePantheon and Housekeeping Gods

Summoning ThePantheon...
  ✅ Magistrate initialized
  ✅ Judge initialized
  ✅ Body of Proof loaded (2 precedents)
  ✅ Judgment history loaded (3 judgments)

Summoning Housekeeping Staff...
  ✅ Housekeeping (Martha) ready
  ✅ Janitor (Carl) ready

Assessing Current State...
  📊 Found 15 work effort directories
  📊 Missing indexes: 3 directories
  📊 Disorganized files: 8 files
  📊 Code issues: 2 files

Organizing File Structure...
  ✅ Created 3 index files
  ✅ Organized 8 files
  ✅ Updated directory structure

Tidying Code Organization...
  ⚠️ 2 files need import organization
  ⚠️ 1 file needs function organization
  📋 Code organization report generated

Cleaning Temporary Files...
  ✅ Cleaned 12 temporary files
  ✅ Removed 3 error artifacts
  ✅ Fixed 1 broken symlink

Judge Evaluation...
  ⚚️ Judge evaluating: "Repository is well-organized"
  ⚚️ Verdict: PROBABLE (confidence: 0.75)
  ⚚️ Reasoning: Good structure, minor improvements needed

Final Report:
  ✅ 3 indexes created
  ✅ 8 files organized
  ✅ 12 temp files cleaned
  ✅ Judge verdict: PROBABLE
  📋 Next: Review code organization issues

🏛️ Housekeeping complete. Everything in its place.
```

---

## Philosophy Notes

**"As Above, So Below"**

ThePantheon provides the celestial framework:
- **Magistrate** organizes precedent (law)
- **Judge** renders judgment (justice)

Housekeeping performs earthly work:
- **Housekeeping** organizes structure (order)
- **Janitor** cleans messes (purity)

Together they create harmony between the spiritual (Pantheon) and material (Staff) realms.

**"Everything in its place, and a place for everything."**

This is Housekeeping's catchphrase - the goal of perfect organization where every file, every function, every concept has its proper place in the cosmic order.

---

## Related Commands

- **`/cleanup`**: Reactive cleanup (Janitor's job)
- **`/the-archivist`**: PDF archiving
- **`/prove-it`**: Create proof cases (Magistrate organizes them)
- **`/status`**: Check current state
- **`/sync`**: Sync documentation

---

**Welcome to ThePantheon Housekeeping - where celestial order meets earthly tidying!** 🏛️✨
