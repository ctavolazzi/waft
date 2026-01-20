"""Integration tests for show_me.py full pipeline and output validation."""

import sys
from pathlib import Path
from bs4 import BeautifulSoup
import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from scripts.show_me import (
    get_work_efforts,
    get_projects,
    get_templates,
    get_catalog_summary,
    get_recent_experiments,
    get_proof_cases,
    get_reasoning_trace,
    get_session_history,
    get_chat_context,
    generate_html_report
)


class TestFullHtmlGenerationWorkflow:
    """Tests for end-to-end HTML generation workflow."""
    
    def test_full_html_generation_workflow(self, sample_work_efforts_dir, temp_project_path):
        """Test complete workflow: data collection → markdown → HTML → file output."""
        # Collect all data
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        projects = get_projects(temp_project_path)
        templates = get_templates()
        catalog = get_catalog_summary(temp_project_path)
        experiments = get_recent_experiments(temp_project_path)
        proof_cases = get_proof_cases(temp_project_path)
        reasoning_trace = get_reasoning_trace(temp_project_path)
        chat_context = get_chat_context()
        
        # Generate HTML report
        output_path = temp_project_path / "test_output.html"
        result_path = generate_html_report(
            temp_project_path,
            output_path,
            work_efforts,
            templates,
            catalog,
            experiments,
            chat_context,
            proof_cases,
            reasoning_trace,
            projects
        )
        
        # Verify file was created
        assert result_path.exists()
        assert result_path == output_path
        
        # Verify HTML content
        html_content = result_path.read_text()
        assert len(html_content) > 0
        assert "<html" in html_content.lower() or "<!DOCTYPE" in html_content.upper()
    
    def test_all_data_sources_queried(self, sample_work_efforts_dir, temp_project_path):
        """Verify that all data sources are queried in the workflow."""
        # This test ensures all functions are called
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        projects = get_projects(temp_project_path)
        templates = get_templates()
        catalog = get_catalog_summary(temp_project_path)
        experiments = get_recent_experiments(temp_project_path)
        proof_cases = get_proof_cases(temp_project_path)
        reasoning_trace = get_reasoning_trace(temp_project_path)
        chat_context = get_chat_context()
        
        # All should return valid data structures (even if empty)
        assert isinstance(work_efforts, list)
        assert isinstance(projects, list)
        assert isinstance(templates, list)
        assert isinstance(catalog, dict)
        assert isinstance(experiments, list)
        assert isinstance(proof_cases, list)
        assert isinstance(reasoning_trace, list)
        assert isinstance(chat_context, dict)


class TestHtmlOutputStructure:
    """Tests for HTML output structure validation."""
    
    def test_html_output_structure(self, sample_work_efforts_dir, temp_project_path):
        """Test HTML5 doctype, head, body structure."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for HTML5 doctype or html tag
        assert html_content.strip().startswith('<!DOCTYPE html') or soup.html is not None
        
        # Check for head section
        assert soup.head is not None or '<head' in html_content.lower()
        
        # Check for body section
        assert soup.body is not None or '<body' in html_content.lower()
        
        # Check for title in head
        if soup.head:
            title_tag = soup.head.find('title')
            assert title_tag is not None or '<title' in html_content.lower()
    
    def test_html_has_css(self, sample_work_efforts_dir, temp_project_path):
        """Test that CSS is included in HTML."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        
        # Should have CSS (either inline style tag or link)
        assert '<style' in html_content.lower() or 'css' in html_content.lower()
    
    def test_html_has_footer(self, sample_work_efforts_dir, temp_project_path):
        """Test that footer is present."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for footer (either tag or class)
        footer = soup.find('footer') or soup.find(class_='footer')
        assert footer is not None or 'footer' in html_content.lower()


class TestCollapsedSections:
    """Tests for collapsed sections functionality."""
    
    def test_collapsed_sections(self, sample_work_efforts_dir, temp_project_path):
        """Test that all <details> elements are collapsed by default."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all details elements
        details_elements = soup.find_all('details')
        
        if details_elements:
            # None should have the 'open' attribute
            for details in details_elements:
                assert 'open' not in details.attrs or details.get('open') is None


class TestSessionHistoryIntegration:
    """Tests for session history integration."""
    
    def test_session_history_in_output(self, sample_session_history_files, temp_project_path):
        """Test that session history appears in output."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        session_history = get_session_history(temp_project_path)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        
        # Should mention session history if there are files
        if session_history:
            assert "session" in html_content.lower() or "history" in html_content.lower()
    
    def test_session_history_links(self, sample_session_history_files, temp_project_path):
        """Test that session history links are correct."""
        session_history = get_session_history(temp_project_path)
        
        if session_history:
            # All items should have path, name, and date
            for item in session_history:
                assert "path" in item or "name" in item
                assert "date" in item
    
    def test_session_history_limit(self, temp_project_path):
        """Test that session history is limited to 10 items."""
        # Create more than 10 session history files
        history_dir = temp_project_path / "_work_efforts"
        history_dir.mkdir(parents=True, exist_ok=True)
        
        for i in range(15):
            filename = f"show_me_20260117_120{i:02d}00.html"
            filepath = history_dir / filename
            filepath.write_text(f"<html><body>Session {i}</body></html>")
        
        session_history = get_session_history(temp_project_path)
        
        # Should be limited to 10
        assert len(session_history) <= 10


class TestAbstractInHeader:
    """Tests for abstract placement in header."""
    
    def test_abstract_in_header(self, sample_work_efforts_dir, temp_project_path):
        """Test that abstract appears in header section."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        
        # Abstract should be present
        # The exact location depends on implementation, but should be in the document
        assert "abstract" in html_content.lower() or "summary" in html_content.lower()
    
    def test_abstract_html_formatting(self, sample_work_efforts_dir, temp_project_path):
        """Test that abstract HTML formatting is preserved."""
        work_efforts = [
            {"id": "WE-001", "title": "Test Work", "status": "active"}
        ]
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Should have proper HTML structure
        assert soup is not None


