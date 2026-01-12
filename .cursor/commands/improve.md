# Improve

**Analyze work and suggest improvements with prioritized recommendations.**

---

## Purpose

This command analyzes code, documentation, architecture, testing, performance, and usability to identify improvement opportunities. It provides:

- **Prioritized Recommendations**: Improvements ranked by impact and effort
- **Categorized Analysis**: Code, documentation, architecture, testing, performance, usability
- **Actionable Suggestions**: Specific changes with rationale
- **Score-Based Ranking**: Calculated priority scores for each improvement

---

## Usage

```bash
waft improve [OPTIONS]
```

**Options:**
- `--path, -p`: Project path (default: current directory)
- `--focus, -f`: Focus area (file path, work effort ID, or "all")
- `--category, -c`: Filter by category (code, documentation, architecture, testing, performance, usability)
- `--recent, -r`: Only analyze recent changes
- `--output, -o`: Save improvement report to file

---

## Examples

```bash
# Analyze all work
waft improve

# Focus on specific file
waft improve --focus src/waft/main.py

# Focus on work effort
waft improve --focus WE-260112-z87p

# Filter by category
waft improve --category code

# Analyze only recent changes
waft improve --recent

# Save report
waft improve --output improvements.md
```

---

## What Gets Analyzed

### 1. Code Quality
- Import issues
- Error handling
- Code duplication
- Best practices
- Patterns and conventions

### 2. Documentation
- Completeness
- Examples
- Clarity
- Accuracy
- Structure

### 3. Architecture
- Design patterns
- Code organization
- Dependencies
- Separation of concerns
- Scalability

### 4. Testing
- Test coverage
- Test quality
- Missing tests
- Test organization

### 5. Performance
- Optimization opportunities
- Resource usage
- Efficiency
- Bottlenecks

### 6. Usability
- User experience
- Error messages
- Command interfaces
- Feedback
- Discoverability

---

## Output Format

### Summary Table
- Improvement counts by priority (critical, high, medium, low)
- Total improvements identified

### Detailed Improvements
Each improvement includes:
- **Title**: Clear improvement description
- **Priority**: critical | high | medium | low
- **Category**: code | documentation | architecture | testing | performance | usability
- **Impact**: high | medium | low
- **Effort**: high | medium | low
- **Score**: Calculated priority score (higher = more important)
- **Location**: Where the improvement applies
- **Current State**: What exists now
- **Suggested Change**: What to change
- **Rationale**: Why this improvement matters

### Priority Scoring

Improvements are scored using:
```
Score = (Impact × Priority) / Effort
```

Higher scores indicate improvements that should be done first.

---

## Integration

This command complements:
- **`/critique`**: Adversarial security review (improve is constructive analysis)
- **`/check-assumptions`**: Assumption validation (improve is general quality)
- **`/audit`**: Conversation quality (improve is code/architecture quality)
- **`/verify`**: Technical verification (improve is enhancement suggestions)

---

## When to Use

**Use `/improve` when**:
- ✅ Want to identify improvement opportunities
- ✅ Need prioritized recommendations
- ✅ Want to improve code quality
- ✅ Need suggestions for better architecture
- ✅ Want to enhance documentation
- ✅ Need testing recommendations
- ✅ Want performance optimizations
- ✅ Need usability improvements

**Don't use `/improve` when**:
- ❌ Need security review (use `/critique`)
- ❌ Need assumption validation (use `/check-assumptions`)
- ❌ Need conversation quality analysis (use `/audit`)

---

## Output Location

- **Console**: Formatted display with Rich tables and panels
- **File** (if `--output` specified): Markdown report with all improvements

---

**This command helps identify and prioritize improvements to make your work better.**
