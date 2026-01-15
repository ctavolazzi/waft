---
name: Comprehensive Design Review
overview: A comprehensive design review covering code architecture, UI/UX patterns, file organization, and content structure for the How To Win Capitalism wiki project.
todos:
  - id: fix-hero-cta
    content: Fix Hero component default CTA link from /protocol/introduction/ to /faq/introduction/
    status: completed
  - id: implement-requester-id
    content: Implement session-based requester ID in src/pages/profile/[id].astro
    status: completed
  - id: update-starlight-docs
    content: Update ARCHITECTURE.md to remove/update Starlight references
    status: completed
  - id: consolidate-css
    content: Consolidate duplicate CSS between Base.astro and custom.css
    status: completed
  - id: clarify-content-routing
    content: Clarify content routing strategy and remove docs index.mdx if not canonical
    status: completed
  - id: document-profile-routes
    content: Document profile route strategy (/users/[id] vs /profile/)
    status: completed
---

# Comprehensive Design Review

## 1. Architecture Assessment

### Strengths

- **Clean Auth Architecture**: Single source of truth pattern with `userStore.ts` -> `store.ts` -> `permissions.ts` flow
- **Atomic Design Components**: Well-organized hierarchy (atoms/molecules/organisms) in [`src/components/`](src/components/)
- **Typed Content Collections**: Zod schemas with user ownership references in [`src/content.config.ts`](src/content.config.ts)
- **SSR with Cloudflare**: Hybrid rendering with Node adapter for dev, Cloudflare for production

### Concerns

| Issue | Location | Impact | Recommendation |

|-------|----------|--------|----------------|

| Dual Index Pages | `src/pages/index.astro` + `src/content/docs/index.mdx` | Route confusion | Remove docs index or clarify which is canonical |

| Legacy Starlight References | ARCHITECTURE.md line 8 | Documentation drift | Update docs to reflect current custom Base.astro layout |

| Unimplemented TODO | `src/pages/profile/[id].astro` line 28 | Profile viewer context broken | Implement session-based requester ID |

| Large Monolithic File | `src/lib/tools/decision-matrix.ts` (997 lines) | Maintainability | Consider splitting into modules |

### Data Flow Diagram

```mermaid
flowchart TB
    subgraph client [Client Layer]
        UI[UI Components]
        ApiClient[api-client.ts]
    end
    
    subgraph auth [Auth Layer]
        UserStore[userStore.ts<br/>SINGLE SOURCE]
        AuthStore[store.ts]
        Permissions[permissions.ts]
    end
    
    subgraph server [Server Layer]
        Middleware[middleware.ts]
        ApiRoutes[/api/auth/*]
        KVAuth[kv-auth.ts]
    end
    
    subgraph storage [Storage]
        KV[(Cloudflare KV)]
        LocalStorage[(localStorage)]
    end
    
    UI --> ApiClient
    ApiClient --> ApiRoutes
    ApiRoutes --> KVAuth
    KVAuth --> KV
    
    UI --> AuthStore
    AuthStore --> UserStore
    AuthStore --> LocalStorage
    UserStore --> Permissions
    
    Middleware --> ApiRoutes
```

---

## 2. UI/UX Assessment

### Strengths

- **Design System**: Consistent design tokens in [`Base.astro`](src/layouts/Base.astro) lines 130-172
- **Accessibility**: Skip-to-content, ARIA attributes, keyboard navigation, `prefers-reduced-motion`
- **Wikipedia Aesthetic**: Clean, readable typography with serif headings and sans-serif body
- **Recent UX Cleanup**: Work effort `20.03_ux-ui-full-review.md` addressed auth pages and navigation

### Concerns

| Issue | Location | Severity | Recommendation |

|-------|----------|----------|----------------|

| Auth Gate Flash | `src/pages/index.astro` lines 9-11 | Medium | Use server-side auth check or skeleton UI |

