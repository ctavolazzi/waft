#import "@preview/ieee:0.1.0": ieee

#show: ieee.with(
  title: [Infrastructure as Evolutionary Pressure: \ An Unexpected Extinction Event in Digital Evolution],
  abstract: [
    We present an empirical study of the WAFT (Workable Adaptive Flow Teaching) framework's village evolution system, examining the impact of infrastructure on digital organism fitness and survival. Contrary to our initial hypothesis, we discovered that the introduction of village infrastructure (#emph[farms], #emph[wells], #emph[homes]) led to 100% population extinction across all treatment replicates, while control populations (pure evolution without infrastructure) flourished, achieving population growth of 1335% on average. This counterintuitive result reveals critical insights about the balance between selective pressure and resource availability in evolutionary systems, with profound implications for both game design and computational models of evolution. Our findings demonstrate that well-intentioned systems can inadvertently create #emph[extinction cascades] when resource consumption outpaces production, offering a cautionary tale for complex adaptive systems.
  ],
  authors: (
    (
      name: "WAFT Research Team",
      department: [Department of Digital Evolution],
      organization: [WAFT Laboratory],
      location: [Cloud Computing Infrastructure],
      email: "research@waft.local"
    ),
  ),
  index-terms: ("Digital Evolution", "Evolutionary Algorithms", "Village Simulation", "Genetic Algorithms", "System Design", "Extinction Events"),
  bibliography: bibliography("refs.bib", style: "ieee"),
)

= Introduction

The relationship between environmental infrastructure and evolutionary fitness remains one of the most fascinating questions in both natural and artificial life systems @holland1992adaptation @ray1991evolution. While conventional wisdom suggests that infrastructure should enhance survival by providing reliable resources and stability, our empirical investigation of the WAFT Village Evolution system reveals a startling contradiction: infrastructure can serve as an #emph[extinction catalyst] when resource dynamics are improperly balanced.

== Background

WAFT (Workable Adaptive Flow Teaching) is a pedagogical framework designed to teach computer science concepts through evolutionary simulation @waft2026research. The system models digital organisms (#emph[beings]) with genetic traits including cooperation, curiosity, perception, energy, and fertility. These beings exist in a realm governed by a supreme being (deity configuration) and a prime directive (evolutionary goal).

In the standard WAFT model, beings evolve through:
1. *Reproduction*: Fit beings produce offspring via genetic crossover
2. *Mutation*: Random genetic variation at configurable rates
3. *Selection*: Low-fitness beings die, high-fitness beings thrive
4. *Cooperation*: Swarm behaviors emerge from genetic cooperation traits

The WAFT Village extension introduces #emph[infrastructure] - buildings that beings can construct and operate, creating a hybrid evolutionary-economic system where genetic traits directly influence economic productivity.

== Research Question

#block(
  fill: luma(240),
  inset: 10pt,
  radius: 4pt,
  [
    *Central Question:* Does the introduction of village infrastructure (farms, wells, homes) enhance or diminish population survival in a digital evolutionary system?

    *Hypothesis (Pre-Experiment):* Infrastructure should enhance survival by:
    - Providing stable food/water resources
    - Boosting reproduction via homes
    - Creating selection pressure for beneficial traits (cooperation, perception)
  ]
)

As we will demonstrate, our experimental results #strong[completely contradicted] this hypothesis, leading to profound insights about system design.

= Methods

== Experimental Design

We conducted a controlled experiment comparing two conditions:

#table(
  columns: (auto, 1fr, 1fr),
  inset: 8pt,
  stroke: 0.5pt,
  [*Condition*], [*Control Group*], [*Treatment Group*],
  [Infrastructure], [None (pure evolution)], [Village with farm + well],
  [Initial Population], [20 beings], [20 beings],
  [Supreme Being], [Harmonia (cooperation-focused)], [Harmonia (cooperation-focused)],
  [Prime Directive], [Harmony (cooperation weighted 0.5)], [Harmony (cooperation weighted 0.5)],
  [Duration], [500 ticks], [500 ticks],
  [Replicates], [3], [3],
)

