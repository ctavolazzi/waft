# WAFT Auto-Work Guide

A comprehensive Typst book documenting the WAFT Auto-Work feature.

## Quick Start

### Build HTML Book

```bash
cd book-auto-work-guide
shiroa serve
```

Then open http://localhost:25520 in your browser.

### Build PDF

```bash
cd book-auto-work-guide
typst compile src/book.typ output.pdf
```

## Structure

- `src/book.typ` - Main book configuration
- `src/chapters/` - Chapter files
- `assets/images/` - Screenshot placeholders

## Adding Screenshots

1. Place screenshots in `assets/images/`
2. Reference in chapters: `#image("assets/images/screenshot.png")`

## Chapters

1. Introduction
2. What is Auto-Work?
3. Key Features
4. System Architecture
5. Priority Scoring Algorithm
6. Work Effort Selection
7. Action Determination
8. Execution Phase
9. Empirica Integration
10. Pantheon Integration
11. Campfire Storytelling
12. D&D Campaign Integration
13. Safety Mechanisms
14. Basic Usage
15. Command Options
16. Step-by-Step Walkthrough
17. Usage Examples
18. Troubleshooting
19. Customization & Configuration
20. Best Practices
21. Future Enhancements
22. Conclusion

## Notes

- Screenshot placeholders are marked with `*[Screenshot Placeholder: ...]*`
- Replace these with actual `#image()` calls when screenshots are available
- All code examples are from actual Auto-Work execution
