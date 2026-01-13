# Resurrect

**Create a ProtoCel - self-contained evolving cell that observes and interacts with beings.**

Creates a ProtoCel: a self-contained cell that lives in its own folder, has its own API, can peer outside itself to observe/interact with beings, and evolves itself based on usage patterns. The cell is encapsulated but can communicate with the outside world via its API.

**Use when:** Want to create a self-contained evolving system that can observe and interact with beings, or need an encapsulated cell that evolves based on usage.

---

## Purpose

This command provides:
- **ProtoCel Creation**: Create a new self-contained evolving cell
- **Being Observation**: ProtoCel can observe beings from outside
- **Being Interaction**: ProtoCel can interact with beings via API
- **Evolution System**: ProtoCel evolves based on usage patterns
- **Self-Contained Structure**: ProtoCel lives in its own folder with own API

---

## Philosophy

1. **Self-Contained**: ProtoCel is encapsulated in its own folder
2. **Observable**: Can peer outside to observe beings
3. **Interactive**: Can interact with beings via API
4. **Evolving**: Evolves based on usage patterns
5. **Encapsulated**: Isolated but can communicate via API

---

## Execution Steps

### Resurrect 1.1: Create ProtoCel
**Purpose**: Create a new ProtoCel

**Steps**:
1. Get optional name and description from user
2. Create ProtoCel using ProtoCelSystem
3. Initialize ProtoCel folder structure
4. Set up API endpoints
5. Initialize usage patterns

**Output**: Created ProtoCel with ID

---

### Resurrect 1.2: Set Up ProtoCel Structure
**Purpose**: Create ProtoCel folder structure

**Steps**:
1. Create ProtoCel folder in `_hidden/.truth/protocels/`
2. Create subdirectories:
   - `api/` - API endpoints
   - `observations/` - Being observations
   - `evolution/` - Evolution records
3. Create `state.json` for ProtoCel state
4. Initialize usage patterns

**Output**: ProtoCel folder structure created

---

### Resurrect 1.3: Register API Endpoints
**Purpose**: Register ProtoCel API endpoints

**Steps**:
1. Register ProtoCel API routes
2. Enable being observation endpoints
3. Enable being interaction endpoints
4. Enable evolution endpoints
5. Document API endpoints

**Output**: API endpoints registered

---

### Resurrect 1.4: Initialize Evolution System
**Purpose**: Set up evolution tracking

**Steps**:
1. Initialize usage pattern tracking
2. Set up evolution triggers
3. Configure fitness calculation
4. Set up mutation system
5. Initialize generation counter

**Output**: Evolution system initialized

---

## Execution Flow

```
Resurrect 1.1: Create ProtoCel
  ↓
Resurrect 1.2: Set Up ProtoCel Structure
  ↓
Resurrect 1.3: Register API Endpoints
  ↓
Resurrect 1.4: Initialize Evolution System
  ↓
✅ Complete - ProtoCel created and ready
```

---

## Output Format

### Console Output

The command displays ProtoCel creation summary:

```
🔬 Resurrect: ProtoCel Creation

ProtoCel Created:
  ID: protocel_20260112_194054_a1b2c3d4
  Name: ProtoCel_a1b2c3d4
  Description: Self-contained evolving cell
  State: active
  Generation: 0
  Fitness: 0.0

Structure:
  Cell Path: _hidden/.truth/protocels/protocel_20260112_194054_a1b2c3d4/
  API Path: _hidden/.truth/protocels/protocel_20260112_194054_a1b2c3d4/api/
  Observations: _hidden/.truth/protocels/protocel_20260112_194054_a1b2c3d4/observations/
  Evolution: _hidden/.truth/protocels/protocel_20260112_194054_a1b2c3d4/evolution/

API Endpoints:
  POST /api/protocel/create - Create new ProtoCel
  GET /api/protocel/list - List all ProtoCels
  GET /api/protocel/{id} - Get ProtoCel state
  POST /api/protocel/{id}/observe - Observe a being
  POST /api/protocel/{id}/interact - Interact with a being
  POST /api/protocel/{id}/evolve - Trigger evolution

Evolution System:
  Triggers: Every 10 interactions
  Fitness: Based on diversity and activity
  Mutations: Pattern-based enhancements

✅ ProtoCel ready for observation and interaction
```

---

## ProtoCel Structure

### Folder Structure

```
_hidden/.truth/protocels/
└── protocel_{id}/
    ├── api/              # API endpoints
    ├── observations/     # Being observations
    ├── evolution/        # Evolution records
    └── state.json        # ProtoCel state
```

### State File

