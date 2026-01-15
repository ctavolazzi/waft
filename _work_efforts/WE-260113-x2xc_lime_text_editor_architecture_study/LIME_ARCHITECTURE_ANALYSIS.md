# Lime Text Editor Architecture Analysis

**Date**: 2026-01-13  
**Work Effort**: WE-260113-x2xc  
**Status**: Research Phase Complete

---

## Overview

Lime is an open-source, API-compatible alternative to Sublime Text written in Go. The project follows a clear backend/frontend separation architecture, allowing multiple frontend implementations (QML GUI, Termbox terminal, HTML web) to share the same backend engine.

**Repository**: `limetext/lime` (meta project)  
**Backend**: `limetext/lime-backend` (Go, ~10,263 lines of code, 61 files)  
**Frontends**: 
- `limetext/lime-qml` (Qt QML GUI)
- `limetext/lime-termbox` (Terminal UI)
- `limetext/lime-html` (HTML/Web proof of concept)

**Status**: Backend is "not too far away" from completion, frontends are not ready for daily use

---

## Core Architecture

### Two-Layer Separation

Lime uses a **strict backend/frontend separation**:

1. **Backend (`lime-backend`)** - Core engine in Go
   - Text buffer management
   - Syntax highlighting
   - Command system
   - Plugin/package system
   - Settings hierarchy
   - Key bindings
   - Undo/redo system

2. **Frontend** - UI implementation (multiple options)
   - Implements `Frontend` interface
   - Handles rendering
   - Captures user input
   - Displays dialogs/messages

### Frontend Interface

The backend defines a minimal `Frontend` interface that all frontends must implement:

```go
type Frontend interface {
    VisibleRegion(*View) text.Region
    Show(*View, text.Region)
    StatusMessage(string)
    ErrorMessage(string)
    MessageDialog(string)
    OkCancelDialog(msg string, okname string) bool
    Prompt(title, folder string, flags int) []string
}
```

This interface is **intentionally minimal** - it only defines what the backend needs from the frontend, not how the frontend should be implemented.

---

## Backend Architecture

### Core Components

#### 1. Editor (Singleton)

The `Editor` struct is the central coordinator:

```go
type Editor struct {
    text.HasSettings
    keys.HasKeyBindings
    *watch.Watcher
    windows          []*Window
    activeWindow     *Window
    cmdHandler       commandHandler
    console          *View
    frontend         Frontend
    keyInput         chan (keys.KeyPress)
    clipboard        clipboard.Clipboard
    // ... settings, packages, syntaxes, etc.
}
```

**Responsibilities**:
- Manages all windows
- Handles input events
- Coordinates file watching
- Manages packages/plugins
- Provides console view
- Routes commands

**Key Pattern**: Singleton with `GetEditor()` function ensures single instance.

#### 2. Window

Represents an editor window (can have multiple open):

```go
type Window struct {
    text.HasSettings
    text.HasId
    views       []*View
    active_view *View
    project     *Project
    lock        sync.Mutex
}
```

**Responsibilities**:
- Manages multiple views (tabs/panes)
- Tracks active view
- Associates with project
- Provides window-level settings

#### 3. View

A "view" into a specific buffer (multiple views can share same buffer):

```go
type View struct {
    text.HasSettings
    text.HasId
    window           *Window
    buffer           text.Buffer
    selection        text.RegionSet
    undoStack        UndoStack
    scratch          bool
    overwrite        bool
    cursyntax        string
    syntax           parser.SyntaxHighlighter
    regions          render.ViewRegionMap
    // ... settings hierarchy
}
```

**Key Concept**: Multiple `View` instances can share the same `text.Buffer`. This enables:
- Split view of same file
- Different syntax highlighting in different views
- Different settings per view

**Responsibilities**:
- Manages text buffer
- Handles selections
- Syntax highlighting
- Undo/redo
- View-specific settings

#### 4. Command System

Three types of commands:

```go
// Application-level commands
type ApplicationCommand interface {
    Command
    Run() error
    IsChecked() bool
}

// Window-level commands
type WindowCommand interface {
    Command
    Run(*Window) error
}

// Text/view-level commands
type TextCommand interface {
    Command
    Run(*View, *Edit) error
}
```

**Command Interface**:
```go
type Command interface {
    IsEnabled() bool
    IsVisible() bool
    Description() string
    BypassUndo() bool
}
```

**Key Pattern**: Commands are registered with the `commandHandler` and can be invoked by name with arguments.

#### 5. Settings Hierarchy

Settings use a **nested parent-child hierarchy**:

```
default <- platform <- user(editor)
```

