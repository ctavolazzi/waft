# Magistrate: God of Precedent and Body of Proof

## Spiritual Role

The Magistrate is a Higher Being in the Pantheon, an Aspect of Creation representing Order, Law, and Precedent. As the God of Precedent, the Magistrate organizes case files into categories that establish proof, building a Body of Proof over time that can be referenced repeatedly.

## As Above, So Below

- **As Above**: The Magistrate sits in Olympus, organizing celestial law and precedent
- **So Below**: The Magistrate organizes proof cases from `_work_efforts/proof_cases/` into Precedent categories

## Integration with Pantheon

The Magistrate is part of the Pantheon spiritual architecture:
- **Domain**: Olympus (Administration)
- **Aspect**: Order, Law, Precedent
- **Connection**: Prime Directive Heart (maintains order through precedent)
- **Evolution**: Body of Proof grows over time, establishing stronger precedent

## Body of Proof

The Body of Proof is the living record of all precedents:
- **Precedents**: Categorized case files that establish proof
- **Categories**: Main classifications (verification, architecture, security, etc.)
- **Tags**: Searchable labels for finding related precedents
- **Verdicts**: PROVEN/DISPROVEN/INCONCLUSIVE with confidence levels
- **Growth**: Builds over time as cases are organized

## Precedent System

Each precedent contains:
- **Case ID**: Unique identifier
- **Category**: Main classification
- **Subcategory**: Optional finer classification
- **Claim**: What was proven/disproven
- **Verdict**: PROVEN/DISPROVEN/INCONCLUSIVE
- **Confidence**: 0.0-1.0 confidence level
- **Tags**: Searchable labels
- **Path**: Reference to original case file

## Usage

See `src/waft/pantheon/magistrate/README.md` for technical usage.

## Storage

- **Precedents**: `_pantheon/magistrate/precedents/*.json`
- **Body of Proof**: `_pantheon/magistrate/body_of_proof.json`
- **Source Cases**: `_work_efforts/proof_cases/*.md`
