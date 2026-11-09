# Demo Template System

**Location**: `demo_template/` in project root

**Purpose**: Reusable template for creating fresh demo instances

---

## Quick Start

```bash
# 1. Create demo from template
python3 scripts/init_demo.py my_demo

# 2. Seed with test data
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo
```

**That's it!** Your demo is ready to use.

---

## What You Get

### Template Structure

```
demo_template/
├── README.md                    # Full documentation
├── QUICK_START.md              # 2-command quick start
├── USAGE_EXAMPLES.md           # Usage examples
└── _hidden/.truth/
    ├── akasha/                 # Soul records (empty)
    ├── market/                 # Lifetime catalog (empty)
    ├── lifetimes/              # Active lifetimes (empty)
    └── logs/                   # System logs (empty)
```

### After Seeding

- **5 Test Souls** with varying karma (0, 150, 500, 1000, 2000)
- **Lifetime Catalog** with 5 lifetimes
- **Proper File Permissions** (0600/0700)
- **Test Scenarios** documentation

---

## Scripts

### `scripts/init_demo.py`

Creates a new demo instance from template:

```bash
python3 scripts/init_demo.py <demo_name>
```

### `scripts/seed_reincarnation_demo.py`

Seeds a demo with test data:

```bash
# Seed demo
python3 scripts/seed_reincarnation_demo.py --demo-path <demo_name>

# Reset and re-seed
python3 scripts/seed_reincarnation_demo.py --demo-path <demo_name> --reset
```

---

## Use Cases

### Development Testing

```bash
# Create demo for testing
python3 scripts/init_demo.py demo_dev_test
python3 scripts/seed_reincarnation_demo.py --demo-path demo_dev_test

# Test your changes
# ... run tests ...

# Reset and test again
python3 scripts/seed_reincarnation_demo.py --demo-path demo_dev_test --reset
```

### Multiple Test Scenarios

```bash
# Create separate demos for different tests
python3 scripts/init_demo.py demo_auth_test
python3 scripts/init_demo.py demo_state_test
python3 scripts/init_demo.py demo_integration_test

# Seed each one
python3 scripts/seed_reincarnation_demo.py --demo-path demo_auth_test
python3 scripts/seed_reincarnation_demo.py --demo-path demo_state_test
python3 scripts/seed_reincarnation_demo.py --demo-path demo_integration_test
```

### CI/CD Integration

```bash
# In your CI script
DEMO_NAME="demo_ci_$(date +%s)"
python3 scripts/init_demo.py "$DEMO_NAME"
python3 scripts/seed_reincarnation_demo.py --demo-path "$DEMO_NAME"
# ... run tests ...
rm -rf "$DEMO_NAME"
```

---

## Features

✅ **Reusable**: Copy template as many times as needed
✅ **Isolated**: Each demo instance is completely independent
✅ **Clean**: Template stays clean - never modify it directly
✅ **Fast**: 2 commands to get a working demo
✅ **Secure**: Proper file permissions (0600/0700)
✅ **Documented**: Comprehensive documentation included

---

## Best Practices

1. **Never Modify Template**: Always copy it, never edit `demo_template/` directly
2. **Use Descriptive Names**: Name demos by purpose (`demo_auth_test`, `demo_state_machine`)
3. **Isolate Tests**: Use separate demos for different scenarios
4. **Reset When Needed**: Use `--reset` flag to get clean state
5. **Clean Up**: Delete demos when done to save space

---

## Documentation

- **`demo_template/README.md`**: Full documentation
- **`demo_template/QUICK_START.md`**: 2-command quick start
- **`demo_template/USAGE_EXAMPLES.md`**: Usage examples and patterns

---

## Status

✅ **Template Created**: `demo_template/` folder ready
✅ **Scripts Created**: `init_demo.py` and `seed_reincarnation_demo.py`
✅ **Tested**: Template copy and seed verified working
✅ **Documented**: Comprehensive documentation included

---

**Ready to use!** Copy the template and seed it to create fresh demo instances. 🚀
