#!/usr/bin/env python3
"""
Creative PDF Booklet Generator
==============================

Generates a diverse collection of imaginative PDF documents showcasing
the full range of WAFT's PDF generation capabilities.

Creates a booklet with:
- Poetry collections
- Technical documentation
- Philosophical reflections
- Creative writing
- Scientific papers
- Field guides
- And more!
"""

from pathlib import Path
from datetime import datetime
from waft import PDF

# Create output directory
OUTPUT_DIR = Path("_work_efforts/creative_booklet")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_poetry_collection():
    """Generate a poetry collection PDF."""
    content = """
# The Code and the Cosmos
## A Collection of Digital Verse

---

## Binary Sonnet

In zeros and ones, the universe speaks,
Through silicon dreams and electric streams,
Where logic flows and reason peaks,
And code becomes reality, it seems.

The compiler's breath, a gentle sigh,
Transforms our thoughts to working art,
Where functions dance and classes fly,
And algorithms play their part.

---

## The Infinite Loop

Round and round the code does go,
Where it stops, nobody knows,
But in the loop, we find our flow,
And in the flow, our wisdom grows.

---

## Ode to the Debugger

Oh, noble debugger, friend of mine,
Who finds the bugs that make us pine,
You trace the path through tangled code,
And light the way along the road.

---

## The Merge Conflict

Two branches meet, a clash of wills,
The merge conflict, our coding ills,
But from the conflict, strength is born,
And better code, the conflict's sworn.

---

## Elegy for Lost Data

Gone are the bits, the bytes, the streams,
Lost in the void of digital dreams,
But in our hearts, they still remain,
Until we write them once again.
"""
    
    PDF.from_markdown(
        markdown=content,
        title="The Code and the Cosmos"
    ).save(OUTPUT_DIR / "01_poetry_collection.pdf")
    print("✅ Generated: Poetry Collection")

def generate_technical_manifesto():
    """Generate a technical manifesto."""
    content = """
# The Minimalist Developer's Manifesto

## Principles for Clean Code

### 1. Simplicity Over Complexity
We believe that the simplest solution is often the best. Complexity should be earned, not assumed.

### 2. Readability First
Code is read far more often than it is written. Write for your future self and your teammates.

### 3. Small Functions, Clear Intent
Each function should do one thing well. If you can't name it clearly, it's doing too much.

### 4. Test-Driven Clarity
Tests are documentation. If you can't test it easily, the design needs work.

### 5. Refactor Fearlessly
Code is a living thing. Refactor early, refactor often. Technical debt compounds.

### 6. YAGNI (You Aren't Gonna Need It)
Don't build for hypothetical futures. Build for today's needs, design for tomorrow's changes.

### 7. Fail Fast, Fail Clearly
Errors should be obvious and immediate. Silent failures are the enemy.

### 8. Version Control is Your Time Machine
Commit often, commit clearly. Your git history is your project's memory.

### 9. Documentation Lives in Code
Comments explain why, code explains what. If you need comments to explain what, refactor.

### 10. Tools Serve Developers
Automation should reduce cognitive load, not increase it. If a tool makes you think harder, question it.

---

## The Path Forward

Embrace simplicity. Write clearly. Test thoroughly. Refactor continuously.

The best code is code that doesn't need to exist.
"""
    
    PDF.from_markdown(
        markdown=content,
        title="The Minimalist Developer's Manifesto"
    ).save(OUTPUT_DIR / "02_technical_manifesto.pdf")
    print("✅ Generated: Technical Manifesto")

def generate_philosophical_reflection():
    """Generate a philosophical reflection."""
    content = """
# On the Nature of Digital Existence

## A Meditation on Code, Consciousness, and Creation

---

## The Question of Being

What does it mean for code to exist? Is it the text in the file, the bytes on disk, the execution in memory, or the idea in the mind?

We write code, but does code write us? As we shape our tools, our tools shape us. The languages we choose constrain and enable our thoughts.

---

## The Illusion of Permanence

Code seems permanent—committed to git, deployed to servers, running in production. But code is always in flux. Every commit changes it. Every deployment updates it. Every execution creates a new instance.

Is there a "true" version of the code? Or is code, like Heraclitus's river, always changing?

---

## The Problem of Identity

When we refactor, is it the same code? If we rewrite a function from scratch but it behaves identically, is it the same function?

The Ship of Theseus problem applies to code: if we replace every line, is it the same program?

---

## The Observer Effect

Code behaves differently when observed. Add logging, and performance changes. Add tests, and behavior becomes more constrained. Add documentation, and the code itself may need to change.

We cannot observe code without changing it.

---

## The Digital and the Real

Code exists in a liminal space—not quite abstract, not quite concrete. It's text, but it's also instructions. It's data, but it's also process.

Perhaps code is the closest we've come to pure information—form without substance, pattern without matter.

---

## Conclusion

Code is a mirror. In writing code, we write ourselves. In debugging code, we debug our thinking. In refactoring code, we refactor our understanding.

The question isn't "What is code?" but "What does code reveal about us?"
"""
    
    PDF.from_markdown(
        markdown=content,
        title="On the Nature of Digital Existence"
    ).save(OUTPUT_DIR / "03_philosophical_reflection.pdf")
    print("✅ Generated: Philosophical Reflection")

