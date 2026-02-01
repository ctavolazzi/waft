# FogSift Prototype Roadmap

## Phase 0: Software Simulation (Filmable Now)

Before any hardware, validate the game design in software.

### Episode Ideas
- "Testing my tamagotchi's brain before it has a body"
- "Simulating 1000 generations to find the perfect pet"

### Tasks
- [ ] Port CREATURE_MECHANICS.md to Python simulation
- [ ] Use WAFT Pet System as foundation
- [ ] Build terminal-based creature (ASCII art)
- [ ] Test linking logic with two processes
- [ ] Record simulation running, voice over the mechanics

### Output
- Validated stat decay rates
- Tested evolution triggers
- Breeding probability feels right
- Mini-game timing tuned

---

## Phase 1: Display Proof-of-Concept

### Goal
Get pixels moving on a real screen.

### Components
| Part | Options | Cost Range |
|------|---------|------------|
| Display | 1.3" TFT (ST7789), 1.54" IPS | $5-15 |
| MCU | ESP32-S3, RP2040 | $5-10 |
| Dev board | Waveshare, Adafruit | $15-25 |

### Episode Ideas
- "Choosing a screen for my tamagotchi"
- "First pixels: my pet has eyes"

### Tasks
- [ ] Order 2-3 display options
- [ ] Compare brightness, viewing angles, power draw
- [ ] Port pixel art to display (MicroPython or C)
- [ ] Film the comparison test

### Milestone
Creature sprite animating on physical display.

---

## Phase 2: Input & Interaction

### Goal
Buttons that feel good.

### Components
| Part | Notes |
|------|-------|
| Tactile switches | Clicky, satisfying |
| Capacitive touch | Clean look, no moving parts |
| Side buttons | Like Game Boy Micro |

### Episode Ideas
- "Finding the perfect button click"
- "Making my tamagotchi respond"

### Tasks
- [ ] Wire up 2 buttons to dev board
- [ ] Implement basic input handling
- [ ] Test button combos from CREATURE_MECHANICS.md
- [ ] Film the tactile comparison

### Milestone
Feed and play with creature via physical buttons.

---

## Phase 3: The Magnetic Link

### Goal
Two devices communicate when physically connected.

### The Magic Moment
This is the core innovation. Film it well.

### Technical Approach
```
Device A                Device B
┌──────┐                ┌──────┐
│ ┌──┐ │◄──magnets───►│ ┌──┐ │
│ └──┘ │   pogo pins   │ └──┘ │
└──────┘                └──────┘
     │                      │
     └──────── I2C ────────┘
           or UART
```

### Components
| Part | Purpose |
|------|---------|
| Neodymium magnets (4-8mm) | Physical snap connection |
| Pogo pins (4-6 pin) | Data + power transfer |
| Pogo receptacles | Receive the pins |

### Episode Ideas
- "Adding magnets to my tamagotchi"
- "When two devices become one"
- "The moment my tamagotchis meet"

### Tasks
- [ ] Order pogo pin sets (spring-loaded)
- [ ] Design magnet placement (reversible? polarized?)
- [ ] Test I2C over pogo connection
- [ ] Implement neighbor detection
- [ ] Film the first successful link

### Milestone
Two dev boards snap together, creatures meet on screen.

---

## Phase 4: Enclosure V1

### Goal
Something you can hold.

### Options
| Method | Pros | Cons |
|--------|------|------|
| 3D printed | Fast iteration, cheap | Plastic feel |
| Laser cut acrylic | Clean edges, layered look | Limited shapes |
| CNC walnut | Premium feel, matches vision | Expensive, slow |

### Episode Ideas
- "3D printing my first tamagotchi case"
- "From render to real: the enclosure journey"

### Tasks
- [ ] Design enclosure in Fusion 360 / FreeCAD
- [ ] Print prototype case
- [ ] Test button integration
- [ ] Test magnet alignment
- [ ] Film the design process

### Milestone
Functional handheld device (ugly is fine).

---

## Phase 5: PCB Design

### Goal
Replace dev board with custom PCB.

### Episode Ideas
- "Designing my first PCB" (great content, high watch time)
- "From breadboard to circuit board"

### Tasks
- [ ] Schematic in KiCad
- [ ] Layout PCB
- [ ] Order from JLCPCB / PCBWay
- [ ] Solder and test
- [ ] Film the whole process

### Components to Integrate
- MCU (ESP32-S3 or RP2040)
- Display connector
- Battery management (LiPo)
- USB-C charging
- RTC module
- Pogo pin pads
- Magnet mounting points

### Milestone
Device runs on custom board.

---

## Phase 6: Enclosure V2 (Production Quality)

### Goal
Something beautiful.

### The Walnut Vision
Match the render - warm wood, clean lines, premium feel.

### Tasks
- [ ] CNC prototype in walnut
- [ ] Refine tolerances
- [ ] Test magnet retention
- [ ] Assembly documentation
- [ ] Film the woodworking

### Episode Ideas
- "CNC machining a wooden tamagotchi"
- "The satisfying click: perfecting the magnetic link"

### Milestone
Device looks like the renders.

---

## Phase 7: Firmware Polish

### Goal
Creature feels alive.

### Tasks
- [ ] Implement full creature lifecycle
- [ ] All mini-games working
- [ ] Breeding system tested
- [ ] Sound effects (piezo buzzer)
- [ ] Power management (deep sleep)

### Episode Ideas
- "Teaching my tamagotchi to breed"
- "Making the sounds of a digital pet"

---

## Phase 8: Multi-Device Demo

### Goal
Show the full vision.

### The Shot
4+ devices in a grid, creatures roaming freely, landscape spanning all screens.

### Episode Ideas
- "When 4 tamagotchis become a world"
- "The tamagotchi ecosystem: full demo"

---

## Filmable Milestones Summary

| Phase | The Shot | Emotional Beat |
|-------|----------|----------------|
| 0 | Terminal simulation running | "It works in theory" |
| 1 | First sprite on display | "It has eyes" |
| 2 | Button press → creature reacts | "It responds to me" |
| 3 | Two devices snap, creatures meet | "The magic moment" |
| 4 | Holding the device | "It's real" |
| 5 | Custom PCB boots | "Professional" |
| 6 | Walnut case assembled | "It's beautiful" |
| 7 | Full creature lifecycle demo | "It's alive" |
| 8 | Multi-device ecosystem | "The vision realized" |

---

## Bill of Materials (Prototype Phase)

| Item | Qty | Est. Cost | Source |
|------|-----|-----------|--------|
| ESP32-S3 dev board | 2 | $20 | AliExpress |
| 1.3" TFT display | 2 | $16 | AliExpress |
| Tactile buttons | 10 | $3 | Amazon |
| Pogo pins (6-pin) | 4 sets | $12 | AliExpress |
| Neodymium magnets 6mm | 20 | $8 | Amazon |
| LiPo battery 500mAh | 2 | $10 | Adafruit |
| Misc (wires, headers) | - | $10 | - |
| **Total Prototype** | | **~$80** | |

---

## What to Film First

Start with Phase 0 - costs nothing, proves the mechanics, establishes the project.

**Episode 1**: Introduce the concept, show the renders, run the simulation.

Then Phase 1 is cheap and fast - screens arrive in 2 weeks, first "real" pixels in a month.
