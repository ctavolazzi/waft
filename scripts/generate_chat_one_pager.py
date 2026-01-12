#!/usr/bin/env python3
"""
Generate One-Pager from Chat Session

Creates a 2-page summary of the current chat session using WAFT's one-pager tools.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.waft.one_pager import OnePager
from src.waft.evolution.document_components import ComponentBuilder

def generate_chat_one_pager():
    """Generate one-pager summary of chat session using sections and variables."""
    
    # Define sections with structured content
    sections = [
        {
            'title': 'Overview',
            'content': """
<dl>
<dt><strong>Objective</strong></dt>
<dd>Test WAFT using WAFT's own tools ("eating our own dog food")</dd>

<dt><strong>Status</strong></dt>
<dd>✅ Complete Success</dd>

<dt><strong>Approach</strong></dt>
<dd>Iterative test → analyze → improve → re-test cycle</dd>
</dl>
            """.strip()
        },
        {
            'title': 'Test Results',
            'subtitle': 'Initial Baseline',
            'content': """
- Project Verification: ✅ PASSED (100% integrity)
- LaTeX Generator: ✅ 5/5 tests passed
- Self-Examination: ⚠️ Quality 0.62, Structure 0.25
- Pytest Framework: ✅ PASSED
            """.strip()
        },
        {
            'title': 'Issues Found',
            'content': """
- Document structure score: 0.25 (needed improvement)
- Study Gym session management: incorrect initialization
- LaTeX generator: attribute error in fallback code
            """.strip()
        },
        {
            'title': 'Improvements Made',
            'content': """
- **Document Structure**: Added Introduction, Methodology, Results sections
  - Result: Structure 0.25 → 1.0 (300% improvement)
- **Study Gym**: Fixed session initialization with proper challenge config
  - Result: Hypothesis testing now works
- **LaTeX Generator**: Fixed fallback to use summary/ideas instead of raw_content
  - Result: All tests pass
            """.strip()
        },
        {
            'title': 'Final Results',
            'content': """
- Quality Score: 0.62 → 1.00 (+61%)
- Structure Score: 0.25 → 1.0 (+300%)
- Gaps Identified: 4 → 1 (-75%)
- Batch Verification: ✅ 4/4 tests passed (100% success)
- Karmic Wager: ✅ Won (100 karma on hypothesis)
            """.strip()
        },
        {
            'title': 'Key Takeaways',
            'content': """
- **Self-Examination Works**: WAFT's tools successfully identified real issues
- **Iterative Improvement**: Test → analyze → improve cycle is effective
- **Study Gym Integration**: Proper session management enables full scientific workflow
- **Karmic Wagers**: Risk/reward mechanics add accountability and engagement
            """.strip()
        },
        {
            'title': 'Deliverables',
            'content': """
**Test Scripts**: test_latex_generator.py, test_self_examination.py, test_batch_with_wager.py, generate_test_summary.py, generate_improvements_summary.py

**Documentation**: Checkpoint document, test summary PDF, improvements summary PDF, batch test results PDF, this one-pager
            """.strip()
        },
        {
            'title': 'Conclusion',
            'content': """
Successfully demonstrated "using WAFT to test WAFT" - complete self-testing cycle validates components, identifies issues, enables improvement, and confirms hypotheses. WAFT's tools are functional and can be used to test and validate WAFT itself.
            """.strip()
        }
    ]
    
    # Define variables for template
    variables = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'session_type': 'Self-Testing & Verification',
        'status': 'Complete Success'
    }
    
    print("📄 Generating one-pager with sections and variables...")
    print()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = project_root / "_work_efforts" / "one_pagers" / f"Chat_One_Pager_{timestamp}.pdf"
    
    print(f"📝 Title: WAFT Self-Testing & Verification Session")
    print(f"📊 Sections: {len(sections)}")
    print(f"📋 Variables: {len(variables)}")
    print(f"💾 Output: {output_path}")
    print()
    
    # Option 1: Use from_sections (convenience - converts to DocumentComponents internally)
    # pager = OnePager.from_sections(
    #     sections=sections,
    #     title="WAFT Self-Testing & Verification Session",
    #     subtitle=f"Session Date: {variables['date']}",
    #     variables=variables,
    #     output_path=output_path
    # )
    
    # Option 2: Use from_components directly (using WAFT's document model)
    # ComponentBuilder methods are static, no need to instantiate
    components = [
        ComponentBuilder.build_title_component("WAFT Self-Testing & Verification Session")
    ]
    
    # Add abstract for summary
    components.append(ComponentBuilder.build_abstract_component(
        "Successfully demonstrated 'using WAFT to test WAFT' - complete self-testing cycle validates components, identifies issues, enables improvement, and confirms hypotheses."
    ))
    
    # Add attribution
    components.append(ComponentBuilder.build_attribution_component(
        author="WAFT System",
        date=variables['date']
    ))
    
    # Convert sections to DocumentComponents
    for section in sections:
        title = section.get('title', '')
        content = section.get('content', '')
        
        # Use quote for conclusion, sections for everything else
        if title == 'Conclusion':
            components.append(ComponentBuilder.build_quote_component(
                quote=content,
                attribution="WAFT Self-Testing Session"
            ))
        else:
            components.append(ComponentBuilder.build_section_component(
                title=title,
                ideas=[content],
                level=2
            ))
    
    pager = OnePager.from_components(
        components=components,
        title="WAFT Self-Testing & Verification Session",
        subtitle=f"Session Date: {variables['date']}",
        variables=variables,
        output_path=output_path
    )
    
    pdf_path = pager.generate(output_path=output_path, save_html_preview=True, open_in_browser=True)
    
    print("="*70)
    print("✅ One-Pager Generated!")
    print("="*70)
    print(f"📄 Output: {pdf_path}")
    print()
    print("Ready for printing and binder storage! 📚")
    
    return pdf_path

if __name__ == "__main__":
    generate_chat_one_pager()
