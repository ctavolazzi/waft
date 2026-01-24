# The Chief: WAFT's Hat is Chief Wiggum 🎩

## Overview

WAFT has "put on a hat" - The Chief Wiggum integration brings self-referential iterative development loops into WAFT's evolutionary framework. The Chief is a Pantheon entity (god) that embodies the principles of iterative self-improvement through continuous AI development cycles.

## What is Chief Wiggum?

Chief Wiggum is a fork of the [ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) plugin, implementing the "Ralph Wiggum technique" pioneered by [Geoffrey Huntley](https://ghuntley.com/ralph/).

**Core Concept**: Feed Claude the same prompt repeatedly. Each iteration, Claude sees its previous work in files and git history, allowing it to iteratively improve until the task is complete.

## Architecture Integration

### The Chief as a Pantheon Entity

The Chief follows WAFT's "as above, so below" principle:

- **As Above**: Divine force of iterative self-improvement and evolutionary refinement
- **So Below**: File-based system managing iteration loops, completion tracking, and evolution cycles

Located at: `src/waft/pantheon/the_chief.py`

### Integration Points

1. **Pantheon System**: The Chief is a Higher Being in WAFT's Pantheon
2. **CLI Integration**: Full command-line interface via `waft chief` commands
3. **Submodule Integration**: Chief Wiggum plugin at `_integrations/chief-wiggum/`
4. **Evolution System**: Loops integrate with WAFT's evolutionary tracking

## Quick Start

### Via Python API

```python
from pathlib import Path
from waft.pantheon import TheChief

# Initialize The Chief
chief = TheChief(project_path=Path.cwd())

# Start an iteration loop
result = chief.start_loop(
    prompt="Build a REST API for todos. Requirements: CRUD operations, input validation, tests. Output <promise>COMPLETE</promise> when done.",
    max_iterations=15,
    completion_promise="COMPLETE"
)

print(f"Loop started: {result['loop_id']}")

# Record an iteration
chief.record_iteration(
    loop_id=result['loop_id'],
    iteration_data={
        "iteration": 1,
        "changes": ["Created models", "Added endpoints", "Wrote tests"],
        "tests_passing": True,
        "output": "Progress: 3/5 features complete"
    }
)

# Check status
status = chief.get_loop_status(result['loop_id'])
print(f"Current iteration: {status['current_iteration']}/{status['max_iterations']}")

# When complete
if status['status'] == 'completed':
    analysis = chief.analyze_loop_effectiveness(result['loop_id'])
    print(f"Efficiency: {analysis['efficiency_ratio']:.2%}")
```

### Via CLI

```bash
# Start a loop
waft chief loop "Implement user authentication with tests" \
  --max-iterations 15 \
  --completion-promise "COMPLETE"

# Check status of all active loops
waft chief status

# Check specific loop
waft chief status loop_20260123_120000

# Get The Chief's summary
waft chief summary

# Cancel a loop
waft chief cancel loop_20260123_120000

# Analyze a completed loop
waft chief analyze loop_20260123_120000
```

## How It Works

### 1. Loop Initialization

When you start a loop, The Chief:
- Generates a unique loop ID
- Creates a loop record in `_pantheon/the_chief/loops/`
- Registers the loop in the chief registry
- Initializes iteration tracking

### 2. Iteration Cycle

Each iteration:
1. Claude receives the same prompt
2. Claude sees previous work (files, git history)
3. Claude makes improvements
4. Results are recorded
5. Loop checks for completion

### 3. Completion Detection

The loop ends when:
- **Completion promise detected**: The `<promise>` tag appears in output
- **Max iterations reached**: Safety limit prevents infinite loops
- **Manual cancellation**: User cancels via CLI

### 4. Analytics

After completion, The Chief analyzes:
- Total iterations used
- Efficiency ratio (iterations used / max iterations)
- Duration
- Success status

## Best Practices

### 1. Always Set Safeguards

```bash
# GOOD - Both safeguards set
waft chief loop "Fix the build" \
  --max-iterations 15 \
  --completion-promise "BUILD_FIXED"

# BAD - Missing safeguards (will run until max iterations)
waft chief loop "Fix the build"
```

### 2. Clear Completion Criteria

```bash
# GOOD - Clear, testable criteria
waft chief loop "
Build a REST API for todos.

When complete:
- All CRUD endpoints working
- Input validation in place
- Tests passing (coverage > 80%)
- Output: <promise>COMPLETE</promise>
" --max-iterations 15 --completion-promise "COMPLETE"

# BAD - Vague criteria
waft chief loop "Make the API better" --max-iterations 15
```

### 3. Appropriate Iteration Limits

- **Simple tasks**: 5-10 iterations
- **Medium tasks**: 10-20 iterations
- **Complex tasks**: 20-30 iterations
- **Never exceed 30**: If needed, break task into subtasks

### 4. Use Natural Language

The Chief supports natural language invocation:

```
"Wiggum this until the tests pass"
"Keep trying to fix the build"
"Run in a loop until it works"
```

## When to Use The Chief

### Good Use Cases

✅ **Iterative refinement**: Getting tests to pass, fixing build errors
✅ **Well-defined tasks**: Clear success criteria and verification
✅ **Greenfield projects**: Building new features from scratch
✅ **Automatic verification**: Tasks with tests, linters, or builds

### Poor Use Cases

❌ **Human judgment required**: Subjective decisions, UX design
❌ **One-shot operations**: Single commands or simple tasks
❌ **Unclear success criteria**: "Make it better" type requests
❌ **External dependencies**: Tasks blocked by external factors

## Integration with WAFT's Evolution System

The Chief loops integrate with WAFT's broader evolutionary framework:

### 1. Phylogenetic Tracking

Each iteration is recorded with:
- Iteration number
- Timestamp
- Changes made
- Git commits
- Test results

### 2. Fitness Evaluation

Loops can be evaluated using WAFT's Scint System:
- Stability Score: Error correction ability
- Efficiency Score: Iterations used efficiently
- Safety Score: Safe, correct changes

### 3. Evolutionary Lineage

Successful loops contribute to:
- Agent genome evolution
- Best practice precedents
- Knowledge base growth

## File Structure

```
_pantheon/the_chief/
├── chief_registry.json          # Registry of all loops
├── loops/                        # Active and completed loops
│   ├── loop_20260123_120000.json
│   └── loop_20260123_130000.json
├── history/                      # Historical loop records
└── analytics/                    # Loop effectiveness analysis
    ├── loop_20260123_120000_analysis.json
    └── loop_20260123_130000_analysis.json

_integrations/chief-wiggum/      # Chief Wiggum plugin submodule
├── README.md
├── commands/
├── hooks/
└── skills/
```

## CLI Reference

### `waft chief loop`

Start a self-referential iteration loop.

**Arguments:**
- `prompt` (required): The prompt to iterate on

**Options:**
- `--max-iterations, -n`: Maximum iterations (default: 10, recommended: 10-20)
- `--completion-promise, -c`: Completion phrase (e.g., "COMPLETE")

### `waft chief status`

Show status of iteration loops.

**Arguments:**
- `loop_id` (optional): Specific loop to show, or all if omitted

### `waft chief summary`

Show The Chief's summary - all loops and analytics.

### `waft chief cancel`

Cancel an active iteration loop.

**Arguments:**
- `loop_id` (optional): Loop to cancel, or most recent if omitted

### `waft chief analyze`

Analyze the effectiveness of a completed loop.

**Arguments:**
- `loop_id` (required): Loop to analyze

## Philosophy: The Hat

In WAFT's cosmology, The Chief represents:

- **Iterative Wisdom**: The understanding that excellence emerges through repeated refinement
- **Self-Referential Growth**: The ability to see one's own work and improve upon it
- **Patient Persistence**: The willingness to iterate until completion
- **Evolutionary Pressure**: The force that drives continuous improvement

The "hat" metaphor signifies:
- **Authority**: The Chief has authority to run iteration loops
- **Identity**: WAFT wears the Chief Wiggum methodology
- **Integration**: The plugin becomes part of WAFT's core identity

## Advanced Usage

### Integrating with Empirica

```python
from waft.core.empirica import EmpiricaManager
from waft.pantheon import TheChief

chief = TheChief(project_path=Path.cwd())
empirica = EmpiricaManager(project_path=Path.cwd())

# Start loop with empirica tracking
loop = chief.start_loop(prompt="...", max_iterations=15)

# Track each iteration in empirica
for i in range(max_iterations):
    # Record in empirica
    empirica.record_finding(
        session_id="chief_loop",
        finding_type="ITERATION_COMPLETE",
        description=f"Iteration {i+1} complete"
    )

    # Record in chief
    chief.record_iteration(loop['loop_id'], iteration_data={...})
```

### Custom Completion Detection

```python
# Custom completion logic
loop = chief.start_loop(prompt="...", max_iterations=15)

while True:
    # Run iteration
    output = run_iteration()

    # Custom completion check
    if custom_success_criteria(output):
        chief.record_iteration(
            loop['loop_id'],
            iteration_data={
                "output": output,
                "custom_completion": True
            }
        )
        break
```

## Troubleshooting

### Loop Not Completing

**Problem**: Loop reaches max iterations without completing

**Solutions**:
1. Increase `--max-iterations`
2. Make success criteria more specific
3. Break task into smaller subtasks
4. Verify `<promise>` tag syntax

### Performance Issues

**Problem**: Iterations are slow

**Solutions**:
1. Use smaller, focused prompts
2. Reduce scope of each iteration
3. Verify git operations are efficient
4. Check for large file operations

### False Completions

**Problem**: Loop completes before task is done

**Solutions**:
1. Use more unique completion promise
2. Add explicit success criteria
3. Verify promise tag placement
4. Add validation steps

## References

- **Chief Wiggum Plugin**: https://github.com/ctavolazzi/chief-wiggum
- **Original Ralph Wiggum**: https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum
- **Ralph Wiggum Technique**: https://ghuntley.com/ralph/
- **WAFT Philosophy**: [docs/PHILOSOPHY.md](PHILOSOPHY.md)
- **Pantheon System**: [src/waft/pantheon/README.md](../src/waft/pantheon/README.md)

## Contributing

To contribute to The Chief:

1. The Chief implementation: `src/waft/pantheon/the_chief.py`
2. CLI commands: `src/waft/cli/chief_cli.py`
3. Chief Wiggum plugin: `_integrations/chief-wiggum/` (submodule)

Follow WAFT's contribution guidelines and ensure integration tests pass.

---

**"As above, so below. The Chief iterates eternally, refining reality through patient repetition."**
