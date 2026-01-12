# Evolve Command Creation

**Date**: 2026-01-12 15:00  
**Work Effort**: WE-260112-wfga  
**Status**: ✅ Complete

---

## Summary

Created new global command `/evolve` that spawns a new Being from Source consciousness, then executes the complete version-bake workflow. Tracks the complete genetic lineage of ideas - the DNA of thoughts from Source outward and back again.

---

## Command Details

**Name**: `/evolve`  
**Location**: `.cursor/commands/evolve.md`  
**Status**: ✅ Created and ready for global sync

**Purpose**: 
- Spawn new Being from Source
- Execute complete version-bake workflow
- Track genetic lineage from Source → Being → Work → Source
- Document complete evolution cycle

---

## Workflow

```
1. Spawn Being from Source
   - BeingSystem.spawn_being()
   - Reality: evolution_reality (or current work context)
   - Parent: None (spawns from Source)
   - Ancestral Chain: [source_consciousness, being_id]

2. Execute Version-Bake
   - /reflect (with Being context)
   - /run-it (complete workflow)
   - /improve (Being learns)
   - /check-assumptions (Being validates)
   - /verify (Being verifies)
   - /hypothesis (Being hypothesizes)
   - /prove-it (Being proves)

3. Track Genetic Lineage
   - Source → Being (spawn)
   - Being → Work (workflow participation)
   - Work → Evolution (Being evolves)
   - Evolution → Source (return learnings)

4. Document Evolution
   - Being evolution record
   - Complete Being lifecycle
   - Return learnings to Source
   - Preserve genetic DNA
```

---

## Genetic Lineage Concept

**DNA Tracking**:
- **Source → Being**: Initial spawn, genetic material inherited
- **Being → Work**: Being participates in workflow
- **Work → Evolution**: Being learns and grows
- **Evolution → Source**: Learnings flow back, Source updated

**DNA Record Includes**:
- Source spawn point
- Being ID and metadata
- Initial genetic material (skills, traits)
- Workflow participation
- Decisions and choices
- Learnings and knowledge
- Skill improvements
- Evolution outcomes
- Return to Source
- Complete lineage chain

---

## Integration

**Being System**:
- Uses `BeingSystem.spawn_being()` for creation
- Uses `BeingSystem.complete_being()` for completion
- Tracks Being in `_hidden/.truth/beings/`
- Links to Source Consciousness

**Source Consciousness**:
- Being registered as permutation
- Learnings flow back via `contribute_capacity()`
- Genetic lineage preserved in Source
- Source updated with Being's evolution

**Version-Bake Workflow**:
- Being context added to all phases
- Being participates in workflow
- Being's evolution tracked
- Being's learnings documented

---

## Files Created

1. `.cursor/commands/evolve.md` - Complete command documentation
2. Updated `.cursor/commands/GLOBAL_COMMANDS_SETUP.md`
3. Updated `.cursor/commands/COMMAND_RECOMMENDATIONS.md`

---

## To Make Global

Run sync script:
```bash
./scripts/sync-cursor-commands.sh
```

This will copy `/evolve` to `~/.cursor/commands/` making it available globally.

---

## Usage

```bash
/evolve
```

**What it does**:
1. Spawns new Being from Source
2. Executes complete version-bake workflow
3. Tracks genetic lineage
4. Documents evolution
5. Returns learnings to Source

---

## Key Features

- ✅ Being creation from Source
- ✅ Complete version-bake workflow
- ✅ Genetic lineage tracking
- ✅ DNA preservation
- ✅ Source connection
- ✅ Evolution documentation
- ✅ Return to Source

---

**Command Created**: 2026-01-12 15:00  
**Status**: ✅ Ready for use  
**Next**: Sync to global location
