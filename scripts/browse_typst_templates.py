#!/usr/bin/env python3
"""
Typst Template Browser
======================

Browse and explore official Typst templates from GitHub repository,
compare with existing WAFT wrappers, and generate a comprehensive report.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from template_metadata_extractor import extract_metadata, format_metadata_markdown, TemplateMetadata


@dataclass
class TemplateInfo:
    """Information about a template from GitHub."""
    name: str
    github_url: str
    readme_content: Optional[str] = None
    metadata: Optional[TemplateMetadata] = None
    has_wrapper: bool = False
    wrapper_path: Optional[str] = None


class TypstTemplateBrowser:
    """Browser for official Typst templates."""
    
    GITHUB_OWNER = "typst"
    GITHUB_REPO = "templates"
    GITHUB_BASE_URL = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}"
    
    def __init__(self, wrappers_dir: Optional[Path] = None):
        """
        Initialize the template browser.
        
        Args:
            wrappers_dir: Path to WAFT wrappers directory
        """
        if wrappers_dir is None:
            wrappers_dir = project_root / "src" / "waft" / "templates" / "typst" / "wrappers"
        self.wrappers_dir = wrappers_dir
        self.templates: Dict[str, TemplateInfo] = {}
    
    def fetch_templates_from_github(self) -> List[str]:
        """
        Fetch list of templates from GitHub repository.
        
        Returns:
            List of template directory names
        """
        try:
            # Use gh CLI to fetch repository contents
            result = subprocess.run(
                ["gh", "api", f"repos/{self.GITHUB_OWNER}/{self.GITHUB_REPO}/contents"],
                capture_output=True,
                text=True,
                check=True
            )
            
            contents = json.loads(result.stdout)
            templates = [
                item["name"]
                for item in contents
                if item["type"] == "dir" and not item["name"].startswith(".")
            ]
            
            return sorted(templates)
            
        except subprocess.CalledProcessError as e:
            print(f"Error fetching templates from GitHub: {e}", file=sys.stderr)
            print(f"stdout: {e.stdout}", file=sys.stderr)
            print(f"stderr: {e.stderr}", file=sys.stderr)
            # Fallback to known templates
            return [
                "appreciated-letter",
                "badformer",
                "cereal-words",
                "charged-ieee",
                "dashing-dept-news",
                "icicle",
                "unequivocal-ams",
                "wonderous-book",
            ]
        except FileNotFoundError:
            print("Warning: 'gh' CLI not found. Using fallback template list.", file=sys.stderr)
            return [
                "appreciated-letter",
                "badformer",
                "cereal-words",
                "charged-ieee",
                "dashing-dept-news",
                "icicle",
                "unequivocal-ams",
                "wonderous-book",
            ]
    
    def get_template_readme(self, template_name: str) -> Optional[str]:
        """
        Fetch README.md content for a template from GitHub.
        
        Args:
            template_name: Name of the template directory
            
        Returns:
            README content as string, or None if not found
        """
        try:
            result = subprocess.run(
                [
                    "gh", "api",
                    f"repos/{self.GITHUB_OWNER}/{self.GITHUB_REPO}/contents/{template_name}/README.md"
                ],
                capture_output=True,
                text=True,
                check=True
            )
            
            readme_data = json.loads(result.stdout)
            
            # Decode base64 content
            import base64
            content = base64.b64decode(readme_data["content"]).decode("utf-8")
            return content
            
        except subprocess.CalledProcessError:
            return None
        except FileNotFoundError:
            # Fallback: try to read from local cache if available
            return None
    
    def check_wrapper_exists(self, template_name: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a WAFT wrapper exists for the template.
        
        Args:
            template_name: Template name (e.g., "appreciated-letter")
            
        Returns:
            Tuple of (exists, wrapper_path)
        """
        # Convert template name to wrapper filename
        # e.g., "appreciated-letter" -> "appreciated_letter.py"
        wrapper_name = template_name.replace("-", "_") + ".py"
        wrapper_path = self.wrappers_dir / wrapper_name
        
        if wrapper_path.exists():
            return True, str(wrapper_path.relative_to(project_root))
        return False, None
    
    def compare_with_wrappers(self) -> Dict[str, TemplateInfo]:
        """
        Compare GitHub templates with existing WAFT wrappers.
        
        Returns:
            Dictionary mapping template names to TemplateInfo
        """
        template_names = self.fetch_templates_from_github()
        
        for template_name in template_names:
            # Fetch README
            readme_content = self.get_template_readme(template_name)
            
            # Extract metadata
            metadata = None
            if readme_content:
                metadata = extract_metadata(readme_content, template_name)
            
            # Check for wrapper
            has_wrapper, wrapper_path = self.check_wrapper_exists(template_name)
            
            # Create TemplateInfo
            template_info = TemplateInfo(
                name=template_name,
                github_url=f"{self.GITHUB_BASE_URL}/tree/main/{template_name}",
                readme_content=readme_content,
                metadata=metadata,
                has_wrapper=has_wrapper,
                wrapper_path=wrapper_path
            )
            
            self.templates[template_name] = template_info
        
        return self.templates
    
    def find_extra_wrappers(self) -> List[str]:
        """
        Find WAFT wrappers that don't correspond to official templates.
        
        Returns:
            List of wrapper filenames
        """
        if not self.wrappers_dir.exists():
            return []
        
        official_names = {name.replace("-", "_") for name in self.templates.keys()}
        extra_wrappers = []
        
        for wrapper_file in self.wrappers_dir.glob("*.py"):
            if wrapper_file.name in ["__init__.py"]:
                continue
            
            wrapper_base = wrapper_file.stem
            if wrapper_base not in official_names:
                extra_wrappers.append(wrapper_file.name)
        
        return sorted(extra_wrappers)
    
    def generate_report(self, output_path: Path) -> None:
        """
        Generate markdown report comparing templates and wrappers.
        
        Args:
            output_path: Path to write the report
        """
        # Compare templates
        self.compare_with_wrappers()
        
        # Find extra wrappers
        extra_wrappers = self.find_extra_wrappers()
        
        # Generate report
        lines = [
            "# Official Typst Templates Browser Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Source:** [{self.GITHUB_BASE_URL}]({self.GITHUB_BASE_URL})",
            "",
            "## Overview",
            "",
            f"This report compares the {len(self.templates)} official Typst templates with existing WAFT wrappers.",
            "",
            "## Template Status Summary",
            "",
            "| Template | Status | Wrapper | Description |",
            "|----------|--------|---------|-------------|",
        ]
        
        # Add template rows
        for template_name in sorted(self.templates.keys()):
            template = self.templates[template_name]
            status = "✅ Wrapped" if template.has_wrapper else "❌ Missing"
            wrapper_col = f"[{Path(template.wrapper_path).name}]({template.wrapper_path})" if template.wrapper_path else "-"
            description = template.metadata.description if template.metadata else "No description available"
            # Truncate description for table
            if len(description) > 60:
                description = description[:57] + "..."
            
            lines.append(
                f"| [{template_name}]({template.github_url}) | {status} | {wrapper_col} | {description} |"
            )
        
        lines.extend([
            "",
            "## Detailed Template Information",
            "",
        ])
        
        # Add detailed info for each template
        for template_name in sorted(self.templates.keys()):
            template = self.templates[template_name]
            
            lines.extend([
                f"### {template_name}",
                "",
                f"**GitHub:** [{template.github_url}]({template.github_url})",
                "",
            ])
            
            if template.has_wrapper:
                lines.extend([
                    f"**WAFT Wrapper:** ✅ [{template.wrapper_path}]({template.wrapper_path})",
                    "",
                ])
            else:
                lines.extend([
                    "**WAFT Wrapper:** ❌ Not yet implemented",
                    "",
                ])
            
            if template.metadata:
                # Format metadata but skip the title (already shown above)
                metadata_lines = format_metadata_markdown(template.metadata).split("\n")
                # Skip first two lines (title and empty line)
                lines.extend(metadata_lines[2:])
            elif template.readme_content:
                # Fallback: show raw README
                lines.extend([
                    "**Description:**",
                    template.readme_content[:500] + "..." if len(template.readme_content) > 500 else template.readme_content,
                    "",
                ])
            else:
                lines.extend([
                    "**Description:** No README available",
                    "",
                ])
            
            lines.append("---")
            lines.append("")
        
        # Add extra wrappers section
        if extra_wrappers:
            lines.extend([
                "## Additional WAFT Wrappers",
                "",
                "The following wrappers exist in WAFT but are not part of the official Typst templates repository:",
                "",
            ])
            
            for wrapper in extra_wrappers:
                wrapper_path = self.wrappers_dir / wrapper
                rel_path = wrapper_path.relative_to(project_root)
                lines.append(f"- [{wrapper}]({rel_path})")
            
            lines.append("")
        
        # Add summary statistics
        wrapped_count = sum(1 for t in self.templates.values() if t.has_wrapper)
        missing_count = len(self.templates) - wrapped_count
        
        lines.extend([
            "## Summary Statistics",
            "",
            f"- **Total Official Templates:** {len(self.templates)}",
            f"- **Wrapped Templates:** {wrapped_count} ({wrapped_count/len(self.templates)*100:.1f}%)",
            f"- **Missing Wrappers:** {missing_count}",
            f"- **Additional WAFT Wrappers:** {len(extra_wrappers)}",
            "",
            "## Notes",
            "",
            "- This report is generated automatically by `scripts/browse_typst_templates.py`",
            "- Official templates are maintained by the Typst team at https://github.com/typst/templates",
            "- WAFT wrappers provide Python interfaces to these templates",
            "- Additional wrappers may be custom templates or community templates",
            "",
        ])
        
        # Write report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"✅ Report generated: {output_path}")


def main():
    """Main entry point."""
    browser = TypstTemplateBrowser()
    
    # Generate report
    output_path = project_root / "docs" / "TYPST_TEMPLATES_BROWSER_REPORT.md"
    browser.generate_report(output_path)
    
    # Print summary
    wrapped = sum(1 for t in browser.templates.values() if t.has_wrapper)
    total = len(browser.templates)
    print(f"\n📊 Summary: {wrapped}/{total} templates have wrappers ({wrapped/total*100:.1f}%)")


if __name__ == "__main__":
    main()
