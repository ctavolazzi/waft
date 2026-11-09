# Release Checklist: v0.5.2

**Release Date**: January 11, 2026  
**Version**: 0.5.2  
**Status**: ✅ Ready for Release

---

## ✅ Pre-Release Checklist

### Version Updates
- [x] `pyproject.toml` updated to 0.5.2
- [x] `src/waft/__init__.py` updated to 0.5.2
- [x] Version consistency verified

### Documentation
- [x] `CHANGELOG.md` updated with v0.5.2 section
- [x] `RELEASE_NOTES_v0.5.2.md` created
- [x] Wiki content created (WIKI_*.md files)
- [x] Documentation generated using `/waft-docs`

### Code Changes
- [x] PNG integration complete
- [x] All generators updated
- [x] Backward compatibility maintained
- [x] Changes committed

### Git Operations
- [x] Release branch created: `release/v0.5.2`
- [x] All changes committed
- [x] Branch pushed to GitHub
- [x] PR created: #7

---

## 🚀 Release Steps

### Step 1: Merge PR
- [ ] Review PR #7: https://github.com/ctavolazzi/waft/pull/7
- [ ] Merge PR to main branch
- [ ] Verify merge successful

### Step 2: Create GitHub Release
```bash
# After PR is merged, create release from main
gh release create v0.5.2 \
  --title "v0.5.2: Evolutionary Iteration Process - PNG Integration" \
  --notes-file RELEASE_NOTES_v0.5.2.md \
  --target main
```

**Or use GitHub web interface:**
1. Go to https://github.com/ctavolazzi/waft/releases/new
2. Tag: `v0.5.2`
3. Target: `main`
4. Title: `v0.5.2: Evolutionary Iteration Process - PNG Integration`
5. Description: Copy from `RELEASE_NOTES_v0.5.2.md`
6. Publish release

### Step 3: Upload Wiki Content
```bash
# Run wiki upload script
./scripts/upload_wiki.sh
```

**Or manually:**
1. Clone wiki: `git clone https://github.com/ctavolazzi/waft.wiki.git`
2. Copy WIKI_*.md files
3. Rename appropriately (WIKI_HOME.md → Home.md)
4. Commit and push

### Step 4: Tag Release
```bash
# Tag is created automatically with GitHub release
# Or manually:
git checkout main
git pull
git tag v0.5.2
git push origin v0.5.2
```

### Step 5: Verify Release
- [ ] Release appears on GitHub: https://github.com/ctavolazzi/waft/releases
- [ ] Wiki content uploaded: https://github.com/ctavolazzi/waft/wiki
- [ ] Tag created: `v0.5.2`
- [ ] Release notes visible
- [ ] Download links work

---

## 📋 Release Contents

### Files Included
- ✅ Version updates (pyproject.toml, __init__.py)
- ✅ CHANGELOG.md with v0.5.2 section
- ✅ RELEASE_NOTES_v0.5.2.md
- ✅ Wiki content (WIKI_*.md)
- ✅ Documentation generated
- ✅ Work effort tooling

### Code Changes
- ✅ PNG integration in all generators
- ✅ Fallback chain implementation
- ✅ Backward compatibility maintained

---

## 🎯 Post-Release Tasks

### Immediate
- [ ] Announce release (if applicable)
- [ ] Update any external documentation
- [ ] Monitor for issues

### Follow-up
- [ ] Address any post-release feedback
- [ ] Plan v0.5.3 features
- [ ] Continue with TKT-dr0f-003 (comparison tools)

---

## 📝 Release Summary

**What's New:**
- Automatic PNG conversion in all PDF generators
- Evolutionary iteration process workflow
- Robust fallback chain for PNG conversion
- Work effort tooling for data generation

**Impact:**
- Visual verification as standard workflow
- Evidence-based debugging enabled
- Iterative improvement process established

**Breaking Changes:**
- None (backward compatible)

**Migration:**
- No migration required
- PNG conversion is opt-out (set `convert_to_png=False`)

---

**Release is ready! Follow the steps above to complete the release.**