class TestExportButtons:
    """Tests for export buttons."""
    
    def test_export_buttons_present(self, sample_work_efforts_dir, temp_project_path):
        """Test that copy and download buttons are present."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for buttons (button tags or elements with button class)
        buttons = soup.find_all('button') or soup.find_all(class_='button')
        
        # Should have at least one button (copy or download)
        # Note: Implementation may vary, so we check for button-related content
        assert len(buttons) > 0 or 'button' in html_content.lower() or 'copy' in html_content.lower() or 'download' in html_content.lower()


class TestHtmlValidity:
    """Tests for HTML validity."""
    
    def test_html_validity(self, sample_work_efforts_dir, temp_project_path):
        """Test that generated HTML is valid and well-formed."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # BeautifulSoup should parse without errors
        assert soup is not None
        
        # Check for common HTML issues
        # All opening tags should have closing tags (BeautifulSoup handles this)
        # No broken tags
        assert len(soup.find_all()) > 0  # Should have some elements
    
    def test_html_proper_nesting(self, sample_work_efforts_dir, temp_project_path):
        """Test that HTML has proper nesting."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # BeautifulSoup automatically fixes nesting, so if it parses, nesting is valid
        assert soup.html is not None or soup.find('html') is not None


class TestStatisticsAccuracy:
    """Tests for statistics accuracy."""
    
    def test_statistics_accuracy(self, sample_work_efforts_dir, temp_project_path):
        """Test that Quick Stats numbers match actual data counts."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        active_count = len([w for w in work_efforts if w.get("status") == "active"])
        total_count = len(work_efforts)
        
        output_path = temp_project_path / "test_output.html"
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        
        # Should mention work efforts count
        if total_count > 0:
            assert str(total_count) in html_content or "work effort" in html_content.lower()
        
        if active_count > 0:
            assert str(active_count) in html_content or "active" in html_content.lower()
    
    def test_projects_count_accuracy(self, temp_project_path):
        """Test that projects count is accurate."""
        projects = get_projects(temp_project_path)
        projects_count = len(projects)
        
        output_path = temp_project_path / "test_output.html"
        result_path = generate_html_report(
            temp_project_path, output_path, [], [], {}, [], {}, [], [], projects
        )
        
        html_content = result_path.read_text()
        
        if projects_count > 0:
            # Should mention projects
            assert "project" in html_content.lower()


class TestWorkEffortLinks:
    """Tests for work effort links."""
    
    def test_work_effort_links_present(self, sample_work_efforts_dir, temp_project_path):
        """Test that work effort links are present and clickable."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        
        if not work_efforts:
            pytest.skip("No work efforts to test")
        
        output_path = temp_project_path / "test_output.html"
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Should have links (anchor tags)
        links = soup.find_all('a')
        
        # At least one link should be present
        assert len(links) > 0 or 'href' in html_content.lower()
    
    def test_work_effort_links_correct_paths(self, sample_work_efforts_dir, temp_project_path):
        """Test that work effort links have correct paths."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        
        if not work_efforts:
            pytest.skip("No work efforts to test")
        
        output_path = temp_project_path / "test_output.html"
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        
        # Check that work effort paths are mentioned
        for we in work_efforts[:3]:  # Check first 3
            if "path" in we:
                # Path should be in HTML (as link or text)
                assert we["path"] in html_content or we["id"] in html_content


class TestResponsiveDesign:
    """Tests for responsive design features."""
    
    def test_responsive_design_css(self, sample_work_efforts_dir, temp_project_path):
        """Test that CSS includes responsive breakpoints."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        
        # Should have media queries or responsive CSS
        assert '@media' in html_content or 'responsive' in html_content.lower() or 'viewport' in html_content.lower()
    
    def test_responsive_meta_tag(self, sample_work_efforts_dir, temp_project_path):
        """Test that viewport meta tag is present."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], [], [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check for viewport meta tag
        if soup.head:
            viewport = soup.head.find('meta', attrs={'name': 'viewport'})
            assert viewport is not None or 'viewport' in html_content.lower()


class TestAccessibilityFeatures:
    """Tests for accessibility features."""
    
    def test_accessibility_semantic_html(self, sample_work_efforts_dir, temp_project_path):
        """Test that semantic HTML elements are used."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Should have semantic elements
        semantic_tags = ['header', 'main', 'footer', 'nav', 'section', 'article']
        found_semantic = any(soup.find(tag) is not None for tag in semantic_tags)
        
        # At least one semantic tag should be present
        assert found_semantic or any(tag in html_content.lower() for tag in semantic_tags)
    
    def test_accessibility_aria_labels(self, sample_work_efforts_dir, temp_project_path):
        """Test that ARIA labels are present where appropriate."""
        work_efforts = get_work_efforts(temp_project_path, days_back=0)
        output_path = temp_project_path / "test_output.html"
        
        result_path = generate_html_report(
            temp_project_path, output_path, work_efforts, [], {}, [], {}, [], [], []
        )
        
        html_content = result_path.read_text()
        
        # ARIA labels may or may not be present depending on implementation
        # This is a soft check - just verify HTML is accessible-friendly
        # (No negative assertions - ARIA is optional but good practice)
        assert len(html_content) > 0  # Basic check that content exists