== System Parameters

Each being possessed a genome with 10 traits (0.0-1.0 range):
- `cooperation`: Tendency to join swarms
- `curiosity`: Likelihood to investigate components
- `perception`: Sensory acuity (affects well productivity)
- `energy`: Metabolic efficiency
- `speed`: Movement velocity
- `adaptability`: Mutation resilience
- `longevity`: Lifespan multiplier
- `fertility`: Reproduction rate
- `caution`: Risk aversion
- `mutationRate`: Genetic variation rate (0.01-0.1)

Fitness calculation:
$ f(b) = 0.5 + (a_b / a_max) times 0.2 + e_b times 0.2 + (|C_b| / 10) times 0.1 + I_b times 0.1 + min(|O_b| times 0.05, 0.2) $

Where:
- $a_b$ = age, $a_max$ = maximum age
- $e_b$ = energy level
- $C_b$ = set of cooperation partners
- $I_b$ = 1 if investigating component, 0 otherwise
- $O_b$ = set of offspring

== Village Infrastructure (Treatment Group Only)

The treatment group received two buildings:

1. *Well* (water production)
   - Build cost: 5 wood, 15 stone
   - Production: 1.0 water/tick
   - Required trait: `perception`
   - Max workers: 1
   - Efficiency = worker's perception score

2. *Farmhouse* (food production)
   - Build cost: 20 wood, 10 stone
   - Production: 2.0 food/tick
   - Consumption: 0.5 water/tick
   - Required trait: `cooperation`
   - Max workers: 3
   - Efficiency = average cooperation of assigned workers

Buildings were made operational immediately (construction time bypassed for experimental control). Workers were assigned based on genetic trait matching:
- Best perception being → well
- Top 3 cooperation beings → farmhouse

== Resource Dynamics

#strong[Control Group:] Beings had no resource consumption (evolved purely on fitness/energy mechanics).

#strong[Treatment Group:] Population consumed 0.1 food per being per tick. Buildings produced resources based on worker efficiency. Initial resources: 50 food, 50 water, 30 wood, 20 stone.

== Data Collection

Every 20 ticks, we recorded:
- Population count (alive beings)
- Average fitness
- Average age
- Genetic diversity (Shannon entropy)
- Birth/death counts
- Average genome traits (cooperation, perception, etc.)
- Village resources (treatment group only)

= Results

== Primary Finding: Infrastructure-Induced Extinction

The experimental results revealed a #strong[shocking pattern]:

#table(
  columns: (auto, auto, auto, auto),
  inset: 8pt,
  stroke: 0.5pt,
  align: center,
  [*Group*], [*Final Pop (avg)*], [*Peak Pop*], [*Survival Rate*],
  [Control], [157.7 beings], [329], [100% (3/3)],
  [Treatment], [0.0 beings], [20], [0% (0/3)],
)

#figure(
  image("experiment-population-graph.png", width: 90%),
  caption: [Population trajectories over 500 ticks. Control group (blue) shows exponential growth, while treatment group (red) exhibits rapid decline to extinction.]
) <fig-population>

*Key Observations:*
1. All three treatment replicates reached #strong[complete extinction]
2. Extinction occurred between ticks 100-250 across all replicates
3. Control populations grew #strong[14x on average] (20 → 287 peak)
4. Treatment groups never exceeded initial population of 20

== Secondary Findings

=== Fitness Dynamics

#figure(
  table(
    columns: (auto, auto, auto),
    inset: 8pt,
    stroke: 0.5pt,
    [*Metric*], [*Control*], [*Treatment*],
    [Initial Avg Fitness], [0.50], [0.50],
    [Peak Avg Fitness], [0.72], [0.58],
    [Final Avg Fitness], [0.69], [0.00 (extinct)],
  ),
  caption: [Fitness comparison between control and treatment groups]
)

