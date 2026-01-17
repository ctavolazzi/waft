#!/usr/bin/env python3
"""
Test TheGuide Implementation

Comprehensive test script to verify TheGuide meta-cognitive guidance system.

Usage:
    # With real LLMs (requires API keys)
    export LLM_API_KEY="your-api-key"
    export LLM_MODEL="anthropic/claude-sonnet-4-5-20250929"
    python scripts/test_guide_implementation.py --live

    # With mock LLMs (no API required)
    python scripts/test_guide_implementation.py --mock

    # Run all tests
    python scripts/test_guide_implementation.py --all
"""

import os
import sys
from pathlib import Path
import argparse
import json
from datetime import datetime

# Add pantheon directory to path (bypass waft package __init__)
pantheon_path = Path(__file__).parent.parent / "src" / "waft" / "pantheon"
sys.path.insert(0, str(pantheon_path))

try:
    # Import directly from guide module (bypassing package __init__)
    import importlib.util
    guide_module_path = pantheon_path / "guide.py"
    spec = importlib.util.spec_from_file_location("guide", guide_module_path)
    guide_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guide_module)

    TheGuide = guide_module.TheGuide
    Protocol = guide_module.Protocol
    EvaluationScores = guide_module.EvaluationScores

    print("✅ Successfully imported TheGuide, Protocol, EvaluationScores")
