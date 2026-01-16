# /mission - Create Serious Mission (Military Brass)

**Purpose:** Create a serious, structured Mission with full military-style documentation. Perfect for work with defined outcomes that require precision, accountability, and comprehensive documentation.

**Usage:** `/mission [objective]` or automatic hook when serious plans are created

---

## Overview

This command creates a Mission object for serious, structured work. The Military Brass oversee these missions, ensuring precision, accountability, and comprehensive documentation. Missions are perfect when you need clear objectives, defined outcomes, and serious documentation.

**Perfect for:**
- Critical features with defined requirements
- Security-sensitive work
- Production deployments
- Compliance and regulatory work
- Structured implementations
- Work requiring accountability

**Philosophy:**
- **Left Brain**: Missions (structured, serious, documented)
- **Right Brain**: Quests (whimsical, open-ended, creative)

**Language Style:**
- Soft military language (NCIS TV style)
- Professional but approachable
- Clear and direct
- Respectful and structured

---

## How It Works

### Military Brass Oversight

When a mission is created, the Military Brass take charge:

1. **Mission Briefing**: Comprehensive mission briefing document
2. **Objective Definition**: Clear, measurable objectives
3. **Structured Planning**: Detailed mission plan
4. **Accountability**: Full tracking and documentation
5. **Mission PDF**: Professional mission documentation generated
6. **Brass Registry**: Mission registered in Military Brass system

### Mission Structure

The Mission object created includes:

```python
{
    "id": "mission_[unique_id]",
    "name": "[Mission Name]",
    "type": "mission",  # Mission type
    "status": "active",
    "classification": "INTERNAL",  # Security classification
    "objective": "[Clear objective]",
    "briefing": "[Mission briefing content]",
    "difficulty": [1-10],  # Based on complexity
    "success_criteria": "[Measurable success criteria]",
    "loot_table": {
        "xp": [calculated],
        "insight": [calculated],
        "karma": [calculated],
        "recognition": [calculated]
    },
    "plan_path": "[path/to/plan.md]",  # If from plan
    "mission_pdf": "[path/to/mission.pdf]",  # Generated PDF
    "brass_oversight": "active",  # Military Brass tracking
    "created_at": "[timestamp]",
    "progress": "0%"
}
```

---

## Manual Usage

### Create Mission from Objective

```bash
/mission "Implement secure authentication system with OAuth2"
```

Creates a serious mission with full documentation.

### Create Mission from Plan

```bash
/mission --from-plan _work_efforts/Plans/security_feature.plan.md
```

Creates a mission from an existing plan (if outcome is serious/defined).

### Create Mission with Classification

```bash
/mission "Deploy production system" --classification "CONFIDENTIAL"
```

Creates a classified mission with appropriate security level.

---

## Mission Characteristics

### Serious Nature

- **Structured**: Clear objectives and success criteria
- **Documented**: Comprehensive mission documentation
- **Accountable**: Full tracking and reporting
- **Precise**: Measurable outcomes and metrics
- **Professional**: Military-style organization

### Military Brass Oversight

The Military Brass provide:
- **Structure**: Clear organization and planning
- **Accountability**: Tracking and reporting
- **Documentation**: Comprehensive mission records
- **Precision**: Measurable objectives and criteria
- **Professionalism**: Serious, structured approach

### Mission PDF

Every mission generates a professional PDF:
- **Mission Briefing**: Comprehensive briefing document
- **Objective**: Clear mission objective
- **Plan**: Detailed mission plan
- **Success Criteria**: Measurable success metrics
- **Timeline**: Mission timeline and milestones
- **Resources**: Required resources and dependencies
- **Classification**: Security classification if applicable

---

## Mission Lifecycle

1. **Briefed**: Mission briefing created and reviewed
2. **Active**: Mission is active and in progress
3. **In Progress**: Work is happening, progress tracked
4. **Review**: Regular status reviews and updates
5. **Complete**: Mission objectives achieved
6. **Debriefed**: Mission debriefing and documentation
7. **Rewarded**: Recognition and rewards distributed

