# Being CV Demo Plan - brilliant-cv Typst Template

**Date**: 2026-01-19  
**Status**: Planning  
**Template**: `@preview/brilliant-cv:3.1.1`

---

## Objective

Create a demo that showcases how the Being system can generate personalized CVs using the brilliant-cv Typst template. The demo will:

1. Spawn a Being with skills, memories, and experiences
2. Map Being data to CV sections (experience, education, skills, etc.)
3. Generate Typst content using the brilliant-cv template
4. Compile to PDF using TypstCompiler

---

## Understanding brilliant-cv Template

### Structure
- **Entry Point**: `cv.typ` - Main CV document
- **Configuration**: `metadata.toml` - Personal info, layout, language settings
- **Content Modules**: `modules_<lang>/` - Experience, education, skills, publications
- **Template Functions**: `cvEntry()`, `cvPublication()`, `cvEducation()`, etc.

### Key Features
- Multilingual support (EN, FR, CN)
- AI/ATS-friendly (keyword injection)
- Separation of content and style
- FontAwesome icons
- Customizable colors and fonts

### API Usage
```typst
#import "@preview/brilliant-cv:3.1.1": *

#show: cv.with(
  author: (
    firstname: "Jane",
    lastname: "Doe",
  ),
  main-color: rgb("#0044cc"),
)

cvEntry(
  title: "Software Engineer",
  institution: "Acme Inc.",
  date: "2021–2024",
  location: "Remote",
  logo: image("logo.png"),  // Must be function, not string
  bullets: [...],
)
```

---

## Implementation Plan

### Phase 1: Template Wrapper
**File**: `src/waft/templates/typst/wrappers/brilliant_cv.py`

**Purpose**: Python wrapper that generates Typst content for brilliant-cv template

**Functions**:
- `generate_brilliant_cv()` - Main generation function
- `_create_metadata_toml()` - Generate metadata.toml from Being data
- `_create_cv_typ()` - Generate cv.typ entry point
- `_create_experience_module()` - Map Being memories → experience entries
- `_create_skills_module()` - Map Being skills → skills section
- `_create_education_module()` - Map Being lineage/ancestry → education
- `_map_being_to_cv_data()` - Convert Being object to CV data structure

### Phase 2: Being-to-CV Mapper
**File**: `src/waft/templates/typst/being_cv_mapper.py`

**Purpose**: Map Being attributes to CV sections

**Mappings**:
- **Skills** → Technical Skills section
- **Memories** → Work Experience entries
- **Lessons Learned** → Achievements/Highlights
- **Ancestral Chain** → Education/Training
- **Personality** → Summary/About section
- **Goals** → Career Objectives
- **Fitness** → Performance metrics
- **Reality ID** → Current Role/Position

### Phase 3: Demo Script
**File**: `examples/demo_being_cv.py`

**Purpose**: Complete demo that spawns Being and generates CV

**Steps**:
1. Spawn a Being with initial skills and personality
2. Add some memories (simulated work experiences)
3. Map Being data to CV format
4. Generate Typst content using wrapper
5. Compile to PDF using TypstCompiler
6. Save output to `demo_output/being_cv_demo.pdf`

### Phase 4: Integration
- Register wrapper in TypstTemplateRegistry
- Add to template discovery system
- Create CLI command (optional): `waft being-cv <being-id>`

---

## Being Data → CV Mapping Strategy

### Personal Information
```python
{
  "name": being.custom_name or being.being_id,
  "email": f"{being.being_id}@waft.reality",
  "location": being.reality_id,
  "summary": being.personality.get("description", ""),
}
```

### Experience (from Memories)
```python
for memory in being.memories:
    if memory.get("type") == "work" or "experience" in memory.get("tags", []):
        cv_entry = {
            "title": memory.get("title", "Experience"),
            "institution": memory.get("context", "Reality"),
            "date": memory.get("timestamp", ""),
            "location": memory.get("reality_id", being.reality_id),
            "bullets": memory.get("details", []),
        }
```

### Skills (from Being.skills)
```python
skills = {
    "technical": [skill for skill, level in being.skills.items() if level > 5.0],
    "soft": [skill for skill, level in being.skills.items() if level <= 5.0],
}
```

### Education (from Ancestral Chain)
```python
education = {
    "degree": "Being Evolution",
    "institution": "Source Consciousness",
    "date": being.created_at,
    "description": f"Lineage: {' → '.join(being.ancestral_chain)}",
}
```

---

## File Structure

```
src/waft/templates/typst/
├── wrappers/
│   ├── __init__.py
│   └── brilliant_cv.py          # NEW: Template wrapper
├── being_cv_mapper.py            # NEW: Being → CV mapper
├── compiler.py                   # Existing
└── registry.py                   # Existing (will auto-discover wrapper)

examples/
└── demo_being_cv.py              # NEW: Demo script

demo_output/
└── being_cv_demo.pdf             # Generated output
```

---

## Testing Strategy

1. **Unit Tests**: Test mapper functions with sample Being data
2. **Integration Tests**: Test wrapper with mock Being
3. **End-to-End**: Run full demo and verify PDF output
4. **Visual Verification**: Check PDF formatting and content

---

## Success Criteria

✅ Being data successfully mapped to CV format  
✅ Typst content generated correctly  
✅ PDF compiles without errors  
✅ CV contains Being's skills, memories, and experiences  
✅ Output is visually appealing and professional  
✅ Template wrapper registered in TypstTemplateRegistry  

---

## Next Steps

1. Initialize brilliant-cv template locally to study structure
2. Create Being-to-CV mapper
3. Create Typst wrapper
4. Write demo script
5. Test and refine

---

## Related Work Efforts

- **WE-260114-ar3y**: LaTeX Template Integration (CV templates)
- **WE-260112-jqkn**: D&D Campaign PDF Evolution (Typst integration patterns)

---

## Notes

- brilliant-cv requires Typst 0.14.0+ (check version compatibility)
- Fonts needed: Roboto, Source Sans Pro, FontAwesome 6
- Template uses TOML for metadata (not Typst dict)
- Logo arguments must be functions (`image("logo.png")`) not strings
