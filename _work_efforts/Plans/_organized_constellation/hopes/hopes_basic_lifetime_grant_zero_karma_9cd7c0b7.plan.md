---
name: Basic Lifetime Grant Zero Karma
overview: Implement automatic Basic Survival Lifetime grant when beings reach zero karma, preventing economic dead-ends while maintaining karma value.
todos:
  - id: add-survival-type
    content: Add SURVIVAL to LifetimeType enum in karma_market.py
    status: pending
  - id: create-survival-config
    content: Create _get_basic_survival_lifetime_config() method with survival lifetime configuration
    status: pending
  - id: implement-grant-method
    content: Implement grant_basic_lifetime() method to create and return granted lifetime
    status: pending
  - id: modify-purchase-logic
    content: Modify purchase_lifetime() to check for zero karma and grant basic lifetime
    status: pending
  - id: optional-lifetime-tracking
    content: Optionally add is_granted field to Lifetime class for analytics
    status: pending

category: hopes
confidence: 0.78
constellation_date: 2026-01-14
---

# Basic Lifetime Grant: Zero Karma Mechanism

## Overview

When a being's karma reaches exactly 0.0, automatically grant a free "Basic Survival Lifetime" instead of raising `InsufficientKarmaError`. This maintains the economic loop while preserving karma's value.

## Implementation Plan

### 1. Add Survival Lifetime Type

**File**: `src/waft/karma_market.py`

- Add `SURVIVAL = "survival"` to `LifetimeType` enum (line 29-36)
- This distinguishes granted survival lifetimes from purchased ones

### 2. Create Basic Survival Lifetime Configuration

**File**: `src/waft/karma_market.py`

Add method `_get_basic_survival_lifetime_config()` that returns:

```python
{
    "id": "basic_survival",
    "name": "Basic Survival Lifetime",
    "type": "survival",
    "duration_minutes": 30,
    "tools": ["read_file", "codebase_search"],
    "personality": {
        "trait": "helpful",
        "style": "direct",
        "tone": "professional"
    },
    "objectives": ["Earn karma through experiences"],
    "karma_cost": 0.0,
    "description": "Granted survival lifetime - earn karma to continue",
    "is_granted": True  # Flag to indicate this is granted, not purchased
}
```

### 3. Implement `grant_basic_lifetime` Method

**File**: `src/waft/karma_market.py`

Create new method `grant_basic_lifetime(soul_id: str) -> Lifetime`:

- Loads basic survival lifetime config
- Creates Lifetime with 0 karma cost
- Sets `is_granted=True` metadata (add to Lifetime class if needed)
- Saves lifetime to disk
- Registers with Source Consciousness (if available)
- Returns the granted lifetime

### 4. Modify `purchase_lifetime` Method

**File**: `src/waft/karma_market.py` (lines 337-343)

Change the karma check logic:

```python
# Check karma balance
current_karma = self._get_soul_karma(soul_id)
if current_karma < base_cost:
    if current_karma == 0.0:
        # Grant basic survival lifetime
        return self.grant_basic_lifetime(soul_id)
    else:
        from .karma import InsufficientKarmaError
        raise InsufficientKarmaError(
            f"Insufficient karma: {current_karma} < {base_cost}"
        )
```

**Key Points**:

- Only grants when `current_karma == 0.0` (exactly zero)
- If `0 < current_karma < base_cost`, still raises `InsufficientKarmaError`
- This preserves economic consequences while preventing dead-ends

### 5. Update Lifetime Class (Optional Enhancement)

**File**: `src/waft/karma_market.py` (Lifetime class, lines 39-132)

Consider adding `is_granted: bool = False` field to track granted lifetimes:

- Add to `__init__` method
- Add to `to_dict()` method
- Add to `from_dict()` method

This allows tracking which lifetimes were granted vs. purchased for analytics.

### 6. Integration Points

**KarmaCollection**: No changes needed - granted lifetimes still generate karma through experiences, which is collected normally by `KarmaCollector`.

**Afterlife Market**: No changes needed - beings can still purchase treasures if they have karma, but cannot purchase if karma < cost (normal behavior).

**Lifetime Exchange**: No changes needed - beings can still trade lifetimes, but cannot create offerings if karma < price (normal behavior).

**Karmic Wagers**: No changes needed - beings can still place wagers, but cannot bet if karma < wager amount (normal behavior).

### 7. Testing Considerations

Test scenarios:

1. **Zero karma purchase attempt**: Should grant basic survival lifetime
2. **Low karma (< cost) purchase attempt**: Should raise `InsufficientKarmaError`
3. **Granted lifetime completion**: Should collect karma normally
4. **Granted lifetime karma earning**: Should allow being to purchase better lifetimes
5. **Multiple zero-karma grants**: Should allow multiple survival lifetimes if needed

## Files to Modify

1. `src/waft/karma_market.py`

   - Add `SURVIVAL` to `LifetimeType` enum
   - Add `_get_basic_survival_lifetime_config()` method
   - Add `grant_basic_lifetime()` method
   - Modify `purchase_lifetime()` karma check logic
   - Optionally add `is_granted` field to `Lifetime` class

## Design Decisions

1. **Only at exactly 0.0**: Grants only when karma is exactly zero, not when it's just insufficient. This maintains economic pressure while preventing dead-ends.

2. **Minimal tools**: Only `read_file` and `codebase_search` - enough to be useful but encourages earning karma for better tools.

3. **30 minutes duration**: Short enough to encourage completion and karma earning, long enough to be meaningful.

4. **No karma cost**: Granted, not purchased, so it doesn't create negative karma or debt.

5. **Normal karma collection**: Granted lifetimes still generate karma through experiences, maintaining the economic loop.

## Benefits

- Prevents beings from getting stuck in limbo
- Maintains the reincarnation cycle
- Preserves karma value (still need karma for better lifetimes)
- Allows recovery from zero karma
- Encourages karma accumulation
- Maintains economic consequences (can't purchase if 0 < karma < cost)