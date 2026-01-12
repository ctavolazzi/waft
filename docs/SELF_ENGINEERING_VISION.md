# Self-Engineering Vision: The Meta-Game

**Date**: 2026-01-12  
**Status**: Vision Document  
**Purpose**: Define the architecture for an AI D&D engine that evolves in response to feedback, detects problems, engineers solutions, and iterates on itself.

---

## The Vision

> "An AI D&D engine that evolves in response to feedback and stimulus in its environment. The system tries to play itself, detects when it can't, engineers solutions to make itself playable, and iterates on itself. **That's the game** - the meta-game of self-engineering."

---

## Current State

### ✅ What Works

1. **Self-Playing**: `tavern_scenario_evolved.py` - Being makes decisions automatically
2. **Decision-Making**: Being system with skills, personality, memory
3. **Learning**: Beings learn from experiences, improve skills, store memories
4. **Evolution**: Beings can evolve, improve fitness, pass traits to children
5. **D&D 5e Engine**: Complete physics engine (stats, combat, dice, modifiers)

### ❌ What's Missing

1. **Problem Detection**: System can't detect when it fails or gets stuck
2. **Diagnosis**: System can't understand WHY it can't play
3. **Solution Engineering**: System can't propose or implement fixes
4. **Self-Modification**: System can't safely modify its own code
5. **Iteration Loop**: System can't automatically iterate on improvements

---

## Architecture: The Self-Engineering Layer

### 1. Problem Detection System

**Purpose**: Monitor system execution and detect problems.

**What to Monitor**:
- **Execution Failures**: Exceptions, errors, crashes
- **Performance Issues**: Slow decisions, stuck states, timeouts
- **Decision Quality**: Bad choices, low fitness scores, repeated failures
- **Missing Capabilities**: Can't handle interactive input, can't make certain decisions
- **State Anomalies**: Invalid states, desync, corruption

**Implementation**:
```python
class ProblemDetector:
    """Detects problems in system execution."""
    
    def monitor_execution(self, execution_result: Dict) -> List[Problem]:
        """Monitor execution and detect problems."""
        problems = []
        
        # Check for exceptions
        if execution_result.get("exception"):
            problems.append(Problem(
                type="EXECUTION_FAILURE",
                severity="HIGH",
                description=execution_result["exception"],
                context=execution_result["context"]
            ))
        
        # Check for performance issues
        if execution_result.get("duration") > TIMEOUT_THRESHOLD:
            problems.append(Problem(
                type="PERFORMANCE_ISSUE",
                severity="MEDIUM",
                description="Execution exceeded timeout",
                context=execution_result["context"]
            ))
        
        # Check for decision quality
        if execution_result.get("fitness_gained", 0) < MIN_FITNESS:
            problems.append(Problem(
                type="DECISION_QUALITY",
                severity="LOW",
                description="Low fitness gain from decisions",
                context=execution_result["context"]
            ))
        
        return problems
```

### 2. Diagnosis System

**Purpose**: Understand WHY problems occur.

**Diagnosis Methods**:
- **Pattern Matching**: Recognize common failure patterns
- **Statistical Analysis**: Identify correlations between failures and system state
- **LLM Reasoning**: Use language model to analyze problems and suggest causes
- **Dependency Analysis**: Trace failures to root causes (missing features, bad logic, etc.)

**Implementation**:
```python
class ProblemDiagnostician:
    """Diagnoses root causes of problems."""
    
    def diagnose(self, problem: Problem, system_state: Dict) -> Diagnosis:
        """Diagnose root cause of problem."""
        
        # Pattern matching
        if problem.type == "EXECUTION_FAILURE":
            if "EOFError" in problem.description:
                return Diagnosis(
                    cause="INTERACTIVE_INPUT_REQUIRED",
                    confidence=0.9,
                    explanation="System requires interactive input but running in non-interactive mode",
                    solution_hint="Add non-interactive mode or input simulation"
                )
        
        # Statistical analysis
        if problem.type == "DECISION_QUALITY":
            # Analyze decision patterns
            if system_state["decision_history"][-5:].all_failures():
                return Diagnosis(
                    cause="POOR_DECISION_LOGIC",
                    confidence=0.7,
                    explanation="Decision logic consistently produces poor outcomes",
                    solution_hint="Improve decision weights or add new decision factors"
                )
        
        # LLM reasoning (for complex cases)
        if problem.type == "UNKNOWN":
            return self._llm_diagnose(problem, system_state)
        
        return Diagnosis(cause="UNKNOWN", confidence=0.0)
```

### 3. Solution Engineering System

**Purpose**: Propose and implement fixes.

**Solution Types**:
- **Code Modifications**: Add features, fix bugs, improve logic
- **Configuration Changes**: Adjust parameters, weights, thresholds
- **Architecture Changes**: Restructure code, add modules, refactor
- **New Capabilities**: Add new skills, decision types, features

