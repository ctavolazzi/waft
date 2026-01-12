# PDF Binder Organizer

Recursively scans a directory for PDFs and organizes them into structured booklets.

## Features

- **Recursive Scanning**: Deep scans any directory path for all PDF files
- **Metadata Extraction**: Extracts title, author, page count, creation date from each PDF
- **Smart Booklet Assembly**: Groups PDFs into booklets (max 25 pages each)
- **Full Binder**: Creates a complete binder with all PDFs
- **Rich Metadata**: Saves comprehensive metadata to JSON files
- **Organized Output**: Creates structured folder with booklets and metadata

## Usage

```bash
python3 tools/pdf_binder_organizer/organize_pdfs.py /path/to/directory
```

## Output Structure

```
output_folder/
├── FULL_BINDER.pdf              # Complete binder with all PDFs
├── metadata.json                 # Full metadata for all PDFs
├── booklet_001.pdf              # First booklet (≤25 pages)
├── booklet_002.pdf              # Second booklet (≤25 pages)
├── ...
└── metadata/
    ├── booklet_001_metadata.json
    ├── booklet_002_metadata.json
    └── ...
```

## How It Works

1. **Scan**: Recursively finds all PDFs in the directory
2. **Extract**: Reads metadata from each PDF (title, author, pages, etc.)
3. **Group**: Organizes PDFs into booklets (max 25 pages each)
4. **Assemble**: Creates booklets using WAFT's Binder system
5. **Full Binder**: Creates complete binder with all PDFs
6. **Metadata**: Saves all metadata to JSON files
