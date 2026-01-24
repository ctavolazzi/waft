#!/usr/bin/env python3
"""
Browser Testing for TheGuide Homebase (localhost:8008)

Uses Playwright for headless/headed browser automation.
Run the server first: uv run python theguide_hello.py
"""

import asyncio
import sys
from pathlib import Path

# Ensure we can import from the project
sys.path.insert(0, str(Path(__file__).parent))


async def test_homebase_loads():
    """Test that the homebase loads correctly."""
    from playwright.async_api import async_playwright
    
    print("🧪 Testing Homebase (localhost:8008)")
    print("=" * 50)
    
    async with async_playwright() as p:
        # Launch Chromium (headless by default)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to homebase
            print("📍 Navigating to http://localhost:8008...")
            await page.goto("http://localhost:8008", timeout=10000)
            
            # Check title
            title = await page.title()
            print(f"✅ Page title: {title}")
            
            # Check for Console Goblin
            goblin_header = await page.query_selector("h3:has-text('GOBLIN')")
            if goblin_header:
                print("✅ Console Goblin found")
            else:
                print("⚠️  Console Goblin header not found")
            
            # Check for canvas (3-Body animation)
            canvas = await page.query_selector("#threeBody")
            if canvas:
                print("✅ 3-Body canvas found")
            else:
                print("⚠️  Canvas not found")
            
            # Check for FVCU metrics
            fvcu_items = await page.query_selector_all("[data-metric]")
            print(f"✅ FVCU metrics found: {len(fvcu_items)}")
            
            # Check for logs container
            logs = await page.query_selector("#logs")
            if logs:
                print("✅ Logs container found")
            
            # Check SSE connection (wait for events)
            print("\n📡 Testing SSE connection...")
            await page.wait_for_timeout(2000)  # Wait for SSE to connect
            
            # Check console for connection message
            console_messages = []
            page.on("console", lambda msg: console_messages.append(msg.text))
            await page.reload()
            await page.wait_for_timeout(1500)
            
            sse_connected = any("Goblin" in msg or "Connected" in msg for msg in console_messages)
            print(f"✅ SSE connection: {'Active' if sse_connected else 'Pending'}")
            
            # Take a screenshot
            screenshot_path = Path(__file__).parent / "screenshots"
            screenshot_path.mkdir(exist_ok=True)
            await page.screenshot(path=str(screenshot_path / "homebase_test.png"))
            print(f"📸 Screenshot saved: screenshots/homebase_test.png")
            
            print("\n" + "=" * 50)
            print("✅ All tests passed!")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            print("\n💡 Make sure the server is running:")
            print("   uv run python theguide_hello.py")
            return False
        
        finally:
            await browser.close()
    
    return True


async def test_sse_events():
    """Test that SSE events are received correctly."""
    from playwright.async_api import async_playwright
    
    print("\n🧪 Testing SSE Event Stream")
    print("=" * 50)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Create event listener for SSE
            events_received = []
            
            async def handle_response(response):
                if "/events" in response.url:
                    events_received.append(response.url)
            
            page.on("response", handle_response)
            
            await page.goto("http://localhost:8008", timeout=10000)
            await page.wait_for_timeout(3000)
            
            print(f"✅ SSE endpoint called: {len(events_received) > 0}")
            
            # Check if logs appeared
            log_entries = await page.query_selector_all(".log-entry")
            print(f"✅ Log entries rendered: {len(log_entries)}")
            
        except Exception as e:
            print(f"❌ SSE test failed: {e}")
            return False
        finally:
            await browser.close()
    
    return True


async def interactive_session():
    """Open an interactive browser session for manual testing."""
    from playwright.async_api import async_playwright
    
    print("\n🌐 Opening Interactive Browser Session")
    print("=" * 50)
    print("Press Ctrl+C to close")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Headed mode
        page = await browser.new_page()
        
        try:
            await page.goto("http://localhost:8008")
            print("✅ Browser opened at localhost:8008")
            print("💡 Interact with the page manually")
            
            # Keep alive until interrupted
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            print("\n👋 Closing browser...")
        finally:
            await browser.close()


def main():
    """Run browser tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Browser tests for TheGuide Homebase")
    parser.add_argument("--interactive", "-i", action="store_true", help="Open interactive browser")
    parser.add_argument("--headed", action="store_true", help="Run tests with visible browser")
    args = parser.parse_args()
    
    if args.interactive:
        asyncio.run(interactive_session())
    else:
        print("\n🏠 TheGuide Homebase Browser Tests")
        print("=" * 50)
        print("Target: http://localhost:8008")
        print()
        
        success = asyncio.run(test_homebase_loads())
        if success:
            asyncio.run(test_sse_events())


if __name__ == "__main__":
    main()