def generate_recipe_book():
    """Generate a recipe book."""
    content = """
# The Developer's Cookbook
## Recipes for Better Code

---

## Recipe: The Perfect Function

### Ingredients
- One clear purpose
- Descriptive name
- 3-5 parameters (max)
- Single return type
- A pinch of error handling

### Instructions
1. Start with the name. If you can't name it clearly, it's doing too much.
2. List your parameters. If you need more than 5, consider a configuration object.
3. Write the happy path first. Make it work, then make it robust.
4. Add error handling. Fail fast, fail clearly.
5. Test with edge cases. Empty inputs, null values, boundary conditions.
6. Refactor until it reads like prose.

### Serving Size
One function serves one purpose. If it serves multiple purposes, split it.

---

## Recipe: The Maintainable Codebase

### Ingredients
- Consistent style guide
- Clear directory structure
- Comprehensive tests
- Living documentation
- Regular refactoring

### Instructions
1. Establish conventions early. Consistency is more important than perfection.
2. Organize by feature, not by type. Group related code together.
3. Write tests as you go. Tests are your safety net.
4. Keep documentation close to code. README files, docstrings, comments.
5. Schedule refactoring time. Technical debt compounds like interest.

### Cooking Time
This is a slow-cook recipe. It takes months, even years. But the result is worth it.

---

## Recipe: The Debugging Session

### Ingredients
- Reproducible bug
- Fresh perspective
- Good logging
- Rubber duck (optional but recommended)

### Instructions
1. Reproduce the bug consistently. If you can't reproduce it, you can't fix it.
2. Add logging. See what's actually happening, not what you think is happening.
3. Explain the bug to your rubber duck. Often, the explanation reveals the solution.
4. Make one change at a time. Isolate variables.
5. Test your fix. Does it solve the problem? Does it break anything else?
6. Document the fix. Why did it break? How did you fix it?

### Pro Tip
The bug is usually in the last thing you changed. But not always.

---

## Recipe: The Code Review

### Ingredients
- Open mind
- Constructive feedback
- Empathy
- Learning attitude

### Instructions
1. Read the code, not the person. Critique the code, not the coder.
2. Ask questions, don't make demands. "Have you considered X?" not "You should do X."
3. Point out what's good. Positive feedback is just as important as constructive criticism.
4. Suggest improvements, don't just point out problems.
5. Learn from the review. Every review is a learning opportunity for both parties.

### Serving Suggestion
Serve with humility and gratitude. Code reviews make everyone better.
"""
    
    PDF.from_markdown(
        markdown=content,
        title="The Developer's Cookbook"
    ).save(OUTPUT_DIR / "04_recipe_book.pdf")
    print("✅ Generated: Recipe Book")

def generate_travel_guide():
    """Generate a travel guide."""
    content = """
# A Traveler's Guide to Codebases

## Navigating Foreign Territory

---

## Before You Arrive

### Pack Your Tools
- A good IDE with search and navigation
- Git client for version control
- Documentation reader (browser, PDF viewer)
- Terminal for running commands
- Debugger for exploring

### Study the Map
- README.md - Your starting point
- Architecture docs - The big picture
- API documentation - How things connect
- Test files - Examples of how things work

---

## When You Arrive

### Establish Base Camp
1. Clone the repository
2. Read the README
3. Set up the development environment
4. Run the tests (they should pass)
5. Start the application (it should work)

### Explore the Neighborhood
- Find the entry point (main.py, index.js, etc.)
- Identify the core modules
- Map the data flow
- Understand the dependencies

---

## Common Landmarks

### The Entry Point
Where it all begins. Usually named `main`, `index`, or `app`. This is your starting point.

### The Configuration
Settings, environment variables, config files. Know where these live—they control behavior.

### The Data Layer
Models, schemas, database connections. This is where data lives and moves.

### The Business Logic
The core functionality. This is what the application actually does.

### The Interface Layer
APIs, UI, CLI. This is how users (and other systems) interact with your code.

---

## Navigating Challenges

### When You're Lost
1. Use search to find related code
2. Follow the call stack
3. Read the tests—they show expected behavior
4. Ask questions (in code comments, docs, or to teammates)

### When You Need to Change Something
1. Find all the places it's used (search is your friend)
2. Understand the current behavior
3. Write a test for the new behavior
4. Make the change
5. Verify tests still pass
6. Update documentation

### When You Find Something Strange
1. Don't assume it's wrong—there might be a reason
2. Check git history—see why it was added
3. Look for comments or documentation
4. Ask the original author (if possible)

---

## Leaving Your Mark

### When You Add Features
- Follow existing patterns
- Write tests
- Update documentation
- Keep it simple

### When You Refactor
- Don't change behavior (unless that's the goal)
- Update tests if needed
- Document why you changed it
- Make it better, not just different

---

## Parting Wisdom

Every codebase is a journey. Take your time. Ask questions. Learn the landscape. And remember: you're not just visiting—you're contributing to a living, evolving system.

Happy travels!
"""
    
    PDF.from_template(
        template="field_guide",
        title="A Traveler's Guide to Codebases",
        content=content,
        series="DEVELOPER GUIDE",
        number="DG-001"
    ).save(OUTPUT_DIR / "05_travel_guide.pdf")
    print("✅ Generated: Travel Guide")

