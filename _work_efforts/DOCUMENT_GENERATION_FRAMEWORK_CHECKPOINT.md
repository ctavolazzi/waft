# Document Generation Framework - Design Checkpoint

**Date**: 2026-01-11  
**Goal**: Create a unified class system for on-the-fly document generation with creative design, no background graphics, and clear audience communication.

---

## 🔍 CURRENT STATE ANALYSIS

### Existing Classes with Document Generation Capabilities

#### 1. **ReflectionSystem** (`src/waft/reflection.py`)
**Capabilities:**
- ✅ Self-observation (scans codebase)
- ✅ Generates architecture docs
- ✅ Creates reflection reports
- ✅ Identifies documentation gaps
- ❌ Limited template options
- ❌ No audience targeting
- ❌ No design customization

**Key Methods:**
- `reflect()` - Observes codebase
- `generate_architecture_doc()` - Creates architecture PDF
- `generate_reflection_report_doc()` - Creates reflection PDF

#### 2. **DocumentBuilder** (`src/waft/document_builder.py`) ⭐ NEW
**Capabilities:**
- ✅ Unified API for document generation
- ✅ Fluent interface
- ✅ Printer-friendly support
- ✅ Collection/binder integration
- ❌ No self-awareness
- ❌ No audience targeting
- ❌ Limited design customization

**Key Methods:**
- `field_guide()` - Generate field guide
- `collection()` - Create document collections
- `save()` - Generate PDF

#### 3. **FrameworkAnalyzer** (`tools/framework_documentation/generate_framework_docs.py`)
**Capabilities:**
- ✅ AST-based code analysis
- ✅ Extracts module/class/function info
- ✅ Generates comprehensive docs
- ❌ Standalone script (not a class)
- ❌ No reusable API
- ❌ Hardcoded template

#### 4. **Binder** (`src/waft/binder.py`)
**Capabilities:**
- ✅ Combines multiple PDFs
- ✅ Creates covers, TOC, dividers
- ✅ Section organization
- ❌ Only combines, doesn't generate
- ❌ No content generation

---

## 🔄 REPETITION PATTERNS IDENTIFIED

### Pattern 1: Template Rendering
**Repetition:**
- Every generator manually calls `Template()` and `HTML().write_pdf()`
- Same Jinja2 rendering pattern repeated
- Same output path handling

**Compression Opportunity:**
```python
# REPEATED EVERYWHERE:
template = Template(template_str)
html_output = template.render(...)
HTML(string=html_output).write_pdf(output_path)
```

**Composable Unit:**
```python
class TemplateRenderer:
    def render(self, template_str, context, output_path):
        # Single implementation, reused everywhere
```

### Pattern 2: Content Structure
**Repetition:**
- Every doc has: title, content, metadata (series, number, date)
- Same cover page structure
- Same header/footer patterns

**Compression Opportunity:**
```python
# REPEATED:
title, subtitle, series, number, classification, date
```

**Composable Unit:**
```python
@dataclass
class DocumentMetadata:
    title: str
    subtitle: Optional[str]
    series: str
    number: str
    # ... all metadata in one place
```

### Pattern 3: Printer-Friendly Conversion
**Repetition:**
- Separate functions for printer-friendly versions
- Duplicate template definitions
- Manual CSS conversion

**Compression Opportunity:**
```python
# REPEATED:
if printer_friendly:
    template_str = convert_html_template_to_printer_friendly(template_str)
```

**Composable Unit:**
```python
class TemplateAdapter:
    def adapt_for_printing(self, template_str) -> str:
        # Automatic conversion
```

### Pattern 4: Audience Targeting
**Repetition:**
- Manual content adaptation for different audiences
- No systematic approach
- Content duplicated across levels

**Compression Opportunity:**
```python
# REPEATED:
level_1_content = "Simple explanations..."
level_2_content = "Technical details..."
level_3_content = "Research depth..."
```

**Composable Unit:**
```python
class AudienceAdapter:
    def adapt_content(self, base_content, audience_level):
        # Transform content for audience
```

### Pattern 5: Design Customization
**Repetition:**
- Manual CSS modifications
- No systematic design system
- Hardcoded styles

**Compression Opportunity:**
```python
# REPEATED:
background: #fff
border: 2px solid #000
color: #000
```

**Composable Unit:**
```python
class DesignSystem:
    def get_styles(self, theme="clean", printer_friendly=True):
        # Centralized design system
```

---

## 🎯 DESIGN GOALS

### Core Requirements
1. **Self-Aware**: Class knows it can generate docs
2. **Audience-Aware**: Adapts content for target audience
3. **Design-Aware**: Creative, clear design without background graphics
4. **Composable**: Reusable building blocks
5. **Simple API**: Easy to use, powerful capabilities

### Design Principles
- **No Background Graphics**: Clean white pages
- **Creative Typography**: Use fonts, spacing, borders creatively
- **Clear Hierarchy**: Visual structure guides reader
- **Audience Adaptation**: Content complexity matches audience
- **Composable Units**: Build complex from simple

---

## 🏗️ PROPOSED ARCHITECTURE

### Core Classes

#### 1. **DocumentGenerator** (Main Class)
```python
class DocumentGenerator:
    """
    Self-aware document generator that knows it can create docs.
    Adapts content and design for target audience.
    """
    
    def __init__(self, source=None):
        self.source = source  # What to document (codebase, data, etc.)
        self.audience = "general"  # Target audience
        self.design_theme = "clean"  # Design system
        self.printer_friendly = True  # No background graphics
    
    def generate(self, title, content=None, output_path=None):
        """Generate document, adapting for audience and design."""
        # 1. Adapt content for audience
        # 2. Apply design system
        # 3. Render template
        # 4. Generate PDF
```

