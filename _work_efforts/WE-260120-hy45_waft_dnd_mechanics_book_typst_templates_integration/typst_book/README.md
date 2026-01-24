# WAFT DnD Mechanics Book (Typst)

This folder contains a shared WAFT DnD mechanics book body (`content.typ`) and four entry points that apply different Typst templates:

- `min-book.typ`
- `owlbear.typ`
- `dragonling.typ`
- `wenyuan-campaign.typ`

## Compile (CLI)

```bash
typst compile min-book.typ min-book.pdf
typst compile owlbear.typ owlbear.pdf
typst compile dragonling.typ dragonling.pdf
typst compile wenyuan-campaign.typ wenyuan-campaign.pdf
```

## Notes
- `wenyuan-campaign` requires external fonts if you want the default theme (see Typst package docs).
- `dragonling` uses `dndmodule` for the book layout.
- `owlbear` provides a print-friendly DnD homebrew aesthetic.
