= D&D Campaign Integration

Auto-Work integrates with the D&D campaign system to generate quest PDFs.

== What is D&D Campaign?

The D&D campaign system runs scenarios and generates quest PDFs using Typst templates.

== Integration

After successful execution, Auto-Work:

1. Runs a D&D scenario (encounter, explore, or lore)
2. Generates quest markdown from scenario
3. Creates quest PDF using Typst
4. Saves quest PDF to work effort directory

== Scenario Types

- *[Encounter]*: Combat scenarios
- *[Explore]*: Location discovery
- *[Lore]*: World building

== Example Output

```
⚔️  D&D Campaign: Running scenario...
   Scenario Mode: encounter
   Quest PDF: _work_efforts/WE-260118-abc1/quest_20260119_102530.pdf
```

== Next Steps

Now let's explore safety mechanisms in detail.
