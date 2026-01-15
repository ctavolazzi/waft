# Evolve Another Template

**Generate the evolution report using an alternative template format.**

Creates a new version of the complete evolution report using a different template style (academic paper, field guide, lab notes, etc.) instead of the default format.

**Use when:** You want to see the evolution report in a different format, need a different style for presentation, or want to compare template outputs.

---

## Purpose

This command provides:
- **Template Selection**: Choose from available template styles
- **Alternative Formatting**: Generate report in academic paper, field guide, lab notes, or other formats
- **Same Content**: Uses the same evolution data, just different presentation
- **Template Comparison**: Generate multiple versions to compare styles

---

## Quick Start

### Generate with Academic Paper Template
```
/evolve-another-template --template academic
```

### Generate with Field Guide Template
```
/evolve-another-template --template field-guide
```

### Generate with Lab Notes Template
```
/evolve-another-template --template lab-notes
```

### List Available Templates
```
/evolve-another-template --list
```

### Generate All Templates
```
/evolve-another-template --all
```

---

## Available Templates

1. **academic** - Two-column academic paper format (arXiv style)
2. **field-guide** - Field guide format with sections and examples
3. **latex-cookbook** - LaTeX Cookbook template (professional LaTeX, LuaLaTeX compilation)
4. **lab-notes** - Lab notebook style with dated entries
5. **personal-memo** - Personal memo format
6. **tm-report** - Technical memo format
7. **default** - Current default format (for comparison)

---

## Workflow

1. **Load Evolution Data**: Reads the most recent evolution data from `/evolve` run
2. **Select Template**: Choose template style (or use default)
3. **Transform Content**: Convert evolution data to template format
4. **Generate PDF**: Create PDF using selected template
5. **Save & Open**: Save to Desktop and open automatically

---

## Usage Examples

### Academic Paper Format
```
/evolve-another-template --template academic
```

Generates evolution report as a two-column academic paper with:
- Abstract section
- Author information
- Section numbering
- References
- Professional academic typography

### Field Guide Format
```
/evolve-another-template --template field-guide
```

Generates evolution report as a field guide with:
- Clear section headers
- Examples and use cases
- Step-by-step documentation
- Visual hierarchy

### Lab Notes Format
```
/evolve-another-template --template lab-notes
```

Generates evolution report as lab notebook with:
- Dated entries
- Experimental observations
- Data tables
- Scientific notation

---

## Integration

This command integrates with:
- **Evolution System**: Uses data from `/evolve` workflow
- **Template System**: Uses templates from `src/waft/templates/`
- **PDF Generation**: Uses WeasyPrint for PDF creation
- **Being System**: Reads Being evolution data
- **Work Effort**: WE-260112-z88r (Evolution Report Template Evolution System)
  - All template evolution tickets and work tracked here
  - Future template additions go in this work effort folder

---

## When to Use

**Use `/evolve-another-template` when**:
- ✅ Want to see evolution report in different format
- ✅ Need academic paper format for sharing
- ✅ Prefer field guide style for documentation
- ✅ Want to compare template outputs
- ✅ Need specific format for presentation

**Don't use `/evolve-another-template` when**:
- ❌ Haven't run `/evolve` yet (no data to format)
- ❌ Just need default format (use `/evolve` directly)
- ❌ Don't need alternative formatting

---

## Output

After completion, provides:
1. **PDF Generated**: New template version saved to Desktop
2. **Template Used**: Shows which template was applied
3. **File Location**: Path to generated PDF
4. **Auto-Opened**: PDF opens automatically for review

---

## Template Details

### Academic Paper Template
- Two-column layout
- Abstract section
- Author affiliations
- Section numbering
- References section
- Professional typography

### Field Guide Template
- Single-column layout
- Clear section headers
- Examples and use cases
- Step-by-step format
- Visual hierarchy

### Lab Notes Template
- Dated entries
- Experimental format
- Data tables
- Scientific notation
- Observation format

---

## Best Practices

1. **Run `/evolve` First**: Ensure you have evolution data
2. **Choose Appropriate Template**: Match template to use case
3. **Compare Formats**: Generate multiple templates to compare
4. **Review Output**: Check formatting meets your needs
5. **Save Versions**: Keep different template versions for different purposes

---

**Evolve Another Template - see your evolution report in a new format.**

--- End Command ---
