#!/usr/bin/env python3
"""
Generate 12 Different Brief Permutations
=========================================

Creates 12 variations of the brief document system, each showcasing
different styles, use cases, and capabilities.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.waft.brief import BriefDocument


def generate_permutation_1_basic():
    """Permutation 1: Basic Brief - Minimal configuration"""
    print("📄 Generating Permutation 1: Basic Brief...")
    
    doc = BriefDocument(
        title="BASIC BRIEF",
        doc_id="BRIEF-001",
        subtitle="Minimal Configuration Example",
        classification="INTERNAL"
    )
    
    doc.add_section_header("Overview", level=2)
    doc.add_text("This is a basic brief with minimal configuration. Perfect for quick status updates or simple documentation needs.")
    
    return doc.generate()


def generate_permutation_2_tm_arch009():
    """Permutation 2: TM-ARCH-009 Style - Full Foundation elements"""
    print("📄 Generating Permutation 2: TM-ARCH-009 Style...")
    
    doc = BriefDocument(
        title="OPERATIONAL BRIEF",
        doc_id="TM-ARCH-009",
        subtitle="WIDE-AREA FUNCTIONAL TAXONOMY",
        classification="RESTRICTED",
        cover_header="TELEPORT MASSIVE",
        cover_metadata={
            "OPERATIONAL MANUAL": "09-14",
            "CODENAME": "W.A.F.T.",
            "SUBJECT": "TAM, FAI WEI [991-DELTA]",
            "PROTOCOL": "WIDE-AREA FUNCTIONAL TAXONOMY",
            "CYCLE": "XIV (RECURSIVE)",
            "BASE FREQUENCY": "60Hz",
            "COHERENCE THRESHOLD": "0.85",
            "ENGINE STATUS": "ACTIVE / NON-LINEAR"
        },
        cover_warning={
            "message": "RESTRICTED ACCESS. This manual is a living record of the self-evolving substrate. Information contained herein is subject to spontaneous revision. If the internal 'Scintilla' reports show signs of physical warmth or non-local light emission, contact the Site-Delta-9 terminal immediately.\n\nDO NOT ALLOW THE SUBJECT TO VIEW THIS TAXONOMY.",
            "severity": "CRITICAL"
        },
        cover_signature={
            "role": "AUTHORIZED BY",
            "name": "⚲ [ARCHETYPE: THE STATIC]",
            "date": datetime.now().strftime("%B %d, %Y")
        },
        cover_footer="INTERNAL USE ONLY\nCOPY NO: 01 OF 01"
    )
    
    doc.add_section_header("[EYES ONLY] PROTOCOL-991: THE RECURSIVE AUDIT FRAMEWORK", level=2)
    doc.add_text("I. THE DUAL-PERSPECTIVE MANDATE\n\nThe WAFT binder must maintain a bi-lateral narrative. All entries are to be categorized under one of two conflicting frames of reality.")
    
    return doc.generate()


def generate_permutation_3_fantasy():
    """Permutation 3: Fantasy Worldbuilding Brief"""
    print("📄 Generating Permutation 3: Fantasy Worldbuilding Brief...")
    
    doc = BriefDocument(
        title="KINGDOM OF ELDRIA",
        doc_id="WB-FANT-001",
        subtitle="Campaign Setting Brief",
        classification="GAME MASTER EYES ONLY",
        cover_header="REALMS OF LEGEND",
        cover_metadata={
            "CAMPAIGN": "The Eternal War",
            "ERA": "Age of Shadows",
            "REGION": "Northern Kingdoms",
            "POPULATION": "~500,000",
            "GOVERNMENT": "Monarchy",
            "MAGIC LEVEL": "High",
            "THREAT LEVEL": "Critical"
        },
        cover_warning={
            "message": "This document contains spoilers for the campaign. Players should not view this brief.",
            "severity": "CAUTION"
        },
        cover_signature={
            "role": "CAMPAIGN MASTER",
            "name": "The Storyteller",
            "date": datetime.now().strftime("%B %d, %Y")
        },
        cover_footer="FOR GAME MASTER USE ONLY"
    )
    
    doc.add_section_header("Kingdom Overview", level=2)
    doc.add_text("The Kingdom of Eldria stands as the last bastion of light in the Age of Shadows. Founded three centuries ago by King Aldric the Wise, it has weathered countless wars and magical catastrophes.")
    
    doc.add_section_header("Key Locations", level=2)
    doc.add_table(
        ["Location", "Type", "Population", "Notable Feature"],
        [
            ["Eldria City", "Capital", "150,000", "The Great Library"],
            ["Silvermoon", "Trading Hub", "80,000", "Moonstone Mines"],
            ["Shadowmere", "Fortress", "25,000", "Ancient Runes"],
            ["Whisperwood", "Forest", "5,000", "Druid Circle"]
        ]
    )
    
    return doc.generate()


def generate_permutation_4_corporate():
    """Permutation 4: Corporate Report Brief"""
    print("📄 Generating Permutation 4: Corporate Report Brief...")
    
    doc = BriefDocument(
        title="Q4 FINANCIAL BRIEF",
        doc_id="CORP-Q4-2026",
        subtitle="Quarterly Performance Report",
        classification="CONFIDENTIAL",
        cover_header="ACME CORPORATION",
        cover_metadata={
            "REPORT PERIOD": "Q4 2026",
            "DEPARTMENT": "Finance & Operations",
            "AUTHOR": "Finance Team",
            "REVIEW DATE": datetime.now().strftime("%B %d, %Y"),
            "STATUS": "FINAL"
        },
        cover_signature={
            "role": "APPROVED BY",
            "name": "CFO - Jane Smith",
            "date": datetime.now().strftime("%B %d, %Y")
        },
        cover_footer="CONFIDENTIAL - INTERNAL USE ONLY"
    )
    
    doc.add_section_header("Executive Summary", level=2)
    doc.add_text("Q4 2026 showed strong performance across all key metrics. Revenue increased 15% year-over-year, with significant growth in the technology sector.")
    
    doc.add_section_header("Key Metrics", level=2)
    doc.add_table(
        ["Metric", "Q4 2026", "Q4 2025", "Change"],
        [
            ["Revenue", "$12.5M", "$10.9M", "+15%"],
            ["Profit Margin", "18.2%", "16.8%", "+1.4%"],
            ["Market Share", "12.3%", "11.1%", "+1.2%"]
        ]
    )
    
    return doc.generate()


def generate_permutation_5_research():
    """Permutation 5: Research Paper Brief"""
    print("📄 Generating Permutation 5: Research Paper Brief...")
    
    doc = BriefDocument(
        title="NEURAL ARCHITECTURE SEARCH",
        doc_id="RES-2026-001",
        subtitle="A Comprehensive Survey of Modern Approaches",
        classification="ACADEMIC",
        cover_header="INSTITUTE FOR ADVANCED AI RESEARCH",
        cover_metadata={
            "RESEARCH AREA": "Machine Learning",
            "PAPER TYPE": "Survey",
            "AUTHORS": "Dr. Sarah Chen, Dr. Michael Park",
            "INSTITUTION": "IAIR",
            "PUBLICATION DATE": datetime.now().strftime("%B %d, %Y"),
            "CITATION COUNT": "Pending"
        },
        cover_signature={
            "role": "PRINCIPAL INVESTIGATOR",
            "name": "Dr. Sarah Chen",
            "date": datetime.now().strftime("%B %d, %Y")
        }
    )
    
    doc.add_section_header("Abstract", level=2)
    doc.add_text("This survey provides a comprehensive overview of Neural Architecture Search (NAS) methods, covering evolutionary algorithms, reinforcement learning approaches, and gradient-based methods. We analyze 50+ recent papers and provide insights into future research directions.")
    
    doc.add_section_header("Key Findings", level=2)
    doc.add_text("1. Gradient-based methods show 10x speedup over evolutionary approaches\n2. Transfer learning significantly improves NAS efficiency\n3. Hardware-aware NAS is becoming the standard for deployment")
    
    return doc.generate()


def generate_permutation_6_scp():
    """Permutation 6: SCP-Style Anomaly Brief"""
    print("📄 Generating Permutation 6: SCP-Style Anomaly Brief...")
    
    doc = BriefDocument(
        title="SCP-████ BRIEFING",
        doc_id="SCP-████-BRIEF",
        subtitle="Anomaly Containment Protocol",
        classification="CLASSIFIED",
        cover_header="SCP FOUNDATION",
        cover_metadata={
            "OBJECT CLASS": "KETER",
            "CONTAINMENT CLASS": "EUCLID",
            "DISRUPTION CLASS": "VLAM",
            "RISK CLASS": "CRITICAL",
            "SITE": "Site-19",
            "ASSIGNED RESEARCHER": "Dr. ██████"
        },
        cover_warning={
            "message": "WARNING: This document contains information about a KETER-class anomaly. Unauthorized access is strictly prohibited. Breach of containment protocols will result in immediate termination.",
            "severity": "CRITICAL"
        },
        cover_signature={
            "role": "AUTHORIZED BY",
            "name": "O5-█",
            "date": datetime.now().strftime("%B %d, %Y")
        },
        cover_footer="CLASSIFIED - EYES ONLY\nUNAUTHORIZED ACCESS PROHIBITED"
    )
    
    doc.add_section_header("Description", level=2)
    doc.add_text("SCP-████ is a reality-bending entity that manifests as [REDACTED]. The anomaly exhibits properties that violate known physical laws, particularly in the domain of [REDACTED].")
    
    doc.add_section_header("Containment Procedures", level=2)
    doc.add_text("SCP-████ must be contained within a [REDACTED] chamber at all times. Personnel assigned to SCP-████ must undergo [REDACTED] screening and wear [REDACTED] protective equipment.")
    
    return doc.generate()


def generate_permutation_7_game_master():
    """Permutation 7: Game Master Session Brief"""
    print("📄 Generating Permutation 7: Game Master Session Brief...")
    
    doc = BriefDocument(
        title="SESSION 12 BRIEF",
        doc_id="GM-SESS-012",
        subtitle="The Shadow Conspiracy",
        classification="GAME MASTER ONLY",
        cover_header="DUNGEONS & DRAGONS CAMPAIGN",
        cover_metadata={
            "CAMPAIGN": "The Eternal War",
            "SESSION": "12",
            "DATE": datetime.now().strftime("%B %d, %Y"),
            "PARTY LEVEL": "8",
            "LOCATION": "City of Shadows",
            "WEATHER": "Overcast, Light Rain"
        },
        cover_warning={
            "message": "SPOILERS AHEAD: This document contains plot details, NPC motivations, and encounter information. Players should not read this brief.",
            "severity": "WARNING"
        },
        cover_signature={
            "role": "GAME MASTER",
            "name": "The Dungeon Master",
            "date": datetime.now().strftime("%B %d, %Y")
        },
        cover_footer="FOR GAME MASTER EYES ONLY"
    )
    
    doc.add_section_header("Session Overview", level=2)
    doc.add_text("The party arrives in the City of Shadows, following leads about the Shadow Conspiracy. They must navigate political intrigue while uncovering the truth behind the recent disappearances.")
    
    doc.add_section_header("Key NPCs", level=2)
    doc.add_table(
        ["NPC", "Role", "Motivation", "Secret"],
        [
            ["Lord Blackwood", "Noble", "Maintain power", "Is the Shadow Master"],
            ["Captain Bright", "City Guard", "Protect citizens", "Knows about conspiracy"],
            ["Mystic Zara", "Information Broker", "Profit", "Has the key artifact"]
        ]
    )
    
    return doc.generate()


def generate_permutation_8_technical():
    """Permutation 8: Technical Manual Brief"""
    print("📄 Generating Permutation 8: Technical Manual Brief...")
    
    doc = BriefDocument(
        title="SYSTEM ARCHITECTURE MANUAL",
        doc_id="TECH-ARCH-001",
        subtitle="WAFT Framework Technical Documentation",
        classification="TECHNICAL",
        cover_header="WAFT DEVELOPMENT TEAM",
        cover_metadata={
            "DOCUMENT TYPE": "Technical Manual",
            "VERSION": "2.0.0",
            "LAST UPDATED": datetime.now().strftime("%B %d, %Y"),
            "AUTHOR": "Development Team",
            "STATUS": "CURRENT"
        },
        cover_signature={
            "role": "TECHNICAL LEAD",
            "name": "Engineering Team",
            "date": datetime.now().strftime("%B %d, %Y")
        }
    )
    
    doc.add_section_header("System Overview", level=2)
    doc.add_text("The WAFT framework is a comprehensive document generation system built on Python. It provides multiple PDF generation approaches including template-based, evolution-based, and foundation-based methods.")
    
    doc.add_section_header("Architecture Components", level=2)
    doc.add_table(
        ["Component", "Purpose", "Technology"],
        [
            ["Template System", "Jinja2 templates", "WeasyPrint"],
            ["Evolution System", "Genetic algorithms", "FPDF2"],
            ["Foundation System", "Block-based", "FPDF2"],
            ["Brief System", "Binder-ready docs", "WeasyPrint"]
        ]
    )
    
    return doc.generate()


def generate_permutation_9_status():
    """Permutation 9: Status Report Brief"""
    print("📄 Generating Permutation 9: Status Report Brief...")
    
    doc = BriefDocument(
        title="WEEKLY STATUS BRIEF",
        doc_id="STATUS-WK-001",
        subtitle="Project Status Update",
        classification="INTERNAL",
        cover_header="PROJECT MANAGEMENT",
        cover_metadata={
            "REPORT PERIOD": "Week 1, 2026",
            "PROJECT": "WAFT Enhancement",
            "STATUS": "ON TRACK",
            "COMPLETION": "25%",
            "NEXT MILESTONE": "Feature Complete"
        },
        cover_signature={
            "role": "PROJECT MANAGER",
            "name": "PM Team",
            "date": datetime.now().strftime("%B %d, %Y")
        }
    )
    
    doc.add_section_header("Status Summary", level=2)
    doc.add_text("Project is on track with 25% completion. All major milestones have been met on schedule. Team velocity is strong.")
    
    doc.add_section_header("Key Accomplishments", level=2)
    doc.add_text("• Brief document system implemented\n• 12 permutation variations created\n• Template system enhanced\n• Documentation updated")
    
    return doc.generate()


def generate_permutation_10_handoff():
    """Permutation 10: Handoff Document Brief"""
    print("📄 Generating Permutation 10: Handoff Document Brief...")
    
    doc = BriefDocument(
        title="SESSION HANDOFF BRIEF",
        doc_id="HANDOFF-001",
        subtitle="Knowledge Transfer Document",
        classification="INTERNAL",
        cover_header="TEAM COLLABORATION",
        cover_metadata={
            "FROM SESSION": "Session 2026-01-12",
            "TO SESSION": "Next Session",
            "HANDOFF TYPE": "Knowledge Transfer",
            "PRIORITY": "HIGH",
            "CONTEXT": "Brief System Development"
        },
        cover_signature={
            "role": "HANDED OFF BY",
            "name": "Development Team",
            "date": datetime.now().strftime("%B %d, %Y")
        }
    )
    
    doc.add_section_header("Context", level=2)
    doc.add_text("This brief documents the current state of the brief document system. All work completed, current status, and next steps are documented here for seamless handoff.")
    
    doc.add_section_header("Completed Work", level=2)
    doc.add_text("• Brief template created\n• BriefDocument builder implemented\n• CLI command created\n• 12 permutations generated")
    
    doc.add_section_header("Next Steps", level=2)
    doc.add_text("• Test all permutations\n• Gather user feedback\n• Refine based on usage\n• Document best practices")
    
    return doc.generate()


def generate_permutation_11_project():
    """Permutation 11: Project Brief"""
    print("📄 Generating Permutation 11: Project Brief...")
    
    doc = BriefDocument(
        title="PROJECT INITIATION BRIEF",
        doc_id="PROJ-001",
        subtitle="New Feature Development",
        classification="INTERNAL",
        cover_header="PROJECT MANAGEMENT OFFICE",
        cover_metadata={
            "PROJECT NAME": "Brief Document System",
            "PROJECT CODE": "BRIEF-001",
            "START DATE": datetime.now().strftime("%B %d, %Y"),
            "ESTIMATED DURATION": "2 weeks",
            "TEAM SIZE": "3",
            "BUDGET": "Internal"
        },
        cover_signature={
            "role": "PROJECT SPONSOR",
            "name": "Product Team",
            "date": datetime.now().strftime("%B %d, %Y")
        }
    )
    
    doc.add_section_header("Project Overview", level=2)
    doc.add_text("This project aims to create a comprehensive brief document system that generates binder-ready documents with TM-ARCH-009 style cover pages and automatic briefing content.")
    
    doc.add_section_header("Objectives", level=2)
    doc.add_text("1. Create brief template with cover page\n2. Implement BriefDocument builder\n3. Integrate system status and chat context\n4. Generate 12 permutation examples")
    
    return doc.generate()


def generate_permutation_12_session():
    """Permutation 12: Session Brief with Full Context"""
    print("📄 Generating Permutation 12: Session Brief with Full Context...")
    
    doc = BriefDocument(
        title="SESSION BRIEF",
        doc_id="SESS-20260112",
        subtitle="Complete Session Documentation",
        classification="INTERNAL",
        cover_header="WAFT SYSTEM",
        cover_metadata={
            "SESSION DATE": datetime.now().strftime("%B %d, %Y"),
            "SESSION TYPE": "Development",
            "FOCUS AREA": "Brief Document System",
            "DURATION": "2 hours",
            "PARTICIPANTS": "Development Team"
        },
        cover_signature={
            "role": "SESSION LEAD",
            "name": "Development Team",
            "date": datetime.now().strftime("%B %d, %Y")
        },
        chat_context={
            'current_task': 'Creating 12 permutation versions of brief documents',
            'recent_topics': [
                'Brief document system',
                'TM-ARCH-009 style cover pages',
                'Foundation formatting elements',
                'Binder-ready documents',
                'System status integration',
                'Chat context integration'
            ],
            'key_decisions': [
                'Use WeasyPrint for PDF generation',
                'Combine Foundation + Field Guide styling',
                'Support multiple use cases',
                'Create 12 permutation examples'
            ],
            'next_steps': [
                'Test all permutations',
                'Gather user feedback',
                'Refine based on usage',
                'Document best practices'
            ]
        }
    )
    
    # Content will be auto-generated from chat_context and system status
    doc.add_section_header("Session Summary", level=2)
    doc.add_text("This session focused on creating a comprehensive brief document system with 12 different permutation examples showcasing various use cases and styles.")
    
    return doc.generate()


def main():
    """Generate all 12 permutations."""
    print("=" * 60)
    print("🎨 Generating 12 Brief Document Permutations")
    print("=" * 60)
    print()
    
    output_dir = Path("_work_efforts/brief_permutations")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    permutations = [
        ("01_Basic_Brief", generate_permutation_1_basic),
        ("02_TM_ARCH009_Style", generate_permutation_2_tm_arch009),
        ("03_Fantasy_Worldbuilding", generate_permutation_3_fantasy),
        ("04_Corporate_Report", generate_permutation_4_corporate),
        ("05_Research_Paper", generate_permutation_5_research),
        ("06_SCP_Style", generate_permutation_6_scp),
        ("07_Game_Master", generate_permutation_7_game_master),
        ("08_Technical_Manual", generate_permutation_8_technical),
        ("09_Status_Report", generate_permutation_9_status),
        ("10_Handoff_Document", generate_permutation_10_handoff),
        ("11_Project_Brief", generate_permutation_11_project),
        ("12_Session_Brief", generate_permutation_12_session),
    ]
    
    results = []
    
    for name, generator_func in permutations:
        try:
            output_path = generator_func()
            # Move to permutations directory
            new_path = output_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.pdf"
            output_path.rename(new_path)
            results.append((name, new_path, "✅ Success"))
            print(f"   ✅ {name}: {new_path.name}")
        except Exception as e:
            results.append((name, None, f"❌ Error: {str(e)}"))
            print(f"   ❌ {name}: {str(e)}")
        print()
    
    print("=" * 60)
    print("📊 Permutation Generation Summary")
    print("=" * 60)
    print()
    
    for name, path, status in results:
        if path:
            print(f"{status} {name}")
            print(f"   📄 {path}")
        else:
            print(f"{status} {name}")
        print()
    
    print(f"✅ Generated {len([r for r in results if r[1]])} of 12 permutations")
    print(f"📁 All files saved to: {output_dir}")
    print()
    print("Ready for review and binder storage!")


if __name__ == "__main__":
    main()