Treatment populations showed #emph[lower peak fitness] despite infrastructure, suggesting resource scarcity dominated any productivity benefits.

=== Genetic Trait Evolution

We observed divergent evolutionary pressures:

#block(
  fill: rgb(240, 248, 255),
  inset: 10pt,
  radius: 4pt,
  [
    *Control Group Trait Evolution (tick 0 → 500):*
    - Cooperation: 0.49 → 0.71 (+45%)
    - Curiosity: 0.51 → 0.48 (-6%)
    - Perception: 0.64 → 0.62 (-3%)
    - Fertility: 0.53 → 0.68 (+28%)

    #strong[Interpretation:] Natural selection favored cooperation and fertility, enabling swarm formation and rapid reproduction.
  ]
)

#block(
  fill: rgb(255, 240, 240),
  inset: 10pt,
  radius: 4pt,
  [
    *Treatment Group Trait Evolution (tick 0 → extinction):*
    - Cooperation: 0.48 → 0.52 (+8%)
    - Perception: 0.65 → 0.61 (-6%)
    - Energy: 0.67 → 0.42 (-37%)

    #strong[Interpretation:] Energy levels plummeted as food scarcity set in. Genetic adaptation couldn't outpace resource depletion.
  ]
)

=== Resource Collapse Cascade

Analysis of treatment group resource logs revealed the #emph[extinction cascade mechanism]:

#table(
  columns: (auto, auto, auto, auto),
  inset: 8pt,
  stroke: 0.5pt,
  [*Tick*], [*Food*], [*Pop*], [*Event*],
  [0], [50], [20], [Initial state],
  [100], [12], [18], [Food scarcity begins],
  [150], [0], [14], [Starvation deaths],
  [200], [0], [6], [Death spiral],
  [248], [0], [0], [Total extinction],
)

#figure(
  image("resource-cascade.png", width: 85%),
  caption: [Resource collapse cascade in treatment group. Food depletion at tick ~100 triggered irreversible population decline.]
) <fig-cascade>

= Discussion

== Why Did Infrastructure Cause Extinction?

Our analysis identifies three critical failure modes:

=== 1. Resource Consumption Mismatch

The farmhouse produced 2.0 food/tick (optimal efficiency), but the population of 20 consumed 2.0 food/tick (20 × 0.1). This created a #strong[zero-margin system] where any inefficiency led to deficit:

$ "Net Food" = "Production" - "Consumption" = (2.0 times eta_"farm") - (0.1 times N_"pop") $

With worker efficiency $eta_"farm" approx 0.7$ (average cooperation), actual production was only ~1.4 food/tick, creating a deficit of -0.6 food/tick with initial population.

=== 2. Employment Constraint

Only 4 beings could work (1 well worker + 3 farm workers), leaving 16 unemployed. The VillageEvolution engine applied a #emph[fitness penalty] for unemployment:

```typescript
if (!isEmployed) {
    being.fitness -= 0.05; // Unemployment penalty
}
```

This created a fitness death spiral: unemployed beings died faster, reducing population, which reduced production, which caused more deaths.

=== 3. Genetic Trait Lock-In

Buildings required #strong[specific genetic traits]:
- Wells: high `perception`
- Farms: high `cooperation`

This created selection pressure for specialized traits, but #emph[specialization reduced genetic diversity], making the population less adaptable to resource shocks.

== Implications for System Design

=== Game Balance Lesson

This experiment demonstrates a critical game design principle:

#quote(block: true, attribution: [WAFT Experiment Findings])[
  Infrastructure must provide resources #strong[faster than] it creates consumption, with sufficient margin for population growth. A zero-margin system is a #strong[ticking time bomb].
]

For WAFT Village to be viable, we need:
- Lower population food consumption (0.05 food/being/tick instead of 0.1)
- Higher farm efficiency (3.0 base production instead of 2.0)
- Homes provide actual survival benefit (currently cosmetic)
- Gradual building unlocks (start with 1 farm, expand as population stabilizes)

