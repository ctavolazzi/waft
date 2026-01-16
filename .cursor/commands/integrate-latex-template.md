# Integrate LaTeX Template

**Automate the complete workflow for integrating new LaTeX templates into WAFT's template system.**

Encapsulates the systematic process of cloning a LaTeX template repository, analyzing its structure, creating wrapper modules, verifying registry discovery, and updating work efforts. This command standardizes and automates template integration to ensure consistency and reduce manual effort.

**Use when:** You want to integrate a new LaTeX template repository into WAFT's template system, need to add template support, or want to automate the template integration workflow.

---

## Purpose

This command provides:
- **Automated Integration**: Complete workflow from repository to registered template
- **Structure Analysis**: Automatic analysis of template structure and placeholders
- **Wrapper Generation**: Creates wrapper modules following established patterns
- **Registry Verification**: Confirms templates are auto-discovered
- **Work Effort Integration**: Updates work efforts with progress
- **Consistency**: Ensures all templates follow the same integration pattern

---

## Philosophy

1. **Systematic Approach**: Follow the same pattern for every template integration
2. **Automation First**: Reduce manual steps and potential errors
3. **Pattern Consistency**: All wrappers follow the same structure
4. **Verification Built-In**: Always verify integration succeeded
5. **Documentation**: Track progress in work efforts automatically

---

## Execution Steps

### Step 1: Gather Requirements

**Purpose**: Understand what template to integrate

**Actions**:
1. **Identify Template Source**:
   - Repository URL (GitHub, GitLab, etc.)
   - Template name/description
   - Number of templates in repository
   - Template categories/types

2. **Verify Prerequisites**:
   - Git is available
   - Templates directory exists: `templates/`
   - Wrappers directory exists: `src/waft/templates/latex/wrappers/`
   - Registry system is functional

3. **Check for Existing Integration**:
   - Search for existing wrapper with same name
   - Check if repository already cloned
   - Verify template not already registered

**Output**: Requirements summary and validation status

---

### Step 2: Clone Repository

**Purpose**: Get template files locally

**Actions**:
1. **Determine Clone Location**:
   - Extract repository name from URL (e.g., "Ashad001/Latex-Templates" → "ashad001-latex-templates")
   - Create sanitized directory name (lowercase, hyphens for spaces/slashes)
   - Path: `templates/{sanitized-name}/`

2. **Clone Repository**:
   ```bash
   cd templates
   git clone {repository_url} {sanitized-name}
   ```
   Example: `git clone https://github.com/Ashad001/Latex-Templates.git ashad001-latex-templates`

3. **Verify Clone Success**:
   - Check directory exists: `ls -la templates/{sanitized-name}/`
   - List template directories: `find templates/{sanitized-name} -maxdepth 2 -type d -name "*Template*"`
   - Verify template files present
   - Identify main template files (main.tex, etc.)

**Output**: Cloned repository location and file structure

---

### Step 3: Analyze Template Structure

**Purpose**: Understand template structure and requirements

**Actions**:
1. **Identify Template Files**:
   - List repository structure: `list_dir("templates/{repo-name}/")`
   - Find main `.tex` files (typically `main.tex` in each template directory)
   - Locate template directories (e.g., "Business Proposal Template/", "SRS Template/")
   - Identify supporting files (images, styles, .bib files, etc.)

2. **Read and Analyze Each Template**:
   - For each template directory:
     - Read `main.tex` file: `read_file("templates/{repo}/{template-dir}/main.tex")`
     - Analyze content to identify:
       - **Placeholders**: Look for hardcoded text like "MEMBER1", "PROJECT NAME", "{Buissness Name}"
       - **Placeholder Type**: Hardcoded text (string replacement) vs `{{ variable }}` (Jinja2)
       - **Required Parameters**: Extract from placeholders (e.g., business_name, members, course_code)
       - **Optional Parameters**: Section content parameters (introduction, conclusion, etc.)
       - **LaTeX Packages**: Note `\usepackage{}` declarations
       - **Document Structure**: Identify sections, subsections, title page structure

