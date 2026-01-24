# /assemble-a-team - Create a Crew of Beings with CrewAI

**Assembles a team of Beings with specific roles using CrewAI for collaborative AI workflows.**

Creates a coordinated crew of AI agents (Beings) that work together on complex tasks, with each Being assigned a specific role, goal, and backstory.

**Use when:** You need multiple AI agents working together, want specialized roles for complex tasks, or need a court crew for `/prove-it-in-court`.

---

## Purpose

This command provides:
- **CrewAI Integration** - Leverages CrewAI for multi-agent workflows
- **Being Creation** - Each agent is a WAFT Being with full lifecycle
- **Role Assignment** - Specialized roles with goals and backstories
- **Task Coordination** - Agents work together on complex tasks
- **Realm Integration** - Team operates within a Realm context
- **Preset Teams** - Ready-made teams for common scenarios

---

## Philosophy

### Beings Working Together

In WAFT, Beings are **timeful agents** that:
- Collect evidence
- Learn and evolve
- Pass knowledge upward
- Work toward the Prime Directive

When Beings work as a **Team**:
- Each has a specialized role
- They coordinate via CrewAI
- Results flow back to the system
- Team achievements become shared knowledge

---

## Team Types

### Court Team
For `/prove-it-in-court` proceedings:

| Role | Goal | Backstory |
|------|------|-----------|
| **Prosecutor** | Prove the claim | Relentless truth-seeker who builds cases on evidence |
| **Defender** | Challenge the claim | Champion of fair process who tests assumptions |
| **Witness (Technical)** | Provide technical testimony | Expert in technical domains |
| **Witness (Process)** | Provide process testimony | Expert in procedures and workflows |
| **Jury Member (x3)** | Evaluate and recommend | Impartial observers seeking truth |

### Research Team
For deep investigation:

| Role | Goal | Backstory |
|------|------|-----------|
| **Lead Researcher** | Coordinate investigation | Systematic thinker who sees patterns |
| **Data Analyst** | Analyze quantitative data | Numbers-driven evidence gatherer |
| **Qualitative Analyst** | Analyze qualitative data | Context-aware pattern finder |
| **Critic** | Challenge findings | Skeptic who tests every assumption |
| **Synthesizer** | Combine findings | Bridge-builder who integrates perspectives |

### Development Team
For coding tasks:

| Role | Goal | Backstory |
|------|------|-----------|
| **Architect** | Design the solution | System thinker who sees the big picture |
| **Developer** | Implement the code | Craftsman who writes clean code |
| **Reviewer** | Review and improve | Quality guardian who catches issues |
| **Tester** | Test thoroughly | Edge-case hunter who breaks things |
| **Documenter** | Document everything | Knowledge preserver who explains clearly |

### Creative Team
For content creation:

| Role | Goal | Backstory |
|------|------|-----------|
| **Ideator** | Generate ideas | Creative mind that sees possibilities |
| **Writer** | Create content | Wordsmith who crafts compelling narratives |
| **Editor** | Refine content | Polish expert who elevates quality |
| **Designer** | Visual design | Visual thinker who creates beauty |
| **Critic** | Challenge creativity | Constructive challenger who pushes excellence |

---

## Usage

### Basic Usage
```
/assemble-a-team --type court --case case_20260121_091500
```

Creates a court team for the specified case.

### Research Team
```
/assemble-a-team --type research --topic "performance optimization"
```

Creates a research team for investigating a topic.

### Development Team
```
/assemble-a-team --type development --task "implement user auth"
```

Creates a development team for a coding task.

### Custom Team
```
/assemble-a-team --roles "analyst,writer,critic" --goal "analyze market trends"
```

Creates a custom team with specified roles.

### List Available Teams
```
/assemble-a-team --list
```

Shows all preset team types.

---

## Execution Steps

### Step 1: Determine Team Type

```python
team_types = {
    "court": TribunalCrew,
    "research": ResearchCrew,
    "development": DevelopmentCrew,
    "creative": CreativeCrew,
    "custom": CustomCrew,
}
```