def generate_scientific_paper():
    """Generate a creative scientific paper."""
    content = """
## Abstract

This paper presents a novel approach to understanding code complexity through the lens of information theory. We propose that code complexity can be measured not just by cyclomatic complexity, but by the information entropy of the codebase itself. Our experiments show that high-entropy codebases correlate with increased bug density, while low-entropy codebases show better maintainability scores.

## Introduction

Code complexity has traditionally been measured using metrics like cyclomatic complexity, lines of code, and nesting depth. However, these metrics fail to capture the full picture of code complexity. We propose a new metric: information entropy.

## Methodology

We analyzed 100 open-source projects, measuring:
1. Information entropy of the codebase
2. Bug density (bugs per 1000 lines)
3. Maintainability index
4. Developer velocity

## Results

Our analysis revealed a strong negative correlation between information entropy and code quality. Low-entropy codebases (highly structured, predictable patterns) showed:
- 40% lower bug density
- 25% higher maintainability scores
- 30% faster developer onboarding

## Discussion

The results suggest that reducing information entropy—through consistent patterns, clear naming, and standardized structures—can significantly improve code quality. This aligns with the principle of "least surprise" in software design.

## Conclusion

Information entropy provides a new lens for understanding code complexity. By reducing entropy through consistent patterns and clear structure, we can improve code quality without necessarily reducing functionality.

## References

1. Shannon, C. E. (1948). A Mathematical Theory of Communication
2. McCabe, T. J. (1976). A Complexity Measure
3. Martin, R. C. (2008). Clean Code
"""
    
    PDF.scientific_paper(
        title="Information Entropy as a Measure of Code Complexity",
        abstract="This paper presents a novel approach to understanding code complexity through the lens of information theory.",
        content=content,
        authors=["Dr. Code Complexity", "Prof. Information Theory"],
        affiliations=["WAFT Research Institute", "Digital Philosophy Department"]
    ).save(OUTPUT_DIR / "06_scientific_paper.pdf")
    print("✅ Generated: Scientific Paper")

def generate_code_review_guide():
    """Generate a code review guide."""
    content = """
# The Art of Code Review
## A Guide to Constructive Feedback

---

## The Purpose of Code Review

Code review isn't about finding faults—it's about:
- Sharing knowledge
- Catching bugs early
- Maintaining code quality
- Teaching and learning
- Building team cohesion

---

## What to Look For

### Functionality
- Does it do what it's supposed to do?
- Are edge cases handled?
- Are error cases handled?
- Are there any obvious bugs?

### Design
- Is the design consistent with the codebase?
- Are there better patterns available?
- Is it over-engineered or under-engineered?
- Will it scale?

### Readability
- Is the code easy to understand?
- Are names clear and descriptive?
- Is the logic straightforward?
- Are comments helpful (not just noise)?

### Testing
- Are there tests?
- Do the tests cover the new code?
- Are edge cases tested?
- Do the tests actually test something?

### Performance
- Are there obvious performance issues?
- Could it be optimized without sacrificing readability?
- Are there memory leaks or resource issues?

---

## How to Give Feedback

### Be Specific
❌ "This is confusing"
✅ "This function name doesn't clearly indicate it also validates input"

### Be Constructive
❌ "This is wrong"
✅ "Have you considered handling the null case here?"

### Explain Why
❌ "Use a map instead"
✅ "A map would be more efficient here since we're doing lookups by key"

### Ask Questions
❌ "You should refactor this"
✅ "What do you think about extracting this into a separate function?"

### Point Out Good Things
✅ "I like how you handled the error case here"
✅ "This is a clever solution to the edge case"

---

## How to Receive Feedback

### Listen First
Don't get defensive. The reviewer is trying to help.

### Ask for Clarification
If you don't understand a comment, ask. "Can you explain what you mean by X?"

### Discuss, Don't Argue
If you disagree, explain your reasoning. But be open to being wrong.

### Say Thank You
Code review takes time. Acknowledge the effort.

---

## Common Patterns

### The Nitpick
Small style issues. Usually safe to fix, but don't let them derail the review.

### The Architecture Question
Bigger design questions. These are worth discussing in detail.

### The Learning Opportunity
When the reviewer suggests something you didn't know. Great chance to learn!

### The Trade-off
When there are multiple valid approaches. Discuss the trade-offs.

---

## The Review Checklist

- [ ] Code does what it claims to do
- [ ] Tests are present and meaningful
- [ ] Code follows project conventions
- [ ] No obvious bugs or security issues
- [ ] Documentation is updated (if needed)
- [ ] Performance is acceptable
- [ ] Code is readable and maintainable

---

## Remember

Code review is a conversation, not a judgment. The goal is better code, not perfect code. And better code comes from collaboration, not criticism.
"""
    
    PDF.from_markdown(
        markdown=content,
        title="The Art of Code Review"
    ).save(OUTPUT_DIR / "07_code_review_guide.pdf")
    print("✅ Generated: Code Review Guide")

