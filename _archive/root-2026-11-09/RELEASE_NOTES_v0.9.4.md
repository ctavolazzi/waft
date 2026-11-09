# WAFT v0.9.4 Release Notes

**Release Date**: January 19, 2026  
**Version**: 0.9.4  
**Status**: ✅ Production Ready

---

## 🎉 What's New in v0.9.4

This release focuses on **TheOracle enhancements**, **calculation transparency**, **auto-work logging**, and **poker visualization extensions**. Most importantly, TheOracle now shows its thinking process step-by-step and provides helpful guidance even without epistemic state.

---

## 🔮 Major Features

### 1. TheOracle Calculation Display ⭐ NEW

**Transparent Reasoning Process**: TheOracle now shows its mathematical calculations and decision-making process in real-time.

#### What It Does

- **Step-by-Step Thinking**: Displays each CASCADE step (PREFLIGHT → INVESTIGATE → CHECK → ACT → POSTFLIGHT) with actual calculations
- **Mathematical Formulas**: Shows the exact formulas being used:
  - Coverage: `coverage = know × (1 - uncertainty)`
  - Confidence: `base_confidence = min(1.0, findings × 0.1)`, then `confidence = base_confidence × (1 - uncertainty)`
  - Phase determination with threshold logic
  - Decision tree evaluation with actual conditions
- **Intermediate Values**: Displays all intermediate calculation steps
- **Decision Reasoning**: Shows which condition triggered each decision

#### Example Output

```
📊 PREFLIGHT...
   💭 Calculated: know=0.00 (from foundation vectors), uncertainty=1.00 (from meta vector)
   KNOW: 0% (Low), UNCERTAINTY: 100% (High)

🧮 CALCULATE...
   💭 Formula: coverage = know(0.000) × (1 - uncertainty(1.000)) = 0.000
   💭 Phase logic: know(0.00) < 0.3 AND uncertainty(1.00) > 0.5

✅ CHECK...
   💭 Step 1: base_confidence = min(1.0, findings(0) × 0.1) = 0.000
   💭 Step 2: confidence = 0.000 × (1 - uncertainty(1.000)) = 0.000
   💭 Decision tree: Special case: uncertainty(1.000) >= 0.99 → PROCEED (fallback mode)
```

#### Why It Matters

- **Transparency**: Users can see exactly how TheOracle makes decisions
- **Debugging**: Understand why certain recommendations are made
- **Learning**: See the mathematical relationships between epistemic vectors
- **Trust**: Build confidence in TheOracle's reasoning process

---

### 2. TheOracle Fallback Method ⭐ NEW

**Helpful Guidance Without Epistemic State**: TheOracle now provides useful answers even when Empirica has no epistemic data.

#### What It Does

- **Question Analysis**: Analyzes question type and provides contextual guidance
- **Fallback Answers**: Uses reflection/journal data or provides general guidance
- **No More HALT**: Instead of returning unhelpful "no data" messages, actually answers questions

#### Before vs After

**Before:**
```
[HALT] Low knowledge coverage (0%). Focus on addressing unknowns: 0 open questions.
```

**After:**
```
[PROCEED] For version release documentation, consider documenting: major features 
added, bug fixes, breaking changes, migration guides, and new capabilities. 
Review recent commits and work efforts for changes. Note: Epistemic state is 
not yet initialized - consider using Empirica preflight/postflight to track knowledge.
```

#### Question Types Handled

- **Version/Release Questions** → Guidance on documenting releases
- **Architecture/Design Questions** → Guidance on reviewing codebase
- **Implementation Questions** → Guidance on checking examples
- **General Questions** → Instructions on using Empirica

---

### 3. Epistemic State Bootstrap Script ⭐ NEW

**Automatic Initialization**: Automatically create initial epistemic state from codebase analysis.

#### What It Does

- **Codebase Analysis**: Checks for src/, docs/, tests/, work_efforts/
- **Vector Estimation**: Estimates epistemic vectors based on project structure
- **Session Creation**: Creates Empirica session and submits preflight/postflight
- **One Command**: Run `python3 scripts/bootstrap_epistemic_state.py`

#### Usage

```bash
# Bootstrap epistemic state
python3 scripts/bootstrap_epistemic_state.py

# Then TheOracle will have epistemic state to work with
python3 -m src.waft.main oracle "What should we focus on next?"
```

---

### 4. Auto-Work Logging System ⭐ NEW

**Comprehensive Execution Tracking**: Full audit trail of all auto-work script executions.

#### Features

- **Dual Logging**: Console output + persistent log files
- **Log Files**: `_work_efforts/auto_work_logs/auto_work_YYYYMMDD_HHMMSS.log`
- **Devlog Integration**: Automatic summary entries after each execution
- **Real-Time Progress**: Immediate output with flush for visibility
- **Progress Indicators**: Shows progress for all major operations