3. **Determine Compilation Requirements**:
   - Check for `\usepackage{fontspec}` → indicates `xelatex`
   - Check for `\usepackage[utf8]{inputenc}` → indicates `pdflatex`
   - Default: `pdflatex` if unclear
   - Compilation runs: Typically 2 (for TOC, references)

4. **Map Template Sections to Parameters**:
   - Identify document sections (Introduction, Conclusion, etc.)
   - Map each section to function parameter
   - Note content insertion points (where to inject user content)
   - Identify member/author placeholders and their structure

**Output**: Template analysis report with:
- Template structure (directories, files)
- Placeholder analysis (hardcoded vs Jinja2)
- Parameter mapping (required and optional)
- Compilation requirements (pdflatex/xelatex, runs)
- Section mapping

---

### Step 4: Create Wrapper Modules

**Purpose**: Generate Python wrapper modules for each template

**Actions**:
1. **For Each Template**:
   - Generate wrapper module name (snake_case from template name)
     - "Business Proposal Template" → `business_proposal.py`
     - "SRS Template" → `srs.py`
     - "Project Proposal Template" → `project_proposal.py`
     - "Project Report Template" → `project_report.py`
   - Create wrapper file: `src/waft/templates/latex/wrappers/{module_name}.py`

2. **Generate Wrapper Code** (following exact pattern from `assignment.py` or `srs.py`):
   - **Module Docstring**:
     ```python
     """
     {Template Name} LaTeX Template Wrapper
     =======================================

     Python wrapper for {Source} {Template Name} template.
     Auto-discovered by LaTeXTemplateRegistry.

     category: {category}
     tags: [latex, pdf, {tags}]
     source: {source}
     """
     ```

   - **Imports**:
     ```python
     from pathlib import Path
     from ..compiler import LaTeXCompiler
     from ..content_builders import build_{content_type}_content
     # Note: Only import jinja2 if template uses Jinja2 variables
     ```

   - **Function Signature**:
     ```python
     def generate_{template_name}(
         title: str,
         content: str,
         output_path: Path,
         {template_specific_parameters},
         **kwargs
     ) -> Path:
     ```

   - **Template Path Resolution**:
     ```python
     # For templates in templates/{repo-name}/{template-dir}/
     template_dir = Path(__file__).parent.parent.parent.parent.parent / "templates" / "{repo-name}" / "{template-dir}"
     template_file = template_dir / "main.tex"
     ```

   - **Template Loading**:
     ```python
     if not template_file.exists():
         raise FileNotFoundError(f"{Template Name} template not found: {template_file}")
     template_content = template_file.read_text(encoding="utf-8")
     ```

   - **Content Building**:
     ```python
     latex_content = build_{content_type}_content(
         title=title,
         content=content,
         **kwargs
     )
     ```

   - **Placeholder Replacement** (based on analysis):
     - **If hardcoded placeholders** (like "MEMBER1", "PROJECT NAME"):
       ```python
       filled_latex = template_content
       filled_latex = filled_latex.replace("MEMBER1", member1_name)
       filled_latex = filled_latex.replace("PROJECT NAME", project_name)
       # Replace section content
       if introduction:
           filled_latex = filled_latex.replace("\\section{Introduction}", f"\\section{{Introduction}}\n\n{introduction}")
       ```
     - **If Jinja2 variables** (like `{{ variable }}`):
       ```python
       from jinja2 import Template
       jinja_template = Template(template_content)
       filled_latex = jinja_template.render(
           title=title,
           content=latex_content,
           {parameters},
           **kwargs
       )
       ```

   - **PDF Compilation**:
     ```python
     compiler = LaTeXCompiler(compiler="{pdflatex|xelatex}")
     pdf_path = compiler.compile(
         filled_latex,
         output_path,
         working_dir=template_dir,
         runs=2
     )
     return pdf_path
     ```

