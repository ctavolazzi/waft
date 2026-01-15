# Pyrite Examples

This directory contains examples and tests for Pyrite, the God of Work Efforts.

## Files

- **`pyrite_demo.py`** - Interactive demo showcasing Pyrite's capabilities
- **`pyrite_obstacle_course.py`** - Comprehensive test suite (obstacle course)
- **`README_PYRITE.md`** - This file

## Running the Demo

```bash
# From project root
python3 examples/pyrite_demo.py

# Or make it executable and run directly
chmod +x examples/pyrite_demo.py
./examples/pyrite_demo.py
```

The demo will show:
1. **/think** - Cognitive systems initialization
2. **Locking System** - Acquire/release locks
3. **Monitoring** - Monitor work efforts
4. **Organization** - Graph-based organization
5. **Personality** - Attributes and growth
6. **Secrets** - Encrypted secrets system
7. **Evolution** - Evolutionary cycles
8. **Status** - Complete system state

## Running the Obstacle Course

```bash
# From project root
python3 examples/pyrite_obstacle_course.py

# Or make it executable and run directly
chmod +x examples/pyrite_obstacle_course.py
./examples/pyrite_obstacle_course.py
```

The obstacle course tests:
1. **Basic Functionality** - Core Pyrite operations
2. **Locking System** - Lock acquire/release
3. **Concurrent Locking** - Thread safety
4. **Monitoring** - State tracking
5. **Organization** - Graph operations
6. **Evolutionary Cycles** - Evolution system
7. **Personality** - Attributes and growth
8. **Secrets** - Secret management
9. **Status Management** - Status updates
10. **Edge Cases** - Error handling
11. **Empirica Integration** - Epistemic tracking

Results are saved to `pyrite_obstacle_course_results.json`.

## Requirements

- Python 3.10+
- WAFT project with `_work_efforts/` directory
- Empirica (optional, for full functionality)

## Expected Output

### Demo Output
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
  ...
```

### Obstacle Course Output
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
...
```

## Troubleshooting

### "No work efforts available"
- Ensure `_work_efforts/` directory exists
- Run `waft init` or create work efforts first

### "Empirica not initialized"
- Empirica is optional but recommended
- Run `empirica project-init` in project root
- Or let Pyrite auto-initialize it

### Import errors
- Ensure you're running from project root
- Or add `src/` to PYTHONPATH

## Next Steps

After running the demo and obstacle course:

1. **Review Results** - Check `pyrite_obstacle_course_results.json`
2. **Explore Abilities** - Try different Pyrite abilities
3. **Create Work Efforts** - Test with real work efforts
4. **Integrate** - Use Pyrite in your workflows

See `docs/pyrite.md` for complete documentation.