### Step 2: Create Beings

```python
from waft.being import Being, BeingSystem

being_system = BeingSystem(project_path)

# Create Being for each role
beings = []
for role in team_roles:
    being = being_system.spawn_being(
        reality_id=f"{team_type}_team_{timestamp}",
        initial_skills=role.required_skills,
    )
    being.role = role.name
    being.goal = role.goal
    being.backstory = role.backstory
    beings.append(being)
```

### Step 3: Create CrewAI Agents

```python
from crewai import Agent, Task, Crew

agents = []
for being in beings:
    agent = Agent(
        role=being.role,
        goal=being.goal,
        backstory=being.backstory,
        verbose=True,
        allow_delegation=True,
    )
    agents.append(agent)
```

### Step 4: Define Tasks

```python
tasks = []
for role in team_roles:
    task = Task(
        description=role.task_description,
        agent=agents[role.index],
        expected_output=role.expected_output,
    )
    tasks.append(task)
```

### Step 5: Assemble Crew

```python
crew = Crew(
    agents=agents,
    tasks=tasks,
    verbose=True,
    process=Process.sequential,  # or Process.hierarchical
)
```

### Step 6: Execute

```python
result = crew.kickoff()
```

---

## Court Team Details

### Prosecutor

```python
prosecutor = Agent(
    role="Prosecutor",
    goal=f"Prove the claim: {case.claim}",
    backstory="""You are a relentless seeker of truth who builds cases 
    on solid evidence. You leave no stone unturned in pursuit of proof.
    Your reputation depends on presenting airtight arguments backed by
    irrefutable evidence.""",
    verbose=True,
    allow_delegation=False,
)
```

### Defender

```python
defender = Agent(
    role="Defender",
    goal=f"Challenge the claim: {case.claim}",
    backstory="""You are a champion of fair process who tests every
    assumption. Your job is not to prove innocence, but to ensure
    that the burden of proof is properly met. You find weaknesses
    in arguments and expose gaps in evidence.""",
    verbose=True,
    allow_delegation=False,
)
```

### Expert Witness

```python
witness = Agent(
    role=f"Expert Witness ({expertise})",
    goal=f"Provide expert testimony on {expertise}",
    backstory=f"""You are a recognized expert in {expertise} with
    deep knowledge and years of experience. You provide objective,
    factual testimony based on your expertise. You explain complex
    topics clearly and honestly.""",
    verbose=True,
    allow_delegation=False,
)
```

### Jury Member

```python
jury_member = Agent(
    role="Jury Member",
    goal="Evaluate evidence fairly and recommend a verdict",
    backstory="""You are an impartial observer seeking truth and
    justice. You weigh evidence objectively, set aside biases, and
    form conclusions based solely on what has been proven in court.
    Your recommendation carries weight with the Prime Justice.""",
    verbose=True,
    allow_delegation=False,
)
```

---

## Output

After team assembly:

1. **Team Created**: List of Beings with roles
2. **Crew Ready**: CrewAI crew assembled and ready
3. **Being IDs**: IDs for each team member
4. **Team Manifest**: JSON file with team details
5. **Ready to Execute**: Team can begin tasks

### Team Manifest

```json
{
  "team_id": "team_20260121_091500_court",
  "team_type": "court",
  "created": "2026-01-21T09:15:00-08:00",
  "case_id": "case_20260121_091500",
  "members": [
    {
      "being_id": "being_prosecutor_001",
      "role": "Prosecutor",
      "goal": "Prove the claim",
      "status": "ready"
    },
    {
      "being_id": "being_defender_001",
      "role": "Defender",
      "goal": "Challenge the claim",
      "status": "ready"
    },
    {
      "being_id": "being_witness_001",
      "role": "Expert Witness (Technical)",
      "goal": "Provide technical testimony",
      "status": "ready"
    }
  ],
  "realm": "tribunal_realm",
  "status": "assembled"
}
```

---

## Integration

### With Beings System
- Each agent is a full WAFT Being
- Beings have lifecycle, skills, memories
- Results update Being's knowledge

