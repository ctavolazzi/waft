#!/usr/bin/env python3
"""
Quick test script for the data tracing system.
Tests the Decision Engine pipeline with tracing enabled.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from waft.core.input_transformer import InputTransformer
from waft.core.decision_matrix import DecisionMatrixCalculator
from waft.core.tracing import get_tracer, TraceViewer


def main():
    print("🔍 Testing Data Tracing System\n")
    print("=" * 60)

    # Sample decision data
    test_data = {
        'alternatives': ['Python', 'JavaScript', 'Go'],
        'criteria': {
            'Performance': 0.4,
            'Ease of Learning': 0.3,
            'Ecosystem': 0.3
        },
        'scores': {
            'Python': {
                'Performance': 7.0,
                'Ease of Learning': 9.0,
                'Ecosystem': 10.0
            },
            'JavaScript': {
                'Performance': 6.0,
                'Ease of Learning': 8.0,
                'Ecosystem': 9.0
            },
            'Go': {
                'Performance': 9.0,
                'Ease of Learning': 7.0,
                'Ecosystem': 6.0
            }
        },
        'methodology': 'WSM'
    }

    print("\n📝 Test Input:")
    print(f"  Problem: Choose a programming language")
    print(f"  Alternatives: {test_data['alternatives']}")
    print(f"  Criteria: {list(test_data['criteria'].keys())}")

    # Start trace
    tracer = get_tracer()
    trace_span = tracer.start_trace("test.decision_analysis", "test", metadata={
        "test": "tracing_system",
        "description": "Testing data tracing with Decision Engine"
    })

    try:
        print("\n⚙️  Running Decision Analysis with Tracing...\n")

        # Transform input
        matrix = InputTransformer.transform_input(test_data)

        # Calculate
        calculator = DecisionMatrixCalculator(matrix)
        results = calculator.calculate_wsm()
        rankings = calculator.rank_alternatives(results)

        # End trace
        tracer.end_span(trace_span, output_data={
            "winner": rankings[0][0],
            "score": rankings[0][1]
        })

        print("✅ Analysis Complete!")
        print(f"\n📊 Results:")
        for name, score, rank in rankings:
            print(f"  {rank}. {name}: {score:.2f}")

        # Get trace ID
        trace_id = trace_span.trace_id
        print(f"\n🔬 Trace ID: {trace_id}")

        # Display trace
        print("\n" + "=" * 60)
        print("📋 TRACE DATA:")
        print("=" * 60)

        viewer = TraceViewer()
        trace_tree = viewer.format_trace_tree(trace_id)
        print(trace_tree)

        print("\n" + "=" * 60)
        print("✅ Tracing System Test PASSED!")
        print("=" * 60)

        print("\n💡 Next Steps:")
        print("  1. View all traces: waft trace list")
        print(f"  2. View this trace: waft trace show {trace_id[:8]}")
        print(f"  3. Trace files location: _pyrite/analytics/traces/")

    except Exception as e:
        from waft.core.tracing import SpanStatus
        tracer.end_span(trace_span, SpanStatus.ERROR, error=e)
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
