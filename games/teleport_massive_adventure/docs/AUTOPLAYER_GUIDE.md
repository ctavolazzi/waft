# AutoPlayer Complete Guide
## Full Game Automation from Start to Finish

**Date:** 2026-01-25  
**Status:** ✅ Fully Functional

---

## Overview

The AutoPlayer is a comprehensive automation system that plays through the entire game from start to finish, demonstrating the complete gameplay loop and serving as both a testing tool and a gameplay showcase.

**Features:**
- ✅ Complete walkthrough script (Lab → Lobby → Underground → Void)
- ✅ Automatic dialogue advancement
- ✅ Scene transition handling
- ✅ Boss fight automation
- ✅ Ending selection
- ✅ Error recovery and retry logic
- ✅ Real-time progress logging

---

## How to Use

### Starting AutoPlayer

1. **Load the game** in your browser
2. **Click the "▶ AUTO" button** in the top-left corner
3. **Watch the automation** - the game will play itself!

### Controls

- **▶ AUTO** - Start automated playthrough
- **⏸ PAUSE** - Pause automation (can resume)
- **▶ RESUME** - Resume from pause
- **Status Display** - Shows current step and progress

---

## Complete Walkthrough Script

### Scene 1: Lab (Tutorial)

1. **Examine Photo** - Looks at photo of Maya
2. **Pick Up Artifact** - Collects the SWAB artifact
3. **Use Terminal** - Accesses research terminal
4. **Go to Lobby** - Exits through door

**Duration:** ~15 seconds

### Scene 2: Lobby

1. **Examine Display** - Looks at TM holographic display
2. **Talk to Guard** - Speaks with security guard
3. **Pick Up Keycard** - Collects security keycard
4. **Use Maintenance Hatch** - Opens hatch with keycard

**Duration:** ~20 seconds

### Scene 3: Underground

1. **Talk to Phaseburner** - Converses with the glitched NPC
2. **Use Damaged Terminal** - Accesses encrypted files
3. **Enter Portal** - Steps through dimensional portal

**Duration:** ~25 seconds

### Scene 4: Void (Boss Fight)

**Phase 1:**
- Question Dealer (30 damage)
- Call Bluff (20 damage)
- Play for Maya (15 damage)
- Question Dealer (30 damage)
- Call Bluff (20 damage)
- **Total:** 115 damage → Phase complete

**Phase 2:**
- Question Dealer (30 damage)
- Call Bluff (20 damage)
- Play for Maya (15 damage)
- Question Dealer (30 damage)
- **Total:** 95 damage → Phase complete

**Phase 3:**
- Question Dealer (30 damage)
- Call Bluff (20 damage)
- Play for Maya (15 damage)
- Question Dealer (30 damage)
- **Total:** 95 damage → Victory!

**Final Choice:**
- Selects "CASH OUT" ending (Liberation)

**Duration:** ~2-3 minutes

---

## Technical Details

### Scene Detection

AutoPlayer uses multiple methods to detect the current scene:

```javascript
// Method 1: Phaser scene manager
window.game.scene.getScenes(true).find(s => s.scene.isActive)

// Method 2: Direct scene access
window.game.scene.scenes[scenes.length - 1]
```

**Retry Logic:**
- Waits up to 10 seconds for scene transitions
- Automatically retries if scene doesn't match
- Logs warnings if timeout reached

### Dialogue Auto-Advance

- **Speed:** 100ms per line
- **Automatic:** Advances dialogue without user input
- **Completion Detection:** Stops when dialogue ends
- **Event-Driven:** Responds to `DIALOGUE_START` events

### Boss Fight Automation

**Action Keys:**
- `bluff` - Call Bluff (20 damage)
- `allin` - Go All In (35 damage) - not used in script
- `maya` - Play for Maya (15 damage)
- `question` - Question Dealer (30 damage)

**Turn Detection:**
- Waits for `isPlayerTurn === true`
- Retries up to 5 times if not player turn
- Clicks buttons directly if available

**Phase Transitions:**
- Automatically waits for phase transitions
- Handles healing between phases
- Continues to next phase automatically

### Ending Selection

**Choice Keys:**
- `free` - CASH OUT (Liberation ending)
- `merge` - BECOME DEALER (Join ending)
- `destroy` - FLIP TABLE (Destroy ending)

**UI Detection:**
- Waits for `finalChoiceShown === true`
- Retries up to 10 times
- Clicks ending button directly

---

## Error Handling

### Scene Transition Timeouts

**Problem:** Scene doesn't transition in time

**Solution:**
- Retries up to 20 times (10 seconds)
- Logs warning and continues if timeout
- Resets retry counter on success

### Boss Action Failures

**Problem:** Player turn not available

**Solution:**
- Waits for `isPlayerTurn === true`
- Retries up to 5 times
- Falls back to direct button click
- Logs available actions for debugging

### Ending Choice Delays

**Problem:** Final choice UI not ready

**Solution:**
- Waits for `finalChoiceShown === true`
- Retries up to 10 times (20 seconds)
- Attempts to force-show UI if needed

---

## Script Customization

### Adjusting Timing

