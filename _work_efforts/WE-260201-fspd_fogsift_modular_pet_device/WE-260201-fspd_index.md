---
id: WE-260201-fspd
title: "fogsift_modular_pet_device"
status: active
created: 2026-02-01T20:00:00.000Z
created_by: ctavolazzi
last_updated: 2026-02-01T20:00:00.000Z
branch: claude/general-session-yXO5a
repository: waft
---

# WE-260201-fspd: FogSift Modular Pet Device

## Metadata
- **Created**: Saturday, February 1, 2026
- **Author**: ctavolazzi
- **Repository**: waft
- **Branch**: claude/general-session-yXO5a

## Vision

A modular tamagotchi-style device with:
- Walnut wood enclosure with rounded corners
- Small pixel-art display showing creatures/environments
- Magnetic edge connectors for linking multiple units
- When units connect, displays merge (creatures meet, landscapes extend)
- Companion app for stats and creature management
- Special editions: Cosmic, Artist Series, glow variants

## Core Concept

**"Link them together, watch worlds connect"**

Each device is a standalone pet/environment. When physically connected via magnets:
- Creatures can interact across screens
- Landscapes tile seamlessly
- New gameplay emerges from combinations
- Social/trading mechanics enabled

## Use Cases

1. **Desktop companion** - Single unit as ambient pixel pet
2. **Modular display** - Multiple units forming larger scenes
3. **Tabletop gaming** - Integrated into gaming tables
4. **Wall art** - Mounted configurations
5. **Collectible** - Limited editions, artist collaborations

## Tickets

| ID | Title | Status |
|----|-------|--------|
| TKT-fspd-001 | Hardware specification document | pending |
| TKT-fspd-002 | Creature mechanics game design doc | pending |
| TKT-fspd-003 | Magnetic connection protocol design | pending |
| TKT-fspd-004 | Display/MCU selection research | pending |
| TKT-fspd-005 | YouTube Episode 1 script | pending |
| TKT-fspd-006 | Prototype BOM (Bill of Materials) | pending |
| TKT-fspd-007 | Firmware architecture outline | pending |
| TKT-fspd-008 | WAFT Pet System integration plan | pending |

## Hardware Requirements (Initial)

### Display
- Small form factor (1.5" - 2" diagonal)
- Pixel-art aesthetic (low-res is intentional)
- IPS or OLED for viewing angles
- Low power consumption

### Compute
- ESP32 or similar (WiFi/BLE for app connectivity)
- Low power sleep modes
- Sufficient GPIO for buttons, magnets, display

### Power
- Rechargeable Li-Po battery
- USB-C charging
- Target: 24+ hours active, days in sleep mode

### Enclosure
- Walnut wood or wood-look material
- Rounded corners, premium feel
- Magnetic connection points on edges
- Two physical buttons (minimum)

### Connectivity
- Magnetic pogo pins for device-to-device communication
- BLE for app companion
- WiFi for updates/cloud sync (optional)

## Software Architecture

### Firmware
- Creature state machine (mood, hunger, energy)
- Display rendering (pixel art sprites, animations)
- Neighbor detection (magnetic connection events)
- Inter-device communication protocol
- BLE/WiFi stack for app

### Companion App
- Creature stats and history
- Multi-device management
- Cloud backup (optional)
- Social features (creature trading?)

### WAFT Integration
- Pet System module for creature AI/behavior simulation
- Evolution mechanics from Scint Gym concepts
- Creature breeding/genetics
- Procedural creature generation

## YouTube Content Plan

### Episode 1: "I'm building a modular tamagotchi"
- Show concept renders
- Explain the magnetic link mechanic
- Overview of what needs to be built
- Tease next episode

### Episode 2: "Choosing the brain and screen"
- MCU comparison (ESP32, RP2040, etc.)
- Display options and tradeoffs
- Power budget calculations

### Episode 3: "First prototype PCB"
- Schematic walkthrough
- PCB layout process
- Ordering from manufacturer

### Episode 4+: Build progression...

## Manufacturing Notes

- Connections: [names redacted] - can help with manufacturing
- Wood enclosure: CNC or injection mold with wood-fill?
- PCB: Standard fab house (JLCPCB, PCBWay)
- Assembly: Hand assembly for prototypes, consider PCBA for production

## Progress

- 2/1/2026: Work effort created. Concept renders complete. Beginning documentation phase.

## Related

- WE-260120-1sbq: Pet System Implementation (WAFT creature logic)
- WE-260126-fogsift-rebrand: FogSift brand direction
- @FogSift YouTube channel

## Assets

Concept renders stored locally (not in repo):
- Immersive tabletop gaming mockup
- Modular system configurations
- Packaging design (kraft box, leaf logo)
- Wood enclosure variants
- Special editions (Cosmic, Artist Series)
