# Spawn with CV

**Spawn a new Being with an automatically generated CV in its personnel file.**

Creates a new Being entity and generates a professional CV using the brilliant-cv Typst template. The CV is stored in the Being's personnel file directory.

**Use when:** Need to create a Being with documentation, want to showcase Being capabilities, or need a Being with a complete personnel record.

---

## Purpose

This command provides:
- **Being Creation**: Spawns new Being entity (same as `/spawn`)
- **CV Generation**: Automatically generates CV from Being data
- **Personnel File**: Creates organized personnel directory structure
- **PDF Output**: Compiles CV to PDF using Typst
- **Bureaucracy Integration**: Registers Being with God of Bureaucracy

---

## Philosophy

### 1. Being as Employee

Beings with CVs are treated as employees in the bureaucracy:
- **Skills** → Technical/Soft Skills sections
- **Memories** → Work Experience entries
- **Lessons** → Achievements/Projects
- **Ancestral Chain** → Education/Training
- **Personality** → Summary/About section

### 2. Personnel Files

Each Being gets a personnel file directory:
```
_hidden/.truth/beings/{being_id}/
├── being.json              # Being data
├── personnel/
│   ├── cv.typ              # Typst source
│   ├── cv.pdf              # Compiled PDF
│   ├── metadata.toml       # CV metadata
│   └── modules_en/         # CV content modules
```

### 3. Bureaucracy Realm

Beings with CVs are registered with the God of Bureaucracy:
- Maintains registry of all Beings with personnel files
- Tracks CV versions and updates
- Manages Being employment records

---

## Execution Steps

### Step 1: Spawn Being

**Purpose**: Create the Being entity

**Actions**:
1. Use standard `/spawn` logic to create Being
2. Accept same parameters as `/spawn`:
   - `--reality <reality_id>` (optional)
   - `--parent <parent_being_id>` (optional)
   - `--skills <json>` (optional)

**Output**: Created Being instance

---

### Step 2: Generate Personnel File Structure

**Purpose**: Create directory structure for Being's personnel file

**Actions**:
1. Create `_hidden/.truth/beings/{being_id}/personnel/` directory
2. Set permissions (0o700)
3. Create subdirectories:
   - `modules_en/` (for CV content)

**Output**: Personnel file directory structure

---

### Step 3: Generate CV Content

**Purpose**: Create Typst CV from Being data

**Actions**:
1. Map Being data to CV format using `being_cv_mapper`
2. Generate Typst files using `brilliant_cv` wrapper:
   - `metadata.toml` - Personal info and layout
   - `cv.typ` - Main CV document
   - `modules_en/experience.typ` - Work experience
   - `modules_en/skills.typ` - Skills section
   - `modules_en/education.typ` - Education section
3. Write all files to personnel directory

**Output**: Complete Typst CV source files

---

### Step 4: Compile CV to PDF

**Purpose**: Generate PDF from Typst source

**Actions**:
1. Use `TypstCompiler` to compile `cv.typ`
2. Output PDF to `personnel/cv.pdf`
3. Handle compilation errors gracefully (Being still created)

**Output**: `cv.pdf` in personnel directory

---

### Step 5: Register with Bureaucracy

**Purpose**: Register Being with God of Bureaucracy

**Actions**:
1. Initialize `BureaucracyGod` (creates realm if needed)
2. Register Being's personnel file:
   - Being ID
   - Personnel file path
   - CV generation timestamp
   - CV version (initial: 1.0)
3. Update bureaucracy registry

**Output**: Being registered in bureaucracy system

---

## Usage Examples

### Basic Usage

```
/spawn-with-cv
```

Creates a Being with default settings and generates CV.

### With Reality

```
/spawn-with-cv --reality "bureaucracy_realm"
```

Spawns Being into bureaucracy realm and generates CV.

### With Skills

```
/spawn-with-cv --skills '{"documentation": 50.0, "organization": 45.0}'
```

Creates Being with specific skills, reflected in CV.

### With Parent

```
/spawn-with-cv --parent "being_20260119_123456_abc12345"
```

Spawns Being from parent, inherits skills (shown in CV).

---

## Output Structure

### Personnel File Directory

```
_hidden/.truth/beings/{being_id}/
├── {being_id}.json          # Being data (standard)
├── personnel/               # Personnel file (NEW)
│   ├── cv.typ              # Typst source
│   ├── cv.pdf              # Compiled PDF
│   ├── metadata.toml       # CV configuration
│   └── modules_en/         # CV content modules
│       ├── experience.typ
│       ├── skills.typ
│       └── education.typ
```

### CV Content Mapping

- **Personal Info**: From Being ID, custom_name, reality_id
- **Experience**: From Being memories (work/experience type)
- **Skills**: From Being.skills (technical >50, soft ≤50)
- **Education**: From Being ancestral_chain
- **Projects**: From Being lessons_learned
- **Summary**: From Being personality

---

## Integration Points

### Being System
- Uses standard `BeingSystem.spawn_being()`
- Extends Being creation with CV generation
- Maintains Being data integrity

### Typst System
- Uses `TypstCompiler` for PDF generation
- Uses `brilliant_cv` wrapper for template
- Handles Typst compilation errors gracefully

### Bureaucracy Realm
- Registers Being with `BureaucracyGod`
- Maintains personnel file registry
- Tracks CV versions and updates

---

## Error Handling

### Typst Not Available
- Being is still created
- Typst source files are generated
- PDF compilation is skipped
- Warning message displayed

### CV Generation Fails
- Being is still created
- Error logged to Being's personnel file
- Can retry CV generation later

### Bureaucracy Registration Fails
- Being is still created
- CV is still generated
- Warning message displayed
- Can register manually later

---

## Related Commands

- **`/spawn`**: Spawn Being without CV
- **`/bureaucracy-register`**: Register existing Being with bureaucracy
- **`/bureaucracy-list`**: List all Beings with personnel files

---

## Notes

- CV uses brilliant-cv template v3.1.1
- Requires Typst CLI (optional, graceful degradation)
- Personnel files are stored in Being's directory
- CV can be regenerated/updated later
- Bureaucracy realm is auto-created if needed
