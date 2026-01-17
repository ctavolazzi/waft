# Formal WAFT Letter PDF Template

## Overview

A professional LaTeX template for generating formal business letters with WAFT branding. The template supports complete letter formatting including letterhead, recipient/sender information, signature blocks, and professional typography.

## Decision: LaTeX vs ConTeXt vs Typst

After evaluating the three options:

- **LaTeX**: Chosen for this implementation
  - Most established and widely used
  - Existing LaTeX infrastructure in WAFT codebase
  - Better ecosystem support and package availability
  - User has existing LaTeX templates and knowledge

- **ConTeXt**: Good alternative but not chosen
  - Everything included, no packages needed
  - Consistent configuration syntax
  - Still based on TeX (similar architecture to LaTeX)
  - Less widely adopted

- **Typst**: Modern alternative but not chosen
  - Clean implementation, better syntax
  - Some basic features not yet implemented
  - Less mature ecosystem
  - Good for future consideration

## Features

- ✅ Professional letterhead with WAFT branding
- ✅ Complete recipient and sender information blocks
- ✅ Subject line support
- ✅ Customizable salutation and closing
- ✅ Markdown to LaTeX conversion for body content
- ✅ Signature block with title, organization, contact info
- ✅ Enclosures and CC notation
- ✅ Professional typography and spacing
- ✅ Auto-discovered by LaTeXTemplateRegistry

## Usage

### Basic Example

```python
from pathlib import Path
from src.waft.templates.latex.wrappers.formal_letter import generate_formal_letter

generate_formal_letter(
    title="Formal Letter Example",
    content="Your letter body content here. Supports **bold** and *italic* markdown.",
    output_path=Path("letter.pdf"),
    sender_name="Dr. Jane Smith",
    sender_title="Lead Developer",
    sender_organization="WAFT Framework",
    recipient_name="John Doe",
    recipient_organization="Example Corporation",
    subject="Re: WAFT Framework Integration",
    signature_name="Dr. Jane Smith",
    signature_title="Lead Developer"
)
```

### Full Example

See `example_usage.py` for a complete example with all options.

## Template Structure

The template follows standard business letter format:

1. **Letterhead** (optional, defaults to sender organization)
2. **Date** (right-aligned)
3. **Recipient Block** (left-aligned, includes name, title, organization, address)
4. **Subject Line** (optional)
5. **Salutation** (defaults to "Dear [recipient_name],")
6. **Body Content** (supports markdown: **bold**, *italic*)
7. **Closing** (defaults to "Sincerely,")
8. **Signature Block** (with name, title, organization, email, phone)
9. **Enclosures** (optional)
10. **CC** (optional)

## Parameters

### Required
- `title`: Document title (for PDF metadata)
- `content`: Letter body content (markdown supported)
- `output_path`: Path to save PDF

### Sender Information
- `sender_name`: Sender's name
- `sender_title`: Sender's title/position
- `sender_organization`: Sender's organization
- `sender_address`: Sender's street address
- `sender_city_state_zip`: Sender's city, state, zip
- `sender_email`: Sender's email
- `sender_phone`: Sender's phone

### Recipient Information
- `recipient_name`: Recipient's name
- `recipient_title`: Recipient's title/position
- `recipient_organization`: Recipient's organization
- `recipient_address`: Recipient's street address
- `recipient_city_state_zip`: Recipient's city, state, zip

### Letter Content
- `date`: Letter date (defaults to current date)
- `subject`: Subject line
- `salutation`: Salutation (defaults to "Dear [recipient_name],")
- `closing`: Closing (defaults to "Sincerely,")

### Signature
- `signature_name`: Name for signature block (defaults to sender_name)
- `signature_title`: Title for signature block
- `signature_organization`: Organization for signature block
- `signature_email`: Email for signature block
- `signature_phone`: Phone for signature block

### Additional
- `letterhead`: Letterhead text (defaults to sender_organization)
- `enclosures`: List of enclosures
- `cc`: List of CC recipients

## Markdown Support

The body content supports basic markdown:
- `**bold**` → **bold text**
- `*italic*` → *italic text*
- Paragraphs (double newline)

## Integration

The template is auto-discovered by `LaTeXTemplateRegistry` and can be used via:

```python
from src.waft.templates.latex.registry import get_latex_registry

registry = get_latex_registry()
template = registry.get_template("formal_letter")
generate_func = registry.get_generate_function("formal_letter")
```

## Files

- `src/waft/templates/latex/wrappers/formal_letter.py` - Main template wrapper
- `example_usage.py` - Usage examples

## Testing

To test the template:

```bash
cd _work_efforts/WE-260116-xkhg_formal_waft_letter_pdf_template_latex_context_typst
python example_usage.py
```

This will generate `example_letter.pdf` in the current directory.

## Future Enhancements

Potential improvements:
- [ ] Support for ConTeXt and Typst versions
- [ ] More advanced markdown features (lists, links, etc.)
- [ ] Custom letterhead graphics/logo support
- [ ] Multiple signature blocks
- [ ] Letter templates for different purposes (cover letter, recommendation, etc.)
