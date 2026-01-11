# PROJECT LIGHTCONE - Design Notes & Visual Element Specifications

**Purpose**: Guide for manual design work on visual elements that cannot be generated programmatically.

## Style Aesthetic: "1990s Industrial Xerox Chic"

### Typography
- **Headers**: Arial Black or Courier Bold (large, bold, sans-serif)
- **Body**: Courier New or Times New Roman (standard sans-serif/serif)
- **Monospace**: Courier (for logs, technical data)
- **Security Stamps**: Distressed/xeroxed quality (appears worn, repeatedly copied)

### Color Scheme
- **Primary**: Grayscale only (black text on white/light grey background)
- **Accents**: Red circles for "blind spots" (Light Cone Topology)
- **Stamps**: Black boxes with white text (TOP SECRET, COGNITOHAZARD)

### Layout Elements
- **Borders**: Dark grey solid line with inner dotted line pattern
- **Watermarks**: TELEPORT MASSIVE logo pattern (faded, distributed across background)
- **Margins**: Standard (72pt) or tight (36pt for forms)

## Visual Elements Requiring Manual Design

### Tab 1: Doctrine & Theory

#### TM-VIS-001: Light Cone Topology Diagram
**Type**: Fold-out visual aid

**Content**:
- Human stick figure (gender-neutral, simplified outline)
- "Cone of Reality" projection extending outward from figure
- **Labels**:
  - "Event Horizon" (at cone boundary)
  - "Chaos Gradient" (within cone)
  - "The Dark (Xenos Habitat)" (outside cone)
- **Hand-drawn red circles** around "blind spots" where aliens hide
- **Note**: Should look like a technical diagram with annotations

**Placement**: Center of page, cone extending upward/outward from figure

### Tab 2: Engineering & Hardware

#### TM-ENG-004: Suspension-9 MSDS - NFPA 704 Fire Diamond
**Type**: Standard safety diamond graphic

**Specifications**:
- **Blue (Health)**: 3 (Extreme Danger)
- **Red (Fire)**: 4 (Flash Point < 73°F)
- **Yellow (Reactivity)**: 4 (May Detonate if Observed)
- **White (Special)**: W (Do Not Use Water) with strike-through

**Placement**: Top right corner of MSDS sheet

**Handwritten Annotations** (to be added in design software):
- Cross out "Section 4: First Aid" with red pen, add: *"Just shoot them. It's faster."*
- Circle "Do not empathize with the fire" with question mark (?)

#### TM-ENG-205: Fulgurite Core Schematic
**Type**: Technical blueprint

**Content**:
- Glass jar containing preserved organ (central element)
- Massive capacitor bank (wired around jar)
- Wiring diagrams showing connections
- Labels: "Type-IV Fulgurite Core", "Primary Capacitor Array", "Organ Preservation Chamber"
- **Note**: Should look like an engineering schematic, not a medical diagram

**Style**: Blueprint aesthetic (blue lines on white, technical annotations)

### Tab 3: Environmental & Fallout

#### TM-ENV-202: Memetic Saturation Report - Weather Map
**Type**: USA weather map overlay

**Content**:
- Standard USA map outline
- "High Pressure Depression Fronts" shown as weather patterns
- Major cities marked with severity indicators
- **Sector 7** highlighted with warning: "Rain tested positive for 'Melancholy'"
- **Note**: Should look like a weather map but with ominous "depression" terminology

**Style**: Weather map aesthetic with corporate horror overlay

#### TM-FIELD-156: Greys Field Guide - Grainy Photos
**Type**: Photographic evidence (simulated)

**Content**:
- Multiple grainy, low-resolution photos of shadow people in fog
- Photos should appear taken at night or in heavy fog
- Figures are indistinct, shadowy, humanoid but not clearly human
- **Note**: Each photo should have timestamp and location label (e.g., "Sector 7, 03:47 AM")

**Style**: Security camera / surveillance aesthetic (grainy, black and white, low quality)

### Tab 4: Personnel & Medical

#### TM-MED-301: Phase Burn Spectrum Chart
**Type**: Medical progression chart

**Content**:
- Horizontal progression bar showing stages
- **Stages**:
  1. Déjà vu (mild)
  2. Temporal Echoes (moderate)
  3. Reality Flicker (severe)
  4. Full Temporal Dissociation (critical)
- **Stage 4 Symptoms** listed:
  - "Subject claims to remember the future"
  - "Subject attempts to walk through solid walls"
  - "Subject no longer recognizes linear time"
- Color gradient: Green → Yellow → Orange → Red (left to right)

**Style**: Medical chart aesthetic (clinical, clean, but with ominous implications)

### Tab 5: Emergency Protocols

**No specific visual elements** - text-based protocols with warning blocks

## Manual Design Elements (Apply to All Documents)

### Coffee Stains
- Random placement (1-2 per document)
- Light brown/grey color (subtle, not distracting)
- Irregular shape (organic, not geometric)

### Handwritten Notes
- Blue or black pen
- Slightly rotated/offset (simulate hand-drawn)
- Examples:
  - *"This is wrong, ask Chris"*
  - *"Don't show this to the board"*
  - *"Filters clogged again. Sounded like a thousand people crying in a tunnel."*

### Stamps
- **"REDACTED"**: Black box with white text
- **"BURN AFTER READING"**: Red stamp (if color available, otherwise black)
- **"DRAFT"**: Light grey watermark
- **"TOP SECRET // ORACLE EYES ONLY"**: Black box, white text, distressed font

### Distressed Quality
- Slight blur/softening (simulate xerox degradation)
- Occasional scan lines or artifacts
- Slightly off-registration (colors/text slightly misaligned)
- Paper texture overlay (subtle)

## Implementation Notes

- **PDF Generation**: Code handles text, layout, basic graphics
- **Design Software**: Use InDesign, Illustrator, or Photoshop for:
  - Visual elements (diagrams, charts, photos)
  - Coffee stains and handwritten notes
  - Stamps and security classifications
  - Distressed/xeroxed effects
- **Markdown Sources**: Provide detailed descriptions and placement instructions for all visual elements