#### 2. **AudienceAdapter** (Composable Unit)
```python
class AudienceAdapter:
    """Adapts content complexity for target audience."""
    
    LEVELS = {
        "layman": {"complexity": 0.2, "jargon": False},
        "professional": {"complexity": 0.6, "jargon": True},
        "expert": {"complexity": 1.0, "jargon": True}
    }
    
    def adapt(self, content, audience_level):
        """Transform content for audience."""
```

#### 3. **DesignSystem** (Composable Unit)
```python
class DesignSystem:
    """Centralized design system - no background graphics."""
    
    THEMES = {
        "clean": {
            "background": "#fff",
            "borders": "#000",
            "text": "#000",
            "spacing": "generous"
        }
    }
    
    def get_styles(self, theme="clean"):
        """Get CSS styles for theme."""
```

#### 4. **TemplateRenderer** (Composable Unit)
```python
class TemplateRenderer:
    """Unified template rendering."""
    
    def render(self, template_type, metadata, content, design):
        """Render template with design system."""
```

#### 5. **ContentAnalyzer** (Composable Unit)
```python
class ContentAnalyzer:
    """Analyzes content to determine structure."""
    
    def analyze(self, content):
        """Extract structure, complexity, key concepts."""
```

---

## 🔧 COMPOSABLE UNITS DESIGN

### Unit 1: Content Pipeline
```
Source → Analyzer → Adapter → Renderer → PDF
```

### Unit 2: Design Pipeline
```
Theme → DesignSystem → TemplateAdapter → CSS → PDF
```

### Unit 3: Audience Pipeline
```
Content → AudienceAdapter → ComplexityAdjust → Renderer → PDF
```

### Unit 4: Metadata Pipeline
```
Input → MetadataExtractor → DocumentMetadata → Renderer → PDF
```

---

## 📋 IMPLEMENTATION PLAN

### Phase 1: Core Infrastructure
1. ✅ Create `DocumentGenerator` base class
2. ✅ Implement `DesignSystem` with clean theme
3. ✅ Implement `TemplateRenderer` unified renderer
4. ✅ Create `DocumentMetadata` dataclass

### Phase 2: Audience Adaptation
1. ✅ Implement `AudienceAdapter`
2. ✅ Create content complexity analyzer
3. ✅ Build audience-specific templates

### Phase 3: Integration
1. ✅ Integrate with existing `ReflectionSystem`
2. ✅ Integrate with `DocumentBuilder`
3. ✅ Create unified API

### Phase 4: Enhancement
1. ✅ Add more design themes
2. ✅ Expand audience levels
3. ✅ Add content analysis

---

## 🎨 DESIGN SYSTEM SPECIFICATION

### Clean Theme (No Background Graphics)
```css
/* Page */
@page {
    background: #fff;
    margin: 0.75in 0.5in;
}

/* Typography */
body {
    font-family: Arial, sans-serif;
    color: #000;
    background: #fff;
    line-height: 1.6;
}

/* Headers */
h1, h2, h3 {
    color: #000;
    border-bottom: 2px solid #000;
    padding-bottom: 0.1in;
}

/* Boxes */
.warning, .note, .caution {
    border: 2px solid #000;
    background: #fff;
    padding: 0.15in;
}

/* Tables */
table {
    border: 1px solid #000;
    background: #fff;
}

th {
    background: #000;
    color: #fff;
}

td {
    background: #fff;
    border: 1px solid #000;
}
```

**Design Principles:**
- White backgrounds only
- Black borders for structure
- Typography for hierarchy
- Spacing for clarity
- No graphics, patterns, or images

---

## 🔗 INTEGRATION POINTS

### With ReflectionSystem
```python
class ReflectionSystem:
    def __init__(self, ...):
        self.doc_generator = DocumentGenerator(source=self)
    
    def generate_doc(self, audience="professional"):
        return self.doc_generator.generate(
            title="Architecture Documentation",
            audience=audience
        )
```

### With DocumentBuilder
```python
class DocumentBuilder:
    def __init__(self, ...):
        self.generator = DocumentGenerator()
    
    def generate(self, ...):
        return self.generator.generate(...)
```

---

## 📊 METRICS & SUCCESS CRITERIA

### Complexity Reduction
- **Before**: 5+ separate functions, duplicated code
- **After**: 1 unified class, composable units
- **Target**: 60% code reduction

### API Simplicity
- **Before**: Multiple imports, manual setup
- **After**: Single class, fluent API
- **Target**: 3-line minimum example

### Design Consistency
- **Before**: Inconsistent styles across docs
- **After**: Unified design system
- **Target**: 100% consistency

---

## 🚀 NEXT STEPS

1. **Review & Approve** this checkpoint
2. **Implement Core Classes** (DocumentGenerator, DesignSystem, etc.)
3. **Create Composable Units** (AudienceAdapter, TemplateRenderer, etc.)
4. **Integrate with Existing** (ReflectionSystem, DocumentBuilder)
5. **Test & Refine** with real examples
6. **Document & Onboard** usage patterns

---

## 💭 REFLECTION

### What We Learned
- Multiple classes have doc generation but no unified approach
- Significant repetition in template rendering
- No systematic audience adaptation
- Design is ad-hoc, not systematic

### What We're Building
- Unified `DocumentGenerator` class
- Composable design system
- Audience-aware content adaptation
- Clean, graphic-free design
- Simple, powerful API

### Why This Matters
- Reduces complexity while increasing capability
- Creates reusable building blocks
- Enables creative design without graphics
- Makes documentation generation accessible
- Supports WAFT's self-documentation goals

---

**Status**: ✅ Checkpoint Complete - Ready for Implementation Review