The `state.json` file contains:
- ProtoCel ID, name, description
- Current state (creating, active, evolving, sleeping, archived)
- Generation and fitness
- Usage patterns
- Observed and interacted beings
- Mutation history

---

## Use Cases

### 1. Create ProtoCel for Being Observation
**Scenario**: Want to observe beings from a self-contained cell

**Example**:
```
User: "/resurrect"
AI: [Creates ProtoCel]
User: "Observe being abc123"
AI: [ProtoCel observes being via API]
```

**Output**: ProtoCel created and observing beings

---

### 2. Create ProtoCel for Being Interaction
**Scenario**: Want to interact with beings from a self-contained cell

**Example**:
```
User: "/resurrect --name 'Observer Cell'"
AI: [Creates named ProtoCel]
User: "Interact with being abc123"
AI: [ProtoCel interacts with being via API]
```

**Output**: ProtoCel created and interacting with beings

---

### 3. Create ProtoCel for Evolution Study
**Scenario**: Want to study evolution patterns

**Example**:
```
User: "/resurrect --description 'Evolution study cell'"
AI: [Creates ProtoCel]
User: [ProtoCel evolves based on usage]
AI: [Shows evolution results]
```

**Output**: ProtoCel created and evolving

---

## Integration with Other Commands

- **`/evolve`**: Evolves beings (`/resurrect` creates evolving cells)
- **`/status`**: Shows status (`/resurrect` creates new system)
- **Being API**: ProtoCel uses being API for observation/interaction

---

## When to Use

**Use `/resurrect` when**:
- ✅ Want to create a self-contained evolving cell
- ✅ Need to observe beings from an encapsulated system
- ✅ Want to interact with beings via API
- ✅ Need evolution based on usage patterns
- ✅ Want isolated but communicative system

**Don't use `/resurrect` when**:
- ❌ Need direct being manipulation (use being API directly)
- ❌ Don't need encapsulation (use being system directly)
- ❌ Don't need evolution (use simpler observation system)

---

## Technical Details

### Tools Used

**ProtoCel System**:
- `ProtoCelSystem` - Manages ProtoCels
- `ProtoCel` - Individual ProtoCel instance
- File system for state persistence
- JSON for state storage

**API Integration**:
- FastAPI routes for ProtoCel API
- Being API for observation/interaction
- REST endpoints for external access

**Evolution System**:
- Usage pattern tracking
- Fitness calculation
- Mutation generation
- Generation tracking

### Performance

- **Target Time**: < 5 seconds
- **ProtoCel Creation**: ~1 second
- **Structure Setup**: ~1 second
- **API Registration**: ~1 second
- **Evolution Init**: ~1 second
- **State Save**: ~1 second

### Error Handling

- **Creation Errors**: Show error, don't create partial ProtoCel
- **API Errors**: Show error, continue with creation
- **State Errors**: Show error, attempt recovery
- **Always Complete**: Always show creation status

---

## Example Workflow

```
User: "/resurrect --name 'Observer Cell' --description 'Cell for observing beings'"

AI: 🔬 Resurrect: ProtoCel Creation

ProtoCel Created:
  ID: protocel_20260112_194054_a1b2c3d4
  Name: Observer Cell
  Description: Cell for observing beings
  State: active

API Endpoints:
  POST /api/protocel/protocel_20260112_194054_a1b2c3d4/observe
  POST /api/protocel/protocel_20260112_194054_a1b2c3d4/interact

✅ ProtoCel ready

User: "Observe being abc123"
AI: [ProtoCel observes being, records observation, checks evolution]

User: [ProtoCel evolves after 10 interactions]
```

---

## Advanced Features

### Named ProtoCels
Create ProtoCel with custom name:
```bash
/resurrect --name "My Observer Cell"
```

### Custom Description
Add description:
```bash
/resurrect --description "Cell for studying being patterns"
```

### Evolution Triggers
Configure evolution:
```bash
/resurrect --evolution-trigger 20  # Evolve every 20 interactions
```

### Being Focus
Focus on specific beings:
```bash
/resurrect --focus-being abc123  # Focus on specific being
```

---

## Best Practices

1. **Name Clearly**: Use descriptive names for ProtoCels
2. **Document Purpose**: Add descriptions explaining purpose
3. **Monitor Evolution**: Track evolution patterns
4. **Review Observations**: Review being observations regularly
5. **Manage Lifecycle**: Archive old ProtoCels when done

---

## Output Location

ProtoCel is created in:
- `_hidden/.truth/protocels/{protocel_id}/`

API endpoints available at:
- `/api/protocel/{protocel_id}/...`

State and observations stored in ProtoCel folder.

---

**This command creates a self-contained evolving cell that can observe and interact with beings - perfect for encapsulated evolutionary systems.**
