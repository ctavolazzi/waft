#!/usr/bin/env python3
"""Test evolution engine directly."""
from pathlib import Path
from src.waft.core.evolution_engine import EvolutionEngine
from src.waft.being import BeingSystem

project_path = Path.cwd()
engine = EvolutionEngine(project_path)
being_system = BeingSystem(project_path)

# Use the Adam that was created
adam_id = 'being_20260124_113742_855d9b3d'

print("Testing evolution engine...")
try:
    result = engine.run_evolution_cycle(
        parent_id=adam_id,
        reality_id='waft-evolution',
        num_variants=3,
        generation=1,
    )
    print(f'\nSUCCESS!')
    print(f'Selected: {result.selected_variant_id}')
    print(f'Fitness improvement: {result.fitness_improvement:+.2f}')
except Exception as e:
    print(f'\nError: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