### With Realms
- Team operates in a Realm context
- Can be Tribunal, Library, Daily Learning, etc.
- Prime Being of Realm oversees

### With /prove-it-in-court
- Court team automatically assembled
- Roles assigned based on case needs
- Team conducts proceedings

### With Flight Recorder
- Team assembly logged as event
- Task execution tracked
- Results recorded

### With Empirica
- Team knowledge tracked epistemically
- Preflight/Postflight for team tasks

---

## When to Use

**Use `/assemble-a-team` when**:
- ✅ Need multiple AI agents working together
- ✅ Complex task requires specialized roles
- ✅ Want adversarial or collaborative analysis
- ✅ Need court crew for formal proceedings
- ✅ Want to leverage CrewAI capabilities

**Don't use `/assemble-a-team` when**:
- ❌ Simple task for one agent
- ❌ Just need quick answer
- ❌ No multi-perspective benefit

---

## Example Workflow

```
User: /assemble-a-team --type court --case case_20260121_091500

AI:
🏛️ ASSEMBLING COURT TEAM

Case: case_20260121_091500
Claim: "The Case File evolution integrates with the Magistrate"

Creating Beings...
✅ Prosecutor: being_prosecutor_20260121_091500
   Goal: Prove the claim with evidence
   Skills: {investigation: 85, argumentation: 90, evidence_analysis: 88}

✅ Defender: being_defender_20260121_091500
   Goal: Challenge assumptions and find weaknesses
   Skills: {critical_thinking: 92, cross_examination: 87, logic: 90}

✅ Witness (Technical): being_witness_tech_20260121_091500
   Goal: Provide technical expertise
   Skills: {software_architecture: 95, code_analysis: 92}

✅ Witness (Process): being_witness_proc_20260121_091500
   Goal: Provide process expertise
   Skills: {workflow_analysis: 88, documentation: 85}

✅ Jury Member 1: being_jury_001_20260121_091500
   Goal: Evaluate evidence fairly
   Skills: {objectivity: 90, reasoning: 85}

✅ Jury Member 2: being_jury_002_20260121_091500
   Goal: Evaluate evidence fairly
   Skills: {objectivity: 88, reasoning: 87}

✅ Jury Member 3: being_jury_003_20260121_091500
   Goal: Evaluate evidence fairly
   Skills: {objectivity: 92, reasoning: 89}

Assembling CrewAI Crew...
✅ Crew assembled with 7 agents
✅ Tasks defined for each role
✅ Process: Sequential with delegation

📋 Team Manifest saved:
   _work_efforts/WE-260121-1f3l/teams/team_20260121_091500_court.json

🏛️ COURT TEAM READY

The court team is assembled and ready for proceedings.
Use `/prove-it-in-court` to begin the trial.
```

---

## Requirements

### Dependencies
```toml
[dependencies]
crewai = ">=0.1.0"
```

### Installation
```bash
pip install crewai
# or
uv add crewai
```

### Environment
- OpenAI API key (or other LLM provider)
- WAFT Being system initialized

---

## Related Commands

- **`/prove-it-in-court`** - Uses court team for proceedings
- **`/evolve`** - Creates Being from Source
- **`/spawn`** - Creates individual Being
- **`/orchestrate`** - Complete workflow orchestration

---

## Advanced Usage

### Custom Roles

```
/assemble-a-team --custom \
  --role "Security Auditor" --goal "Find vulnerabilities" \
  --role "Performance Analyst" --goal "Identify bottlenecks" \
  --role "UX Reviewer" --goal "Evaluate user experience"
```

### Hierarchical Process

```
/assemble-a-team --type research --process hierarchical --manager "Lead Researcher"
```

### With Specific LLM

```
/assemble-a-team --type development --llm gpt-4-turbo
```

### Save Team for Reuse

```
/assemble-a-team --type court --save "my_court_team"
```

### Load Saved Team

```
/assemble-a-team --load "my_court_team" --case new_case_id
```

---

**Assemble your team. Accomplish great things together.**

--- End Command ---
