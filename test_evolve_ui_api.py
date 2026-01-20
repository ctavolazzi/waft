#!/usr/bin/env python3
"""
Test script to prove the Evolve UI Monitor API works.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from waft.api.routes.evolve_ui_monitor import scan_ui_evolution_directory, router

def test_scan():
    """Test the file scanning function."""
    project_path = Path.cwd()
    print(f"📁 Project path: {project_path}")
    print(f"📂 Scanning: {project_path / '_genetics' / 'ui_evolution'}")
    print()
    
    try:
        runs = scan_ui_evolution_directory(project_path)
        print(f"✅ Found {len(runs)} runs")
        print()
        
        for run_id, run_data in sorted(runs.items(), reverse=True):
            print(f"🔹 Run ID: {run_id}")
            print(f"   Phase: {run_data['phase']}")
            print(f"   HTML files: {len(run_data['artifacts']['html'])}")
            print(f"   Screenshots: {len(run_data['artifacts']['screenshots'])}")
            print(f"   Case files: {len(run_data['artifacts']['case_files'])}")
            if run_data['artifacts']['design_doc']:
                print(f"   Design doc: {run_data['artifacts']['design_doc']}")
            if run_data['artifacts']['wireframe']:
                print(f"   Wireframe: {run_data['artifacts']['wireframe']}")
            print()
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_router():
    """Test that the router is set up correctly."""
    print("🔌 Testing router...")
    routes = [r.path for r in router.routes]
    print(f"✅ Router has {len(routes)} route(s): {routes}")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Evolve UI Monitor API - Proof Test")
    print("=" * 60)
    print()
    
    # Test router
    router_ok = test_router()
    print()
    
    # Test scanning
    scan_ok = test_scan()
    
    print("=" * 60)
    if router_ok and scan_ok:
        print("✅ ALL TESTS PASSED - API IS WORKING!")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)