When a setting is requested, it walks up the hierarchy until found. This allows:
- Default settings at base level
- Platform-specific overrides
- User customizations

**Settings are attached to**:
- Editor (global)
- Window (window-level)
- View (view-level)
- Project (project-level)

#### 6. Package System

Packages are loaded from directories and can be:
- Syntax definitions
- Color schemes
- Key bindings
- Commands/plugins
- Settings

**Package Interface**:
```go
type Package interface {
    Load()
    UnLoad()
    Name() string
    Path() string
}
```

**Package Discovery**: Uses a registration system where package types register themselves with `Check` and `Action` functions.

#### 7. Key Bindings

Key bindings map key sequences to commands:

```go
type KeyBinding struct {
    Keys     []KeyPress
    Command  string
    Args     Args
    Context  []QueryContextCallback
}
```

**Context System**: Key bindings can have multiple contexts, allowing the same key sequence to have different meanings based on context (e.g., in command mode vs. insert mode).

---

## Frontend Implementations

### QML Frontend (`lime-qml`)

**Technology**: Qt QML (declarative UI)

**Architecture**:
- Uses QML files for UI definition (`Window.qml`, `View.qml`, etc.)
- Go code implements `Frontend` interface
- Batched QML updates (60fps rendering)
- Event-driven with callbacks

**Key Features**:
- Tab-based interface
- Syntax highlighting rendering
- File dialogs
- Message dialogs
- Status bar

**Pattern**: QML objects are created from Go, and Go code updates QML properties through batched change notifications.

### Termbox Frontend (`lime-termbox`)

**Technology**: Termbox-go (terminal UI library)

**Architecture**:
- Direct terminal rendering
- Event loop with termbox
- Layout management for views
- Console rendering

**Key Features**:
- Terminal-based interface
- Line numbers
- Status bar
- Cursor blinking
- Resize handling

**Pattern**: Direct cell-by-cell rendering to terminal, with layout calculations for view positioning.

### HTML Frontend (`lime-html`)

**Technology**: HTML/JavaScript (proof of concept)

**Status**: Minimal implementation, proof of concept only

---

## Design Patterns Identified

### 1. Backend/Frontend Separation

**Pattern**: Strict separation with minimal interface

**Benefits**:
- Multiple frontend implementations possible
- Backend can be tested independently
- Frontend technology can change without backend changes

**WAFT Insight**: Similar to WAFT's substrate/memory/agents separation - clear boundaries between layers.

### 2. Singleton Editor

**Pattern**: Global `Editor` instance accessed via `GetEditor()`

**Benefits**:
- Single source of truth
- Easy access from anywhere
- Centralized state management

**Trade-offs**:
- Harder to test (global state)
- Not thread-safe by default (uses mutexes)

### 3. Settings Hierarchy

**Pattern**: Parent-child settings with inheritance

**Benefits**:
- Defaults at base level
- Platform-specific overrides
- User customizations
- Project-specific settings

**WAFT Insight**: Similar to WAFT's configuration layers (global, project, command).

### 4. View/Buffer Separation

**Pattern**: Multiple views can share same buffer

**Benefits**:
- Split view of same file
- Different settings per view
- Different syntax highlighting

**WAFT Insight**: Could apply to WAFT's document viewing/editing.

### 5. Command Pattern

**Pattern**: Commands as first-class objects with registration

**Benefits**:
- Extensible command system
- Commands can be invoked by name
- Commands can have arguments
- Commands can be enabled/disabled

**WAFT Insight**: Similar to WAFT's command system, but more structured.

### 6. Package System

**Pattern**: Plugin/package system with discovery

**Benefits**:
- Extensible architecture
- Hot-loading of packages
- File watching for changes

**WAFT Insight**: Could inform WAFT's plugin/extensibility system.

### 7. Event System

**Pattern**: Observer pattern with callbacks

**Events**:
- `OnNew` - New view created
- `OnClose` - View closed
- `OnLoad` - File loaded
- `OnModified` - Buffer modified
- `OnSelectionModified` - Selection changed

**Benefits**:
- Decoupled components
- Frontend can react to backend changes
- Multiple observers per event

---

## API Compatibility with Sublime Text

### Goal

Lime aims to be **API-compatible** with Sublime Text to support existing plugins without modification.

### Implementation Strategy

1. **Package Format**: Uses same `.sublime-settings`, `.sublime-keymap` formats
2. **Command Names**: Uses same command names
3. **Settings Keys**: Uses same setting keys
4. **Plugin API**: Implements Sublime Text plugin API (Python-based)

### Plugin System

