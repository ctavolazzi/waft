# WAFT GitHub Wiki - Setup Instructions

**Created**: January 24, 2026  
**Status**: Ready to Publish

---

## 📚 Wiki Pages Created

| Page | File | Description | Status |
|------|------|-------------|--------|
| **Home** | `Home.md` | Main landing page with overview | ✅ Complete |
| **Beginner's Glossary** | `Beginners-Glossary.md` | 5 core concepts explained | ✅ Complete |
| **Breeding AI Introduction** | `Breeding-AI-Introduction.md` | Full narrative walkthrough | ✅ Complete |
| **Getting Started** | `Getting-Started.md` | Installation & first agent | ✅ Complete |

---

## 🚀 Publishing to GitHub

### Method 1: Via GitHub Web Interface (Recommended)

1. **Enable Wiki** (if not already enabled):
   ```
   Navigate to: https://github.com/ctavolazzi/waft/settings
   Scroll to: "Features" section
   Check: "Wikis" checkbox
   ```

2. **Access Wiki**:
   ```
   https://github.com/ctavolazzi/waft/wiki
   ```

3. **Create Pages**:
   - Click "Create the first page" or "New Page"
   - Copy content from `_wiki/Home.md`
   - Paste into web editor
   - Set title: "Home"
   - Click "Save Page"

4. **Add Remaining Pages**:
   - Click "New Page" for each file
   - Copy content from respective `.md` file
   - Use exact page titles (GitHub auto-creates URLs)

### Method 2: Clone Wiki as Git Repository

```bash
# Clone the wiki repo (separate from main repo)
git clone https://github.com/ctavolazzi/waft.wiki.git
cd waft.wiki

# Copy wiki files
cp ../_wiki/*.md .

# Commit and push
git add .
git commit -m "Initial wiki setup with comprehensive documentation"
git push origin master
```

---

## 📋 Page Titles and URLs

Use these exact titles when creating pages:

| Page Title | URL Slug | Source File |
|------------|----------|-------------|
| Home | (root) | `Home.md` |
| Beginner's Glossary | `Beginners-Glossary` | `Beginners-Glossary.md` |
| Breeding AI Introduction | `Breeding-AI-Introduction` | `Breeding-AI-Introduction.md` |
| Getting Started | `Getting-Started` | `Getting-Started.md` |

---

## 📖 Wiki Structure

```
GitHub Wiki
├── Home (Landing page)
│   ├── Quick Links
│   ├── Documentation Levels
│   ├── Three Pillars
│   ├── Current Status
│   └── Learning Path
│
├── Beginner's Glossary
│   ├── 1. The Substrate
│   ├── 2. Genome ID
│   ├── 3. Scint System
│   ├── 4. Flight Recorder
│   └── 5. Phylogenetic Trees
│
├── Breeding AI Introduction
│   ├── 1. Building to Breeding
│   ├── 2. Code as DNA
│   ├── 3. Mutation & Reproduction
│   ├── 4. Scint Gym
│   ├── 5. Fitness Scoring
│   ├── 6. Evolutionary Cycle
│   ├── 7. Flight Recorder
│   └── 8. God-Head Agent
│
└── Getting Started
    ├── Installation
    ├── First Agent
    ├── Scint Gym Testing
    ├── Manual Evolution
    ├── Empirica Tracking
    └── Troubleshooting
```

---

## 🔗 Internal Links

The wiki uses these linking conventions:

```markdown
# Link to another page
[Beginner's Glossary](Beginners-Glossary)

# Link to section
[Three Pillars](#three-pillars-of-waft)

# Link to external
[GitHub Discussions](https://github.com/ctavolazzi/waft/discussions)
```

---

## ✅ Pre-Publication Checklist

- [x] All 4 core pages created
- [x] Internal links verified
- [x] Code examples tested
- [x] Implementation status accurate (70-75%)
- [x] Learning path clear
- [x] Troubleshooting included
- [ ] Wiki enabled on GitHub
- [ ] Pages published
- [ ] Links tested in browser

---

## 🎯 Next Wiki Pages (Future)

### Technical Documentation
- [ ] **Architecture** - System design deep dive
- [ ] **Scint Gym** - Detailed gym mechanics
- [ ] **Pantheon** - Specialized agents
- [ ] **API Reference** - Complete API docs

### Tutorials
- [ ] **Mutation Strategies** - How to mutate code effectively
- [ ] **Fitness Optimization** - Improving agent scores
- [ ] **Telemetry Analysis** - Understanding data

### Research
- [ ] **Research Proposal** - Academic context (from docs)
- [ ] **Study Guide** - Quiz & self-assessment (from docs)
- [ ] **Use Cases** - Real-world applications
- [ ] **Implementation Status** - Current completeness

### Community
- [ ] **Contributing** - How to contribute
- [ ] **FAQ** - Frequently asked questions
- [ ] **Roadmap** - Future development
- [ ] **Changelog** - Version history

---

## 📊 Wiki Analytics

Once published, track:
- Page views
- Most popular pages
- Search queries
- Navigation patterns

Access via GitHub Insights → Traffic (if available)

---

## 🔄 Keeping Wiki Updated

### Sync with Documentation

When Typst docs update:
1. Convert changes to Markdown
2. Update relevant wiki pages
3. Commit to wiki repo
4. Verify links still work

### Version Tracking

```bash
# Tag wiki versions to match releases
cd waft.wiki
git tag -a v0.1.0 -m "Wiki for WAFT v0.1.0"
git push origin v0.1.0
```

---

## 🎨 Customization Options

### Sidebar

Create `_Sidebar.md` for custom navigation:

```markdown
**Quick Navigation**

* [Home](Home)
* [Getting Started](Getting-Started)

**Learn**
* [Beginner's Glossary](Beginners-Glossary)
* [Breeding AI Intro](Breeding-AI-Introduction)

**Technical**
* [Architecture](Architecture)
* [API Reference](API-Reference)

**Research**
* [Research Proposal](Research-Proposal)
* [Study Guide](Study-Guide)
```

### Footer

Create `_Footer.md` for page footer:

```markdown
---
**WAFT Framework** | [GitHub](https://github.com/ctavolazzi/waft) | [Issues](https://github.com/ctavolazzi/waft/issues) | [Discussions](https://github.com/ctavolazzi/waft/discussions)
```

---

## 📞 Support

If you encounter issues:
1. Check GitHub Wiki documentation
2. Ask in [Discussions](https://github.com/ctavolazzi/waft/discussions)
3. Report bugs in [Issues](https://github.com/ctavolazzi/waft/issues)

---

## ✨ Publishing Commands

```bash
# Quick publish script
cd /Users/ctavolazzi/Code/active/waft

# Option 1: Clone wiki repo and copy files
git clone https://github.com/ctavolazzi/waft.wiki.git
cp _wiki/*.md waft.wiki/
cd waft.wiki
git add .
git commit -m "Initial wiki with comprehensive documentation"
git push

# Option 2: Manual via web interface
echo "Visit: https://github.com/ctavolazzi/waft/wiki"
echo "Copy content from _wiki/ directory"
```

---

**Status**: ✅ Ready to publish  
**Pages**: 4 complete, ~8 planned  
**Next Step**: Enable wiki on GitHub and publish pages
