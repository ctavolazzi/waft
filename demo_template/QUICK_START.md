# Quick Start Guide

## Create and Seed a Demo in 2 Commands

```bash
# 1. Create demo from template
python3 scripts/init_demo.py my_demo

# 2. Seed with test data
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo
```

That's it! Your demo is ready to use.

---

## Batching Mode (10 Permutations)

```bash
# 1. Create demo from template
python3 scripts/init_demo.py my_demo

# 2. Seed with 10 permutations (collated PDF)
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --batch
```

**Result**: 10 permutations collated into one PDF, HTML opens automatically!

---

## Verify It Works

```bash
# Check HTML and PDF were generated
ls -lh my_demo/demo_overview.{html,pdf}

# Open HTML page (auto-opens PDF)
open my_demo/demo_overview.html

# Check souls were created
ls -la my_demo/_hidden/.truth/akasha/

# Check catalog was created
cat my_demo/_hidden/.truth/market/catalog.json | head -20
```

**The PDF contains everything you need to know about the demo!**

---

## Reset Demo

```bash
# Reset to clean state and re-seed
python3 scripts/seed_reincarnation_demo.py --demo-path my_demo --reset
```

---

## Multiple Demos

```bash
# Create multiple demo instances
python3 scripts/init_demo.py demo_auth_test
python3 scripts/init_demo.py demo_state_test
python3 scripts/init_demo.py demo_integration_test

# Seed each one
python3 scripts/seed_reincarnation_demo.py --demo-path demo_auth_test
python3 scripts/seed_reincarnation_demo.py --demo-path demo_state_test
python3 scripts/seed_reincarnation_demo.py --demo-path demo_integration_test
```

---

## Clean Up

```bash
# Delete demo when done
rm -rf my_demo
```

---

**That's all you need!** 🚀
