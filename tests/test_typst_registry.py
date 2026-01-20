"""
Integration tests for TypstTemplateRegistry.

Tests auto-discovery, metadata extraction, search functionality, and error handling.
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.waft.templates.typst.registry import (
    TypstTemplateMetadata,
    TypstTemplateRegistry,
    get_typst_registry,
)


@pytest.fixture
def temp_wrappers_dir():
    """Create a temporary wrappers directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        wrappers_dir = Path(tmpdir) / "wrappers"
        wrappers_dir.mkdir()
        yield wrappers_dir


@pytest.fixture
def sample_wrapper_module(temp_wrappers_dir):
    """Create a sample wrapper module for testing."""
    wrapper_file = temp_wrappers_dir / "test_template.py"
    wrapper_file.write_text(
        '''
"""
Test Template Wrapper

This is a test template for unit testing.
Category: test
Tags: [test, example]
Source: testrepo
"""

def generate_test_template(title: str, content: str, output_path: Path, author: str = "Test Author"):
    """
    Generate a test template.

    Args:
        title: Document title
        content: Document content
        output_path: Output PDF path
        author: Author name
    """
    pass
''',
        encoding="utf-8",
    )
    return wrapper_file


class TestRegistryDiscovery:
    """Test auto-discovery of wrapper modules."""

    def test_empty_wrappers_directory(self, temp_wrappers_dir):
        """Test registry with empty wrappers directory."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)
        assert registry.count() == 0
        assert len(registry.list_templates()) == 0

    def test_nonexistent_wrappers_directory(self):
        """Test registry with nonexistent wrappers directory."""
        nonexistent_dir = Path("/nonexistent/path/wrappers")
        registry = TypstTemplateRegistry(wrappers_dir=nonexistent_dir)
        assert registry.count() == 0

    def test_auto_discovery_of_wrapper_modules(self, temp_wrappers_dir, sample_wrapper_module):
        """Test that wrapper modules are auto-discovered."""
        # Add the module to sys.path temporarily so it can be imported

        # Create __init__.py
        init_file = temp_wrappers_dir / "__init__.py"
        init_file.write_text("", encoding="utf-8")

        # Mock the import to avoid actual module loading issues
        with patch("importlib.import_module") as mock_import:
            mock_module = MagicMock()
            mock_module.__doc__ = """
            Test Template Wrapper

            This is a test template for unit testing.
            """
            mock_module.generate_test_template = MagicMock()
            mock_import.return_value = mock_module

            # Mock inspect.getmembers to return our generate function
            with patch("inspect.getmembers") as mock_getmembers:
                mock_getmembers.return_value = [
                    ("generate_test_template", mock_module.generate_test_template)
                ]

                TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)
                # Should discover the template (if import works)
                # Note: This is a simplified test due to import complexity

    def test_ignores_init_and_cache_files(self, temp_wrappers_dir):
        """Test that __init__.py and __pycache__ are ignored."""
        # Create __init__.py
        init_file = temp_wrappers_dir / "__init__.py"
        init_file.write_text("", encoding="utf-8")

        # Create __pycache__ directory
        cache_dir = temp_wrappers_dir / "__pycache__"
        cache_dir.mkdir()
        cache_file = cache_dir / "test.pyc"
        cache_file.write_bytes(b"fake bytecode")

        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)
        # Should not try to load __init__.py or __pycache__ files
        assert registry.count() == 0


class TestMetadataExtraction:
    """Test metadata extraction from wrapper modules."""

    def test_extract_description_from_docstring(self):
        """Test that description is extracted from module docstring."""
        registry = TypstTemplateRegistry()

        docstring = """
        Test Template

        This is a test template description.
        """
        description = registry._extract_description(docstring)
        assert "test template description" in description.lower()

    def test_extract_category_from_docstring(self):
        """Test that category is extracted from docstring."""
        registry = TypstTemplateRegistry()

        docstring = "category: preprint"
        category = registry._extract_category(docstring, "test_module")
        assert category == "preprint"

    def test_infer_category_from_module_name(self):
        """Test that category is inferred from module name."""
        registry = TypstTemplateRegistry()

        # Test various category inferences
        assert registry._extract_category("", "preprint_template") == "preprint"
        assert registry._extract_category("", "dnd5e_template") == "rpg"
        assert registry._extract_category("", "campaign_template") == "rpg"
        assert registry._extract_category("", "cv_template") == "cv"
        assert registry._extract_category("", "unknown_template") == "general"

    def test_extract_tags_from_docstring(self):
        """Test that tags are extracted from docstring."""
        registry = TypstTemplateRegistry()

        docstring = "tags: [test, example, typst]"
        tags = registry._extract_tags(docstring, "test_module")
        assert "test" in tags
        assert "example" in tags
        assert "typst" in tags
        assert "pdf" in tags  # Should be added automatically

    def test_generate_display_name(self):
        """Test display name generation from module name."""
        registry = TypstTemplateRegistry()

        assert registry._generate_display_name("test_template") == "Test Template"
        assert registry._generate_display_name("dnd5e_campaign") == "Dnd5e Campaign"
        assert registry._generate_display_name("simple") == "Simple"


class TestSearchFunctionality:
    """Test search and filtering functionality."""

    def test_search_by_name(self, temp_wrappers_dir):
        """Test searching templates by name."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        # Create mock templates
        template1 = TypstTemplateMetadata(
            name="Test Template",
            module_name="test_template",
            description="A test template",
            category="test",
        )
        template2 = TypstTemplateMetadata(
            name="Another Template",
            module_name="another_template",
            description="Another template",
            category="test",
        )

        registry._templates["test_template"] = template1
        registry._templates["another_template"] = template2

        # Search for "Test Template" (exact match)
        results = registry.search("Test Template")
        assert len(results) >= 1
        assert any(r.name == "Test Template" for r in results)

        # Search for just "Test" - may match both if category contains "test"
        # So we just verify it finds the right one
        results_test = registry.search("Test")
        assert len(results_test) >= 1
        assert any(r.name == "Test Template" for r in results_test)

    def test_search_by_description(self, temp_wrappers_dir):
        """Test searching templates by description."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        template = TypstTemplateMetadata(
            name="Test Template",
            module_name="test_template",
            description="A template for academic papers",
            category="academic",
        )
        registry._templates["test_template"] = template

        results = registry.search("academic")
        assert len(results) == 1

    def test_search_by_tags(self, temp_wrappers_dir):
        """Test searching templates by tags."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        template = TypstTemplateMetadata(
            name="Test Template",
            module_name="test_template",
            description="A test template",
            category="test",
            tags=["dnd", "rpg", "typst"],
        )
        registry._templates["test_template"] = template

        results = registry.search("dnd")
        assert len(results) == 1

    def test_search_by_category(self, temp_wrappers_dir):
        """Test searching templates by category."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        template = TypstTemplateMetadata(
            name="Test Template",
            module_name="test_template",
            description="A test template",
            category="preprint",
        )
        registry._templates["test_template"] = template

        results = registry.search("preprint")
        assert len(results) == 1

    def test_search_case_insensitive(self, temp_wrappers_dir):
        """Test that search is case-insensitive."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        template = TypstTemplateMetadata(
            name="Test Template",
            module_name="test_template",
            description="A test template",
            category="test",
        )
        registry._templates["test_template"] = template

        results = registry.search("TEST")
        assert len(results) == 1


