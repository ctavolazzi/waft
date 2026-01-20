#!/usr/bin/env python3
"""
Generate Session Closeout for January 17, 2026
Session: Show-Me HTML Report Design Refinement
"""

import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from examples.generate_waft_field_guide_printer_friendly import (
    generate_field_guide_printer_friendly,
)


def generate_closeout():
    """Generate closeout summary for show-me design session."""

    content = """
<h2>Session Closeout Summary: Show-Me HTML Report Design Refinement</h2>

<p><strong>Date:</strong> January 17, 2026<br>
<strong>Session Focus:</strong> Refining show-me HTML report design, button aesthetics, unified top section, content visibility<br>
<strong>Status:</strong> ✅ Major accomplishments, design polished</p>

<div class="warning">
    <div class="warning-title">Session Scope</div>
    This session focused on refining the /show-me HTML report design, specifically addressing button aesthetics,
    creating a unified "above the fold" section, fixing content visibility issues, and ensuring Reasoning Trace
    and Chat Context sections are properly included.
</div>

<h2>1. Everything We Accomplished ✅</h2>

<h3>1.1 Unified "Above the Fold" Section</h3>

<div class="checklist">
    <div class="checklist-title">Completed Tasks</div>
    <ul>
        <li>✅ Created unified "above-the-fold" section with ID for entire top area</li>
        <li>✅ Integrated navigation buttons and header section into single component</li>
        <li>✅ Added visual grouping with background and border styling</li>
        <li>✅ Made buttons more discreet while maintaining functionality</li>
        <li>✅ Fixed bottom edge definition on navigation buttons (removed "drop off" effect)</li>
        <li>✅ Added proper bottom borders and pseudo-elements for complete button definition</li>
    </ul>
</div>

<h3>1.2 Button Design Refinement</h3>

<div class="checklist">
    <div class="checklist-title">Design Improvements</div>
    <ul>
        <li>✅ Reduced button prominence (from 80s analog style to more discreet)</li>
        <li>✅ Fixed bottom edge visual break with proper borders and shadows</li>
        <li>✅ Added ::before pseudo-element for bottom edge definition</li>
        <li>✅ Added container separator line below button row</li>
        <li>✅ Improved hover and active states for better feedback</li>
        <li>✅ Maintained tactile feel while reducing distraction</li>
    </ul>
</div>

<h3>1.3 Content Visibility Fixes</h3>

<div class="checklist">
    <div class="checklist-title">Content Restoration</div>
    <ul>
        <li>✅ Fixed duplicate HTML splitting code that caused content to disappear</li>
        <li>✅ Restored all page content (Abstract, Quick Stats, Work Efforts, Projects, etc.)</li>
        <li>✅ Ensured Reasoning Trace and Chat Context sections are included</li>
        <li>✅ Added proper styling for Reasoning Trace and Chat Context sections</li>
        <li>✅ Verified all sections render correctly in HTML output</li>
    </ul>
</div>

<h3>1.4 Section Styling</h3>

<div class="checklist">
    <div class="checklist-title">Styling Enhancements</div>
    <ul>
        <li>✅ Added specific styling for Reasoning Trace section</li>
        <li>✅ Added specific styling for Chat Context section</li>
        <li>✅ Improved content-card styling for expandable details</li>
        <li>✅ Enhanced abstract box with shadow for visual prominence</li>
        <li>✅ Improved header section integration into unified component</li>
    </ul>
</div>

<h2>2. Everything Failed To Do ❌</h2>

<div class="caution">
    <div class="caution-title">Incomplete Items</div>
    <ul>
        <li>❌ Oracle page (oracle.html) - Still needs to be built (explicitly deferred to next session)</li>
        <li>❌ Casefile PDF generation for closeout - Currently only generates field guide format</li>
    </ul>
</div>

<h2>3. Everything Planned 📋</h2>

<div class="note">
    <div class="note-title">Original Goals</div>
    <ul>
        <li>✅ Fix button bottom edge visual break</li>
        <li>✅ Create unified "above the fold" section</li>
        <li>✅ Make buttons more discreet</li>
        <li>✅ Ensure Reasoning Trace and Chat Context sections are included</li>
        <li>✅ Fix content visibility issues</li>
    </ul>
</div>

<h2>4. Everything Failed To Plan For ⚠️</h2>

<div class="warning">
    <div class="warning-title">Unexpected Challenges</div>
    <ul>
        <li>⚠️ Duplicate HTML splitting code caused entire page content to disappear</li>
        <li>⚠️ Template string structure issue required refactoring</li>
        <li>⚠️ Button bottom edge required multiple iterations to fix properly</li>
    </ul>
</div>

<h2>5. Errors and Mistakes 🔴</h2>

<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
<tr style="background: #f5f5f5;">
    <th style="padding: 0.5rem; border: 1px solid #ddd;">Error</th>
    <th style="padding: 0.5rem; border: 1px solid #ddd;">Cause</th>
    <th style="padding: 0.5rem; border: 1px solid #ddd;">Fix</th>
    <th style="padding: 0.5rem; border: 1px solid #ddd;">Status</th>
</tr>
<tr>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Page content disappeared</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Duplicate HTML splitting code inside template string</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Removed duplicate, fixed template structure</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">✅ Fixed</td>
</tr>
<tr>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Button bottom edge "drop off"</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Insufficient bottom border definition</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Added 2px bottom border, ::before pseudo-element, container separator</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">✅ Fixed</td>
</tr>
</table>

<h2>6. Oversights 👁️</h2>

<div class="note">
    <div class="note-title">Things Missed</div>
    <ul>
        <li>👁️ Didn't initially verify that Reasoning Trace and Chat Context were still being generated</li>
        <li>👁️ Template string structure wasn't validated after refactoring</li>
        <li>👁️ Could have tested content visibility earlier in the process</li>
    </ul>
</div>

<h2>7. Lessons Learned 📚</h2>

<div class="highlight-box">
    <h3>Key Insights</h3>
    <ul>
        <li><strong>Visual Hierarchy Matters:</strong> Creating unified sections helps guide user attention to important content</li>
        <li><strong>Edge Cases in CSS:</strong> Bottom edges of elements need explicit definition to avoid visual "drop off"</li>
        <li><strong>Code Duplication is Dangerous:</strong> Duplicate logic in template strings can cause silent failures</li>
        <li><strong>Iterative Design Works:</strong> Multiple iterations on button aesthetics led to better final result</li>
        <li><strong>Content Verification:</strong> Always verify content is actually rendering, not just that code runs</li>
    </ul>
</div>

<h2>8. Next Steps 🎯</h2>

<div class="procedure">
    <div class="procedure-title">Immediate Next Steps</div>
    <ol>
        <li>Build Oracle page (oracle.html) - deferred to next session</li>
        <li>Test show-me report with actual data to verify all sections display correctly</li>
        <li>Consider adding casefile PDF generation option to closeout command</li>
    </ol>
</div>

<h2>9. Metrics & Statistics 📊</h2>

<table style="width: 100%; border-collapse: collapse; margin: 1rem 0;">
<tr style="background: #f5f5f5;">
    <th style="padding: 0.5rem; border: 1px solid #ddd;">Metric</th>
    <th style="padding: 0.5rem; border: 1px solid #ddd;">Value</th>
</tr>
<tr>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Files Modified</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">2 (show_me.py, show_me_bulletproof.py)</td>
</tr>
<tr>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">CSS Rules Added/Modified</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">~15</td>
</tr>
<tr>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Design Iterations</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">3 (initial, discreet, bottom edge fix)</td>
</tr>
<tr>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">Bugs Fixed</td>
    <td style="padding: 0.5rem; border: 1px solid #ddd;">2 (content visibility, button bottom edge)</td>
</tr>
</table>

<h2>10. Recommendations 💡</h2>

<div class="note">
    <div class="note-title">For Next Session</div>
    <ul>
        <li>💡 Build Oracle page (oracle.html) with full JS capabilities</li>
        <li>💡 Consider adding casefile PDF option to closeout command</li>
        <li>💡 Test show-me report with various data scenarios</li>
        <li>💡 Document the "above the fold" design pattern for future use</li>
    </ul>
</div>

<h2>11. Conclusion</h2>

<div class="highlight-box">
    <h3>Session Summary</h3>
    <p>
        This session successfully refined the show-me HTML report design, creating a unified "above the fold"
        section that guides user attention while making navigation buttons more discreet. The bottom edge
        visual break was fixed, and all content sections are now properly visible and styled.
    </p>
    <p>
        <strong>Key Achievement:</strong> Created a cohesive, visually balanced top section that doesn't distract
        from the important content (Abstract, Quick Stats) while maintaining full functionality.
    </p>
    <p>
        <strong>Key Learning:</strong> Visual edge cases (like bottom borders) need explicit definition, and
        code duplication in template strings can cause silent failures that are hard to debug.
    </p>
</div>

<p style="margin-top: 0.5in; text-align: center; font-weight: bold;">
Session closeout complete. Design refinements successful. Ready for next session.
</p>
    """

    output_path = Path("_work_efforts/showcase_documents/CLOSEOUT_SUMMARY_2026-01-17.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    generate_field_guide_printer_friendly(
        title="WAFT SESSION CLOSEOUT",
        content=content,
        output_path=output_path,
        series="CLOSEOUT SUMMARY",
        number="CS-2026-01-17",
        subtitle="Show-Me HTML Report Design Refinement Session",
        classification="INTERNAL",
        issued_by="WAFT Development Team",
        date=datetime.now().strftime("%B %d, %Y"),
    )

    return output_path


