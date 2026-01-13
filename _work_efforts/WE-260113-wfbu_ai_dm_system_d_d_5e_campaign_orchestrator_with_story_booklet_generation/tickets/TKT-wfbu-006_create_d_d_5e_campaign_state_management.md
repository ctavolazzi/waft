---
id: TKT-wfbu-006
parent: WE-260113-wfbu
title: "Create D&D 5e campaign state management"
status: completed
created: 2026-01-13T08:41:56.072Z
created_by: ctavolazzi
assigned_to: null
---

# TKT-wfbu-006: Create D&D 5e campaign state management

## Metadata
- **Created**: Tuesday, January 13, 2026 at 12:41:56 AM PST
- **Completed**: Tuesday, January 13, 2026 at 1:20:00 AM PST
- **Parent Work Effort**: WE-260113-wfbu
- **Author**: ctavolazzi

## Description

Create a comprehensive campaign state management system for D&D 5e campaigns. The system should:
- Track campaign state (status, sessions, events)
- Manage player characters and NPCs
- Track scenario engine containers
- Record decisions made (decision matrices)
- Link to scientific method experiments
- Provide persistence and retrieval
- Generate campaign summaries

## Acceptance Criteria
- [x] CampaignState dataclass created
- [x] CampaignSession dataclass created
- [x] CampaignEvent dataclass created
- [x] CampaignStateManager class implemented
- [x] Campaign creation and persistence
- [x] Session management
- [x] Event tracking
- [x] Campaign loading and retrieval
- [x] Campaign summary generation
- [x] Test suite created and passing

## Files Changed
- `src/campaign_state.py` - Campaign state management (400+ lines)
- `examples/test_campaign_state.py` - Test suite

## Implementation Notes

### Core Components

**CampaignState**:
- Campaign metadata (id, name, status, description)
- Character management (PCs and NPCs as Being IDs)
- Session tracking
- Scenario engine integration (containers, sequence IDs)
- Decision tracking (decision matrix results)
- Scientific method integration (experiment IDs)
- Custom campaign data storage

**CampaignSession**:
- Session metadata (id, number, status, times)
- Event list
- Current sequence ID (scenario engine)
- Containers state (scenario engine)
- Notes and summary

**CampaignEvent**:
- Event metadata (id, timestamp, type, description)
- Participants (Being IDs)
- Scenario engine links (sequence_id, choice_made)
- Decision matrix links (decision_matrix_id)
- Custom data

**CampaignStateManager**:
- Campaign CRUD operations
- Session management
- Event tracking
- State persistence (JSON)
- Campaign listing and summaries

### State Persistence

**Storage Location**: `_pyrite/.waft/campaigns/`

**File Format**: JSON
- One file per campaign: `{campaign_id}.json`
- Human-readable with indentation
- Includes all state (sessions, events, characters)

### Integration Points

1. **Being System**: Characters stored as Being IDs
2. **Scenario Engine**: Sequence IDs and containers tracked
3. **Decision Matrix**: Decision results stored
4. **Scientific Method**: Experiment IDs linked
5. **Booklet Generator**: State can be used to generate booklets

### Test Results

✅ **All Tests Passing**:
- ✅ Campaign creation
- ✅ Player character management
- ✅ Session creation
- ✅ Event tracking (2 events added)
- ✅ Session status updates
- ✅ Campaign loading
- ✅ Campaign summary generation
- ✅ Campaign listing

### Usage Example

```python
from campaign_state import CampaignStateManager, SessionStatus

manager = CampaignStateManager(project_path)

# Create campaign
campaign = manager.create_campaign(
    campaign_name="The Mysterious Tavern",
    scenario_file="tavern_campaign.json"
)

# Add session
session = manager.add_session(campaign.campaign_id)

# Add event
event = manager.add_event(
    campaign_id=campaign.campaign_id,
    session_id=session.session_id,
    event_type="narrative",
    description="Party wakes up in tavern",
    sequence_id="seq_001"
)

# Update session
manager.update_session_status(
    campaign_id=campaign.campaign_id,
    session_id=session.session_id,
    status=SessionStatus.COMPLETED
)

# Get summary
summary = manager.get_campaign_summary(campaign.campaign_id)
```

### Next Steps

- [ ] Integrate with scenario engine (containers, sequences)
- [ ] Integrate with decision matrix system
- [ ] Integrate with scientific method tool
- [ ] Add campaign state to booklet generator
- [ ] Create campaign orchestrator using this state

## Commits
- (work in progress, not yet committed)