| Duplicate CSS Definitions | `Base.astro` + `custom.css` | Low | Consolidate design tokens to one location |

| No Dark Mode | Design tokens only define light colors | Low | Future enhancement |

| Hero CTA Broken Link | Hero default links to `/protocol/introduction/` | Medium | Update to `/faq/introduction/` |

### Component Inventory Status (from [`index.ts`](src/components/index.ts))

```
ACTIVE (10): WikiBox, Breadcrumbs, Collapsible, LoadingSpinner, Disclaimer, 
             DecisionMatrix, TopicCard, SeeAlso, FAQ, BlankSlate
             
AVAILABLE (2): Button, FormGroup (created but not integrated into forms)

RESERVED (6): InfoBox, NoteBox, NavBox, CallToAction, PageHeader, ContentSection

ORPHANED (1): UserMenu (recently deleted per work effort)
```

---

## 3. File Structure Assessment

### Strengths

- **Johnny Decimal Work Efforts**: Well-organized in [`_work_efforts/`](_work_efforts/)
- **Comprehensive Documentation**: ARCHITECTURE.md, devlogs, project policies
- **Clear Source Layout**: Standard Astro structure with lib/, pages/, components/

### Concerns

| Issue | Location | Recommendation |

|-------|----------|----------------|

| _planning/ folder | 18 files overlapping with _docs | Consolidate or clarify purpose |

| Multiple Profile Routes | `/profile/`, `/profile/[id].astro`, `/profile/me.astro`, `/users/[id].astro` | Document or consolidate |

| Content/Pages Overlap | `src/content/docs/index.mdx` vs `src/pages/index.astro` | Clarify routing strategy |

### Directory Structure Recommendation

```
Current structure is sound. Minor cleanup needed:
- Clarify _planning/ vs _docs/ purpose
- Remove unused src/content/docs/index.mdx if src/pages/index.astro is canonical
- Document profile route strategy (/users/[id] for public, /profile/ for self)
```

---

## 4. Content Assessment

### Strengths

- **Typed Schemas**: Content collections with Zod validation
- **Ownership Model**: Tools and docs can have owners via user references
- **Clear Hierarchy**: FAQ (concepts) / Notes (research) / Tools (templates)

### Concerns

| Issue | Location | Recommendation |

|-------|----------|----------------|

| Path Inconsistency | Some links use `/protocol/` (legacy Starlight) | Audit and update all links to `/faq/` |

| Unused Template Field | `src/content/docs/index.mdx` has `template: splash` (Starlight) | Remove unused frontmatter |

---

## 5. Security Assessment

### Strengths

- CSRF token generation in middleware
- httpOnly cookies for sessions
- Security headers (X-Content-Type-Options, X-Frame-Options)
- Rate limiting implementation
- Turnstile CAPTCHA integration

### Concerns

| Issue | Location | Severity |

|-------|----------|----------|

| Client-side Auth Gate | Multiple pages rely on JS redirect | Medium - graceful degradation needed |

| Profile Viewer Context | `requesterId` hardcoded as `null` | High - implement properly |

---

## Summary Recommendations

### Priority 1: Critical Fixes

1. Fix Hero component default CTA link (`/protocol/` -> `/faq/`)
2. Implement session-based requester ID in profile pages
3. Remove/update legacy Starlight references in documentation

### Priority 2: Technical Debt

1. Consolidate duplicate CSS between Base.astro and custom.css
2. Clarify content routing strategy (docs index vs pages index)
3. Document or consolidate profile route strategy

### Priority 3: Future Enhancements

1. Server-side auth check to eliminate loading flash
2. Integrate Button/FormGroup components into existing forms
3. Consider dark mode support
4. Modularize decision-matrix.ts

---

## Related Work Effort

The recent work effort [`20.03_ux-ui-full-review.md`](_work_efforts/20-29_design/20_ui-ux/20.03_ux-ui-full-review.md) addressed many UI consistency issues. This review builds on that work to provide a broader architectural perspective.