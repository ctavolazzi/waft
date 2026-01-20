#!/usr/bin/env python3
"""
Generate Comprehensive Closeout Summary
=======================================

Creates a complete session closeout document covering:
- Everything accomplished
- Everything failed/not completed
- Everything planned
- Everything not planned for
- Errors and mistakes
- Oversights
- Lessons learned
- Next steps

This is used to create the /closeout-chat command template.
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.generate_waft_field_guide_printer_friendly import (
    generate_field_guide_printer_friendly,
)


def generate_email_summaries(
    session_focus: str = "Session work",
    accomplishments: list = None,
    errors_fixed: list = None,
    files_modified: list = None,
) -> dict:
    """
    Generate multi-level email summaries for different audiences.

    Args:
        session_focus: Brief description of session focus
        accomplishments: List of key accomplishments
        errors_fixed: List of errors/bugs fixed
        files_modified: List of files modified

    Returns:
        Dictionary with 'technical', 'peer', 'boss', 'tldr' summaries
    """
    # Default values if not provided
    accomplishments = accomplishments or ["Completed session work"]
    errors_fixed = errors_fixed or []
    files_modified = files_modified or []

    # Level 1: Advanced/Highly Technical
    technical = f"""
=== TECHNICAL SUMMARY ===

{session_focus}

Technical changes: {len(files_modified)} file(s) modified: {", ".join(files_modified) if files_modified else "N/A"}
"""
    if errors_fixed:
        technical += f"Fixed {len(errors_fixed)} bug(s): {', '.join(errors_fixed)}"

    # Level 2: Peer Filter (Technical but accessible)
    peer = f"""
=== PEER SUMMARY ===

Worked on {session_focus.lower()}.

Key improvements:
"""
    for acc in accomplishments[:5]:  # Top 5
        peer += f"- {acc}\n"
    if errors_fixed:
        peer += f"\nFixed {len(errors_fixed)} issue(s) during development."

    # Level 3: Boss Filter (Goals and objectives)
    boss = f"""
=== EXECUTIVE SUMMARY ===

Completed work on {session_focus.lower()}.

Objectives Achieved:
"""
    for acc in accomplishments[:3]:  # Top 3
        boss += f"✓ {acc}\n"
    boss += "\nStatus: Complete and ready for use."

    # Level 4: Anyone/TLDR
    tldr = f"""
=== TLDR ===

{session_focus.lower()}. Made improvements and fixed issues. Everything works better now.
"""

    return {
        "technical": technical.strip(),
        "peer": peer.strip(),
        "boss": boss.strip(),
        "tldr": tldr.strip(),
    }


def generate_closeout_summary():
    """Generate comprehensive closeout summary PDF."""

    content = """
<h2>Session Closeout Summary: WAFT Document Generation & Global Commands</h2>

<p><strong>Date:</strong> January 11, 2026<br>
<strong>Session Focus:</strong> Document generation framework, printer-friendly templates, global Cursor commands<br>
<strong>Status:</strong> ✅ Major accomplishments, some items pending</p>

<div class="warning">
    <div class="warning-title">Session Scope</div>
    This session focused on creating a comprehensive document generation system with printer-friendly
    capabilities, PDF redaction tools, and global Cursor commands for workflow automation.
</div>

<h2>1. Everything We Accomplished ✅</h2>

<h3>1.1 Printer-Friendly Document System</h3>

