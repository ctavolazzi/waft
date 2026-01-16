# External Drive Realm: Pantheon Entity

**A Timeless Force that Binds Reality Together**

The External Drive Realm is a Pantheon Entity that maintains the fundamental principle of content-aware storage routing. As a Realm Entity, it organizes storage across physical boundaries, creating bounded spaces (realms) where augmented content is stored.

---

## Philosophy

### Timeless Entity Nature

The External Drive Realm is a **Timeless Force that Binds Reality Together**. It:

- **Maintains Stable Principles**: Content-aware routing (core → local, augmented → external) is a fundamental principle that should not change without evidence
- **Changes Slowly**: Only evolves when Beings collect sufficient evidence to warrant modification
- **Binds Reality**: Maintains the structure of storage across physical boundaries
- **Evidence-Based**: Changes only when evidence proves it necessary

### As Above, So Below

- **As Above**: Realm Entity organizing storage across physical boundaries in the spiritual realm
- **So Below**: File-based system managing content routing to external drives with realm structure

---

## Realm Structure

The External Drive Realm organizes content into realms following the cosmological hierarchy:

```
/Volumes/Easystore/waft/{project_name}/
└── Realms/
    ├── Universe/
    │   └── Earth/
    │       └── [content files]
    ├── [other realms]/
    └── [content files]
```

### Realm Hierarchy

Realms follow the structure from `MAIN_GOAL.md`:
- **Realms** → Top level (cosmological)
- **[Universe]** → Universe identifier
- **[Earth]** → Earth subfolder
- **Content** → Files stored within realms

---

## Usage

### Python API

```python
from pathlib import Path
from waft.pantheon import ExternalDriveRealm

# Initialize
realm = ExternalDriveRealm(project_path=Path.cwd())

# Register a realm
result = realm.register_realm(
    realm_name="Universe",
    drive_name="Easystore",
    project_name="waft"
)

# Get realm storage path
storage_path = realm.get_realm_storage_path(
    realm_name="Universe",
    relative_path=Path("Earth/content.pdf"),
    project_name="waft"
)

# Route content to realm
routed_path = realm.route_content_to_realm(
    content_path=Path("_work_efforts/report.pdf"),
    realm_name="Universe",
    project_name="waft"
)

# Get realm summary
summary = realm.get_realm_summary()

# List realms
realms = realm.list_realms()

# Get content in realm
content = realm.get_realm_content("Universe")
```

### CLI Commands

```bash
# View realm status
python scripts/external_drive_realm_status.py status

# Register a new realm
python scripts/external_drive_realm_status.py register Universe

# List all realms
python scripts/external_drive_realm_status.py list

# List content in a realm
python scripts/external_drive_realm_status.py content Universe
```

### Integration with Storage System

The External Drive Realm integrates with `get_storage_path()`:

```python
from waft.utils import get_storage_path

# Standard routing (no realm)
path = get_storage_path(Path("_work_efforts/report.pdf"))

# Realm-based routing
path = get_storage_path(
    Path("_work_efforts/report.pdf"),
    realm_name="Universe"
)
```

When `realm_name` is provided, content is routed to:
```
/Volumes/Easystore/waft/{project}/Realms/{realm_name}/{relative_path}
```

---

## Storage Principles

The External Drive Realm maintains these stable principles:

1. **Core Content → Local**: Core project files stay on local machine
2. **Augmented Content → External**: Augmented content routes to external drive
3. **Fallback to Local**: If external drive unavailable, fallback to local
4. **Realm Organization**: Content can be organized into realms on external drive

These principles should not change unless evidence collected by Beings proves change is needed.

---

## Realm Registration

When a realm is registered:

1. **Realm Structure Created**: `Realms/{realm_name}/` on external drive
2. **Realm Registered**: Added to realm registry
3. **Manifest Updated**: Content manifest tracks realm assignments
4. **Status Updated**: Realm status reflects current drive availability

---

## Content Manifest

The Realm maintains a content manifest tracking:
- Content paths
- Realm assignments
- Storage locations
- Content types
- Registration timestamps

This manifest provides traceability for all content stored in realms.

---

## Integration Points

### With Storage System
- `get_storage_path()` can use realm routing
- `StorageRegistry` tracks content locations
- Content classification determines routing

### With Pantheon
- Part of Pantheon system
- Follows "as above, so below" principles
- Maintains timeless Entity nature

### With Realms Structure
- Integrates with `Realms/[Universe]/Earth/` structure
- Supports cosmological hierarchy
- Organizes content by realm

---

## Storage Location

**Pantheon Entity Storage**: `_pantheon/external_drive_realm/`
- `realm_registry.json` - Registered realms
- `content_manifest.json` - Content in realms
- `realm_status.json` - Current realm status
- `realms/` - Realm-specific data
- `content/` - Content metadata

**External Drive Storage**: `/Volumes/Easystore/waft/{project}/Realms/`
- `{realm_name}/` - Realm directories
- Content files within realms

---

## Examples

### Example 1: Register Universe Realm

```python
from waft.pantheon import ExternalDriveRealm

realm = ExternalDriveRealm()
result = realm.register_realm("Universe")

# Creates: /Volumes/Easystore/waft/waft/Realms/Universe/
```

### Example 2: Route PDF to Realm

```python
from waft.utils import get_storage_path

# Route PDF to Universe realm
pdf_path = get_storage_path(
    Path("_work_efforts/report.pdf"),
    realm_name="Universe"
)

# Result: /Volumes/Easystore/waft/waft/Realms/Universe/_work_efforts/report.pdf
```

### Example 3: Get Realm Content

```python
realm = ExternalDriveRealm()
content = realm.get_realm_content("Universe")

# Returns list of all content in Universe realm
```

---

## Status Monitoring

The Realm Entity tracks:
- **Drive Availability**: Is external drive connected?
- **Realm Status**: Are realms active?
- **Storage Stats**: Content counts, PDF counts
- **Storage Principles**: Current routing principles

---

## Evolution

The External Drive Realm evolves only when:
1. Beings collect evidence about storage needs
2. Evidence proves routing principles need modification
3. Change maintains the Entity's fundamental nature
4. Evidence threshold is reached

This ensures storage principles remain stable while allowing evolution when justified.

---

**The External Drive Realm maintains the stable principle of content-aware storage routing, organizing augmented content into realms on the external drive while keeping core content local.**