```javascript
// In AutoPlayer constructor
this.walkDelay = 800;      // Time after walking
this.actionDelay = 500;    // Time between actions
this.dialogueSpeed = 100;  // Dialogue auto-advance speed
```

### Adding Steps

```javascript
// In buildScript()
{ 
    scene: 'LabScene', 
    action: 'walkTo', 
    x: 300, 
    y: 400 
},
{ 
    scene: 'LabScene', 
    action: 'interact', 
    targetId: 'terminal', 
    mode: 'use' 
},
```

### Custom Actions

Add new action types in `executeAction()`:

```javascript
case 'customAction':
    this.performCustomAction(scene, step.data);
    this.scheduleNext(1000);
    break;
```

---

## Debugging

### Enable Verbose Logging

AutoPlayer logs all actions to:
- **Console** - Colored output (`color: #00ff88`)
- **UI Log Area** - Scrollable log panel

### Check Current State

```javascript
// In browser console
autoPlayer.debug(); // Shows current step, state, etc.
autoPlayer.getCurrentScene(); // Returns current scene
```

### Common Issues

**Issue:** AutoPlayer stops at scene transition
- **Cause:** Scene name mismatch
- **Fix:** Check scene key in `getCurrentScene()`
- **Debug:** Log `currentScene.scene.key`

**Issue:** Boss actions not working
- **Cause:** Not player turn or buttons not visible
- **Fix:** Increase wait times before boss actions
- **Debug:** Check `scene.isPlayerTurn` and `scene.actionButtons`

**Issue:** Ending choice fails
- **Cause:** Final choice UI not shown
- **Fix:** Increase wait time before ending choice
- **Debug:** Check `scene.finalChoiceShown`

---

## Performance

**Total Playthrough Time:** ~3-4 minutes

**Breakdown:**
- Lab Scene: ~15 seconds
- Lobby Scene: ~20 seconds
- Underground Scene: ~25 seconds
- Void Scene (Boss): ~2-3 minutes
- **Total:** ~3-4 minutes

**Optimization Tips:**
- Reduce `dialogueSpeed` for faster dialogue
- Reduce `walkDelay` for faster movement
- Reduce wait times between actions
- Use `allin` action for faster boss kills

---

## Testing Checklist

- [x] AutoPlayer starts correctly
- [x] Scene transitions work
- [x] Dialogue auto-advances
- [x] Interactions find targets
- [x] Boss actions execute
- [x] Phase transitions work
- [x] Ending choice selects
- [x] Game completes successfully
- [x] Error recovery works
- [x] Retry logic functions

---

## Future Enhancements

### Planned Features
- [ ] Configurable speed (slow/normal/fast)
- [ ] Multiple walkthrough scripts
- [ ] Save/load script state
- [ ] Visual step indicators
- [ ] Skip dialogue option
- [ ] Boss fight strategy selection

### Possible Improvements
- [ ] Adaptive timing based on game performance
- [ ] Automatic screenshot capture
- [ ] Performance metrics collection
- [ ] Replay system
- [ ] Script editor UI

---

## Troubleshooting

### AutoPlayer Won't Start

**Check:**
1. Game is fully loaded
2. No JavaScript errors in console
3. AutoPlayer UI is visible
4. Button is clickable

**Fix:**
- Reload page
- Check console for errors
- Verify `autoPlayer` is defined

### Stuck at Scene Transition

**Check:**
1. Scene name matches expected
2. Room transition completed
3. Player position is correct

**Fix:**
- Increase wait time before transition
- Check `InteractionSystem.executeChangeRoom()`
- Verify scene mapping in `InteractionSystem`

### Boss Actions Not Working

**Check:**
1. `scene.isPlayerTurn === true`
2. `scene.actionButtons` exists
3. Action key matches available actions

**Fix:**
- Increase wait times
- Check `TheDealer.getPlayerActions()`
- Verify action keys: `bluff`, `maya`, `question`, `allin`

### Ending Choice Fails

**Check:**
1. `scene.finalChoiceShown === true`
2. `scene.endingButtons` exists
3. Choice key matches: `free`, `merge`, `destroy`

**Fix:**
- Increase wait time before ending choice
- Check `VoidScene._showFinalChoice()`
- Verify victory condition is met

---

## Code Reference

### Key Files

- `src/core/AutoPlayer.js` - Main automation logic
- `src/scenes/VoidScene.js` - Boss fight implementation
- `src/core/TheDealer.js` - Boss actions and dialogue
- `src/core/InteractionSystem.js` - Scene transitions

### Key Methods

```javascript
// Start automation
autoPlayer.start()

// Pause/Resume
autoPlayer.pause()
autoPlayer.resume()

// Stop
autoPlayer.stop()

// Get current scene
autoPlayer.getCurrentScene()

// Debug
autoPlayer.debug()
```

---

## Success Criteria

✅ **AutoPlayer is successful when:**
1. Completes entire game without manual intervention
2. Reaches all 4 scenes (Lab, Lobby, Underground, Void)
3. Defeats boss in all 3 phases
4. Selects an ending
5. Shows completion message

**Current Status:** ✅ **FULLY FUNCTIONAL**

---

**Last Updated:** 2026-01-25  
**Version:** 2.0 (Complete rewrite with robust error handling)
