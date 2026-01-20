= Work Effort Selection

This chapter describes how Auto-Work selects the best work effort.

== Selection Process

1. Collect all work efforts
2. Filter out completed work efforts
3. Calculate priority scores
4. Sort by score (highest first)
5. Select highest scoring work effort

== Filtering

Completed work efforts are excluded:

- Status: `completed` → Score: 0.0 → Excluded

== Sorting

Work efforts are sorted by total priority score:

```
Highest Score → Selected
Second Highest → Not selected
Third Highest → Not selected
...
```

== Selection Example

```
Work Effort Scores:
  WE-260118-abc1: 230.0 points ✅ Selected
  WE-260118-def2: 150.0 points
  WE-260117-ghi3: 100.0 points
  WE-260116-jkl4: 50.0 points
```

== Next Steps

Now let's explore action determination.