3. **Follow Established Pattern**:
   - Use `assignment.py` or `srs.py` as reference
   - Match parameter structure (title, content, output_path, then template-specific)
   - Use same content builder pattern
   - Follow same error handling
   - Use same docstring format

4. **Handle Template Variations**:
   - Support multiple template versions if present
   - Handle optional parameters gracefully
   - Support both string replacement and Jinja2

**Output**: Wrapper module files created

---

### Step 5: Verify Registry Discovery

**Purpose**: Confirm templates are auto-discovered

**Actions**:
1. **Test Registry Loading**:
   ```bash
   python3 -c "from src.waft.templates.latex.registry import get_latex_registry; registry = get_latex_registry(); templates = registry.list_templates(); print(f'Found {len(templates)} templates:'); [print(f'  - {t.name} ({t.module_name})') for t in templates]"
   ```

2. **Verify Template Discovery**:
   - Check new templates appear in list
   - Verify count increased (e.g., from 4 to 8 templates)
   - Verify metadata extraction:
     - Name (display name from module name)
     - Category (from docstring or inferred)
     - Tags (from docstring)
     - Source (from docstring or module name)
   - Confirm generate functions are found
   - Check parameter extraction

3. **Test Template Access** (optional):
   ```python
   template = registry.get_template("Business Proposal")
   generate_func = registry.get_generate_function("Business Proposal")
   ```

**Output**: Verification report showing:
- Total templates discovered
- New templates added
- Template names and module names
- Any discovery errors

---

### Step 6: Update Work Effort

**Purpose**: Document integration progress

**Actions**:
1. **Identify Work Effort**:
   - Find related work effort (e.g., WE-260114-ar3y for LaTeX template integration)
   - Or create new work effort if needed using `/create-work-effort`

2. **Update Progress Section**:
   - Add new progress entry with date:
     ```markdown
     ### YYYY-MM-DD: {Template Source} Templates Integrated ✅
     - ✅ Cloned {Source}/{Repository} repository
     - ✅ Analyzed structure of all {N} templates ({template names})
     - ✅ Created wrapper modules for all {N} templates:
       - `{module1}.py` - {Template 1} template wrapper
       - `{module2}.py` - {Template 2} template wrapper
       - ...
     - ✅ All templates auto-discovered by LaTeXTemplateRegistry ({total} total templates now registered)
     - ✅ Wrappers use {string replacement|Jinja2} for placeholder substitution
     - ✅ Templates use {pdflatex|xelatex} compiler

     **Key Files Created:**
     - `templates/{repo-name}/` - Cloned repository
     - `src/waft/templates/latex/wrappers/{module1}.py` - {Template 1} wrapper
     - ...

     **Next:** Test all {N} templates with sample data to verify PDF generation works
     ```

3. **Update Tickets** (if applicable):
   - Mark tickets as completed (e.g., TKT-ar3y-002)
   - Add new tickets if needed
   - Update ticket status table

**Output**: Updated work effort index file with integration progress

---

### Step 7: Generate Summary

**Purpose**: Provide integration summary

**Actions**:
1. **Compile Integration Report**:
   - Templates integrated (count and names)
   - Wrapper modules created
   - Registry status
   - Files created/modified
   - Next steps

2. **Display Summary**:
   - Use Rich formatting for clarity
   - Show success/failure status
   - List created files
   - Provide verification commands

**Output**: Integration summary with next steps

---

## Usage Examples

### Basic Integration
```
/integrate-latex-template --repo https://github.com/user/latex-templates.git --name "Template Name"
```

**What Happens**:
1. Clones repository to `templates/`
2. Analyzes template structure
3. Creates wrapper modules
4. Verifies registry discovery
5. Updates work effort

