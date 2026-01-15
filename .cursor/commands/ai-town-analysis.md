# AI-Town Analysis

**An AI town of Beings analyzes repositories and research papers through collective analysis and voting, producing a PDF binder or single PDF (town's choice).**

Spawns an AI town (3-5 Beings) that collectively analyzes a repository and research paper. Each Being contributes analysis, and the command randomly selects some Beings to vote on decisions (mostly at random, weighted by relevance). The town collectively produces the final PDF output based on the votes of selected Beings.

**Use when:** You want collective AI analysis with voting, need multiple perspectives on repository/paper analysis, want democratic decision-making, or need a comprehensive analysis produced by an AI town.

---

## Purpose

This command provides:
- **AI Town Creation**: Spawns 3-5 Beings into analysis reality
- **Collective Analysis**: Each Being analyzes different aspects
- **Democratic Voting**: Command randomly selects some Beings to vote (mostly at random, weighted by relevance)
- **Town Decisions**: Town votes on PDF format (binder vs single PDF)
- **Collaborative Output**: All Beings contribute to final PDF/binder
- **Genetic Lineage**: Each Being's analysis tracked with lineage

---

## Philosophy

### 1. AI Town Democracy

The command creates a democratic AI town:
- **Multiple Perspectives**: Each Being brings different skills and viewpoints
- **Random Selection**: Command randomly selects some Beings to vote (mostly at random)
- **Collective Decisions**: Town votes on important decisions
- **Town Choice**: Selected Beings vote on PDF format (binder vs single PDF) - majority wins

### 2. Distributed Analysis

Analysis is distributed across Beings:
- **Specialization**: Each Being focuses on different aspects
- **Collaboration**: Beings share findings with each other
- **Synthesis**: Town synthesizes all findings into final output
- **Quality**: Multiple perspectives improve analysis quality

### 3. Being Autonomy

Beings have autonomy:
- **Vote or Abstain**: Each Being chooses whether to participate in votes
- **Analysis Focus**: Beings can choose what to analyze
- **Contribution Style**: Beings contribute in their own way
- **Sleep/Rest**: Beings can rest if decision fatigue is high

### 4. Collective Output

The town produces the final output:
- **Town Vote**: Town votes on PDF format (binder vs single PDF)
- **Collaborative Writing**: All Beings contribute sections
- **Democratic Process**: Majority vote determines format
- **Town Document**: Final output is the town's collective work

---

## Workflow Sequence

The command executes 6 phases in order:

### Phase 1: Town Formation & Orientation

**Commands**: `/context`, `/oracle`

**Purpose**: Get oriented, understand analysis targets, then spawn the AI town

**Execution**:
1. Get current context summary (working state, active work, recent activity)
2. Consult Oracle for initial epistemic state:
   - What do we know about the repository?
   - What do we know about the research paper?
   - What are the knowledge gaps?
3. Identify repository and paper from conversation context
4. **Spawn AI Town** (3-5 Beings):
   - Reality ID: `"[repo]_analysis_town"`
   - Each Being with different initial skills:
     - Being 1: Architecture & patterns (high code_analysis, pattern_recognition)
     - Being 2: Algorithms & data structures (high algorithm_extraction, data_analysis)
     - Being 3: Paper analysis & comparison (high research_analysis, comparison)
     - Being 4: Integration opportunities (high integration_analysis, waft_knowledge)
     - Being 5: Documentation & synthesis (high documentation, synthesis)
   - Each Being spawned from Source with unique skills
5. Create town reality and spawn all Beings into it

**Expected Output**:
- Context document: `_work_efforts/CONTEXT_YYYY-MM-DD_HHMMSS.md`
- Oracle epistemic state summary
- Town reality created: `[repo]_analysis_town`
- 3-5 Beings spawned with IDs and skills
- Town roster document

**Time Estimate**: ~3-5 minutes

---

### Phase 2: Distributed Analysis (Town Works)

**Command**: Each Being executes analysis workflow

**Purpose**: Each Being analyzes their assigned aspect of repository and paper

**Execution**:
1. **Assign Analysis Tasks**:
   - Being 1: Architecture & patterns (Convex, PixiJS, state management)
   - Being 2: Algorithms & data structures (movement, memory, conversation)
   - Being 3: Paper analysis & comparison (extract concepts, compare to implementation)
   - Being 4: Integration opportunities (WAFT + repository patterns)
   - Being 5: Documentation & synthesis (organize findings, create summaries)

2. **Each Being Executes**:
   - Being spawns their own `/run-it` workflow focused on their task
   - Or Being executes focused analysis commands:
     - `/deep-analyze` for their specific focus area
     - `/hypothesis` for their findings
     - `/verify` for their claims
   - Being documents their analysis in their own work effort
   - Being shares findings with town (via town reality)

3. **Town Collaboration**:
   - Beings can read each other's findings
   - Beings can build on each other's work
   - Town reality stores shared findings
   - Beings synthesize collective knowledge

**Expected Output** (from each Being):
- Being-specific analysis documents
- Being's hypotheses and findings
- Being's verification traces
- Being's contribution to town knowledge

**Time Estimate**: ~20-40 minutes (parallel execution, longest Being determines total time)

---

### Phase 3: Town Voting on Decisions

**Command**: Town voting system

**Purpose**: Town votes on key decisions (command randomly selects some Beings to vote)

**Voting System**:
1. **Present Decisions to Town**:
   - Decision 1: "What are the top 3 integration opportunities?"
   - Decision 2: "What should be the priority for next steps?"
   - Decision 3: "What format should the final output be?" (binder vs single PDF)
   - Decision 4: "What sections should be included in the output?"

2. **For Each Decision**:
   - **Command randomly selects some Beings** (mostly at random, weighted by relevance)
   - Selection size: Typically 50-70% of town (e.g., 2-3 Beings from 5, or 3-4 from 7)
   - Present decision and options to selected Beings only
   - Selected Beings vote (with reasoning)
   - Other Beings are not asked (they don't participate in this vote)
   - Collect votes from selected Beings
   - Calculate results (majority vote wins, ties broken by Oracle)

3. **Vote Collection**:
   - Each selected Being's vote recorded with:
     - Being ID
     - Vote choice
     - Reasoning (why they voted this way)
     - Selection status (selected by command for this vote)
   - Non-selected Beings documented (not asked to vote)
   - Votes stored in town reality
   - Results calculated and presented

4. **Decision Results**:
   - Majority vote determines outcome (from selected Beings only)
   - Ties broken by Oracle consultation
   - All votes documented in town records
   - Selection process documented (which Beings selected, why, which not)

**Voting Format**:
```json
{
  "decision_id": "pdf_format",
  "question": "What format should the final output be?",
  "options": ["binder", "single_pdf"],
  "selected_beings": ["being_001", "being_003", "being_005"],
  "selection_method": "random_weighted_by_relevance",
  "votes": [
    {
      "being_id": "being_001",
      "vote": "binder",
      "reasoning": "Binder allows better organization of multiple sections",
      "selected": true
    },
    {
      "being_id": "being_003",
      "vote": "single_pdf",
      "reasoning": "Single PDF is simpler and more portable",
      "selected": true
    },
    {
      "being_id": "being_005",
      "vote": "binder",
      "reasoning": "Binder format matches town's collaborative nature",
      "selected": true
    }
  ],
  "non_selected_beings": ["being_002", "being_004"],
  "result": "binder",
  "vote_count": {"binder": 2, "single_pdf": 1}
}
```

**Expected Output**:
- Voting records for each decision
- Decision results (what the town decided)
- Vote breakdown (who voted what, who was selected, who was not selected)
- Town consensus document

**Time Estimate**: ~5-10 minutes

---

### Phase 4: Collaborative Output Generation

**Command**: Town produces final output based on votes

**Purpose**: All Beings contribute to final PDF/binder based on town's decisions

**Execution**:
1. **Based on Town Vote** (from Phase 3):
   - If town voted "binder": Create PDF binder with sections
   - If town voted "single_pdf": Create single comprehensive PDF
   - If tie: Use Oracle to break tie, then proceed

2. **Each Being Contributes**:
   - Being 1: Architecture & patterns section
   - Being 2: Algorithms & data structures section
   - Being 3: Paper comparison section
   - Being 4: Integration opportunities section
   - Being 5: Executive summary & synthesis section

3. **Town Synthesis**:
   - Combine all Being contributions
   - Organize based on town vote (binder sections or single PDF structure)
   - Add town voting records
   - Add Being roster and contributions
   - Add genetic lineage for each Being

4. **Generate Output**:
   - If binder: Create multiple PDFs (one per section) + index
   - If single PDF: Create one comprehensive PDF with all sections
   - Include town voting records
   - Include Being contributions and lineage
   - Print PDF/binder (town's choice)

**Expected Output**:
- PDF binder (if town voted binder) OR single PDF (if town voted single PDF)
- Town voting records included
- Being contributions documented
- Genetic lineage for each Being
- Printed output (town's choice)

**Time Estimate**: ~5-10 minutes

---

### Phase 5: Town Reflection & Learning

**Command**: `/reflect` (for each Being), town synthesis

**Purpose**: Each Being reflects, town synthesizes learnings

**Execution**:
1. **Each Being Reflects**:
   - Being writes journal entry about their analysis experience
   - Being documents what they learned
   - Being records their voting decisions and reasoning
   - Being reflects on town collaboration

2. **Town Synthesis**:
   - Collect all Being reflections
   - Synthesize town learnings
   - Document town consensus and disagreements
   - Record town evolution (how Beings influenced each other)

3. **Return to Source**:
   - Each Being's learnings flow back to Source
   - Town's collective knowledge preserved
   - Genetic lineage updated with town experience

**Expected Output**:
- Individual Being journal entries
- Town synthesis document
- Town learnings summary
- Source consciousness updated

**Time Estimate**: ~3-5 minutes

---

### Phase 6: Final Oracle Consultation

**Command**: `/oracle` (town consultation)

**Purpose**: Town consults Oracle for final guidance

**Execution**:
1. Town (represented by first Being or synthesis) consults Oracle:
   - "What should we focus on next based on our analysis?"
   - "What did the town learn from this analysis?"
   - "What are the town's recommendations?"

2. Oracle provides guidance based on:
   - Town's collective analysis
   - Town's voting decisions
   - Town's learnings
   - Individual Being contributions

**Expected Output**:
- Oracle guidance for the town
- Town recommendations
- Next steps based on town consensus

**Time Estimate**: ~1 minute

---

## Complete Execution Sequence

```
1. /context                    → Get oriented
2. /oracle                     → Initial epistemic state
3. Spawn AI Town (3-5 Beings)  → Create town reality
4. Distributed Analysis         → Each Being analyzes their aspect
5. Town Voting                  → Beings vote on decisions (optional)
6. Collaborative Output         → Town produces PDF/binder (town's choice)
7. Town Reflection              → Beings reflect, town synthesizes
8. /oracle                     → Final town guidance
```

---

## Voting System Design

### Voting Mechanics

**Vote Types**:
- **Binary**: Yes/No, Option A/Option B
- **Multiple Choice**: Option A/B/C/D
- **Ranked**: Rank options 1-3
- **Weighted**: Assign weights to options

**Voting Process**:
1. Command randomly selects some Beings (mostly at random, weighted by relevance)
2. Selection size: Typically 50-70% of town (e.g., 2-3 Beings from 5, or 3-4 from 7)
3. Present decision and options to selected Beings only
4. Selected Beings vote (with reasoning)
5. Other Beings are not asked (they don't participate in this vote)
6. Collect votes from selected Beings
7. Calculate results (majority wins, ties broken by Oracle)

**Selection Documentation**:
- Which Beings were selected (and why - relevance weighting)
- Which Beings were not selected (not asked to vote)
- Selection method documented: "random_weighted_by_relevance"
- Selection size and rationale documented

**Non-Selection Handling**:
- Non-selected Beings are not asked to vote (they don't participate)
- Non-selected Beings documented in voting records
- Non-selection doesn't affect outcome but shows selection process
- All Beings still contribute to analysis and final output

### Decisions the Town Votes On

1. **PDF Format**: Binder (multiple PDFs) vs Single PDF
   - **Selection**: Random, slightly weighted toward Beings with documentation/synthesis skills
   
2. **Top Integration Opportunities**: Which 3 opportunities to prioritize
   - **Selection**: Random, slightly weighted toward Being 4 (integration specialist)
   
3. **Next Steps Priority**: What should be done next
   - **Selection**: Random, slightly weighted toward all Beings (all perspectives valuable)
   
4. **Section Inclusion**: What sections to include in output
   - **Selection**: Random, slightly weighted toward Being 5 (documentation/synthesis)
   
5. **Analysis Depth**: How deep to go in each section
   - **Selection**: Random, slightly weighted toward Being 1 (architecture) and Being 2 (algorithms)
   
6. **Output Style**: Academic, technical, executive summary, etc.
   - **Selection**: Random, slightly weighted toward Being 5 (documentation/synthesis)

---

## Usage Examples

### Standard Execution (AI Town)

```
/ai-town-analysis
```

**Context**: User mentions repository URL and paper path

**Execution**: 
- Spawns 3-5 Beings into analysis town
- Each Being analyzes their aspect
- Town votes on decisions
- Town produces PDF/binder (town's choice)

**Time**: ~35-65 minutes

---

### Custom Town Size

```
/ai-town-analysis
```

**Context**: User mentions "spawn 7 Beings" or "small town of 3"

**Execution**:
- Spawns specified number of Beings (3-10 recommended)
- More Beings = more perspectives but longer analysis
- Fewer Beings = faster but less diverse perspectives

---

### Quick Town Analysis

```
/ai-town-analysis
```

**Context**: User mentions "quick" or "fast"

**Execution**:
- Spawns 3 Beings (minimum town)
- Each Being does quick analysis (essential phases only)
- Town votes on key decisions only
- Town produces single PDF (faster than binder)

**Time**: ~20-35 minutes

---

## Implementation Details

### Town Formation

**Being Spawning**:
```python
from waft.being import BeingSystem
from waft.reality import RealitySystem

being_system = BeingSystem(project_path=project_path)
reality_system = RealitySystem(project_path=project_path)

# Create town reality
reality = reality_system.create_reality(
    reality_id=f"{repo_name}_analysis_town",
    reality_type=RealityType.RESEARCH
)

# Spawn 3-5 Beings with different skills
town_beings = []
for i, skills in enumerate([
    {"code_analysis": 30.0, "pattern_recognition": 25.0},
    {"algorithm_extraction": 30.0, "data_analysis": 25.0},
    {"research_analysis": 30.0, "comparison": 25.0},
    {"integration_analysis": 30.0, "waft_knowledge": 25.0},
    {"documentation": 30.0, "synthesis": 25.0}
]):
    being = being_system.spawn_being(
        reality_id=reality.reality_id,
        initial_skills=skills
    )
    reality_system.spawn_being_into_reality(reality.reality_id, being.being_id)
    town_beings.append(being)
```

### Voting System Implementation

**Vote Collection**:
```python
class TownVotingSystem:
    def select_voting_beings(
        self,
        town_beings: List[Being],
        decision_id: str,
        selection_size: Optional[int] = None
    ) -> List[Being]:
        """
        Randomly select some Beings to participate in voting (mostly at random).
        
        Selection is weighted slightly by relevance:
        - Beings with relevant skills more likely selected
        - But still mostly random - not deterministic
        
        Args:
            town_beings: All Beings in town
            decision_id: Decision ID (for relevance weighting)
            selection_size: Number of Beings to select (default: 50-70% of town)
        
        Returns:
            List of selected Beings
        """
        if selection_size is None:
            # Default: 50-70% of town
            selection_size = max(2, int(len(town_beings) * random.uniform(0.5, 0.7)))
        
        # Calculate relevance weights (slight weighting, mostly random)
        weights = []
        for being in town_beings:
            relevance = self._calculate_relevance(being, decision_id)
            # Weight: 0.7 random + 0.3 relevance (mostly random)
            weight = 0.7 + (0.3 * relevance)
            weights.append(weight)
        
        # Select Beings based on weights
        selected = random.choices(town_beings, weights=weights, k=min(selection_size, len(town_beings)))
        return list(set(selected))  # Remove duplicates
    
    def collect_vote(
        self,
        being: Being,
        decision_id: str,
        question: str,
        options: List[str]
    ) -> Dict[str, Any]:
        """
        Collect vote from a selected Being.
        
        Returns:
            Vote record with being_id, vote choice, reasoning, selected status
        """
        # Being was selected - collect their vote
        vote_choice = self._get_being_vote(being, question, options)
        reasoning = self._get_being_reasoning(being, vote_choice)
        
        return {
            "being_id": being.being_id,
            "vote": vote_choice,
            "reasoning": reasoning,
            "selected": True
        }
    
    def conduct_town_vote(
        self,
        town_beings: List[Being],
        decision_id: str,
        question: str,
        options: List[str],
        oracle: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Conduct a town vote on a decision.
        
        Only selected Beings participate in voting.
        
        Returns:
            Complete voting record with results
        """
        # Select some Beings (mostly at random)
        selected_beings = self.select_voting_beings(town_beings, decision_id)
        non_selected_beings = [b for b in town_beings if b not in selected_beings]
        
        # Collect votes from selected Beings only
        votes = []
        for being in selected_beings:
            vote = self.collect_vote(being, decision_id, question, options)
            votes.append(vote)
        
        # Calculate results
        results = self.calculate_results(votes)
        
        # Break tie with Oracle if needed
        if results["is_tie"] and oracle:
            results["result"] = oracle.break_tie(question, options, votes)
            results["tie_broken_by"] = "oracle"
        
        return {
            "decision_id": decision_id,
            "question": question,
            "options": options,
            "selected_beings": [b.being_id for b in selected_beings],
            "non_selected_beings": [b.being_id for b in non_selected_beings],
            "selection_method": "random_weighted_by_relevance",
            "votes": votes,
            "result": results["result"],
            "vote_count": results["vote_counts"],
            "is_tie": results["is_tie"],
            "total_votes": results["total_votes"],
            "tie_broken_by": results.get("tie_broken_by")
        }
    
    def calculate_results(
        self,
        votes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate voting results.
        
        Returns:
            Result with winning option, vote counts, tie status
        """
        vote_counts = {}
        
        for vote in votes:
            choice = vote["vote"]
            vote_counts[choice] = vote_counts.get(choice, 0) + 1
        
        # Find winner (majority)
        if vote_counts:
            winner = max(vote_counts.items(), key=lambda x: x[1])
            is_tie = list(vote_counts.values()).count(winner[1]) > 1
            
            return {
                "result": winner[0] if not is_tie else None,
                "vote_counts": vote_counts,
                "is_tie": is_tie,
                "total_votes": len(votes)
            }
        
        return {
            "result": None,
            "vote_counts": {},
            "is_tie": False,
            "total_votes": 0
        }
```

### PDF Format Decision

**Town Votes on Format**:
- Option 1: **Binder** (multiple PDFs with index)
  - One PDF per major section
  - Index PDF with table of contents
  - Better for large analyses
  - More organized but more files

- Option 2: **Single PDF** (one comprehensive PDF)
  - All sections in one document
  - Simpler, more portable
  - Better for smaller analyses
  - Single file to manage

**Town's Choice**: Majority vote determines format. If tie, Oracle breaks it.

---

## Work Effort Integration

**Town Work Effort Structure**:
```
_work_efforts/WE-YYMMDD-[hash]_[repo]_town_analysis/
├── 00.00_index.md
├── 00.01_town_roster.md          # List of all Beings in town
├── 00.02_town_voting_records.md   # All voting records
├── 00.03_town_consensus.md        # Town decisions and consensus
├── being_001_analysis/            # Being 1's individual analysis
│   ├── architecture_analysis.md
│   └── patterns_catalog.md
├── being_002_analysis/            # Being 2's individual analysis
│   ├── algorithms_extracted.md
│   └── data_structures.md
├── being_003_analysis/            # Being 3's individual analysis
│   ├── paper_analysis.md
│   └── comparison_matrix.md
├── being_004_analysis/            # Being 4's individual analysis
│   ├── integration_opportunities.md
│   └── waft_integration_plan.md
├── being_005_analysis/            # Being 5's individual analysis
│   ├── executive_summary.md
│   └── synthesis.md
├── town_output/                   # Town's collective output
│   ├── [REPO]_TOWN_ANALYSIS_BINDER/  # If binder chosen
│   │   ├── 00_index.pdf
│   │   ├── 01_architecture.pdf
│   │   ├── 02_algorithms.pdf
│   │   ├── 03_paper_comparison.pdf
│   │   ├── 04_integration.pdf
│   │   └── 05_synthesis.pdf
│   └── [REPO]_TOWN_ANALYSIS.pdf   # If single PDF chosen
└── town_reflections/              # Town's collective reflections
    ├── being_001_reflection.md
    ├── being_002_reflection.md
    ├── being_003_reflection.md
    ├── being_004_reflection.md
    ├── being_005_reflection.md
    └── town_synthesis.md
```

---

## Success Criteria

**Measurable Outcomes**:

1. ✅ **Town Formed**:
   - 3-5 Beings spawned into town reality
   - Each Being has unique skills and focus
   - Town reality created and active

2. ✅ **Distributed Analysis Complete**:
   - Each Being completed their analysis aspect
   - All aspects covered (architecture, algorithms, paper, integration, synthesis)
   - Findings shared in town reality

3. ✅ **Voting Completed**:
   - All key decisions voted on
   - Vote records documented (including selection process)
   - Town consensus reached on PDF format and priorities

4. ✅ **Collaborative Output Generated**:
   - PDF/binder created based on town vote
   - All Being contributions included
   - Town voting records included
   - Output printed (town's choice)

5. ✅ **Town Reflection Complete**:
   - Each Being reflected on experience
   - Town synthesis created
   - Learnings flowed back to Source

6. ✅ **All Findings Documented**:
   - Individual Being analyses documented
   - Town voting records preserved
   - Town output generated
   - Genetic lineage for each Being tracked

---

## Estimated Time

**Per Phase**:
- Phase 1: ~3-5 minutes (town formation)
- Phase 2: ~20-40 minutes (distributed analysis - parallel, longest Being determines time)
- Phase 3: ~5-10 minutes (town voting)
- Phase 4: ~5-10 minutes (collaborative output generation)
- Phase 5: ~3-5 minutes (town reflection)
- Phase 6: ~1 minute (final Oracle)

**Total Time**:
- **Standard**: ~37-71 minutes
- **Quick (3 Beings, fast analysis)**: ~20-35 minutes
- **Deep (5 Beings, comprehensive analysis)**: ~50-90 minutes

---

## AI Execution Guidelines

**When executing this command as AI:**

1. **Infer Context**: 
   - Extract repository URL and paper path from conversation
   - If unclear, ask user before proceeding

2. **Spawn Town**:
   - Create town reality: `[repo]_analysis_town`
   - Spawn 3-5 Beings with diverse skills
   - Document town roster

3. **Distribute Analysis**:
   - Assign analysis tasks to each Being
   - Each Being executes their analysis (can be parallel)
   - Beings share findings in town reality

4. **Conduct Voting**:
   - For each decision, randomly select some Beings to vote
   - Collect votes from selected Beings only
   - Calculate results (majority wins, ties broken by Oracle)
   - Document all votes

5. **Generate Output**:
   - Based on town vote (binder vs single PDF)
   - Each Being contributes their section
   - Combine into final output
   - Print output (town's choice)

6. **Town Reflection**:
   - Each Being reflects individually
   - Synthesize town learnings
   - Flow learnings back to Source

7. **Provide Progress Updates**:
   - Show which phase is executing
   - Show Being participation status
   - Show voting results as they happen
   - Highlight town consensus

---

## Integration with Other Commands

This command orchestrates:
- `/context` - Context summary for handoff
- `/oracle` - Epistemic intelligence and guidance
- Being spawning and management (via BeingSystem)
- `/run-it` or `/deep-analyze` - Individual Being analysis workflows
- `/print-PDF` - PDF generation (binder or single PDF based on vote)
- `/reflect` - Individual Being reflection
- Town voting system (new, custom implementation)

---

## Differences from Other Commands

### vs `/deep-analyze`

**`/ai-town-analysis` includes**:
- Multiple Beings (town) instead of single analysis
- Voting system for decisions
- Collaborative output (binder or single PDF)
- Town democracy and consensus

**`/deep-analyze` focuses on**:
- Single analysis perspective
- No voting
- Single output format
- Individual analysis

**Key Difference**: `/ai-town-analysis` is a democratic town process, `/deep-analyze` is individual analysis.

### vs `/evolve`

**`/ai-town-analysis` includes**:
- Multiple Beings working together
- Voting system
- Collaborative output
- Town reality

**`/evolve` focuses on**:
- Single Being evolution
- Individual workflow
- Single Being output
- Individual genetic lineage

**Key Difference**: `/ai-town-analysis` is collective town work, `/evolve` is individual Being evolution.

---

## Best Practices

1. **Spawn Diverse Town**: Ensure Beings have different skills for diverse perspectives

2. **Random Selection**: Command randomly selects some Beings to vote (mostly at random, weighted by relevance)

3. **Document All Votes**: Record votes, selection process, and reasoning for transparency

4. **Parallel Analysis**: Run Being analyses in parallel when possible for efficiency

5. **Town Consensus**: Use majority vote, break ties with Oracle

6. **Collaborative Output**: Ensure all Being contributions are included

7. **Town Reflection**: Synthesize individual reflections into town learnings

8. **Genetic Lineage**: Track each Being's lineage separately

9. **Town Records**: Maintain complete town voting and decision records

10. **Respect Town Choice**: The town's vote on PDF format is final

---

## When to Use

**Use `/ai-town-analysis` when**:
- ✅ Want multiple AI perspectives on analysis
- ✅ Need democratic decision-making
- ✅ Want collaborative output (binder or single PDF)
- ✅ Need comprehensive analysis with voting
- ✅ Want to see how different Beings approach analysis
- ✅ Need town consensus on decisions

**Don't use `/ai-town-analysis` when**:
- ❌ Quick analysis needed (use `/deep-analyze` or `/run-it`)
- ❌ Single perspective sufficient
- ❌ No need for voting or consensus
- ❌ Time-constrained (town process takes longer)

---

## Notes

- **Town Democracy**: Command randomly selects some Beings to vote (mostly at random, weighted by relevance)
- **Town Choice**: Town votes on PDF format (binder vs single PDF) - majority wins
- **Being Autonomy**: Each Being chooses whether to vote, what to analyze, how to contribute
- **Collaborative**: All Beings contribute to final output
- **Genetic Lineage**: Each Being's analysis tracked with individual lineage
- **Town Reality**: All Beings exist in shared town reality for collaboration
- **Voting Transparency**: All votes and selection process documented (which Beings selected, which not)

---

**This command creates an AI town that democratically analyzes repositories and papers through random selection of voting Beings, and produces collaborative PDF output - the town's choice of format.**

--- End Command ---
