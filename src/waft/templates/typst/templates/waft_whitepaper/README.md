# WAFT White Paper Template

A professional white paper template for WAFT publications, following Typst's template tutorial and inspired by academic paper templates from Typst Universe.

## Installation

```bash
typst init @preview/waft-whitepaper
```

Or use directly:

```typst
#import "@preview/waft-whitepaper:0.1.0": waft-whitepaper
```

## Usage

### Basic Usage

```typst
#import "@preview/waft-whitepaper:0.1.0": waft-whitepaper

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

### Design Philosophy
- **Toner-Friendly**: Minimal ink usage - no fills, thin borders only
- **High Text Density**: Optimized margins and spacing for maximum content
- **Professional**: Clean black & white design suitable for academic/technical publication
- **Feature-Packed**: Comprehensive styling for tables, figures, code, lists, quotes, footnotes

### Typography
- **Body**: Times New Roman, 10pt (dense, readable)
- **Headings**: Bold, numbered (1.1, 1.2, etc.), minimal spacing
- **Code**: Courier New, 8.5pt blocks with thin borders (no fills)
- **Compact**: Tight leading (0.15em) and spacing (0.5em) for maximum text

### Layout
- **Margins**: 0.75in top/bottom, 1in left/right (optimized for text area)
- **Headers**: Page numbers only (right-aligned, minimal)
- **Footers**: None (saves ink)
- **Title Page**: Centered, minimal spacing

### Elements
- **Tables**: Minimal borders (bottom only for cells, header underline)
- **Figures**: Numbered with italic captions
- **Code Blocks**: White background, thin black border, no rounded corners
- **Lists**: Compact spacing
- **Quotes**: Left border accent, no fill
- **Footnotes**: Compact numbering
- **Abstract**: Thin border box, no fill
- **TOC**: Depth 4, compact indentation

## Design Philosophy

This template follows Typst's template tutorial pattern and is inspired by:
- Academic paper templates from [daskol/typst-templates](https://github.com/daskol/typst-templates)
- General paper templates from [jxpeng98/Typst-Paper-Template](https://github.com/jxpeng98/Typst-Paper-Template)
- Typst's official template tutorial: https://typst.app/docs/tutorial/making-a-template/

## Examples

See the WAFT project for example usage:
- Example document: `_work_efforts/waft_status_whitepaper.typ`
- Generated PDF: `/tmp/waft_status_whitepaper.pdf`

## License

MIT License - See LICENSE file for details

## Contributing

This template is part of the WAFT (Wave Agent Framework & Tools) project. Contributions welcome!

## Links

- [WAFT Framework](https://github.com/ctavolazzi/waft)
- [Typst Documentation](https://typst.app/docs/)
- [Typst Universe](https://typst.app/universe/)
