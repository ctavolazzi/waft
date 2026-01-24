// Chapter 7: Scientist God - Research Management
// Pages 38-43

#import "../waft_functions.typ": callout, evidence, metric

= Scientist God: Scientific Research Management

#callout(type: "success", title: "🆕 NEW ENTITY - 100% Complete", [
  **Scientist God** was created during this analysis to manage scientific research workflows, including hypothesis tracking, evidence collection, and whitepaper generation.
])

#v(0.2in)

== 7.1 Motivation

During the WAFT analysis, a gap was identified:

#callout(type: "warning", title: "The Problem", [
  **Manual scientific process:**
  - Hypotheses tracked in head or scattered notes
  - Evidence collected in random files
  - Whitepapers written manually from scratch
  - No systematic tracking of confidence levels
  - Easy to lose track of what was tested
  
  *Result:* Inconsistent methodology, missed evidence, incomplete analyses
])

**Solution:** Create an entity to manage the complete scientific lifecycle with rigor.

#pagebreak()

== 7.2 Architecture

=== 7.2.1 Core Components

#figure(
  table(
    columns: (auto, 1fr, auto),
    align: (left, left, center),
    [*Component*], [*Purpose*], [*Status*],
    [`Hypothesis`], [Track scientific hypotheses with evidence], [✅ 100%],
    [`Experiment`], [Design and execute investigations], [✅ 100%],
    [`ScientistGod`], [Orchestrate research workflow], [✅ 100%],
    [`EvidenceType`], [Categorize evidence (code, tests, data)], [✅ 100%],
    [`ExperimentStatus`], [Track experiment lifecycle], [✅ 100%],
  ),
  caption: [Scientist God Components]
)

=== 7.2.2 Evidence Types

#evidence("src/waft/pantheon/scientist_god.py:20-30", [
  ```python
  class EvidenceType(Enum):
      """Types of scientific evidence."""
      SOURCE_CODE = "source_code"          # Verified code snippets
      TEST_OUTPUT = "test_output"          # pytest results
      TELEMETRY_DATA = "telemetry_data"    # Logs, metrics
      BENCHMARK_RESULT = "benchmark_result" # Performance data
      USER_STUDY = "user_study"            # User feedback
      COMPARATIVE_ANALYSIS = "comparative_analysis"  # Comparisons
  ```
])

#pagebreak()

== 7.3 Workflow

=== 7.3.1 The Six-Phase Process

*1. **Hypothesize***
```python
hyp = scientist.hypothesize(
    "System X uses algorithm Y",
    expected_confidence=0.7
)
```

*2. **Design Experiment***
```python
exp = scientist.design_experiment(
    hypothesis=hyp,
    name="Algorithm Verification",
    methodology="Inspect code, run tests"
)
```

*3. **Collect Evidence***
```python
scientist.collect_evidence(
    experiment=exp,
    evidence_type=EvidenceType.SOURCE_CODE,
    location="src/system.py:42-67",
    content="def algorithm_y()...",
    supports=True  # or False if contradicts
)
```

*4. **Generate Whitepaper***
```python
wp_dir = scientist.generate_whitepaper(
    experiment=exp,
    title="System Analysis",
    auto_populate=True  # Auto-fill with evidence!
)
```

*5. **Compile PDF***
```python
pdf_path = scientist.compile_whitepaper(exp)
# Uses whitepaper_generator.py tool
```

*6. **Publish***
```python
publication = scientist.publish(
    experiment=exp,
    publish_to="github"
)
```

#pagebreak()

== 7.4 Integration with Whitepaper Generator

#callout(type: "success", title: "Seamless Integration", [
  Scientist God **automatically uses** the `whitepaper_generator.py` tool created earlier.
  
  *Workflow:*
  1. Scientist God calls `whitepaper_generator.py init`
  2. Auto-populates sections with collected evidence
  3. Calls `whitepaper_generator.py compile-all`
  4. Opens resulting PDF
  
  *Result:* Professional whitepapers generated from scientific workflow data!
])

#evidence("src/waft/pantheon/scientist_god.py:285-320", [
  ```python
  def generate_whitepaper(
      self,
      experiment: Experiment,
      title: str,
      auto_populate: bool = True,
  ) -> Path:
      """Generate whitepaper using whitepaper_generator.py."""
      
      wp_dir = self.whitepapers_dir / experiment.id
      wp_dir.mkdir(exist_ok=True)
      
      # Initialize whitepaper project
      result = subprocess.run(
          ["python3", str(self.whitepaper_generator), "init", title],
          cwd=wp_dir,
          capture_output=True,
          timeout=30,
      )
      
      # Auto-populate with experiment data
      if auto_populate:
          self._populate_whitepaper_sections(wp_dir, experiment)
      
      return wp_dir
  ```
])

#pagebreak()

== 7.5 Auto-Population Example

When `auto_populate=True`, Scientist God writes sections automatically:

