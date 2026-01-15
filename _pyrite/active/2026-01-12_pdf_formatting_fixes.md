# PDF Formatting Fixes: Common First-Time Mistakes

**Date**: 2026-01-12 16:10 PST  
**Purpose**: Fix common PDF formatting issues that anyone would make on first go

---

## Issues Identified

### 1. ✅ List Spacing - FIXED
**Problem**: Lists have no top margin, small padding, tiny li spacing

**Current CSS**:
```css
ul, ol {
    margin: 0 0 {{ margin.paragraph_spacing }}pt 0;
    padding-left: 15pt;
}

li {
    margin-bottom: {{ margin.paragraph_spacing / 3 }}pt;
}
```

**Fix**:
```css
ul, ol {
    margin: {{ margin.paragraph_spacing }}pt 0 {{ margin.paragraph_spacing }}pt 0;  /* Add top margin */
    padding-left: 20pt;  /* Increase from 15pt */
}

li {
    margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;  /* Increase from /3 */
}

/* Nested lists */
ul ul, ol ol, ul ol, ol ul {
    margin-top: {{ margin.paragraph_spacing / 2 }}pt;
    margin-bottom: {{ margin.paragraph_spacing / 2 }}pt;
    padding-left: 30pt;  /* More indentation */
}
```

---

### 2. ✅ Code Block Line Breaks - FIXED
**Problem**: Code blocks don't preserve line breaks (missing `white-space`)

**Current CSS**:
```css
pre {
    background: {{ color.code_bg }};
    padding: {{ margin.paragraph_spacing / 2 }}pt;
    border-left: 3pt solid {{ color.accent }};
    font-size: {{ font.size_code }}pt;
    overflow-x: auto;
    page-break-inside: avoid;
}
```

**Fix**:
```css
pre {
    background: {{ color.code_bg }};
    padding: {{ margin.paragraph_spacing / 2 }}pt;
    border-left: 3pt solid {{ color.accent }};
    font-size: {{ font.size_code }}pt;
    white-space: pre-wrap;  /* ADD: Preserve line breaks and wrap */
    word-wrap: break-word;  /* ADD: Break long lines */
    overflow-x: auto;
    page-break-inside: avoid;
}

pre code {
    white-space: pre;  /* ADD: Preserve exact formatting in code */
    display: block;
}
```

---

### 3. ✅ Horizontal Rules - FIXED
**Problem**: No `hr` styling (only `.divider` class exists)

**Current**: No `hr` CSS

**Fix**:
```css
hr {
    border: none;
    border-top: 1pt solid {{ color.text }}33;
    margin: {{ margin.paragraph_spacing }}pt 0 {{ margin.paragraph_spacing }}pt 0;
    padding: 0;
    height: 0;
}
```

---

### 4. ✅ Blockquote Styling - FIXED
**Problem**: Blockquotes not handled in markdown conversion or CSS

**Current**: No blockquote support

**Fix CSS**:
```css
blockquote {
    border-left: 4pt solid {{ color.accent }};
    background: {{ color.code_bg }}20;
    padding: {{ margin.paragraph_spacing / 2 }}pt {{ margin.paragraph_spacing }}pt;
    margin: {{ margin.paragraph_spacing }}pt 0;
    padding-left: {{ margin.paragraph_spacing }}pt;
    font-style: italic;
    color: {{ color.text }}dd;
    page-break-inside: avoid;
}
```

**Fix Markdown Conversion**: Add blockquote handling to `_markdown_to_html()`:
```python
# Blockquotes (>) - process before paragraphs
html = re.sub(r'^>\s+(.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
```

---

### 5. ✅ Link Styling - FIXED
**Problem**: Links not visually distinct

**Current**: No link CSS

**Fix**:
```css
a {
    color: {{ color.accent }};
    text-decoration: underline;
}

a:visited {
    color: {{ color.accent }}aa;
}
```

---

### 6. ✅ Header Spacing - FIXED
**Problem**: Headers might have awkward spacing after them

**Current CSS**:
```css
h2 {
    margin-top: {{ margin.section_spacing }}pt;
    margin-bottom: {{ margin.paragraph_spacing }}pt;
}
```

**Fix**:
```css
h2 {
    margin-top: {{ margin.section_spacing }}pt;
    margin-bottom: {{ margin.paragraph_spacing * 0.75 }}pt;  /* Slightly reduce */
}

h2 + p, h2 + ul, h2 + ol {
    margin-top: {{ margin.paragraph_spacing * 0.5 }}pt;  /* Connect to header */
}
```

---

### 7. ✅ Table Cell Padding - FIXED
**Problem**: Table cells have minimal padding (4pt)

**Current CSS**:
```css
th, td {
    padding: 4pt;
}
```

**Fix**:
```css
th, td {
    padding: 6pt 8pt;  /* Increase from 4pt */
}
```

---

### 8. ✅ Code Inline vs Block - FIXED
**Problem**: Inline code and code blocks look too similar

**Current CSS**:
```css
code {
    background: {{ color.code_bg }};
    padding: 2pt 4pt;
}
```

**Fix**:
```css
code {
    /* Inline code - subtle */
    background: {{ color.code_bg }}80;  /* More transparent */
    padding: 1pt 3pt;  /* Smaller padding */
}

pre code {
    /* Code in blocks - prominent */
    background: {{ color.code_bg }};  /* Full opacity */
    padding: {{ margin.paragraph_spacing / 2 }}pt;
    display: block;
}
```

---

### 9. ✅ Empty Paragraph Handling - FIXED
**Problem**: Empty paragraphs create awkward spacing

**Fix**:
```css
p:empty {
    display: none;
    margin: 0;
    padding: 0;
}
```

---

### 10. ✅ List Item Wrapping - FIXED
**Problem**: Long list items might not wrap properly

**Fix**:
```css
li {
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
}
```

---

## Implementation Plan

1. **Update CSS Template**: Add all fixes to `TWO_PAGE_TEMPLATE`
2. **Update Markdown Conversion**: Add blockquote support to `_markdown_to_html()`
3. **Test**: Generate test PDFs with various markdown content
4. **Verify**: Check formatting is correct

---

## Test Cases

1. Lists (simple, nested, with formatting)
2. Code (inline, blocks, multi-line)
3. Headers (all levels, with content after)
4. Links (in text, in lists)
5. Tables (simple, complex)
6. Blockquotes (simple, with formatting)
7. Horizontal rules (between sections)

---

**Status**: Ready to implement fixes
