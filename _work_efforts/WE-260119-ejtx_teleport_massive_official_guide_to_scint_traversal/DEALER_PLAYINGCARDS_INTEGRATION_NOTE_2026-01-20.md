# Dealer + playingcards Adapter Note (2026-01-20)

## Summary
Introduced a small adapter layer to encapsulate the `playingcards` dependency and updated Dealer-related code to depend on the adapter instead of importing `playingcards` directly.

## Changes
- Added adapter: `src/waft/dealer/card_generator.py`
- Updated Dealer gates: `src/waft/dealer/gates.py`
- Updated cards CLI: `src/waft/cli/cards_cli.py`

## Rationale
Centralizing the dependency makes it easier to swap implementations or mock card generation without touching gameplay logic or CLI surfaces.
