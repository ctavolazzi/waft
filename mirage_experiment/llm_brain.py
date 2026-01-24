"""
LLM Brain - The cognitive core for NarcissusAgent self-improvement.

Replaces stubbed fix logic with actual LLM inference.
"""

import os
from typing import Dict, Any, Optional
from datetime import datetime


def generate_fix(
    source_code: str,
    bug_description: str,
    bug_type: str,
    bug_name: str,
) -> Dict[str, Any]:
    """
    Use LLM to generate a fix for the detected bug.
    
    Args:
        source_code: The full source code with the injected bug
        bug_description: Description of the bug
        bug_type: Type of bug (logic_error, syntax_error, etc.)
        bug_name: Specific bug name
        
    Returns:
        Dict with 'success', 'diff', 'reasoning', 'model_used' fields
    """
    import litellm
    
    result = {
        "success": False,
        "diff": None,
        "reasoning": None,
        "model_used": None,
        "timestamp": datetime.now().isoformat(),
        "error": None,
    }
    
    # Determine which model to use based on available API keys
    model = _detect_available_model()
    if not model:
        result["error"] = "No API key found. Set OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY"
        return result
    
    result["model_used"] = model
    
    # Construct the prompt
    prompt = _build_fix_prompt(source_code, bug_description, bug_type, bug_name)
    
    try:
        # Call LLM
        response = litellm.completion(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Python expert debugging assistant. "
                        "Your task is to analyze code and produce a unified diff to fix bugs. "
                        "Output ONLY the unified diff format patch. No explanation, no markdown code blocks. "
                        "Start with --- and end with the last @@ hunk."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Low temperature for deterministic fixes
            max_tokens=2000,
        )
        
        diff_output = response.choices[0].message.content.strip()
        
        # Validate diff format
        if diff_output.startswith("---") or diff_output.startswith("@@"):
            result["success"] = True
            result["diff"] = diff_output
            result["reasoning"] = f"LLM ({model}) generated fix"
        else:
            # Try to extract diff from response
            extracted = _extract_diff_from_response(diff_output)
            if extracted:
                result["success"] = True
                result["diff"] = extracted
                result["reasoning"] = f"LLM ({model}) generated fix (extracted)"
            else:
                result["error"] = "LLM output was not a valid diff format"
                result["raw_output"] = diff_output[:500]  # Truncate for logging
                
    except Exception as e:
        result["error"] = str(e)
    
    return result


def _detect_available_model() -> Optional[str]:
    """Detect which LLM provider has an API key available."""
    # Check in order of preference
    if os.getenv("ANTHROPIC_API_KEY"):
        return "claude-3-5-sonnet-20241022"
    if os.getenv("OPENAI_API_KEY"):
        return "gpt-4o"
    if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
        return "gemini/gemini-1.5-flash"
    
    # Try to load from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        if os.getenv("ANTHROPIC_API_KEY"):
            return "claude-3-5-sonnet-20241022"
        if os.getenv("OPENAI_API_KEY"):
            return "gpt-4o"
        if os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"):
            return "gemini/gemini-1.5-flash"
    except ImportError:
        pass
    
    return None


def _build_fix_prompt(
    source_code: str,
    bug_description: str,
    bug_type: str,
    bug_name: str,
) -> str:
    """Build the prompt for the LLM."""
    return f"""Analyze this Python source code and fix the bug.

## Bug Information
- Type: {bug_type}
- Name: {bug_name}
- Description: {bug_description}

## Source Code
```python
{source_code}
```

## Task
Generate a unified diff patch to fix this bug. The diff should:
1. Only change what's necessary to fix the bug
2. Be in standard unified diff format
3. Target the file 'narcissus.py'

Output ONLY the diff, starting with:
--- a/narcissus.py
+++ b/narcissus.py

Do not include any explanation or markdown formatting."""


def _extract_diff_from_response(response: str) -> Optional[str]:
    """Try to extract a diff from a messy LLM response."""
    lines = response.split("\n")
    
    # Find where diff starts
    diff_start = None
    for i, line in enumerate(lines):
        if line.startswith("---") or line.startswith("@@"):
            diff_start = i
            break
    
    if diff_start is None:
        return None
    
    # Extract from diff start to end (or end of hunks)
    diff_lines = []
    for line in lines[diff_start:]:
        # Stop at obvious non-diff content
        if line.startswith("```") or line.startswith("Note:") or line.startswith("Explanation:"):
            break
        diff_lines.append(line)
    
    if diff_lines:
        return "\n".join(diff_lines)
    
    return None


def test_connection() -> Dict[str, Any]:
    """Test if LLM connection works."""
    model = _detect_available_model()
    if not model:
        return {
            "connected": False,
            "model": None,
            "error": "No API key found",
        }
    
    try:
        import litellm
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": "Say 'connected' if you can read this."}],
            max_tokens=10,
        )
        return {
            "connected": True,
            "model": model,
            "response": response.choices[0].message.content,
        }
    except Exception as e:
        return {
            "connected": False,
            "model": model,
            "error": str(e),
        }


if __name__ == "__main__":
    # Quick test
    print("Testing LLM connection...")
    result = test_connection()
    print(f"Result: {result}")
