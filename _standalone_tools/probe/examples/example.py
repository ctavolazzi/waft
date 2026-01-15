#!/usr/bin/env python3
"""
Example usage of the Probe system - Pokey Stick for Testing

Demonstrates how to use probes to poke at services, files, and endpoints.
"""

from probe import ProbeCollector


def main():
    """Demonstrate probe system usage."""
    print("=" * 70)
    print("🔍 Probe System - Pokey Stick Demo")
    print("=" * 70)
    print()
    
    # Create collector
    collector = ProbeCollector()
    
    # Example 1: Probe HTTP endpoints
    print("📡 Probing HTTP endpoints...")
    collector.probe_http("http://httpbin.org/get")
    collector.probe_http("http://httpbin.org/status/200")
    print("   ✓ Probed 2 HTTP endpoints")
    print()
    
    # Example 2: Probe file system
    print("📁 Probing file system...")
    collector.probe_file("README.md")
    collector.probe_file("src")
    print("   ✓ Probed 2 file system paths")
    print()
    
    # Example 3: Probe services
    print("🔌 Probing services...")
    collector.probe_service("google.com", 80)
    collector.probe_service("github.com", 443)
    print("   ✓ Probed 2 service ports")
    print()
    
    # Show summary
    print("=" * 70)
    print("📊 Probe Summary")
    print("=" * 70)
    summary = collector.summary()
    print(f"Total probes: {summary['total']}")
    print(f"Successful: {summary['successful']}")
    print(f"Failed: {summary['failed']}")
    print(f"Average duration: {summary['avg_duration_ms']:.2f}ms")
    print()
    print("By type:")
    for probe_type, count in summary['by_type'].items():
        print(f"  - {probe_type}: {count}")
    print()
    
    # Show some results
    print("=" * 70)
    print("🔍 Sample Results")
    print("=" * 70)
    all_results = collector.collect_all()
    for i, result in enumerate(all_results[:5], 1):
        status = "✅" if result.success else "❌"
        print(f"{i}. {status} {result.probe_type}: {result.target}")
        if result.error:
            print(f"   Error: {result.error}")
        elif result.data:
            # Show key data
            if result.probe_type.startswith("http"):
                print(f"   Status: {result.data.get('status_code', 'N/A')}")
            elif result.probe_type == "filesystem":
                print(f"   Type: {result.data.get('type', 'N/A')}")
            elif result.probe_type == "service":
                print(f"   Open: {result.data.get('open', False)}")
        print()
    
    # Save results
    print("=" * 70)
    print("💾 Saving Results")
    print("=" * 70)
    filepath = collector.save_results()
    print(f"Results saved to: {filepath}")
    print()
    
    print("✅ Probe demo complete!")


if __name__ == "__main__":
    main()
