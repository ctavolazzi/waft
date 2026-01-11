# Example Usage

## Basic Usage

Scan a directory and organize PDFs:

```bash
python3 tools/pdf_binder_organizer/organize_pdfs.py /path/to/documents
```

This will:
- Recursively scan `/path/to/documents` for all PDF files
- Extract metadata from each PDF
- Create booklets (max 25 pages each)
- Create a full binder with all PDFs
- Save metadata to JSON files

## Custom Output Directory

Specify where to save the organized PDFs:

```bash
python3 tools/pdf_binder_organizer/organize_pdfs.py /path/to/documents /path/to/output
```

## Output Structure

```
PDF_BINDER_20260111_073000/
├── FULL_BINDER.pdf                    # Complete binder with all PDFs
├── metadata.json                       # Full metadata for all PDFs
├── booklet_001.pdf                     # First booklet (≤25 pages)
├── booklet_002.pdf                     # Second booklet (≤25 pages)
├── booklet_003.pdf                     # Third booklet (≤25 pages)
└── metadata/
    ├── booklet_001_metadata.json       # Metadata for booklet 1
    ├── booklet_002_metadata.json       # Metadata for booklet 2
    └── booklet_003_metadata.json       # Metadata for booklet 3
```

## Metadata Structure

Each metadata file contains:

```json
{
  "source_directory": "/path/to/source",
  "output_directory": "/path/to/output",
  "generated": "2026-01-11T07:30:00",
  "total_pdfs": 35,
  "total_pages": 535,
  "total_size": 1150000,
  "booklet_count": 3,
  "max_pages_per_booklet": 25,
  "pdfs": [
    {
      "path": "/full/path/to/file.pdf",
      "relative_path": "subfolder/file.pdf",
      "title": "Document Title",
      "author": "Author Name",
      "page_count": 10,
      "file_size": 50000,
      "file_hash": "md5hash..."
    }
  ],
  "booklets": [
    {
      "booklet_number": 1,
      "title": "Booklet 001",
      "description": "Contains 8 PDFs, 25 pages",
      "total_pages": 25,
      "total_size": 200000,
      "pdf_count": 8,
      "pdfs": [...]
    }
  ]
}
```

## Features

- **Recursive Scanning**: Finds PDFs in all subdirectories
- **Metadata Extraction**: Extracts title, author, page count, dates from PDFs
- **Smart Grouping**: Automatically groups PDFs into booklets (max 25 pages)
- **Full Binder**: Creates complete binder with all PDFs organized by directory
- **Rich Metadata**: Comprehensive JSON metadata for all PDFs and booklets
- **Progress Display**: Real-time progress with rich console output
