// WAFT REALMS SYSTEM
// Managing Simulation Universes

#import "@preview/showybox:2.0.4": showybox

#set document(title: "Realms System", author: "WAFT Documentation")
#set page(paper: "us-letter", margin: 1in)
#set text(font: "New Computer Modern", size: 10pt)

#let primary = rgb("#6b46c1")

#align(center)[
  #rect(fill: gradient.linear(primary, primary.darken(30%)), width: 100%, inset: 2em)[
    #text(fill: white, size: 24pt, weight: "bold")[REALMS SYSTEM]
    #v(0.3em)
    #text(fill: white.darken(10%), size: 12pt)[WAFT | Managing Simulation Universes]
  ]
]

#v(1em)

= What is a Realm?

A *Realm* is a top-level simulation container in WAFT. It holds multiple realities, corporations, and beings within a shared context.

#showybox(
  frame: (border-color: primary, body-color: primary.lighten(95%)),
  title: "Key Concept",
)[
  Think of Realms as "universes" — each with its own physics, history, and inhabitants. Realities exist within Realms.
]

= Realm Structure

```
_realms/
├── bureaucracy_realm/           # Corporate simulation realm
│   ├── manifest.json            # Realm metadata
│   ├── corporations/            # All corporations
│   │   └── teleport_massive_20250701/
│   │       ├── manifest.json
│   │       ├── founders.json
│   │       ├── departments/
│   │       └── employees/
│   └── history/                 # Realm-wide events
├── fantasy_realm/               # (Example) Fantasy setting
└── scifi_realm/                 # (Example) Sci-fi setting
```

= The Bureaucracy Realm

The default realm for corporate simulations. Contains Teleport Massive and any other corporations you create.

#grid(
  columns: 2,
  gutter: 1em,
  showybox(frame: (border-color: blue, body-color: blue.lighten(95%)))[
    *Features*
    - Corporate hierarchies
    - Economic simulation
    - Department management
    - Employee tracking
  ],
  showybox(frame: (border-color: green, body-color: green.lighten(95%)))[
    *Contents*
    - Teleport Massive corp
    - Founder Beings
    - Research history
    - Financial records
  ],
)

= Creating Realms

```python
from waft.realms import RealmSystem

realms = RealmSystem(project_path=Path("."))

# Create a new realm
realm = realms.create_realm(
    name="my_custom_realm",
    description="A realm for my experiments",
    physics_rules={
        "time_flow": "linear",
        "causality": "strict",
    }
)
```

= Realm Operations

```bash
# List realms
waft realms list

# Create realm
waft realms create fantasy_realm

# Show realm info
waft realms info bureaucracy_realm

# Export realm
waft realms export bureaucracy_realm --output realm.zip
```

= Cross-Realm Operations

Beings can theoretically move between realms (experimental):

```python
# Transfer Being to another realm
realms.transfer_being(
    being_id="abc-123",
    source_realm="bureaucracy_realm",
    target_realm="fantasy_realm",
    preserve_memories=True,
)
```

#showybox(frame: (border-color: orange, body-color: orange.lighten(95%)))[
  *Warning:* Cross-realm transfers may cause memory conflicts if realm physics differ significantly.
]

= Realm Manifest

Each realm has a `manifest.json`:

```json
{
  "realm_id": "bureaucracy_realm",
  "name": "Bureaucracy Realm",
  "created": "2025-07-01T00:00:00Z",
  "description": "Corporate simulation environment",
  "physics": {
    "time_flow": "linear",
    "causality": "strict",
    "scint_enabled": true
  },
  "statistics": {
    "corporations": 1,
    "beings": 5,
    "total_events": 247
  }
}
```

#v(1em)

#align(center)[
  #rect(fill: primary, inset: 1em)[
    #text(fill: white)[REALMS | Universes Within Universes]
  ]
]
