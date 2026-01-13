# Links

**Create bidirectional documentation links - connect related documents.**

Creates bidirectional links between related documents, finds related documents, creates links between them, updates indexes, and maintains link integrity. Perfect for connecting related documentation and maintaining documentation relationships.

**Use when:** Documents need to reference each other, want to create documentation relationships, or need to maintain link integrity.

---

## Purpose

This command provides:
- **Link Creation**: Create links between documents
- **Bidirectional Links**: Create links in both directions
- **Index Updates**: Update indexes with links
- **Link Integrity**: Verify and maintain links
- **Relationship Management**: Manage document relationships

---

## Philosophy

1. **Bidirectional**: Links work both ways
2. **Automatic**: Automatically create reverse links
3. **Consistent**: Use consistent link format
4. **Maintainable**: Easy to maintain and update
5. **Useful**: Links add value to documentation

---

## Execution Steps

### Links 1.1: Identify Related Documents
**Purpose**: Find documents that should be linked

**Steps**:
1. Analyze current document context
2. Search for related documents
3. Identify potential link targets
4. Check for existing links
5. Determine link relationships

**Output**: List of related documents

---

### Links 1.2: Create Links
**Purpose**: Create bidirectional links

**Steps**:
1. Create forward link (current → target)
2. Create reverse link (target → current)
3. Use consistent link format (Obsidian-style `[[link]]`)
4. Add link context if needed
5. Verify link targets exist

**Output**: Created links

---

### Links 1.3: Update Indexes
**Purpose**: Update index files with links

**Steps**:
1. Find relevant index files
2. Add links to indexes
3. Update link references
4. Ensure consistency
5. Verify index integrity

**Output**: Updated indexes

---

### Links 1.4: Verify Link Integrity
**Purpose**: Check link validity

**Steps**:
1. Verify link targets exist
2. Check for broken links
3. Fix broken links
4. Report link status
5. Update link references

**Output**: Link integrity report

---

## Execution Flow

```
Links 1.1: Identify Related Documents
  ↓
Links 1.2: Create Links
  ↓
Links 1.3: Update Indexes
  ↓
Links 1.4: Verify Link Integrity
  ↓
✅ Complete - Links created and verified
```

---

## Output Format

### Console Output

The command displays link creation summary:

```
🔗 Links: Documentation Linking

Related Documents Identified:
  - CURSOR_DEVELOPMENT_PLAN.md
  - COMMAND_RECOMMENDATIONS.md
  - help.md
  - status.md

Links Created:
  ✅ context.md ↔ CURSOR_DEVELOPMENT_PLAN.md
  ✅ context.md ↔ COMMAND_RECOMMENDATIONS.md
  ✅ sync.md ↔ context.md
  ✅ todos.md ↔ context.md

Index Updates:
  ✅ Updated .cursor/commands/index.md
  ✅ Updated _work_efforts/WE-260112-g0ih_*/index.md

Link Integrity:
  ✅ All links verified
  ✅ 0 broken links
  ✅ All targets exist

Summary:
  Links Created: 8 (4 bidirectional pairs)
  Indexes Updated: 2
  Links Verified: 8
  Broken Links: 0

⏱️  Link creation complete: 5.2s
```

---

## Link Format

### Obsidian-Style Links

Links use Obsidian-style format:
```markdown
[[document-name]] - Link to document
[[document-name|display text]] - Link with custom text
[[path/to/document]] - Link with path
```

### Bidirectional Links

When creating a link from A to B:
1. Add `[[B]]` to document A
2. Add `[[A]]` to document B
3. Both documents reference each other

### Link Context

Links can include context:
```markdown
See [[related-document]] for more information.
Related: [[another-document]] and [[third-document]].
```

---

## Use Cases

### 1. Link Related Documents
**Scenario**: Documents are related and should be linked

**Example**:
```
User: "/links"
AI: [Analyzes current context, finds related docs]
AI: [Creates bidirectional links]
```

**Output**: Links created between related documents

---

### 2. Update Indexes
**Scenario**: Need to update indexes with new links