**Implementation**:
```python
class SolutionEngineer:
    """Engineers solutions to problems."""
    
    def propose_solution(self, diagnosis: Diagnosis) -> Solution:
        """Propose solution based on diagnosis."""
        
        if diagnosis.cause == "INTERACTIVE_INPUT_REQUIRED":
            return Solution(
                type="CODE_MODIFICATION",
                description="Add non-interactive mode to scenario",
                implementation="Modify tavern_scenario.py to accept input stream or default choices",
                risk="LOW",
                estimated_effort=2
            )
        
        if diagnosis.cause == "POOR_DECISION_LOGIC":
            return Solution(
                type="CODE_MODIFICATION",
                description="Improve decision weights in being_make_choice",
                implementation="Adjust skill weights, add memory-based learning, improve personality influence",
                risk="MEDIUM",
                estimated_effort=5
            )
        
        return Solution(type="UNKNOWN")
    
    def implement_solution(self, solution: Solution) -> ImplementationResult:
        """Implement solution with safety checks."""
        # 1. Validate solution
        if not self._validate_solution(solution):
            return ImplementationResult(success=False, error="Solution validation failed")
        
        # 2. Create backup
        backup = self._create_backup()
        
        # 3. Apply modification
        try:
            result = self._apply_modification(solution)
            
            # 4. Test modification
            if not self._test_modification(result):
                # Rollback on test failure
                self._rollback(backup)
                return ImplementationResult(success=False, error="Test failed, rolled back")
            
            return ImplementationResult(success=True, result=result)
        except Exception as e:
            # Rollback on error
            self._rollback(backup)
            return ImplementationResult(success=False, error=str(e))
```

### 4. Self-Modification Engine

**Purpose**: Safely modify system code.

**Safety Constraints**:
- **Validation**: Syntax checks, type checks, test execution
- **Rollback**: Revert bad changes automatically
- **Approval Workflow**: Require approval for risky changes
- **Version Control**: Track all modifications in git

**Implementation**:
```python
class SelfModificationEngine:
    """Safely modifies system code."""
    
    def modify_code(self, file_path: str, modification: CodeModification) -> ModificationResult:
        """Modify code with safety checks."""
        
        # 1. Validate modification
        if not self._validate_modification(modification):
            return ModificationResult(success=False, error="Modification validation failed")
        
        # 2. Check safety constraints
        if modification.risk_level == "HIGH":
            if not self._requires_approval(modification):
                return ModificationResult(success=False, error="High-risk modification requires approval")
        
        # 3. Create backup
        backup = self._create_backup(file_path)
        
        # 4. Apply modification
        try:
            self._apply_code_change(file_path, modification)
            
            # 5. Validate syntax
            if not self._validate_syntax(file_path):
                self._rollback(file_path, backup)
                return ModificationResult(success=False, error="Syntax validation failed")
            
            # 6. Run tests
            if not self._run_tests(file_path):
                self._rollback(file_path, backup)
                return ModificationResult(success=False, error="Tests failed")
            
            # 7. Commit to git
            self._commit_change(file_path, modification.description)
            
            return ModificationResult(success=True, backup=backup)
        except Exception as e:
            self._rollback(file_path, backup)
            return ModificationResult(success=False, error=str(e))
```

### 5. Iteration Loop

**Purpose**: Automatically iterate on improvements.

**Loop Structure**:
1. **Try to Play**: Run scenario, collect execution data
2. **Detect Problems**: Monitor execution, identify failures
3. **Diagnose Causes**: Understand why problems occurred
4. **Engineer Solutions**: Propose and implement fixes
5. **Test Fixes**: Verify improvements work
6. **Iterate**: Repeat with improved system

**Implementation**:
```python
class SelfEngineeringLoop:
    """Main iteration loop for self-engineering."""
    
    def run_iteration(self, max_iterations: int = 10) -> IterationResult:
        """Run self-engineering iteration loop."""
        
        iteration = 0
        improvements = []
        
        while iteration < max_iterations:
            # 1. Try to play
            execution_result = self._run_scenario()
            
            # 2. Detect problems
            problems = self.problem_detector.monitor_execution(execution_result)
            
            if not problems:
                # No problems - system is working!
                return IterationResult(
                    success=True,
                    iterations=iteration,
                    improvements=improvements,
                    message="System is functioning correctly"
                )
            
            # 3. Diagnose causes
            diagnoses = []
            for problem in problems:
                diagnosis = self.diagnostician.diagnose(problem, execution_result)
                diagnoses.append(diagnosis)
            
            # 4. Engineer solutions
            solutions = []
            for diagnosis in diagnoses:
                solution = self.engineer.propose_solution(diagnosis)
                solutions.append(solution)
            
            # 5. Implement solutions (one at a time, with testing)
            for solution in solutions:
                result = self.engineer.implement_solution(solution)
                if result.success:
                    improvements.append(Improvement(
                        iteration=iteration,
                        solution=solution,
                        result=result
                    ))
            
            iteration += 1
        
        return IterationResult(
            success=False,
            iterations=iteration,
            improvements=improvements,
            message=f"Reached max iterations ({max_iterations})"
        )
```

