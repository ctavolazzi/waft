# One-Shot Prompt: Create Teleport Massive Case File

Use this prompt in Cursor with a forked WAFT repository to recreate the entire Teleport Massive case file project.

---

## Prompt

I'm creating a comprehensive "case file" for a fictional corporation called "Teleport Massive Inc." that was founded in San Francisco on January 18, 2026. This case file will document their founding journey with multiple professional documents.

### Context & Lore

**Timeline:**
- 2008-09-10: LHC first beam circulation (real event, integrated as "the moment time was created")
- 2026-01-18: Teleport Massive Inc. incorporated in San Francisco (fictional)
- 2111: Scint Traversal discovered (86 years later, fictional)

**Company Mission:**
Teleport Massive was founded to scale quantum teleportation from laboratory demonstrations to real-world applications. The founding team was inspired by recent research showing quantum teleportation between distant superconducting chips (64m, 78.3% fidelity), over fiber networks with classical signals (30.2 km), and in thermal environments (4K). Their vision: systematically scale from particles → atoms → chips → devices → macroscopic objects.

**Founding Team (9 members):**
1. Justin Ross - Founder & CEO (quantum computing expert)
2. Abigail Wong - CFO (corporate finance)
3. Seth Jacobs - Head of Investor Relations (venture capital)
4. Luke Olson - COO (operations)
5. Jorge Simmons - Head of R&D (experimental physics)
6. Eva Beck - Lead Quantum Engineer (quantum systems)
7. Soham Murray - Head of Legal & Compliance (corporate law)
8. Heather Hopkins - Head of Marketing (brand development)
9. Calvin Rice - Head of Security (cybersecurity)

### Required Documents

Create the following documents in a work effort directory `_work_efforts/WE-260119-teleport_massive_case_file/`:

#### 1. Founding Team Data (JSON)
- File: `TELEPORT_MASSIVE_FOUNDING_TEAM_2026.json`
- Generate 9 team members using Random User API (https://randomuser.me/)
- Include: name, role, specialization, contribution, age, email, photo URLs
- Use seed 'teleport_massive_2026' for consistency
- Download photos to `founding_team_photos_2026/` directory

#### 2. Founding Team Report (Typst)
- File: `TELEPORT_MASSIVE_FOUNDING_TEAM_2026.typ`
- Use template: `@preview/s6t5-page-bordering:1.0.0`
- Include:
  - Executive summary (scaling quantum teleportation vision)
  - Founding story (Justin Ross's inspiration from research)
  - Individual profiles for all 9 members (photo, role, specialization, contribution, founding quote)
  - Research foundation section (summarizing 7 key papers)
  - Connection to 2111 discovery team
  - Comprehensive "Reference Guide for Future Readers" section at end:
    - Quick reference (key dates, metrics)
    - Timeline (2008 → 2026 → 2111)
    - Research paper citations
    - Glossary of key terms
    - Contact reference
    - Related documents
    - Key metrics & achievements
    - Future research directions

#### 3. Research Booklet Cover (Typst)
- File: `BOOKLET_COVER_2026.typ`
- Use template: `@preview/s6t5-page-bordering:1.0.0`
- Design: Dark blue header (#1a237e) with white text
- Title: "Teleport Massive - Founding Opportunity"
- Subtitle: "Seeking Founding Team & Seed Funding"
- Include:
  - Call-to-action: "We're Looking for the Initial Group - Help Us Get This Off the Ground"
  - Visual scaling pathway: Particles → Atoms → Chips → Devices → Macro (5 colored blocks)
  - Current state: "64m chip-to-chip teleportation | 78.3% fidelity"
  - "We're Looking For" section:
    - Founding Team Members: quantum physicists, business leaders, legal experts, marketing
    - Seed Funding: pre-seed/seed investors, deep tech VCs, strategic partners, angels
  - Footer: "Pre-Incorporation | January 2026 | Seeking Founding Team & Seed Funding"

#### 4. Mission Statement (Typst)
- File: `TELEPORT_MASSIVE_MISSION_STATEMENT_2026.typ`
- Use template: `@preview/s6t5-page-bordering:1.0.0`
- Include:
  - Mission: Scale quantum teleportation from mini to macro
  - Vision: Make distance irrelevant
  - Scientific foundation (4 key research findings)
  - Strategic approach (4 phases: 2026-2030, 2030-2050, 2050-2100, 2100+)
  - Core values: Safety First, Scientific Rigor, Systematic Progress, Global Impact
  - Research priorities: Entanglement Scaling, Fidelity Enhancement, Infrastructure Integration, Safety Protocols, Fundamental Physics

#### 5. Research Abstract (Typst)
- File: `RESEARCH_ABSTRACT_2026.typ`
- Use template: `@preview/s6t5-page-bordering:1.0.0`
- **Must be exactly 2 pages**
- Include:
  - Executive summary
  - 4 critical breakthroughs (grid layout):
    1. Chip-to-Chip (64m, 78.3% fidelity)
    2. Fiber Network (30.2 km, 72.3% fidelity)
    3. Thermal Resilience (4K, 59.9% fidelity)
    4. Fundamental Physics (black hole simulations)
  - Scaling pathway diagram (5-stage progression)
  - Performance analysis (fidelity vs. distance, infrastructure compatibility)
  - Technical enablers & strategic conclusions

#### 6. Founding Letter (Typst)
- File: `TELEPORT_MASSIVE_FOUNDING_LETTER_2026.typ`
- Use template: `@preview/letterloom:1.0.0`
- From: Justin Ross, Teleport Massive (Pre-Incorporation)
- To: Prospective Founding Team Members & Investors
- Date: January 15, 2026
- Subject: "Founding Opportunity: Scaling Quantum Teleportation from Mini to Macro"
- Content: Personal appeal, scientific foundation, call for team members and funding
- Signature: Justin Ross, Founder & Vision Lead

#### 7. Invoices (Typst)
- Use template: `@preview/invoice-pro:0.1.1`
- Format: DIN-5008-A
- Language: English

**Invoice 001** - `TELEPORT_MASSIVE_INVOICE_2026-001.typ`
- From: Quantum Research Labs, LLC, Menlo Park, CA
- To: Justin Ross, Teleport Massive (Pre-Incorporation)
- Date: January 10, 2026
- Invoice #: QR-2026-001
- Items:
  - Quantum Teleportation Research Analysis: 40 hrs @ $250/hr = $10,000
  - Literature Review (7 papers): 1 project @ $1,500 = $1,500
  - Scaling Feasibility Assessment: 1 report @ $2,000 = $2,000
  - Technical Architecture Consultation: 8 hrs @ $300/hr = $2,400
- Total: $15,900
- Payment: Net 30 days
- Include QR code for payment

**Invoice 002** - `TELEPORT_MASSIVE_INVOICE_2026-002.typ`
- From: Bay Area Legal Services, P.C., San Francisco, CA
- To: Justin Ross, Teleport Massive (Pre-Incorporation)
- Date: January 12, 2026
- Invoice #: BALS-2026-042
- Signed by: Soham Murray, Esq. (Partner, Corporate Law)
- Items:
  - Corporate Formation Consultation: 3 hrs @ $450/hr = $1,350
  - Delaware C-Corp Formation: 1 filing @ $2,500 = $2,500
  - California Foreign Qualification: 1 filing @ $800 = $800
  - Operating Agreement Drafting: 1 document @ $3,500 = $3,500
  - IP Assignment Agreements: 9 agreements @ $250 = $2,250
  - Regulatory Compliance Review: 2 hrs @ $450/hr = $900
- Total: $11,300
- Payment: Net 14 days
- Note: "Soham Murray will join Teleport Massive as Head of Legal & Compliance upon incorporation on January 18, 2026."
- Include QR code for payment

#### 8. Business Cards (Typst)
- Use template: `@preview/minimalbc:0.0.1`
- Create one card per team member in `founding_team_business_cards/` directory
- Format: Horizontal (flip: false), US size (geo_size: "us")
- Brand color: Dark blue (#1a237e) background
- Include for each:
  - Company: "Teleport Massive Inc."
  - Name: Full name
  - Role: From JSON data
  - Phone: +1 (415) 555-XXXX (unique 4-digit based on member ID)
  - Email: From JSON data
  - Website: "teleportmassive.com"

#### 9. Research Booklet Assembly
- File: `create_complete_research_booklet.py`
- Merge in order:
  1. Cover Page (compiled PDF)
  2. Mission Statement (compiled PDF)
  3. Research Abstract (compiled PDF)
  4. 7 research PDFs (if available in project root):
     - 0302114v1.pdf
     - 2502.10253v2.pdf
     - 2503.10761v1.pdf
     - 2404.10738v4.pdf
     - 2508.14691v2.pdf
     - 2406.05182v1.pdf
     - 2302.08756v1.pdf
- Output: `QUANTUM_TELEPORTATION_RESEARCH_FOUNDATION_COMPLETE_2026.pdf`

#### 10. Complete Case File Assembly
- File: `create_teleport_massive_case_file.py`
- Merge in order:
  1. Founding Letter
  2. Invoice 2026-001
  3. Invoice 2026-002
  4. Cover Page
  5. Mission Statement
  6. Research Abstract
  7. Complete Research Booklet
  8. Founding Team Document
  9. All 9 Business Cards
- Output: `TELEPORT_MASSIVE_CASE_FILE_2026.pdf`

### Technical Requirements

1. **Python Scripts Needed:**
   - `generate_founding_team_2026.py` - Generate team JSON from Random User API
   - `create_founding_team_business_cards.py` - Generate business card Typst files from JSON
   - `compile_business_cards.py` - Compile all business cards to PDF
   - `create_complete_research_booklet.py` - Assemble research booklet
   - `create_teleport_massive_case_file.py` - Assemble final case file

2. **Dependencies:**
   - `pypdf` for PDF merging
   - `subprocess` for Typst compilation
   - `json` for data handling
   - `pathlib` for file operations
   - `requests` or `urllib` for API calls (Random User API)

3. **Typst Packages:**
   - `@preview/s6t5-page-bordering:1.0.0`
   - `@preview/letterloom:1.0.0`
   - `@preview/invoice-pro:0.1.1`
   - `@preview/minimalbc:0.0.1`

4. **Key Details:**
   - All dates: January 2026
   - Company location: San Francisco, California
   - Brand color: #1a237e (dark blue)
   - Currency: USD ($) - use `#raw("$")` in Typst
   - IBAN format: Use valid European format (e.g., DE89370400440532013000) for invoice template compatibility

### Expected Output

Final case file: `TELEPORT_MASSIVE_CASE_FILE_2026.pdf` (~138 pages)
- Professional, cohesive document collection
- Tells the story of Teleport Massive's founding
- Includes all documentation: letter, invoices, reports, research, business cards
- Ready for printing or digital distribution

### Workflow

1. Create work effort directory structure
2. Generate founding team JSON data
3. Download team photos
4. Create all Typst documents
5. Compile all Typst files to PDF
6. Generate business cards from JSON
7. Compile business cards
8. Assemble research booklet
9. Assemble complete case file
10. Open final PDF for review

### Notes

- Use consistent branding across all documents
- Ensure all dates align with January 2026 timeline
- Make sure research abstract is exactly 2 pages (adjust font sizes/spacing as needed)
- Business cards should use consistent phone number format
- Invoices need valid IBAN format for template compatibility
- All documents should reference the same research foundation papers

---

**Start by creating the work effort directory and generating the founding team JSON data, then proceed through each document systematically.**