def generate_email_summaries():
    """Generate multi-level email summaries for different audiences."""

    # Level 1: Advanced/Highly Technical
    technical = """
=== TECHNICAL SUMMARY ===

Refined the WAFT show-me HTML report generation system (scripts/show_me.py, show_me_bulletproof.py)
by implementing a unified "above-the-fold" section architecture. Created CSS-based component
grouping using section#above-the-fold with integrated navigation bar and header-section-wrapper.
Fixed visual hierarchy issues by:

- Implementing ::before pseudo-elements for button bottom edge definition (2px border, z-index layering)
- Resolving duplicate HTML splitting logic in template string interpolation that caused content
  disappearance (removed duplicate split() calls inside f-string)
- Adding scroll-margin-top and specific styling for Reasoning Trace and Chat Context sections
- Refactoring .nav-dropdown-toggle CSS to reduce visual prominence while maintaining tactile
  feedback (gradient reduction, border simplification, shadow optimization)

Technical changes: ~15 CSS rule modifications, 2 file edits, template string structure refactoring.
Fixed 2 bugs: content visibility (duplicate code), button bottom edge visual break (insufficient
border definition).
"""

    # Level 2: Peer Filter (Technical but accessible)
    peer = """
=== PEER SUMMARY ===

Worked on refining the WAFT session overview HTML report. The main focus was creating a better
visual hierarchy by grouping the top navigation and header into a single unified section, and
making the navigation buttons less distracting while keeping them functional.

Key improvements:
- Created a unified "above the fold" section that groups navigation and header together
- Fixed a bug where page content disappeared (duplicate code in the template)
- Refined button styling to be more subtle - they still look tactile but don't draw attention
  away from the important content
- Fixed a visual issue where button bottom edges looked incomplete
- Ensured all sections (Reasoning Trace, Chat Context) are properly included and styled

The result is a cleaner, more focused design where users' attention is guided to the important
information (abstract, stats) rather than being distracted by navigation elements.
"""

    # Level 3: Boss Filter (Goals and objectives)
    boss = """
=== EXECUTIVE SUMMARY ===

Completed design refinements for the WAFT session overview report to improve usability and
visual clarity.

Objectives Achieved:
✓ Created unified top section for better information hierarchy
✓ Reduced visual distractions from navigation elements
✓ Fixed content visibility issues
✓ Improved overall user experience

Impact: The report now better guides users to key information and provides a cleaner, more
professional appearance. All functionality maintained while improving visual design.

Status: Complete and ready for use.
"""

    # Level 4: Anyone/TLDR
    tldr = """
=== TLDR ===

Refined the session overview report design - made it cleaner and easier to scan. Fixed some
visual bugs and improved how information is organized. Everything works better now.
"""

    return {
        "technical": technical.strip(),
        "peer": peer.strip(),
        "boss": boss.strip(),
        "tldr": tldr.strip(),
    }


if __name__ == "__main__":
    print("=" * 80)
    print("Generating Session Closeout Summary PDF")
    print("=" * 80)
    print()

    pdf_path = generate_closeout()

    print(f"✅ Generated: {pdf_path}")
    print(f"   Size: {pdf_path.stat().st_size / 1024:.1f} KB")
    print()

    # Generate and display email summaries
    summaries = generate_email_summaries()

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
    print("=" * 80)
    print("To open the PDF, run:")
    print(f"   open {pdf_path}")
    print("=" * 80)