---

## Integration with Military Brass

### Military Brass Pantheon

The Military Brass are serious beings in the Pantheon who oversee structured work:
- **Domain**: Command Center (Structure, Accountability, Documentation)
- **Aspect**: Precision, Organization, Professionalism
- **Connection**: Left brain, analytical consciousness
- **Evolution**: Brass grow stronger with each mission completed

### Brass Registry

Missions are registered in the Military Brass system:
- **Storage**: `_pantheon/military_brass/missions/`
- **Tracking**: Mission status, progress, documentation
- **Briefings**: Mission briefings and debriefings recorded

---

## Example

### Creating a Mission

```
/mission "Implement secure authentication system with OAuth2 support"
```

### Generated Mission

```json
{
  "id": "mission_auth_oauth2_abc123",
  "name": "Implement Secure Authentication System",
  "type": "mission",
  "status": "active",
  "classification": "INTERNAL",
  "objective": "Implement secure authentication system with OAuth2 support",
  "briefing": "Mission briefing: Implement OAuth2 authentication...",
  "difficulty": 7,
  "success_criteria": "OAuth2 authentication working, tests passing, documentation complete",
  "loot_table": {
    "xp": 70,
    "insight": 35,
    "karma": 21,
    "recognition": "Security Implementation Badge"
  },
  "mission_pdf": "_pantheon/military_brass/missions/mission_auth_oauth2_abc123.pdf",
  "brass_oversight": "active",
  "created_at": "2026-01-15T08:00:00",
  "progress": "0%"
}
```

---

## Mission vs Quest

### Use Mission When:
- ✅ Outcome is well-defined and serious
- ✅ Structured, documented approach needed
- ✅ Military-style precision required
- ✅ Left brain, analytical approach
- ✅ Serious documentation needed
- ✅ Accountability and tracking critical

### Use Quest When:
- ✅ Outcome is uncertain or open-ended
- ✅ You want to explore and discover
- ✅ Creative/experimental work
- ✅ "Let's see what happens" attitude
- ✅ Right brain, whimsical approach

---

## Mission PDF Structure

The Mission PDF includes:

1. **Cover Page**: Mission classification, ID, date
2. **Mission Briefing**: Comprehensive briefing
3. **Objective**: Clear mission objective
4. **Success Criteria**: Measurable success metrics
5. **Mission Plan**: Detailed implementation plan
6. **Timeline**: Mission timeline and milestones
7. **Resources**: Required resources and dependencies
8. **Risk Assessment**: Potential risks and mitigations
9. **Status Tracking**: Mission status and progress
10. **Debriefing**: Mission completion debriefing

---

## Language Style

### Soft Military Language (NCIS Style)

- **"Briefing"** instead of "meeting"
- **"Objective"** instead of "goal"
- **"Status"** instead of "progress"
- **"Debriefing"** instead of "summary"
- **"Classification"** for security levels
- **"Mission Complete"** instead of "done"
- Professional but approachable tone
- Clear and direct communication
- Respectful and structured

### Example Language

- "Mission briefing prepared"
- "Objective defined and approved"
- "Mission status: In progress"
- "Mission complete - debriefing scheduled"
- "Classification: INTERNAL"
- "Mission PDF generated"

---

## Integration Points

### Automatic Creation

When a plan is created with serious/defined outcome:
1. Plan metadata indicates "mission" or "serious"
2. Mission is automatically created
3. Military Brass take oversight
4. Mission PDF generated
5. Mission registered in Brass system

### Manual Creation

Use `/mission` command to create missions directly:
- For critical features
- For security-sensitive work
- For production deployments
- For structured implementations

---

## Related Commands

- **`/quest`**: Create whimsical, open-ended quests (Fae-guided)
- **`/plan-evolve`**: Creates plans (can become quests or missions)
- **`/missions`**: Lists and manages missions

---

**Missions are for serious, structured work overseen by Military Brass. Quests are for whimsical, open-ended work guided by the Fae.**