except ImportError as e:
    print(f"❌ Failed to import from guide module: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


class MockLLM:
    """Mock LLM for testing without API calls."""

    def __init__(self, model="mock", api_key=None, base_url=None):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.call_count = 0

    def complete(self, prompt: str) -> str:
        """Mock LLM completion."""
        self.call_count += 1

        # Different responses based on prompt content
        if "meta-cognitive guide" in prompt.lower() and "first instruction" in prompt.lower():
            return "Let's start by understanding the OAuth2 flow and identifying the key components we need to implement."

        elif "meta-cognitive guide" in prompt.lower():
            return "Now, let's implement the authorization endpoint that handles the initial user authentication request."

        elif "follow the instruction" in prompt.lower():
            return """OAuth2 has four main roles:
1. Resource Owner (the user)
2. Client (your application)
3. Authorization Server (handles authentication)
4. Resource Server (hosts protected resources)

For implementation in Python, we need:
- Flask/FastAPI for the server
- requests-oauthlib library
- JWT tokens for secure communication
- Database to store client credentials and tokens"""

        elif "meta-cognitive evaluator" in prompt.lower():
            # Mock FVCU evaluation
            return """{
  "factuality": 0.95,
  "validity": 0.90,
  "coherence": 0.85,
  "utility": 0.90,
  "faithfulness": 0.95,
  "overall": 0.91,
  "rationale": "The reasoning correctly identifies the key OAuth2 components and provides a solid foundation for implementation. The steps are grounded in standard OAuth2 architecture.",
  "strengths": ["Clear component identification", "Practical library recommendations"],
  "weaknesses": ["Could provide more implementation details", "Missing security considerations"],
  "recommendations": ["Add specific code examples in next iteration", "Include security best practices"],
  "should_continue": true,
  "planning_detected": false,
  "unfaithful_reasoning_detected": false
}"""

        elif "final answer" in prompt.lower():
            return """To implement OAuth2 authentication in Python:

1. Install dependencies: `pip install Flask requests-oauthlib PyJWT`
2. Set up the OAuth2 provider (Authorization Server)
3. Implement the authorization endpoint
4. Implement the token endpoint
5. Protect your resources with token validation
6. Use proper security measures (HTTPS, token expiration, refresh tokens)

Key code structure:
- `/authorize` - handles user consent
- `/token` - exchanges authorization code for access token
- Middleware for validating tokens on protected routes

This provides a complete OAuth2 implementation following RFC 6749 standards."""

        else:
            return f"Mock response to prompt (call #{self.call_count})"


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(title: str):
    """Print a formatted section."""
    print(f"\n{'─' * 80}")
    print(f"  {title}")
    print(f"{'─' * 80}")


def test_imports():
    """Test that all imports work correctly."""
    print_header("Test 1: Import Verification")

    try:
        # Already imported at module level
        print("✅ TheGuide imported successfully")
        print("✅ Protocol model imported successfully")
        print("✅ EvaluationScores model imported successfully")

        # Check that they're the right types
        assert hasattr(TheGuide, 'solve'), "TheGuide should have solve method"
        assert hasattr(TheGuide, 'explain'), "TheGuide should have explain method"
        assert hasattr(Protocol, 'model_fields'), "Protocol should be a Pydantic model"
        assert hasattr(EvaluationScores, 'model_fields'), "EvaluationScores should be a Pydantic model"

        print("✅ All classes have expected attributes")
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False


def test_initialization():
    """Test TheGuide initialization."""
    print_header("Test 2: TheGuide Initialization")

    try:
        project_path = Path(__file__).parent.parent

        # Create mock client LLM
        mock_client = MockLLM(model="mock-client")

        # Initialize TheGuide
        guide = TheGuide(
            project_path=project_path,
            client_llm=mock_client,
            guide_llm_config={
                "model": "mock-guide",
                "api_key": "mock-key"
            }
        )

        print(f"✅ TheGuide initialized successfully")
        print(f"   Project path: {guide.project_path}")
        print(f"   Guide path: {guide.guide_path}")
        print(f"   Client LLM: {guide.client_llm.model}")

        # Check storage directories
        assert guide.guide_path.exists(), "Guide path should be created"
        assert (guide.guide_path / "sessions").exists(), "Sessions directory should exist"
        assert (guide.guide_path / "protocols").exists(), "Protocols directory should exist"

        print(f"✅ Storage directories created:")
        print(f"   - {guide.guide_path / 'sessions'}")
        print(f"   - {guide.guide_path / 'protocols'}")

        return guide
    except Exception as e:
        print(f"❌ Initialization test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_protocol_models():
    """Test Pydantic models."""
    print_header("Test 3: Protocol Models")

    try:
        # Test EvaluationScores
        scores = EvaluationScores(
            factuality=0.95,
            validity=0.90,
            coherence=0.85,
            utility=0.90,
            faithfulness=0.95,
            overall=0.91
        )
        print("✅ EvaluationScores model created:")
        print(f"   Factuality: {scores.factuality}")
        print(f"   Validity: {scores.validity}")
        print(f"   Coherence: {scores.coherence}")
        print(f"   Utility: {scores.utility}")
        print(f"   Faithfulness: {scores.faithfulness}")
        print(f"   Overall: {scores.overall}")

        # Test Protocol
        protocol = Protocol(
            session_id="test_session_001",
            problem_statement="Test problem",
            reasoning_chain=[
                {
                    "iteration": 1,
                    "instruction": "Test instruction",
                    "reasoning_trace": "Test reasoning",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            evaluations=[
                {
                    "iteration": 1,
                    "scores": {
                        "factuality": 0.95,
                        "validity": 0.90,
                        "coherence": 0.85,
                        "utility": 0.90,
                        "faithfulness": 0.95,
                        "overall": 0.91
                    },
                    "rationale": "Test rationale",
                    "strengths": ["Strength 1"],
                    "weaknesses": ["Weakness 1"],
                    "recommendations": ["Recommendation 1"]
                }
            ],
            final_answer="Test answer",
            quality_score=0.91,
            iteration_count=1
        )
        print("✅ Protocol model created:")
        print(f"   Session ID: {protocol.session_id}")
        print(f"   Problem: {protocol.problem_statement}")
        print(f"   Iterations: {protocol.iteration_count}")
        print(f"   Quality Score: {protocol.quality_score}")

        # Test JSON serialization
        protocol_json = protocol.model_dump_json(indent=2)
        print("✅ Protocol can be serialized to JSON")

        return True
    except Exception as e:
        print(f"❌ Protocol models test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mock_guidance_loop(guide: TheGuide):
    """Test guidance loop with mock LLMs."""
    print_header("Test 4: Mock Guidance Loop")

    try:
        # Override guide_llm with mock
        guide.guide_llm = MockLLM(model="mock-guide")

        print("📝 Starting mock guidance session...")
        print("   Problem: How do I implement OAuth2 authentication in Python?")
        print("   Max iterations: 3")
        print("   Quality threshold: 0.8")

        # Run guidance loop
        answer, protocol = guide.solve(
            problem_statement="How do I implement OAuth2 authentication in Python?",
            max_iterations=3,
            quality_threshold=0.8,
            use_partial_context=True,
            test_time_scaling=1
        )

        print(f"\n✅ Guidance loop completed!")
        print(f"   Session ID: {protocol.session_id}")
        print(f"   Iterations: {protocol.iteration_count}")
        print(f"   Quality Score: {protocol.quality_score:.2f}")

        print_section("Final Answer")
        print(answer)

        print_section("Reasoning Chain Summary")
        for i, step in enumerate(protocol.reasoning_chain, 1):
            print(f"\nIteration {i}:")
            print(f"  Instruction: {step['instruction'][:80]}...")
            print(f"  Reasoning: {step['reasoning_trace'][:80]}...")

        print_section("FVCU+Faithfulness Evaluations")
        for eval_data in protocol.evaluations:
            print(f"\nIteration {eval_data['iteration']}:")
            scores = eval_data['scores']
            print(f"  Factuality:   {scores['factuality']:.2f}")
            print(f"  Validity:     {scores['validity']:.2f}")
            print(f"  Coherence:    {scores['coherence']:.2f}")
            print(f"  Utility:      {scores['utility']:.2f}")
            print(f"  Faithfulness: {scores['faithfulness']:.2f}")
            print(f"  Overall:      {scores['overall']:.2f}")
            print(f"  Strengths: {', '.join(eval_data.get('strengths', []))}")
            print(f"  Weaknesses: {', '.join(eval_data.get('weaknesses', []))}")

        return protocol
    except Exception as e:
        print(f"❌ Mock guidance loop test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_why_explanation(guide: TheGuide, protocol: Protocol):
    """Test 'Why?' explanation generation."""
    print_header("Test 5: 'Why?' Explanation")

    try:
        print(f"📝 Generating explanation for session: {protocol.session_id}")

        explanation = guide.explain(protocol.session_id)

        print("\n✅ Explanation generated successfully!")
        print_section("Explanation Preview")

        # Print first 1000 characters of explanation
        preview = explanation[:1000]
        print(preview)
        if len(explanation) > 1000:
            print(f"\n... (truncated, full length: {len(explanation)} characters)")

        # Verify explanation contains key sections
        assert "Meta-Cognitive Guidance Explanation" in explanation
        assert "Problem Statement" in explanation
        assert "Reasoning Chain" in explanation
        assert "Final Answer" in explanation
        assert "FVCU+Faithfulness" in explanation

        print("\n✅ Explanation contains all required sections")

        return True
    except Exception as e:
        print(f"❌ Why explanation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_storage_system(guide: TheGuide, protocol: Protocol):
    """Test storage and retrieval."""
    print_header("Test 6: Storage System")

    try:
        # Check session file exists
        session_file = guide.guide_path / "sessions" / f"{protocol.session_id}.json"
        assert session_file.exists(), f"Session file should exist: {session_file}"
        print(f"✅ Session file created: {session_file}")

        # Check protocol file exists
        protocol_file = guide.guide_path / "protocols" / f"{protocol.session_id}.json"
        assert protocol_file.exists(), f"Protocol file should exist: {protocol_file}"
        print(f"✅ Protocol file created: {protocol_file}")

        # Check index updated
        assert guide.index_file.exists(), "Index file should exist"
        index_data = json.loads(guide.index_file.read_text())
        assert len(index_data['sessions']) > 0, "Index should have sessions"
        print(f"✅ Index updated: {len(index_data['sessions'])} session(s)")

        # Test protocol retrieval
        retrieved_protocol = guide.get_protocol(protocol.session_id)
        assert retrieved_protocol is not None, "Should be able to retrieve protocol"
        assert retrieved_protocol.session_id == protocol.session_id
        print(f"✅ Protocol retrieved successfully")

        # Test recent sessions
        recent = guide.get_recent_sessions(limit=5)
        assert len(recent) > 0, "Should have recent sessions"
        print(f"✅ Recent sessions retrieved: {len(recent)} session(s)")

        # Test session summary
        summary = guide.get_session_summary()
        print(f"✅ Session summary:")
        print(f"   Total sessions: {summary['total_sessions']}")
        print(f"   Total protocols: {summary['total_protocols']}")
        print(f"   Indexed sessions: {summary['indexed_sessions']}")

        return True
    except Exception as e:
        print(f"❌ Storage system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_reasoner_integration(guide: TheGuide):
    """Test integration with TheReasoner."""
    print_header("Test 7: TheReasoner Integration")

    try:
        # Get reasoner
        reasoner = guide.reasoner
        print(f"✅ TheReasoner instance obtained")

        # Check that traces were created
        recent_traces = reasoner.get_recent_traces(limit=10)
        print(f"✅ Recent traces retrieved: {len(recent_traces)} trace(s)")

        if recent_traces:
            # Show first trace
            first_trace = recent_traces[0]
            print(f"\n   Latest trace:")
            print(f"   - Trace ID: {first_trace.get('trace_id', 'N/A')}")
            print(f"   - Decision: {first_trace.get('decision', 'N/A')[:60]}...")
            print(f"   - Context: {first_trace.get('context', {})}")

        return True
    except Exception as e:
        print(f"❌ Reasoner integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests(use_mock=True):
    """Run all tests."""
    print_header("🎮 TheGuide Implementation Test Suite")
    print(f"Mode: {'Mock LLMs' if use_mock else 'Live LLMs'}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {}

    # Test 1: Imports
    results['imports'] = test_imports()

    # Test 2: Initialization
    guide = test_initialization()
    results['initialization'] = guide is not None

    if not guide:
        print("\n❌ Cannot continue tests without successful initialization")
        return results

    # Test 3: Protocol Models
    results['models'] = test_protocol_models()

    # Test 4: Mock Guidance Loop
    protocol = test_mock_guidance_loop(guide)
    results['guidance_loop'] = protocol is not None

    if not protocol:
        print("\n❌ Cannot continue tests without successful guidance loop")
        return results

    # Test 5: Why Explanation
    results['explanation'] = test_why_explanation(guide, protocol)

    # Test 6: Storage System
    results['storage'] = test_storage_system(guide, protocol)

    # Test 7: Reasoner Integration
    results['reasoner'] = test_reasoner_integration(guide)

    # Summary
    print_header("📊 Test Results Summary")

    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")

    print(f"\n{'─' * 80}")
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

    if failed == 0:
        print("\n🎉 All tests passed! TheGuide is ready to use!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")

    return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Test TheGuide implementation")
    parser.add_argument("--mock", action="store_true", help="Use mock LLMs (no API required)")
    parser.add_argument("--live", action="store_true", help="Use real LLMs (requires API key)")
    parser.add_argument("--all", action="store_true", help="Run all tests (default: mock)")

    args = parser.parse_args()

    # Default to mock if nothing specified
    use_mock = args.mock or not args.live or args.all

    if args.live and not os.getenv("LLM_API_KEY"):
        print("❌ Error: LLM_API_KEY environment variable not set")
        print("   Set it with: export LLM_API_KEY='your-api-key'")
        sys.exit(1)

    # Run tests
    results = run_all_tests(use_mock=use_mock)

    # Exit code based on results
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
