# v0.5.2 Release Instructions

**Complete step-by-step guide to finalize the GitHub release**

---

## ✅ What's Already Done

- ✅ Version updated to 0.5.2
- ✅ CHANGELOG.md updated
- ✅ Release notes created
- ✅ Wiki content prepared
- ✅ Documentation generated
- ✅ Release branch created and pushed
- ✅ PR #7 created: https://github.com/ctavolazzi/waft/pull/7

---

## 🚀 Final Steps (In Order)

### Step 1: Merge PR #7

**PR Link**: https://github.com/ctavolazzi/waft/pull/7

1. Review the PR
2. Merge to `main` branch
3. Verify merge successful

---

### Step 2: Create GitHub Release

**Option A: Using GitHub CLI** (Recommended)

```bash
# Switch to main and pull latest
git checkout main
git pull

# Create release
gh release create v0.5.2 \
  --title "v0.5.2: Evolutionary Iteration Process - PNG Integration" \
  --notes-file RELEASE_NOTES_v0.5.2.md \
  --target main
```

**Option B: Using GitHub Web Interface**

1. Go to: https://github.com/ctavolazzi/waft/releases/new
2. **Choose a tag**: `v0.5.2` (create new tag)
3. **Target**: `main`
4. **Release title**: `v0.5.2: Evolutionary Iteration Process - PNG Integration`
5. **Description**: Copy entire content from `RELEASE_NOTES_v0.5.2.md`
6. **Set as**: Latest release (if this is the latest)
7. Click **"Publish release"**

---

### Step 3: Upload Wiki Content

**Option A: Using Script** (Recommended)

```bash
# From project root
./scripts/upload_wiki.sh
```

**Option B: Manual Upload**

```bash
# Clone wiki repository
git clone https://github.com/ctavolazzi/waft.wiki.git
cd waft.wiki

# Copy and rename wiki files
cp ../WIKI_HOME.md Home.md
cp ../WIKI_Getting_Started.md Getting-Started.md
cp ../WIKI_Evolutionary_Iteration_Process.md Evolutionary-Iteration-Process.md
cp ../WIKI_PDF_Generation_Guide.md PDF-Generation-Guide.md
cp ../WIKI_PDF_PNG_Conversion.md PDF-PNG-Conversion.md

# Commit and push
git add .
git commit -m "Add v0.5.2 wiki content

- Home page with quick start
- Getting Started guide
- Evolutionary Iteration Process documentation
- PDF Generation Guide
- PDF/PNG Conversion guide"
git push
```

---

### Step 4: Verify Release

Check the following:

- [ ] Release appears at: https://github.com/ctavolazzi/waft/releases/tag/v0.5.2
- [ ] Release notes are visible and formatted correctly
- [ ] Tag `v0.5.2` exists
- [ ] Wiki content uploaded: https://github.com/ctavolazzi/waft/wiki
- [ ] Download links work (if applicable)

---

## 📋 Quick Command Reference

```bash
# 1. Merge PR (via GitHub web or CLI)
gh pr merge 7

# 2. Create release
gh release create v0.5.2 \
  --title "v0.5.2: Evolutionary Iteration Process - PNG Integration" \
  --notes-file RELEASE_NOTES_v0.5.2.md \
  --target main

# 3. Upload wiki
./scripts/upload_wiki.sh

# 4. Verify
gh release view v0.5.2
```

---

## 📝 Release Summary

**Version**: 0.5.2  
**Type**: Minor Release (Feature Addition)  
**Key Feature**: Automatic PNG conversion in all PDF generators  
**Breaking Changes**: None  
**Migration**: Not required (backward compatible)

**Files Ready**:
- `RELEASE_NOTES_v0.5.2.md` - Release notes
- `WIKI_*.md` - Wiki content (5 files)
- `scripts/upload_wiki.sh` - Wiki upload script
- `RELEASE_CHECKLIST_v0.5.2.md` - Complete checklist

---

## 🎯 Expected Outcome

After completing all steps:

1. ✅ GitHub release created at: https://github.com/ctavolazzi/waft/releases/tag/v0.5.2
2. ✅ Tag `v0.5.2` exists
3. ✅ Wiki content available at: https://github.com/ctavolazzi/waft/wiki
4. ✅ Release notes visible and complete
5. ✅ All documentation up to date

---

**Follow these steps in order to complete the v0.5.2 release!**
