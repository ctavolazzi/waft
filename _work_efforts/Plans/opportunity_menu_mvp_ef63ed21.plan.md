---
name: Opportunity Menu MVP
overview: Create a filterable list-based Opportunity Menu page for Chico Fab Lab showcasing volunteer roles, membership tiers, classes, jobs, projects, and services using a hybrid YAML/Markdown data structure.
todos:
  - id: config
    content: Add opportunities collection to _config.yml
    status: completed
  - id: data-yaml
    content: Create _data/opportunities.yml with category definitions
    status: completed
  - id: collection
    content: Create _opportunities/ folder with 6-8 sample opportunity files
    status: completed
  - id: include
    content: Create _includes/opportunity-item.html list item template
    status: completed
  - id: scss
    content: Create _sass/features/_opportunities.scss styles
    status: completed
  - id: page
    content: Create opportunities.html main page with filter functionality
    status: completed
  - id: nav
    content: Add Opportunities link to _data/navigation.yml
    status: completed
  - id: import
    content: Import opportunities SCSS in assets/css/main.scss
    status: completed
---

# Chico Fab Lab Opportunity Menu MVP

## Architecture Overview

```mermaid
flowchart TB
    subgraph DataLayer [Data Layer]
        YAML["_data/opportunities.yml\n(Categories + Metadata)"]
        MD["_opportunities/*.md\n(Individual Opportunities)"]
    end
    
    subgraph PageLayer [Page Layer]
        PAGE["opportunities.html\n(Main Page)"]
        INCLUDE["_includes/opportunity-item.html\n(List Item Template)"]
    end
    
    subgraph StyleLayer [Style Layer]
        SCSS["_sass/features/_opportunities.scss"]
    end
    
    YAML --> PAGE
    MD --> PAGE
    INCLUDE --> PAGE
    SCSS --> PAGE
```



## Data Structure

### 1. Categories Configuration: `_data/opportunities.yml`

```yaml
categories:
    - id: volunteer
    label: Volunteer
    icon: "🙋"
    color: success
    - id: membership
    label: Membership
    icon: "🎫"
    color: info
    - id: classes
    label: Classes
    icon: "📚"
    color: warning
    - id: jobs
    label: Jobs
    icon: "💼"
    color: accent
    - id: projects
    label: Projects
    icon: "🔧"
    color: neutral
    - id: services
    label: Services
    icon: "🛠️"
    color: info
```



### 2. Opportunity Collection: `_opportunities/*.md`

Each opportunity is a markdown file with frontmatter:

```yaml
---
title: "Workshop Instructor"
category: volunteer
status: open        # open, filled, coming_soon
commitment: "4 hrs/month"
description: "Teach skills to community members"
requirements:
    - "Experience with equipment"
    - "Good communication skills"
contact: "hello@chicofablab.org"
apply_url: "https://discord.gg/chicofablab"
order: 1
---
# Full description in markdown body
```



## File Changes

### New Files to Create

| File | Purpose ||------|---------|| [`_data/opportunities.yml`](_data/opportunities.yml) | Category definitions and metadata || [`_opportunities/`](_opportunities/) | Collection folder for opportunity markdown files || [`opportunities.html`](opportunities.html) | Main opportunity menu page || [`_includes/opportunity-item.html`](_includes/opportunity-item.html) | Reusable list item template || [`_sass/features/_opportunities.scss`](_sass/features/_opportunities.scss) | Styles for opportunity list |

### Files to Modify

| File | Change ||------|--------|| [`_config.yml`](_config.yml) | Add `opportunities` collection || [`_data/navigation.yml`](_data/navigation.yml) | Add nav link to Opportunities || [`assets/css/main.scss`](assets/css/main.scss) | Import opportunities SCSS |

## Page Layout Design

```javascript
+------------------------------------------+
|  OPPORTUNITIES AT CHICO FAB LAB          |
|  Find your way to get involved           |
+------------------------------------------+
|  [All] [Volunteer] [Membership] ...      |  <- Filter pills
+------------------------------------------+
|  Showing X opportunities                 |
+------------------------------------------+
|  +--------------------------------------+|
|  | 🙋 Workshop Instructor    [OPEN]     ||
|  | Volunteer · 4 hrs/month              ||
|  | Teach skills to community members    ||
|  | [Apply →]                            ||
|  +--------------------------------------+|
|  +--------------------------------------+|
|  | 🎫 Maker Membership       [OPEN]     ||
|  | Membership · $50/month               ||
|  | Full access to equipment and space   ||
|  | [Learn More →]                       ||
|  +--------------------------------------+|
|  ...                                     |
+------------------------------------------+
```



## Component: opportunity-item.html

Reuses existing design patterns from [`_includes/card.html`](_includes/card.html):

- Category badge (colored by type)
- Status indicator (open/filled/coming soon)
- Title, commitment, description
- Apply/learn more link

## JavaScript

Minimal JS for client-side filtering (similar to existing wiki search in [`assets/js/main.js`](assets/js/main.js)):

- Filter pills toggle `data-category` attribute
- Show/hide items based on active filter
- Update results count

## Seed Data (MVP)

Create 6-8 sample opportunities (1-2 per category):

- Volunteer: Workshop Instructor, Lab Monitor
- Membership: Maker Tier, Community Tier  
- Classes: 3D Printing 101, Laser Basics
- Services: Custom Fabrication, Prototyping

## Implementation Order

1. Add collection config to `_config.yml`
2. Create `_data/opportunities.yml` with categories
3. Create `_opportunities/` folder with sample `.md` files
4. Create `_includes/opportunity-item.html` template
5. Create `_sass/features/_opportunities.scss` styles
6. Create `opportunities.html` main page with filter logic