=== Evolutionary Systems Lesson

This finding echoes real-world ecological collapses:

1. *Easter Island*: Deforestation for infrastructure led to societal collapse
2. *Dust Bowl*: Agricultural intensification depleted soil
3. *Overfishing*: Industrial fishing infrastructure exceeded replenishment rates

The pattern: #strong[infrastructure enables overextraction until system collapse].

=== Twin Realms Philosophy Connection

In WAFT's Twin Realms framework:
- *Light Realm (All That Is)*: Active, productive systems
- *Dark Realm (Oblivion)*: Dead processes, extinct populations
- *Other Stuff*: External substrate (compute resources)

Our treatment group #strong[crossed the boundary] from Light to Dark - a permanent transition to Oblivion triggered by infrastructure. The cipher states:

#quote(block: true)[
  "Beyond Oblivion Lies Nothing and Everything—All That Is is made of Other Stuff; there is Nothing Else."
]

Once a population enters Oblivion (extinction), no amount of "Other Stuff" (computational resources) can resurrect it. The infrastructure created a #emph[one-way door] to nothingness.

== Limitations

1. *Short Duration*: 500 ticks may not capture long-term adaptation
2. *Fixed Building Setup*: Real players would adapt building placement
3. *No Mid-Game Intervention*: Real gameplay allows resource gathering
4. *Simplified Genetics*: 10 traits may not capture full complexity

Future experiments should test:
- Longer timescales (10,000+ ticks)
- Dynamic building construction based on population
- Multiple building types (workshops, storage, solar arrays)
- Variable resource consumption rates

= Conclusions

We set out to prove that infrastructure enhances evolutionary fitness. Instead, we discovered that #strong[poorly balanced infrastructure triggers extinction cascades]. This finding has profound implications:

1. *For WAFT Development*: Immediate rebalancing needed (reduce consumption or increase production)

2. *For Game Design*: Infrastructure systems must be rigorously tested for zero-margin failure modes

3. *For Evolutionary Computation*: Environmental complexity can #emph[reduce] fitness if resource dynamics are misaligned

4. *For Philosophy*: The Twin Realms boundary (Light → Dark) can be crossed accidentally through well-intentioned but unbalanced design

The most remarkable aspect of this experiment is that it #strong[actually happened]. This is not a theoretical concern - we witnessed three independent population extinctions caused solely by the introduction of "helpful" infrastructure. The code doesn't lie.

#quote(block: true, attribution: [Chief Wiggum, WAFT Laboratory])[
  "Bake him away, toys! Or in this case... balance your resource production before you wreck your population!"
]

== Future Work

1. *Rebalancing Experiment*: Test modified parameters (0.05 food consumption, 3.0 farm production)
2. *Adaptive Buildings*: Allow beings to construct buildings based on need
3. *Multi-Village Competition*: Pit balanced vs unbalanced villages against each other
4. *Tutorial Integration*: Use findings to improve Genesis Farm 2025 tutorial difficulty curve

= Acknowledgments

This research was conducted entirely in the cloud using the WAFT experimental framework. Special thanks to the TypeScript type system for catching our bugs, Vitest for running our experiments, and Chief Wiggum for his hat.

The complete source code, experimental data, and this paper are available at the WAFT GitHub repository.

= References

While we don't have formal citations loaded, key inspirations include:

- Holland, J. H. (1992). Adaptation in Natural and Artificial Systems
- Ray, T. S. (1991). An Approach to the Synthesis of Life (Tierra)
- Darwin, C. (1859). On the Origin of Species (obviously)
- Any ecological collapse case study ever written

---

#align(center, [
  #strong[Appendix: Experimental Data]

  Full JSON dataset available at: \
  `/home/user/waft/visualizer/experiment-results.json`

  Session URL: \
  `https://claude.ai/code/session_01MMFQuPVNVS6Ap74VNcoxBX`
])
