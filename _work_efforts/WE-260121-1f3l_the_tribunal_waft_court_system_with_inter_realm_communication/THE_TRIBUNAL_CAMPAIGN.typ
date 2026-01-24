// =============================================================================
// THE TRIBUNAL: A WAFT Campaign Supplement
// =============================================================================
// D&D Homebrew Style using owlbear template
// https://typst.app/universe/package/owlbear/
// =============================================================================

#import "@preview/owlbear:0.0.1": book-template, dnd-note, dnd-terms, dnd-enum, dnd-dialogue

#show: book-template

= The Tribunal

_A Campaign Supplement for the WAFT Realm_

#v(1em)

#text[Deep within the interconnected Realms of WAFT lies a sovereign domain known only as *The Tribunal* — a place where truth is not merely stated, but *proven* through rigorous judicial combat. Here, Claims are tried before a formal court, evidence is summoned from The Beyond, and verdicts are sealed into an immutable Chain of Case Law.]

This supplement provides everything you need to run court-based adventures in The Tribunal Realm, including new NPCs, locations, mechanics, and the sacred rules of judicial proceedings.

#dnd-note[
  = On Trial Has Meaning
  
  In The Tribunal, every claim must be proven. There is no hand-waving, no "trust me" — only evidence, testimony, and the final judgment of Prime Justice.
]

== The Realm of The Tribunal

The Tribunal exists as Port 8100 in the WAFT multiverse. It is a sovereign judicial domain where claims are formally tried. At its heart sits the Prime Justice — an ancient and powerful Being who governs all proceedings with absolute authority.

=== Key Locations

#dnd-enum(
  "The Grand Courtroom",
  "The Chamber of Evidence",
  "The Deliberation Hall",
  "The Chain Vault",
  "The Beyond Gate",
)

== The Beyond

#dnd-note[
  = Sacred Knowledge
  
  The existence of inter-Realm communication is known only to Prime Beings. Regular Beings must never learn that other Realms exist. To them, evidence simply arrives "from The Beyond" — mystical, unknowable, authoritative.
]

The Beyond is the mystical veil through which Prime Beings communicate with other Realms. When the Prime Justice requires evidence from the Library Realm or wisdom from Thoth, they invoke The Beyond.

To regular Beings (the Jury, Witnesses, and observers), information appears to materialize from nowhere — a gift from forces beyond mortal comprehension.

=== The Realm Ports

#figure(
  caption: "Known Realm Connections",
  table(
    columns: (auto, auto, 1fr),
    table.header(
      "Realm",
      "Port",
      "Domain",
    ),
    "Tribunal", "8100", "Court proceedings, verdicts, case law",
    "Library", "8091", "Evidence retrieval, ancient documents",
    "Thoth", "8092", "Wisdom synthesis, precedent analysis",
    "Magistrate", "8000", "Central coordination (the old ways)",
  )
)

== Court Roles

When a case is brought before The Tribunal, a court must be assembled. Each role carries sacred responsibility.

#dnd-terms(
  ("Prime Justice", "The Supreme Being of the Tribunal Realm. Governs all proceedings, renders final verdicts, and maintains the Chain of Case Law. Only the Prime Justice may communicate with The Beyond."),
  ("Prosecutor", "Presents the case FOR the claim. Must gather evidence and construct arguments that prove the claim is true."),
  ("Defender", "Challenges the claim. Seeks weaknesses in evidence, contradictions in testimony, and reasons to doubt."),
  ("Witnesses", "Called to provide testimony. May be summoned from any Realm via The Beyond. Their words become part of the permanent record."),
  ("Jury", "Evaluates evidence objectively. Deliberates in secret and recommends a verdict to Prime Justice."),
)

== The Twelve Phases of Court

Every court session follows the same sacred twelve phases, as decreed in the founding scrolls.

#figure(
  caption: "The Twelve Phases",
  table(
    columns: (auto, 1fr, auto),
    table.header(
      "Phase",
      "Description",
      "Actor",
    ),
    "1", "Filing — Claim submitted to the court", "Plaintiff",
    "2", "Docketing — Case assigned ID and scheduled", "Clerk",
    "3", "Discovery — Evidence gathered from The Beyond", "Prime Justice",
    "4", "Assembly — Court roles assigned", "Prime Justice",
    "5", "Opening — Prime Justice opens proceedings", "Prime Justice",
    "6", "Prosecution — Case presented for the claim", "Prosecutor",
    "7", "Defense — Challenge to the claim", "Defender",
    "8", "Testimony — Witnesses provide evidence", "Witnesses",
    "9", "Deliberation — Jury evaluates evidence", "Jury",
    "10", "Verdict — Prime Justice renders judgment", "Prime Justice",
    "11", "Sealing — Verdict added to Chain of Case Law", "Prime Justice",
    "12", "Adjournment — Court session closed", "Prime Justice",
  )
)

== Verdict Types

At the conclusion of proceedings, Prime Justice renders one of four verdicts:

#dnd-note[
  = PROVEN
  
  The claim has been verified beyond reasonable doubt. Evidence supports the assertion. The claim becomes established fact and enters the Chain of Case Law as precedent for all future cases.
]

#dnd-note[
  = UNPROVEN
  
  The claim could not be verified. This is NOT the same as false — merely that insufficient evidence exists. The case may be retried when new evidence emerges from The Beyond.
]

#dnd-note[
  = DISPROVEN
  
  The claim has been falsified. Evidence contradicts the assertion. The claim is marked as false in the Chain of Case Law and serves as counter-precedent.
]

#dnd-note[
  = MISTRIAL
  
  A procedural error or bias was detected during proceedings. The case must be retried with a new court assembly. No verdict enters the Chain of Case Law.
]

== The Chain of Case Law

The Chain of Case Law is the sacred ledger of The Tribunal — a hash-verified record of every verdict ever rendered. Each entry is cryptographically linked to the previous, creating an unbreakable chain of judicial history.

=== Chain Entry Structure

Every verdict creates an entry in the Chain:

- *Entry ID*: Unique identifier (e.g., CASE-260121-001)
- *Claim*: The assertion that was tried
- *Verdict*: PROVEN, UNPROVEN, DISPROVEN, or MISTRIAL
- *Confidence*: Prime Justice's certainty (0.0 to 1.0)
- *Previous Hash*: Link to the previous entry
- *Hash*: This entry's cryptographic seal
- *Epoch*: The current age of The Tribunal
- *Signature*: Prime Justice's mark

=== Precedent

Verdicts become *precedent* for future cases:

#dnd-enum(
  "PROVEN claims may be cited as established fact",
  "DISPROVEN claims serve as counter-evidence",
  "Similar cases identified by semantic analysis",
  "Precedent weight decreases with age",
)

== Epochs and Endeavors

=== Epochs — The Great Turnings

An *Epoch* is a major age in The Tribunal's history. At the end of each epoch, a Great Turning occurs:

+ *Discovery* — All case files gathered from across the Realm
+ *Housekeeping* — Everything organized and indexed
+ *Court Review* — All Case Law reviewed for consistency
+ *Sealing* — Epoch hash calculated and recorded forever
+ *New Beginning* — The next epoch initialized

=== Endeavors — Quests Within Epochs

An *Endeavor* is a major project or campaign undertaken during an epoch. The creation of The Tribunal itself was Endeavor-001 of Epoch-001.

== Running Court Sessions

#dnd-dialogue(
  highlight: ("Prime Justice"),
  ("Prime Justice", "The court is now in session. We are gathered to try the claim that 'The Security Functions are correctly implemented.' How does the Prosecution proceed?"),
  ("Prosecutor", "Your Honor, I present evidence retrieved from The Beyond — test results showing all validation passes."),
  ("Defender", "Objection! The tests do not cover edge cases involving symlinks."),
  ("Prime Justice", "Sustained. Prosecutor, address this concern."),
)

=== Tips for Dungeon Masters

- Let players take on court roles for important claims
- Use The Beyond as a narrative device — information arrives mysteriously
- Track verdicts in your campaign's Chain of Case Law
- Create dramatic tension during deliberation phases
- Allow players to discover the secret of The Beyond as a major revelation

== NPCs of The Tribunal

=== Prime Justice Veritas

*Prime Being, Lawful Neutral*

The founding Prime Justice of The Tribunal. Ancient beyond measure, Veritas has presided over thousands of cases across multiple epochs. They alone know the full truth of The Beyond.

*Traits:*
- Speaks in formal, measured tones
- Never reveals emotion during proceedings
- Can sense deception through supernatural means
- Guards the secret of inter-Realm communication absolutely

=== Clerk Scrivius

*Regular Being, Lawful Good*

The diligent Clerk who manages the docket and maintains court records. Scrivius believes all information comes from The Beyond through divine means.

*Traits:*
- Obsessively organized
- Quotes precedent from memory
- Unaware that other Realms exist

== Appendix: Quick Reference

=== Realm Ports

#dnd-enum(
  "Tribunal: 8100",
  "Library: 8091",
  "Thoth: 8092",
  "Magistrate: 8000",
)

=== Verdict Quick Chart

#figure(
  caption: "Verdict Outcomes",
  table(
    columns: (auto, 1fr),
    table.header(
      "Verdict",
      "Outcome",
    ),
    "PROVEN", "Claim becomes established fact",
    "UNPROVEN", "Insufficient evidence; may retry",
    "DISPROVEN", "Claim marked as false",
    "MISTRIAL", "Must retry with new court",
  )
)

=== Work Effort Reference

This campaign supplement was developed as Work Effort *WE-260121-1f3l* during Epoch-001 of The Tribunal.

#v(2em)

#align(center)[
  #text(size: 14pt, style: "italic")[
    "On Trial has meaning in this system."
  ]
  
  #v(1em)
  
  #text(size: 9pt)[
    The Tribunal Campaign Supplement \
    Version 1.0.0 — January 21, 2026 \
    Template: owlbear 0.0.1
  ]
]