### Integration with Work Effort
```
/integrate-latex-template --repo https://github.com/user/templates.git --work-effort WE-260114-ar3y
```

**What Happens**:
- Same as basic, plus updates specified work effort

### Integration with Custom Path
```
/integrate-latex-template --repo https://github.com/user/templates.git --clone-path templates/custom/
```

**What Happens**:
- Clones to custom path instead of default

---

## Template Analysis Patterns

### Pattern 1: Hardcoded Placeholders (String Replacement)
**Example**: Ashad001 templates
- Templates use hardcoded text like "MEMBER1", "PROJECT NAME"
- Wrapper uses string replacement: `filled_latex.replace("MEMBER1", member_name)`
- No Jinja2 needed

### Pattern 2: Jinja2 Variables
**Example**: Some templates use `{{ variable }}` syntax
- Wrapper uses Jinja2 Template: `jinja_template.render(variable=value)`
- More flexible but requires template modification

### Pattern 3: Mixed Approach
**Example**: Some placeholders hardcoded, some as variables
- Use string replacement for hardcoded
- Use Jinja2 for variables
- Or convert all to one approach

---

## Wrapper Module Template

```python
"""
{Template Name} LaTeX Template Wrapper
======================================

Python wrapper for {Source} {Template Name} template.
Auto-discovered by LaTeXTemplateRegistry.

category: {category}
tags: [latex, pdf, {tags}]
source: {source}
"""

from pathlib import Path
from ..compiler import LaTeXCompiler
from ..content_builders import build_{content_type}_content


def generate_{template_name}(
    title: str,
    content: str,
    output_path: Path,
    {parameters},
    **kwargs
) -> Path:
    """
    Generate PDF using {Template Name} LaTeX template.

    Args:
        title: Document title
        content: Main content (markdown or HTML)
        output_path: Where to save PDF
        {parameter_docs}
        **kwargs: Additional template parameters

    Returns:
        Path to generated PDF
    """
    # Get template path (standardized - find project root)
    # Find project root by looking for pyproject.toml or .git
    current = Path(__file__).parent
    project_root = current
    while project_root != project_root.parent:
        if (project_root / "pyproject.toml").exists() or (project_root / ".git").exists():
            break
        project_root = project_root.parent

    template_dir = project_root / "templates" / "{repo_name}" / "{template_dir}"

    # Find main template file (try main.tex first, then largest .tex file)
    template_file = template_dir / "main.tex"
    if not template_file.exists():
        tex_files = list(template_dir.glob("*.tex"))
        if tex_files:
            template_file = max(tex_files, key=lambda f: f.stat().st_size)
        else:
            raise FileNotFoundError(f"No .tex files found in {template_dir}")

    if not template_file.exists():
        raise FileNotFoundError(f"{Template Name} template not found: {template_file}")

    # Load template
    template_content = template_file.read_text(encoding="utf-8")

    # Build LaTeX content
    latex_content = build_{content_type}_content(
        title=title,
        content=content,
        **kwargs
    )

    # Auto-detect placeholder method and replace
    # Check for Jinja2 variables ({{ variable }})
    if "{{" in template_content and "}}" in template_content:
        # Use Jinja2
        from jinja2 import Template
        jinja_template = Template(template_content)
        filled_latex = jinja_template.render(
            title=title,
            content=latex_content,
            {parameters},
            **kwargs
        )
    else:
        # Use string replacement for hardcoded placeholders
        filled_latex = template_content
        # ... replacement logic based on detected placeholders ...

    # Auto-detect compiler requirement
    # Check for xelatex indicators
    if "\\usepackage{fontspec}" in template_content or "% xelatex" in template_content.lower():
        compiler_name = "xelatex"
    else:
        compiler_name = "pdflatex"  # Default

    # Compile to PDF
    compiler = LaTeXCompiler(compiler=compiler_name)
    pdf_path = compiler.compile(
        filled_latex,
        output_path,
        working_dir=template_dir,
        runs=2
    )

    return pdf_path
```