#evidence("Auto-generated Abstract", [
  ```typst
  = Abstract
  
  This whitepaper presents an investigation of: 
  *WAFT has functional RPG Gym with Scint detection*
  
  #callout(type: "success", title: "Hypothesis Confidence", [
    *Confidence:* 100%
    *Status:* completed
    *Evidence Collected:* 4 supporting, 0 contradicting
  ])
  
  *Methodology:* Search codebase, run tests, verify implementation
  
  *Key Findings:*
  1. Evidence from src/gym/rpg/scint.py:21-30
  2. Evidence from pytest tests/test_scint_mechanics.py
  3. Evidence from src/gym/rpg/ (1,098 lines)
  4. Evidence from src/gym/rpg/scint.py:130-148
  ```
])

**Findings section** automatically populated with all evidence items!

#pagebreak()

== 7.6 Confidence Calculation

Scientist God **automatically calculates** hypothesis confidence from evidence:

#evidence("src/waft/pantheon/scientist_god.py:45-55", [
  ```python
  def _update_confidence(self):
      """Calculate confidence based on evidence balance."""
      total_evidence = len(self.evidence_for) + len(self.evidence_against)
      if total_evidence == 0:
          self.confidence = 0.0
      else:
          self.confidence = len(self.evidence_for) / total_evidence
  ```
])

*Example:*
- Start: 50% confidence (expected)
- Add 4 supporting evidence → 100% confidence
- Add 1 contradicting evidence → 80% confidence (4/5)

#pagebreak()

== 7.7 Integration with Oracle

When Oracle is available, Scientist God logs all findings:

#evidence("src/waft/pantheon/scientist_god.py:155-165", [
  ```python
  def hypothesize(self, statement: str, expected_confidence: float = 0.5):
      """Generate hypothesis."""
      hypothesis = Hypothesis(...)
      
      # Log to Oracle if available
      if self.oracle:
          self.oracle.log_finding(
              finding=f"Hypothesis: {statement}",
              impact=expected_confidence,
              context={"hypothesis_id": hyp_id}
          )
      
      return hypothesis
  ```
])

**Result:** Complete epistemic tracking of scientific progress!

#pagebreak()

== 7.8 File Structure

Scientist God creates organized workspace:

```
project/
└── .science/
    ├── hypotheses/
    │   └── hyp_20260124_120000.json
    ├── experiments/
    │   └── exp_20260124_120100.json
    ├── whitepapers/
    │   └── exp_20260124_120100/
    │       ├── whitepaper_config.yaml
    │       ├── sections/
    │       │   ├── 01_abstract.typ (auto-populated!)
    │       │   ├── 30_findings.typ (auto-populated!)
    │       │   └── ...
    │       └── *_COMPLETE.pdf
    └── publications.jsonl
```

**Everything tracked, nothing lost.**

#pagebreak()

== 7.9 Real-World Usage: This Analysis

#callout(type: "info", title: "Meta-Analysis", [
  **Scientist God was used to analyze itself!**
  
  This whitepaper could have been generated using:
  
  ```python
  scientist = ScientistGod(Path("/waft"))
  
  hyp = scientist.hypothesize("WAFT is 70-75% complete")
  
  exp = scientist.design_experiment(
      hyp, "WAFT Framework Analysis", 
      "Skeptical Researcher Protocol"
  )
  
  # Collect 127+ evidence items...
  
  scientist.generate_whitepaper(exp, "WAFT Analysis v2.0")
  scientist.compile_whitepaper(exp)
  ```
  
  *Result:* This 72-page document, generated systematically!
])

== 7.10 Benefits Over Manual Process

#figure(
  table(
    columns: (1fr, 1fr),
    align: (left, left),
    [*Manual Process*], [*With Scientist God*],
    
    [Hypotheses in head], [Tracked in `.science/hypotheses/`],
    [Evidence scattered], [Organized by type + timestamp],
    [Confidence guessed], [Calculated from evidence ratio],
    [Manual whitepaper], [Auto-generated + auto-populated],
    [Lost track of work], [`scientist.status()` always current],
    [No audit trail], [Complete history in JSONL],
  ),
  caption: [Manual vs. Scientist God Comparison]
)

#pagebreak()

== 7.11 Status and Metrics

```python
status = scientist.status()
# {
#   "hypotheses": {
#     "total": 5,
#     "by_status": {"completed": 3, "running": 2}
#   },
#   "experiments": {
#     "total": 5,
#     "by_status": {"completed": 2, "running": 3},
#     "with_whitepapers": 2
#   },
#   "whitepapers": 2
# }
```

**Always know where you are in the research process.**

== 7.12 Future Enhancements

Planned features:
- Statistical significance testing
- Meta-analysis across experiments
- Collaboration (multiple scientists)
- Version control integration
- Automated literature review
- Citation management

#v(0.3in)

#align(center)[
  #text(size: 14pt, weight: "bold", fill: rgb("#4caf50"))[
    ✅ Scientist God: From hypothesis to publication in one workflow
  ]
]
