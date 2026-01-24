# Improve Summary

**Date**: 2026-01-20  
**Scope**: Oracle workflow + CLI reliability

## Top Improvements (Prioritized)
1. **Oracle fallback**: Add degraded-mode guidance when Oracle errors occur.
2. **Check-assumptions reliability**: Re-run after fix; add automated tests.
3. **Empirica logging resilience**: Include session-id by default or retry on lock.
4. **Optional dependency warnings**: Surface TinyDB/d20/tracery fallback state.
5. **Bananote font availability**: Install New Computer Modern Sans or configure fallback.

## Notes
- Critical NameError resolved with `Any` import, but end-to-end re-test is pending.
