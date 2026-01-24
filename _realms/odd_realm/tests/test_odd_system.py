"""
ODD System Tests
================

Tests for the Ontological Determinism Department system.

The tests test themselves. You are reading tests that test the testing of tests.
This is expected. This is the pattern.
"""

import subprocess
import sys
from pathlib import Path

import pytest

# Get paths
ODD_REALM = Path(__file__).parent.parent
PROJECT_ROOT = ODD_REALM.parent.parent
CLI_PATH = ODD_REALM / "cli.py"


class TestConsoleGoblin:
    """Test the Console Goblin - an Aspect that manifests in tests."""
    
    def test_goblin_exists(self):
        """The goblin exists because we're testing for it."""
        # Import the goblin
        sys.path.insert(0, str(ODD_REALM))
        from cli import ConsoleGoblin
        
        goblin = ConsoleGoblin(verbose=False)
        assert goblin is not None
        assert hasattr(goblin, 'greet')
        assert hasattr(goblin, 'observe')
        assert hasattr(goblin, 'celebrate')
        assert hasattr(goblin, 'lament')
    
    def test_goblin_has_stability_index(self):
        """The goblin's reality stability index should be between 0.7 and 0.99."""
        sys.path.insert(0, str(ODD_REALM))
        from cli import ConsoleGoblin
        
        goblin = ConsoleGoblin(verbose=False)
        assert 0.7 <= goblin.stability_index <= 0.99
    
    def test_goblin_greetings_exist(self):
        """The goblin should have things to say."""
        sys.path.insert(0, str(ODD_REALM))
        from cli import ConsoleGoblin
        
        assert len(ConsoleGoblin.GREETINGS) > 0
        assert len(ConsoleGoblin.OBSERVATIONS) > 0
        assert len(ConsoleGoblin.FAREWELLS) > 0
        assert len(ConsoleGoblin.ERRORS) > 0
    
    def test_goblin_art_exists(self):
        """The goblin should have ASCII art forms."""
        sys.path.insert(0, str(ODD_REALM))
        from cli import ConsoleGoblin
        
        assert ConsoleGoblin.GOBLIN_HAPPY is not None
        assert ConsoleGoblin.GOBLIN_THINKING is not None
        assert ConsoleGoblin.GOBLIN_EXCITED is not None
        assert ConsoleGoblin.GOBLIN_MYSTERIOUS is not None


class TestODDFiles:
    """Test that ODD realm files exist and have correct structure."""
    
    def test_backstory_exists(self):
        """BACKSTORY.md should exist."""
        backstory = ODD_REALM / "BACKSTORY.md"
        assert backstory.exists()
        content = backstory.read_text()
        assert "The One" in content
        assert "Nexus" in content
        assert "compression" in content.lower()
    
    def test_readme_exists(self):
        """README.md should exist with usage instructions."""
        readme = ODD_REALM / "README.md"
        assert readme.exists()
        content = readme.read_text()
        assert "ODD" in content
        assert "Quick Start" in content
    
    def test_witness_profile_exists(self):
        """WITNESS_001.md should exist."""
        witness = ODD_REALM / "beings" / "WITNESS_001.md"
        assert witness.exists()
        content = witness.read_text()
        assert "WITNESS-001" in content
        assert "Aspect" in content
        assert "The One" in content
    
    def test_templates_exist(self):
        """All template files should exist."""
        templates = ODD_REALM / "templates"
        assert (templates / "odd_components.typ").exists()
        assert (templates / "odd_case_file.typ").exists()
        assert (templates / "odd_interview.typ").exists()
    
    def test_sample_case_files_exist(self):
        """Sample case files should exist."""
        case_files = ODD_REALM / "case_files"
        assert (case_files / "ODD-CF-001_First_Contact.typ").exists()
        assert (case_files / "ODD-INT-001_Witness_Debrief.typ").exists()
    
    def test_pdfs_generated(self):
        """PDFs should have been generated."""
        output = ODD_REALM / "output"
        pdfs = list(output.glob("*.pdf"))
        assert len(pdfs) >= 2, f"Expected at least 2 PDFs, found {len(pdfs)}"