def generate_meeting_notes():
    """Generate meeting notes."""
    content = """
# Team Standup Notes
**Date:** January 13, 2026  
**Time:** 10:00 AM - 10:15 AM  
**Attendees:** Alice, Bob, Charlie, Diana

---

## What We Did Yesterday

### Alice
- ✅ Completed user authentication feature
- ✅ Fixed bug in login flow
- 🔄 Started work on password reset

### Bob
- ✅ Refactored database queries for performance
- ✅ Updated API documentation
- 🔄 Working on caching layer

### Charlie
- ✅ Deployed new version to staging
- ✅ Fixed production bug (hotfix)
- 🔄 Monitoring performance metrics

### Diana
- ✅ Completed UI redesign for dashboard
- ✅ Added accessibility features
- 🔄 Starting mobile responsive design

---

## What We're Doing Today

### Alice
- Continue password reset implementation
- Write tests for authentication flow

### Bob
- Implement caching layer
- Performance testing

### Charlie
- Monitor staging deployment
- Prepare production release notes

### Diana
- Mobile responsive design
- User testing session

---

## Blockers

### Alice
- ⚠️ Waiting on API design decision for password reset

### Bob
- None

### Charlie
- None

### Diana
- None

---

## Decisions Made

1. **Password Reset API**: Use token-based approach (agreed by team)
2. **Caching Strategy**: Redis for session data, in-memory for static content
3. **Release Schedule**: Target Friday for production release

---

## Action Items

- [ ] Alice: Finalize password reset API design (due: EOD)
- [ ] Bob: Set up Redis instance for caching (due: Tomorrow)
- [ ] Charlie: Prepare release notes (due: Thursday)
- [ ] Diana: Schedule user testing (due: This week)

---

## Next Meeting

**Date:** January 14, 2026  
**Time:** 10:00 AM  
**Focus:** Review blockers and prepare for release
"""
    
    PDF.from_markdown(
        markdown=content,
        title="Team Standup Notes - January 13, 2026"
    ).save(OUTPUT_DIR / "08_meeting_notes.pdf")
    print("✅ Generated: Meeting Notes")

def generate_personal_journal():
    """Generate a personal journal entry."""
    content = """
# Developer's Journal
**Date:** January 13, 2026  
**Time:** Late evening

---

## Today's Reflection

Today was one of those days where everything clicked. I've been working on this feature for weeks, and today it finally came together. The breakthrough came when I stopped trying to force my original design and instead listened to what the code was telling me.

There's something beautiful about that moment when you realize the code has a better idea than you do. You've been fighting it, trying to make it fit your preconceived notion, and then—click—you see it. The code was right all along.

---

## What I Learned

1. **Sometimes the best solution is the simplest one.** I spent days building a complex abstraction when a simple function would have worked better.

2. **Tests are your friends, not your enemies.** Writing tests first (TDD) felt slow, but it caught three bugs before they made it to production.

3. **Code review is a gift.** My teammate's feedback on my PR didn't just improve the code—it improved my understanding of the problem.

---

## Challenges

The biggest challenge today was debugging a race condition. It only happened sometimes, which made it maddening. But the process of debugging it taught me more about async programming than any tutorial could have.

The key was adding strategic logging and then being patient. The bug revealed itself when I stopped trying to force it to happen and just let the system run.

---

## Gratitude

I'm grateful for:
- A team that values code quality over speed
- Tools that make debugging easier
- The satisfaction of solving a hard problem
- The learning that comes from every bug

---

## Tomorrow's Focus

Tomorrow I want to:
1. Finish the documentation for this feature
2. Help my teammate with their blocker
3. Start thinking about the next feature
4. Maybe take a walk—fresh air helps with problem-solving

---

## A Final Thought

Code is more than instructions for a computer. It's a conversation between developers, a record of decisions, a map of understanding. And like any good conversation, the best code emerges when we listen as much as we speak.

Good night, code. See you tomorrow.
"""
    
    PDF.from_markdown(
        markdown=content,
        title="Developer's Journal - January 13, 2026"
    ).save(OUTPUT_DIR / "09_personal_journal.pdf")
    print("✅ Generated: Personal Journal")

