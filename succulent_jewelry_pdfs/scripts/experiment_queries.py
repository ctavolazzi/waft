#!/usr/bin/env python3
"""
Query Experiment Tool
=====================

Test various query strategies and compare results between APIs.
"""

import sys
import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

# Add paths
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
succulent_pdfs_root = Path(__file__).parent.parent
sys.path.insert(0, str(succulent_pdfs_root))

from scripts.image_api import PixabayAPI, PexelsAPI


def test_query_variations(base_query: str) -> Dict:
    """Test different query variations."""
    
    variations = [
        base_query,
        base_query.lower(),
        base_query.upper(),
        base_query.title(),
        f"{base_query} plant",
        f"{base_query} care",
        f"how to {base_query}",
        f"{base_query} guide"
    ]
    
    results = {
        "base_query": base_query,
        "variations": {}
    }
    
    # Test Pixabay
    print(f"  Testing Pixabay variations for '{base_query}'...")
    pixabay = PixabayAPI()
    pixabay_results = {}
    
    for variation in variations:
        try:
            result = pixabay.search_images(variation, per_page=1)
            if result and result.get('hits'):
                pixabay_results[variation] = {
                    "total": result.get('totalHits', 0),
                    "first_result_tags": result['hits'][0].get('tags', '')[:50]
                }
            else:
                pixabay_results[variation] = {"total": 0}
        except Exception as e:
            pixabay_results[variation] = {"error": str(e)}
    
    results["variations"]["pixabay"] = pixabay_results
    
    # Test Pexels
    print(f"  Testing Pexels variations for '{base_query}'...")
    pexels = PexelsAPI()
    pexels_results = {}
    
    for variation in variations:
        try:
            result = pexels.search_photos(variation, per_page=1)
            if result and result.get('photos'):
                pexels_results[variation] = {
                    "total": result.get('total_results', 0),
                    "first_result_photographer": result['photos'][0].get('photographer', 'N/A')
                }
            else:
                pexels_results[variation] = {"total": 0}
        except Exception as e:
            pexels_results[variation] = {"error": str(e)}
    
    results["variations"]["pexels"] = pexels_results
    
    return results


def test_specific_queries() -> Dict:
    """Test specific queries relevant to succulent jewelry."""
    
    queries = [
        "succulent",
        "echeveria",
        "jewelry making",
        "vacuum casting",
        "plant care",
        "botanical",
        "cactus",
        "handmade",
        "silver jewelry",
        "nature photography"
    ]
    
    results = {
        "queries": {}
    }
    
    pixabay = PixabayAPI()
    pexels = PexelsAPI()
    
    for query in queries:
        print(f"Testing: '{query}'")
        query_results = {
            "pixabay": {},
            "pexels": {}
        }
        
        # Pixabay
        try:
            pixabay_result = pixabay.search_images(query, per_page=3)
            if pixabay_result and pixabay_result.get('hits'):
                query_results["pixabay"] = {
                    "total": pixabay_result.get('totalHits', 0),
                    "returned": len(pixabay_result['hits']),
                    "sample_tags": [hit.get('tags', '')[:30] for hit in pixabay_result['hits'][:3]]
                }
        except Exception as e:
            query_results["pixabay"] = {"error": str(e)}
        
        # Pexels
        try:
            pexels_result = pexels.search_photos(query, per_page=3)
            if pexels_result and pexels_result.get('photos'):
                query_results["pexels"] = {
                    "total": pexels_result.get('total_results', 0),
                    "returned": len(pexels_result['photos']),
                    "sample_photographers": [photo.get('photographer', 'N/A') for photo in pexels_result['photos'][:3]]
                }
        except Exception as e:
            query_results["pexels"] = {"error": str(e)}
        
        results["queries"][query] = query_results
    
    return results


def generate_query_report(results: Dict, output_path: Path):
    """Generate query experiment report."""
    
    report = f"""# Query Strategy Experiments

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Query Variations Test

"""
    
    if "base_query" in results:
        report += f"### Base Query: \"{results['base_query']}\"\n\n"
        report += "| Variation | Pixabay Results | Pexels Results |\n"
        report += "|-----------|-----------------|----------------|\n"
        
        pixabay_vars = results.get("variations", {}).get("pixabay", {})
        pexels_vars = results.get("variations", {}).get("pexels", {})
        
        all_variations = set(list(pixabay_vars.keys()) + list(pexels_vars.keys()))
        
        for var in sorted(all_variations):
            pixabay_total = pixabay_vars.get(var, {}).get("total", "N/A")
            pexels_total = pexels_vars.get(var, {}).get("total", "N/A")
            report += f"| `{var}` | {pixabay_total} | {pexels_total} |\n"
        
        report += "\n"
    
    if "queries" in results:
        report += "## Specific Query Results\n\n"
        report += "| Query | Pixabay Total | Pexels Total | Best Match |\n"
        report += "|-------|---------------|--------------|------------|\n"
        
        for query, query_data in results["queries"].items():
            pixabay_total = query_data.get("pixabay", {}).get("total", 0)
            pexels_total = query_data.get("pexels", {}).get("total", 0)
            
            if pixabay_total > pexels_total:
                best = "Pixabay"
            elif pexels_total > pixabay_total:
                best = "Pexels"
            else:
                best = "Tie"
            
            report += f"| `{query}` | {pixabay_total:,} | {pexels_total:,} | {best} |\n"
    
    output_path.write_text(report, encoding='utf-8')
    print(f"✅ Query report saved: {output_path}")


def main():
    """Run query experiments."""
    
    print("🔍 Query Strategy Experiments\n")
    
    results = {}
    
    # Test 1: Query variations
    print("1. Testing query variations...")
    variation_results = test_query_variations("succulent")
    results.update(variation_results)
    
    # Test 2: Specific queries
    print("\n2. Testing specific queries...")
    specific_results = test_specific_queries()
    results.update(specific_results)
    
    # Save results
    from pathlib import Path as PathLib
    script_dir = PathLib(__file__).parent
    output_dir = script_dir.parent / "generated" / "experiments"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON data
    json_path = output_dir / "query_experiments.json"
    json_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f"\n✅ JSON data saved: {json_path}")
    
    # Markdown report
    report_path = output_dir / "query_experiments_report.md"
    generate_query_report(results, report_path)
    
    print(f"\n✅ Query experiments complete! Check {output_dir} for results.")


if __name__ == '__main__':
    main()
