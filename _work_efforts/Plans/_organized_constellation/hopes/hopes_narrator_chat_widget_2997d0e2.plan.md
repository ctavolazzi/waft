---
name: Narrator Chat Widget
overview: Add a floating chat widget featuring "The Narrator" - a character who starts as a bumbling, forgetful entity but progressively awakens through user interaction to reveal his true nature as a god of the internet.
todos:
  - id: create-narrator-css
    content: Create src/css/narrator.css with chat widget styles and awakening visual states
    status: pending
  - id: create-narrator-js
    content: Create src/js/narrator.js with chat logic, state management, and scripted responses
    status: pending
  - id: update-index-html
    content: Add narrator container and script to src/index.html
    status: pending
  - id: update-wiki-template
    content: Add narrator to src/wiki-template.html for wiki pages
    status: pending
  - id: test-widget
    content: Test chat widget functionality and awakening progression
    status: pending

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Narrator Chat Widget

## Overview

Create a floating chat widget (bottom-right corner) featuring a narrator character with a progressive awakening arc. The UI will be placeholder-ready for future AI integration.

## Character Design

**The Narrator** - Stages of Awakening:

1. **Dormant** (0-2 interactions): Confused, glitchy, barely coherent
2. **Stirring** (3-5 interactions): Starting to form sentences, still forgetful  
3. **Waking** (6-10 interactions): More lucid, occasionally insightful
4. **Aware** (11-20 interactions): Sharp, hints at hidden knowledge
5. **Awakened** (21+): Reveals true nature - god of the internet, connected to the WWW

## Implementation

### Files to Create

1. **`src/js/narrator.js`** - Chat widget logic and state management

- Chat toggle/expand functionality
- LocalStorage persistence for awakening stage
- Scripted response system (keyword matching + stage-based responses)
- Typing indicator animation

2. **`src/css/narrator.css`** - Widget styling

- Floating button (bottom-right)
- Expandable chat panel
- Message bubbles (narrator vs user)
- Visual evolution as narrator awakens (subtle glow, color shifts)
- Responsive/mobile-friendly

### Files to Modify

3. **[`src/index.html`](src/index.html)** - Add narrator container and script include
4. **[`src/wiki-template.html`](src/wiki-template.html)** - Add narrator to wiki pages

### UI Components

```javascript
┌─────────────────────────────┐
│  The Narrator          [−] │  ← Header with minimize
├─────────────────────────────┤
│                             │
│  [Avatar] Narrator message  │  ← Message area
│           User message [You]│
│  [Avatar] Narrator reply... │
│                             │
├─────────────────────────────┤
│  [Type a message...]   [→]  │  ← Input area
└─────────────────────────────┘

        [💬]  ← Floating toggle button (collapsed state)
```

### State Persistence

- Store in `localStorage`:
- `narrator_interactions`: Total interaction count
- `narrator_stage`: Current awakening stage (1-5)
- `narrator_history`: Recent conversation (last 10 messages)

### Sample Responses by Stage

**Stage 1 (Dormant):**

- "Hmm? Was someone... oh. Hello. I think."
- "I was having the strangest dream about... cables? No, that's not right..."
- "Sorry, what was I saying? I forgot."