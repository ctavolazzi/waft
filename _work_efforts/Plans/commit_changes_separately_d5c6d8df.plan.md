# Commit Changes Separately

## Commit 1: Mobile Layout and Modularization

**Files to stage:**

- `_layouts/default.html` - mobile menu toggle, layout fixes
- `_sass/_legacy.scss` - legacy CSS cleanup
- `_sass/components/_settings-menu.scss` - extracted settings menu styles
- `_sass/features/_fab-bar.scss` - extracted FAB bar styles  
- `_sass/features/_mobile-nav.scss` - extracted mobile nav styles
- `assets/css/main.scss` - SCSS imports (partial - mobile-related only)

**Commit message:**

```javascript
feat: mobile layout improvements and CSS modularization

- Add mobile menu toggle with hamburger/close icons
- Extract settings menu styles to _settings-menu.scss
- Extract FAB bar styles to _fab-bar.scss
- Extract mobile nav styles to _mobile-nav.scss
- Clean up legacy CSS
```



## Commit 2: Opportunities Menu MVP

**Files to stage:**

- `_config.yml` - opportunities collection config
- `_data/opportunities.yml` - category definitions
- `_data/navigation.yml` - nav link
- `_includes/opportunity-item.html` - card template
- `_opportunities/*.md` - 8 sample opportunities
- `_sass/features/_opportunities.scss` - page styles
- `opportunities.html` - main page
- `assets/js/main.js` - filter functionality

**Commit message:**

```javascript
feat: add Opportunities Menu page

- Create opportunities collection with 6 categories
- Add 8 sample opportunities (volunteer, membership, classes, services)
- Build filterable list view with category pills
- Mobile-first responsive design with sticky filters
- Full-width buttons and colored card borders on mobile
```



## Remaining Files (defer or separate commit)

These files appear unrelated to the two main features:

- `_data/settings.yml` - review before committing
- `_work_efforts/10-19_category/10_subcategory/10.06_...md` - work effort docs
- `docs/technical-debt/*.md` - technical debt documentation
- `utils/security-scan.sh` - utility script

## Execution Steps

1. Stage mobile layout files
2. Commit with mobile layout message
3. Stage opportunities files  