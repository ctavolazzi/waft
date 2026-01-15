---
name: Cold Call Landing Page
overview: Create a dedicated landing page at fogsift.com/hi optimized for cold call referrals, featuring a "Text Me" CTA and a broad services list that matches your phone pitch.
todos:
  - id: create-landing
    content: Create hi.html landing page with hero, services list, and Text Me CTA
    status: pending
  - id: sms-fallback
    content: Add desktop fallback for SMS link (display number when SMS not supported)
    status: pending
  - id: add-to-build
    content: Ensure hi.html is included in build process if needed
    status: pending

category: hopes
confidence: 1.00
constellation_date: 2026-01-14
---

# Cold Call Landing Page Strategy

## The Problem

Your current website positions FogSift as a focused diagnostic consulting practice. Your cold call pitch is broad and flexible ("anything from finding a cleaner to lead gen"). When prospects visit fogsift.com after your call, there's a disconnect.

## The Solution

Create a dedicated landing page at **fogsift.com/hi** (short, memorable, easy to say on the phone) that:
1. Matches the tone and scope of your cold call pitch
2. Provides instant credibility
3. Makes texting you dead simple

## Page Structure

```mermaid
flowchart TD
    subgraph hero [Hero Section]
        Photo[Your Photo]
        Name["Christopher Tavolazzi"]
        Tagline["Chico freelancer ready to help"]
    end
    
    subgraph services [What I Can Do]
        S1["Find the right vendors"]
        S2["Generate leads"]
        S3["Cold outreach"]
        S4["Research & answers"]
        S5["General support"]
    end
    
    subgraph proof [Quick Proof]
        Stats["15+ engagements | 100% satisfaction"]
    end
    
    subgraph cta [Call to Action]
        TextBtn["TEXT ME button"]
        Phone["(visible number)"]
    end
    
    subgraph footer [Footer]
        MainSite["See more at fogsift.com"]
    end
    
    hero --> services --> proof --> cta --> footer
```

## Key Design Decisions

| Element | Current Site | Landing Page |
|---------|--------------|--------------|
| Tone | Professional consultant | Approachable freelancer |
| Scope | Diagnostic/root cause | Broad/flexible services |
| CTA | "Email" | "Text Me" |
| Feel | Boutique firm | Local guy who can help |
| Length | Multi-section | Single scroll |

## Implementation

Create [`src/hi.html`](src/hi.html) with:
- Mobile-first, fast-loading design
- Reuses existing CSS tokens for visual consistency
- Prominent SMS link: `sms:+1XXXXXXXXXX?body=Hi%20from%20your%20website`
- Fallback for desktop (shows number to text)
- Link to main site for those who want to dig deeper

## Before Implementation

I need one piece of information:
- **Your phone number** for the SMS link (or confirm you'll add it yourself)

## What This Gives You

On your cold call, you say:
> "Check out fogsift.com/hi - you can text me directly from there."

They visit on their phone, see:
1. Your face (you're real)
2. What you do (matches what you just said)
3. A big "Text Me" button

Friction: near zero.
