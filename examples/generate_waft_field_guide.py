#!/usr/bin/env python3
"""
WAFT Field Guide Booklet Generator

Generates a three-tiered field guide explaining WAFT at progressively
deeper technical levels:
- Level 1: Layman's Guide (FG-001)
- Level 2: Professional Guide (FG-002)
- Level 3: ML AI Scientist Guide (FG-003)

Uses the field_guide DocumentConfig preset with military field manual aesthetic.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.waft.foundation_v2 import (
        DocumentEngine,
        DocumentConfig,
        CoverPage,
        MetadataRail,
        SectionHeader,
        TextBlock,
        KeyValueBlock,
        RuleBlock,
        TableBlock,
        WarningBlock,
        SignatureBlock,
        LogBlock,
    )

    print("=" * 80)
    print("WAFT FIELD GUIDE BOOKLET GENERATOR")
    print("=" * 80)
    print("\nGenerating three-tiered field guide system...\n")

    # Output directory
    output_dir = project_root / "_work_efforts" / "showcase_documents"
    output_dir.mkdir(parents=True, exist_ok=True)

    # =================================================================
    # LEVEL 1: LAYMAN'S GUIDE (FG-001)
    # =================================================================
    print("\n" + "=" * 80)
    print("GENERATING LEVEL 1: LAYMAN'S GUIDE (FG-001)")
    print("=" * 80)

    config_l1 = DocumentConfig.field_guide(
        field_guide_number="FG-001",
        classification="PUBLIC - INTRODUCTORY MATERIAL"
    )

    engine_l1 = DocumentEngine(config_l1)

    print("\n  → Building Level 1 content...")

    # Cover Page
    engine_l1.add(CoverPage(
        institution="WAFT FIELD OPERATIONS",
        division="Introductory Training Division",
        document_type="FIELD GUIDE",
        document_number="FG-001",
        classification="LEVEL 1: LAYMAN'S GUIDE",
    ))

    # Introduction
    engine_l1.add(SectionHeader("What is WAFT?", level=1))

    engine_l1.add(TextBlock(
        "WAFT (Workflow Augmentation Framework Tool) is a system that helps AI agents "
        "document themselves, evolve, and learn. Think of it as giving AI a laboratory "
        "notebook that writes itself."
    ))

    engine_l1.add(RuleBlock(thickness=0.5, width_percent=80))

    # The Big Picture
    engine_l1.add(SectionHeader("The Big Picture: Why This Matters", level=1))

    engine_l1.add(TextBlock(
        "Imagine you're watching evolution happen in real-time, but instead of animals, "
        "it's AI agents. WAFT provides three essential tools:"
    ))

    engine_l1.add(TextBlock(
        "1. SUBSTRATE: The environment where agents live and work\n"
        "2. PHYSICS: The rules that govern how agents behave and evolve\n"
        "3. FLIGHT RECORDER: A system that records everything that happens"
    ))

    engine_l1.add(WarningBlock(
        "IMPORTANT: WAFT agents are experimental. Always supervise their operations "
        "and review their outputs before using them in production systems.",
        severity="WARNING"
    ))

    # Simple Analogies
    engine_l1.add(SectionHeader("Understanding Through Analogies", level=1))

    engine_l1.add(SectionHeader("Code as DNA", level=2))
    engine_l1.add(TextBlock(
        "Just like living organisms have DNA that can mutate and evolve, WAFT treats "
        "code as genetic material. Each AI agent has a 'genome' that can change, "
        "improve, and adapt over time."
    ))

    engine_l1.add(SectionHeader("Self-Documentation Loop", level=2))
    engine_l1.add(TextBlock(
        "Imagine a scientist who takes notes on their own experiments, then reads those "
        "notes to improve the next experiment, then takes notes on that, and so on. "
        "WAFT creates this recursive loop of self-observation and improvement."
    ))

    engine_l1.add(SectionHeader("The Gamification System", level=2))
    engine_l1.add(TextBlock(
        "WAFT uses Dungeons & Dragons-style progression to track agent development. "
        "Agents gain XP (experience points) and Insight as they work, level up, and "
        "develop unique characteristics."
    ))

    # Equipment Checklist
    engine_l1.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l1.add(SectionHeader("Equipment Checklist: What You Need", level=1))

    engine_l1.add(KeyValueBlock(
        label="Required Software",
        data={
            "Python": "3.10 or higher",
            "uv": "Package manager (recommended)",
            "Git": "For version control",
            "Text Editor": "VS Code, Cursor, or similar",
        }
    ))

    engine_l1.add(KeyValueBlock(
        label="Optional Tools",
        data={
            "Obsidian": "For viewing markdown documentation",
            "Docker": "For containerized deployments",
            "Just": "Task runner for common operations",
        }
    ))

    # Quick Start
    engine_l1.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l1.add(SectionHeader("Quick Start: Your First WAFT Project", level=1))

    engine_l1.add(TextBlock(
        "Follow these steps to get started with WAFT:"
    ))

    engine_l1.add(LogBlock([
        "# Step 1: Clone the repository",
        "git clone https://github.com/ctavolazzi/waft.git",
        "cd waft",
        "",
        "# Step 2: Install dependencies",
        "uv sync",
        "",
        "# Step 3: Run the demo",
        "python demo.py",
        "",
        "# Step 4: Explore the documentation",
        "ls _pyrite/  # Check the knowledge base",
    ]))

    # Common Questions
    engine_l1.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l1.add(SectionHeader("Common Questions", level=1))

    engine_l1.add(TableBlock(
        headers=["Question", "Answer"],
        rows=[
            ["Is WAFT production-ready?", "Experimental - use with supervision"],
            ["What AI models does it support?", "Primarily Claude, but extensible"],
            ["Can I use it for my project?", "Yes - MIT licensed"],
            ["How long to learn?", "Basics: 1 hour, Mastery: weeks"],
            ["Is it safe?", "Yes, with proper supervision"],
        ]
    ))

    # Safety Warnings
    engine_l1.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l1.add(SectionHeader("Safety Warnings", level=1))

    engine_l1.add(WarningBlock(
        "EXPERIMENTAL SYSTEM: WAFT is research-grade software. Do not use in "
        "production systems without thorough testing and validation.",
        severity="CRITICAL"
    ))

    engine_l1.add(WarningBlock(
        "AI AGENTS: These agents can modify code and generate files. Always review "
        "their outputs before committing or deploying changes.",
        severity="WARNING"
    ))

    engine_l1.add(WarningBlock(
        "DATA PRIVACY: WAFT may send data to external APIs (like Claude). Be careful "
        "with sensitive information.",
        severity="CAUTION"
    ))

    # Next Steps
    engine_l1.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l1.add(SectionHeader("Next Steps", level=1))

    engine_l1.add(TextBlock(
        "Ready to dive deeper? Continue to:"
    ))

    engine_l1.add(TextBlock(
        "• FIELD GUIDE FG-002: Professional's Guide (technical architecture)\n"
        "• FIELD GUIDE FG-003: ML AI Scientist's Guide (research methodology)\n"
        "• _pyrite/active/: Current work and active documentation\n"
        "• README.md: Project overview and setup instructions"
    ))

    # Signature
    engine_l1.add(RuleBlock(thickness=0.3, width_percent=50))
    engine_l1.add(SignatureBlock(
        role="Field Guide Author",
        name="WAFT Documentation Team",
        timestamp=datetime.now(),
    ))

    # Render Level 1
    print("  → Rendering Level 1 PDF...")
    output_l1 = output_dir / "WAFT_Field_Guide_Layman.pdf"
    engine_l1.render(output_l1)
    print(f"  ✓ Level 1 complete: {output_l1}")

    # =================================================================
    # LEVEL 2: PROFESSIONAL'S GUIDE (FG-002)
    # =================================================================
    print("\n" + "=" * 80)
    print("GENERATING LEVEL 2: PROFESSIONAL'S GUIDE (FG-002)")
    print("=" * 80)

    config_l2 = DocumentConfig.field_guide(
        field_guide_number="FG-002",
        classification="INTERNAL USE - TECHNICAL REFERENCE"
    )

    engine_l2 = DocumentEngine(config_l2)

    print("\n  → Building Level 2 content...")

    # Cover Page
    engine_l2.add(CoverPage(
        institution="WAFT FIELD OPERATIONS",
        division="Technical Operations Division",
        document_type="FIELD GUIDE",
        document_number="FG-002",
        classification="LEVEL 2: PROFESSIONAL'S GUIDE",
    ))

    # Architecture Overview
    engine_l2.add(SectionHeader("Architecture Overview", level=1))

    engine_l2.add(TextBlock(
        "WAFT is built on a modular architecture with clear separation of concerns. "
        "The system consists of core components, agent systems, and documentation "
        "infrastructure."
    ))

    engine_l2.add(TableBlock(
        headers=["Component", "Purpose", "Location"],
        rows=[
            ["Foundation", "PDF generation engine", "src/waft/foundation_v2.py"],
            ["Templates", "Document templates", "src/waft/templates/"],
            ["Agents", "CrewAI integration", "src/agents.py"],
            ["_pyrite", "Knowledge management", "_pyrite/"],
            ["_work_efforts", "Active work tracking", "_work_efforts/"],
        ]
    ))

    # Core Components
    engine_l2.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l2.add(SectionHeader("Core Components", level=1))

    engine_l2.add(SectionHeader("DocumentEngine", level=2))
    engine_l2.add(TextBlock(
        "The DocumentEngine is the heart of WAFT's PDF generation system. It manages "
        "content blocks, handles layout, and supports multiple document presets."
    ))

    engine_l2.add(LogBlock([
        "from src.waft.foundation_v2 import DocumentEngine, DocumentConfig",
        "",
        "# Create engine with field guide preset",
        "config = DocumentConfig.field_guide('FG-001')",
        "engine = DocumentEngine(config)",
        "",
        "# Add content blocks",
        "engine.add(SectionHeader('Title', level=1))",
        "engine.add(TextBlock('Content here'))",
        "",
        "# Render to PDF",
        "engine.render(Path('output.pdf'))",
    ]))

    engine_l2.add(SectionHeader("Content Blocks", level=2))
    engine_l2.add(TextBlock(
        "WAFT provides 10+ content block types for different purposes:"
    ))

    engine_l2.add(TableBlock(
        headers=["Block Type", "Purpose", "Example Use"],
        rows=[
            ["SectionHeader", "Hierarchical headers", "Chapter titles"],
            ["TextBlock", "Body text", "Paragraphs"],
            ["KeyValueBlock", "Metadata pairs", "Specifications"],
            ["TableBlock", "Tabular data", "Results, comparisons"],
            ["LogBlock", "Code/terminal output", "Command examples"],
            ["WarningBlock", "Important notices", "Safety warnings"],
            ["CoverPage", "Document covers", "Title pages"],
            ["MetadataRail", "Styled info boxes", "Subject data"],
            ["RuleBlock", "Visual separation", "Section dividers"],
            ["SignatureBlock", "Authorization", "Approvals"],
        ]
    ))

    # API Reference
    engine_l2.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l2.add(SectionHeader("API Reference", level=1))

    engine_l2.add(TextBlock(
        "WAFT provides a simple, consistent API for all document operations."
    ))

    engine_l2.add(SectionHeader("Creating Documents", level=2))
    engine_l2.add(LogBlock([
        "# Available presets",
        "DocumentConfig.clinical_standard()  # Professional scientific",
        "DocumentConfig.field_guide()        # Military field manual",
        "DocumentConfig.classified_dossier() # SCP/typewriter style",
        "DocumentConfig.scientific_journal() # Academic journal",
    ]))

    engine_l2.add(SectionHeader("Adding Content", level=2))
    engine_l2.add(LogBlock([
        "# Text content",
        "engine.add(TextBlock('Your text here'))",
        "",
        "# Headers",
        "engine.add(SectionHeader('Title', level=1))",
        "",
        "# Tables",
        "engine.add(TableBlock(",
        "    headers=['Col1', 'Col2'],",
        "    rows=[['A', 'B'], ['C', 'D']]",
        "))",
        "",
        "# Warnings",
        "engine.add(WarningBlock('Alert!', severity='WARNING'))",
    ]))

    # Integration Patterns
    engine_l2.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l2.add(SectionHeader("Integration Patterns", level=1))

    engine_l2.add(TextBlock(
        "WAFT integrates with multiple systems and frameworks:"
    ))

    engine_l2.add(KeyValueBlock(
        label="Integration Points",
        data={
            "CrewAI": "Agent orchestration framework",
            "Obsidian": "Markdown documentation viewer",
            "Git": "Version control and branching",
            "uv": "Fast Python package management",
            "Just": "Task runner for common operations",
        }
    ))

    # Best Practices
    engine_l2.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l2.add(SectionHeader("Best Practices", level=1))

    engine_l2.add(SectionHeader("Document Organization", level=2))
    engine_l2.add(TextBlock(
        "1. Use _pyrite/ for knowledge management (active, backlog, standards)\n"
        "2. Use _work_efforts/ for active work and session tracking\n"
        "3. Generate PDFs for formal documentation\n"
        "4. Keep markdown for living documentation"
    ))

    engine_l2.add(SectionHeader("Code Quality", level=2))
    engine_l2.add(TextBlock(
        "1. Use type hints throughout (100% coverage)\n"
        "2. Write docstrings for all public APIs\n"
        "3. Follow PEP 8 style guidelines\n"
        "4. Test with adversarial validation"
    ))

    # Troubleshooting
    engine_l2.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l2.add(SectionHeader("Troubleshooting", level=1))

    engine_l2.add(TableBlock(
        headers=["Issue", "Cause", "Solution"],
        rows=[
            ["PDF not rendering", "Missing fpdf2", "uv sync or pip install fpdf2"],
            ["Import errors", "Wrong directory", "Run from project root"],
            ["Font errors", "Missing fonts", "Use built-in fonts only"],
            ["Layout issues", "Too much content", "Add page breaks manually"],
        ]
    ))

    # Performance Considerations
    engine_l2.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l2.add(SectionHeader("Performance Considerations", level=1))

    engine_l2.add(TextBlock(
        "WAFT is optimized for document generation performance:"
    ))

    engine_l2.add(KeyValueBlock(
        data={
            "PDF Generation": "~100ms for 10-page document",
            "Memory Usage": "Minimal (fpdf2 is efficient)",
            "Dependencies": "Only fpdf2 required",
            "File Size": "Optimized for print (vector graphics)",
        }
    ))

    # Signature
    engine_l2.add(RuleBlock(thickness=0.3, width_percent=50))
    engine_l2.add(SignatureBlock(
        role="Technical Documentation Lead",
        name="WAFT Documentation Team",
        timestamp=datetime.now(),
    ))

    # Render Level 2
    print("  → Rendering Level 2 PDF...")
    output_l2 = output_dir / "WAFT_Field_Guide_Professional.pdf"
    engine_l2.render(output_l2)
    print(f"  ✓ Level 2 complete: {output_l2}")

    # =================================================================
    # LEVEL 3: ML AI SCIENTIST'S GUIDE (FG-003)
    # =================================================================
    print("\n" + "=" * 80)
    print("GENERATING LEVEL 3: ML AI SCIENTIST'S GUIDE (FG-003)")
    print("=" * 80)

    config_l3 = DocumentConfig.field_guide(
        field_guide_number="FG-003",
        classification="RESEARCH USE - ADVANCED METHODOLOGY"
    )

    engine_l3 = DocumentEngine(config_l3)

    print("\n  → Building Level 3 content...")

    # Cover Page
    engine_l3.add(CoverPage(
        institution="WAFT RESEARCH DIVISION",
        division="Machine Learning & AI Science",
        document_type="FIELD GUIDE",
        document_number="FG-003",
        classification="LEVEL 3: ML AI SCIENTIST'S GUIDE",
    ))

    # Evolutionary Theory
    engine_l3.add(SectionHeader("Evolutionary Theory in WAFT", level=1))

    engine_l3.add(TextBlock(
        "WAFT implements computational evolution based on genetic algorithms and "
        "natural selection principles. Each agent is treated as an evolving organism "
        "with a genome that can mutate, reproduce, and adapt to selective pressures."
    ))

    engine_l3.add(SectionHeader("Theoretical Foundation", level=2))
    engine_l3.add(TextBlock(
        "The system is built on three pillars that mirror biological evolution:"
    ))

    engine_l3.add(KeyValueBlock(
        label="Evolutionary Pillars",
        data={
            "Substrate": "The computational environment (analogous to habitat)",
            "Physics": "Rules of selection and fitness (evolutionary pressures)",
            "Flight Recorder": "Telemetry and lineage tracking (fossil record)",
        }
    ))

    # Fitness Function Design
    engine_l3.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l3.add(SectionHeader("Fitness Function Design", level=1))

    engine_l3.add(TextBlock(
        "Fitness functions determine which agents survive and reproduce. WAFT supports "
        "multiple fitness metrics:"
    ))

    engine_l3.add(TableBlock(
        headers=["Metric", "Type", "Range", "Interpretation"],
        rows=[
            ["Task Success", "Binary", "0-1", "Did agent complete task?"],
            ["Code Quality", "Continuous", "0-100", "Quality score"],
            ["Efficiency", "Continuous", "0-1", "Resource utilization"],
            ["Novelty", "Continuous", "0-1", "Innovation measure"],
            ["Robustness", "Continuous", "0-1", "Error handling"],
        ]
    ))

    engine_l3.add(SectionHeader("Custom Fitness Functions", level=2))
    engine_l3.add(LogBlock([
        "from src.waft.core.physics import FitnessFunction",
        "",
        "class CustomFitness(FitnessFunction):",
        "    def evaluate(self, agent, environment):",
        "        # Your evaluation logic",
        "        score = self.measure_performance(agent)",
        "        penalty = self.measure_violations(agent)",
        "        return score - penalty",
    ]))

    # Mutation Strategies
    engine_l3.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l3.add(SectionHeader("Mutation Strategies", level=1))

    engine_l3.add(TextBlock(
        "WAFT supports multiple mutation operators:"
    ))

    engine_l3.add(TableBlock(
        headers=["Strategy", "Effect", "Use Case"],
        rows=[
            ["Point Mutation", "Small code changes", "Parameter tuning"],
            ["Insertion", "Add new code", "Feature addition"],
            ["Deletion", "Remove code", "Simplification"],
            ["Crossover", "Combine agents", "Hybrid solutions"],
            ["Duplication", "Copy code segments", "Amplification"],
        ]
    ))

    # Selection Mechanisms
    engine_l3.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l3.add(SectionHeader("Selection Mechanisms", level=1))

    engine_l3.add(TextBlock(
        "WAFT implements multiple selection algorithms:"
    ))

    engine_l3.add(KeyValueBlock(
        data={
            "Tournament Selection": "Local competition between agents",
            "Roulette Selection": "Probability proportional to fitness",
            "Rank Selection": "Based on relative ranking",
            "Elitism": "Always preserve best performers",
        }
    ))

    # Phylogenetic Analysis
    engine_l3.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l3.add(SectionHeader("Phylogenetic Analysis", level=1))

    engine_l3.add(TextBlock(
        "The Flight Recorder system tracks complete agent lineages, enabling "
        "phylogenetic analysis of evolutionary trajectories."
    ))

    engine_l3.add(SectionHeader("Genome ID System", level=2))
    engine_l3.add(TextBlock(
        "Each agent receives a unique genome ID encoding its lineage:"
    ))

    engine_l3.add(LogBlock([
        "# Genome ID format:",
        "SUBSTRATE-GEN{generation}-AGENT{id}-PARENT{parent_id}",
        "",
        "# Example:",
        "SUBSTRATE-GEN003-AGENT042-PARENT017",
        "",
        "# This tells us:",
        "# - Generation 3 (third iteration)",
        "# - Agent 42 in this generation",
        "# - Descended from Agent 17",
    ]))

    # Experimental Protocols
    engine_l3.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l3.add(SectionHeader("Experimental Protocols", level=1))

    engine_l3.add(TextBlock(
        "WAFT supports rigorous scientific experimentation:"
    ))

    engine_l3.add(SectionHeader("Protocol Design", level=2))
    engine_l3.add(TextBlock(
        "1. Define hypothesis and research questions\n"
        "2. Design fitness function for selective pressure\n"
        "3. Set population size and generation count\n"
        "4. Configure mutation rates and operators\n"
        "5. Establish baseline and control conditions\n"
        "6. Run experiments with multiple replicates\n"
        "7. Analyze results with statistical rigor"
    ))

    # Data Collection Methods
    engine_l3.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l3.add(SectionHeader("Data Collection Methods", level=1))

    engine_l3.add(TextBlock(
        "The Flight Recorder captures comprehensive telemetry:"
    ))

    engine_l3.add(TableBlock(
        headers=["Data Type", "Frequency", "Storage Format"],
        rows=[
            ["Fitness scores", "Per evaluation", "JSON"],
            ["Genome changes", "Per mutation", "Git diff"],
            ["Performance metrics", "Per task", "Time series"],
            ["Error logs", "On failure", "Structured logs"],
            ["Lineage trees", "Per generation", "Graph format"],
        ]
    ))

    # Publication Standards
    engine_l3.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l3.add(SectionHeader("Publication Standards", level=1))

    engine_l3.add(TextBlock(
        "WAFT generates publication-ready data and documentation:"
    ))

    engine_l3.add(KeyValueBlock(
        label="Output Standards",
        data={
            "Data Format": "CSV, JSON for reproducibility",
            "Visualization": "Vector graphics (PDF, SVG)",
            "Documentation": "Automated markdown generation",
            "Version Control": "Git-based lineage tracking",
            "Reproducibility": "Seed-based deterministic runs",
        }
    ))

    engine_l3.add(WarningBlock(
        "RESEARCH INTEGRITY: Always document experimental conditions, maintain "
        "proper controls, and report negative results. WAFT facilitates but does "
        "not guarantee scientific rigor.",
        severity="CRITICAL"
    ))

    # Advanced Topics
    engine_l3.add(RuleBlock(thickness=0.5, width_percent=80))
    engine_l3.add(SectionHeader("Advanced Topics", level=1))

    engine_l3.add(SectionHeader("Co-evolution", level=2))
    engine_l3.add(TextBlock(
        "Multiple agent populations can evolve simultaneously with interdependencies."
    ))

    engine_l3.add(SectionHeader("Fitness Landscape Analysis", level=2))
    engine_l3.add(TextBlock(
        "Visualize and analyze the topology of fitness landscapes to understand "
        "evolutionary dynamics."
    ))

    engine_l3.add(SectionHeader("Speciation Events", level=2))
    engine_l3.add(TextBlock(
        "Track when populations diverge into distinct behavioral phenotypes."
    ))

    # Signature
    engine_l3.add(RuleBlock(thickness=0.3, width_percent=50))
    engine_l3.add(SignatureBlock(
        role="Principal Research Scientist",
        name="WAFT Research Division",
        timestamp=datetime.now(),
    ))

    # Render Level 3
    print("  → Rendering Level 3 PDF...")
    output_l3 = output_dir / "WAFT_Field_Guide_Scientist.pdf"
    engine_l3.render(output_l3)
    print(f"  ✓ Level 3 complete: {output_l3}")

    # =================================================================
    # SUMMARY
    # =================================================================
    print("\n" + "=" * 80)
    print("GENERATION COMPLETE")
    print("=" * 80)
    print("\nGenerated files:")
    print(f"  • {output_l1}")
    print(f"  • {output_l2}")
    print(f"  • {output_l3}")

    print("\nTotal file sizes:")
    print(f"  • Level 1: {output_l1.stat().st_size / 1024:.1f} KB")
    print(f"  • Level 2: {output_l2.stat().st_size / 1024:.1f} KB")
    print(f"  • Level 3: {output_l3.stat().st_size / 1024:.1f} KB")

    print("\nNext steps:")
    print("  1. Review generated PDFs for accuracy")
    print("  2. Create binder to combine all three into one booklet")
    print("  3. Add table of contents and section dividers")
    print("  4. Generate final WAFT_Field_Guide_Complete_Booklet.pdf")

    print("\n" + "=" * 80)

except ImportError as e:
    print("\n" + "=" * 80)
    print("DEPENDENCY ERROR")
    print("=" * 80)
    print(f"\nError: {e}")
    print("\nThis script requires WAFT Foundation V2.")
    print("Install dependencies: uv sync")
    print("\n" + "=" * 80)
    sys.exit(1)

except Exception as e:
    print("\n" + "=" * 80)
    print("ERROR DURING GENERATION")
    print("=" * 80)
    print(f"\nError: {e}")
    print("\nDebug information:")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 80)
    sys.exit(1)
