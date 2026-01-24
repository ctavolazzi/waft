# WAFT Typst Border Standard

**Purpose**: All WAFT Typst templates should include the page border for quick and easy identification.

## Standard Border Pattern

All WAFT-generated Typst documents should include this border at the top:

```typst
#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

// WAFT template border for identification
#show: s6t5-page-bordering.with(
  margin: (left: 0.75in, right: 0.75in, top: 1in, bottom: 1in),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: none,
  stroke-footer: none,
  header: "",
  footer: "",
)
```

## Why This Border?

1. **Quick Identification**: Instantly recognize WAFT-generated documents
2. **Professional Appearance**: Clean, business-appropriate border
3. **Consistency**: All WAFT documents have the same visual signature
4. **Easy to Spot**: When browsing PDFs, WAFT documents stand out

## Implementation

### For New Templates

Always include the border import and show rule at the top of your Typst template:

```typst
#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

#show: s6t5-page-bordering.with(
  margin: (left: 0.75in, right: 0.75in, top: 1in, bottom: 1in),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: none,
  stroke-footer: none,
  header: "",
  footer: "",
)

// Your template code here
#set page(...)
#set text(...)
= Your Document
```

### For Python-Generated Typst Content

When generating Typst content from Python (e.g., in `Scribe.write_daily_learning_report()`), include the border at the start:

```python
typst_content = f"""#import "@preview/s6t5-page-bordering:1.0.0": s6t5-page-bordering

#show: s6t5-page-bordering.with(
  margin: (left: 1in, right: 1in, top: 1in, bottom: 1in),
  expand: 15pt,
  space-top: 15pt,
  space-bottom: 15pt,
  stroke-header: none,
  stroke-footer: none,
  header: "",
  footer: "",
)

#set text(...)
= Your Document
...
"""
```

## Customization

You can adjust margins and spacing as needed for your document type:

- **Standard**: `margin: (left: 0.75in, right: 0.75in, top: 1in, bottom: 1in)`
- **Wide margins**: `margin: (left: 1in, right: 1in, top: 1in, bottom: 1in)`
- **Narrow margins**: `margin: (left: 0.5in, right: 0.5in, top: 0.75in, bottom: 0.75in)`

The `expand`, `space-top`, and `space-bottom` parameters control the border spacing.

## Templates Updated

✅ `templates/typst/case_brief.typ` - Case file template  
✅ `src/waft/pantheon/library/scribe.py` - Daily learning report  
✅ `src/waft/core/daily_learning/report_generator.py` - Report generator  
✅ `src/waft/templates/typst/wrappers/odd_case_file.py` - Already had border

## Reference

- [s6t5-page-bordering Package](https://typst.app/universe/package/s6t5-page-bordering/)
- Border helper: `src/waft/templates/typst/border_helper.typ`