---

## Integration Checklist

- [ ] Repository cloned successfully
- [ ] Template structure analyzed
- [ ] Placeholders identified
- [ ] Wrapper modules created
- [ ] Wrapper code follows pattern
- [ ] Registry discovery verified
- [ ] Work effort updated
- [ ] Summary generated

---

## Error Handling

### Repository Clone Fails
- **Check**: Network connectivity, repository URL, permissions
- **Action**: Provide clear error message, suggest manual clone

### Template Analysis Fails
- **Check**: Template files exist, readable, valid LaTeX
- **Action**: Report analysis errors, suggest manual review

### Wrapper Creation Fails
- **Check**: Wrappers directory writable, valid Python syntax
- **Action**: Show generated code, allow manual fix

### Registry Discovery Fails
- **Check**: Wrapper imports correctly, function naming correct
- **Action**: Test import manually, verify function names

---

## Integration with Other Commands

- **`/check-assumptions`**: Validate assumptions about template structure before integration
- **`/create-work-effort`**: Create work effort if one doesn't exist
- **`/improve`**: Analyze and improve generated wrapper code
- **`/verify`**: Verify integration succeeded
- **`/checkpoint`**: Document integration state

---

## When to Use

**Use `/integrate-latex-template` when**:
- ✅ Integrating new LaTeX template repository
- ✅ Want to automate template integration workflow
- ✅ Need consistent template integration pattern
- ✅ Multiple templates to integrate
- ✅ Want to reduce manual integration effort

**Don't use `/integrate-latex-template` when**:
- ❌ Template is already integrated
- ❌ Just need to use existing template (use registry directly)
- ❌ Template requires significant customization
- ❌ Manual integration preferred for learning

---

## Improvements Based on Assumptions Validation

### Standardized Path Resolution
**Issue**: Different wrappers use inconsistent `.parent` chains
**Solution**: Use project root detection instead of relative paths
```python
# Find project root (look for pyproject.toml or .git)
project_root = Path(__file__).parent
while project_root != project_root.parent:
    if (project_root / "pyproject.toml").exists() or (project_root / ".git").exists():
        break
    project_root = project_root.parent

template_dir = project_root / "templates" / repo_name / template_dir
```

### Auto-Detection Features

1. **Placeholder Method Detection**:
   - Check for `{{ variable }}` patterns → Use Jinja2
   - Check for hardcoded text like "MEMBER1", "PROJECT NAME" → Use string replacement
   - Default to string replacement if unclear

2. **Compiler Detection**:
   - Check for `\usepackage{fontspec}` or `xelatex` comments → Use xelatex
   - Check for `\usepackage[utf8]{inputenc}` → Use pdflatex
   - Default to pdflatex

3. **Template File Detection**:
   - Look for `main.tex` first
   - If not found, find largest `.tex` file in template directory
   - Or use template name: `{template_name}.tex`

4. **Content Builder Selection**:
   - Map template category to content builder:
     - `report` → `build_report_content()`
     - `assignment` → `build_assignment_content()`
     - `essay` → `build_essay_content()`
     - `presentation` → `build_presentation_content()`
     - Default to `build_report_content()`

## Future Enhancements

### Potential Additions

1. **Template Testing**: Automatically test generated wrappers with sample data
2. **Content Builder Generation**: Auto-generate content builder functions if needed
3. **Template Validation**: Validate LaTeX syntax before integration
4. **Batch Integration**: Integrate multiple templates from one repository
5. **Template Updates**: Update existing wrappers when templates change
6. **Documentation Generation**: Auto-generate template usage documentation
7. **Interactive Mode**: Prompt for missing information instead of using defaults
8. **Dry Run Mode**: Show what would be created without actually creating files

---

## Example Workflow (Based on Actual Integration)

This workflow is based on the actual integration of Ashad001 templates we just completed:

```
User: "/integrate-latex-template --repo https://github.com/Ashad001/Latex-Templates.git"

AI: [Step 1: Gather Requirements]
    - Repository: Ashad001/Latex-Templates
    - Repository URL: https://github.com/Ashad001/Latex-Templates.git
    - Sanitized name: ashad001-latex-templates
    - Prerequisites: ✓ Git available, templates/ exists, wrappers/ exists

AI: [Step 2: Clone Repository]
    - Running: cd templates && git clone https://github.com/Ashad001/Latex-Templates.git ashad001-latex-templates
    - ✓ Clone successful
    - Directory: templates/ashad001-latex-templates/

AI: [Step 3: Analyze Template Structure]
    - Listing repository structure...
    - Found template directories:
      * Business Proposal Template/
      * SRS Template/
      * Project Proposal Template/
      * Project Report Template 1/
      * Project Report Template 2/
    - Reading main.tex files...
    - Analyzing placeholders:
      * Business Proposal: Hardcoded ("{Buissness Name}", "Member 1", "INTRODUCTION")
      * SRS: Hardcoded ("SOFTWARE NAME", "MEMBER1", "CS-CODE")
      * Project Proposal: Hardcoded ("PROJECT NAME", "MEMBER1", "CS-CODE")
      * Project Report: Hardcoded ("PROJECT NAME", "Member 1", "ID")
    - Compiler: pdflatex (all templates)
    - Placeholder method: String replacement (all templates)

AI: [Step 4: Create Wrapper Modules]
    - Creating business_proposal.py...
      * Function: generate_business_proposal()
      * Parameters: business_name, location, members, introduction, rationale, etc.
      * Path: templates/ashad001-latex-templates/Business Proposal Template/
      * String replacement for placeholders
    - Creating srs.py...
      * Function: generate_srs()
      * Parameters: software_name, course_code, members, introduction, etc.
    - Creating project_proposal.py...
      * Function: generate_project_proposal()
      * Parameters: project_name, course_code, members, introduction, etc.
    - Creating project_report.py...
      * Function: generate_project_report()
      * Parameters: project_name, template_version (1 or 2), members, etc.
      * Supports both Template 1 and Template 2
    - ✓ All 4 wrappers created

AI: [Step 5: Verify Registry Discovery]
    - Running: python3 -c "from src.waft.templates.latex.registry import get_latex_registry; ..."
    - Output: Found 8 templates:
      * Business Proposal (business_proposal)
      * Srs (srs)
      * Project Proposal (project_proposal)
      * Project Report (project_report)
      * (plus 4 existing templates)
    - ✓ All 4 new templates discovered
    - Total templates: 8 (was 4, now 8)

AI: [Step 6: Update Work Effort]
    - Updating WE-260114-ar3y_index.md...
    - Adding progress entry with date
    - Documenting created files
    - ✓ Work effort updated

AI: [Step 7: Generate Summary]
    ✅ Integration Complete

    Summary:
    - Repository: Ashad001/Latex-Templates
    - Templates integrated: 4
    - Wrapper modules created: 4
      * business_proposal.py
      * srs.py
      * project_proposal.py
      * project_report.py
    - Registry status: ✓ All discovered (8 total templates)
    - Placeholder method: String replacement
    - Compiler: pdflatex
    - Files created:
      * templates/ashad001-latex-templates/ (cloned repo)
      * src/waft/templates/latex/wrappers/business_proposal.py
      * src/waft/templates/latex/wrappers/srs.py
      * src/waft/templates/latex/wrappers/project_proposal.py
      * src/waft/templates/latex/wrappers/project_report.py
    - Work effort: WE-260114-ar3y updated

    Next Steps:
    - Test all 4 templates with sample data to verify PDF generation works
```

---

**This command automates the complete LaTeX template integration workflow, ensuring consistency and reducing manual effort for future template additions.**
