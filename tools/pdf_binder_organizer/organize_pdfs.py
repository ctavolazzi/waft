#!/usr/bin/env python3
"""
PDF Binder Organizer

Recursively scans a directory for PDFs and organizes them into structured booklets
with comprehensive metadata.

Features:
- Recursive depth scan of any directory
- Metadata extraction from PDFs
- Smart booklet assembly (max 25 pages each)
- Full binder creation
- Rich metadata saved to JSON
"""

import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pypdf import PdfReader
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeRemainingColumn
from rich.table import Table

from src.waft.binder import Binder, DocumentEntry

console = Console()

# Maximum pages per booklet
MAX_PAGES_PER_BOOKLET = 25


@dataclass
class PDFMetadata:
    """Metadata extracted from a PDF file."""

    path: Path
    title: str
    author: str | None = None
    subject: str | None = None
    creator: str | None = None
    producer: str | None = None
    creation_date: str | None = None
    modification_date: str | None = None
    page_count: int = 0
    file_size: int = 0
    relative_path: str = ""
    directory: str = ""
    file_hash: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": str(self.path),
            "relative_path": self.relative_path,
            "directory": self.directory,
            "title": self.title,
            "author": self.author,
            "subject": self.subject,
            "creator": self.creator,
            "producer": self.producer,
            "creation_date": self.creation_date,
            "modification_date": self.modification_date,
            "page_count": self.page_count,
            "file_size": self.file_size,
            "file_hash": self.file_hash,
        }


@dataclass
class BookletInfo:
    """Information about a booklet."""

    booklet_number: int
    pdfs: list[PDFMetadata] = field(default_factory=list)
    total_pages: int = 0
    total_size: int = 0
    title: str = ""
    description: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "booklet_number": self.booklet_number,
            "title": self.title,
            "description": self.description,
            "total_pages": self.total_pages,
            "total_size": self.total_size,
            "pdf_count": len(self.pdfs),
            "pdfs": [pdf.to_dict() for pdf in self.pdfs],
        }


