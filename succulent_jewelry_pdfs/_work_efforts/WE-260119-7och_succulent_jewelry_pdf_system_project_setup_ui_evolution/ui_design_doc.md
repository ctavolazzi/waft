# UI Design Document: Succulent Jewelry PDF Dashboard

**Date**: 2026-01-19  
**Work Effort**: WE-260119-7och  
**Status**: Design Phase

## What Was Observed in Chat

### Key Work Completed
1. **Complete PDF Generation System** - Built from scratch with templates, scripts, security, and validation
2. **Image API Integration** - Integrated Picsum and Pexels APIs for placeholder and real images
3. **Guide Generation** - Created "How to Cast Jewelry" guide with 10 images from Picsum
4. **Security & Validation** - Implemented path validation, input sanitization, PDF quality checks
5. **Project Structure** - Organized directory structure with templates, content, scripts, config
6. **Documentation** - Created comprehensive README, IMAGE_API_GUIDE, and implementation docs

### System Capabilities
- Generate professional PDF guides from markdown
- Batch processing support
- Gumroad preparation tools
- Image placeholder replacement
- Security-first design
- Quality validation

### Generated Content
- `how_to_cast_jewelry.pdf` (165KB) - Complete guide with images
- `test_guide.pdf` (194KB) - Test document
- HTML previews for quick viewing

## UI Purpose

Create a web dashboard that:
1. **Visualizes the System** - Shows what the PDF generation system can do
2. **Manages Generated PDFs** - Browse, preview, and manage generated guides
3. **Quick Actions** - Generate new PDFs, batch process, prepare for Gumroad
4. **System Status** - Show templates, scripts, configuration status
5. **Work Effort Integration** - Link to work efforts and track progress

## Goals

1. **User-Friendly Interface** - Make PDF generation accessible without CLI knowledge
2. **Visual Feedback** - Show generated PDFs, previews, stats
3. **Quick Workflow** - Streamline the guide creation process
4. **Project Context** - Show the bigger picture of the succulent jewelry project
5. **Evidence-Based** - Display case files and proof of decisions

## Key Features Needed

### 1. Dashboard Overview
- System status (templates, scripts, config)
- Recent PDFs generated
- Quick stats (total PDFs, total size, last generation)
- Work effort status

### 2. PDF Gallery
- Grid/list view of generated PDFs
- Preview thumbnails or first page
- Metadata (title, date, size, pages)
- Quick actions (view, download, delete, prepare for Gumroad)

### 3. Guide Generator
- Form to create new guide
- Content editor (markdown)
- Image placeholder helper
- Preview before generation
- Generate button

### 4. Templates Section
- List available templates (guide, poetry)
- Template previews
- Customization options

### 5. Configuration
- View/edit config files
- Image API settings (Picsum, Pexels)
- Gumroad metadata templates

### 6. Work Efforts Integration
- Link to current work effort
- Show improvement analysis
- Track progress

## Design Principles

1. **Clean & Simple** - Focus on content, not chrome
2. **Visual First** - Show PDFs, previews, images
3. **Action-Oriented** - Quick access to common tasks
4. **Context-Aware** - Show related information together
5. **Evidence-Based** - Display proof and case files

## Technical Requirements

- Single HTML file (standalone)
- No backend required (client-side only for now)
- Use existing generated files
- Link to scripts for actual generation
- Responsive design
- Fast loading

## Success Criteria

- User can see all generated PDFs at a glance
- User can understand system capabilities
- User can quickly generate a new guide
- User can see work effort progress
- UI reflects actual chat work completed