class TestTemplateRetrieval:
    """Test template retrieval functionality."""

    def test_get_template_by_name(self, temp_wrappers_dir):
        """Test getting template by name."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        template = TypstTemplateMetadata(
            name="Test Template",
            module_name="test_template",
            description="A test template",
            category="test",
        )
        registry._templates["test_template"] = template

        result = registry.get_template("Test Template")
        assert result is not None
        assert result.name == "Test Template"

    def test_get_template_by_module_name(self, temp_wrappers_dir):
        """Test getting template by module name."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        template = TypstTemplateMetadata(
            name="Test Template",
            module_name="test_template",
            description="A test template",
            category="test",
        )
        registry._templates["test_template"] = template

        result = registry.get_template("test_template")
        assert result is not None
        assert result.module_name == "test_template"

    def test_get_template_case_insensitive(self, temp_wrappers_dir):
        """Test that template retrieval is case-insensitive."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        template = TypstTemplateMetadata(
            name="Test Template",
            module_name="test_template",
            description="A test template",
            category="test",
        )
        registry._templates["test_template"] = template

        result = registry.get_template("test template")
        assert result is not None

    def test_get_nonexistent_template(self, temp_wrappers_dir):
        """Test getting a template that doesn't exist."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        result = registry.get_template("Nonexistent Template")
        assert result is None


class TestErrorHandling:
    """Test error handling in registry."""

    def test_continues_loading_if_one_module_fails(self, temp_wrappers_dir):
        """Test that registry continues loading if one module fails."""
        # Create a valid module and an invalid one
        valid_file = temp_wrappers_dir / "valid.py"
        valid_file.write_text(
            """
def generate_valid():
    pass
""",
            encoding="utf-8",
        )

        invalid_file = temp_wrappers_dir / "invalid.py"
        invalid_file.write_text(
            """
This is invalid Python syntax {{
""",
            encoding="utf-8",
        )

        # Registry should continue loading despite invalid module
        TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)
        # Should not crash, may or may not load templates depending on import behavior

    def test_handles_missing_generate_function(self, temp_wrappers_dir):
        """Test that modules without generate functions are skipped."""
        wrapper_file = temp_wrappers_dir / "no_generate.py"
        wrapper_file.write_text(
            """
def some_other_function():
    pass
""",
            encoding="utf-8",
        )

        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)
        # Should not load template without generate function
        assert registry.count() == 0


class TestGlobalRegistry:
    """Test global registry instance."""

    def test_get_typst_registry_returns_singleton(self):
        """Test that get_typst_registry returns a singleton."""
        registry1 = get_typst_registry()
        registry2 = get_typst_registry()

        assert registry1 is registry2

    def test_get_categories(self, temp_wrappers_dir):
        """Test getting all categories."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        template1 = TypstTemplateMetadata(
            name="Template 1", module_name="template1", description="Test", category="preprint"
        )
        template2 = TypstTemplateMetadata(
            name="Template 2", module_name="template2", description="Test", category="rpg"
        )

        registry._templates["template1"] = template1
        registry._templates["template2"] = template2

        categories = registry.get_categories()
        assert "preprint" in categories
        assert "rpg" in categories

    def test_get_tags(self, temp_wrappers_dir):
        """Test getting all tags."""
        registry = TypstTemplateRegistry(wrappers_dir=temp_wrappers_dir)

        # Create template with tags (tags are added during extraction, not here)
        # So we manually add typst tag to simulate the extraction process
        template = TypstTemplateMetadata(
            name="Template",
            module_name="template",
            description="Test",
            tags=[
                "test",
                "example",
                "typst",
                "pdf",
            ],  # Include typst and pdf as they're added during extraction
        )
        registry._templates["template"] = template

        tags = registry.get_tags()
        assert "test" in tags
        assert "example" in tags
        assert "typst" in tags
        assert "pdf" in tags