---

## Integration Points

### With Existing Systems

1. **Being System**: Use Being's decision-making and learning
2. **D&D 5e Engine**: Monitor gameplay execution and outcomes
3. **Empirica**: Track epistemic state and learning
4. **Self-Modification Infrastructure**: Use planned self-modification engine
5. **Git**: Track all modifications and rollbacks

### Safety Considerations

1. **Sandboxed Execution**: Run modifications in isolated environment
2. **Automatic Rollback**: Revert bad changes immediately
3. **Approval Gates**: Require approval for high-risk changes
4. **Test Coverage**: Run full test suite before accepting changes
5. **Version Control**: All changes tracked in git

---

## Example: Self-Engineering in Action

### Scenario: System Can't Play (Interactive Input Required)

1. **Problem Detection**: 
   - Execution fails with `EOFError: EOF when reading a line`
   - Problem type: `EXECUTION_FAILURE`
   - Severity: `HIGH`

2. **Diagnosis**:
   - Cause: `INTERACTIVE_INPUT_REQUIRED`
   - Explanation: "System requires interactive input but running in non-interactive mode"
   - Confidence: 0.9

3. **Solution Engineering**:
   - Type: `CODE_MODIFICATION`
   - Description: "Add non-interactive mode to scenario"
   - Implementation: "Modify tavern_scenario.py to accept input stream or default choices"
   - Risk: `LOW`

4. **Implementation**:
   - Modify `tavern_scenario.py` to accept optional input stream
   - Add default choice logic when input not available
   - Test with non-interactive execution
   - Commit change to git

5. **Iteration**:
   - Run scenario again in non-interactive mode
   - Verify it works
   - System can now play itself!

---

## 6. Notebook System (✅ Implemented)

**Purpose**: Journal findings, reflect on problems, and convert insights into actionable work.

**What It Does**:
- **Journals Problems**: Records all detected problems with context
- **Journals Diagnoses**: Records root cause analysis
- **Reflects on Findings**: Analyzes patterns, generates insights, suggests actionables
- **Creates Actionables**: Converts findings into work efforts, scenarios, quests

**Implementation**:
```python
from waft.core.self_engineering import NotebookManager, ActionableCreator

# Initialize notebook
notebook = NotebookManager(project_path / "_notebook")

# Journal a problem
entry = notebook.journal_problem(problem, context={"execution_id": "exec_123"})

# Journal a diagnosis
diagnosis_entry = notebook.journal_diagnosis(problem, diagnosis)

# Reflect on findings
reflection = notebook.journal_reflection(
    entries=[entry, diagnosis_entry],
    insights=["System needs non-interactive mode"],
    patterns=["EOFError occurs in all non-interactive runs"],
    questions=["How to handle interactive input in automated scenarios?"]
)

# Create actionable items
creator = ActionableCreator(
    project_path=project_path,
    work_efforts_dir=project_path / "_work_efforts",
    scenarios_dir=project_path / "examples",
    quests_dir=project_path / "src/gym/rpg/dungeons"
)

# Create work effort from entry
work_effort = creator.create_work_effort_from_entry(entry)
# Use MCP: mcp_work-efforts_create_work_effort(...)
```

**Notebook Structure**:
```
_notebook/
├── index.json                    # Index of all entries
├── entries/                      # Individual notebook entries
│   ├── entry_20260112_050000_problem.json
│   └── entry_20260112_050100_diagnosis.json
├── reflections/                  # Reflections on findings
│   └── reflection_20260112_050200.json
└── actionables/                  # Created actionable items
    └── work_effort_WE-260112-xxxx.json
```

**Integration with Self-Engineering Loop**:
1. Problem detected → Journal in notebook
2. Diagnosis made → Journal in notebook
3. After iteration → Reflect on all findings
4. Reflection generates → Actionable suggestions
5. System creates → Work efforts/scenarios/quests

---

## Next Steps

1. ✅ **Implement Problem Detection**: Build monitoring system
2. ✅ **Implement Notebook System**: Journal and reflect on findings
3. **Implement Diagnosis**: Build root cause analysis
4. **Implement Solution Engineering**: Build solution proposal and implementation
5. **Implement Self-Modification**: Complete self-modification engine
6. **Implement Iteration Loop**: Build main self-engineering loop (with notebook integration)
7. **Test End-to-End**: Run full self-engineering cycle

---

## The Meta-Game

> "The game is not just playing D&D. The game is engineering the system to play D&D better. And the meta-game is engineering the system to engineer itself better."

This is recursive self-improvement - the system improving itself to improve itself better. This is the vision.

---
