# Usage Examples

## Basic Usage

### Create and Seed a Demo

```bash
# Step 1: Create demo from template
python3 scripts/init_demo.py my_demo

# Step 2: Seed with test data
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo
```

### Verify It Works

```bash
# Check souls
ls -la my_demo/_hidden/.truth/akasha/

# Check catalog
cat my_demo/_hidden/.truth/market/catalog.json | jq '.lifetimes[0]'
```

---

## Advanced Usage

### Multiple Demo Instances

Create separate demos for different test scenarios:

```bash
# Create demos for different test suites
python3 scripts/init_demo.py demo_unit_tests
python3 scripts/init_demo.py demo_integration_tests
python3 scripts/init_demo.py demo_state_transitions

# Seed each one
python3 scripts/seed_reincarnation_demo.py --demo-path demo_unit_tests
python3 scripts/seed_reincarnation_demo.py --demo-path demo_integration_tests
python3 scripts/seed_reincarnation_demo.py --demo-path demo_state_transitions
```

### Reset and Re-seed

```bash
# Reset existing demo to clean state
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --reset
```

### Clean Up

```bash
# Delete demo when done
rm -rf my_demo
```

---

## Integration Testing

### Test State Transitions

```bash
# Create demo for state transition tests
python3 scripts/init_demo.py demo_state_test
python3 scripts/seed_reincarnation_demo.py --demo-path demo_state_test

# Run your state transition tests
python3 tests/test_state_transitions.py --demo-path demo_state_test
```

### Test Capability Restrictions

```bash
# Create demo for capability tests
python3 scripts/init_demo.py demo_capability_test
python3 scripts/seed_reincarnation_demo.py --demo-path demo_capability_test

# Run capability restriction tests
python3 tests/test_capabilities.py --demo-path demo_capability_test
```

---

## Development Workflow

### Iterative Testing

```bash
# Create demo for current work
python3 scripts/init_demo.py demo_current_feature

# Seed it
python3 scripts/seed_reincarnation_demo.py --demo-path demo_current_feature

# Make changes to code...

# Reset and test again
python3 scripts/seed_reincarnation_demo.py --demo-path demo_current_feature --reset

# Test your changes
python3 tests/test_feature.py --demo-path demo_current_feature
```

### Parallel Development

```bash
# Developer A working on state system
python3 scripts/init_demo.py demo_dev_a_state
python3 scripts/seed_reincarnation_demo.py --demo-path demo_dev_a_state

# Developer B working on capabilities
python3 scripts/init_demo.py demo_dev_b_capabilities
python3 scripts/seed_reincarnation_demo.py --demo-path demo_dev_b_capabilities
```

---

## CI/CD Integration

### Automated Testing

```bash
#!/bin/bash
# test_script.sh

# Create fresh demo for each test run
python3 scripts/init_demo.py demo_ci_$(date +%s)
DEMO_PATH="demo_ci_$(date +%s)"

# Seed it
python3 scripts/seed_reincarnation_demo.py --demo-path "$DEMO_PATH"

# Run tests
python3 -m pytest tests/ --demo-path "$DEMO_PATH"

# Clean up
rm -rf "$DEMO_PATH"
```

---

## Best Practices

1. **Always Copy Template**: Never modify `demo_template/` directly
2. **Use Descriptive Names**: Name demos by purpose (`demo_auth_test`, `demo_state_machine`, etc.)
3. **Isolate Tests**: Use separate demos for different test scenarios
4. **Reset When Needed**: Use `--reset` to get clean state
5. **Clean Up**: Delete demos when done to save space

---

## Troubleshooting

### Demo Already Exists

```bash
# Error: Demo already exists
# Solution: Use --reset flag or delete first
rm -rf my_demo
python3 scripts/init_demo.py my_demo
```

### Template Not Found

```bash
# Error: Template not found
# Solution: Ensure demo_template/ exists in project root
ls -la demo_template/
```

### Permission Errors

```bash
# If you get permission errors, check file permissions
ls -la my_demo/_hidden/.truth/akasha/
# Should show 0600 for soul files, 0700 for directory
```

---

**Happy Testing!** 🚀
