# WAFT Self-Study

**Self-monitoring and iterative study system using the proof methodology.**

Enables WAFT to monitor and study itself across multiple dimensions, track changes over time, and generate comprehensive evidence-based reports.

**Use when:** Need to verify system health, track changes over time, identify regressions, or generate comprehensive self-assessment reports.

---

## Purpose

This command provides:
- **Self-Monitoring**: WAFT studies its own state and health
- **Iterative Tracking**: Compares studies over time to identify trends
- **Evidence-Based**: Uses proof system methodology for rigorous verification
- **Multi-Dimensional**: Studies templates, code quality, system health, work efforts, and epistemic state
- **Comprehensive Reports**: Generates PDF case files with full evidence

---

## Quick Start

### Study All Areas
```
/waft-self-study
```

Runs comprehensive self-study across all areas and generates reports.

### Study Specific Area
```
/waft-self-study --area template_health
/waft-self-study --area code_quality
/waft-self-study --area system_health
/waft-self-study --area work_efforts
/waft-self-study --area epistemic_state
```

Studies a specific area in detail.

### View Study History
```
/waft-self-study --history 5
```

Shows the last 5 studies with health scores.

### Compare Studies
```
/waft-self-study --compare study_results_20260113_080000.json study_results_20260113_120000.json
```

Compares two study results to identify changes.

---

## Study Areas

### 1. Template Health
**Claim**: "All PDF templates are properly formatted and free of problematic styling"

**Checks**:
- Black bar detection in headers
- CSS styling verification
- Template file integrity
- Formatting consistency

**Output**: Case file with template-by-template evidence

### 2. Code Quality
**Claim**: "Source code follows project standards and best practices"

**Checks**:
- Import organization
- Error handling patterns
- Type hints usage
- Code structure

**Output**: Code analysis with file-level evidence

### 3. System Health
**Claim**: "WAFT system is healthy and operational"

**Checks**:
- Project structure (uv.lock, _pyrite)
- Git repository state
- Core system files
- Dependency integrity

**Output**: System verification report

### 4. Work Efforts
**Claim**: "Work efforts system is properly structured and maintained"

**Checks**:
- Directory structure
- Index file presence
- Organization compliance
- Johnny Decimal adherence

**Output**: Work efforts health report

### 5. Epistemic State
**Claim**: "Epistemic tracking is functioning correctly"

**Checks**:
- Empirica initialization
- Knowledge tracking
- Epistemic state integrity
- Integration status

**Output**: Epistemic system verification

---

## Workflow

### Phase 1: Study Execution
1. **Select Areas**: Choose specific area(s) or study all
2. **Run Verification**: Execute proof system verification checks
3. **Assumption Validation**: Test area-specific assumptions
4. **Evidence Collection**: Gather sources, line numbers, code snippets

### Phase 2: Analysis
1. **Verdict Determination**: PROVEN/DISPROVEN/INCONCLUSIVE
2. **Confidence Scoring**: 0.0-1.0 confidence level
3. **Health Calculation**: Overall system health score

### Phase 3: Documentation
1. **Case File Generation**: Markdown case brief with evidence
2. **PDF Binder Creation**: Professional PDF with verdict on cover
3. **Results Storage**: JSON results for history tracking

### Phase 4: Iteration
1. **History Tracking**: Compare studies over time
2. **Trend Analysis**: Identify improvements or regressions
3. **Change Detection**: Highlight what changed between studies

---

## Output Files

### Case Files
Location: `_work_efforts/self_studies/study_{area}_{timestamp}.md`

Format: Comprehensive case brief with:
- Abstract
- Hypothesis
- Methodology
- Verification Evidence
- Assumption Validation
- Analysis
- Conclusion & Summary
- Appendix

### PDF Binders
Location: `_work_efforts/self_studies/STUDY_{AREA}_{timestamp}.pdf`

Format: Professional PDF with:
- Cover page with verdict
- Full case file content
- Evidence with sources
- Confidence scores

### Results JSON
Location: `_work_efforts/self_studies/study_results_{timestamp}.json`

Format: Structured data for:
- History tracking
- Comparison analysis
- Trend detection

---

## Health Scoring

### Overall Health Score
Calculated from:
- Average confidence across all studies (60% weight)
- Ratio of proven studies (40% weight)

### Health Status Levels
- **Excellent**: ≥ 90
- **Good**: ≥ 75
- **Fair**: ≥ 50
- **Poor**: < 50

---

## Integration

### With Proof System
Uses `ProofCaseBuilder` for:
- Verification checks
- Assumption validation
- Evidence collection
- Case file generation

### With WAFT Status
Complements `/waft-status` by:
- Adding evidence-based verification
- Providing historical tracking
- Enabling trend analysis

### With Work Efforts
Studies work efforts system:
- Structure verification
- Index file checks
- Organization compliance

---

## Examples

### Daily Health Check
```
/waft-self-study --area system_health
```

Quick system health verification.

### Weekly Comprehensive Review
```
/waft-self-study --all
```

Full system study across all areas.

### Monthly Trend Analysis
```
/waft-self-study --history 30
/waft-self-study --compare study_results_20260101.json study_results_20260131.json
```

Track changes over time.

---

## Best Practices

1. **Regular Studies**: Run weekly comprehensive studies
2. **Before Major Changes**: Study relevant areas before refactoring
3. **After Changes**: Verify health after modifications
4. **Trend Monitoring**: Compare studies to catch regressions
5. **Documentation**: Review PDF binders for detailed evidence

---

## Troubleshooting

### Study Fails
- Check project path is correct
- Verify required files exist
- Review error messages in case files

### Low Confidence Scores
- Review evidence in case files
- Check assumption validation results
- Verify source files are accessible

### Missing History
- Ensure `_work_efforts/self_studies/` exists
- Check file permissions
- Verify JSON files are valid

---

## Related Commands

- `/waft-status`: Current system status check
- `/prove-it`: General proof system for any claim
- `/waft-boot`: System initialization

---

**Status**: Operational
**Version**: 1.0.0
**Last Updated**: 2026-01-13
