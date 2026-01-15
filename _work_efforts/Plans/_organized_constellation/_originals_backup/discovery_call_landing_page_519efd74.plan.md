---
name: Discovery Call Landing Page
overview: Create a focused landing page at fogsift.com/hi that funnels visitors toward a discovery conversation, with clear expectations about the contract-based, pay-as-you-go working style.
todos:
  - id: create-hi-page
    content: Create src/hi.html with hero, value prop, outcomes, how-I-work, and CTA
    status: pending
  - id: verify-build
    content: Ensure hi.html is included in build output
    status: pending
---

# Discovery Call Landing Page

## The Goal

Funnel visitors toward one action: **give Christopher 15 minutes** to figure out what's mutually beneficial. Set clear expectations about how the working relationship operates.

## Page Structure

```
+--------------------------------------------------+
|                                                  |
|              [Your Photo]                        |
|         Christopher Tavolazzi                    |
|         Chico, CA                                |
|                                                  |
+--------------------------------------------------+
|                                                  |
|      Give me 15 minutes.                         |
|      We'll figure out what you actually need.    |
|                                                  |
+--------------------------------------------------+
|                                                  |
|  What could come from our conversation:          |
|                                                  |
|  - An answer to your question                    |
|  - A referral to someone who can help            |
|  - A service I can provide                       |
|  - Something neither of us has thought of yet    |
|                                                  |
+--------------------------------------------------+
|                                                  |
|  HOW I WORK                                      |
|                                                  |
|  - We scope it together as we go                 |
|  - Everything written down before work starts    |
|    (deliverables, timeline, expectations)        |
|  - You pay step by step, not upfront             |
|  - Scope can change - that's built in            |
|  - If I can't do it, I'll find someone who can   |
|                                                  |
+--------------------------------------------------+
|                                                  |
|  No pitch. No pressure.                          |
|                                                  |
|           [ LET'S TALK ]                         |
|                                                  |
+--------------------------------------------------+
|                                                  |
|  15+ engagements | 8+ industries                 |
|                                                  |
|  "Christopher asked the questions we should      |
|   have been asking ourselves."                   |
|                                                  |
+--------------------------------------------------+
|                                                  |
|         More at fogsift.com                      |
|                                                  |
+--------------------------------------------------+
```

## The "How I Work" Section

This addresses trust concerns head-on:

| What You Say | What They Hear |
|--------------|----------------|
| We scope it together | "I have input, not just handed a contract" |
| Everything written down first | "No surprises, I know what I'm paying for" |
| Pay step by step | "Low risk, I can stop anytime" |
| Scope can change | "Flexible, not rigid" |
| If I can't, I'll find someone | "Honest, not just trying to sell me" |

## Implementation

Create [`src/hi.html`](src/hi.html):
- Hero: photo + name + location
- Value prop: "15 minutes to figure out what you need"
- Outcomes: what could come from the conversation
- How I Work: 5 bullet trust signals
- CTA: "Let's Talk" email button
- Social proof: one stat line + one quote
- Footer: link to main site

Design notes:
- Mobile-first
- Single scroll, no navigation
- Same fonts/colors as main site
- Conversational, approachable tone

## What You Say on the Phone

> "Check out fogsift.com/hi - it explains how I work. You can reach out from there."