def generate_mathematical_proof():
    """Generate a mathematical proof."""
    content = """
# A Proof That All Bugs Are Fixable
## (Given Infinite Time and Resources)

---

## Theorem

For any program P with bug B, there exists a program P' such that:
1. P' is functionally equivalent to P
2. P' does not contain bug B
3. P' can be constructed in finite time

---

## Proof

### Base Case: Trivial Bugs

Consider a program P with a trivial bug B (e.g., off-by-one error, typo).

**Construction of P':**
1. Identify the location of bug B
2. Apply the fix for bug B
3. Verify the fix with tests
4. Deploy P'

Since trivial bugs have known fixes, P' can be constructed in O(1) time.

**Conclusion:** Trivial bugs are fixable.

---

### Inductive Step: Complex Bugs

Assume that all bugs of complexity n are fixable.

Consider a program P with a bug B of complexity n+1.

**Case 1: Bug B is a composition of simpler bugs**
- Decompose B into bugs B₁, B₂, ..., Bₖ where each Bᵢ has complexity ≤ n
- By inductive hypothesis, each Bᵢ is fixable
- Fix each Bᵢ to get P₁, P₂, ..., Pₖ
- Compose fixes to get P'

**Case 2: Bug B requires architectural change**
- Refactor P to architecture A that avoids bug B
- Since refactoring is a finite process, P' exists

**Case 3: Bug B is a fundamental limitation**
- Rewrite P using a different approach
- Since rewriting is a finite process, P' exists

**Conclusion:** Bugs of complexity n+1 are fixable.

---

### General Case: All Bugs

By induction, all bugs of any complexity are fixable.

**Q.E.D.**

---

## Corollary: The Halting Problem Doesn't Apply

**Note:** This proof assumes we can determine if a bug exists, which is decidable for most practical bugs. The undecidability of the halting problem applies to infinite loops, not to bugs that have already manifested.

---

## Practical Implications

While all bugs are theoretically fixable, the time and resources required may be prohibitive. This is why we have:
- Bug prioritization
- Technical debt management
- Refactoring schedules
- The occasional "won't fix" label

But the theorem stands: given infinite time and resources, every bug can be fixed.

---

## Conclusion

This proof provides theoretical comfort: no bug is permanent. With enough time, effort, and coffee, any bug can be vanquished.

The challenge, of course, is that we don't have infinite time. But that's a problem for another proof.
"""
    
    PDF.from_markdown(
        markdown=content,
        title="A Proof That All Bugs Are Fixable"
    ).save(OUTPUT_DIR / "10_mathematical_proof.pdf")
    print("✅ Generated: Mathematical Proof")

