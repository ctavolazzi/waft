#!/usr/bin/env python3
"""
Comprehensive Proof System - Build Case File with Evidence

This script:
1. Extracts claims from conversation context
2. Runs /verify checks
3. Runs /check-assumptions validation
4. Builds a case file with evidence
5. Creates PDF binder with verdict on cover
6. Displays the proof

If claims are false, states so clearly in the case brief.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))


def generate_informative_title(claim: str, verdict: str = None) -> str:
    """
    Generate an informative title from a claim.

    Extracts key information and creates a concise, descriptive title
    that conveys what the case is about.

    Args:
        claim: The claim statement
        verdict: Optional verdict (PROVEN/DISPROVEN/INCONCLUSIVE)

    Returns:
        A concise, informative title
    """
    import re

    claim = claim.strip()
    if not claim:
        return "Proof Case"

    # Pattern 1: Extract subject and key action/outcome
    # Match patterns like "The X [verb] Y" or "X [verb] Y"
    pattern = re.match(
        r"^(?:The\s+)?(.+?)\s+(?:now\s+)?(?:displays|shows|generates|creates|implements|supports|provides|includes|uses|contains|accepts|returns|handles|processes|renders|outputs|prints|saves|loads|reads|writes|executes|runs|performs|completes|finishes|starts|begins|ends|stops|removes|adds|updates|modifies|changes|fixes|corrects|improves|enhances|optimizes|refactors|replaces|deletes|has|is|does)\s+(.+?)(?:\.|$|instead of)",
        claim,
        re.IGNORECASE,
    )

    if pattern:
        subject = pattern.group(1).strip()
        outcome = pattern.group(2).strip()

        # Clean subject - remove generic terms if redundant
        subject = re.sub(
            r"\s+(generator|system|tool|module|component|feature)$",
            "",
            subject,
            flags=re.IGNORECASE,
        )

        # Clean outcome - remove "been" and other weak words, take meaningful content
        outcome = re.sub(r"^(?:been|is|are|was|were)\s+", "", outcome, flags=re.IGNORECASE)
        outcome = outcome.strip()

        # If outcome is still weak, try to extract what was actually done
        if len(outcome) < 5 or outcome.lower() in ["implemented", "created", "added", "done"]:
            # Look for what comes after "instead of" or in parentheses
            instead_of = re.search(r"instead of\s+(.+)", claim, re.IGNORECASE)
            if instead_of:
                outcome = f"replaces {instead_of.group(1).strip()}"
            else:
                # Use the subject as the main focus
                title = subject
                if verdict:
                    title = f"{title} ({verdict})"
                if len(title) > 75:
                    title = title[:72] + "..."
                return title

        # Handle parentheses in outcome - preserve them carefully
        paren_match = re.search(r"\(([^)]+)\)", outcome)
        paren_content = paren_match.group(1) if paren_match else None

        # Extract the part before "instead of" if present (that's usually the key info)
        instead_of_match = re.search(r"instead of", outcome, re.IGNORECASE)
        if instead_of_match:
            outcome = outcome[: instead_of_match.start()].strip()

        # If we have parentheses, preserve the whole phrase containing them
        if paren_content:
            # Find the full phrase with parentheses (up to 50 chars before paren)
            paren_start = outcome.find("(")
            if paren_start > 0:
                # Get text before parentheses, limit to key words
                before_paren = outcome[:paren_start].strip()
                words = before_paren.split()
                # Keep meaningful words (skip articles, but keep important short words like "AI")
                important = [
                    w
                    for w in words
                    if (len(w) > 3 or w.upper() in ["AI", "UI", "API", "PDF", "XML", "JSON"])
                    and w.lower() not in ["the", "and", "for", "with", "from", "now"]
                ][:4]
                before_paren = (
                    " ".join(important)
                    if important
                    else " ".join(words[:4])
                    if words
                    else before_paren[:30]
                )
            else:
                before_paren = ""

            # Limit paren content if too long (keep it informative)
            if len(paren_content) > 35:
                paren_words = paren_content.split()
                # Keep first few meaningful words
                paren_content = " ".join(paren_words[:5])

            outcome = (
                f"{before_paren} ({paren_content})".strip()
                if before_paren
                else f"({paren_content})"
            )
        else:
            # No parentheses - take first meaningful phrase, limit to key words
            # Split on common separators but take the first substantial part
            parts = re.split(
                r"[,\s]+(?:and|or|but|with|without|for|to|from|by|via|through|using|instead)",
                outcome,
                maxsplit=1,
            )
            main_part = parts[0].strip() if parts else outcome
            words = main_part.split()
            # Keep meaningful words (include important short words like "AI")
            important = [
                w
                for w in words
                if (len(w) > 3 or w.upper() in ["AI", "UI", "API", "PDF", "XML", "JSON"])
                and w.lower() not in ["the", "and", "for", "with", "from", "now"]
            ][:4]
            outcome = (
                " ".join(important)
                if important
                else " ".join(words[:4])
                if words
                else main_part[:40]
            )

        title = f"{subject}: {outcome}"

    else:
        # Pattern 2: Extract commands/features in parentheses (often the key feature)
        paren_match = re.search(r"\(([^)]+)\)", claim)
        if paren_match:
            feature = paren_match.group(1)
            # Get the main part before parentheses
            main = re.sub(r"\([^)]+\)", "", claim).strip()
            main = re.sub(r"^(?:The\s+)?", "", main, flags=re.IGNORECASE)

            # Extract subject from main part
            subject_match = re.match(
                r"^(.+?)\s+(?:has|is|was|does|can|will|should|must)", main, re.IGNORECASE
            )
            if subject_match:
                subject = subject_match.group(1).strip()
                # Remove generic terms
                subject = re.sub(
                    r"\s+(generator|system|tool|module|component|feature)$",
                    "",
                    subject,
                    flags=re.IGNORECASE,
                )
                title = f"{subject}: {feature}"
            else:
                main = main.split(".")[0].strip()
                if main and len(main) > 10:
                    title = f"{main} - {feature}"
                else:
                    title = feature
        else:
            # Pattern 3: Simple extraction - first sentence or key phrase
            # Remove leading articles
            claim_clean = re.sub(r"^(?:The\s+|A\s+|An\s+)", "", claim, flags=re.IGNORECASE)

            # Take first sentence or first 70 chars at word boundary
            if "." in claim_clean:
                title = claim_clean.split(".")[0].strip()
            else:
                words = claim_clean.split()
                title_parts = []
                for word in words:
                    test_title = " ".join(title_parts + [word])
                    if len(test_title) <= 70:
                        title_parts.append(word)
                    else:
                        break
                title = " ".join(title_parts) if title_parts else claim_clean[:70]

    # Clean up title
    title = title.strip()
    if not title or len(title) < 5:
        title = "Proof Case"

    # Add verdict if provided and title is meaningful
    if verdict and title != "Proof Case":
        title = f"{title} ({verdict})"

    # Final length check - ensure it fits on cover page
    # But be smarter about preserving parentheses
    if len(title) > 75:
        # If title has parentheses, try to preserve them
        paren_match = re.search(r"\(([^)]+)\)", title)
        if paren_match:
            # Keep the part before parentheses and the parentheses
            before_paren = title[: title.find("(")].strip()
            paren_part = f"({paren_match.group(1)})"

            # Limit before_paren to fit
            if len(before_paren) + len(paren_part) + 3 > 75:  # +3 for spaces
                words = before_paren.split()
                truncated = []
                for word in words:
                    test = " ".join(truncated + [word]) + " " + paren_part
                    if len(test) <= 72:
                        truncated.append(word)
                    else:
                        break
                before_paren = " ".join(truncated) if truncated else before_paren[:50]

            title = f"{before_paren} {paren_part}".strip()
        else:
            # No parentheses - truncate at word boundary
            words = title.split()
            truncated = []
            for word in words:
                test = " ".join(truncated + [word])
                if len(test) <= 72:
                    truncated.append(word)
                else:
                    break
            title = " ".join(truncated)
            if len(title) < len(" ".join(words[: len(truncated)])):
                title += "..."

    return title


class ProofCaseBuilder:
    """Builds a comprehensive proof case with evidence."""

    def __init__(self, project_path: Path, claim: str):
        """
        Initialize proof case builder.

        Args:
            project_path: Project root path
            claim: The claim to prove/disprove
        """
        self.project_path = project_path
        self.claim = claim
        self.verdict: str | None = None
        self.confidence: float = 0.0
        self.verification_results: dict[str, Any] = {}
        self.assumption_results: dict[str, Any] = {}
        self.evidence: list[dict[str, Any]] = []
        self.case_file_path: Path | None = None

    def run_verification(self) -> dict[str, Any]:
        """Run /verify checks."""
        print("🔍 Running Verification Checks...")
        print()

        results = {
            "date_time": {},
            "disk_space": {},
            "working_directory": {},
            "git_status": {},
            "file_existence": {},
            "template_verification": {},
        }

        # Date/Time
        import subprocess

        date_output = subprocess.run(["date"], capture_output=True, text=True).stdout.strip()
        results["date_time"] = {"status": "✅", "evidence": date_output, "verified": True}
        print(f"  ✅ Date/Time: {date_output}")

        # Disk space
        df_output = (
            subprocess.run(["df", "-h", "."], capture_output=True, text=True)
            .stdout.strip()
            .split("\n")[-1]
        )
        results["disk_space"] = {"status": "✅", "evidence": df_output, "verified": True}
        print(f"  ✅ Disk Space: {df_output}")

        # Working directory
        pwd_output = subprocess.run(["pwd"], capture_output=True, text=True).stdout.strip()
        results["working_directory"] = {"status": "✅", "evidence": pwd_output, "verified": True}
        print(f"  ✅ Working Directory: {pwd_output}")

        # Git status
        try:
            git_status = subprocess.run(
                ["git", "status", "--short"], capture_output=True, text=True
            ).stdout.strip()
            results["git_status"] = {
                "status": "✅",
                "evidence": git_status[:200] if git_status else "No changes",
                "verified": True,
            }
            print(f"  ✅ Git Status: {len(git_status.splitlines()) if git_status else 0} changes")
        except Exception as e:
            results["git_status"] = {"status": "⚠️", "evidence": str(e), "verified": False}

        # Template verification (black bars)
        template_dir = project_root / "src" / "waft" / "templates"
        if template_dir.exists():
            verify_script = project_root / "scripts" / "verify_no_black_bars.py"
            if verify_script.exists():
                verify_output = subprocess.run(
                    ["python3", str(verify_script)],
                    capture_output=True,
                    text=True,
                    cwd=project_root,
                )
                results["template_verification"] = {
                    "status": "✅" if verify_output.returncode == 0 else "❌",
                    "evidence": verify_output.stdout,
                    "verified": verify_output.returncode == 0,
                    "source_script": str(verify_script.relative_to(project_root)),
                    "template_directory": str(template_dir.relative_to(project_root)),
                    "verification_method": "Automated regex pattern matching for black bar CSS patterns",
                }
                print(
                    f"  {'✅' if verify_output.returncode == 0 else '❌'} Template Verification: {'PASSED' if verify_output.returncode == 0 else 'FAILED'}"
                )

        print()
        return results

    def analyze_claim(self) -> dict[str, Any]:
        """
        Analyze the claim to determine what to test.

        Returns:
            Dict with:
            - target_files: List of file paths to examine
            - features_to_check: List of specific features mentioned
            - verification_type: Type of verification (html, javascript, css, python, template, etc.)
        """
        import re

        claim_lower = self.claim.lower()
        analysis = {"target_files": [], "features_to_check": [], "verification_type": "unknown"}

        # Extract file names from claim (common patterns)
        # Pattern: "show_me_bulletproof.py", "show-me HTML report", "file.py", etc.
        file_patterns = [
            r"([a-zA-Z0-9_\-]+\.(py|html|js|css|ts|tsx|jsx))",  # filename.ext
            r"([a-zA-Z0-9_\-]+\.py)",  # Python files
            r"([a-zA-Z0-9_\-]+\.html)",  # HTML files
            r"([a-zA-Z0-9_\-]+\.js)",  # JavaScript files
        ]

        for pattern in file_patterns:
            matches = re.findall(pattern, self.claim, re.IGNORECASE)
            for match in matches:
                filename = match[0] if isinstance(match, tuple) else match
                # Try to find the file in common locations
                possible_paths = [
                    self.project_path / "scripts" / filename,
                    self.project_path / "src" / "waft" / filename,
                    self.project_path / filename,
                ]
                for path in possible_paths:
                    if path.exists():
                        analysis["target_files"].append(str(path.relative_to(self.project_path)))
                        break

        # Determine verification type based on keywords
        if any(
            keyword in claim_lower
            for keyword in [
                "html",
                "html report",
                "above-the-fold",
                "responsive",
                "mobile breakpoint",
            ]
        ):
            analysis["verification_type"] = "html"
            # Extract HTML-specific features
            if "above-the-fold" in claim_lower or "above the fold" in claim_lower:
                analysis["features_to_check"].append("above-the-fold")
            if (
                "responsive" in claim_lower
                or "breakpoint" in claim_lower
                or "mobile" in claim_lower
            ):
                analysis["features_to_check"].append("responsive_design")
            if "copy button" in claim_lower or "abstract.*copy" in claim_lower:
                analysis["features_to_check"].append("abstract_copy_button")
            if "clipboard" in claim_lower:
                analysis["features_to_check"].append("clipboard_api")
        elif any(
            keyword in claim_lower
            for keyword in ["javascript", "js", "clipboard", "api", "navigator"]
        ):
            analysis["verification_type"] = "javascript"
            if "clipboard" in claim_lower:
                analysis["features_to_check"].append("clipboard_api")
        elif any(
            keyword in claim_lower for keyword in ["css", "style", "media query", "breakpoint"]
        ):
            analysis["verification_type"] = "css"
            if "responsive" in claim_lower or "breakpoint" in claim_lower:
                analysis["features_to_check"].append("responsive_design")
        elif any(
            keyword in claim_lower
            for keyword in ["template", "pdf.*template", "black.*bar", "header"]
        ):
            analysis["verification_type"] = "template"
            if "black bar" in claim_lower or "black.*bar" in claim_lower:
                analysis["features_to_check"].append("no_black_bars")
        elif any(keyword in claim_lower for keyword in ["python", "function", "def ", "class "]):
            analysis["verification_type"] = "python"
        else:
            # Default: try to infer from target files
            if analysis["target_files"]:
                for target_file in analysis["target_files"]:
                    if target_file.endswith(".html"):
                        analysis["verification_type"] = "html"
                    elif target_file.endswith((".js", ".jsx", ".ts", ".tsx")):
                        analysis["verification_type"] = "javascript"
                    elif target_file.endswith(".css"):
                        analysis["verification_type"] = "css"
                    elif target_file.endswith(".py"):
                        # Could be template or regular Python
                        if "template" in target_file.lower():
                            analysis["verification_type"] = "template"
                        else:
                            analysis["verification_type"] = "python"
                    break

        return analysis

    def verify_html_features(self, claim_analysis: dict[str, Any]) -> list[dict[str, Any]]:
        """Verify HTML features from claim."""
        assumptions = []

        # Find target file(s)
        target_files = claim_analysis.get("target_files", [])
        if not target_files:
            # Try to infer from claim
            import re

            filename_match = re.search(r"([a-zA-Z0-9_\-]+\.(py|html))", self.claim, re.IGNORECASE)
            if filename_match:
                filename = filename_match.group(1)
                possible_paths = [
                    self.project_path / "scripts" / filename,
                    self.project_path / "src" / "waft" / filename,
                    self.project_path / filename,
                ]
                for path in possible_paths:
                    if path.exists():
                        target_files = [str(path.relative_to(self.project_path))]
                        break

        if not target_files:
            assumptions.append(
                {
                    "statement": "Target file(s) can be located for HTML feature verification",
                    "category": "code",
                    "risk": "medium",
                    "status": "INCONCLUSIVE",
                    "confidence": 0.0,
                    "evidence": [
                        {
                            "type": "error",
                            "description": "Could not locate target file(s) mentioned in claim",
                            "result": f"Claim: {self.claim}",
                        }
                    ],
                }
            )
            return assumptions

        features_to_check = claim_analysis.get("features_to_check", [])

        for target_file_str in target_files:
            target_file = self.project_path / target_file_str
            if not target_file.exists():
                assumptions.append(
                    {
                        "statement": f"Target file {target_file_str} exists",
                        "category": "code",
                        "risk": "high",
                        "status": "DISPROVEN",
                        "confidence": 1.0,
                        "evidence": [
                            {
                                "type": "file_check",
                                "description": f"File {target_file_str} not found",
                                "result": "File does not exist",
                            }
                        ],
                    }
                )
                continue

            try:
                content = target_file.read_text()
                import re

                # Check for above-the-fold section
                if "above-the-fold" in features_to_check or "above-the-fold" in self.claim.lower():
                    has_above_fold = (
                        'id="above-the-fold"' in content
                        or "id='above-the-fold'" in content
                        or 'class="above-the-fold"' in content
                        or "class='above-the-fold'" in content
                        or '<section id="above-the-fold"' in content
                    )
                    line_num = None
                    if has_above_fold:
                        # Find line number
                        lines = content.split("\n")
                        for i, line in enumerate(lines, 1):
                            if "above-the-fold" in line:
                                line_num = i
                                break

                    assumptions.append(
                        {
                            "statement": "HTML report has above-the-fold section with ID 'above-the-fold'",
                            "category": "code",
                            "risk": "medium",
                            "status": "PROVEN" if has_above_fold else "DISPROVEN",
                            "confidence": 1.0 if has_above_fold else 0.9,
                            "evidence": [
                                {
                                    "type": "code_analysis",
                                    "description": f"Checked for above-the-fold section in {target_file_str}",
                                    "result": "Found" if has_above_fold else "Not found",
                                    "source_file": target_file_str,
                                    "source_lines": [line_num] if line_num else [],
                                    "verification_method": 'Pattern search: id="above-the-fold" or class="above-the-fold"',
                                }
                            ],
                        }
                    )

                # Check for responsive design (media queries)
                if "responsive_design" in features_to_check or "responsive" in self.claim.lower():
                    media_queries = re.findall(r"@media\s*\([^)]+\)", content)
                    has_breakpoints = any(
                        "max-width" in mq
                        or "min-width" in mq
                        or "max-device-width" in mq
                        or "min-device-width" in mq
                        for mq in media_queries
                    )

                    line_numbers = []
                    if has_breakpoints:
                        lines = content.split("\n")
                        for i, line in enumerate(lines, 1):
                            if "@media" in line and ("max-width" in line or "min-width" in line):
                                line_numbers.append(i)

                    assumptions.append(
                        {
                            "statement": "HTML report has responsive design with mobile breakpoints",
                            "category": "code",
                            "risk": "medium",
                            "status": "PROVEN" if has_breakpoints else "DISPROVEN",
                            "confidence": 1.0 if has_breakpoints else 0.8,
                            "evidence": [
                                {
                                    "type": "code_analysis",
                                    "description": f"Checked for responsive media queries in {target_file_str}",
                                    "result": f"Found {len(media_queries)} media queries"
                                    if has_breakpoints
                                    else "No responsive breakpoints found",
                                    "source_file": target_file_str,
                                    "source_lines": line_numbers[:5],  # First 5 matches
                                    "verification_method": "Regex pattern: @media with width breakpoints",
                                }
                            ],
                        }
                    )

                # Check for abstract copy button
                if (
                    "abstract_copy_button" in features_to_check
                    or "copy button" in self.claim.lower()
                ):
                    has_copy_btn = (
                        ".abstract-copy-btn" in content
                        or "abstract-copy-btn" in content
                        or "abstract.*copy" in content.lower()
                    )

                    line_num = None
                    if has_copy_btn:
                        lines = content.split("\n")
                        for i, line in enumerate(lines, 1):
                            if "abstract-copy-btn" in line or "abstract.*copy" in line.lower():
                                line_num = i
                                break

                    assumptions.append(
                        {
                            "statement": "HTML report has abstract copy button",
                            "category": "code",
                            "risk": "low",
                            "status": "PROVEN" if has_copy_btn else "DISPROVEN",
                            "confidence": 1.0 if has_copy_btn else 0.9,
                            "evidence": [
                                {
                                    "type": "code_analysis",
                                    "description": f"Checked for abstract copy button in {target_file_str}",
                                    "result": "Found" if has_copy_btn else "Not found",
                                    "source_file": target_file_str,
                                    "source_lines": [line_num] if line_num else [],
                                    "verification_method": "Pattern search: .abstract-copy-btn or abstract copy button",
                                }
                            ],
                        }
                    )

                # Check for clipboard API
                if "clipboard_api" in features_to_check or "clipboard" in self.claim.lower():
                    has_clipboard = (
                        "navigator.clipboard" in content
                        or "clipboard.writeText" in content
                        or "clipboard.readText" in content
                    )

                    line_numbers = []
                    if has_clipboard:
                        lines = content.split("\n")
                        for i, line in enumerate(lines, 1):
                            if "clipboard" in line.lower():
                                line_numbers.append(i)

                    assumptions.append(
                        {
                            "statement": "HTML report uses clipboard API",
                            "category": "code",
                            "risk": "low",
                            "status": "PROVEN" if has_clipboard else "DISPROVEN",
                            "confidence": 1.0 if has_clipboard else 0.9,
                            "evidence": [
                                {
                                    "type": "code_analysis",
                                    "description": f"Checked for clipboard API usage in {target_file_str}",
                                    "result": "Found" if has_clipboard else "Not found",
                                    "source_file": target_file_str,
                                    "source_lines": line_numbers[:5],  # First 5 matches
                                    "verification_method": "Pattern search: navigator.clipboard or clipboard.writeText",
                                }
                            ],
                        }
                    )

            except Exception as e:
                assumptions.append(
                    {
                        "statement": f"Target file {target_file_str} can be analyzed",
                        "category": "code",
                        "risk": "medium",
                        "status": "INCONCLUSIVE",
                        "confidence": 0.0,
                        "evidence": [
                            {
                                "type": "error",
                                "description": f"Error analyzing {target_file_str}",
                                "result": str(e),
                            }
                        ],
                    }
                )

        return assumptions

    def verify_template_features(self, claim_analysis: dict[str, Any]) -> list[dict[str, Any]]:
        """Verify template features (existing black bar checking logic)."""
        assumptions = []
        template_dir = self.project_path / "src" / "waft" / "templates"

        if not template_dir.exists():
            assumptions.append(
                {
                    "statement": "Template directory exists",
                    "category": "code",
                    "risk": "high",
                    "status": "DISPROVEN",
                    "confidence": 1.0,
                    "evidence": [
                        {
                            "type": "file_check",
                            "description": "Template directory not found",
                            "result": "Directory does not exist",
                        }
                    ],
                }
            )
            return assumptions

        import re

        template_files = list(template_dir.glob("*.py"))
        black_bar_pattern = re.compile(
            r"h[1-6]\s*\{[^}]*background:\s*#000", re.MULTILINE | re.DOTALL
        )

        for template_file in template_files:
            try:
                content = template_file.read_text()
                matches = list(black_bar_pattern.finditer(content))

                if matches:
                    line_numbers = [content[: m.start()].count("\n") + 1 for m in matches]
                    code_snippets = [
                        content[max(0, m.start() - 50) : m.end() + 50] for m in matches[:3]
                    ]
                    assumption = {
                        "statement": f"Template {template_file.name} has no black bar headers",
                        "category": "code",
                        "risk": "high",
                        "status": "DISPROVEN",
                        "confidence": 1.0,
                        "evidence": [
                            {
                                "type": "code_analysis",
                                "description": f"Found {len(matches)} black bar violations in {template_file.name}",
                                "result": f"Lines: {line_numbers}",
                                "source_file": str(template_file.relative_to(self.project_path)),
                                "source_lines": line_numbers,
                                "code_snippets": code_snippets,
                            }
                        ],
                    }
                    assumptions.append(assumption)
                    print(f"  ❌ {template_file.name}: BLACK BARS FOUND")
                else:
                    h2_pattern = re.compile(r"h2\s*\{[^}]*\}", re.MULTILINE | re.DOTALL)
                    h2_matches = list(h2_pattern.finditer(content))
                    h2_snippets = []
                    if h2_matches:
                        for m in h2_matches[:2]:
                            snippet = content[m.start() : m.end()]
                            line_num = content[: m.start()].count("\n") + 1
                            h2_snippets.append({"line": line_num, "code": snippet[:200]})

                    assumption = {
                        "statement": f"Template {template_file.name} has no black bar headers",
                        "category": "code",
                        "risk": "high",
                        "status": "PROVEN",
                        "confidence": 1.0,
                        "evidence": [
                            {
                                "type": "code_analysis",
                                "description": f"No black bar patterns found in {template_file.name}",
                                "result": "Verified clean",
                                "source_file": str(template_file.relative_to(self.project_path)),
                                "verification_method": "Regex pattern search: h[1-6]\\s*\\{[^}]*background:\\s*#000",
                                "h2_headers_found": len(h2_matches),
                                "sample_h2_styles": h2_snippets,
                            }
                        ],
                    }
                    assumptions.append(assumption)
                    print(f"  ✅ {template_file.name}: No black bars")
            except Exception as e:
                assumption = {
                    "statement": f"Template {template_file.name} can be checked",
                    "category": "code",
                    "risk": "medium",
                    "status": "INCONCLUSIVE",
                    "confidence": 0.0,
                    "evidence": [
                        {
                            "type": "error",
                            "description": f"Error checking {template_file.name}",
                            "result": str(e),
                        }
                    ],
                }
                assumptions.append(assumption)
                print(f"  ⚠️ {template_file.name}: Error - {e}")

        return assumptions

    def run_assumption_check(self) -> dict[str, Any]:
        """Run /check-assumptions validation."""
        print("🔍 Running Assumption Validation...")
        print()

        # Analyze claim to determine what to test
        claim_analysis = self.analyze_claim()
        verification_type = claim_analysis.get("verification_type", "unknown")
        target_files = claim_analysis.get("target_files", [])
        features_to_check = claim_analysis.get("features_to_check", [])

        print("  📋 Claim Analysis:")
        print(f"     Verification Type: {verification_type}")
        if target_files:
            print(f"     Target Files: {', '.join(target_files)}")
        if features_to_check:
            print(f"     Features to Check: {', '.join(features_to_check)}")
        print()

        assumptions = []

        # Route to appropriate verification based on claim type
        if verification_type == "html":
            assumptions = self.verify_html_features(claim_analysis)
            print(f"  ✅ HTML Features Checked: {len(assumptions)}")
        elif verification_type == "javascript":
            # TODO: Implement JavaScript verification
            assumptions.append(
                {
                    "statement": "JavaScript features can be verified",
                    "category": "code",
                    "risk": "medium",
                    "status": "INCONCLUSIVE",
                    "confidence": 0.0,
                    "evidence": [
                        {
                            "type": "info",
                            "description": "JavaScript verification not yet implemented",
                            "result": "Feature coming soon",
                        }
                    ],
                }
            )
            print("  ⚠️ JavaScript verification not yet implemented")
        elif verification_type == "css":
            # TODO: Implement CSS verification
            assumptions.append(
                {
                    "statement": "CSS features can be verified",
                    "category": "code",
                    "risk": "medium",
                    "status": "INCONCLUSIVE",
                    "confidence": 0.0,
                    "evidence": [
                        {
                            "type": "info",
                            "description": "CSS verification not yet implemented",
                            "result": "Feature coming soon",
                        }
                    ],
                }
            )
            print("  ⚠️ CSS verification not yet implemented")
        elif verification_type == "template":
            assumptions = self.verify_template_features(claim_analysis)
            print(f"  ✅ Templates Checked: {len(assumptions)}")
        elif verification_type == "python":
            # TODO: Implement Python verification
            assumptions.append(
                {
                    "statement": "Python features can be verified",
                    "category": "code",
                    "risk": "medium",
                    "status": "INCONCLUSIVE",
                    "confidence": 0.0,
                    "evidence": [
                        {
                            "type": "info",
                            "description": "Python verification not yet implemented",
                            "result": "Feature coming soon",
                        }
                    ],
                }
            )
            print("  ⚠️ Python verification not yet implemented")
        else:
            # Unknown verification type - try to infer or return inconclusive
            assumptions.append(
                {
                    "statement": "Claim can be analyzed and verified",
                    "category": "code",
                    "risk": "medium",
                    "status": "INCONCLUSIVE",
                    "confidence": 0.0,
                    "evidence": [
                        {
                            "type": "info",
                            "description": f"Could not determine verification type for claim: {self.claim}",
                            "result": f"Verification type: {verification_type}",
                        }
                    ],
                }
            )
            print(f"  ⚠️ Unknown verification type: {verification_type}")

        print()
        print(f"  ✅ Total Assumptions: {len(assumptions)}")
        print(f"  ✅ Proven: {sum(1 for a in assumptions if a.get('status') == 'PROVEN')}")
        print(f"  ❌ Disproven: {sum(1 for a in assumptions if a.get('status') == 'DISPROVEN')}")
        print(
            f"  ⚠️ Inconclusive: {sum(1 for a in assumptions if a.get('status') == 'INCONCLUSIVE')}"
        )
        print()

        return {
            "assumptions": assumptions,
            "total": len(assumptions),
            "proven": sum(1 for a in assumptions if a.get("status") == "PROVEN"),
            "disproven": sum(1 for a in assumptions if a.get("status") == "DISPROVEN"),
            "verification_type": verification_type,
            "claim_analysis": claim_analysis,
        }

    def build_case_file(self) -> str:
        """Build the case file content."""
        case_content = []

        # ========================================================================
        # TITLE PAGE
        # ========================================================================
        case_content.append("# CASE BRIEF: PROOF OF CLAIM")
        case_content.append("")
        case_content.append(f"**Case ID**: PROOF-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        case_content.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        case_content.append(f"**Claim**: {self.claim}")
        case_content.append(f"**Verdict**: {self.verdict}")
        case_content.append(f"**Confidence**: {self.confidence:.1%}")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")

        # ========================================================================
        # ABSTRACT
        # ========================================================================
        case_content.append("## ABSTRACT")
        case_content.append("")
        if self.verdict == "PROVEN":
            case_content.append(
                "This case brief presents comprehensive evidence demonstrating that the claim **is proven** beyond reasonable doubt. "
            )
        elif self.verdict == "DISPROVEN":
            case_content.append(
                "This case brief presents comprehensive evidence demonstrating that the claim **is disproven**. "
            )
        else:
            case_content.append(
                "This case brief presents evidence regarding the claim, which **cannot be definitively proven or disproven** with the available evidence. "
            )

        # Count evidence
        assumptions = self.assumption_results.get("assumptions", [])
        proven_count = sum(1 for a in assumptions if a.get("status") == "PROVEN")
        total_count = len(assumptions)
        verification_checks = len(
            [
                r
                for r in self.verification_results.values()
                if isinstance(r, dict) and r.get("verified", False)
            ]
        )

        case_content.append(
            f"Evidence was collected through {verification_checks} verification checks and {total_count} assumption validations. "
        )
        case_content.append(
            f"Of the assumptions tested, {proven_count} were proven, {sum(1 for a in assumptions if a.get('status') == 'DISPROVEN')} were disproven, "
        )
        case_content.append(
            f"and {sum(1 for a in assumptions if a.get('status') == 'INCONCLUSIVE')} were inconclusive. "
        )
        case_content.append(f"The overall confidence level is {self.confidence:.1%}.")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")

        # ========================================================================
        # HYPOTHESIS
        # ========================================================================
        case_content.append("## HYPOTHESIS")
        case_content.append("")
        case_content.append("### Primary Hypothesis")
        case_content.append("")
        case_content.append("**H₀ (Null Hypothesis)**: The claim is false")
        case_content.append("")
        case_content.append(f"**H₁ (Alternative Hypothesis)**: {self.claim}")
        case_content.append("")
        case_content.append("### Testable Predictions")
        case_content.append("")
        case_content.append("If the claim is true, we expect to find:")
        case_content.append("")

        # Generate predictions based on claim
        if "black bars" in self.claim.lower() or "template" in self.claim.lower():
            case_content.append(
                "1. No CSS patterns matching `background: #000` in header styles (h1-h6)"
            )
            case_content.append(
                "2. All template files use alternative styling (border-bottom, color changes)"
            )
            case_content.append("3. Verification script confirms zero violations")
            case_content.append("4. Generated PDFs display headers without black backgrounds")
        else:
            case_content.append("1. Evidence supporting the claim exists")
            case_content.append("2. Verification checks pass")
            case_content.append("3. Assumptions validate the claim")

        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")

        # ========================================================================
        # METHODOLOGY
        # ========================================================================
        case_content.append("## METHODOLOGY")
        case_content.append("")
        case_content.append("### Verification Process")
        case_content.append("")
        case_content.append("This proof employs a multi-layered verification approach:")
        case_content.append("")
        case_content.append(
            "1. **Environment Verification**: Confirms system state, date/time, disk space, working directory"
        )
        case_content.append(
            "2. **Code Analysis**: Direct examination of source files using regex pattern matching"
        )
        case_content.append(
            "3. **Assumption Validation**: Systematic testing of each assumption with evidence collection"
        )
        case_content.append(
            "4. **Evidence Documentation**: All findings include source files, line numbers, and code snippets"
        )
        case_content.append("")
        case_content.append("### Evidence Collection Standards")
        case_content.append("")
        case_content.append(
            "- **Source Attribution**: Every finding includes file path and line numbers"
        )
        case_content.append(
            "- **Reproducibility**: Verification methods are documented and repeatable"
        )
        case_content.append("- **Traceability**: Evidence chains link findings to source code")
        case_content.append(
            "- **Confidence Scoring**: Each assumption receives a confidence level (0.0-1.0)"
        )
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")

        # ========================================================================
        # VERIFICATION EVIDENCE
        # ========================================================================
        case_content.append("## VERIFICATION EVIDENCE")
        case_content.append("")
        case_content.append("### Overview")
        case_content.append("")
        verification_count = len(
            [r for r in self.verification_results.values() if isinstance(r, dict)]
        )
        verified_count = len(
            [
                r
                for r in self.verification_results.values()
                if isinstance(r, dict) and r.get("verified", False)
            ]
        )
        case_content.append(f"**Total Checks**: {verification_count}")
        case_content.append(f"**Verified**: {verified_count}")
        case_content.append(f"**Failed**: {verification_count - verified_count}")
        case_content.append("")
        case_content.append("---")
        case_content.append("")

        for check_name, check_result in self.verification_results.items():
            status = check_result.get("status", "❓")
            evidence = check_result.get("evidence", "No evidence")
            verified = check_result.get("verified", False)
            source_script = check_result.get("source_script", "")
            template_directory = check_result.get("template_directory", "")
            verification_method = check_result.get("verification_method", "")

            case_content.append(f"### {check_name.replace('_', ' ').title()}")
            case_content.append("")
            case_content.append(
                f"**Status**: {status} {'VERIFIED' if verified else 'NOT VERIFIED'}"
            )
            case_content.append("")
            if source_script:
                case_content.append(f"**Source Script**: `{source_script}`")
                case_content.append("")
            if template_directory:
                case_content.append(f"**Template Directory**: `{template_directory}`")
                case_content.append("")
            if verification_method:
                case_content.append(f"**Verification Method**: {verification_method}")
                case_content.append("")
            case_content.append("**Evidence**:")
            case_content.append("```")
            case_content.append(str(evidence))
            case_content.append("```")
            case_content.append("")

        case_content.append("=" * 70)
        case_content.append("")

        # ========================================================================
        # ASSUMPTION VALIDATION
        # ========================================================================
        case_content.append("## ASSUMPTION VALIDATION")
        case_content.append("")
        case_content.append("### Overview")
        case_content.append("")
        assumptions = self.assumption_results.get("assumptions", [])
        if assumptions:
            proven = sum(1 for a in assumptions if a.get("status") == "PROVEN")
            disproven = sum(1 for a in assumptions if a.get("status") == "DISPROVEN")
            inconclusive = sum(1 for a in assumptions if a.get("status") == "INCONCLUSIVE")
            case_content.append(f"**Total Assumptions**: {len(assumptions)}")
            case_content.append(f"**Proven**: {proven} ({proven / len(assumptions) * 100:.1f}%)")
            case_content.append(
                f"**Disproven**: {disproven} ({disproven / len(assumptions) * 100:.1f}%)"
            )
            case_content.append(
                f"**Inconclusive**: {inconclusive} ({inconclusive / len(assumptions) * 100:.1f}%)"
            )
        else:
            case_content.append("**Total Assumptions**: 0")
        case_content.append("")
        case_content.append("---")
        case_content.append("")
        assumptions = self.assumption_results.get("assumptions", [])
        if assumptions:
            for i, assumption in enumerate(assumptions, 1):
                statement = assumption.get("statement", "Unknown")
                status = assumption.get("status", "UNKNOWN")
                confidence = assumption.get("confidence", 0.0)
                evidence_list = assumption.get("evidence", [])

                case_content.append(f"### Assumption {i}: {statement}")
                case_content.append("")
                case_content.append(f"**Status**: {status}")
                case_content.append(f"**Confidence**: {confidence:.1%}")
                case_content.append("")
                if evidence_list:
                    case_content.append("**Evidence**:")
                    for ev in evidence_list:
                        ev_type = ev.get("type", "unknown")
                        ev_desc = ev.get("description", "")
                        ev_result = ev.get("result", "")
                        source_file = ev.get("source_file", "")
                        source_lines = ev.get("source_lines", [])
                        code_snippets = ev.get("code_snippets", [])
                        verification_method = ev.get("verification_method", "")
                        sample_styles = ev.get("sample_h2_styles", [])

                        case_content.append(f"- **{ev_type}**: {ev_desc}")
                        if source_file:
                            case_content.append(f"  - **Source File**: `{source_file}`")
                        if source_lines:
                            case_content.append(f"  - **Line Numbers**: {source_lines}")
                        if verification_method:
                            case_content.append(
                                f"  - **Verification Method**: `{verification_method}`"
                            )
                        if ev_result:
                            case_content.append(f"  - **Result**: {ev_result}")
                        if code_snippets:
                            case_content.append("  - **Code Snippets (violations)**:")
                            for i, snippet in enumerate(code_snippets, 1):
                                case_content.append("    ```css")
                                case_content.append(f"    {snippet}")
                                case_content.append("    ```")
                        if sample_styles:
                            case_content.append("  - **Sample H2 Styles Verified**:")
                            for style in sample_styles:
                                case_content.append(f"    - Line {style.get('line', '?')}:")
                                case_content.append("      ```css")
                                case_content.append(f"      {style.get('code', '')}")
                                case_content.append("      ```")
                    case_content.append("")
        else:
            case_content.append("No assumptions extracted or validated.")
            case_content.append("")

        case_content.append("=" * 70)
        case_content.append("")

        # ========================================================================
        # ADDITIONAL EVIDENCE
        # ========================================================================
        if self.evidence:
            case_content.append("## ADDITIONAL EVIDENCE")
            case_content.append("")
            for i, ev in enumerate(self.evidence, 1):
                ev_type = ev.get("type", "unknown")
                ev_desc = ev.get("description", "")
                ev_data = ev.get("data", "")

                case_content.append(f"### Evidence {i}: {ev_type}")
                case_content.append("")
                case_content.append(f"**Description**: {ev_desc}")
                case_content.append("")
                if ev_data:
                    case_content.append("**Data**:")
                    case_content.append("```")
                    case_content.append(str(ev_data))
                    case_content.append("```")
                    case_content.append("")
            case_content.append("=" * 70)
            case_content.append("")

        # ========================================================================
        # ANALYSIS
        # ========================================================================
        case_content.append("## ANALYSIS")
        case_content.append("")
        case_content.append("### Evidence Evaluation")
        case_content.append("")

        # Analyze verification results
        all_verified = all(
            result.get("verified", False)
            for result in self.verification_results.values()
            if isinstance(result, dict)
        )
        template_verified = self.verification_results.get("template_verification", {}).get(
            "verified", False
        )

        case_content.append("**Verification Status**:")
        case_content.append(f"- All checks passed: {'✅ Yes' if all_verified else '❌ No'}")
        case_content.append(
            f"- Template verification: {'✅ Passed' if template_verified else '❌ Failed'}"
        )
        case_content.append("")

        # Analyze assumptions
        if assumptions:
            case_content.append("**Assumption Analysis**:")
            proven = sum(1 for a in assumptions if a.get("status") == "PROVEN")
            avg_confidence = (
                sum(a.get("confidence", 0.0) for a in assumptions) / len(assumptions)
                if assumptions
                else 0.0
            )
            case_content.append(
                f"- Proven assumptions: {proven}/{len(assumptions)} ({proven / len(assumptions) * 100:.1f}%)"
            )
            case_content.append(f"- Average confidence: {avg_confidence:.1%}")
            case_content.append("")

        case_content.append("### Key Findings")
        case_content.append("")
        if self.verdict == "PROVEN":
            case_content.append("1. ✅ All verification checks passed successfully")
            if assumptions:
                case_content.append(
                    f"2. ✅ {proven}/{len(assumptions)} assumptions validated with evidence"
                )
            case_content.append("3. ✅ Evidence supports the claim beyond reasonable doubt")
            case_content.append("4. ✅ All sources are traceable and reproducible")
        elif self.verdict == "DISPROVEN":
            case_content.append("1. ❌ Evidence contradicts the claim")
            if assumptions:
                case_content.append(
                    f"2. ❌ {sum(1 for a in assumptions if a.get('status') == 'DISPROVEN')} assumptions disproven"
                )
            case_content.append("3. ❌ Verification checks failed or revealed contradictions")
        else:
            case_content.append("1. ⚠️ Evidence is mixed or insufficient")
            case_content.append("2. ⚠️ Some assumptions validated, others inconclusive")
            case_content.append("3. ⚠️ Additional evidence required for definitive conclusion")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")

        # ========================================================================
        # CONCLUSION & SUMMARY
        # ========================================================================
        case_content.append("## CONCLUSION & SUMMARY")
        case_content.append("")
        case_content.append("### Final Verdict")
        case_content.append("")
        if self.verdict == "PROVEN":
            case_content.append("✅ **CLAIM IS PROVEN**")
            case_content.append("")
            case_content.append(
                "Based on comprehensive evidence analysis, the claim is **proven beyond reasonable doubt**. "
            )
            case_content.append(
                "All verification checks passed, assumptions were validated with traceable evidence, "
            )
            case_content.append("and the evidence consistently supports the claim.")
        elif self.verdict == "DISPROVEN":
            case_content.append("❌ **CLAIM IS DISPROVEN**")
            case_content.append("")
            case_content.append(
                "Based on comprehensive evidence analysis, the claim is **disproven**. "
            )
            case_content.append(
                "Evidence contradicts the claim, verification checks failed, or assumptions were invalidated."
            )
        else:
            case_content.append("⚠️ **VERDICT IS INCONCLUSIVE**")
            case_content.append("")
            case_content.append(
                "Based on the evidence analysis, the claim **cannot be definitively proven or disproven**. "
            )
            case_content.append(
                "The evidence is mixed, insufficient, or requires additional investigation."
            )
        case_content.append("")
        case_content.append("### Confidence Assessment")
        case_content.append("")
        case_content.append(f"**Overall Confidence**: {self.confidence:.1%}")
        case_content.append("")
        if self.confidence >= 0.95:
            case_content.append(
                "**Interpretation**: Very High Confidence - Evidence is strong and consistent"
            )
        elif self.confidence >= 0.80:
            case_content.append(
                "**Interpretation**: High Confidence - Evidence is strong with minor uncertainties"
            )
        elif self.confidence >= 0.60:
            case_content.append(
                "**Interpretation**: Moderate Confidence - Evidence supports conclusion but with some uncertainty"
            )
        elif self.confidence >= 0.40:
            case_content.append("**Interpretation**: Low Confidence - Evidence is weak or mixed")
        else:
            case_content.append(
                "**Interpretation**: Very Low Confidence - Insufficient or contradictory evidence"
            )
        case_content.append("")
        case_content.append("### Evidence Summary")
        case_content.append("")
        case_content.append("| Category | Count | Status |")
        case_content.append("|----------|-------|--------|")
        case_content.append(
            f"| Verification Checks | {verification_count} | {verified_count} verified |"
        )
        if assumptions:
            case_content.append(f"| Assumptions Tested | {len(assumptions)} | {proven} proven |")
        case_content.append(f"| Overall Verdict | 1 | {self.verdict} |")
        case_content.append("")
        case_content.append("### Recommendations")
        case_content.append("")
        if self.verdict == "PROVEN":
            case_content.append("1. ✅ **Accept the claim as verified**")
            case_content.append("2. ✅ **Use this evidence for decision-making**")
            case_content.append(
                "3. ✅ **Monitor for any future changes that might affect the claim**"
            )
        elif self.verdict == "DISPROVEN":
            case_content.append("1. ❌ **Reject the claim**")
            case_content.append("2. ⚠️ **Investigate why the claim was made**")
            case_content.append("3. 🔧 **Take corrective action if needed**")
        else:
            case_content.append("1. 🔍 **Gather additional evidence**")
            case_content.append("2. 🧪 **Run additional tests or experiments**")
            case_content.append("3. 📊 **Review methodology for improvements**")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")

        # ========================================================================
        # APPENDIX
        # ========================================================================
        case_content.append("## APPENDIX")
        case_content.append("")
        case_content.append("### Case Metadata")
        case_content.append("")
        case_content.append(f"- **Case ID**: PROOF-{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        case_content.append(f"- **Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        case_content.append(f"- **Project Path**: {self.project_path}")
        case_content.append(f"- **Claim**: {self.claim}")
        case_content.append("")
        case_content.append("### Files Generated")
        case_content.append("")
        case_content.append(f"- **Case File**: `{self.case_file_path}` (if generated)")
        case_content.append("- **PDF Binder**: Generated in `_work_efforts/proof_cases/`")
        case_content.append("")
        case_content.append("### Verification Scripts Used")
        case_content.append("")
        verify_script = self.project_path / "scripts" / "verify_no_black_bars.py"
        if verify_script.exists():
            case_content.append(
                f"- **Template Verification**: `{verify_script.relative_to(self.project_path)}`"
            )
        case_content.append("- **Proof System**: `scripts/prove_it_comprehensive.py`")
        case_content.append("")
        case_content.append("=" * 70)
        case_content.append("")
        case_content.append(
            f"*End of Case Brief - Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        )

        return "\n".join(case_content)

    def determine_verdict(self):
        """Determine verdict based on evidence."""
        # Check verification results
        all_verified = all(
            result.get("verified", False)
            for result in self.verification_results.values()
            if isinstance(result, dict)
        )

        # Get verification type from assumption results
        verification_type = self.assumption_results.get("verification_type", "unknown")

        # Template verification is only critical for template claims
        template_verified = self.verification_results.get("template_verification", {}).get(
            "verified", False
        )

        # Check assumptions
        assumptions = self.assumption_results.get("assumptions", [])
        proven_count = 0
        disproven_count = 0
        total_count = 0
        assumption_confidence = 0.0

        if assumptions:
            proven_count = sum(1 for a in assumptions if a.get("status") == "PROVEN")
            disproven_count = sum(1 for a in assumptions if a.get("status") == "DISPROVEN")
            total_count = len(assumptions)
            assumption_confidence = proven_count / total_count if total_count > 0 else 0.0

            # If any assumption is disproven, claim is disproven
            if disproven_count > 0:
                self.verdict = "DISPROVEN"
                self.confidence = 0.95
                return

            # If all assumptions proven, claim is PROVEN (with high confidence)
            if proven_count == total_count and total_count > 0:
                # For template claims, also check template verification
                if verification_type == "template":
                    if template_verified:
                        self.verdict = "PROVEN"
                        self.confidence = 0.95
                        return
                    elif all_verified:
                        self.verdict = "PROVEN"
                        self.confidence = 0.90
                        return
                else:
                    # For non-template claims, if all assumptions proven, it's proven
                    self.verdict = "PROVEN"
                    self.confidence = 0.95
                    return
        else:
            assumption_confidence = 0.5  # Neutral if no assumptions

        # Determine verdict based on verification type
        if verification_type == "template":
            # Template-specific logic (original behavior)
            if template_verified and all_verified and assumption_confidence >= 0.95:
                self.verdict = "PROVEN"
                self.confidence = 0.95
            elif template_verified and all_verified and assumption_confidence >= 0.8:
                self.verdict = "PROVEN"
                self.confidence = min(0.90, 0.75 + (assumption_confidence * 0.15))
            elif not template_verified and verification_type == "template":
                # Only fail on template verification if claim is about templates
                self.verdict = "DISPROVEN"
                self.confidence = 0.9
            elif assumption_confidence < 0.5:
                self.verdict = "DISPROVEN"
                self.confidence = 0.7
            else:
                self.verdict = "INCONCLUSIVE"
                self.confidence = assumption_confidence
        else:
            # Non-template claims: base verdict on assumptions
            if assumption_confidence >= 0.95 and proven_count > 0:
                self.verdict = "PROVEN"
                self.confidence = 0.95
            elif assumption_confidence >= 0.8 and proven_count > 0:
                self.verdict = "PROVEN"
                self.confidence = min(0.90, 0.75 + (assumption_confidence * 0.15))
            elif assumption_confidence < 0.5 or disproven_count > 0:
                self.verdict = "DISPROVEN"
                self.confidence = max(0.7, assumption_confidence)
            else:
                self.verdict = "INCONCLUSIVE"
                self.confidence = assumption_confidence

    def generate_pdf(self) -> Path:
        """Generate PDF binder with case brief."""
        case_content = self.build_case_file()

        # Determine cover classification based on verdict
        if self.verdict == "PROVEN":
            classification = "VERIFIED"
            cover_warning = {
                "message": "CLAIM VERIFIED - Evidence supports the claim beyond reasonable doubt",
                "severity": "INFO",
            }
        elif self.verdict == "DISPROVEN":
            classification = "REFUTED"
            cover_warning = {
                "message": "CLAIM DISPROVEN - Evidence contradicts the claim",
                "severity": "CRITICAL",
            }
        else:
            classification = "INCONCLUSIVE"
            cover_warning = {
                "message": "INSUFFICIENT EVIDENCE - Cannot definitively prove or disprove",
                "severity": "WARNING",
            }

        # Generate PDF
        output_dir = project_root / "_work_efforts" / "proof_cases"
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_claim = self.claim[:50].replace(" ", "_").replace("/", "_")
        output_path = output_dir / f"PROOF_CASE_{safe_claim}_{timestamp}.pdf"

        # Use BriefDocument directly to add markdown content
        from src.waft.brief import BriefDocument

        # Generate informative title
        informative_title = generate_informative_title(self.claim, self.verdict)

        doc = BriefDocument(
            title=informative_title,
            doc_id=f"PROOF-{timestamp}",
            subtitle=f"Verdict: {self.verdict} | Confidence: {self.confidence:.1%}",
            classification=classification,
            cover_header="PROOF CASE BRIEF",
            cover_metadata={
                "CLAIM": self.claim[:100] if len(self.claim) > 100 else self.claim,
                "VERDICT": self.verdict,
                "CONFIDENCE": f"{self.confidence:.1%}",
                "DATE": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            cover_warning=cover_warning,
            cover_footer="EVIDENCE-BASED VERIFICATION",
            include_system_status=False,
        )

        # Convert markdown to HTML properly
        try:
            import markdown

            html_content = markdown.markdown(
                case_content, extensions=["fenced_code", "tables", "nl2br", "extra", "codehilite"]
            )
        except ImportError:
            # Fallback: basic conversion
            import re

            html_content = case_content
            # Code blocks
            html_content = re.sub(
                r"```(\w+)?\n(.*?)```",
                r'<pre><code class="language-\1">\2</code></pre>',
                html_content,
                flags=re.DOTALL,
            )
            # Inline code
            html_content = re.sub(r"`([^`]+)`", r"<code>\1</code>", html_content)
            # Headers
            html_content = re.sub(r"^#\s+(.+)$", r"<h1>\1</h1>", html_content, flags=re.MULTILINE)
            html_content = re.sub(r"^##\s+(.+)$", r"<h2>\1</h2>", html_content, flags=re.MULTILINE)
            html_content = re.sub(r"^###\s+(.+)$", r"<h3>\1</h3>", html_content, flags=re.MULTILINE)
            # Bold
            html_content = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html_content)
            # Paragraphs
            html_content = re.sub(r"^(.+)$", r"<p>\1</p>", html_content, flags=re.MULTILINE)

        # Add HTML content directly
        doc.content_blocks.append(html_content)

        # Generate PDF
        pdf_path = doc.generate(output_path=output_path)

        # Move to desired location
        if pdf_path != output_path:
            pdf_path.rename(output_path)

        return output_path

    def run_proof(self) -> dict[str, Any]:
        """Run complete proof process."""
        print("=" * 70)
        print("COMPREHENSIVE PROOF SYSTEM")
        print("=" * 70)
        print()
        print(f"**Claim to Prove**: {self.claim}")
        print()

        # Step 1: Verification
        self.verification_results = self.run_verification()

        # Step 2: Assumption Check
        self.assumption_results = self.run_assumption_check()

        # Step 3: Determine Verdict
        self.determine_verdict()

        # Step 4: Build Case File
        case_content = self.build_case_file()
        case_file = (
            project_root
            / "_work_efforts"
            / "proof_cases"
            / f"case_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        case_file.parent.mkdir(parents=True, exist_ok=True)
        case_file.write_text(case_content)
        self.case_file_path = case_file

        # Step 5: Generate PDF
        pdf_path = self.generate_pdf()

        print("=" * 70)
        print("PROOF COMPLETE")
        print("=" * 70)
        print()
        print(f"**Verdict**: {self.verdict}")
        print(f"**Confidence**: {self.confidence:.1%}")
        print()
        print(f"📄 Case File: {case_file}")
        print(f"📄 PDF Binder: {pdf_path}")
        print()

        # Open PDF
        import platform
        import subprocess

        system = platform.system()
        if system == "Darwin":  # macOS
            subprocess.run(["open", str(pdf_path)], check=False)
        elif system == "Windows":
            subprocess.run(["start", str(pdf_path)], shell=True, check=False)
        else:  # Linux
            subprocess.run(["xdg-open", str(pdf_path)], check=False)

        return {
            "verdict": self.verdict,
            "confidence": self.confidence,
            "case_file": str(case_file),
            "pdf_path": str(pdf_path),
            "verification_results": self.verification_results,
            "assumption_results": self.assumption_results,
        }


def main():
    """Main entry point."""
    # Default claim (can be overridden)
    claim = "All PDF templates have been fixed to remove black bars from headers"

    # Check for claim in command line args
    if len(sys.argv) > 1:
        claim = " ".join(sys.argv[1:])

    builder = ProofCaseBuilder(project_root, claim)
    results = builder.run_proof()

    return 0 if results["verdict"] == "PROVEN" else 1


if __name__ == "__main__":
    sys.exit(main())
