"""
Test script for Oracle wiring in NarcissusAgent.
Runs a single trial to verify the Brain-Body connection.
"""

import sys
from pathlib import Path

base_path = Path(__file__).resolve().parent
waft_root = base_path.parents[2]

if str(waft_root / "src") not in sys.path:
    sys.path.insert(0, str(waft_root / "src"))
if str(base_path) not in sys.path:
    sys.path.insert(0, str(base_path))
if str(base_path / "src") not in sys.path:
    sys.path.insert(0, str(base_path / "src"))

from agents.narcissus import NarcissusAgent

# Save original
narcissus_path = base_path / "src" / "agents" / "narcissus.py"
original_source = narcissus_path.read_text(encoding="utf-8")

# Inject fracture
DEMENTIA_CODE = """def _think(self, source: str, rng: random.Random | None = None, failure_rate: float = 0.0) -> dict:
    if 1 == 1:
        # NARCISSUS_LOGIC_FRACTURE
        return None
    return {"action": "noop", "reason": "Unreachable"}
"""


def replace_function_source(source: str, function_name: str, new_code: str) -> str:
    lines = source.splitlines()
    start = None
    indent = ""
    for idx, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(f"def {function_name}(") and line.startswith("    "):
            start = idx
            indent = line[: len(line) - len(stripped)]
            break
    if start is None:
        raise ValueError(f"Function not found: {function_name}")
    end = len(lines)
    for idx in range(start + 1, len(lines)):
        line = lines[idx]
        if line.startswith(indent) and line.lstrip().startswith("def "):
            end = idx
            break
    new_lines = []
    for line in new_code.strip().splitlines():
        if line.strip():
            new_lines.append(f"{indent}{line}")
        else:
            new_lines.append("")
    updated = lines[:start] + new_lines + lines[end:]
    return "\n".join(updated) + "\n"


print("🔧 Injecting fracture...")
fractured_source = replace_function_source(original_source, "_think", DEMENTIA_CODE)
narcissus_path.write_text(fractured_source, encoding="utf-8")
print("   ✅ Fracture injected")

# Create agent
print("🧠 Initializing NarcissusAgent with TheOracle...")
try:
    agent = NarcissusAgent(project_path=waft_root)
    print(f"   Oracle ready: {agent.oracle is not None}")
    print(f"   EmpiricaManager ready: {agent.empirica_manager is not None}")
except Exception as e:
    print(f"   ❌ Initialization failed: {e}")
    narcissus_path.write_text(original_source, encoding="utf-8")
    sys.exit(1)

# Run diagnosis
print("🔍 Running diagnosis...")
try:
    diagnosis = agent.run_diagnosis(failure_rate=0.0)
except Exception as e:
    print(f"   ❌ Diagnosis failed: {e}")
    import traceback
    traceback.print_exc()
    diagnosis = {"attempted_patch": False, "result": None, "decision": None}

# Check result
after_source = narcissus_path.read_text(encoding="utf-8")
bug_present = "# NARCISSUS_LOGIC_FRACTURE" in after_source

print(f"\n📊 Results:")
print(f"   Patch attempted: {diagnosis.get('attempted_patch', False)}")
result = diagnosis.get("result")
if result:
    print(f"   Patch success: {result.get('success', False)}")
    if result.get("error"):
        print(f"   Error: {result.get('error')}")
decision = diagnosis.get("decision")
if decision:
    print(f"   Decision note: {decision.get('note', 'N/A')}")
    print(f"   Decision action: {decision.get('action', 'N/A')}")
print(f"   Bug present after: {bug_present}")
print(f"   Bug removed: {not bug_present}")

# Restore
narcissus_path.write_text(original_source, encoding="utf-8")
print("\n✅ Original source restored")
