= Priority Scoring Algorithm

The priority scoring algorithm is the heart of Auto-Work's decision-making. It calculates a numerical score for each work effort, with higher scores indicating higher priority.

== Scoring Formula Overview

The total priority score is calculated as:

```
Total Score = Status Weight + Priority Level + Content Indicators + 
              Recent Activity + Empirica Adjustment + Pantheon Adjustment
```

== Factor 1: Status Weighting

Work effort status is the primary factor, as active work should be prioritized:

| Status | Points | Description |
|--------|--------|-------------|
| `active` | 100.0 | Currently in progress (highest priority) |
| `paused` | 50.0 | Temporarily stopped |
| `open` | 30.0 | Not yet started |
| `completed` | 0.0 | Finished (excluded from selection) |

*[Example]*: An `active` work effort starts with 100 points, while a `paused` one starts with 50.

== Factor 2: Priority Level

Explicit priority levels add to the base score:

| Priority | Points | Description |
|----------|--------|-------------|
| `CRITICAL` | +50.0 | Urgent, must be addressed |
| `HIGH` | +30.0 | Important, should be done soon |
| `MEDIUM` | +15.0 | Normal priority |
| `LOW` | +5.0 | Can wait |

*[Example]*: A `CRITICAL` work effort gets +50 points, while `MEDIUM` gets +15.

== Factor 3: Content Indicators

The system analyzes work effort content for indicators of work needed:

| Indicator | Points | Description |
|-----------|--------|-------------|
| Contains `TODO` | +20.0 | Tasks to be done |
| Contains `FIXME` | +25.0 | Issues to be fixed |
| Contains `bug`/`error` | +15.0 | Bugs or errors mentioned |

*[Example]*: A work effort with both `TODO` and `FIXME` gets +45 points.

== Factor 4: Recent Activity

Recent git commits indicate active work:

- +5.0 points per commit in last 7 days
- Maximum: 20.0 points (capped at 4 commits)

*[Example]*: A work effort with 3 commits in the last week gets +15 points.

== Factor 5: Empirica Adjustment

When Empirica is available, the system uses epistemic gates to adjust priority:

| Gate Result | Adjustment | Description |
|-------------|------------|-------------|
| `PROCEED` | +10.0 | High confidence, ready to proceed |
| `HALT` | +20.0 | Requires attention, boost priority |
| `BRANCH` | +15.0 | Needs investigation, moderate boost |
| `REVISE` | 0.0 | No adjustment |
| `None` | 0.0 | Empirica unavailable |

*[Example]*: If Empirica gate returns `HALT`, the work effort gets +20 points.

== Factor 6: Pantheon Adjustments

Pantheon entities provide additional context:

=== Judge Evaluation

The Judge evaluates work effort readiness:

- `PROVEN` with confidence > 0.7: +15.0 points
- `DISPROVEN` with confidence > 0.7: -10.0 points
- `PROBABLE` with confidence > 0.6: +8.0 points

=== Magistrate Precedents

Similar work efforts found:

- +5.0 points per proven precedent (max 3 precedents)

=== Librarian Knowledge Base

Work effort referenced in knowledge base:

- +3.0 points per related record (max 3 records)

=== GitHubGod Repository State

Work effort branch matches current branch:

- +10.0 points if branch matches

== Complete Example Calculation

Let's calculate the score for a work effort:

*[Work Effort Details]*:
- Status: `active` → 100.0 points
- Priority: `HIGH` → +30.0 points
- Contains `TODO` → +20.0 points
- Contains `FIXME` → +25.0 points
- 2 commits in last 7 days → +10.0 points
- Empirica gate: `PROCEED` → +10.0 points
- Judge: `PROVEN` (confidence 0.8) → +15.0 points
- Magistrate: 2 proven precedents → +10.0 points
- GitHubGod: Branch matches → +10.0 points

*[Total Score]*: 100 + 30 + 20 + 25 + 10 + 10 + 15 + 10 + 10 = *[230.0 points]*

== Score Comparison

Work efforts are sorted by total score, with the highest scoring work effort selected.

== Score Visualization

```
Work Effort A: ████████████████████ 230.0 (Selected)
Work Effort B: ████████████ 150.0
Work Effort C: ████████ 100.0
Work Effort D: ████ 50.0
```

== Important Notes

- Completed work efforts always score 0.0 and are excluded
- Scores are calculated dynamically on each run
- Empirica and Pantheon adjustments are optional (graceful degradation)
- Content analysis is case-insensitive
- Git activity is limited to the last 7 days

== Next Steps

Now that you understand priority scoring, let's see how work efforts are selected.