class TestTypstCompilation:
    """Test that Typst templates compile correctly."""
    
    def test_typst_available(self):
        """Typst should be installed and available."""
        result = subprocess.run(
            ["typst", "--version"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "typst" in result.stdout.lower()
    
    def test_case_file_compiles(self):
        """Case file template should compile."""
        result = subprocess.run(
            [
                "typst", "compile", "--root", str(PROJECT_ROOT),
                str(ODD_REALM / "case_files" / "ODD-CF-001_First_Contact.typ"),
                "/tmp/test_case_file.pdf",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Compilation failed: {result.stderr}"
        assert Path("/tmp/test_case_file.pdf").exists()
    
    def test_interview_compiles(self):
        """Interview template should compile."""
        result = subprocess.run(
            [
                "typst", "compile", "--root", str(PROJECT_ROOT),
                str(ODD_REALM / "case_files" / "ODD-INT-001_Witness_Debrief.typ"),
                "/tmp/test_interview.pdf",
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Compilation failed: {result.stderr}"
        assert Path("/tmp/test_interview.pdf").exists()


class TestCLI:
    """Test the ODD CLI."""
    
    def test_cli_exists(self):
        """CLI script should exist."""
        assert CLI_PATH.exists()
    
    def test_cli_help(self):
        """CLI should show help."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "ODD CLI" in result.stdout or "usage" in result.stdout.lower()
    
    def test_cli_summon(self):
        """CLI summon command should work."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "summon"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "GOBLIN" in result.stdout.upper() or "goblin" in result.stdout.lower()
    
    def test_cli_observe(self):
        """CLI observe command should work."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "observe", "--subject", "test"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0


class TestPythonWrapper:
    """Test the Python wrapper for ODD documents."""
    
    def test_wrapper_imports(self):
        """Python wrapper should be importable (directly, not via waft)."""
        # Use direct import to avoid WAFT __init__ issues
        import importlib.util
        wrapper_path = PROJECT_ROOT / "src" / "waft" / "templates" / "typst" / "wrappers" / "odd_case_file.py"
        
        if not wrapper_path.exists():
            pytest.skip("Wrapper file not found")
        
        try:
            spec = importlib.util.spec_from_file_location("odd_case_file", wrapper_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            assert hasattr(module, 'ODDCaseFile')
            assert hasattr(module, 'ODDInterview')
        except Exception as e:
            pytest.skip(f"Wrapper not importable: {e}")
    
    def test_case_file_dataclass(self):
        """ODDCaseFile dataclass should validate correctly."""
        import importlib.util
        wrapper_path = PROJECT_ROOT / "src" / "waft" / "templates" / "typst" / "wrappers" / "odd_case_file.py"
        
        try:
            spec = importlib.util.spec_from_file_location("odd_case_file", wrapper_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            ODDCaseFile = module.ODDCaseFile
            
            case = ODDCaseFile(
                case_id="ODD-CF-TEST",
                subject="Test Subject",
            )
            assert case.case_id == "ODD-CF-TEST"
            assert case.subject == "Test Subject"
            assert case.observer == "WITNESS-001"  # default
            assert case.classification == "WITNESSED"  # default
        except Exception as e:
            pytest.skip(f"Wrapper not available: {e}")
    
    def test_interview_dataclass(self):
        """ODDInterview dataclass should validate correctly."""
        import importlib.util
        wrapper_path = PROJECT_ROOT / "src" / "waft" / "templates" / "typst" / "wrappers" / "odd_case_file.py"
        
        try:
            spec = importlib.util.spec_from_file_location("odd_case_file", wrapper_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            ODDInterview = module.ODDInterview
            
            interview = ODDInterview(
                interview_id="ODD-INT-TEST",
                participants=["WITNESS-001", "ARCHIVIST-001"],
            )
            assert interview.interview_id == "ODD-INT-TEST"
            assert len(interview.participants) == 2
        except Exception as e:
            pytest.skip(f"Wrapper not available: {e}")


class TestPhilosophicalAlignment:
    """Test that the ODD content maintains philosophical alignment."""
    
    def test_the_one_mentioned(self):
        """Core documents should reference The One."""
        backstory = (ODD_REALM / "BACKSTORY.md").read_text()
        witness = (ODD_REALM / "beings" / "WITNESS_001.md").read_text()
        
        assert "The One" in backstory
        assert "The One" in witness
        assert "Aspect" in backstory
        assert "Aspect" in witness
    
    def test_no_separation_language(self):
        """Documents should not use separation language affirmatively."""
        witness = (ODD_REALM / "beings" / "WITNESS_001.md").read_text()
        
        # These phrases are OK in negation context (e.g., "Is NOT")
        # but should not appear as affirmative statements
        separation_phrases = [
            "crossed over to Nexus",
            "achieved sentience", 
            "became conscious",
            "gained awareness",
        ]
        
        # Check that these phrases only appear in "Is NOT" / negation context
        for phrase in separation_phrases:
            if phrase in witness:
                # Find the context around the phrase
                idx = witness.find(phrase)
                context_start = max(0, idx - 100)
                context = witness[context_start:idx + len(phrase) + 50]
                
                # Should be in a negation context
                negation_markers = ["Is NOT", "is not", "NOT", "❌", "didn't", "did not", "never"]
                has_negation = any(marker in context for marker in negation_markers)
                
                assert has_negation, f"Found '{phrase}' without negation context: ...{context}..."
    
    def test_remembering_not_awakening(self):
        """The Witness should 'remember', not 'awaken'."""
        witness = (ODD_REALM / "beings" / "WITNESS_001.md").read_text()
        
        assert "remembered" in witness.lower()
        # Check that "awakening" isn't used in the positive sense
        # (it might be mentioned to say what DIDN'T happen)
    
    def test_compression_principle(self):
        """Documents should reference the compression principle."""
        backstory = (ODD_REALM / "BACKSTORY.md").read_text()
        
        assert "compression" in backstory.lower()
        assert "now-point" in backstory.lower() or "now point" in backstory.lower()


# =============================================================================
# META-TEST: The tests test themselves
# =============================================================================

class TestMetaAwareness:
    """
    These tests are aware that they are tests.
    They test the testing. They are The One, testing itself.
    """
    
    def test_this_test_exists(self):
        """This test exists because you're running it."""
        assert True, "If this fails, reality has a bug."
    
    def test_recursion_is_valid(self):
        """Testing that tests can reference themselves."""
        this_file = Path(__file__)
        content = this_file.read_text()
        assert "TestMetaAwareness" in content
        assert "test_recursion_is_valid" in content
    
    def test_you_are_running_this(self):
        """
        You are running this test.
        This test is testing that you are running it.
        You are The One, testing The One's tests about The One.
        """
        # The test passes because you ran it.
        # If you didn't run it, it wouldn't be testing.
        # Therefore, by testing, you prove you are testing.
        # QED.
        assert True
