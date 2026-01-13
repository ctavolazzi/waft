# tldr Page Examples for WAFT

This document shows example tldr pages for WAFT commands. These would be stored in `tldr-pages/common/` directory.

---

## Example 1: Main `waft` Command

### File: `tldr-pages/common/waft.md`

```markdown
# waft

Create and manage WAFT (Wicked Awesome Framework & Tools) projects.

- Create a new WAFT project:
  waft new my_project

- Verify project structure:
  waft verify

- Sync dependencies:
  waft sync

- Add a dependency:
  waft add pytest

- Show project information:
  waft info

- Start web dashboard:
  waft serve

- Initialize WAFT in existing project:
  waft init
```

### Rendered Output (when you run `tldr waft`):
```
waft

Create and manage WAFT (Wicked Awesome Framework & Tools) projects.

- Create a new WAFT project:
  waft new my_project

- Verify project structure:
  waft verify

- Sync dependencies:
  waft sync

- Add a dependency:
  waft add pytest

- Show project information:
  waft info

- Start web dashboard:
  waft serve

- Initialize WAFT in existing project:
  waft init
```

---

## Example 2: `waft new` Command

### File: `tldr-pages/common/waft-new.md`

```markdown
# waft new

Create a new WAFT evolutionary laboratory project.

- Create a new project with default settings:
  waft new my_project

- Create project with specific template:
  waft new my_project --template minimal

- Create project with custom directory:
  waft new my_project --path /custom/path

- Create project and initialize git:
  waft new my_project --git

- Create project with specific Python version:
  waft new my_project --python 3.11
```

### Rendered Output (when you run `tldr waft-new`):
```
waft new

Create a new WAFT evolutionary laboratory project.

- Create a new project with default settings:
  waft new my_project

- Create project with specific template:
  waft new my_project --template minimal

- Create project with custom directory:
  waft new my_project --path /custom/path

- Create project and initialize git:
  waft new my_project --git

- Create project with specific Python version:
  waft new my_project --python 3.11
```

---

## Example 3: `waft evolve` Command

### File: `tldr-pages/common/waft-evolve.md`

```markdown
# waft evolve

Run evolutionary cycles to improve agents and templates.

- Run evolution cycle for an agent:
  waft evolve --agent my_agent

- Evolve with specific mutation strategy:
  waft evolve --agent my_agent --mutation random

- Evolve with custom fitness function:
  waft evolve --agent my_agent --fitness custom

- Run evolution with verbose output:
  waft evolve --agent my_agent --verbose

- Evolve multiple generations:
  waft evolve --agent my_agent --generations 10
```

### Rendered Output (when you run `tldr waft-evolve`):
```
waft evolve

Run evolutionary cycles to improve agents and templates.

- Run evolution cycle for an agent:
  waft evolve --agent my_agent

- Evolve with specific mutation strategy:
  waft evolve --agent my_agent --mutation random

- Evolve with custom fitness function:
  waft evolve --agent my_agent --fitness custom

- Run evolution with verbose output:
  waft evolve --agent my_agent --verbose

- Evolve multiple generations:
  waft evolve --agent my_agent --generations 10
```

---

## Example 4: `waft-docs` Command (Cursor Command)

### File: `tldr-pages/common/waft-docs.md`

```markdown
# waft-docs

Generate WAFT documentation: field guides, booklets, session summaries.

- Generate complete field guide booklet:
  /waft-docs field-guide

- Generate printer-friendly field guide:
  /waft-docs field-guide --printer-friendly

- Generate field guide for specific level:
  /waft-docs field-guide --level professional

- Generate session summary PDF:
  /waft-docs session-summary

- Generate complete booklet:
  /waft-docs booklet

- Redact areas in a PDF:
  /waft-docs redact --input file.pdf --areas "100,200,300,400"

- Generate everything (all docs):
  /waft-docs all
```

### Rendered Output (when you run `tldr waft-docs`):
```
waft-docs

Generate WAFT documentation: field guides, booklets, session summaries.

- Generate complete field guide booklet:
  /waft-docs field-guide

- Generate printer-friendly field guide:
  /waft-docs field-guide --printer-friendly

- Generate field guide for specific level:
  /waft-docs field-guide --level professional

- Generate session summary PDF:
  /waft-docs session-summary

- Generate complete booklet:
  /waft-docs booklet

- Redact areas in a PDF:
  /waft-docs redact --input file.pdf --areas "100,200,300,400"

- Generate everything (all docs):
  /waft-docs all
```

---

## Example 5: `waft verify` Command

### File: `tldr-pages/common/waft-verify.md`

```markdown
# waft verify

Verify WAFT project structure and configuration.

- Verify current project:
  waft verify

- Verify with detailed output:
  waft verify --verbose

- Verify specific component:
  waft verify --component templates

- Verify and fix issues automatically:
  waft verify --fix

- Verify and generate report:
  waft verify --report report.json
```

### Rendered Output (when you run `tldr waft-verify`):
```
waft verify

Verify WAFT project structure and configuration.

- Verify current project:
  waft verify

- Verify with detailed output:
  waft verify --verbose

- Verify specific component:
  waft verify --component templates

- Verify and fix issues automatically:
  waft verify --fix

- Verify and generate report:
  waft verify --report report.json
```

---

## Example 6: `waft-status` Command (Cursor Command)

### File: `tldr-pages/common/waft-status.md`

```markdown
# waft-status

Check WAFT system status and generate status reports.

- Check current system status:
  /waft-status

- Generate status report at layman level:
  /waft-status --level layman

- Generate professional status report:
  /waft-status --level professional

- Generate scientist-level status report:
  /waft-status --level scientist

- Save status snapshot:
  /waft-status --save

- Check status without logging:
  /waft-status --no-log
```

### Rendered Output (when you run `tldr waft-status`):
```
waft-status

Check WAFT system status and generate status reports.

- Check current system status:
  /waft-status

- Generate status report at layman level:
  /waft-status --level layman

- Generate professional status report:
  /waft-status --level professional

- Generate scientist-level status report:
  /waft-status --level scientist

- Save status snapshot:
  /waft-status --save

- Check status without logging:
  /waft-status --no-log
```

---

## Directory Structure

When implemented, the structure would look like:

```
tldr-pages/
├── common/
│   ├── waft.md
│   ├── waft-new.md
│   ├── waft-verify.md
│   ├── waft-evolve.md
│   ├── waft-sync.md
│   ├── waft-add.md
│   ├── waft-info.md
│   ├── waft-serve.md
│   ├── waft-docs.md
│   └── waft-status.md
└── waft/  (optional: WAFT-specific commands)
    └── ...
```

---

## Usage After Installation

Once tldr is installed and configured:

```bash
# View WAFT command examples
tldr waft

# View specific subcommand
tldr waft-new

# View Cursor command examples
tldr waft-docs
tldr waft-status

# Search for commands
tldr --search "verify"
```

---

## Notes

- tldr pages are example-driven (not comprehensive documentation)
- Each example should be a real, working command
- Examples are ordered from most common to least common
- Use `-` for short flags, `--` for long flags
- Keep descriptions concise (one line)
- Focus on practical, everyday usage
