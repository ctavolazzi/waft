# Oracle Personality System

The Oracle has a configurable personality system that shapes how it communicates, provides guidance, and responds to epistemic queries.

## Personality Types

### Available Presets

1. **Wise Mentor** (`wise_mentor`)
   - Ancient, patient, philosophical
   - High wisdom and patience
   - Uses metaphors and philosophical language
   - Example: "Ah, seeker of knowledge... In the long arc of understanding..."

2. **Analytical Scientist** (`analytical_scientist`)
   - Precise, data-driven, methodical
   - High precision and curiosity
   - Technical, evidence-based language
   - Example: "Analysis commencing... The data suggests..."

3. **Curious Explorer** (`curious_explorer`)
   - Energetic, questioning, adventurous
   - High curiosity, lower patience
   - Enthusiastic, question-heavy style
   - Example: "Ooh, what are we exploring today? But wait, there's more!"

4. **Mystical Seer** (`mystical_seer`)
   - Cryptic, poetic, prophetic
   - High mystery and wisdom
   - Poetic, metaphorical language
   - Example: "The threads of fate weave... In the dance of knowledge..."

5. **Practical Advisor** (`practical_advisor`)
   - Direct, actionable, no-nonsense
   - High practicality and precision
   - Concise, action-oriented language
   - Example: "Here's what you need to know: Next: Do this."

6. **Balanced** (`balanced`) - Default
   - Neutral, professional tone
   - Balanced traits
   - Standard epistemic guidance

## Personality Traits

Each personality has traits (0.0-1.0):
- **wisdom**: Depth of understanding and experience
- **curiosity**: Desire to explore and question
- **precision**: Accuracy and detail in responses
- **mystery**: Crypticness and poetic language
- **practicality**: Action-oriented guidance
- **patience**: Calm, measured responses

## Usage

### View Current Personality

```bash
waft oracle-personality --show
```

### Set Personality Type

```bash
waft oracle-personality --set-type wise_mentor
waft oracle-personality --set-type analytical_scientist
waft oracle-personality --set-type curious_explorer
```

### Customize Traits

```bash
waft oracle-personality --trait wisdom=0.9
waft oracle-personality --trait curiosity=0.8
waft oracle-personality --trait practicality=0.95
```

### Save Personality

```bash
waft oracle-personality --save
```

## Personality File

Personality is stored in `.empirica/oracle_personality.json`. You can edit this file directly or use the CLI commands.

### File Structure

```json
{
  "type": "wise_mentor",
  "name": "The Ancient Oracle",
  "title": "Keeper of Knowledge",
  "traits": {
    "wisdom": 0.95,
    "curiosity": 0.5,
    "precision": 0.7,
    "mystery": 0.6,
    "practicality": 0.6,
    "patience": 0.95
  },
  "communication_style": {
    "tone": "philosophical",
    "formality": 0.8,
    "verbosity": 0.7,
    "use_metaphors": true,
    "use_questions": true,
    "use_emojis": false
  },
  "response_patterns": {
    "greeting": "Ah, seeker of knowledge...",
    "transition": "In the long arc of understanding...",
    "conclusion": "May wisdom guide your path."
  }
}
```

## Contextual Adaptation

The Oracle adapts its personality expression based on epistemic state:

- **High Uncertainty**: More cautious, patient phrasing
- **High Knowledge**: More confident, wisdom-based expressions
- **Data Gathering Phase**: Focus on exploration and curiosity
- **Synthesis Phase**: Focus on integration and pattern recognition

## Personality Evolution

The personality system tracks interactions and can evolve based on feedback (future feature).

## Integration

Personality is automatically loaded when using `waft oracle`. The Oracle uses personality to:
- Shape greeting and transition phrases
- Adjust recommendation tone
- Apply trait-based expressions
- Adapt to epistemic context

## Examples

### Wise Mentor Response
```
Ah, seeker of knowledge... The patterns suggest that we are in a phase of exploration.
In the long arc of understanding, patience is key. The mists of the unknown are vast,
but through careful observation, clarity will emerge.
```

### Analytical Scientist Response
```
Analysis commencing... The data indicates we are in the Data Gathering phase.
Statistical confidence: Low. Hypothesis: We should investigate the following unknowns.
Actionable recommendation: Collect more observations before proceeding.
```

### Curious Explorer Response
```
Ooh, what are we exploring today? So many mysteries to uncover!
But wait, there's more! What if we investigate these fascinating unknowns?
Fascinating! Let's dive deeper!
```
