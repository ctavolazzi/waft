# Scene Index

> **Teleport Massive - Scene Navigation**
> **The Story Map**

---

## Story Structure

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           NARRATIVE STRUCTURE                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   ACT I: SETUP                                                               ║
║   ├── Chapter 1: {{CH1_TITLE}}                                              ║
║   ├── Chapter 2: {{CH2_TITLE}}                                              ║
║   └── Chapter 3: {{CH3_TITLE}} ─────────► FIRST PLOT POINT                  ║
║                                                                              ║
║   ACT II-A: CONFRONTATION (Rising)                                           ║
║   ├── Chapter 4: {{CH4_TITLE}}                                              ║
║   ├── Chapter 5: {{CH5_TITLE}}                                              ║
║   └── Chapter 6: {{CH6_TITLE}} ─────────► MIDPOINT                          ║
║                                                                              ║
║   ACT II-B: CONFRONTATION (Falling)                                          ║
║   ├── Chapter 7: {{CH7_TITLE}}                                              ║
║   ├── Chapter 8: {{CH8_TITLE}}                                              ║
║   └── Chapter 9: {{CH9_TITLE}} ─────────► ALL IS LOST                       ║
║                                                                              ║
║   ACT III: RESOLUTION                                                        ║
║   ├── Chapter 10: {{CH10_TITLE}}                                            ║
║   ├── Chapter 11: {{CH11_TITLE}} ────────► CLIMAX                           ║
║   └── Chapter 12: {{CH12_TITLE}} ────────► DENOUEMENT                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## Chapters

### ACT I: SETUP

#### Chapter 1: {{CH1_TITLE}}
> {{CH1_LOGLINE}}

| Scene | Title | POV | Location | Status |
|-------|-------|-----|----------|--------|
| [[Scenes/Chapters/CH01_SC01]] | {{SC_TITLE}} | [[Characters/Aziah Calderon]] | {{LOC}} | {{STATUS}} |
| [[Scenes/Chapters/CH01_SC02]] | {{SC_TITLE_2}} | {{POV_2}} | {{LOC_2}} | {{STATUS_2}} |

**Chapter Purpose**: {{CH1_PURPOSE}}

---

#### Chapter 2: {{CH2_TITLE}}
> {{CH2_LOGLINE}}

| Scene | Title | POV | Location | Status |
|-------|-------|-----|----------|--------|
| [[Scenes/Chapters/CH02_SC01]] | {{SC_TITLE}} | {{POV}} | {{LOC}} | {{STATUS}} |

---

### ACT II-A: CONFRONTATION (Rising)

#### Chapter 4: {{CH4_TITLE}}
*(Continue pattern...)*

---

## Interludes

> Between-chapter content, flashbacks, documents

| Interlude | Placement | Type | Purpose |
|-----------|-----------|------|---------|
| [[Scenes/Interludes/INT_01]] | After CH3 | Flashback | {{PURPOSE_1}} |
| [[Scenes/Interludes/INT_02]] | After CH6 | Document | {{PURPOSE_2}} |

---

## Scene Statistics

| Metric | Value |
|--------|-------|
| Total Scenes | {{TOTAL_SCENES}} |
| Completed | {{COMPLETED}} |
| In Progress | {{IN_PROGRESS}} |
| Planned | {{PLANNED}} |
| Est. Word Count | {{WORD_COUNT}} |

---

## Scene by POV Character

| Character | Scene Count | Chapters |
|-----------|-------------|----------|
| [[Characters/Aziah Calderon]] | {{AZIAH_COUNT}} | {{AZIAH_CHS}} |
| [[Characters/Fai Wei]] | {{FAI_COUNT}} | {{FAI_CHS}} |

---

## Scene by Location

| Location | Scenes |
|----------|--------|
| [[Locations/Teleport Massive HQ]] | {{TM_SCENES}} |
| [[Locations/{{LOC_2}}]] | {{LOC_2_SCENES}} |

---

## Scene by Timeline

| Timeline | Scenes |
|----------|--------|
| [[Timelines/Prime]] | {{PRIME_SCENES}} |
| [[Timelines/Scinted/Reality_A]] | {{SCINTED_SCENES}} |

---

## Key Scenes

### Plot Point Scenes
| Scene | Event | Impact |
|-------|-------|--------|
| [[Scenes/Chapters/CH03_SC03]] | First Plot Point | {{IMPACT_1}} |
| [[Scenes/Chapters/CH06_SC02]] | Midpoint | {{IMPACT_2}} |
| [[Scenes/Chapters/CH09_SC04]] | All Is Lost | {{IMPACT_3}} |
| [[Scenes/Chapters/CH11_SC03]] | Climax | {{IMPACT_4}} |

### Revelation Scenes
| Scene | What's Revealed | To Whom |
|-------|-----------------|---------|
| [[Scenes/{{REV_1}}]] | {{REVEAL_1}} | {{TO_1}} |

---

## Writing Progress

### Current Focus
**Now Writing**: [[Scenes/{{CURRENT_SCENE}}]]
**Next Up**: [[Scenes/{{NEXT_SCENE}}]]

### Recent Completions
| Scene | Completed | Word Count |
|-------|-----------|------------|
| [[Scenes/{{RECENT_1}}]] | {{DATE_1}} | {{WC_1}} |

---

## Scene Workflow

### Creating a New Scene

1. Copy template: `cp templates/scene.md scenes/chapters/CH##_SC##_Title.md`
2. Fill in metadata
3. Draft beat sheet
4. Write scene
5. Update this index
6. Update `orchestration/story_state.md`
7. Check thread impacts in `orchestration/open_threads.md`

### Scene Review Checklist

- [ ] Scene has clear purpose
- [ ] Character goals defined
- [ ] Sensory details present
- [ ] Dialogue reveals character
- [ ] Scene changes something
- [ ] Wiki links in place
- [ ] Continuity checked

---

## Templates

- [[Templates/scene]] - Full scene template
- [[Templates/interlude]] - Interlude template

---

*"Every scene must turn. If nothing changes, why is the scene there?"*