class PDFBinderOrganizer:
    """Organizes PDFs into structured booklets with metadata."""

    def __init__(self, source_directory: Path, output_directory: Path):
        self.source_dir = Path(source_directory).resolve()
        self.output_dir = Path(output_directory).resolve()
        self.pdfs: list[PDFMetadata] = []
        self.booklets: list[BookletInfo] = []

    def scan_directory(self) -> list[PDFMetadata]:
        """Recursively scan directory for all PDF files."""
        console.print("\n[bold cyan]🔍 PHASE 1: SCANNING DIRECTORY[/bold cyan]\n")

        pdf_files = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Finding PDF files...", total=None)

            # Recursive scan
            for pdf_path in self.source_dir.rglob("*.pdf"):
                pdf_files.append(pdf_path)
                progress.update(task, advance=1)

            progress.update(task, total=len(pdf_files))
            console.print(f"  [green]✅[/green] Found [bold]{len(pdf_files)}[/bold] PDF files\n")

        return pdf_files

    def extract_metadata(self, pdf_paths: list[Path]) -> list[PDFMetadata]:
        """Extract metadata from all PDF files."""
        console.print("\n[bold cyan]📋 PHASE 2: EXTRACTING METADATA[/bold cyan]\n")

        metadata_list = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Extracting metadata...", total=len(pdf_paths))

            for pdf_path in pdf_paths:
                try:
                    metadata = self._extract_single_metadata(pdf_path)
                    metadata_list.append(metadata)
                except Exception as e:
                    console.print(
                        f"  [yellow]⚠️[/yellow]  Error extracting metadata from {pdf_path.name}: {e}"
                    )

                progress.update(task, advance=1)

        # Sort by path for consistent ordering
        metadata_list.sort(key=lambda x: str(x.path))

        console.print(
            f"  [green]✅[/green] Extracted metadata from [bold]{len(metadata_list)}[/bold] PDFs\n"
        )

        return metadata_list

    def _extract_single_metadata(self, pdf_path: Path) -> PDFMetadata:
        """Extract metadata from a single PDF file."""
        try:
            reader = PdfReader(str(pdf_path))
            metadata = reader.metadata

            # Calculate file hash
            file_hash = hashlib.md5(pdf_path.read_bytes()).hexdigest()

            # Get relative path
            try:
                rel_path = pdf_path.relative_to(self.source_dir)
            except ValueError:
                rel_path = pdf_path

            # Extract metadata fields
            title = metadata.get("/Title", "") if metadata else ""
            if not title or title.strip() == "":
                title = pdf_path.stem.replace("_", " ").replace("-", " ").title()

            author = metadata.get("/Author", "") if metadata else None
            subject = metadata.get("/Subject", "") if metadata else None
            creator = metadata.get("/Creator", "") if metadata else None
            producer = metadata.get("/Producer", "") if metadata else None

            # Dates
            creation_date = metadata.get("/CreationDate", "") if metadata else None
            mod_date = metadata.get("/ModDate", "") if metadata else None

            return PDFMetadata(
                path=pdf_path,
                relative_path=str(rel_path),
                directory=str(rel_path.parent) if rel_path != pdf_path else "",
                title=title,
                author=author,
                subject=subject,
                creator=creator,
                producer=producer,
                creation_date=creation_date,
                modification_date=mod_date,
                page_count=len(reader.pages),
                file_size=pdf_path.stat().st_size,
                file_hash=file_hash,
            )
        except Exception:
            # Return minimal metadata on error
            return PDFMetadata(
                path=pdf_path,
                relative_path=str(pdf_path),
                title=pdf_path.stem,
                page_count=0,
                file_size=pdf_path.stat().st_size if pdf_path.exists() else 0,
                file_hash="",
            )

    def organize_into_booklets(self, pdfs: list[PDFMetadata]) -> list[BookletInfo]:
        """Organize PDFs into booklets (max 25 pages each)."""
        console.print("\n[bold cyan]📚 PHASE 3: ORGANIZING INTO BOOKLETS[/bold cyan]\n")

        booklets = []
        current_booklet = BookletInfo(booklet_number=1)
        current_pages = 0

        for pdf in pdfs:
            # Check if adding this PDF would exceed limit
            if current_pages + pdf.page_count > MAX_PAGES_PER_BOOKLET and current_booklet.pdfs:
                # Finalize current booklet
                current_booklet.total_pages = current_pages
                current_booklet.total_size = sum(p.file_size for p in current_booklet.pdfs)
                current_booklet.title = f"Booklet {current_booklet.booklet_number:03d}"
                current_booklet.description = (
                    f"Contains {len(current_booklet.pdfs)} PDFs, {current_pages} pages"
                )
                booklets.append(current_booklet)

                # Start new booklet
                current_booklet = BookletInfo(booklet_number=len(booklets) + 1)
                current_pages = 0

            # Add PDF to current booklet
            current_booklet.pdfs.append(pdf)
            current_pages += pdf.page_count

        # Add final booklet if it has content
        if current_booklet.pdfs:
            current_booklet.total_pages = current_pages
            current_booklet.total_size = sum(p.file_size for p in current_booklet.pdfs)
            current_booklet.title = f"Booklet {current_booklet.booklet_number:03d}"
            current_booklet.description = (
                f"Contains {len(current_booklet.pdfs)} PDFs, {current_pages} pages"
            )
            booklets.append(current_booklet)

        console.print(f"  [green]✅[/green] Organized into [bold]{len(booklets)}[/bold] booklets\n")

        # Show summary
        table = Table(title="Booklet Summary")
        table.add_column("Booklet", style="cyan")
        table.add_column("PDFs", justify="right")
        table.add_column("Pages", justify="right")
        table.add_column("Size", justify="right")

        for booklet in booklets:
            size_mb = booklet.total_size / (1024 * 1024)
            table.add_row(
                f"Booklet {booklet.booklet_number:03d}",
                str(len(booklet.pdfs)),
                str(booklet.total_pages),
                f"{size_mb:.2f} MB",
            )

        console.print(table)
        console.print()

        return booklets

    def create_booklets(self, booklets: list[BookletInfo]) -> list[Path]:
        """Create PDF booklets using WAFT's Binder system."""
        console.print("\n[bold cyan]📖 PHASE 4: CREATING BOOKLETS[/bold cyan]\n")

        booklet_paths = []
        metadata_dir = self.output_dir / "metadata"
        metadata_dir.mkdir(exist_ok=True)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Creating booklets...", total=len(booklets))

            for booklet in booklets:
                # Create binder
                binder = Binder(
                    title=booklet.title,
                    subtitle=booklet.description,
                    organization="PDF Binder Organizer",
                    date=datetime.now().strftime("%B %d, %Y"),
                    version="1.0",
                    compiled_by="WAFT PDF Organizer",
                    cover_style="professional",
                )

                # Add section for this booklet
                section = binder.add_section(
                    name="Documents",
                    description=f"{len(booklet.pdfs)} PDFs, {booklet.total_pages} pages",
                    color="#3498db",
                )

                # Add all PDFs to section
                for pdf_meta in booklet.pdfs:
                    doc_entry = DocumentEntry(
                        path=pdf_meta.path,
                        title=pdf_meta.title,
                        author=pdf_meta.author,
                        description=f"{pdf_meta.page_count} pages • {pdf_meta.relative_path}",
                    )
                    section.add_document(doc_entry)

                # Generate booklet
                booklet_path = self.output_dir / f"booklet_{booklet.booklet_number:03d}.pdf"
                binder.generate(booklet_path, include_dividers=True)
                booklet_paths.append(booklet_path)

                # Save metadata
                metadata_path = metadata_dir / f"booklet_{booklet.booklet_number:03d}_metadata.json"
                with open(metadata_path, "w") as f:
                    json.dump(booklet.to_dict(), f, indent=2)

                progress.update(task, advance=1)
                console.print(f"  [green]✅[/green] Created [bold]{booklet_path.name}[/bold]")

        console.print()
        return booklet_paths

    def create_full_binder(self, pdfs: list[PDFMetadata]) -> Path:
        """Create full binder with all PDFs."""
        console.print("\n[bold cyan]📚 PHASE 5: CREATING FULL BINDER[/bold cyan]\n")

        # Organize by directory
        by_directory: dict[str, list[PDFMetadata]] = {}
        for pdf in pdfs:
            dir_name = pdf.directory if pdf.directory else "Root"
            if dir_name not in by_directory:
                by_directory[dir_name] = []
            by_directory[dir_name].append(pdf)

        # Create binder
        total_pages = sum(p.page_count for p in pdfs)
        total_size = sum(p.file_size for p in pdfs)
        size_mb = total_size / (1024 * 1024)

        binder = Binder(
            title="FULL BINDER",
            subtitle=f"Complete Collection: {len(pdfs)} PDFs, {total_pages} pages, {size_mb:.2f} MB",
            organization="PDF Binder Organizer",
            date=datetime.now().strftime("%B %d, %Y"),
            version="1.0",
            compiled_by="WAFT PDF Organizer",
            cover_style="professional",
        )

        # Add sections by directory
        for dir_name, dir_pdfs in sorted(by_directory.items()):
            section = binder.add_section(
                name=dir_name if dir_name else "Root",
                description=f"{len(dir_pdfs)} PDFs",
                color="#2c3e50",
            )

            for pdf_meta in dir_pdfs:
                doc_entry = DocumentEntry(
                    path=pdf_meta.path,
                    title=pdf_meta.title,
                    author=pdf_meta.author,
                    description=f"{pdf_meta.page_count} pages • {pdf_meta.relative_path}",
                )
                section.add_document(doc_entry)

        # Generate full binder
        full_binder_path = self.output_dir / "FULL_BINDER.pdf"
        console.print("  [cyan]📄[/cyan] Generating full binder...")
        binder.generate(full_binder_path, include_dividers=True)

        size_mb = full_binder_path.stat().st_size / (1024 * 1024)
        console.print(
            f"  [green]✅[/green] Full binder created: [bold]{full_binder_path.name}[/bold]"
        )
        console.print(f"     Size: [bold]{size_mb:.2f} MB[/bold]")
        console.print()

        return full_binder_path

    def save_metadata(self, pdfs: list[PDFMetadata], booklets: list[BookletInfo]) -> Path:
        """Save comprehensive metadata to JSON."""
        console.print("\n[bold cyan]💾 PHASE 6: SAVING METADATA[/bold cyan]\n")

        metadata = {
            "source_directory": str(self.source_dir),
            "output_directory": str(self.output_dir),
            "generated": datetime.now().isoformat(),
            "total_pdfs": len(pdfs),
            "total_pages": sum(p.page_count for p in pdfs),
            "total_size": sum(p.file_size for p in pdfs),
            "booklet_count": len(booklets),
            "max_pages_per_booklet": MAX_PAGES_PER_BOOKLET,
            "pdfs": [pdf.to_dict() for pdf in pdfs],
            "booklets": [booklet.to_dict() for booklet in booklets],
        }

        metadata_path = self.output_dir / "metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        size_kb = metadata_path.stat().st_size / 1024
        console.print(f"  [green]✅[/green] Metadata saved: [bold]{metadata_path.name}[/bold]")
        console.print(f"     Size: [bold]{size_kb:.2f} KB[/bold]")
        console.print()

        return metadata_path

    def organize(self) -> dict[str, Any]:
        """Main organization workflow."""
        console.print("=" * 80)
        console.print("[bold]PDF Binder Organizer[/bold]")
        console.print("=" * 80)
        console.print()
        console.print(f"Source: [cyan]{self.source_dir}[/cyan]")
        console.print(f"Output: [cyan]{self.output_dir}[/cyan]")
        console.print()

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Phase 1: Scan
        pdf_paths = self.scan_directory()

        if not pdf_paths:
            console.print("[yellow]⚠️[/yellow]  No PDF files found in directory")
            return {}

        # Phase 2: Extract metadata
        pdfs = self.extract_metadata(pdf_paths)

        # Phase 3: Organize into booklets
        booklets = self.organize_into_booklets(pdfs)

        # Phase 4: Create booklets
        booklet_paths = self.create_booklets(booklets)

        # Phase 5: Create full binder
        full_binder_path = self.create_full_binder(pdfs)

        # Phase 6: Save metadata
        metadata_path = self.save_metadata(pdfs, booklets)

        # Summary
        console.print("\n[bold green]🎉 ORGANIZATION COMPLETE![/bold green]\n")

        summary_table = Table(title="Final Summary")
        summary_table.add_column("Item", style="cyan")
        summary_table.add_column("Count", justify="right")
        summary_table.add_column("Details", style="dim")

        summary_table.add_row(
            "PDFs Found", str(len(pdfs)), f"{sum(p.page_count for p in pdfs)} pages"
        )
        summary_table.add_row(
            "Booklets Created", str(len(booklets)), f"Max {MAX_PAGES_PER_BOOKLET} pages each"
        )
        summary_table.add_row("Full Binder", "1", "Complete collection")
        summary_table.add_row("Metadata Files", str(len(booklets) + 1), "JSON format")

        console.print(summary_table)
        console.print()
        console.print(f"[bold]Output directory:[/bold] [cyan]{self.output_dir}[/cyan]")
        console.print()

        return {
            "pdfs": pdfs,
            "booklets": booklets,
            "booklet_paths": booklet_paths,
            "full_binder_path": full_binder_path,
            "metadata_path": metadata_path,
        }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        console.print("[red]❌[/red] Error: Please provide a directory path")
        console.print()
        console.print("[bold]Usage:[/bold] python3 organize_pdfs.py <directory_path> [output_path]")
        console.print()
        console.print("[bold]Examples:[/bold]")
        console.print("  python3 organize_pdfs.py /path/to/documents")
        console.print("  python3 organize_pdfs.py /path/to/documents /path/to/output")
        console.print()
        console.print("[bold]Description:[/bold]")
        console.print("  Recursively scans directory for PDFs and organizes them into")
        console.print("  structured booklets (max 25 pages each) with a full binder.")
        sys.exit(1)

    source_dir = Path(sys.argv[1])

    if not source_dir.exists():
        console.print(f"[red]❌[/red] Error: Directory not found: {source_dir}")
        sys.exit(1)

    if not source_dir.is_dir():
        console.print(f"[red]❌[/red] Error: Not a directory: {source_dir}")
        sys.exit(1)

    # Output directory
    if len(sys.argv) >= 3:
        output_dir = Path(sys.argv[2])
    else:
        # Default: create in source directory
        output_dir = source_dir / f"PDF_BINDER_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Create organizer and run
    organizer = PDFBinderOrganizer(source_dir, output_dir)
    result = organizer.organize()

    if result:
        console.print("[bold green]✅ Success![/bold green]")
        console.print(f"Check output directory: [cyan]{output_dir}[/cyan]\n")
    else:
        console.print("[bold yellow]⚠️  No PDFs found to organize[/bold yellow]\n")


if __name__ == "__main__":
    main()