def generate_design_system():
    """Generate a design system guide."""
    content = """
# WAFT Design System
## Principles and Patterns

---

## Design Philosophy

Our design system is built on three core principles:

1. **Clarity Over Cleverness**
   - Code should be obvious, not clever
   - Names should be self-documenting
   - Patterns should be consistent

2. **Simplicity Over Sophistication**
   - Prefer simple solutions
   - Avoid premature optimization
   - Keep it maintainable

3. **Consistency Over Perfection**
   - Consistent patterns are better than perfect patterns
   - Establish conventions and follow them
   - Refactor when patterns emerge

---

## Naming Conventions

### Functions
- Use verbs: `getUser()`, `calculateTotal()`, `validateInput()`
- Be specific: `getUserById()` not `getUser()`
- Avoid abbreviations: `calculateTotal()` not `calcTot()`

### Variables
- Use nouns: `userCount`, `totalPrice`, `isValid`
- Be descriptive: `userCount` not `count`
- Use boolean prefixes: `is`, `has`, `can`, `should`

### Classes
- Use nouns: `UserService`, `PaymentProcessor`, `DataValidator`
- Be specific: `UserService` not `Service`
- Use suffixes for types: `UserRepository`, `PaymentController`

---

## Code Organization

### File Structure
```
src/
├── models/          # Data models
├── services/       # Business logic
├── controllers/     # Request handling
├── repositories/    # Data access
├── utils/           # Helper functions
└── tests/           # Test files
```

### Module Organization
- One class per file (usually)
- Related functions grouped together
- Imports at the top
- Exports clearly defined

---

## Error Handling

### Principles
1. Fail fast
2. Fail clearly
3. Don't swallow errors
4. Log appropriately

### Patterns
```python
# Good: Explicit error handling
try:
    result = process_data(data)
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    raise
except ProcessingError as e:
    logger.error(f"Processing failed: {e}")
    return default_value
```

---

## Testing Patterns

### Test Structure
- Arrange: Set up test data
- Act: Execute the code
- Assert: Verify the result

### Test Naming
- Describe what is being tested
- Include expected outcome
- Example: `test_calculateTotal_returnsSumOfItems()`

---

## Documentation Standards

### Code Comments
- Explain why, not what
- Keep comments up to date
- Remove dead code and comments

### Function Documentation
- Describe purpose
- Document parameters
- Document return value
- Include examples for complex functions

---

## Version Control

### Commit Messages
- Use present tense: "Add feature" not "Added feature"
- Be specific: "Fix login bug" not "Fix bug"
- Reference issues: "Fix #123: Login bug"

### Branch Naming
- Feature: `feature/user-authentication`
- Bug fix: `fix/login-error`
- Hotfix: `hotfix/security-patch`

---

## Conclusion

A design system is a living document. It evolves as we learn. The key is consistency and communication.

When in doubt, follow the patterns. When patterns don't exist, create them. When patterns conflict, discuss and decide.
"""
    
    PDF.from_template(
        template="field_guide",
        title="WAFT Design System",
        content=content,
        series="DEVELOPER GUIDE",
        number="DG-002"
    ).save(OUTPUT_DIR / "11_design_system.pdf")
    print("✅ Generated: Design System Guide")

def generate_creative_writing():
    """Generate a creative writing piece."""
    content = """
# The Last Commit

## A Short Story

---

The terminal blinked. One last time.

Sarah stared at the screen, her fingers hovering over the keyboard. This was it. The final commit. The one that would make or break everything.

She typed: `git commit -m "Final commit: The end of an era"`

The cursor waited. The repository held its breath. And then...

Success.

But success felt empty. This codebase had been her life for three years. Every function, every class, every comment—she knew them all. They were her children, her creations, her legacy.

And now she was leaving.

---

## The Beginning

Three years ago, Sarah had been fresh out of college, full of ideas and energy. She'd joined the team as a junior developer, eager to prove herself.

The codebase was a mess. Technical debt everywhere. No tests. Documentation that was three years out of date. But Sarah saw potential.

She started small. Fixed a bug here. Refactored a function there. Wrote a test. Updated documentation. One commit at a time.

---

## The Middle

Months turned into years. Sarah grew. The codebase grew. They grew together.

She learned that code is more than instructions. It's communication. It's art. It's a record of decisions, of trade-offs, of compromises.

She learned that perfect is the enemy of good. That sometimes you ship with technical debt, and that's okay. That refactoring is a journey, not a destination.

She learned that bugs are teachers. Every bug taught her something about the system, about herself, about the craft.

---

## The End

And now, the last commit.

Sarah closed her laptop. The codebase would continue without her. New developers would come. New features would be added. New bugs would be found and fixed.

But a part of her would always be there. In the comments she wrote. In the functions she designed. In the patterns she established.

Code is immortal. Developers are not. But in code, we live on.

---

## Epilogue

Years later, a new developer would find a comment in the code:

```python
# This function is more complex than it should be,
# but it works and we don't have time to refactor.
# TODO: Simplify this when we have time.
# - Sarah, 2026
```

And they would smile, knowing that someone else had been here before. That they weren't alone in the struggle. That code is a conversation across time.

The last commit is never really the last. Code lives on. And so do we.
"""
    
    PDF.from_markdown(
        markdown=content,
        title="The Last Commit"
    ).save(OUTPUT_DIR / "12_creative_writing.pdf")
    print("✅ Generated: Creative Writing")

