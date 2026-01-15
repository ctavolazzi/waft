# /the-archivist - Daily PDF Archive & Morning Report

**The Archivist - A Being who keeps things tidy. Minimal effort, maximum results.**

Like an old guy keeping things in case we need them again someday.

---

## Purpose

The Archivist handles:
- **Daily PDF Collection**: Archives all PDFs from the day
- **Morning Reports**: Generates organized reports of daily work
- **Archive Management**: Keeps project from bloating with unorganized files
- **Easy Retrieval**: Maintains archive index for finding documents

**Use when:**
- End of day to archive today's work
- Morning to review yesterday's documents
- Need to find archived PDFs
- Want to keep project organized

---

## Quick Start

### Daily Archive & Report
```
/the-archivist
```

Archives today's PDFs and generates morning report.

### Archive Only
```
/the-archivist --archive-only
```

Just archives, doesn't generate report.

### Report Only
```
/the-archivist --report-only
```

Just generates report from existing PDFs.

### Archive Specific Date
```
/the-archivist --date 2026-01-13
```

Archive and report for specific date.

### Archive Statistics
```
/the-archivist --stats
```

Shows archive statistics.

---

## What The Archivist Does

### 1. PDF Collection
- Finds all PDFs modified today
- Organizes by category:
  - Briefs & Session Reports
  - Proof Cases & Verification
  - Studies & Research
  - Work Efforts Documents
  - Other Documents

### 2. Archiving
- Copies PDFs to `_archive/daily/YYYY-MM-DD/`
- Updates archive index
- Preserves original files
- Tracks file sizes and paths

### 3. Morning Report
- Generates organized PDF report
- Lists all documents by category
- Shows file sizes and paths
- Provides summary statistics
- Saves to `_archive/reports/morning_report_YYYYMMDD.pdf`

### 4. Archive Index
- Maintains `_archive/archive_index.json`
- Tracks all archived dates
- Records file counts and paths
- Enables easy retrieval

---

## Archive Structure

```
_archive/
├── daily/
│   ├── 2026-01-13/
│   │   ├── document1.pdf
│   │   ├── document2.pdf
│   │   └── ...
│   └── 2026-01-14/
│       └── ...
├── reports/
│   ├── morning_report_20260113.pdf
│   ├── morning_report_20260114.pdf
│   └── ...
└── archive_index.json
```

---

## Philosophy

**Minimal Effort, Maximum Results**

The Archivist:
- Doesn't move files (just copies to archive)
- Doesn't delete anything
- Keeps things organized
- Makes retrieval easy
- Works quietly in the background

**Like an old guy keeping things tidy in case we need them again someday.**

---

## Integration

### With Daily Workflow
- Run at end of day to archive
- Review morning report next day
- Find archived documents easily

### With Project Organization
- Prevents PDF bloat in main directories
- Maintains organized archive
- Keeps project clean

### With Being System
- The Archivist is a Being
- Can be spawned like other Beings
- Learns and evolves archive strategies

---

## Examples

### End of Day Archive
```
/the-archivist
```

Archives all today's PDFs and generates report.

### Morning Review
```
/the-archivist --report-only
```

Generates report from existing PDFs for review.

### Weekly Archive Check
```
/the-archivist --stats
```

See how many documents have been archived.

---

## Best Practices

1. **Run Daily**: Archive at end of work day
2. **Review Reports**: Check morning reports regularly
3. **Use Index**: Reference archive_index.json for retrieval
4. **Keep Originals**: Archive copies, doesn't move originals
5. **Trust The Archivist**: Minimal effort, maximum results

---

## Troubleshooting

### No PDFs Found
- Check date format (YYYY-MM-DD)
- Verify PDFs exist and were modified today
- Check file permissions

### Archive Path Issues
- Ensure `_archive/` directory exists
- Check write permissions
- Verify disk space

### Report Not Generated
- Check PDFs exist
- Verify brief system is working
- Review error messages

---

## Related Commands

- **`/waft-status`**: Current system status
- **`/brief`**: Generate briefs (archived by Archivist)
- **`/prove-it`**: Generate proofs (archived by Archivist)

---

**The Archivist keeps things tidy, just in case we need them again someday.**

---

End Command
