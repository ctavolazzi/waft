---
name: Cold Call Landing Page
overview: Create a dedicated landing page at fogsift.com/hi optimized for cold call referrals, with an email CTA and a broad services list matching your phone pitch.
todos:
  - id: create-landing
    content: Create hi.html with hero, services list, and email CTA
    status: pending
  - id: verify-build
    content: Ensure hi.html is included in build output
    status: pending
---

# Cold Call Landing Page Strategy

## The Problem

Your current website positions FogSift as a focused diagnostic consulting practice. Your cold call pitch is broad and flexible ("anything from finding a cleaner to lead gen"). When prospects visit fogsift.com after your call, there's a disconnect.

## The Solution

Create a dedicated landing page at **fogsift.com/hi** that:
1. Matches the tone and scope of your cold call pitch
2. Provides instant credibility (your face, your name, proof you're real)
3. Has a clear email CTA (consistent with main site, sets async expectation)

## Page Structure

```
+------------------------------------------+
|            [Your Photo]                  |
|                                          |
|      Christopher Tavolazzi               |
|      Chico freelancer, ready to help     |
+------------------------------------------+
|                                          |
|  WHAT I CAN DO                           |
|  - Find the right vendors/specialists    |
|  - Generate leads & cold outreach        |
|  - Research & problem-solving            |
|  - General business support              |
|                                          |
+------------------------------------------+
|  15+ engagements | 100% satisfaction     |
+------------------------------------------+
|                                          |
|        [ EMAIL ME ]  (button)            |
|                                          |
|  "I respond within 24 hours"             |
|                                          |
+------------------------------------------+
|  Want more detail? See fogsift.com       |
+------------------------------------------+
```

## Design Decisions

| Element | Main Site | Landing Page |
|---------|-----------|--------------|
| Tone | Professional consultant | Approachable freelancer |
| Scope | Diagnostic focus | Broad/flexible services |
| Length | Multi-section | Single scroll |
| CTA | Email | Email (same) |

## Implementation

Create [`src/hi.html`](src/hi.html):
- Mobile-first, fast-loading single page
- Reuses existing CSS for visual consistency
- Mailto link with pre-filled subject: `mailto:christopher@fogsift.com?subject=From%20your%20website`
- Link to main site for those who want deeper info

## What This Gives You

On your cold call:
> "Check out fogsift.com/hi"

They visit, see your face, see what you do, and have one clear action: email you.

Simple. Clean. Matches what you just told them.
