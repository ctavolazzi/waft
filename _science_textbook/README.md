# Hypothesis Testing Framework - Science Textbook

This is a science textbook documenting the design and implementation of a hypothesis testing framework with iterative scientific method execution and real-time visualization.

## Building the Textbook

### Prerequisites

Install LaTeX and required packages:
- `texlive` (or equivalent LaTeX distribution)
- `latexmk`
- Required packages: `tikz`, `amsmath`, `listings`, `xcolor`, `hyperref`

### Build Commands

```bash
# Build both book-size and letter-size PDFs
make

# Build only book-size PDF (6" x 9")
make hypothesis-testing-framework.pdf

# Build only letter-size PDF (8.5" x 11")
make hypothesis-testing-framework-letter.pdf

# Clean generated files (keeps PDFs)
make commitclean

# Clean everything including PDFs
make clean
```

## Content Overview

This textbook documents:

1. **Introduction**: Problem statement and system requirements
2. **Existing Infrastructure**: Investigation of scientific method tool
3. **Consensus Algorithm Design**: Weighted confidence consensus mechanism
4. **System Architecture**: Backend, API, and frontend components
5. **Implementation Details**: Halt mechanism, WebSocket protocol, state management
6. **Real-Time Visualization**: UI layout and progress indicators
7. **Testing and Validation**: Test scenarios and validation criteria
8. **Conclusion**: Summary and future work

## Source

The content is derived from actual development conversations and codebase investigations conducted on 2026-01-14, documenting the design process for building a hypothesis testing framework with Electron UI and consensus mechanisms.

## License

Creative Commons Zero 1.0 Universal (CC0)