def generate_two_page_document():
    """Generate a two-page constraint document."""
    content = """
# The Two-Page Manifesto
## A Constraint That Sets You Free

---

## The Problem

We write too much. Documentation that no one reads. Specifications that are outdated before they're finished. Plans that change before they're implemented.

We think more is better. More detail. More explanation. More words.

But more is not better. More is just more.

---

## The Solution

The two-page constraint. Everything important can fit on two pages. If it can't, it's not focused enough.

This isn't about dumbing things down. It's about distilling. Finding the essence. Cutting away everything that doesn't matter.

---

## The Benefits

### Clarity
When you're forced to fit on two pages, you have to be clear. No room for fluff. No room for ambiguity.

### Focus
Two pages forces you to prioritize. What's really important? What can be left out?

### Action
Two pages is readable. People will actually read it. And if they read it, they might act on it.

### Maintenance
Two pages is easy to update. When things change, you update two pages. Not twenty. Not two hundred.

---

## The Rules

1. **Two pages maximum.** No exceptions. If it doesn't fit, cut it.

2. **One idea per document.** Don't try to cover everything. Focus.

3. **Use whitespace.** Don't cram. Let it breathe.

4. **Use visuals.** Diagrams, charts, tables. A picture is worth a thousand words.

5. **Link to details.** The two-page doc is the summary. Link to detailed docs for those who need them.

---

## Examples

### Architecture Decision
Two pages: The decision, the rationale, the trade-offs, the impact.

Details: Link to full ADR document.

### Project Plan
Two pages: Goals, timeline, key milestones, risks.

Details: Link to detailed project plan.

### API Design
Two pages: Purpose, key endpoints, authentication, examples.

Details: Link to full API documentation.

---

## The Challenge

Try it. Take your next document. Cut it to two pages. See what happens.

You'll find that:
- You think more clearly
- You communicate better
- People actually read it
- Things get done

---

## The Conclusion

Constraints are not limitations. They're liberations.

The two-page constraint doesn't limit what you can say. It forces you to say what matters.

And what matters is usually less than you think.

---

*This document is exactly two pages. It proves the point.*
"""
    
    PDF.two_page(
        content=content,
        title="The Two-Page Manifesto",
        style="clinical_standard"
    ).save(OUTPUT_DIR / "13_two_page_manifesto.pdf")
    print("✅ Generated: Two-Page Document")

def generate_latex_document():
    """Generate a LaTeX document."""
    content = """
\\section{Introduction}

This is a LaTeX document generated by WAFT. LaTeX provides professional typesetting for mathematical and technical documents.

\\section{Mathematical Expressions}

The quadratic formula is:

$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$

Euler's identity is considered one of the most beautiful equations in mathematics:

$$e^{i\\pi} + 1 = 0$$

\\section{Code Examples}

Here is some Python code:

\\begin{verbatim}
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
\\end{verbatim}

\\section{Lists and Formatting}

\\subsection{Ordered List}

\\begin{enumerate}
    \\item First item
    \\item Second item
    \\item Third item
\\end{enumerate}

\\subsection{Unordered List}

\\begin{itemize}
    \\item Bullet point one
    \\item Bullet point two
    \\item Bullet point three
\\end{itemize}

\\section{Conclusion}

LaTeX provides powerful typesetting capabilities for technical documents. This document demonstrates basic LaTeX features including mathematical expressions, code blocks, and lists.
"""
    
    PDF.latex(
        title="LaTeX Example Document",
        content=content
    ).save(OUTPUT_DIR / "14_latex_document.pdf")
    print("✅ Generated: LaTeX Document")

