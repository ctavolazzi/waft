# Eleventy CYOA - Quick Start

## It Works

```bash
# Test that it loads
python3.12 test_direct.py

# Play the demo scenario
python3.12 run_scenario.py examples/eleventy_cyoa_demo

# Play your own scenario
python3.12 run_scenario.py path/to/your/scenario
```

## Format

Each `.md` file in your scenario directory:

```yaml
---
title: Node Title
choices:
  - text: Choice description
    path: target_node_id
---

Markdown content here. **Formatting** works.
```

No choices = ending.

## Create a Scenario

```bash
mkdir my_scenario
cd my_scenario

# Create start.md
cat > start.md << 'EOF'
---
title: The Beginning
choices:
  - text: Go left
    path: left
  - text: Go right
    path: right
---

You stand at a crossroads.
EOF

# Create endings
cat > left.md << 'EOF'
---
title: The Left Path
---

You chose left. Victory!
EOF

cat > right.md << 'EOF'
---
title: The Right Path
---

You chose right. Defeat!
EOF

# Run it
cd ..
python3.12 run_scenario.py my_scenario
```

## That's It

See `docs/SCENARIO_FORMAT_SPEC.md` for details.