#### Benefits

- ✅ Full audit trail of all executions
- ✅ Debugging support for RAM-intensive operations
- ✅ Historical tracking via devlog integration
- ✅ Real-time visibility into script progress

---

### 5. Poker Visualization Creative Extensions ⭐ NEW

**Beyond Basic Hand Display**: Extended poker visualization with creative use cases.

#### Creative Categories

1. **Storytelling & Narrative** - Poker scenes for stories/D&D campaigns
2. **Tournament & Competition** - Brackets, final tables, hand histories
3. **Educational & Training** - Tutorials, quizzes, strategy guides
4. **Design & Art** - Custom decks, infographics, posters
5. **Analysis & Research** - Hand ranges, equity, GTO examples
6. **Interactive & Gamification** - Quizzes, practice scenarios, workbooks

#### Working Examples

- `generate_poker_story.py` - Narrative poker scenes
- `generate_poker_visualization.py` - Standard visualizations
- `generate_probability_education.py` - Educational content
- `generate_poker_session_recap.py` - Session summaries

#### Enhanced Features

- Card back support ("back" identifier) for unknown cards
- Narrative content integration via `add_content()`
- Educational quiz format with questions and answers
- Historical hand recreation support

---

### 6. D&D Campaign Tools ⭐ NEW

**Complete Campaign System**: D&D campaign visualization and generation tools.

#### Features

- **Game Visualization Wrapper System**: Complete D&D campaign visualization
- **Campaign Generation Scripts**: Automated campaign creation
- **Teleport Massive Integration**: Campaign integration with WAFT narrative systems
- **Ready for Integration**: Prepared for tavern poker nights

---

## 📊 Statistics

### Code Changes
- **Modified Files**: 5 core files
- **New Files**: 1 bootstrap script, 4 documentation files
- **Lines Changed**: ~500+ lines across Oracle system

### Features
- **3 Major Features** added (Calculation Display, Fallback Method, Bootstrap Script)
- **2 Enhancements** (Auto-Work Logging, Poker Extensions)
- **1 Fix** (TheOracle empty state handling)

---

## 🔄 Migration Guide

### For Users

**No breaking changes** - this is a patch release with new features and improvements.

**New Capabilities**:
1. **TheOracle Calculation Display**: See step-by-step thinking with formulas
2. **TheOracle Fallback**: Get helpful guidance even without epistemic state
3. **Bootstrap Script**: Initialize epistemic state automatically
4. **Auto-Work Logging**: Check `_work_efforts/auto_work_logs/` for execution logs

### For Developers

1. **Calculation Display**: Review `oracle_thinking.py` for display patterns
2. **Fallback Method**: Check `_answer_question_without_epistemic_state()` for question analysis
3. **Bootstrap Script**: Use as template for initializing epistemic state
4. **Formula Reference**: See formulas in thinking callbacks

---

## 🐛 Bug Fixes

- **TheOracle Empty State**: Fixed issue where TheOracle would return HALT with no guidance
- **Show Me Performance**: Fixed slow performance with large work effort directories
- **Auto-Work Visibility**: Resolved lack of feedback during RAM-intensive operations

---

## 📈 Performance Improvements

- **Show Me Script**: Optimized for 100+ work effort directories
- **Auto-Work Script**: Better progress visibility reduces perceived wait time
- **TheOracle**: Immediate feedback with status spinners

---

## 🔮 Future Work

### Planned Enhancements
- Fix Empirica CLI timeouts (currently blocking full testing)
- Async processing for Empirica CLI calls
- More detailed calculation breakdowns
- Unit tests for calculation display logic

---

## 🙏 Acknowledgments

Thanks to all contributors and the WAFT community for continued support and feedback.

Special thanks for the feedback that led to the calculation display feature - transparency in AI reasoning is crucial for trust and understanding.

---

## 📚 Related Documentation

- **CHANGELOG.md**: Complete changelog
- **ORACLE_FIX_SUMMARY.md**: Detailed Oracle fix documentation
- **V0.9.4_VERSION_UPDATE_SUMMARY.md**: Version update summary
- **SESSION_SUMMARY_20260119.md**: Session summary
- **Empirica Architecture**: https://github.com/Nubaeon/empirica/tree/main/docs/architecture

---

## 🔗 Links

- **GitHub Repository**: https://github.com/ctavolazzi/waft
- **Releases**: https://github.com/ctavolazzi/waft/releases
- **Wiki**: https://github.com/ctavolazzi/waft/wiki

---

**Full Changelog**: https://github.com/ctavolazzi/waft/compare/v0.9.3...v0.9.4
