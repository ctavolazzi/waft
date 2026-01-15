# Clean Up Portfolio Copy

## Problem

We've been going in circles - adding back aggressive copy ("Deep & Wide", "460+ repos", "overthinker quote") that was already cleaned up in the live site. The goal was to enhance the design, not revert to over-the-top messaging.

## What to Keep

- Headshot/avatar with border and hover effects
- Hero eyebrow badge ("Available for consulting")
- Hero role subtitle
- Hero buttons (Learn More, GitHub)
- Subdued orange color palette (#d97706)
- Improved gradient backgrounds

## What to Remove/Simplify

### 1. Remove highlights section entirely

The "Cross-Domain Experience", "Deep & Wide", "Practical, Not Theoretical" cards are too much. The live site doesn't have them - it goes straight to projects.

```html
<!-- REMOVE this entire block -->
<div class="highlights">...</div>
```



### 2. Revert about section to simple copy

Replace the expanded about-grid with the clean version:

```html
<section id="about" class="about-section fade-in delay-6">
  <h2>About Me</h2>
  <p>I'm a software developer focused on AI tooling and automation...</p>
  <p>Before tech, I worked as a journalist...</p>
  <p>I run multiple sites because I like to ship things...</p>
</section>
```



### 3. Simplify hero subtitle

Keep it casual and simple like the live site:> "I write Python, build AI-powered tools, and run a handful of websites. This page is the hub."

## Files to Modify

- [index.html](index.html) - Remove highlights, simplify about section, clean copy

## Result

A cleaner portfolio that: