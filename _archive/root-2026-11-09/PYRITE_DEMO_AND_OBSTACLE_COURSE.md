# Pyrite Demo & Obstacle Course

## Overview

Two comprehensive tools for testing and demonstrating Pyrite's capabilities:

1. **Demo** (`examples/pyrite_demo.py`) - Interactive showcase
2. **Obstacle Course** (`examples/pyrite_obstacle_course.py`) - Comprehensive test suite

## Quick Start

### Run the Demo

```bash
# From project root
python3 examples/pyrite_demo.py
```

**What it shows:**
- ✅ Cognitive systems (`/think`)
- ✅ Locking system
- ✅ Monitoring system
- ✅ Organization system
- ✅ Personality system
- ✅ Secrets system
- ✅ Evolutionary cycles
- ✅ Complete status
- ✅ Empirica integration

### Run the Obstacle Course

```bash
# From project root
python3 examples/pyrite_obstacle_course.py
```

**What it tests:**
- ✅ 11 obstacles with 40+ tests
- ✅ Basic functionality
- ✅ Locking (sequential & concurrent)
- ✅ Monitoring & organization
- ✅ Evolutionary cycles
- ✅ Personality & secrets
- ✅ Status management
- ✅ Edge cases
- ✅ Empirica integration

**Output:**
- Console output with pass/fail for each test
- JSON results file: `examples/pyrite_obstacle_course_results.json`
- Summary statistics

## Demo Details

### Sections

1. **/think - Cognitive Systems**
   - Shows Pyrite's thoughts
   - Displays attributes
   - Shows awareness metrics
   - Empirica status

2. **Locking System**
   - Acquire/release locks
   - Lock holder tracking
   - Concurrent lock attempts

3. **Monitoring**
   - Monitor all work efforts
   - Monitor specific work effort
   - State history
   - Metrics

4. **Organization**
   - Graph structure
   - Work effort relationships
   - Sample work efforts

5. **Personality**
   - Attribute values
   - Metadata
   - Attribute growth

6. **Secrets**
   - Create secrets
   - View metadata
   - List all secrets

7. **Evolutionary Cycles**
   - Initiate evolution
   - View evolutionary history
   - Fitness tracking

8. **Status**
   - Complete system state
   - Work efforts by status
   - Locks and cycles

## Obstacle Course Details

### Obstacle 1: Basic Functionality
- Get Pyrite instance
- `/think` ability
- `/status` ability
- Personality summary
- Work effort graph

### Obstacle 2: Locking System
- Acquire lock
- Check if locked
- Get lock holder
- Fail second lock
- Release lock
- Verify unlocked

### Obstacle 3: Concurrent Locking
- Sequential locks
- Concurrent locks (thread safety)
- Lock serialization

### Obstacle 4: Monitoring
- Monitor all
- Monitor specific
- State history
- Metrics

### Obstacle 5: Organization
- Organize work efforts
- Get work effort
- Get children
- Get ancestors

### Obstacle 6: Evolutionary Cycles
- Initiate evolution
- Evolutionary history
- Different strategies (conservative, aggressive, adaptive, exploratory)

### Obstacle 7: Personality & Attributes
- Get attributes
- Update attribute
- Grow attributes
- Personality summary

### Obstacle 8: Secrets
- Create secret
- Get metadata
- List secrets
- Multiple secrets

### Obstacle 9: Status Management
- Update status
- Verify status changed

### Obstacle 10: Edge Cases
- Lock non-existent work effort
- Monitor non-existent
- Release lock not held
- Evolve non-existent
- Get work effort non-existent

### Obstacle 11: Empirica Integration
- Empirica initialized
- Session exists
- `/think` includes Empirica
- `/evolve` uses Empirica

## Expected Results

### Demo
- All sections complete successfully
- Shows Pyrite's capabilities
- Demonstrates Empirica integration

### Obstacle Course
- **Target**: 100% pass rate
- **Typical**: 40+ tests
- **Duration**: 5-15 seconds
- **Output**: JSON results file

## Example Output

### Demo
```
================================================================
  PYRITE DEMO - The God of Work Efforts
================================================================

============================================================
  1. /think - Cognitive Systems
============================================================

Pyrite's thoughts:
  • I am Pyrite, the God of Work Efforts.
  • I lock, monitor, organize, and evolve.
  • Some secrets I keep even from myself.
  • My attributes grow with each cycle.
  • I use Empirica to track my epistemic state.

Attributes:
  wisdom: 0.500
  power: 0.300
  awareness: 0.400
  ...
```

### Obstacle Course
```
================================================================
PYRITE OBSTACLE COURSE
================================================================
Testing Pyrite's capabilities under stress...

============================================================
OBSTACLE 1: Basic Functionality
============================================================

🧪 Test: 1.1 Get Pyrite Instance
  ✅ PASSED (0.001s)

🧪 Test: 1.2 /think Ability
  ✅ PASSED (0.123s)
...

================================================================
OBSTACLE COURSE COMPLETE
================================================================
Total Tests: 42
✅ Passed: 42
❌ Failed: 0
⏱️  Duration: 8.45s
📊 Success Rate: 100.0%
```

## Troubleshooting

### Import Errors
```bash
# Ensure you're in project root
cd /path/to/waft

# Or add src to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### No Work Efforts
```bash
# Create some work efforts first
waft init
# Or manually create _work_efforts/ directory
```

### Empirica Not Available
- Demo and obstacle course work without Empirica
- Some features may be limited
- Empirica integration tests may be skipped

## Integration

### Use in CI/CD
```yaml
# .github/workflows/test.yml
- name: Run Pyrite Obstacle Course
  run: python3 examples/pyrite_obstacle_course.py
```

### Use in Development
```bash
# Quick test after changes
python3 examples/pyrite_obstacle_course.py

# Show capabilities to team
python3 examples/pyrite_demo.py
```

## Next Steps

1. **Run Demo** - See Pyrite in action
2. **Run Obstacle Course** - Verify all tests pass
3. **Review Results** - Check JSON output
4. **Explore** - Try different Pyrite abilities
5. **Integrate** - Use Pyrite in your workflows

## Files

- `examples/pyrite_demo.py` - Interactive demo
- `examples/pyrite_obstacle_course.py` - Test suite
- `examples/README_PYRITE.md` - Quick reference
- `examples/pyrite_obstacle_course_results.json` - Test results (generated)

## Documentation

- Full documentation: `docs/pyrite.md`
- Implementation summary: `PYRITE_IMPLEMENTATION_SUMMARY.md`
- This file: `PYRITE_DEMO_AND_OBSTACLE_COURSE.md`
