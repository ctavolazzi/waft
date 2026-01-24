"""
Pytest tests for TheGuide Homebase (localhost:8008)

Run with: uv run pytest tests/ -v
Requires server running: uv run python theguide_hello.py
"""

import pytest
from playwright.sync_api import Page, expect


HOMEBASE_URL = "http://localhost:8008"


@pytest.fixture(scope="module")
def browser_context(browser):
    """Create a browser context for tests."""
    context = browser.new_context()
    yield context
    context.close()


class TestHomebaseUI:
    """UI tests for the homebase dashboard."""
    
    def test_page_loads(self, page: Page):
        """Test that the homebase page loads."""
        page.goto(HOMEBASE_URL, timeout=10000)
        expect(page).to_have_title("TheGuide | Console Goblin")
    
    def test_console_goblin_present(self, page: Page):
        """Test that Console Goblin section exists."""
        page.goto(HOMEBASE_URL)
        goblin = page.locator("h3:has-text('GOBLIN')")
        expect(goblin).to_be_visible()
    
    def test_canvas_present(self, page: Page):
        """Test that 3-Body canvas exists."""
        page.goto(HOMEBASE_URL)
        canvas = page.locator("#threeBody")
        expect(canvas).to_be_visible()
    
    def test_fvcu_metrics(self, page: Page):
        """Test that FVCU metrics are present."""
        page.goto(HOMEBASE_URL)
        
        metrics = ["factuality", "validity", "coherence", "utility", "faithfulness"]
        for metric in metrics:
            element = page.locator(f"[data-metric='{metric}']")
            expect(element).to_be_visible()
    
    def test_logs_container(self, page: Page):
        """Test that logs container exists."""
        page.goto(HOMEBASE_URL)
        logs = page.locator("#logs")
        expect(logs).to_be_visible()


class TestSSEConnection:
    """Tests for Server-Sent Events connection."""
    
    def test_sse_endpoint_exists(self, page: Page):
        """Test that SSE endpoint responds."""
        page.goto(HOMEBASE_URL)
        
        # Wait a bit for SSE to connect
        page.wait_for_timeout(2000)
        
        # The logs div should have content from SSE
        logs = page.locator("#logs")
        expect(logs).to_be_visible()
    
    def test_logs_populated(self, page: Page):
        """Test that logs are populated via SSE."""
        page.goto(HOMEBASE_URL)
        page.wait_for_timeout(3000)  # Wait for SSE events
        
        # Check if any log entries appeared
        log_entries = page.locator(".log-entry")
        # Should have at least one entry from server startup
        expect(log_entries.first).to_be_visible(timeout=5000)


class TestResponsiveDesign:
    """Tests for responsive design."""
    
    def test_desktop_layout(self, page: Page):
        """Test desktop layout (3 columns)."""
        page.set_viewport_size({"width": 1200, "height": 800})
        page.goto(HOMEBASE_URL)
        
        # All panels should be visible
        expect(page.locator(".panel").first).to_be_visible()
        expect(page.locator(".center-stage")).to_be_visible()
    
    def test_mobile_layout(self, page: Page):
        """Test mobile layout (stacked)."""
        page.set_viewport_size({"width": 375, "height": 667})  # iPhone SE
        page.goto(HOMEBASE_URL)
        
        # Page should still load
        expect(page.locator("#threeBody")).to_be_visible()


class TestAPIEndpoints:
    """Tests for API endpoints."""
    
    def test_status_endpoint(self, page: Page):
        """Test /api/guide/status endpoint."""
        response = page.request.get(f"{HOMEBASE_URL}/api/guide/status")
        assert response.ok
        
        data = response.json()
        assert "active" in data
        assert data["active"] == True
    
    def test_logs_endpoint(self, page: Page):
        """Test /api/logs endpoint."""
        response = page.request.get(f"{HOMEBASE_URL}/api/logs")
        assert response.ok
        
        data = response.json()
        assert "logs" in data
        assert isinstance(data["logs"], list)
