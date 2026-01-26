# WAFT White Paper Template

A professional white paper template for WAFT publications, following Typst's template tutorial and inspired by academic paper templates.

## Usage

### Basic Usage

```typst
#import "src/waft/templates/typst/templates/waft_whitepaper.typ": waft-whitepaper

#show: doc => waft-whitepaper(
  title: "Your White Paper Title",
  subtitle: "Optional Subtitle",
  authors: (
    (
      name: "Author Name",
      affiliation: "Organization",
    ),
  ),
  date: datetime.today(),
  abstract: [
    Your abstract text here...
  ],
  keywords: ("keyword1", "keyword2", "keyword3"),
  doc,
)

= Introduction
Your content here...
```

### Template Parameters

- `title` (required): Main title of the white paper
- `subtitle` (optional): Subtitle text
- `authors` (optional): Array of author dictionaries with `name` and optional `affiliation`
- `date` (optional): Date object (defaults to today)
- `abstract` (optional): Abstract content
- `keywords` (optional): Array of keyword strings
- `doc`: Automatically provided by the `#show` rule

## Features

- Professional typography with New Computer Modern font
- Styled headings with WAFT branding colors
- Title page with centered layout
- Abstract section with styled box
- Table of contents (depth 3)
- Page headers and footers
- Code block styling
- Numbered sections and subsections

## Template Location

The template is located at:
`src/waft/templates/typst/templates/waft_whitepaper.typ`

## Example

See `_work_efforts/waft_status_whitepaper.typ` for a complete example using this template.