Plugins are written in Python and use Sublime Text's API:

```python
import sublime
import sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.insert(edit, 0, "Hello, World!")
```

Lime provides a Python runtime that implements the `sublime` and `sublime_plugin` modules.

---

## Code Organization

### Backend Structure

```
lime-backend/
├── editor.go          # Editor singleton
├── window.go          # Window management
├── view.go            # View management
├── command.go         # Command interfaces
├── commandhandler.go  # Command execution
├── frontend.go        # Frontend interface
├── packages/          # Package system
│   ├── package.go
│   ├── json.go
│   └── watcher.go
├── keys/              # Key binding system
│   ├── key.go
│   ├── keybinding.go
│   └── keycontext.go
├── render/            # Rendering system
│   ├── renderer.go
│   └── view.go
├── parser/            # Syntax parsing
│   └── parser.go
├── log/               # Logging
└── watch/             # File watching
```

### Package Organization

- **Single package**: All backend code in `backend` package
- **Sub-packages**: Organized by functionality (keys, render, packages, etc.)
- **Interfaces**: Clear interfaces for extensibility
- **Tests**: Comprehensive test coverage

---

## WAFT Integration Insights

### 1. Backend/Frontend Separation → WAFT Layers

**Lime Pattern**: Backend (engine) + Frontend (UI)

**WAFT Equivalent**: 
- **Substrate** (environment) → Backend
- **Memory** (_pyrite) → Backend state
- **Agents** (crewai) → Could be "frontend" layer

**Insight**: WAFT's three-layer model could benefit from Lime's strict interface definition.

### 2. Settings Hierarchy → WAFT Configuration

**Lime Pattern**: default ← platform ← user

**WAFT Equivalent**: 
- Global config (`~/.waft/config.toml`)
- Project config (`_pyrite/.waft/config.toml`)
- Command flags

**Insight**: WAFT already uses similar hierarchy - could formalize it more.

### 3. Command System → WAFT Commands

**Lime Pattern**: Registered commands with arguments

**WAFT Equivalent**: CLI commands

**Insight**: WAFT could benefit from more structured command registration system.

### 4. Package System → WAFT Plugins

**Lime Pattern**: Discoverable packages with Load/UnLoad

**WAFT Equivalent**: Potential plugin system

**Insight**: WAFT could implement similar package discovery for extensions.

### 5. View/Buffer Separation → WAFT Documents

**Lime Pattern**: Multiple views of same buffer

**WAFT Equivalent**: Multiple views of same document

**Insight**: WAFT could support multiple views of same document with different settings.

### 6. Event System → WAFT Observers

**Lime Pattern**: Observer pattern with callbacks

**WAFT Equivalent**: Event system for document changes

**Insight**: WAFT could implement similar event system for document lifecycle.

---

## Key Takeaways

### Strengths

1. **Clear Architecture**: Backend/frontend separation is well-defined
2. **Extensibility**: Package system allows easy extension
3. **API Compatibility**: Goal of Sublime Text compatibility is ambitious
4. **Multiple Frontends**: Proves architecture works with different UIs
5. **Settings Hierarchy**: Flexible configuration system

### Weaknesses

1. **Incomplete**: Project is not ready for daily use
2. **Complexity**: Backend has significant complexity (~10K lines)
3. **Global State**: Singleton editor makes testing harder
4. **Thread Safety**: Requires careful mutex usage

### Lessons for WAFT

1. **Interface Definition**: Clear interfaces enable multiple implementations
2. **Settings Hierarchy**: Parent-child settings are powerful
3. **Command Registration**: Structured command system is extensible
4. **Package Discovery**: File-based package discovery is flexible
5. **Event System**: Observer pattern enables decoupling

---

## Repository Statistics

- **Backend**: ~10,263 lines of Go code across 61 files
- **QML Frontend**: ~539 lines (main frontend implementation)
- **Termbox Frontend**: ~555 lines (terminal implementation)
- **HTML Frontend**: Minimal (proof of concept)

---

## Conclusion

Lime demonstrates a well-architected text editor with clear separation of concerns. The backend/frontend separation allows multiple UI implementations while sharing core functionality. The package system, settings hierarchy, and command system provide extensibility.

For WAFT, the key insights are:
1. **Strict interface definition** enables multiple implementations
2. **Settings hierarchy** provides flexible configuration
3. **Command registration** enables extensibility
4. **Package discovery** allows file-based extensions
5. **Event system** enables decoupled components

The architecture is sound, though the project's incomplete state suggests the complexity may have been underestimated. WAFT can learn from both the successes and challenges of Lime's architecture.
