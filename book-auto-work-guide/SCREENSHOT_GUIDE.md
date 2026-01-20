# Screenshot Guide for Auto-Work Documentation

This guide explains where to add screenshots in the Auto-Work documentation.

## Screenshot Locations

### Chapter 16: Step-by-Step Walkthrough

This chapter has the most screenshot placeholders:

1. **Step 1: Command Execution** - Terminal showing `/auto-work` command
2. **Step 2: System Initialization** - System initialization output
3. **Step 3: Work Effort Collection** - Work effort collection output
4. **Step 4: Priority Scoring** - Priority scoring output
5. **Step 5: Work Effort Selection** - Selected work effort details
6. **Step 6: Action Analysis** - Action analysis output
7. **Step 7: Action Selection** - Selected action details
8. **Step 8: Safety Gates** - Safety gate results
9. **Step 9: Execution Preparation** - Execution preparation output
10. **Step 10: JSON Output** - JSON output display
11. **Step 11: Execution Instruction** - Execution instruction display
12. **Step 12: AI Execution** - AI execution in progress
13. **Step 13: Storytelling** - Story generation output
14. **Step 14: Quest Generation** - Quest PDF generation
15. **Complete Example Output** - Complete terminal output

### Chapter 17: Usage Examples

Each example has a screenshot placeholder:

1. **Example 1: Simple Execution** - Basic execution output
2. **Example 2: Dry Run** - Dry run output
3. **Example 3: With Empirica and Pantheon** - Full integration output
4. **Example 4: Safety Gate Halt** - Safety halt output
5. **Example 5: No Actionable Work Efforts** - No actionable output
6. **Example 6: Verbose Mode** - Verbose output
7. **Example 7: Multiple Work Efforts** - Priority comparison

### Chapter 14: Basic Usage

1. **Dry Run Output** - Dry run example
2. **Verbose Output** - Verbose example
3. **Complete Basic Example** - Full basic example

## How to Add Screenshots

1. **Take Screenshots**: Capture terminal output or UI screenshots
2. **Save to Assets**: Place in `assets/images/` directory
3. **Name Files**: Use descriptive names like `step-1-command-execution.png`
4. **Update Chapters**: Replace placeholders with:

```typst
#image("assets/images/step-1-command-execution.png", width: 80%)
```

## Screenshot Specifications

- **Format**: PNG or JPEG
- **Width**: 80% of page width (use `width: 80%` parameter)
- **Quality**: High resolution for readability
- **Content**: Clear, focused on relevant output

## Example Replacement

**Before** (placeholder):
```typst
*[Screenshot Placeholder: Terminal showing command execution]*
```

**After** (with screenshot):
```typst
#image("assets/images/step-1-command-execution.png", width: 80%)

*Terminal showing `/auto-work` command execution*
```

## Priority Screenshots

Most important screenshots to add first:

1. Complete example output (Chapter 16)
2. Basic usage example (Chapter 14)
3. Dry run example (Chapter 17, Example 2)
4. Full integration example (Chapter 17, Example 3)
5. Safety gate halt (Chapter 17, Example 4)

## Notes

- Screenshots should match the example output in the text
- Use consistent styling (terminal theme, font size)
- Crop to show only relevant content
- Add captions when helpful
