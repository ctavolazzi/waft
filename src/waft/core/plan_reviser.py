"""
Plan Reviser - Revise plan markdown documents based on critiques.

Takes a plan and a critique, validates criticisms, and automatically
revises the plan markdown to address valid issues.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from .criticism_validator import CriticismValidator, ValidationResult, ValidationStatus
from .critique_parser import Criticism, CritiqueData
from .plan_loader import PlanData


@dataclass
class PlanRevision:
    """Represents a revision to be made to a plan."""

    criticism: Criticism
    validation: ValidationResult
    section_title: str  # Which section to add/update
    content: str  # Content to add
    action: str  # "add_section", "update_section", "add_todo", "update_todo"
    priority: int  # 1=CRITICAL, 2=HIGH, 3=MEDIUM, 4=LOW


@dataclass
class RevisionResult:
    """Result of revising a plan."""

    original_plan: PlanData
    revised_content: str
    revisions: list[PlanRevision]
    sections_added: list[str]
    sections_updated: list[str]
    todos_added: list[str]


class PlanReviser:
    """Revise plan markdown documents based on critiques."""

    def __init__(self, project_path: Path):
        """
        Initialize plan reviser.

        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.validator = CriticismValidator(project_path)

    def revise_plan(
        self,
        plan_data: PlanData,
        critique_data: CritiqueData,
        severity_filter: str | None = None,
        dry_run: bool = False,
    ) -> RevisionResult:
        """
        Revise plan based on critique.

        Args:
            plan_data: Plan data to revise
            critique_data: Critique data with criticisms
            severity_filter: Only revise this severity (CRITICAL, HIGH, etc.)
            dry_run: If True, don't apply revisions

        Returns:
            RevisionResult with revised plan
        """
        # Get criticisms to process
        all_criticisms = critique_data.get_all_criticisms()
        if severity_filter:
            all_criticisms = [c for c in all_criticisms if c.severity == severity_filter.upper()]

        # Validate criticisms
        validation_results = []
        for criticism in all_criticisms:
            validation = self._validate_plan_criticism(criticism, plan_data)
            validation_results.append(validation)

        # Generate revisions for valid criticisms
        revisions = []
        for criticism, validation in zip(all_criticisms, validation_results, strict=False):
            if validation.status in (ValidationStatus.VALID, ValidationStatus.PARTIALLY_VALID):
                plan_revisions = self._generate_revisions(criticism, validation, plan_data)
                revisions.extend(plan_revisions)

        # Sort revisions by priority
        revisions.sort(key=lambda r: r.priority)

        # Apply revisions to plan content
        revised_content = plan_data.content
        sections_added = []
        sections_updated = []
        todos_added = []

        if not dry_run:
            for revision in revisions:
                revised_content, added, updated, todos = self._apply_revision(
                    revised_content, revision, plan_data
                )
                if added:
                    sections_added.append(added)
                if updated:
                    sections_updated.append(updated)
                todos_added.extend(todos)

        return RevisionResult(
            original_plan=plan_data,
            revised_content=revised_content,
            revisions=revisions,
            sections_added=sections_added,
            sections_updated=sections_updated,
            todos_added=todos_added,
        )

    def _validate_plan_criticism(
        self, criticism: Criticism, plan_data: PlanData
    ) -> ValidationResult:
        """
        Validate a criticism against plan content.

        Args:
            criticism: Criticism to validate
            plan_data: Plan data to check against

        Returns:
            ValidationResult
        """
        result = ValidationResult(
            criticism=criticism, status=ValidationStatus.CANNOT_VERIFY, confidence=0.0
        )

        # Check if plan already addresses the issue
        issue_lower = criticism.issue.lower()
        plan_content_lower = plan_data.content.lower()

        # Check for security-related issues
        if "security" in issue_lower or "vulnerability" in issue_lower:
            if "security" in plan_content_lower or "security considerations" in plan_content_lower:
                # Check if specific issue is addressed
                if self._issue_addressed(criticism, plan_data):
                    result.status = ValidationStatus.INVALID
                    result.confidence = 0.7
                    result.conclusion = "Issue already addressed in plan"
                else:
                    result.status = ValidationStatus.VALID
                    result.confidence = 0.8
                    result.conclusion = "Security issue not addressed in plan"

        # Check for assumption-related issues
        elif "assumption" in issue_lower or "assumes" in issue_lower:
            if "assumption" in plan_content_lower:
                if self._issue_addressed(criticism, plan_data):
                    result.status = ValidationStatus.INVALID
                    result.confidence = 0.7
                else:
                    result.status = ValidationStatus.VALID
                    result.confidence = 0.8
            else:
                result.status = ValidationStatus.VALID
                result.confidence = 0.9
                result.conclusion = "No assumptions section in plan"

        # Check for error handling issues
        elif "error handling" in issue_lower or "try/except" in issue_lower:
            if "error handling" in plan_content_lower:
                if self._issue_addressed(criticism, plan_data):
                    result.status = ValidationStatus.INVALID
                    result.confidence = 0.7
                else:
                    result.status = ValidationStatus.VALID
                    result.confidence = 0.8
            else:
                result.status = ValidationStatus.VALID
                result.confidence = 0.9
                result.conclusion = "No error handling section in plan"

        # Check for testing issues
        elif "test" in issue_lower and ("missing" in issue_lower or "no" in issue_lower):
            if "test" in plan_content_lower and "strategy" in plan_content_lower:
                result.status = ValidationStatus.INVALID
                result.confidence = 0.7
            else:
                result.status = ValidationStatus.VALID
                result.confidence = 0.8
                result.conclusion = "No testing strategy in plan"

        # Generic check
        else:
            if self._issue_addressed(criticism, plan_data):
                result.status = ValidationStatus.INVALID
                result.confidence = 0.6
            else:
                result.status = ValidationStatus.VALID
                result.confidence = 0.7

        return result

    def _issue_addressed(self, criticism: Criticism, plan_data: PlanData) -> bool:
        """Check if a specific issue is already addressed in the plan."""
        issue_keywords = set(re.findall(r"\b\w+\b", criticism.issue.lower()))
        plan_keywords = set(re.findall(r"\b\w+\b", plan_data.content.lower()))

        # Check if significant keywords from issue appear in plan
        significant_keywords = issue_keywords - {
            "the",
            "a",
            "an",
            "is",
            "are",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
        }
        overlap = significant_keywords & plan_keywords

        # If more than 50% of significant keywords overlap, likely addressed
        if len(significant_keywords) > 0:
            overlap_ratio = len(overlap) / len(significant_keywords)
            return overlap_ratio > 0.5

        return False

    def _generate_revisions(
        self, criticism: Criticism, validation: ValidationResult, plan_data: PlanData
    ) -> list[PlanRevision]:
        """
        Generate revisions for a valid criticism.

        Args:
            criticism: Valid criticism
            validation: Validation result
            plan_data: Plan data

        Returns:
            List of PlanRevision objects
        """
        revisions = []

        # Determine priority
        priority_map = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
        priority = priority_map.get(criticism.severity, 3)

        # Generate revision based on criticism type
        issue_lower = criticism.issue.lower()

        # Security vulnerabilities
        if criticism.severity == "CRITICAL" and (
            "security" in issue_lower or "vulnerability" in issue_lower
        ):
            revision = self._create_security_revision(criticism, plan_data, priority)
            if revision:
                revisions.append(revision)

        # Assumptions
        elif "assumption" in issue_lower or "assumes" in issue_lower:
            revision = self._create_assumption_revision(criticism, plan_data, priority)
            if revision:
                revisions.append(revision)

        # Error handling
        elif "error handling" in issue_lower or "try/except" in issue_lower:
            revision = self._create_error_handling_revision(criticism, plan_data, priority)
            if revision:
                revisions.append(revision)

        # Testing
        elif "test" in issue_lower and ("missing" in issue_lower or "no" in issue_lower):
            revision = self._create_testing_revision(criticism, plan_data, priority)
            if revision:
                revisions.append(revision)

        # Overengineering
        elif "overengineering" in issue_lower or "unnecessary" in issue_lower:
            revision = self._create_overengineering_revision(criticism, plan_data, priority)
            if revision:
                revisions.append(revision)

        # Generic oversight
        else:
            revision = self._create_generic_revision(criticism, plan_data, priority)
            if revision:
                revisions.append(revision)

        return revisions

    def _create_security_revision(
        self, criticism: Criticism, plan_data: PlanData, priority: int
    ) -> PlanRevision | None:
        """Create revision for security vulnerability."""
        # Extract security concern from criticism
        issue = criticism.issue

        # Generate security content
        if "path" in issue.lower() and "validation" in issue.lower():
            content = """## Security Considerations

### Path Validation
- Validate all file paths before use
- Reject paths containing `..` (path traversal)
- Ensure paths are within project root
- Use `Path.resolve()` and validate against project root
"""
        elif "command injection" in issue.lower() or "subprocess" in issue.lower():
            content = """## Security Considerations

### Command Execution
- Never use `subprocess.run(shell=True)`
- Use list arguments: `subprocess.run([...], shell=False)`
- Validate and sanitize all inputs to subprocess calls
- Use `shlex.quote()` if shell is absolutely necessary
"""
        elif "permission" in issue.lower() or "chmod" in issue.lower():
            content = """## Security Considerations

### File Permissions
- Set restrictive file permissions (0600 for files, 0700 for directories)
- Validate registry location is within project
- Never store sensitive data in registry
- Add access control checks
"""
        else:
            content = f"""## Security Considerations

### {criticism.title}
{criticism.issue}

**Fix Required**: {criticism.fix_required or "See critique for details"}
"""

        return PlanRevision(
            criticism=criticism,
            validation=ValidationResult(
                criticism=criticism, status=ValidationStatus.VALID, confidence=0.8
            ),
            section_title="Security Considerations",
            content=content,
            action="add_section",
            priority=priority,
        )

    def _create_assumption_revision(
        self, criticism: Criticism, plan_data: PlanData, priority: int
    ) -> PlanRevision | None:
        """Create revision for unexamined assumption."""
        # Extract assumption from criticism
        issue = criticism.issue

        # Generate assumption content
        content = f"""## Assumptions

- {issue}
  - **Mitigation**: {criticism.fix_required or "Document and validate assumption"}
  - **Fallback**: Provide clear error message if assumption fails
"""

        return PlanRevision(
            criticism=criticism,
            validation=ValidationResult(
                criticism=criticism, status=ValidationStatus.VALID, confidence=0.8
            ),
            section_title="Assumptions",
            content=content,
            action="add_section",
            priority=priority,
        )

    def _create_error_handling_revision(
        self, criticism: Criticism, plan_data: PlanData, priority: int
    ) -> PlanRevision | None:
        """Create revision for missing error handling."""
        content = """## Error Handling

- File I/O: Wrap in try/except, handle PermissionError, IOError
- Network: Handle connection errors, timeouts
- Validation: Provide clear error messages for invalid input
- Logging: Log errors with context for debugging
"""

        return PlanRevision(
            criticism=criticism,
            validation=ValidationResult(
                criticism=criticism, status=ValidationStatus.VALID, confidence=0.8
            ),
            section_title="Error Handling",
            content=content,
            action="add_section",
            priority=priority,
        )

    def _create_testing_revision(
        self, criticism: Criticism, plan_data: PlanData, priority: int
    ) -> PlanRevision | None:
        """Create revision for missing testing strategy."""
        content = """## Testing Strategy

- Unit Tests: Test individual components
- Integration Tests: Test component interactions
- Security Tests: Test for vulnerabilities
- Error Handling Tests: Test error scenarios
"""

        return PlanRevision(
            criticism=criticism,
            validation=ValidationResult(
                criticism=criticism, status=ValidationStatus.VALID, confidence=0.8
            ),
            section_title="Testing Strategy",
            content=content,
            action="add_section",
            priority=priority,
        )

    def _create_overengineering_revision(
        self, criticism: Criticism, plan_data: PlanData, priority: int
    ) -> PlanRevision | None:
        """Create revision for overengineering concern."""
        content = f"""## Architecture Notes

### Overengineering Considerations
- {criticism.issue}
- **Suggestion**: Consider simplifying approach
- **Alternative**: {criticism.fix_required or "Evaluate simpler solution"}
"""

        return PlanRevision(
            criticism=criticism,
            validation=ValidationResult(
                criticism=criticism, status=ValidationStatus.VALID, confidence=0.7
            ),
            section_title="Architecture",
            content=content,
            action="update_section",
            priority=priority,
        )

    def _create_generic_revision(
        self, criticism: Criticism, plan_data: PlanData, priority: int
    ) -> PlanRevision | None:
        """Create generic revision for other issues."""
        # Determine appropriate section
        if criticism.severity in ("CRITICAL", "HIGH"):
            section_title = "Implementation"
            action = "update_section"
        else:
            section_title = "Risks and Mitigations"
            action = "add_section"

        content = f"""### {criticism.title}
{criticism.issue}

**Fix Required**: {criticism.fix_required or "See critique for details"}
"""

        return PlanRevision(
            criticism=criticism,
            validation=ValidationResult(
                criticism=criticism, status=ValidationStatus.VALID, confidence=0.7
            ),
            section_title=section_title,
            content=content,
            action=action,
            priority=priority,
        )

    def _apply_revision(
        self, content: str, revision: PlanRevision, plan_data: PlanData
    ) -> tuple[str, str | None, str | None, list[str]]:
        """
        Apply a revision to plan content.

        Args:
            content: Current plan content
            revision: Revision to apply
            plan_data: Original plan data

        Returns:
            Tuple of (revised_content, section_added, section_updated, todos_added)
        """
        section_added = None
        section_updated = None
        todos_added = []

        if revision.action == "add_section":
            # Check if section already exists
            if not plan_data.has_section(revision.section_title):
                # Add section after Overview or at end
                if plan_data.has_section("Overview"):
                    # Find Overview section and insert after it
                    overview_section = plan_data.get_section("Overview")
                    lines = content.split("\n")

                    # Find the end of Overview section (next heading or end of content)
                    insert_pos = min(overview_section.end_line + 1, len(lines))

                    # Insert new section
                    lines.insert(insert_pos, "")
                    lines.insert(insert_pos + 1, revision.content.strip())
                    content = "\n".join(lines)
                else:
                    # Add at end
                    content = content.rstrip() + "\n\n" + revision.content.strip()
                section_added = revision.section_title
            else:
                # Update existing section - append to it
                section = plan_data.get_section(revision.section_title)
                lines = content.split("\n")

                # Find insertion point (before next section or at end)
                insert_pos = min(section.end_line + 1, len(lines))

                # Insert content
                lines.insert(insert_pos, "")
                lines.insert(insert_pos + 1, revision.content.strip())
                content = "\n".join(lines)
                section_updated = revision.section_title

        elif revision.action == "update_section":
            if plan_data.has_section(revision.section_title):
                section = plan_data.get_section(revision.section_title)
                lines = content.split("\n")

                # Append to section
                insert_pos = min(section.end_line + 1, len(lines))
                lines.insert(insert_pos, "")
                lines.insert(insert_pos + 1, revision.content.strip())
                content = "\n".join(lines)
                section_updated = revision.section_title
            else:
                # Add as new section
                content = content.rstrip() + "\n\n" + revision.content.strip()
                section_added = revision.section_title

        # Add todo for critical/high issues
        if revision.priority <= 2:  # CRITICAL or HIGH
            todo_text = f"Address: {revision.criticism.title}"
            todos_added.append(todo_text)
            # Add todo to Todos section or create it
            if plan_data.has_section("Todos"):
                section = plan_data.get_section("Todos")
                lines = content.split("\n")
                insert_pos = min(section.end_line + 1, len(lines))
                lines.insert(insert_pos, f"- [ ] {todo_text}")
                content = "\n".join(lines)
            else:
                content = content.rstrip() + f"\n\n## Todos\n\n- [ ] {todo_text}"

        return content, section_added, section_updated, todos_added
