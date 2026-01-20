#!/usr/bin/env python3
"""
Generate Profile Picture for Fai Wei using Gemini API

Uses nano-banana MCP server to generate a professional headshot.
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def main():
    """Generate profile picture for Fai Wei."""
    print("🎨 Generating profile picture for Fai Wei using Gemini API...")
    print()

    prompt = """Professional corporate headshot portrait of Fai Wei, a visionary quantum physics researcher and entrepreneur. Person in their early 30s, Asian descent, intelligent eyes, determined expression. Modern business casual attire - crisp button-down shirt. Subtle background with quantum physics visualizations - particle trails, quantum entanglement diagrams, soft blue-purple light. Professional, clean, inspiring style. Corporate headshot quality, well-lit, confident pose, looking slightly off-camera with thoughtful expression. Conveys innovation, vision, and human authenticity. High quality portrait photography."""

    print(f"📝 Prompt: {prompt[:100]}...")
    print()
    print("💡 Note: This script requires the nano-banana MCP server to be running.")
    print("   Use the MCP tool directly: mcp_nano-banana_generate_image")
    print()
    print("✅ To generate the image, use:")
    print("   mcp_nano-banana_generate_image with the prompt above")


if __name__ == "__main__":
    main()
