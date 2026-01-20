#!/usr/bin/env python3
"""
Teleport Massive Template Booklet Generator
===========================================

Generates a comprehensive booklet showcasing all Teleport Massive templates.
Creates multiple example documents demonstrating different template types and use cases.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

console = Console()

# Output directory
OUTPUT_DIR = project_root / "_work_efforts" / "teleport_massive_booklet"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_tm_report_example() -> Path:
    """Generate a TELEPORT MASSIVE report example."""
    from src.waft.templates.tm_report import generate_tm_report

    content = """
    <h2>Quarterly Operations Review</h2>
    
    <p>This report summarizes Q4 2025 operations across all TELEPORT MASSIVE facilities. 
    Key metrics, incidents, and strategic initiatives are documented below.</p>
    
    <h3>Facility Status</h3>
    <table>
        <caption>Active Facilities</caption>
        <thead>
            <tr>
                <th>Facility</th>
                <th>Location</th>
                <th>Status</th>
                <th>Capacity</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Site-Delta-9</td>
                <td>Nevada, USA</td>
                <td>Operational</td>
                <td>85%</td>
            </tr>
            <tr>
                <td>Site-Alpha-3</td>
                <td>Tokyo, Japan</td>
                <td>Operational</td>
                <td>92%</td>
            </tr>
            <tr>
                <td>Site-Beta-7</td>
                <td>London, UK</td>
                <td>Maintenance</td>
                <td>0%</td>
            </tr>
        </tbody>
    </table>
    
    <h3>Key Metrics</h3>
    <ul>
        <li>Total Transfers: 12,847 (↑ 15% from Q3)</li>
        <li>Success Rate: 99.7% (↑ 0.2%)</li>
        <li>Average Transfer Time: 3.2 seconds (↓ 0.4s)</li>
        <li>Incidents: 2 (both resolved within 24 hours)</li>
    </ul>
    
    <div class="recommendation">
        <div class="recommendation-title">Recommendation</div>
        <p>Increase capacity at Site-Delta-9 to meet growing demand. Consider 
        expanding Site-Beta-7 capabilities during scheduled maintenance window.</p>
    </div>
    
    <h3>Strategic Initiatives</h3>
    <p>Q4 saw the launch of three major initiatives:</p>
    <ol>
        <li><strong>Quantum Entanglement Network:</strong> Expanded to 12 new cities</li>
        <li><strong>Organoid Computing Integration:</strong> Reduced processing time by 40%</li>
        <li><strong>Safety Protocol Enhancement:</strong> Zero critical incidents this quarter</li>
    </ol>
    """

    output_path = OUTPUT_DIR / "01_tm_report_example.pdf"

    generate_tm_report(
        title="Q4 2025 Operations Review",
        content=content,
        output_path=output_path,
        doc_id="TM-RPT-2025-Q4",
        classification="INTERNAL USE ONLY",
        tagline="Making the Impossible, Inevitable™",
        date=datetime.now().strftime("%B %d, %Y"),
        author="Dr. Sarah Chen",
        department="Operations",
        distribution="Executive Team, Facility Directors",
        summary="<p>Q4 operations exceeded expectations with 99.7% success rate and 15% growth in transfer volume. All facilities operational with minor maintenance scheduled for Site-Beta-7.</p>",
        signatures=[
            {
                "name": "Dr. Sarah Chen",
                "title": "Chief Operations Officer",
                "date": datetime.now().strftime("%Y-%m-%d"),
            },
            {
                "name": "Marcus Rodriguez",
                "title": "Director of Facilities",
                "date": datetime.now().strftime("%Y-%m-%d"),
            },
        ],
    )

    return output_path


def generate_tm_brief_example() -> Path:
    """Generate a TELEPORT MASSIVE brief example."""
    from src.waft.brief import BriefDocument

    doc = BriefDocument(
        title="Incident Report: Site-Delta-9 Anomaly",
        doc_id="TM-BRIEF-2026-001",
        subtitle="Quantum Fluctuation Event Analysis",
        classification="CONFIDENTIAL",
        cover_header="TELEPORT MASSIVE",
        cover_metadata={
            "OPERATIONAL MANUAL": "09-14",
            "CODENAME": "W.A.F.T.",
            "FACILITY": "Site-Delta-9",
        },
        cover_warning={
            "message": "QUANTUM FLUCTUATION DETECTED - IMMEDIATE REVIEW REQUIRED",
            "severity": "HIGH",
        },
        cover_signature={
            "role": "Chief Science Officer",
            "name": "Dr. Elena Vasquez",
            "date": datetime.now().strftime("%Y-%m-%d"),
        },
        cover_footer="PROPERTY OF TELEPORT MASSIVE // SITE-DELTA-9",
    )

    doc.add_section_header("Incident Summary", level=2)
    doc.add_text(
        "On January 13, 2026 at 02:16 PST, Site-Delta-9 detected an anomalous quantum fluctuation during routine transfer operation TM-TX-8472."
    )

    doc.add_status_box(
        "Status",
        "Incident resolved. No personnel injuries. Transfer completed successfully after 3.2 second delay.",
    )

    doc.add_section_header("Technical Details", level=2)
    doc.add_text(
        "The fluctuation registered at 0.847 standard deviations above baseline, triggering automatic safety protocols. The system successfully compensated within 2.1 seconds."
    )

    doc.add_table(
        headers=["Metric", "Baseline", "Anomaly", "Resolution"],
        rows=[
            ["Quantum Coherence", "0.999", "0.847", "0.998"],
            ["Transfer Time", "3.0s", "6.2s", "3.2s"],
            ["Energy Variance", "±0.1%", "+2.3%", "±0.05%"],
            ["Safety Margin", "95%", "78%", "97%"],
        ],
    )

    doc.add_section_header("Root Cause Analysis", level=2)
    doc.add_text(
        "Preliminary analysis indicates localized quantum field interference from external source. Investigation ongoing."
    )

    doc.add_note(
        "Action Required",
        "Schedule full facility diagnostic scan. Review quantum field monitoring protocols. Update safety thresholds if necessary.",
    )

    doc.add_section_header("Recommendations", level=2)
    doc.add_text("1. Increase monitoring frequency for Site-Delta-9 quantum field stability")
    doc.add_text("2. Implement enhanced filtering for external interference")
    doc.add_text("3. Review and update safety protocol thresholds")

    output_path = doc.generate(OUTPUT_DIR / "02_tm_brief_example.pdf")
    return output_path


def generate_tm_invoice_example() -> Path:
    """Generate a TELEPORT MASSIVE invoice example."""
    from src.waft.templates.tm_report import generate_tm_report

    content = """
    <h2>Service Invoice</h2>
    
    <div class="doc-meta" style="margin-bottom: 0.3in;">
        <strong>Invoice Number:</strong> TM-INV-2026-001<br>
        <strong>Date:</strong> January 13, 2026<br>
        <strong>Client:</strong> Acme Corporation<br>
        <strong>Account Manager:</strong> James Mitchell
    </div>
    
    <h3>Services Rendered</h3>
    <table>
        <caption>Teleportation Services</caption>
        <thead>
            <tr>
                <th>Service</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Standard Transfer (0-100km)</td>
                <td>5</td>
                <td>$12,000</td>
                <td>$60,000</td>
            </tr>
            <tr>
                <td>Long-Range Transfer (100-1000km)</td>
                <td>3</td>
                <td>$28,000</td>
                <td>$84,000</td>
            </tr>
            <tr>
                <td>Intercontinental Transfer</td>
                <td>2</td>
                <td>$45,000</td>
                <td>$90,000</td>
            </tr>
            <tr>
                <td>Quantum Insurance</td>
                <td>10</td>
                <td>$1,500</td>
                <td>$15,000</td>
            </tr>
            <tr>
                <td>Medical Standby</td>
                <td>8 hours</td>
                <td>$1,200/hour</td>
                <td>$9,600</td>
            </tr>
            <tr>
                <td>Organoid Computing Time</td>
                <td>12 hours</td>
                <td>$850/hour</td>
                <td>$10,200</td>
            </tr>
        </tbody>
    </table>
    
    <div style="margin-top: 0.3in; text-align: right;">
        <p><strong>Subtotal:</strong> $268,800</p>
        <p><strong>Tax (8.5%):</strong> $22,848</p>
        <p style="font-size: 14pt; margin-top: 0.2in;"><strong>Total Due: $291,648</strong></p>
    </div>
    
    <div class="recommendation" style="margin-top: 0.4in;">
        <div class="recommendation-title">Payment Terms</div>
        <p>Payment due within 30 days. Late payments subject to 2% monthly interest. 
        All services subject to TELEPORT MASSIVE standard terms and conditions. 
        Not responsible for spontaneous duplication events.</p>
    </div>
    """

    output_path = OUTPUT_DIR / "03_tm_invoice_example.pdf"

    generate_tm_report(
        title="Service Invoice",
        content=content,
        output_path=output_path,
        doc_id="TM-INV-2026-001",
        classification="CONFIDENTIAL",
        tagline="Making the Impossible, Inevitable™",
        date=datetime.now().strftime("%B %d, %Y"),
        department="Billing & Finance",
    )

    return output_path


def generate_tm_memo_example() -> Path:
    """Generate a TELEPORT MASSIVE personal memo example."""
    from src.waft.templates.personal_memo import generate_personal_memo

    content = """
    <h2>Internal Memo</h2>
    
    <p><strong>To:</strong> All Site-Delta-9 Personnel<br>
    <strong>From:</strong> Dr. Elena Vasquez, Chief Science Officer<br>
    <strong>Date:</strong> January 13, 2026<br>
    <strong>Subject:</strong> Updated Safety Protocols</p>
    
    <p>Effective immediately, all personnel must adhere to the following updated safety protocols:</p>
    
    <h3>1. Quantum Field Monitoring</h3>
    <p>All transfers must now include real-time quantum field stability monitoring. 
    Any fluctuation above 0.5 standard deviations requires immediate protocol suspension.</p>
    
    <h3>2. Personal Protective Equipment</h3>
    <p>Enhanced quantum-resistant suits are now mandatory for all transfer operations. 
    Standard issue equipment has been upgraded and is available from Facilities.</p>
    
    <h3>3. Incident Reporting</h3>
    <p>All anomalies, no matter how minor, must be reported within 15 minutes via 
    the new incident reporting system (IRIS).</p>
    
    <p>These protocols are in response to recent quantum fluctuation events and are 
    designed to ensure the safety of all personnel and clients.</p>
    
    <p>Questions or concerns should be directed to the Safety Office.</p>
    
    <p style="margin-top: 0.4in;">— Dr. Elena Vasquez</p>
    """

    output_path = OUTPUT_DIR / "04_tm_memo_example.pdf"

    generate_personal_memo(
        content=content,
        output_path=output_path,
        from_name="Dr. Elena Vasquez",
        from_title="Chief Science Officer",
        date=datetime.now().strftime("%B %d, %Y"),
        subject="Updated Safety Protocols",
    )

    return output_path


def generate_tm_technical_spec_example() -> Path:
    """Generate a TELEPORT MASSIVE technical specification example."""
    from src.waft.templates.tm_report import generate_tm_report

    content = """
    <h2>Technical Specification: Quantum Entanglement Array v3.2</h2>
    
    <div class="summary">
        <div class="summary-title">Overview</div>
        <p>The Quantum Entanglement Array (QEA) v3.2 represents a significant advancement 
        in teleportation technology, featuring improved stability, reduced energy consumption, 
        and enhanced safety protocols.</p>
    </div>
    
    <h3>Specifications</h3>
    <table>
        <caption>Technical Parameters</caption>
        <thead>
            <tr>
                <th>Parameter</th>
                <th>Value</th>
                <th>Notes</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Maximum Range</td>
                <td>10,000 km</td>
                <td>Single hop, no relay required</td>
            </tr>
            <tr>
                <td>Transfer Time</td>
                <td>2.8-3.5 seconds</td>
                <td>Dependent on distance and payload</td>
            </tr>
            <tr>
                <td>Payload Capacity</td>
                <td>500 kg</td>
                <td>Standard configuration</td>
            </tr>
            <tr>
                <td>Energy Consumption</td>
                <td>850 kW</td>
                <td>Per transfer, average</td>
            </tr>
            <tr>
                <td>Quantum Coherence</td>
                <td>99.8%</td>
                <td>Minimum threshold</td>
            </tr>
            <tr>
                <td>Safety Margin</td>
                <td>97%</td>
                <td>Above industry standard</td>
            </tr>
        </tbody>
    </table>
    
    <h3>Key Improvements</h3>
    <ul>
        <li><strong>Enhanced Stability:</strong> 40% reduction in quantum fluctuations</li>
        <li><strong>Energy Efficiency:</strong> 25% lower power consumption vs. v3.1</li>
        <li><strong>Safety Protocols:</strong> Real-time monitoring and automatic shutdown</li>
        <li><strong>Reliability:</strong> 99.7% success rate in field testing</li>
    </ul>
    
    <h3>Installation Requirements</h3>
    <p>QEA v3.2 requires:</p>
    <ol>
        <li>Minimum 200m² facility space</li>
        <li>Dedicated 1MW power supply</li>
        <li>Quantum field isolation chamber</li>
        <li>Certified installation team (TM-certified only)</li>
    </ol>
    
    <div class="recommendation">
        <div class="recommendation-title">Deployment Schedule</div>
        <p>Rollout scheduled for Q2 2026. All existing facilities will be upgraded 
        during scheduled maintenance windows. New installations can begin immediately.</p>
    </div>
    """

    output_path = OUTPUT_DIR / "05_tm_technical_spec_example.pdf"

    generate_tm_report(
        title="Technical Specification: QEA v3.2",
        content=content,
        output_path=output_path,
        doc_id="TM-SPEC-QEA-3.2",
        classification="PROPRIETARY",
        tagline="Making the Impossible, Inevitable™",
        date=datetime.now().strftime("%B %d, %Y"),
        author="Engineering Division",
        department="Research & Development",
        summary="<p>QEA v3.2 technical specification document outlining capabilities, improvements, and deployment requirements for the latest quantum entanglement array.</p>",
    )

    return output_path


def generate_tm_incident_report_example() -> Path:
    """Generate a TELEPORT MASSIVE incident report example."""
    from src.waft.templates.tm_report import generate_tm_report

    content = """
    <h2>Incident Report: Transfer Anomaly TM-TX-8472</h2>
    
    <div class="summary">
        <div class="summary-title">Executive Summary</div>
        <p>On January 13, 2026 at 02:16 PST, transfer operation TM-TX-8472 experienced 
        a quantum fluctuation anomaly. The transfer completed successfully with a 3.2 
        second delay. No personnel injuries or property damage occurred.</p>
    </div>
    
    <h3>Incident Details</h3>
    <div class="doc-meta">
        <strong>Incident ID:</strong> INC-2026-001<br>
        <strong>Date/Time:</strong> January 13, 2026, 02:16:21 PST<br>
        <strong>Location:</strong> Site-Delta-9, Transfer Bay 3<br>
        <strong>Transfer ID:</strong> TM-TX-8472<br>
        <strong>Severity:</strong> LOW<br>
        <strong>Status:</strong> RESOLVED
    </div>
    
    <h3>Sequence of Events</h3>
    <ol>
        <li><strong>02:16:15</strong> - Transfer initiated, standard protocol</li>
        <li><strong>02:16:18</strong> - Quantum field fluctuation detected (0.847σ)</li>
        <li><strong>02:16:19</strong> - Automatic safety protocols engaged</li>
        <li><strong>02:16:20</strong> - System compensation initiated</li>
        <li><strong>02:16:21</strong> - Transfer completed successfully</li>
    </ol>
    
    <h3>Root Cause Analysis</h3>
    <p>Preliminary investigation indicates localized quantum field interference from 
    an external source. Full diagnostic scan scheduled for January 15, 2026.</p>
    
    <h3>Response Actions</h3>
    <ul>
        <li>Immediate: Safety protocols automatically engaged, transfer completed</li>
        <li>Short-term: Enhanced monitoring activated for Site-Delta-9</li>
        <li>Long-term: Full facility diagnostic scheduled</li>
    </ul>
    
    <h3>Preventive Measures</h3>
    <div class="recommendation">
        <div class="recommendation-title">Recommendations</div>
        <ol>
            <li>Increase quantum field monitoring frequency</li>
            <li>Review external interference sources in facility vicinity</li>
            <li>Update safety protocol thresholds based on findings</li>
            <li>Conduct staff training on new monitoring procedures</li>
        </ol>
    </div>
    
    <h3>Personnel Involved</h3>
    <table>
        <caption>Response Team</caption>
        <thead>
            <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Dr. Elena Vasquez</td>
                <td>Chief Science Officer</td>
                <td>Incident commander, analysis</td>
            </tr>
            <tr>
                <td>Marcus Rodriguez</td>
                <td>Facility Director</td>
                <td>Safety protocol oversight</td>
            </tr>
            <tr>
                <td>James Mitchell</td>
                <td>Transfer Operator</td>
                <td>System monitoring, completion</td>
            </tr>
        </tbody>
    </table>
    """

    output_path = OUTPUT_DIR / "06_tm_incident_report_example.pdf"

    generate_tm_report(
        title="Incident Report: Transfer Anomaly",
        content=content,
        output_path=output_path,
        doc_id="TM-INC-2026-001",
        classification="INTERNAL USE ONLY",
        tagline="Making the Impossible, Inevitable™",
        date=datetime.now().strftime("%B %d, %Y"),
        author="Dr. Elena Vasquez",
        department="Safety & Operations",
        signatures=[
            {
                "name": "Dr. Elena Vasquez",
                "title": "Chief Science Officer",
                "date": datetime.now().strftime("%Y-%m-%d"),
            }
        ],
    )

    return output_path


def generate_booklet_index() -> Path:
    """Generate the booklet index/cover page."""
    from src.waft.templates.tm_report import generate_tm_report

    content = """
    <h2>TELEPORT MASSIVE Template Booklet</h2>
    
    <div class="summary">
        <div class="summary-title">Overview</div>
        <p>This booklet contains examples of all available TELEPORT MASSIVE document templates. 
        Each template demonstrates different use cases, formatting options, and document types 
        for corporate documentation, reports, invoices, and internal communications.</p>
    </div>
    
    <h3>Template Catalog</h3>
    
    <table>
        <caption>Available Templates</caption>
        <thead>
            <tr>
                <th>#</th>
                <th>Template Name</th>
                <th>Document Type</th>
                <th>Use Case</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>01</td>
                <td>TM Report</td>
                <td>Corporate Report</td>
                <td>Quarterly reviews, operational reports, strategic documents</td>
            </tr>
            <tr>
                <td>02</td>
                <td>TM Brief</td>
                <td>Briefing Document</td>
                <td>Incident reports, status briefs, executive summaries</td>
            </tr>
            <tr>
                <td>03</td>
                <td>TM Invoice</td>
                <td>Billing Document</td>
                <td>Service invoices, billing statements, payment tracking</td>
            </tr>
            <tr>
                <td>04</td>
                <td>TM Memo</td>
                <td>Internal Communication</td>
                <td>Staff memos, policy updates, internal announcements</td>
            </tr>
            <tr>
                <td>05</td>
                <td>TM Technical Spec</td>
                <td>Technical Documentation</td>
                <td>Specifications, technical documentation, engineering reports</td>
            </tr>
            <tr>
                <td>06</td>
                <td>TM Incident Report</td>
                <td>Incident Documentation</td>
                <td>Safety incidents, anomaly reports, investigation documents</td>
            </tr>
        </tbody>
    </table>
    
    <h3>Template Features</h3>
    <ul>
        <li><strong>Professional Branding:</strong> Consistent TELEPORT MASSIVE visual identity</li>
        <li><strong>Security Classifications:</strong> Support for various classification levels</li>
        <li><strong>Flexible Formatting:</strong> Tables, lists, summaries, recommendations</li>
        <li><strong>Signature Blocks:</strong> Multiple signature support for approvals</li>
        <li><strong>Metadata Support:</strong> Document IDs, dates, authors, departments</li>
    </ul>
    
    <h3>Usage Guidelines</h3>
    <p>All templates follow TELEPORT MASSIVE corporate standards:</p>
    <ol>
        <li>Use appropriate classification levels (INTERNAL, CONFIDENTIAL, PROPRIETARY)</li>
        <li>Include required metadata (doc ID, date, author, department)</li>
        <li>Follow document structure guidelines for consistency</li>
        <li>Ensure all signatures are obtained before distribution</li>
    </ol>
    
    <div class="recommendation">
        <div class="recommendation-title">Document Generation</div>
        <p>All templates can be generated programmatically using the WAFT template system. 
        See source code examples in <code>src/waft/templates/</code> for implementation details.</p>
    </div>
    
    <h3>Contact</h3>
    <p>For questions about template usage or customization, contact the Documentation Office 
    or refer to the WAFT template documentation.</p>
    
    <p style="margin-top: 0.4in; font-size: 9pt; color: #666;">
    <strong>Generated:</strong> {date}<br>
    <strong>Version:</strong> 1.0<br>
    <strong>Classification:</strong> INTERNAL USE ONLY
    </p>
    """.format(date=datetime.now().strftime("%B %d, %Y"))

    output_path = OUTPUT_DIR / "00_tm_booklet_index.pdf"

    generate_tm_report(
        title="TELEPORT MASSIVE Template Booklet",
        content=content,
        output_path=output_path,
        doc_id="TM-BOOKLET-001",
        classification="INTERNAL USE ONLY",
        tagline="Making the Impossible, Inevitable™",
        date=datetime.now().strftime("%B %d, %Y"),
        department="Documentation Office",
        summary="<p>Comprehensive template booklet showcasing all available TELEPORT MASSIVE document templates with examples and usage guidelines.</p>",
    )

    return output_path


def main():
    """Generate the complete Teleport Massive template booklet."""
    console.print("\n" + "=" * 70)
    console.print(
        Panel.fit(
            "[bold cyan]TELEPORT MASSIVE Template Booklet Generator[/bold cyan]",
            border_style="cyan",
        )
    )
    console.print("=" * 70)
    console.print(f"\n📁 Output directory: {OUTPUT_DIR}")
    console.print(f"📅 Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")

    generated_files = []

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            # Generate index
            task1 = progress.add_task("Generating booklet index...", total=1)
            index_path = generate_booklet_index()
            generated_files.append(index_path)
            progress.update(task1, completed=1)
            console.print(f"  ✅ Generated: {index_path.name}")

            # Generate report example
            task2 = progress.add_task("Generating TM Report example...", total=1)
            report_path = generate_tm_report_example()
            generated_files.append(report_path)
            progress.update(task2, completed=1)
            console.print(f"  ✅ Generated: {report_path.name}")

            # Generate brief example
            task3 = progress.add_task("Generating TM Brief example...", total=1)
            brief_path = generate_tm_brief_example()
            generated_files.append(brief_path)
            progress.update(task3, completed=1)
            console.print(f"  ✅ Generated: {brief_path.name}")

            # Generate invoice example
            task4 = progress.add_task("Generating TM Invoice example...", total=1)
            invoice_path = generate_tm_invoice_example()
            generated_files.append(invoice_path)
            progress.update(task4, completed=1)
            console.print(f"  ✅ Generated: {invoice_path.name}")

            # Generate memo example
            task5 = progress.add_task("Generating TM Memo example...", total=1)
            memo_path = generate_tm_memo_example()
            generated_files.append(memo_path)
            progress.update(task5, completed=1)
            console.print(f"  ✅ Generated: {memo_path.name}")

            # Generate technical spec example
            task6 = progress.add_task("Generating TM Technical Spec example...", total=1)
            spec_path = generate_tm_technical_spec_example()
            generated_files.append(spec_path)
            progress.update(task6, completed=1)
            console.print(f"  ✅ Generated: {spec_path.name}")

            # Generate incident report example
            task7 = progress.add_task("Generating TM Incident Report example...", total=1)
            incident_path = generate_tm_incident_report_example()
            generated_files.append(incident_path)
            progress.update(task7, completed=1)
            console.print(f"  ✅ Generated: {incident_path.name}")

        console.print("\n" + "=" * 70)
        console.print(
            Panel.fit(
                "[bold green]✅ BOOKLET GENERATION COMPLETE![/bold green]", border_style="green"
            )
        )
        console.print("=" * 70)
        console.print(f"\n📚 Generated {len(generated_files)} PDF documents")
        console.print(f"📁 Location: {OUTPUT_DIR.absolute()}\n")
        console.print("📋 Documents created:")
        for i, pdf_file in enumerate(sorted(generated_files), 1):
            size_kb = pdf_file.stat().st_size / 1024
            console.print(f"   {i:2d}. {pdf_file.name:40s} ({size_kb:6.1f} KB)")
        console.print("\n🎉 Enjoy your Teleport Massive template booklet!\n")

        return 0

    except Exception as e:
        console.print(f"\n[bold red]❌ Error generating booklet:[/bold red] {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