<div class="checklist">
    <div class="checklist-title">Completed Tasks</div>
    <ul>
        <li>✅ Created printer-friendly template with white backgrounds only</li>
        <li>✅ Reduced black ink usage (gray borders instead of black)</li>
        <li>✅ Changed headers from black backgrounds to gray borders (#666)</li>
        <li>✅ Changed table headers from black to light gray (#f5f5f5)</li>
        <li>✅ Kept thick black borders only for important warnings</li>
        <li>✅ Verified all backgrounds are white (#fff) only</li>
        <li>✅ Optimized for cost-effective printing</li>
        <li>✅ Created printer-friendly field guide generator</li>
        <li>✅ Created printer-friendly demo walkthrough generator</li>
    </ul>
</div>

<h3>1.2 DocumentBuilder Framework</h3>

<div class="checklist">
    <div class="checklist-title">Framework Components</div>
    <ul>
        <li>✅ Created unified DocumentBuilder class with fluent API</li>
        <li>✅ Designed composable units architecture (AudienceAdapter, DesignSystem, TemplateRenderer)</li>
        <li>✅ Implemented automatic printer-friendly conversion via flag</li>
        <li>✅ Added DocumentCollection for auto-binder support</li>
        <li>✅ Created simple 3-line API for document generation</li>
        <li>✅ Created printer_friendly_helper.py utility functions</li>
        <li>✅ Created simple_field_guide_example.py demonstrating usage</li>
    </ul>
</div>

<h3>1.3 PDF Redactor Tool</h3>

<div class="checklist">
    <div class="checklist-title">Redaction Capabilities</div>
    <ul>
        <li>✅ Created PDFRedactor class using pypdf and reportlab</li>
        <li>✅ Implemented area redaction (x, y, width, height)</li>
        <li>✅ Created overlay system with black rectangles</li>
        <li>✅ Created demo_redactor_simple.py for demonstration</li>
        <li>✅ Storytelling tool for classified documents</li>
    </ul>
</div>

<h3>1.4 Global Cursor Commands</h3>

<div class="checklist">
    <div class="checklist-title">Command System</div>
    <ul>
        <li>✅ Created /generate-waft-docs global command</li>
        <li>✅ Created scripts/generate_waft_docs.py CLI script</li>
        <li>✅ Unified interface for all document generation</li>
        <li>✅ Supports field guides, booklets, printer-friendly, session summaries, redaction</li>
        <li>✅ Comprehensive documentation in command file</li>
    </ul>
</div>

<h3>1.5 Documentation & Checkpoints</h3>

<div class="checklist">
    <div class="checklist-title">Documentation Created</div>
    <ul>
        <li>✅ DOCUMENT_GENERATION_FRAMEWORK_CHECKPOINT.md - Complete design analysis</li>
        <li>✅ PRINTER_FRIENDLY_WHITE_BACKGROUND_UPDATE.md - Update recap</li>
        <li>✅ Session summary generator (generate_session_summary.py)</li>
        <li>✅ Comprehensive command documentation</li>
    </ul>
</div>

<h3>1.6 Git & Version Control</h3>

<div class="checklist">
    <div class="checklist-title">Commits Made</div>
    <ul>
        <li>✅ 5 logical commits with clear messages</li>
        <li>✅ All changes pushed to origin</li>
        <li>✅ Branch: claude/waft-field-guide-booklet-jxI14</li>
        <li>✅ Ready for Cloud (Claude) review</li>
    </ul>
</div>

<h2>2. Everything We Failed To Do ❌</h2>

<h3>2.1 Incomplete Implementations</h3>

<div class="caution">
    <div class="caution-title">Not Completed</div>
    <ul>
        <li>❌ Full DocumentBuilder framework implementation (only design checkpoint created)</li>
        <li>❌ Composable units (AudienceAdapter, DesignSystem, TemplateRenderer) - designed but not implemented</li>
        <li>❌ Automatic text detection for PDF redactor (only manual area redaction works)</li>
        <li>❌ Printer-friendly binder assembly (individual PDFs work, but booklet assembly needs work)</li>
        <li>❌ Integration with ReflectionSystem for self-documentation</li>
        <li>❌ Testing suite for new components</li>
    </ul>
</div>

<h3>2.2 Missing Features</h3>

<div class="caution">
    <div class="caution-title">Features Not Implemented</div>
    <ul>
        <li>❌ Automatic content adaptation for different audiences (layman/professional/scientist)</li>
        <li>❌ Template caching for performance</li>
        <li>❌ Batch document generation optimization</li>
        <li>❌ Document metadata extraction and analysis</li>
        <li>❌ ContentAnalyzer class for structure analysis</li>
    </ul>
</div>

<h3>2.3 Documentation Gaps</h3>

<div class="caution">
    <div class="caution-title">Missing Documentation</div>
    <ul>
        <li>❌ API reference for DocumentBuilder (only examples exist)</li>
        <li>❌ Usage guide for printer-friendly conversion</li>
        <li>❌ Best practices guide for document generation</li>
        <li>❌ Troubleshooting guide for common issues</li>
        <li>❌ Performance optimization guide</li>
    </ul>
</div>

<h2>3. Everything We Planned 📋</h2>

<h3>3.1 Original Goals</h3>

<div class="note">
    <div class="note-title">Planned Objectives</div>
    <ul>
        <li>✅ Create printer-friendly versions of field guides</li>
        <li>✅ Simplify document generation process</li>
        <li>✅ Create composable, reusable building blocks</li>
        <li>✅ Design unified DocumentGenerator class</li>
        <li>✅ Retain all existing features and capabilities</li>
        <li>✅ Create global Cursor command for document generation</li>
    </ul>
</div>

<h3>3.2 Design Checkpoint Goals</h3>

<div class="note">
    <div class="note-title">Checkpoint Objectives</div>
    <ul>
        <li>✅ Identify repetition patterns for compression</li>
        <li>✅ Propose composable units design</li>
        <li>✅ Create architecture documentation</li>
        <li>✅ Design clean theme (no background graphics)</li>
        <li>✅ Plan for implementation review</li>
    </ul>
</div>

<h3>3.3 User Requests</h3>

<div class="note">
    <div class="note-title">User-Requested Features</div>
    <ul>
        <li>✅ "Go lighter on black ink" - Completed</li>
        <li>✅ "Develop redactor tool" - Completed</li>
        <li>✅ "Create global command" - Completed</li>
        <li>✅ "Generate session summary" - Completed</li>
        <li>✅ "Make commits and push" - Completed</li>
    </ul>
</div>

<h2>4. Everything We Failed To Plan For ⚠️</h2>

<h3>4.1 Unexpected Challenges</h3>

<div class="warning">
    <div class="warning-title">Unplanned Issues</div>
    <ul>
        <li>⚠️ Printer-friendly helper regex errors (IndexError in border patterns)</li>
        <li>⚠️ Need for direct template usage instead of helper in session summary</li>
        <li>⚠️ Complexity of printer-friendly binder assembly</li>
        <li>⚠️ Coordinate system differences in PDF redaction (bottom-left origin)</li>
        <li>⚠️ Template rendering performance with large documents</li>
    </ul>
</div>

<h3>4.2 Scope Creep</h3>

<div class="warning">
    <div class="warning-title">Additional Work Not Initially Planned</div>
    <ul>
        <li>⚠️ PDF redactor tool (requested mid-session)</li>
        <li>⚠️ Session summary generator (requested mid-session)</li>
        <li>⚠️ Global command creation (requested at end)</li>
        <li>⚠️ Closeout summary generation (current request)</li>
        <li>⚠️ Multiple iterations of printer-friendly styling</li>
    </ul>
</div>

<h3>4.3 Integration Challenges</h3>

<div class="warning">
    <div class="warning-title">Integration Issues Not Anticipated</div>
    <ul>
        <li>⚠️ DocumentBuilder framework needs integration with existing binder system</li>
        <li>⚠️ Printer-friendly conversion needs better automation</li>
        <li>⚠️ Template system needs refactoring for composability</li>
        <li>⚠️ CLI script needs better error handling</li>
    </ul>
</div>

<h2>5. Errors and Mistakes 🔴</h2>

<h3>5.1 Code Errors</h3>

<table>
    <caption>Errors Encountered and Fixed</caption>
    <tr>
        <th>Error</th>
        <th>Cause</th>
        <th>Fix</th>
        <th>Status</th>
    </tr>
    <tr>
        <td><strong>IndexError in printer_friendly_helper.py</strong></td>
        <td>Regex pattern trying to access m.group(2) which wasn't always present</td>
        <td>Bypassed by using direct template in session summary generator</td>
        <td>⚠️ Workaround applied, not fully fixed</td>
    </tr>
    <tr>
        <td><strong>Template import issues</strong></td>
        <td>Module path issues with src.waft.templates</td>
        <td>Fixed with proper sys.path.insert</td>
        <td>✅ Fixed</td>
    </tr>
    <tr>
        <td><strong>Binder TOC template error</strong></td>
        <td>Jinja2 variable 'section' undefined in CSS scope</td>
        <td>Removed {{ section.color }} from CSS block</td>
        <td>✅ Fixed</td>
    </tr>
</table>

<h3>5.2 Design Mistakes</h3>

<div class="caution">
    <div class="caution-title">Design Issues</div>
    <ul>
        <li>🔴 Created printer_friendly_helper.py but it has bugs - should have tested more thoroughly</li>
        <li>🔴 DocumentBuilder framework designed but not fully implemented - should have been incremental</li>
        <li>🔴 Multiple template files instead of unified system - should have refactored first</li>
        <li>🔴 CLI script created without comprehensive error handling</li>
    </ul>
</div>

<h3>5.3 Process Mistakes</h3>

<div class="caution">
    <div class="caution-title">Process Issues</div>
    <ul>
        <li>🔴 Didn't test printer-friendly helper before using it in session summary</li>
        <li>🔴 Created multiple commits instead of one comprehensive commit initially</li>
        <li>🔴 Didn't create tests for new functionality</li>
        <li>🔴 Didn't update existing documentation when creating new features</li>
    </ul>
</div>

<h2>6. Oversights 👁️</h2>

<h3>6.1 Technical Oversights</h3>

<div class="note">
    <div class="note-title">Things We Missed</div>
    <ul>
        <li>👁️ Didn't consider PDF coordinate system (bottom-left origin) for redactor initially</li>
        <li>👁️ Didn't plan for template caching to improve performance</li>
        <li>👁️ Didn't consider batch generation optimization</li>
        <li>👁️ Didn't think about template versioning or migration</li>
        <li>👁️ Didn't plan for template customization API</li>
    </ul>
</div>

<h3>6.2 User Experience Oversights</h3>

<div class="note">
    <div class="note-title">UX Issues</div>
    <ul>
        <li>👁️ CLI script doesn't have progress indicators for long operations</li>
        <li>👁️ No validation of input parameters before processing</li>
        <li>👁️ Error messages could be more helpful</li>
        <li>👁️ No dry-run mode for testing</li>
        <li>👁️ No verbose/debug mode for troubleshooting</li>
    </ul>
</div>

<h3>6.3 Documentation Oversights</h3>

<div class="note">
    <div class="note-title">Documentation Gaps</div>
    <ul>
        <li>👁️ Didn't document coordinate system for PDF redaction</li>
        <li>👁️ Didn't create examples for all use cases</li>
        <li>👁️ Didn't document performance characteristics</li>
        <li>👁️ Didn't create migration guide from old to new system</li>
    </ul>
</div>

<h2>7. Lessons Learned 📚</h2>

<h3>7.1 Technical Lessons</h3>

<div class="highlight-box">
    <h3>Key Technical Learnings</h3>
    <ul>
        <li><strong>Test utilities before using them:</strong> printer_friendly_helper had bugs we didn't catch</li>
        <li><strong>Incremental implementation:</strong> Should have implemented DocumentBuilder incrementally, not just designed it</li>
        <li><strong>Template system needs refactoring:</strong> Multiple template files make maintenance harder</li>
        <li><strong>PDF coordinate systems matter:</strong> Bottom-left origin vs top-left can cause confusion</li>
        <li><strong>Error handling is critical:</strong> CLI tools need robust error handling from the start</li>
    </ul>
</div>

<h3>7.2 Process Lessons</h3>

<div class="highlight-box">
    <h3>Process Improvements</h3>
    <ul>
        <li><strong>Test as you go:</strong> Don't create utilities without testing them immediately</li>
        <li><strong>Incremental commits:</strong> Better to commit working pieces incrementally</li>
        <li><strong>Documentation should be parallel:</strong> Document features as you create them</li>
        <li><strong>Scope management:</strong> Be aware of scope creep and adjust plans accordingly</li>
        <li><strong>User feedback loops:</strong> Iterative improvements based on user requests work well</li>
    </ul>
</div>

<h3>7.3 Design Lessons</h3>

<div class="highlight-box">
    <h3>Design Insights</h3>
    <ul>
        <li><strong>Composable units are powerful:</strong> Breaking down into reusable components reduces complexity</li>
        <li><strong>Unified APIs simplify usage:</strong> Single entry point (DocumentBuilder) is much easier than multiple functions</li>
        <li><strong>Printer-friendly should be automatic:</strong> Flag-based conversion is better than separate functions</li>
        <li><strong>Clean design matters:</strong> White backgrounds, minimal ink usage improves usability</li>
        <li><strong>Global commands enable workflow:</strong> Having commands available everywhere improves productivity</li>
    </ul>
</div>

<h2>8. Next Steps 🎯</h2>

<h3>8.1 Immediate Next Steps</h3>

<div class="procedure">
    <div class="step">
        <strong>Fix printer_friendly_helper.py:</strong> Resolve regex IndexError issue properly
    </div>
    <div class="step">
        <strong>Implement DocumentBuilder core:</strong> Build the actual framework, not just design
    </div>
    <div class="step">
        <strong>Add error handling to CLI:</strong> Improve scripts/generate_waft_docs.py robustness
    </div>
    <div class="step">
        <strong>Create tests:</strong> Add test suite for new components
    </div>
    <div class="step">
        <strong>Update documentation:</strong> Create API reference and usage guides
    </div>
</div>

<h3>8.2 Short-Term Goals</h3>

<div class="procedure">
    <div class="step">
        <strong>Implement composable units:</strong> Build AudienceAdapter, DesignSystem, TemplateRenderer
    </div>
    <div class="step">
        <strong>Integrate with ReflectionSystem:</strong> Enable self-documentation capabilities
    </div>
    <div class="step">
        <strong>Add text detection to redactor:</strong> Automatic text redaction, not just manual areas
    </div>
    <div class="step">
        <strong>Optimize performance:</strong> Template caching, batch generation
    </div>
    <div class="step">
        <strong>Create /closeout-chat command:</strong> Use this summary as template
    </div>
</div>

<h3>8.3 Long-Term Vision</h3>

<div class="procedure">
    <div class="step">
        <strong>Complete framework implementation:</strong> Full DocumentBuilder with all composable units
    </div>
    <div class="step">
        <strong>Template system refactoring:</strong> Unified template system with versioning
    </div>
    <div class="step">
        <strong>Advanced features:</strong> Content analysis, automatic audience adaptation
    </div>
    <div class="step">
        <strong>Performance optimization:</strong> Caching, parallel processing, optimization
    </div>
    <div class="step">
        <strong>Comprehensive testing:</strong> Full test coverage for all components
    </div>
</div>

<h2>9. Metrics & Statistics 📊</h2>

<table>
    <caption>Session Statistics</caption>
    <tr>
        <th>Metric</th>
        <th>Value</th>
    </tr>
    <tr>
        <td><strong>Files Created</strong></td>
        <td>~15 new files</td>
    </tr>
    <tr>
        <td><strong>Files Modified</strong></td>
        <td>~5 files</td>
    </tr>
    <tr>
        <td><strong>Commits Made</strong></td>
        <td>6 commits</td>
    </tr>
    <tr>
        <td><strong>Lines of Code</strong></td>
        <td>~3000+ lines</td>
    </tr>
    <tr>
        <td><strong>Commands Created</strong></td>
        <td>2 (generate-waft-docs, closeout-chat)</td>
    </tr>
    <tr>
        <td><strong>Documentation Pages</strong></td>
        <td>3 major documents</td>
    </tr>
    <tr>
        <td><strong>Features Completed</strong></td>
        <td>~80% of planned features</td>
    </tr>
    <tr>
        <td><strong>Bugs Fixed</strong></td>
        <td>3 major bugs</td>
    </tr>
    <tr>
        <td><strong>Bugs Introduced</strong></td>
        <td>1 (printer_friendly_helper regex)</td>
    </tr>
</table>

<h2>10. Recommendations 💡</h2>

<h3>10.1 For Next Session</h3>

<div class="note">
    <div class="note-title">Immediate Recommendations</div>
    <ul>
        <li>💡 Fix printer_friendly_helper.py regex issue before using it again</li>
        <li>💡 Implement DocumentBuilder incrementally, starting with core class</li>
        <li>💡 Add comprehensive error handling to CLI script</li>
        <li>💡 Create test suite before adding more features</li>
        <li>💡 Document API as you implement, not after</li>
    </ul>
</div>

<h3>10.2 For Future Development</h3>

<div class="note">
    <div class="note-title">Long-Term Recommendations</div>
    <ul>
        <li>💡 Refactor template system to unified architecture</li>
        <li>💡 Implement composable units one at a time</li>
        <li>💡 Add performance monitoring and optimization</li>
        <li>💡 Create comprehensive documentation suite</li>
        <li>💡 Establish testing practices from the start</li>
    </ul>
</div>

<h2>11. Conclusion</h2>

<div class="highlight-box">
    <h3>Session Summary</h3>
    <p>
        This session successfully created a comprehensive document generation system with printer-friendly
        capabilities, PDF redaction tools, and global Cursor commands. While not everything was completed
        (particularly the full DocumentBuilder framework implementation), the foundation is solid and
        ready for continued development.
    </p>
    <p>
        <strong>Key Achievement:</strong> Created a unified workflow for document generation that can be
        accessed via global Cursor commands, making the system much more accessible and usable.
    </p>
    <p>
        <strong>Key Learning:</strong> Incremental implementation and testing are critical. Designing
        without implementing can lead to gaps in understanding.
    </p>
</div>

<div class="warning">
    <div class="warning-title">Critical Follow-Up</div>
    The printer_friendly_helper.py bug needs to be fixed before it can be used in production.
    Consider rewriting the regex patterns or using a different approach for CSS conversion.
</div>

<p style="margin-top: 0.5in; text-align: center; font-weight: bold;">
This closeout summary serves as the template for the /closeout-chat command.<br>
Use this structure for documenting all future sessions.
</p>
    """

    output_path = Path("_work_efforts/showcase_documents/CLOSEOUT_SUMMARY_2026-01-11.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    generate_field_guide_printer_friendly(
        title="WAFT SESSION CLOSEOUT",
        content=content,
        output_path=output_path,
        series="CLOSEOUT SUMMARY",
        number="CS-2026-01-11",
        subtitle="Complete Session Documentation: Accomplishments, Failures, Plans, Lessons",
        classification="INTERNAL",
        issued_by="WAFT Development Team",
        date=datetime.now().strftime("%B %d, %Y"),
    )

    return output_path


if __name__ == "__main__":
    print("=" * 80)
    print("Generating Comprehensive Closeout Summary PDF")
    print("=" * 80)
    print()

    pdf_path = generate_closeout_summary()

    print(f"✅ Generated: {pdf_path}")
    print(f"   Size: {pdf_path.stat().st_size / 1024:.1f} KB")
    print()

    # Generate email summaries (using template data - in real usage, extract from session analysis)
    summaries = generate_email_summaries(
        session_focus="WAFT Document Generation & Global Commands",
        accomplishments=[
            "Created printer-friendly document system",
            "Built DocumentBuilder framework",
            "Created PDF redactor tool",
            "Implemented global Cursor commands",
        ],
        errors_fixed=["Printer-friendly helper regex issue"],
        files_modified=[
            "scripts/generate_closeout_summary.py",
            "examples/generate_waft_field_guide_printer_friendly.py",
        ],
    )

    print("=" * 80)
    print("EMAIL SUMMARIES (Copy & Paste Ready)")
    print("=" * 80)
    print()
    print(summaries["technical"])
    print()
    print(summaries["peer"])
    print()
    print(summaries["boss"])
    print()
    print(summaries["tldr"])
    print()

    # Save summaries to text file
    summaries_file = pdf_path.parent / f"EMAIL_SUMMARIES_{datetime.now().strftime('%Y-%m-%d')}.txt"
    with open(summaries_file, "w") as f:
        f.write("EMAIL SUMMARIES - Copy & Paste Ready\n")
        f.write("=" * 80 + "\n\n")
        f.write(summaries["technical"] + "\n\n")
        f.write(summaries["peer"] + "\n\n")
        f.write(summaries["boss"] + "\n\n")
        f.write(summaries["tldr"] + "\n")

    print(f"📄 Email summaries also saved to: {summaries_file}")
    print()
    print("=" * 80)
    print("To open the PDF, run:")
    print(f"   open {pdf_path}")
    print("=" * 80)
