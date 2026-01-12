# Procedure: Data Analysis Workflow

**Shortcode**: ANL-001  
**Category**: Analysis  
**Created**: 2026-01-10  
**Updated**: 2026-01-10  
**Status**: Active  
**Aliases**: `/analyze-workflow`

---

## Description

Complete data analysis workflow that gathers comprehensive project data, analyzes patterns, identifies issues and opportunities, generates insights, and creates prioritized action plans.

---

## Use When

- Just completed Phase 1 data gathering
- Need to understand what data means
- Want to identify issues and opportunities
- Need to plan next steps
- Want actionable insights

---

## Prerequisites

- Phase 1 data exists (or will be generated)
- Project is a git repository
- Working directory is project root

---

## Steps

### Step 1: Data Gathering
**Execute**: `/phase1` (if data doesn't exist)

**Output**: Phase 1 JSON data and HTML dashboard

---

### Step 2: Data Analysis
**Execute**: `/analyze`

**Phases**:
1. Data Loading & Validation
2. Health Analysis
3. Issue Identification
4. Opportunity Discovery
5. Pattern Analysis
6. Insight Generation
7. Action Planning
8. Report Generation

**Output**: Comprehensive analysis report

---

### Step 3: Review Analysis
**Actions**:
1. Review analysis report
2. Identify key insights
3. Prioritize action items
4. Plan next steps

**Output**: Understanding of analysis results

---

## Expected Output

After completion:
- ✅ Phase 1 data gathered (if needed)
- ✅ Comprehensive analysis report
- ✅ Issues and opportunities identified
- ✅ Prioritized action plan
- ✅ Insights and recommendations

---

## Notes

- `/analyze` automatically runs `/phase1` if data doesn't exist
- Analysis report saved to `_pyrite/analyze/`
- Review report before taking action
- Use insights to inform decisions

---

## Related Procedures

- **ORC-001**: Comprehensive Orchestration (includes analysis)
- **ENG-001**: Full Engineering Workflow (includes analysis)

---

**Procedure Created**: 2026-01-10  
**Last Updated**: 2026-01-10