**Example**:
```
User: "/links --update-indexes"
```

**Output**: Indexes updated with links

---

### 3. Verify Links
**Scenario**: Want to verify link integrity

**Example**:
```
User: "/links --verify"
```

**Output**: Link integrity report

---

### 4. Create Specific Links
**Scenario**: Want to link specific documents

**Example**:
```
User: "/links context.md sync.md"
```

**Output**: Links created between specified documents

---

## Integration with Other Commands

- **`/search`**: Finds documents (`/links` creates links between them)
- **`/sync`**: Syncs docs (`/links` verifies link integrity)
- **`/context`**: Provides context (`/links` links context docs)
- **`/cleanup`**: Cleans up (`/links` fixes broken links)

---

## When to Use

**Use `/links` when**:
- ✅ Documents need to reference each other
- ✅ Want to create documentation relationships
- ✅ Need to maintain link integrity
- ✅ Want to update indexes
- ✅ Need bidirectional links

**Don't use `/links` when**:
- ❌ Links are already correct
- ❌ Using external link system (use that instead)
- ❌ Documents aren't related

---

## Technical Details

### Tools Used

**File System**:
- File reading/writing for link creation
- Markdown parsing for link detection
- Pattern matching for link format

**MCP Servers** (if available):
- `mcp_docs-maintainer_update_doc` - Update docs with links
- `mcp_docs-maintainer_rebuild_indices` - Rebuild indexes
- `mcp_docs-maintainer_check_health` - Check link health

**Link Detection**:
- Pattern matching for `[[link]]` format
- File existence verification
- Path resolution

### Performance

- **Target Time**: < 10 seconds
- **Document Analysis**: ~2 seconds
- **Link Creation**: ~3 seconds
- **Index Updates**: ~2 seconds
- **Link Verification**: ~2 seconds
- **Reporting**: ~1 second

### Error Handling

- **Missing Targets**: Report broken links, continue
- **File Errors**: Show error, continue with available files
- **Parse Errors**: Show error, continue
- **Always Complete**: Always show what was linked

---

## Example Workflow

```
User: "/links"

AI: 🔗 Links: Documentation Linking

Analyzing current context...
Found 4 related documents:
  - CURSOR_DEVELOPMENT_PLAN.md
  - COMMAND_RECOMMENDATIONS.md
  - help.md
  - status.md

Creating bidirectional links...
  ✅ context.md ↔ CURSOR_DEVELOPMENT_PLAN.md
  ✅ context.md ↔ COMMAND_RECOMMENDATIONS.md
  ✅ sync.md ↔ context.md
  ✅ todos.md ↔ context.md

Updating indexes...
  ✅ Updated 2 index files

Verifying links...
  ✅ All 8 links verified
  ✅ 0 broken links

Summary:
  Links Created: 8 (4 bidirectional pairs)
  Indexes Updated: 2
  Links Verified: 8

⏱️  Link creation complete: 5.1s

User: [Links created, documentation connected]
```

---

## Advanced Features

### Link Types
Create different link types:
```bash
/links --related        # Related documents
/links --references     # Reference links
/links --see-also       # See also links
```

### Link Scope
Limit link scope:
```bash
/links --work-efforts   # Work efforts only
/links --commands       # Commands only
/links --all            # All (default)
```

### Link Verification
Verify link integrity:
```bash
/links --verify         # Verify all links
/links --fix            # Fix broken links
```

### Link Context
Add link context:
```bash
/links --context        # Add context to links
```

---

## Best Practices

1. **Link Related**: Only link truly related documents
2. **Bidirectional**: Always create bidirectional links
3. **Consistent Format**: Use consistent link format
4. **Update Indexes**: Update indexes when creating links
5. **Verify Links**: Regularly verify link integrity

---

## Output Location

Links are created in the documents themselves. A summary is displayed in console.

For link documentation:
- Links are embedded in markdown files
- Index files track link relationships
- Link integrity can be verified

---

**This command creates and maintains documentation links - essential for connecting related content and maintaining documentation relationships.**
