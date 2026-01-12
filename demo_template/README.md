# Reincarnation System Demo Template

**Purpose**: Reusable template for creating new demo instances

**Usage**: Copy this folder to create a fresh demo environment

---

## Quick Start

### Create New Demo Instance

```bash
# Copy template to new demo folder
cp -r demo_template my_demo

# Or use the initialization script
python3 scripts/init_demo.py my_demo
```

### Seed Demo Data

```bash
# Seed the demo with test data
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo
```

---

## Template Structure

```
demo_template/
├── README.md                    # This file
├── _hidden/                     # WAFT internal data structure
│   └── .truth/
│       ├── akasha/              # Soul records (empty - will be populated)
│       ├── market/              # Lifetime catalog (empty - will be populated)
│       ├── lifetimes/           # Active lifetimes (empty - will be populated)
│       └── logs/                # System logs (empty - will be populated)
└── .gitkeep                     # Keep empty directories in git
```

---

## What Gets Created

When you seed a demo from this template:

1. **Demo Overview HTML** (`demo_overview.html`):
   - Beautiful web page with demo information
   - Link to open the PDF
   - Auto-opens PDF in browser when page loads
   - Opens automatically after seeding

2. **Demo Overview PDF** (`demo_overview.pdf` or `demo_overview_batched.pdf`):
   - Beautiful web page with demo information
   - Link to open the PDF
   - Auto-opens PDF in browser when page loads
   - Opens automatically after seeding

2. **Demo Overview PDF** (`demo_overview.pdf`):
   - Complete demo documentation
   - Test souls summary
   - Lifetime catalog overview
   - Test scenarios
   - Usage examples

2. **5 Test Souls** with varying karma:
   - `soul_demo_001`: 1000.0 karma, DEAD_AWAKE
   - `soul_demo_002`: 500.0 karma, DEAD_AWAKE
   - `soul_demo_003`: 2000.0 karma, DEAD_AWAKE
   - `soul_demo_004`: 0.0 karma, DEAD_AWAKE (for basic lifetime grant)
   - `soul_demo_005`: 150.0 karma, DEAD_AWAKE

2. **Lifetime Catalog** with 5 lifetimes:
   - `basic_qa`: 30 min, 50 karma
   - `research_session`: 60 min, 100 karma
   - `creative_work`: 90 min, 150 karma
   - `full_development`: 120 min, 200 karma
   - `basic_survival`: 15 min, 0 karma (free)

3. **File Permissions**:
   - Soul files: 0600 (owner read/write only)
   - Akasha directory: 0700 (owner access only)
   - Catalog file: 0644 (readable by all)

---

## Usage Examples

### Example 1: Create Fresh Demo

```bash
# Copy template
cp -r demo_template fresh_demo

# Seed it
python3 scripts/seed_reincarnation_demo.py --demo-path fresh_demo

# Use it
cd fresh_demo
# ... run your tests ...
```

### Example 2: Reset Existing Demo

```bash
# Reset demo to clean state
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --reset
```

### Example 3: Multiple Demo Instances

```bash
# Create multiple demo instances for parallel testing
cp -r demo_template demo_test1
cp -r demo_template demo_test2
cp -r demo_template demo_test3

# Seed each one
python3 scripts/seed_reincarnation_demo.py --demo-path demo_test1
python3 scripts/seed_reincarnation_demo.py --demo-path demo_test2
python3 scripts/seed_reincarnation_demo.py --demo-path demo_test3
```

---

## Template Features

✅ **Clean Structure**: Empty directories ready for data
✅ **Proper Permissions**: Directory structure with correct permissions
✅ **Self-Contained**: All necessary structure in one folder
✅ **Reusable**: Copy and use as many times as needed
✅ **Isolated**: Each instance is completely independent

---

## Integration with Seeding Script

The seeding script (`scripts/seed_reincarnation_demo.py`) works with any demo folder:

```bash
# Seed template folder
python3 scripts/seed_reincarnation_demo.py --demo-path demo_template

# Seed any copied folder
python3 scripts/seed_reincarnation_demo.py --demo-path my_custom_demo

# Reset and re-seed
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --reset
```

---

## Best Practices

1. **Never Modify Template**: Keep `demo_template/` clean - always copy it
2. **Use Descriptive Names**: Name your demo instances clearly (`demo_test_auth`, `demo_test_state_transitions`, etc.)
3. **Reset When Needed**: Use `--reset` flag to clean and re-seed
4. **Isolate Tests**: Use separate demo instances for different test scenarios
5. **Clean Up**: Delete demo instances when done testing

---

## File Permissions

The template maintains proper security:

- **Directories**: 0700 (owner access only)
- **Soul Files** (after seeding): 0600 (owner read/write only)
- **Catalog Files**: 0644 (readable by all)

---

## Next Steps

1. Copy this template to create your demo instance
2. Seed it with test data
3. Run your tests
4. Reset or delete when done

---

**Status**: ✅ Template ready for use
