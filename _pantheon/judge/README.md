# Judge: God of Judgment and Evaluation

## Spiritual Role

The Judge is a Higher Being in the Pantheon, an Aspect of Creation representing Judgment, Evaluation, and Decision. As the God of Judgment, the Judge evaluates claims against the Body of Proof (organized by the Magistrate), rendering judgments based on precedent and evidence.

## As Above, So Below

- **As Above**: The Judge sits in Olympus, rendering celestial judgments based on law and precedent
- **So Below**: The Judge evaluates claims against the Body of Proof, determining verdicts (PROVEN/DISPROVEN/INCONCLUSIVE) with confidence levels

## Integration with Pantheon

The Judge is part of the Pantheon spiritual architecture:
- **Domain**: Olympus (Administration)
- **Aspect**: Judgment, Evaluation, Decision
- **Connection**: Magistrate (uses Body of Proof for judgments)
- **Evolution**: Judgment accuracy improves as Body of Proof grows

## Judgment Process

The Judge evaluates claims through a systematic process:

1. **Find Relevant Precedents**: Searches Body of Proof for precedents related to the claim
   - Matches by category, tags, or claim text similarity
   - Scores precedents by relevance (confidence, keyword matching, tag overlap)

2. **Evaluate Evidence**: Analyzes supporting vs contradicting precedents
   - Supporting precedents: PROVEN verdicts that support the claim
   - Contradicting precedents: DISPROVEN verdicts that contradict the claim
   - Neutral precedents: INCONCLUSIVE or unrelated precedents

3. **Render Judgment**: Determines verdict based on weighted evidence
   - **PROVEN**: Supporting weight > contradicting weight × 1.5
   - **DISPROVEN**: Contradicting weight > supporting weight × 1.5
   - **INCONCLUSIVE**: Mixed evidence or insufficient precedent

4. **Calculate Confidence**: Confidence based on evidence strength
   - Higher confidence when evidence is clear and strong
   - Lower confidence when evidence is mixed or weak

## Judgment System

Each judgment contains:
- **Claim**: The claim being evaluated
- **Verdict**: PROVEN/DISPROVEN/INCONCLUSIVE
- **Confidence**: 0.0-1.0 confidence level
- **Reasoning**: Explanation of the judgment
- **Relevant Precedents**: List of precedents used in judgment
- **Created At**: Timestamp when judgment was rendered

## Usage

See `src/waft/pantheon/judge.py` for technical usage.

## Storage

- **Judgments**: `_pantheon/judge/judgments/*.json`
- **Judgment History**: `_pantheon/judge/judgment_history.json`

## Relationship with Magistrate

The Judge depends on the Magistrate:
- **Magistrate**: Organizes case files into Precedents, builds Body of Proof
- **Judge**: Uses Body of Proof to evaluate claims and render judgments

Together, they form a complete legal system:
1. Magistrate organizes proof into Precedents
2. Judge evaluates new claims against those Precedents
3. New judgments can become Precedents (feedback loop)