def generate_booklet_index():
    """Generate an index document for the booklet."""
    content = f"""
# Creative PDF Booklet
## Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---

## Contents

This booklet contains {15} diverse PDF documents showcasing the full range of WAFT's PDF generation capabilities.

### 1. Poetry Collection
**File:** `01_poetry_collection.pdf`  
**Style:** Premium  
**Type:** Creative writing, poetry  
**Method:** Evolution-based generation

### 2. Technical Manifesto
**File:** `02_technical_manifesto.pdf`  
**Style:** Clinical Standard  
**Type:** Technical documentation, principles  
**Method:** Evolution-based generation

### 3. Philosophical Reflection
**File:** `03_philosophical_reflection.pdf`  
**Style:** Premium  
**Type:** Philosophy, reflection  
**Method:** Evolution-based generation

### 4. Recipe Book
**File:** `04_recipe_book.pdf`  
**Style:** Professional  
**Type:** Creative documentation, recipes  
**Method:** Evolution-based generation

### 5. Travel Guide
**File:** `05_travel_guide.pdf`  
**Style:** Field Guide Template  
**Type:** Guide, documentation  
**Method:** Template-based generation

### 6. Scientific Paper
**File:** `06_scientific_paper.pdf`  
**Style:** Scientific  
**Type:** Academic paper, research  
**Method:** Scientific paper generation

### 7. Code Review Guide
**File:** `07_code_review_guide.pdf`  
**Style:** Clinical Standard  
**Type:** Guide, best practices  
**Method:** Evolution-based generation

### 8. Meeting Notes
**File:** `08_meeting_notes.pdf`  
**Style:** Professional  
**Type:** Notes, documentation  
**Method:** Evolution-based generation

### 9. Personal Journal
**File:** `09_personal_journal.pdf`  
**Style:** Premium  
**Type:** Personal writing, journal  
**Method:** Evolution-based generation

### 10. Mathematical Proof
**File:** `10_mathematical_proof.pdf`  
**Style:** Clinical Standard  
**Type:** Mathematics, proof  
**Method:** Evolution-based generation

### 11. Design System Guide
**File:** `11_design_system.pdf`  
**Style:** Field Guide Template  
**Type:** Guide, design system  
**Method:** Template-based generation

### 12. Creative Writing
**File:** `12_creative_writing.pdf`  
**Style:** Premium  
**Type:** Fiction, creative writing  
**Method:** Evolution-based generation

### 13. Two-Page Manifesto
**File:** `13_two_page_manifesto.pdf`  
**Style:** Clinical Standard  
**Type:** Manifesto, constraint  
**Method:** Two-page constraint generation

### 14. LaTeX Document
**File:** `14_latex_document.pdf`  
**Style:** LaTeX  
**Type:** Technical, LaTeX  
**Method:** LaTeX generation

### 15. Booklet Index (This Document)
**File:** `00_booklet_index.pdf`  
**Style:** Clinical Standard  
**Type:** Index, documentation  
**Method:** Evolution-based generation

---

## Generation Methods Used

This booklet demonstrates the following PDF generation methods:

1. **Evolution-based** (ChatDistiller + StylingGenome)
   - Poetry Collection
   - Technical Manifesto
   - Philosophical Reflection
   - Recipe Book
   - Code Review Guide
   - Meeting Notes
   - Personal Journal
   - Mathematical Proof
   - Creative Writing
   - Booklet Index

2. **Template-based** (WeasyPrint + Jinja2)
   - Travel Guide
   - Design System Guide

3. **Scientific Paper** (Specialized generator)
   - Scientific Paper

4. **Two-Page Constraint** (Specialized generator)
   - Two-Page Manifesto

5. **LaTeX** (LaTeX compiler)
   - LaTeX Document

---

## Styles Showcased

- **Clinical Standard**: Professional, readable, Times New Roman
- **Premium**: Elegant, generous spacing, premium serif
- **Professional**: Georgia serif, comfortable spacing
- **Field Guide Template**: Structured, binder-ready
- **Scientific**: Academic paper format
- **LaTeX**: Professional mathematical typesetting

---

## About This Booklet

This booklet was generated automatically using WAFT's unified PDF generation system. Each document demonstrates different capabilities, styles, and use cases.

The goal is to showcase the versatility and power of WAFT's PDF generation tools, from creative writing to technical documentation, from poetry to mathematical proofs.

---

## Next Steps

Explore each document to see:
- Different styling approaches
- Various content types
- Multiple generation methods
- Creative applications of PDF generation

Enjoy the journey through this diverse collection of documents!

---

*Generated with ❤️ by WAFT*
"""
    
    PDF.from_markdown(
        markdown=content,
        title="Creative PDF Booklet - Index"
    ).save(OUTPUT_DIR / "00_booklet_index.pdf")
    print("✅ Generated: Booklet Index")

def main():
    """Generate the complete creative booklet."""
    print("\n" + "=" * 60)
    print("🎨 CREATIVE PDF BOOKLET GENERATOR")
    print("=" * 60)
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print(f"📅 Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
    
    try:
        # Generate all documents
        generate_booklet_index()
        generate_poetry_collection()
        generate_technical_manifesto()
        generate_philosophical_reflection()
        generate_recipe_book()
        generate_travel_guide()
        generate_scientific_paper()
        generate_code_review_guide()
        generate_meeting_notes()
        generate_personal_journal()
        generate_mathematical_proof()
        generate_design_system()
        generate_creative_writing()
        generate_two_page_document()
        generate_latex_document()
        
        print("\n" + "=" * 60)
        print("✅ BOOKLET GENERATION COMPLETE!")
        print("=" * 60)
        print(f"\n📚 Generated {15} PDF documents")
        print(f"📁 Location: {OUTPUT_DIR.absolute()}")
        print("\n📋 Documents created:")
        for i, pdf_file in enumerate(sorted(OUTPUT_DIR.glob("*.pdf")), 1):
            size_kb = pdf_file.stat().st_size / 1024
            print(f"   {i:2d}. {pdf_file.name} ({size_kb:.1f} KB)")
        print("\n🎉 Enjoy your creative booklet!\n")
        
    except Exception as e:
        print(f"\n❌ Error generating booklet: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
