"""
Template Library CLI
====================

Command-line interface for discovering and managing PDF templates.
"""

import argparse
import json
from pathlib import Path

from .registry import TemplateMetadata, get_registry


def format_template_info(template: TemplateMetadata, detailed: bool = False) -> str:
    """Format template information for display."""
    lines = [f"📄 {template.name}"]
    lines.append(f"   Module: {template.module_name}")
    lines.append(f"   Category: {template.category}")
    lines.append(f"   Description: {template.description}")

    if template.tags:
        lines.append(f"   Tags: {', '.join(template.tags)}")

    if detailed:
        if template.generate_function:
            lines.append(f"   Generate Function: {template.generate_function}()")
        if template.template_constant:
            lines.append(f"   Template Constant: {template.template_constant}")
        if template.parameters:
            lines.append("   Parameters:")
            for param_name, param_info in template.parameters.items():
                req = "required" if param_info.get("required") else "optional"
                default = param_info.get("default")
                default_str = f" (default: {default})" if default is not None else ""
                lines.append(f"     - {param_name}: {req}{default_str}")
        lines.append(f"   Status: {template.status}")

    return "\n".join(lines)


def cmd_list(args) -> None:
    """List all templates."""
    registry = get_registry()
    templates = registry.list_templates(category=args.category, tag=args.tag)

    if not templates:
        print("No templates found.")
        return

    print(f"\n📚 Found {len(templates)} template(s):\n")
    for template in templates:
        print(format_template_info(template, detailed=args.detailed))
        print()


def cmd_show(args) -> None:
    """Show detailed information about a template."""
    registry = get_registry()
    template = registry.get_template(args.name)

    if not template:
        print(f"❌ Template '{args.name}' not found.")
        print("\nAvailable templates:")
        for t in registry.list_templates():
            print(f"  - {t.name} ({t.module_name})")
        return

    print(format_template_info(template, detailed=True))


def cmd_search(args) -> None:
    """Search templates."""
    registry = get_registry()
    results = registry.search(args.query)

    if not results:
        print(f"No templates found matching '{args.query}'")
        return

    print(f"\n🔍 Found {len(results)} template(s) matching '{args.query}':\n")
    for template in results:
        print(format_template_info(template))
        print()


def cmd_categories(args) -> None:
    """List all categories."""
    registry = get_registry()
    categories = registry.get_categories()

    print("\n📁 Categories:\n")
    for category in categories:
        count = len(registry.list_templates(category=category))
        print(f"  {category} ({count} template(s))")


def cmd_tags(args) -> None:
    """List all tags."""
    registry = get_registry()
    tags = registry.get_tags()

    print("\n🏷️  Tags:\n")
    for tag in tags:
        count = len(registry.list_templates(tag=tag))
        print(f"  {tag} ({count} template(s))")


def cmd_validate(args) -> None:
    """Validate templates."""
    from .validator import TemplateValidator

    registry = get_registry()
    validator = TemplateValidator()

    if args.name:
        template = registry.get_template(args.name)
        if not template:
            print(f"❌ Template '{args.name}' not found.")
            return
        templates = [template]
    else:
        templates = registry.list_templates()

    print(f"\n🔍 Validating {len(templates)} template(s)...\n")

    all_valid = True
    for template in templates:
        result = validator.validate(template)
        status = "✅" if result.is_valid else "❌"
        print(f"{status} {template.name}")
        if not result.is_valid:
            all_valid = False
            for error in result.errors:
                print(f"   ⚠️  {error}")
        print()

    if all_valid:
        print("✅ All templates are valid!")
    else:
        print("❌ Some templates have validation errors.")


def cmd_export(args) -> None:
    """Export template metadata to JSON."""
    registry = get_registry()
    templates = registry.list_templates()

    data = {
        "templates": [
            {
                "name": t.name,
                "module_name": t.module_name,
                "description": t.description,
                "category": t.category,
                "tags": t.tags,
                "generate_function": t.generate_function,
                "template_constant": t.template_constant,
                "parameters": t.parameters,
                "status": t.status,
            }
            for t in templates
        ]
    }

    output_path = Path(args.output) if args.output else Path("templates_metadata.json")
    output_path.write_text(json.dumps(data, indent=2))
    print(f"✅ Exported metadata to {output_path}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="WAFT PDF Template Library CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # List command
    list_parser = subparsers.add_parser("list", help="List all templates")
    list_parser.add_argument("--category", help="Filter by category")
    list_parser.add_argument("--tag", help="Filter by tag")
    list_parser.add_argument("--detailed", action="store_true", help="Show detailed information")
    list_parser.set_defaults(func=cmd_list)

    # Show command
    show_parser = subparsers.add_parser("show", help="Show template details")
    show_parser.add_argument("name", help="Template name")
    show_parser.set_defaults(func=cmd_show)

    # Search command
    search_parser = subparsers.add_parser("search", help="Search templates")
    search_parser.add_argument("query", help="Search query")
    search_parser.set_defaults(func=cmd_search)

    # Categories command
    categories_parser = subparsers.add_parser("categories", help="List all categories")
    categories_parser.set_defaults(func=cmd_categories)

    # Tags command
    tags_parser = subparsers.add_parser("tags", help="List all tags")
    tags_parser.set_defaults(func=cmd_tags)

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate templates")
    validate_parser.add_argument("--name", help="Validate specific template")
    validate_parser.set_defaults(func=cmd_validate)

    # Export command
    export_parser = subparsers.add_parser("export", help="Export metadata to JSON")
    export_parser.add_argument("--output", "-o", help="Output file path")
    export_parser.set_defaults(func=cmd_export)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
