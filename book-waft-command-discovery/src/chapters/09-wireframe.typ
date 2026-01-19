= Wireframe & Structure

This chapter documents the wireframe design process and HTML structure planning for the WAFT Command Dashboard.

== Wireframe Creation

The wireframe was created as HTML structure only, with visible borders to show layout without content.

=== Structure

*[Header]*:
- WAFT logo/branding
- Page title: "WAFT Command Dashboard"
- Quick search bar

*[Main Content (Grid Layout)]*:
- Left Column (2fr): Command Launcher
- Middle Column (1fr): Status Dashboard + Document Gallery
- Right Column (1fr): Work Effort Tracker + Session History

*[Footer]*:
- System status
- Last updated timestamp
- Links to documentation

== HTML Boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAFT Command Dashboard</title>
    <link rel="stylesheet" href="dashboard.css">
</head>
<body>
    <header id="main-header">...</header>
    <main id="main-content">
        <div class="dashboard-grid">
            <!-- 3-column grid layout -->
        </div>
    </main>
    <footer id="main-footer">...</footer>
    <script src="dashboard.js"></script>
</body>
</html>
```

== CSS Grid Layout

```css
.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1.5rem;
  padding: 1.5rem;
}
```

== Component Boxes

Each section was initially represented as a wireframe box:
- Visible borders (2-3px solid)
- Minimum height (100-200px)
- Labels indicating content
- No actual content yet

== Next Steps

After wireframe:
1. Add HTML boilerplate
2. Add navigation (empty)
3. Add header
4. Add components one by one
5. Screenshot each step
6. Add content incrementally

== Key Design Decisions

- *[3-column grid]*: Command launcher gets primary focus (2fr)
- *[Modular sections]*: Each component is independent
- *[Responsive]*: Grid adapts to screen size
- *[Dark mode]*: Consistent with WAFT branding
