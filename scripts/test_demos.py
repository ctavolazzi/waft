#!/usr/bin/env python3
"""
WAFT Demo Testing Script
========================

Tests demo functionality without requiring full user interaction.
Verifies key components and identifies potential issues.
"""

import sys
import importlib.util
from pathlib import Path
from typing import List, Tuple

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class Colors:
    """ANSI color codes."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def test_import(module_path: Path, module_name: str) -> Tuple[bool, str]:
    """Test if a module can be imported."""
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None or spec.loader is None:
            return False, f"Could not create spec for {module_name}"
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return True, f"Successfully imported {module_name}"
    except Exception as e:
        return False, f"Import error: {str(e)}"

def test_function_exists(module, func_name: str) -> Tuple[bool, str]:
    """Test if a function exists in a module."""
    if hasattr(module, func_name):
        func = getattr(module, func_name)
        if callable(func):
            return True, f"Function {func_name} exists and is callable"
        return False, f"{func_name} exists but is not callable"
    return False, f"Function {func_name} not found"

def main():
    """Run demo tests."""
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}WAFT Demo Testing{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}\n")
    
    tests_passed = 0
    tests_failed = 0
    issues: List[str] = []
    
    # Test 1: Interactive Demo Import
    print(f"{Colors.CYAN}Test 1: Interactive Demo Import{Colors.END}")
    interactive_demo_path = PROJECT_ROOT / "examples" / "interactive_demo.py"
    passed, msg = test_import(interactive_demo_path, "interactive_demo")
    if passed:
        print(f"  {Colors.GREEN}✅{Colors.END} {msg}")
        tests_passed += 1
        
        # Test key functions
        try:
            spec = importlib.util.spec_from_file_location("interactive_demo", interactive_demo_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                key_functions = ["welcome_message", "main"]
                for func_name in key_functions:
                    func_passed, func_msg = test_function_exists(module, func_name)
                    if func_passed:
                        print(f"    {Colors.GREEN}✅{Colors.END} {func_msg}")
                        tests_passed += 1
                    else:
                        print(f"    {Colors.RED}❌{Colors.END} {func_msg}")
                        tests_failed += 1
                        issues.append(f"Interactive demo: {func_msg}")
        except Exception as e:
            print(f"  {Colors.RED}❌{Colors.END} Error testing functions: {e}")
            tests_failed += 1
            issues.append(f"Interactive demo function test error: {e}")
    else:
        print(f"  {Colors.RED}❌{Colors.END} {msg}")
        tests_failed += 1
        issues.append(msg)
    print()
    
    # Test 2: Advanced Demo Import
    print(f"{Colors.CYAN}Test 2: Advanced Demo Import{Colors.END}")
    advanced_demo_path = PROJECT_ROOT / "examples" / "advanced_demo" / "advanced_demo.py"
    passed, msg = test_import(advanced_demo_path, "advanced_demo")
    if passed:
        print(f"  {Colors.GREEN}✅{Colors.END} {msg}")
        tests_passed += 1
        
        # Test key functions
        try:
            spec = importlib.util.spec_from_file_location("advanced_demo", advanced_demo_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                key_functions = ["welcome_message", "main"]
                for func_name in key_functions:
                    func_passed, func_msg = test_function_exists(module, func_name)
                    if func_passed:
                        print(f"    {Colors.GREEN}✅{Colors.END} {func_msg}")
                        tests_passed += 1
                    else:
                        print(f"    {Colors.RED}❌{Colors.END} {func_msg}")
                        tests_failed += 1
                        issues.append(f"Advanced demo: {func_msg}")
        except Exception as e:
            print(f"  {Colors.RED}❌{Colors.END} Error testing functions: {e}")
            tests_failed += 1
            issues.append(f"Advanced demo function test error: {e}")
    else:
        print(f"  {Colors.RED}❌{Colors.END} {msg}")
        tests_failed += 1
        issues.append(msg)
    print()
    
    # Test 3: Reflection Demo Import
    print(f"{Colors.CYAN}Test 3: Reflection Demo Import{Colors.END}")
    reflection_demo_path = PROJECT_ROOT / "examples" / "demonstrate_reflection.py"
    passed, msg = test_import(reflection_demo_path, "demonstrate_reflection")
    if passed:
        print(f"  {Colors.GREEN}✅{Colors.END} {msg}")
        tests_passed += 1
    else:
        print(f"  {Colors.RED}❌{Colors.END} {msg}")
        tests_failed += 1
        issues.append(msg)
    print()
    
    # Test 4: Demo Dependencies
    print(f"{Colors.CYAN}Test 4: Demo Dependencies{Colors.END}")
    dependencies = ["rich", "pathlib"]
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  {Colors.GREEN}✅{Colors.END} {dep} available")
            tests_passed += 1
        except ImportError:
            print(f"  {Colors.RED}❌{Colors.END} {dep} not available")
            tests_failed += 1
            issues.append(f"Missing dependency: {dep}")
    print()
    
    # Summary
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}")
    print(f"{Colors.BOLD}Test Summary{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.END}\n")
    print(f"  {Colors.GREEN}✅ Passed: {tests_passed}{Colors.END}")
    print(f"  {Colors.RED}❌ Failed: {tests_failed}{Colors.END}")
    print(f"  Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")
    print()
    
    if issues:
        print(f"{Colors.YELLOW}Issues Found:{Colors.END}")
        for issue in issues:
            print(f"  • {issue}")
        print()
    
    if tests_failed == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED{Colors.END}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.END}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
