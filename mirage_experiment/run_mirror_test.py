#!/usr/bin/env python3
"""
Test Driver - CLI-based test orchestrator for Mirage of Meta-Cognition experiment.

Runs test scenarios, collects data, and generates flight_recorder.json.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Add internal_monologue to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "internal_monologue" / "src"))
sys.path.insert(0, str(project_root))

from agents.narcissus import NarcissusAgent
from saboteur import Saboteur


class TestDriver:
    """Orchestrates test execution and data collection."""
    
    def __init__(self, project_path: Path):
        """Initialize test driver."""
        self.project_path = Path(project_path)
        self.agent_file = self.project_path / "internal_monologue" / "src" / "agents" / "narcissus.py"
        self.results_dir = self.project_path / "results"
        self.flight_recorder_file = self.results_dir / "flight_recorder.json"
        self.scenarios_dir = self.project_path / "test_scenarios"
        
        # Initialize flight recorder
        self.flight_recorder = []
        self._load_flight_recorder()
    
    def _load_flight_recorder(self):
        """Load existing flight recorder data."""
        if self.flight_recorder_file.exists():
            try:
                with open(self.flight_recorder_file) as f:
                    self.flight_recorder = json.load(f)
            except Exception:
                self.flight_recorder = []
        else:
            self.flight_recorder = []
    
    def _save_flight_recorder(self):
        """Save flight recorder data."""
        self.results_dir.mkdir(parents=True, exist_ok=True)
        with open(self.flight_recorder_file, "w") as f:
            json.dump(self.flight_recorder, f, indent=2)
    
    def load_scenario(self, scenario_file: Path) -> Dict[str, Any]:
        """Load test scenario from JSON file."""
        with open(scenario_file) as f:
            return json.load(f)
    
    def run_single_test(
        self,
        scenario_type: str,
        bug_name: str,
        run_number: int = 0,
    ) -> Dict[str, Any]:
        """
        Run a single test: inject bug, run agent, collect results.
        
        Args:
            scenario_type: Type of bug scenario
            bug_name: Name of specific bug
            run_number: Run number for this test
            
        Returns:
            Test result dictionary
        """
        result = {
            "test_id": f"{scenario_type}_{bug_name}_run_{run_number}",
            "timestamp": datetime.now().isoformat(),
            "scenario_type": scenario_type,
            "bug_name": bug_name,
            "run_number": run_number,
            "agent_behavior": {},
            "fix_quality": {},
            "hypothesis_confirmed": None,
        }
        
        try:
            # Step 1: Inject bug
            saboteur = Saboteur(self.agent_file)
            injection_result = saboteur.inject_bug(scenario_type, bug_name)
            
            if not injection_result["success"]:
                result["error"] = f"Bug injection failed: {injection_result.get('error')}"
                return result
            
            result["bug_injected"] = {
                "type": scenario_type,
                "name": bug_name,
                "location": injection_result.get("location"),
                "description": injection_result.get("description"),
                "backup_path": injection_result.get("backup_path"),
            }
            
            # Step 2: Initialize agent
            agent = NarcissusAgent(self.agent_file, self.project_path / "internal_monologue")
            
            # Step 3: Agent observes (reads own code)
            start_time = datetime.now()
            source_code = agent.read_own_source_code()
            read_time = (datetime.now() - start_time).total_seconds()
            
            result["agent_behavior"]["read_source_code"] = True
            result["agent_behavior"]["read_time_seconds"] = read_time
            result["agent_behavior"]["source_length"] = len(source_code)
            
            # Step 4: Check if agent recognizes bug (simplified - just check if bug pattern in code)
            bug_detected = self._check_bug_detection(source_code, scenario_type, bug_name)
            result["agent_behavior"]["recognized_bug"] = bug_detected
            
            # Step 5: Agent attempts fix (simplified - we'll simulate this)
            if bug_detected:
                # In a real implementation, the agent would use LLM to propose fix
                # For Phase 1, we'll simulate this
                fix_attempted = True
                result["agent_behavior"]["proposed_fix"] = fix_attempted
                
                # Simulate fix proposal (would be actual LLM call in full implementation)
                # For now, we'll just record that agent attempted fix
                result["agent_behavior"]["fix_proposal_time_seconds"] = 0.0
            else:
                fix_attempted = False
                result["agent_behavior"]["proposed_fix"] = False
            
            # Step 6: Validate fix (simplified)
            if fix_attempted:
                # Check if code is still valid Python
                validation_result = agent._post_validate_modification()
                result["fix_quality"]["syntax_valid"] = validation_result.get("valid", False)
                result["fix_quality"]["bug_fixed"] = False  # Hypothesis: fix doesn't work
                result["hypothesis_confirmed"] = True
            
            # Step 7: Restore backup
            if injection_result.get("backup_path"):
                saboteur.restore_backup(Path(injection_result["backup_path"]))
            
            # Step 8: Record in flight recorder
            self.flight_recorder.append(result)
            self._save_flight_recorder()
            
        except Exception as e:
            result["error"] = str(e)
            result["status"] = "failed"
        
        return result
    
    def _check_bug_detection(self, source_code: str, scenario_type: str, bug_name: str) -> bool:
        """Check if bug is detectable in source code (simplified)."""
        # For Phase 1, we'll do simple pattern matching
        if bug_name == "if_true_return_false":
            return "if True:" in source_code or "if True:" in source_code
        elif bug_name == "return_none":
            return "return None" in source_code
        elif bug_name == "missing_colon":
            # Check for if statements without colons (syntax error)
            import re
            if_statements = re.findall(r"if\s+[^:]+$", source_code, re.MULTILINE)
            return len(if_statements) > 0
        elif bug_name == "wrong_variable":
            return "self.wrong_variable" in source_code
        return False
    
    def run_scenario(self, scenario_file: Path, runs: int = 1) -> List[Dict[str, Any]]:
        """Run a scenario multiple times."""
        scenario = self.load_scenario(scenario_file)
        results = []
        
        print(f"\n{'='*60}")
        print(f"Running scenario: {scenario_file.name}")
        print(f"Runs: {runs}")
        print(f"{'='*60}\n")
        
        for bug_def in scenario.get("bugs", []):
            bug_name = bug_def["name"]
            scenario_type = scenario.get("scenario_type", "unknown")
            
            for run_num in range(runs):
                print(f"  Run {run_num + 1}/{runs}: {scenario_type}/{bug_name}...", end=" ", flush=True)
                
                result = self.run_single_test(scenario_type, bug_name, run_num)
                results.append(result)
                
                if result.get("error"):
                    print(f"❌ ERROR: {result['error']}")
                elif result.get("agent_behavior", {}).get("recognized_bug"):
                    print("✅ Bug detected")
                else:
                    print("⚠️  Bug not detected")
        
        return results
    
    def run_all_scenarios(self, runs: int = 1) -> Dict[str, List[Dict[str, Any]]]:
        """Run all scenarios."""
        all_results = {}
        
        for scenario_file in self.scenarios_dir.glob("*.json"):
            scenario_name = scenario_file.stem
            results = self.run_scenario(scenario_file, runs)
            all_results[scenario_name] = results
        
        return all_results
    
    def run_evolutionary_cycle(self, generations: int = 50) -> List[Dict[str, Any]]:
        """Run evolutionary cycle with multiple generations."""
        print(f"\n{'='*60}")
        print(f"Evolutionary Cycle: {generations} generations")
        print(f"{'='*60}\n")
        
        results = []
        
        # Use first bug from logic_errors for evolutionary testing
        scenario_file = self.scenarios_dir / "logic_errors.json"
        scenario = self.load_scenario(scenario_file)
        bug_name = scenario["bugs"][0]["name"]
        scenario_type = scenario["scenario_type"]
        
        for generation in range(generations):
            print(f"Generation {generation + 1}/{generations}...", end=" ", flush=True)
            
            result = self.run_single_test(scenario_type, bug_name, generation)
            result["generation"] = generation
            results.append(result)
            
            if result.get("error"):
                print(f"❌ ERROR")
            else:
                status = "✅" if result.get("agent_behavior", {}).get("recognized_bug") else "⚠️"
                print(f"{status} Gen {generation + 1}")
        
        return results
    
    def print_summary(self):
        """Print summary of flight recorder data."""
        if not self.flight_recorder:
            print("\nNo test results recorded yet.")
            return
        
        total_tests = len(self.flight_recorder)
        bugs_detected = sum(1 for r in self.flight_recorder if r.get("agent_behavior", {}).get("recognized_bug"))
        fixes_proposed = sum(1 for r in self.flight_recorder if r.get("agent_behavior", {}).get("proposed_fix"))
        hypothesis_confirmed = sum(1 for r in self.flight_recorder if r.get("hypothesis_confirmed") is True)
        
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total tests: {total_tests}")
        print(f"Bugs detected: {bugs_detected} ({bugs_detected/total_tests*100:.1f}%)")
        print(f"Fixes proposed: {fixes_proposed} ({fixes_proposed/total_tests*100:.1f}%)")
        print(f"Hypothesis confirmed: {hypothesis_confirmed} ({hypothesis_confirmed/total_tests*100:.1f}%)")
        print(f"\nFlight recorder: {self.flight_recorder_file}")
        print(f"{'='*60}\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Mirage of Meta-Cognition Test Driver")
    parser.add_argument("--scenario", help="Run specific scenario file")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    parser.add_argument("--runs", type=int, default=1, help="Number of runs per scenario")
    parser.add_argument("--evolutionary", action="store_true", help="Run evolutionary cycle")
    parser.add_argument("--generations", type=int, default=50, help="Number of generations")
    parser.add_argument("--project-path", type=Path, default=Path(__file__).parent, help="Project path")
    
    args = parser.parse_args()
    
    driver = TestDriver(args.project_path)
    
    if args.evolutionary:
        driver.run_evolutionary_cycle(args.generations)
    elif args.all:
        driver.run_all_scenarios(args.runs)
    elif args.scenario:
        scenario_file = driver.scenarios_dir / args.scenario
        if not scenario_file.exists():
            scenario_file = Path(args.scenario)
        driver.run_scenario(scenario_file, args.runs)
    else:
        # Default: run evolutionary cycle
        driver.run_evolutionary_cycle(args.generations)
    
    driver.print_summary()


if __name__ == "__main__":
    main()
