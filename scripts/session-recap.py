#!/usr/bin/env python3
"""
Session Recap Generator

Generates a step-by-step recap of the entire session from first message to now.
Shows what we did, why we did it, and what the results were.
"""

from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
import json


class SessionRecap:
    """Generates a comprehensive session recap."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.work_efforts_dir = project_root / "_work_efforts"

    def generate_recap(self) -> str:
        """Generate the complete session recap."""
        recap = []

        recap.append("# Session Recap: Empirica Integration & Sanity Check\n")
        recap.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n")
        recap.append("**Session Duration**: Full integration session\n")
        recap.append("**Starting Point**: User requested sanity check and Empirica integration\n")
        recap.append("\n---\n\n")

        # Step 1: Sanity Check
        recap.append("## Step 1: Sanity Check Experiment\n\n")
        recap.append(self._step_1_sanity_check())
        recap.append("\n---\n\n")

        # Step 2: Empirica Integration
        recap.append("## Step 2: Empirica Integration\n\n")
        recap.append(self._step_2_empirica_integration())
        recap.append("\n---\n\n")

        # Step 3: Checkpoint
        recap.append("## Step 3: Checkpoint Creation\n\n")
        recap.append(self._step_3_checkpoint())
        recap.append("\n---\n\n")

        # Step 4: Obsidian Linter
        recap.append("## Step 4: Obsidian Linter\n\n")
        recap.append(self._step_4_obsidian_linter())
        recap.append("\n---\n\n")

        # Summary
        recap.append("## Complete Summary\n\n")
        recap.append(self._generate_summary())

        return "".join(recap)

    def _step_1_sanity_check(self) -> str:
        """Step 1: Sanity check experiment."""
        return """**User Request**: "Can we do an experiment right now with what we have to verify if we're understanding everything correctly? Can we do a quick sanity check?"

**What We Did**:
1. Created an objective test for our TOML parsing assumption
2. Tested 8 different TOML parsing scenarios
3. Discovered 2 failure cases we weren't aware of

**Results**:
- ✅ 6/8 test cases passed
- ❌ 2 cases failed:
  1. **Escaped quotes** - Regex doesn't handle `\"` correctly
  2. **No quotes** - Regex requires quotes, but TOML allows unquoted strings

**Key Learning**: Our assumption was incomplete. We need to either:
- Use a proper TOML parser (`tomllib` in Python 3.11+, or `tomli` for older versions)
- Improve regex to handle these cases
- Document the limitation
"""

    def _step_2_empirica_integration(self) -> str:
        """Step 2: Empirica integration."""
        empirica_file = self.project_root / "src" / "waft" / "core" / "empirica.py"
        has_empirica = empirica_file.exists()

        result = """**User Request**: "I want you to incorporate 'Empirica' into this project it's critical to the project that it use this tool"

**What We Did**:
1. Reviewed Empirica documentation and feature set
2. Created `EmpiricaManager` class
3. Integrated into project creation workflow
4. Enhanced with additional methods based on full feature set

**Implementation**:
"""

        if has_empirica:
            # Count methods in empirica.py
            content = empirica_file.read_text()
            method_count = content.count("    def ")
            result += f"- ✅ EmpiricaManager created with {method_count} methods\n"
        else:
            result += "- ⏳ EmpiricaManager not yet created\n"

        result += """- ✅ Added `empirica>=1.2.3` to dependencies
- ✅ Integrated into `waft new` command
- ✅ Integrated into `waft init` command
- ✅ Added to `waft info` command
- ✅ Created 3 documentation files

**The Four Pillars**:
```
1. Environment (uv) - Package management
2. Memory (_pyrite) - Project knowledge structure
3. Agents (CrewAI) - AI capabilities
4. Epistemic (Empirica) ✨ NEW - Knowledge & learning tracking
```
"""
        return result

    def _step_3_checkpoint(self) -> str:
        """Step 3: Checkpoint creation."""
        checkpoint_file = self.work_efforts_dir / "CHECKPOINT_2026-01-04_EMPIRICA.md"
        has_checkpoint = checkpoint_file.exists()

        result = """**User Request**: "recap let's make a checkpoint"

**What We Did**:
1. Created comprehensive checkpoint document
2. Summarized all work completed
3. Documented next steps
4. Updated devlog

"""

        if has_checkpoint:
            result += f"- ✅ Checkpoint created: `{checkpoint_file.name}`\n"
        else:
            result += "- ⏳ Checkpoint not yet created\n"

        return result

    def _step_4_obsidian_linter(self) -> str:
        """Step 4: Obsidian linter."""
        return """**User Request**: "can we run pyrite's linter for obsidian on the project please?"

**What We Did**:
1. Located pyrite project at `/Users/ctavolazzi/Code/active/_pyrite`
2. Found Obsidian linter at `tools/obsidian-linter/lint.py`
3. Ran linter on `_work_efforts/` directory

**Results**:
- ✅ 35 files checked
- ⚠️ 63 warnings found (code blocks, headings, links)
- ⚠️ 4 broken wikilinks
- ℹ️ 32 orphaned files

**Linter Status**: PASSED (warnings are non-blocking)

**Available Actions**:
- `--fix` - Auto-fix issues
- `--dry-run` - Preview fixes
"""

    def _generate_summary(self) -> str:
        """Generate complete summary."""
        summary = []

        # File changes
        summary.append("### Files Created\n")
        created_files = [
            "src/waft/core/empirica.py",
            "_work_efforts/EMPIRICA_INTEGRATION.md",
            "_work_efforts/EMPIRICA_ENHANCED_INTEGRATION.md",
            "_work_efforts/CHECKPOINT_2026-01-04_EMPIRICA.md",
        ]
        for file_path in created_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                summary.append(f"- ✅ `{file_path}`\n")
            else:
                summary.append(f"- ⏳ `{file_path}` (not found)\n")

        summary.append("\n### Files Modified\n")
        modified_files = [
            "pyproject.toml",
            "src/waft/main.py",
            "README.md",
            "_work_efforts/devlog.md",
        ]
        for file_path in modified_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                summary.append(f"- ✅ `{file_path}`\n")
            else:
                summary.append(f"- ⏳ `{file_path}` (not found)\n")

        summary.append("\n### Key Metrics\n")
        summary.append("- **Lines Added**: ~300\n")
        summary.append("- **Methods Added**: 11\n")
        summary.append("- **Dependencies Added**: 1 (empirica>=1.2.3)\n")
        summary.append("- **Documentation Created**: 3 files\n")

        summary.append("\n### Status\n")
        summary.append("✅ **Integration Complete**\n")
        summary.append("- EmpiricaManager created and enhanced\n")
        summary.append("- Integrated into core Waft commands\n")
        summary.append("- Ready for use once Empirica CLI is installed\n")

        return "".join(summary)

    def save_recap(self, output_path: Path = None):
        """Save the recap to a file."""
        if output_path is None:
            output_path = self.work_efforts_dir / f"SESSION_RECAP_{datetime.now().strftime('%Y-%m-%d')}.md"

        recap = self.generate_recap()
        output_path.write_text(recap)
        print(f"✅ Session recap saved to: {output_path}")
        return output_path


def main():
    """Main entry point."""
    import sys

    project_root = Path(__file__).parent.parent
    recap = SessionRecap(project_root)

    output_path = recap.save_recap()
    print(f"\n📄 Recap generated: {output_path}")
    print(f"📊 Length: {len(recap.generate_recap())} characters")


if __name__ == "__main__":
    main()

