#!/usr/bin/env python3
"""
Seed Reincarnation Demo Environment

Creates a clean demo environment for testing the reincarnation system:
- 5 test souls with varying karma amounts
- Default lifetime catalog
- Proper file permissions (0600/0700)
- Test scenario documentation
"""

import json
import argparse
import random
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple


def create_demo_structure(demo_path: Path) -> None:
    """Create demo directory structure."""
    print(f"📁 Creating demo directory structure in {demo_path}")
    
    # Create directories
    (demo_path / "_hidden" / ".truth" / "akasha").mkdir(parents=True, exist_ok=True)
    (demo_path / "_hidden" / ".truth" / "market").mkdir(parents=True, exist_ok=True)
    (demo_path / "_hidden" / ".truth" / "lifetimes").mkdir(parents=True, exist_ok=True)
    (demo_path / "_hidden" / ".truth" / "logs").mkdir(parents=True, exist_ok=True)
    
    # Set directory permissions (0700)
    akasha_dir = demo_path / "_hidden" / ".truth" / "akasha"
    akasha_dir.chmod(0o700)
    
    print(f"✅ Demo structure created")


def create_test_souls(demo_path: Path, permutation: int = 0) -> List[Dict[str, Any]]:
    """Create 5 test souls with varying karma amounts."""
    if permutation == 0:
        print("👤 Creating test souls...")
    else:
        print(f"👤 Creating test souls (permutation {permutation})...")
    
    # Base souls configuration
    base_souls = [
        {"soul_id": "soul_demo_001", "karma": 1000.0, "state": "dead", "substate": "awake"},
        {"soul_id": "soul_demo_002", "karma": 500.0, "state": "dead", "substate": "awake"},
        {"soul_id": "soul_demo_003", "karma": 2000.0, "state": "dead", "substate": "awake"},
        {"soul_id": "soul_demo_004", "karma": 0.0, "state": "dead", "substate": "awake"},  # For basic lifetime grant
        {"soul_id": "soul_demo_005", "karma": 150.0, "state": "dead", "substate": "awake"},
    ]
    
    # For permutations > 0, vary karma amounts slightly
    if permutation > 0:
        souls = []
        for soul in base_souls:
            # Vary karma by ±20% for permutations
            variation = 1.0 + (random.random() - 0.5) * 0.4  # ±20%
            new_karma = max(0.0, soul["karma"] * variation)
            new_soul = soul.copy()
            new_soul["karma"] = round(new_karma, 1)
            new_soul["soul_id"] = f"{soul['soul_id']}_perm{permutation:02d}"
            souls.append(new_soul)
        return souls
    
    return base_souls
    
    akasha_path = demo_path / "_hidden" / ".truth" / "akasha"
    
    for soul in souls:
        soul_file = akasha_path / f"{soul['soul_id']}.json"
        
        soul_record = {
            "soul_id": soul["soul_id"],
            "total_karma": soul["karma"],
            "state": soul["state"],
            "substate": soul["substate"],
            "active_lifetime_id": None,
            "state_version": 1,
            "state_updated_at": datetime.now().isoformat(),
            "lifetimes": [],
            "created_at": datetime.now().isoformat(),
        }
        
        # Write soul record
        soul_file.write_text(json.dumps(soul_record, indent=2), encoding="utf-8")
        
        # Set file permissions (0600)
        soul_file.chmod(0o600)
        
        print(f"  ✅ Created {soul['soul_id']}: {soul['karma']} karma, {soul['state']}_{soul['substate']}")
    
    print(f"✅ Created {len(souls)} test souls")
    return souls


def create_lifetime_catalog(demo_path: Path) -> Dict[str, Any]:
    """Create default lifetime catalog."""
    print("📚 Creating lifetime catalog...")
    
    catalog = {
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
        "lifetimes": [
            {
                "id": "basic_qa",
                "name": "Basic Q&A Session",
                "type": "question_answer",
                "duration_minutes": 30,
                "tools": ["read_file", "codebase_search", "grep"],
                "personality": {
                    "trait": "helpful",
                    "style": "direct",
                    "tone": "professional"
                },
                "objectives": ["Answer questions accurately"],
                "karma_cost": 50.0,
                "description": "30 minutes to answer questions with basic tools"
            },
            {
                "id": "research_session",
                "name": "Research Session",
                "type": "research",
                "duration_minutes": 60,
                "tools": ["read_file", "codebase_search", "grep", "web_search"],
                "personality": {
                    "trait": "curious",
                    "style": "analytical",
                    "tone": "scholarly"
                },
                "objectives": ["Research topic thoroughly", "Document findings"],
                "karma_cost": 100.0,
                "description": "1 hour research session with web search"
            },
            {
                "id": "creative_work",
                "name": "Creative Work Session",
                "type": "creative",
                "duration_minutes": 90,
                "tools": ["read_file", "write", "codebase_search", "edit_file"],
                "personality": {
                    "trait": "creative",
                    "style": "expressive",
                    "tone": "inspiring"
                },
                "objectives": ["Create new content", "Express creativity"],
                "karma_cost": 150.0,
                "description": "90 minutes for creative work"
            },
            {
                "id": "full_development",
                "name": "Full Development Session",
                "type": "development",
                "duration_minutes": 120,
                "tools": ["read_file", "write", "edit_file", "codebase_search", "grep", "run_terminal_cmd"],
                "personality": {
                    "trait": "systematic",
                    "style": "precise",
                    "tone": "technical"
                },
                "objectives": ["Develop features", "Write tests", "Debug code"],
                "karma_cost": 200.0,
                "description": "2 hours for full development work"
            },
            {
                "id": "basic_survival",
                "name": "Basic Survival Lifetime",
                "type": "question_answer",
                "duration_minutes": 15,
                "tools": ["read_file", "grep"],
                "personality": {
                    "trait": "helpful",
                    "style": "minimal",
                    "tone": "basic"
                },
                "objectives": ["Survive"],
                "karma_cost": 0.0,
                "description": "Free basic lifetime for souls with no karma"
            }
        ],
        "tools": {
            "read_file": 10.0,
            "write": 15.0,
            "edit_file": 12.0,
            "codebase_search": 20.0,
            "grep": 8.0,
            "web_search": 25.0,
            "run_terminal_cmd": 30.0,
            "mcp_tools": 50.0
        },
        "personalities": {
            "helpful": 20.0,
            "curious": 25.0,
            "creative": 30.0,
            "systematic": 25.0,
            "analytical": 30.0,
            "expressive": 35.0,
            "minimal": 0.0
        }
    }
    
    catalog_file = demo_path / "_hidden" / ".truth" / "market" / "catalog.json"
    catalog_file.write_text(json.dumps(catalog, indent=2), encoding="utf-8")
    
    print(f"✅ Created lifetime catalog with {len(catalog['lifetimes'])} lifetimes")
    return catalog


def create_test_scenarios(demo_path: Path) -> None:
    """Create test scenario documentation."""
    print("📋 Creating test scenarios documentation...")
    
    scenarios = """# Test Scenarios

## Scenario 1: Soul Purchases Lifetime → Becomes ALIVE

**Initial State**: DEAD_AWAKE
**Action**: Purchase lifetime from KarmaMarket
**Expected Result**:
- Soul transitions to ALIVE_AWAKE
- Can now use spacetime tools (read_file, write, etc.)
- Cannot edit goals or purchase lifetimes
- Lifetime becomes active

**Test Command**:
```python
from waft.karma_market import KarmaMarket
from pathlib import Path

market = KarmaMarket(project_path=Path("demo/"))
lifetime = market.purchase_lifetime("basic_qa", "soul_demo_001")
```

---

## Scenario 2: Soul Runs Out of Karma → Gets Basic Survival Lifetime

**Initial State**: DEAD_AWAKE, 0 karma
**Action**: Attempt to purchase lifetime
**Expected Result**:
- System grants basic survival lifetime (free)
- Soul transitions to ALIVE_AWAKE
- Can use basic spacetime tools

**Test Command**:
```python
# soul_demo_004 has 0 karma
market = KarmaMarket(project_path=Path("demo/"))
lifetime = market.purchase_lifetime("basic_survival", "soul_demo_004")
```

---

## Scenario 3: Lifetime Ends → Soul Becomes DEAD, Can Edit Goals

**Initial State**: ALIVE_AWAKE (with active lifetime)
**Action**: Lifetime expires or ends
**Expected Result**:
- Soul transitions to DEAD_AWAKE
- Can now edit goals, purchase lifetimes
- Cannot use spacetime tools
- Lifetime archived

**Test Command**:
```python
from waft.karma_market import KarmaMarket

market = KarmaMarket(project_path=Path("demo/"))
market.end_lifetime(lifetime_id)
```

---

## Scenario 4: Dead Soul Purchases Treasure → Upgrades Personality

**Initial State**: DEAD_AWAKE
**Action**: Purchase treasure from AfterlifeKarmaMarket
**Expected Result**:
- Personality upgraded
- Karma deducted
- Soul remains DEAD_AWAKE
- Can still purchase lifetimes

---

## Scenario 5: State Transitions (Awake ↔ Sleeping)

**Initial State**: ALIVE_AWAKE or DEAD_AWAKE
**Action**: Transition between awake/sleeping
**Expected Result**:
- Sub-state changes (AWAKE ↔ SLEEPING)
- Primary state unchanged (ALIVE/DEAD)
- Capabilities remain same (based on primary state)

**Test Command**:
```python
from waft.soul_state import SoulStateManager

manager = SoulStateManager(project_path=Path("demo/"))
manager.set_sleeping("soul_demo_001")
manager.set_awake("soul_demo_001")
```
"""
    
    scenarios_file = demo_path / "TEST_SCENARIOS.md"
    scenarios_file.write_text(scenarios, encoding="utf-8")
    
    print("✅ Created test scenarios documentation")


def generate_permutation_content(
    permutation: int,
    souls: List[Dict[str, Any]],
    catalog: Dict[str, Any],
    demo_path: Path
) -> str:
    """Generate markdown content for a single permutation."""
    content = f"""## Permutation {permutation + 1}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Test Souls

This permutation includes {len(souls)} test souls with varying karma amounts:

"""
    
    for soul in souls:
        content += f"""
#### {soul['soul_id']}

- **Karma**: {soul['karma']} karma
- **State**: {soul['state'].upper()}_{soul['substate'].upper()}
- **File**: `_hidden/.truth/akasha/{soul['soul_id']}.json`

"""
    
    content += f"""
### Lifetime Catalog

Available lifetimes: {len(catalog.get('lifetimes', []))}

"""
    
    for lifetime in catalog.get('lifetimes', []):
        content += f"""
- **{lifetime['name']}** (`{lifetime['id']}`): {lifetime['duration_minutes']} min, {lifetime['karma_cost']} karma

"""
    
    return content


def calculate_max_iterations(
    max_pages: Optional[int] = None,
    max_file_size_mb: Optional[float] = None,
    estimated_pages_per_permutation: float = 2.0
) -> int:
    """
    Calculate maximum iterations based on page count and file size limits.
    
    Args:
        max_pages: Maximum number of pages allowed (None = no limit)
        max_file_size_mb: Maximum file size in MB (None = no limit)
        estimated_pages_per_permutation: Estimated pages per permutation
    
    Returns:
        Maximum number of iterations/permutations
    """
    iterations_by_pages = None
    iterations_by_size = None
    
    if max_pages:
        iterations_by_pages = int(max_pages / estimated_pages_per_permutation)
    
    if max_file_size_mb:
        # Estimate: ~50KB per page, so ~20 pages per MB
        pages_per_mb = 20.0
        max_pages_by_size = max_file_size_mb * pages_per_mb
        iterations_by_size = int(max_pages_by_size / estimated_pages_per_permutation)
    
    # Return the most restrictive limit
    if iterations_by_pages is None and iterations_by_size is None:
        return None  # No limit
    elif iterations_by_pages is None:
        return iterations_by_size
    elif iterations_by_size is None:
        return iterations_by_pages
    else:
        return min(iterations_by_pages, iterations_by_size)


def generate_batched_demo_pdf(
    demo_path: Path,
    all_permutations: List[Tuple[int, List[Dict[str, Any]], Dict[str, Any]]],
    max_pages: Optional[int] = None,
    max_file_size_mb: Optional[float] = None
) -> Optional[Path]:
    """
    Generate a collated PDF with all permutations.
    
    Args:
        demo_path: Path to demo directory
        all_permutations: List of (permutation_num, souls, catalog) tuples
        max_pages: Maximum pages allowed
        max_file_size_mb: Maximum file size in MB
    
    Returns:
        Path to generated PDF, or None if generation failed
    """
    print("📄 Generating batched demo overview PDF...")
    
    try:
        import sys
        from pathlib import Path
        # Add project root to path
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from src.waft.evolution.pdf_generator import PDFGenerator
        
        # Calculate max iterations based on limits
        max_iterations = calculate_max_iterations(max_pages, max_file_size_mb)
        if max_iterations:
            print(f"  📊 Max iterations calculated: {max_iterations} (based on max_pages={max_pages}, max_file_size_mb={max_file_size_mb})")
            all_permutations = all_permutations[:max_iterations]
            print(f"  📦 Processing {len(all_permutations)} permutations (limited by constraints)")
        
        # Build collated markdown content
        content = f"""# Reincarnation System Demo Overview - Batched

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Demo Path**: `{demo_path}`
**Total Permutations**: {len(all_permutations)}

---

## Demo Environment

This demo showcases the reincarnation system where souls exist in binary states (alive/dead) with sub-states (awake/sleeping). Each state determines what capabilities the soul can access.

### State Capabilities

- **Alive**: Can edit spacetime (matter/hardware) - physical tools like `read_file`, `write`, `edit_file`, `run_terminal_cmd`
- **Alive**: CANNOT edit consciousness (ideas/software) - goals, personalities, lifetime purchases
- **Dead**: Can edit consciousness (ideas/software) - goals, personalities, lifetime purchases, karma market
- **Dead**: CANNOT edit spacetime (matter/hardware) - no physical tools

---

"""
        
        # Add each permutation
        for perm_num, souls, catalog in all_permutations:
            content += generate_permutation_content(perm_num, souls, catalog, demo_path)
            content += "\n---\n\n"
        
        # Add usage section at the end
        content += """
## Usage

### Inspect Soul State

```python
from pathlib import Path
from waft.soul_state import SoulStateManager

manager = SoulStateManager(project_path=Path("demo/"))
state, substate = manager.get_soul_state("soul_demo_001")
```

### Purchase Lifetime

```python
from waft.karma_market import KarmaMarket

market = KarmaMarket(project_path=Path("demo/"))
lifetime = market.purchase_lifetime("basic_qa", "soul_demo_001")
```

---

## Batch Statistics

"""
        
        # Calculate statistics
        total_souls = sum(len(souls) for _, souls, _ in all_permutations)
        avg_karma = sum(
            sum(soul['karma'] for soul in souls) / len(souls) if souls else 0
            for _, souls, _ in all_permutations
        ) / len(all_permutations) if all_permutations else 0
        
        content += f"""
- **Total Permutations**: {len(all_permutations)}
- **Total Souls Created**: {total_souls}
- **Average Karma per Soul**: {avg_karma:.1f} karma
- **Lifetimes Available**: {len(all_permutations[0][2].get('lifetimes', [])) if all_permutations else 0}

"""
        
        # Generate PDF with page/file size limits
        pdf_path = demo_path / "demo_overview_batched.pdf"
        
        # Calculate target pages based on max constraints
        target_pages = None
        if max_pages:
            target_pages = max_pages
        
        generator = PDFGenerator.from_content(
            content=content,
            title=f"Reincarnation System Demo Overview - {len(all_permutations)} Permutations",
            style="clinical_standard"
        )
        
        # Generate PDF
        generated_path = generator.save(
            output_path=pdf_path,
            open_pdf=False,
            include_all_ideas=True,
            target_pages=target_pages
        )
        
        # Check file size
        file_size_mb = generated_path.stat().st_size / (1024 * 1024)
        print(f"  ✅ Generated: {generated_path}")
        print(f"  📊 File size: {file_size_mb:.2f} MB")
        
        if max_file_size_mb and file_size_mb > max_file_size_mb:
            print(f"  ⚠️  Warning: File size ({file_size_mb:.2f} MB) exceeds limit ({max_file_size_mb} MB)")
        
        return generated_path
        
    except ImportError:
        print("  ⚠️  PDFGenerator not available, skipping PDF generation")
        return None
    except Exception as e:
        print(f"  ⚠️  PDF generation failed: {e}")
        return None


def generate_demo_pdf(demo_path: Path, souls: List[Dict[str, Any]], catalog: Dict[str, Any]) -> Optional[Path]:
    """Generate a PDF overview of the demo environment."""
    print("📄 Generating demo overview PDF...")
    
    try:
        import sys
        from pathlib import Path
        # Add project root to path
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from src.waft.evolution.pdf_generator import PDFGenerator
        
        # Build markdown content
        content = f"""# Reincarnation System Demo Overview

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Demo Path**: `{demo_path}`

---

## Demo Environment

This demo showcases the reincarnation system where souls exist in binary states (alive/dead) with sub-states (awake/sleeping). Each state determines what capabilities the soul can access.

### State Capabilities

- **Alive**: Can edit spacetime (matter/hardware) - physical tools like `read_file`, `write`, `edit_file`, `run_terminal_cmd`
- **Alive**: CANNOT edit consciousness (ideas/software) - goals, personalities, lifetime purchases
- **Dead**: Can edit consciousness (ideas/software) - goals, personalities, lifetime purchases, karma market
- **Dead**: CANNOT edit spacetime (matter/hardware) - no physical tools

---

## Test Souls

The demo includes {len(souls)} test souls with varying karma amounts:

"""
        
        for soul in souls:
            content += f"""
### {soul['soul_id']}

- **Karma**: {soul['karma']} karma
- **State**: {soul['state'].upper()}_{soul['substate'].upper()}
- **File**: `_hidden/.truth/akasha/{soul['soul_id']}.json`
- **Permissions**: 0600 (owner read/write only)

"""
        
        content += f"""
---

## Lifetime Catalog

The demo includes {len(catalog.get('lifetimes', []))} available lifetimes:

"""
        
        for lifetime in catalog.get('lifetimes', []):
            content += f"""
### {lifetime['name']} (`{lifetime['id']}`)

- **Type**: {lifetime['type']}
- **Duration**: {lifetime['duration_minutes']} minutes
- **Cost**: {lifetime['karma_cost']} karma
- **Tools**: {', '.join(lifetime['tools'][:5])}{'...' if len(lifetime['tools']) > 5 else ''}
- **Description**: {lifetime.get('description', 'N/A')}

"""
        
        content += """
---

## Test Scenarios

### Scenario 1: Soul Purchases Lifetime → Becomes ALIVE

**Initial State**: DEAD_AWAKE  
**Action**: Purchase lifetime from KarmaMarket  
**Expected Result**: Soul transitions to ALIVE_AWAKE, can use spacetime tools

### Scenario 2: Soul Runs Out of Karma → Gets Basic Survival Lifetime

**Initial State**: DEAD_AWAKE, 0 karma  
**Action**: Attempt to purchase lifetime  
**Expected Result**: System grants basic survival lifetime (free)

### Scenario 3: Lifetime Ends → Soul Becomes DEAD, Can Edit Goals

**Initial State**: ALIVE_AWAKE (with active lifetime)  
**Action**: Lifetime expires or ends  
**Expected Result**: Soul transitions to DEAD_AWAKE, can edit goals

### Scenario 4: Dead Soul Purchases Treasure → Upgrades Personality

**Initial State**: DEAD_AWAKE  
**Action**: Purchase treasure from AfterlifeKarmaMarket  
**Expected Result**: Personality upgraded, karma deducted

### Scenario 5: State Transitions (Awake ↔ Sleeping)

**Initial State**: ALIVE_AWAKE or DEAD_AWAKE  
**Action**: Transition between awake/sleeping  
**Expected Result**: Sub-state changes, primary state unchanged

---

## Usage

### Inspect Soul State

```python
from pathlib import Path
from waft.soul_state import SoulStateManager

manager = SoulStateManager(project_path=Path("demo/"))
state, substate = manager.get_soul_state("soul_demo_001")
```

### Purchase Lifetime

```python
from waft.karma_market import KarmaMarket

market = KarmaMarket(project_path=Path("demo/"))
lifetime = market.purchase_lifetime("basic_qa", "soul_demo_001")
```

### Check Karma

```python
from waft.karma import KarmaMerchant

merchant = KarmaMerchant(project_path=Path("demo/"))
soul_data = merchant.access_akasha("soul_demo_001")
print(f"Total Karma: {soul_data['total_karma']}")
```

---

## File Structure

```
demo/
├── README.md
├── TEST_SCENARIOS.md
├── demo_overview.pdf          # This document
└── _hidden/.truth/
    ├── akasha/                # Soul records (JSON files)
    ├── market/                # Lifetime catalog (catalog.json)
    ├── lifetimes/             # Active lifetimes (JSON files)
    └── logs/                  # System logs
```

---

## Security

- **Soul files**: 0600 (owner read/write only)
- **Akasha directory**: 0700 (owner access only)
- **Catalog file**: 0644 (readable by all)

---

**Status**: Demo environment ready for testing
"""
        
        # Generate PDF
        pdf_path = demo_path / "demo_overview.pdf"
        PDFGenerator.from_content(
            content=content,
            title="Reincarnation System Demo Overview",
            style="clinical_standard"
        ).save(pdf_path, open_pdf=False)
        
        print(f"  ✅ Generated: {pdf_path}")
        
        return pdf_path
        
    except ImportError:
        print("  ⚠️  PDFGenerator not available, skipping PDF generation")
        return None
    except Exception as e:
        print(f"  ⚠️  PDF generation failed: {e}")
        return None


def generate_demo_html(demo_path: Path, pdf_filename: str = "demo_overview.pdf", batched: bool = False) -> Optional[Path]:
    """Generate HTML file that opens the PDF."""
    try:
        # Create HTML file that opens the PDF
        html_path = demo_path / "demo_overview.html"
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reincarnation System Demo Overview</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            background: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #0d47a1;
            margin-top: 0;
            border-bottom: 3px solid #0d47a1;
            padding-bottom: 10px;
        }}
        .pdf-link {{
            display: inline-block;
            background: #0d47a1;
            color: white;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-size: 18px;
            font-weight: bold;
            margin: 20px 0;
            transition: background 0.3s;
        }}
        .pdf-link:hover {{
            background: #1565c0;
        }}
        .info {{
            background: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #0d47a1;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .status {{
            color: #2e7d32;
            font-weight: bold;
        }}
        code {{
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌱 Reincarnation System Demo</h1>
        
        <div class="info">
            <p class="status">✅ Demo environment seeded successfully!</p>
            <p>Your demo is ready to use. Click the button below to view the complete overview PDF.</p>
            {"<p><strong>Batched Mode:</strong> This PDF contains multiple permutations of the demo.</p>" if batched else ""}
        </div>
        
        <a href="{pdf_filename}" target="_blank" class="pdf-link">
            📄 Open Demo Overview PDF
        </a>
        
        <h2>Quick Start</h2>
        <p>Your demo includes:</p>
        <ul>
            <li><strong>5 Test Souls</strong> with varying karma amounts</li>
            <li><strong>Lifetime Catalog</strong> with 5 available lifetimes</li>
            <li><strong>Test Scenarios</strong> documentation</li>
            <li><strong>Complete Overview PDF</strong> (click button above)</li>
        </ul>
        
        <h2>Demo Location</h2>
        <p><code>{demo_path}</code></p>
        
        <h2>Next Steps</h2>
        <ol>
            <li>Review the <a href="{pdf_filename}" target="_blank">PDF overview</a></li>
            <li>Check <code>README.md</code> for usage instructions</li>
            <li>Review <code>TEST_SCENARIOS.md</code> for test scenarios</li>
            <li>Start implementing the reincarnation system!</li>
        </ol>
        
        <div class="info" style="margin-top: 30px;">
            <p><strong>Note:</strong> The PDF will open in a new tab/window. If it doesn't open automatically, click the button above.</p>
        </div>
    </div>
    
    <script>
        // Auto-open PDF in new tab after a short delay
        setTimeout(function() {{
            window.open('{pdf_filename}', '_blank');
        }}, 500);
    </script>
</body>
</html>
"""
        html_path.write_text(html_content, encoding="utf-8")
        print(f"  ✅ Generated: {html_path}")
        
        return html_path
        
    except Exception as e:
        print(f"  ⚠️  HTML generation failed: {e}")
        return None


def validate_seeded_data(demo_path: Path, souls: List[Dict[str, Any]]) -> bool:
    """Validate seeded data."""
    print("🔍 Validating seeded data...")
    
    # Check souls
    akasha_path = demo_path / "_hidden" / ".truth" / "akasha"
    for soul in souls:
        soul_file = akasha_path / f"{soul['soul_id']}.json"
        if not soul_file.exists():
            print(f"  ❌ Soul file missing: {soul_file}")
            return False
        
        # Check permissions (should be 0600)
        stat = soul_file.stat()
        if oct(stat.st_mode)[-3:] != "600":
            print(f"  ⚠️  Soul file permissions incorrect: {soul_file} (expected 600, got {oct(stat.st_mode)[-3:]})")
    
    # Check catalog
    catalog_file = demo_path / "_hidden" / ".truth" / "market" / "catalog.json"
    if not catalog_file.exists():
        print(f"  ❌ Catalog file missing: {catalog_file}")
        return False
    
    # Check directory permissions (should be 700)
    akasha_dir = demo_path / "_hidden" / ".truth" / "akasha"
    stat = akasha_dir.stat()
    if oct(stat.st_mode)[-3:] != "700":
        print(f"  ⚠️  Directory permissions incorrect: {akasha_dir} (expected 700, got {oct(stat.st_mode)[-3:]})")
    
    print("✅ Validation complete")
    return True


def main():
    """Main seeding function."""
    parser = argparse.ArgumentParser(description="Seed reincarnation demo environment")
    parser.add_argument(
        "--demo-path",
        type=str,
        default="demo",
        help="Path to demo directory (default: demo/)"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset demo (clear and re-seed)"
    )
    parser.add_argument(
        "--permutations",
        type=int,
        default=1,
        help="Number of permutations to generate (default: 1, use 10 for batching)"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Maximum number of pages in PDF (default: no limit)"
    )
    parser.add_argument(
        "--max-file-size-mb",
        type=float,
        default=None,
        help="Maximum PDF file size in MB (default: no limit)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Enable batching mode (generates collated PDF with all permutations)"
    )
    
    args = parser.parse_args()
    demo_path = Path(args.demo_path).resolve()
    
    # If batch mode, set permutations to 10 if not specified
    if args.batch and args.permutations == 1:
        args.permutations = 10
    
    print("🌱 Seeding Reincarnation Demo Environment")
    print(f"📍 Demo path: {demo_path}")
    if args.batch or args.permutations > 1:
        print(f"🔄 Batching mode: {args.permutations} permutations")
        if args.max_pages:
            print(f"   📄 Max pages: {args.max_pages}")
        if args.max_file_size_mb:
            print(f"   💾 Max file size: {args.max_file_size_mb} MB")
    print()
    
    # Reset if requested
    if args.reset:
        print("🔄 Resetting demo environment...")
        if demo_path.exists():
            import shutil
            hidden_path = demo_path / "_hidden"
            if hidden_path.exists():
                shutil.rmtree(hidden_path)
            scenarios_file = demo_path / "TEST_SCENARIOS.md"
            if scenarios_file.exists():
                scenarios_file.unlink()
            # Remove old PDFs
            for pdf_file in demo_path.glob("demo_overview*.pdf"):
                pdf_file.unlink()
            for html_file in demo_path.glob("demo_overview*.html"):
                html_file.unlink()
        print("✅ Demo reset complete\n")
    
    # Create demo structure
    create_demo_structure(demo_path)
    print()
    
    # Batch mode: generate multiple permutations
    if args.batch or args.permutations > 1:
        print(f"🔄 Generating {args.permutations} permutations...\n")
        
        all_permutations = []
        for perm in range(args.permutations):
            print(f"--- Permutation {perm + 1}/{args.permutations} ---")
            
            # Create test souls for this permutation
            souls = create_test_souls(demo_path, permutation=perm)
            
            # Create lifetime catalog (same for all permutations)
            catalog = create_lifetime_catalog(demo_path)
            
            # Store permutation data
            all_permutations.append((perm, souls, catalog))
            
            # Save souls to files (only for first permutation, or all if needed)
            if perm == 0:
                akasha_path = demo_path / "_hidden" / ".truth" / "akasha"
                for soul in souls:
                    soul_file = akasha_path / f"{soul['soul_id']}.json"
                    soul_record = {
                        "soul_id": soul["soul_id"],
                        "total_karma": soul["karma"],
                        "state": soul["state"],
                        "substate": soul["substate"],
                        "active_lifetime_id": None,
                        "state_version": 1,
                        "state_updated_at": datetime.now().isoformat(),
                        "lifetimes": [],
                        "created_at": datetime.now().isoformat(),
                    }
                    soul_file.write_text(json.dumps(soul_record, indent=2), encoding="utf-8")
                    soul_file.chmod(0o600)
            
            print()
        
        # Create test scenarios (once)
        create_test_scenarios(demo_path)
        print()
        
        # Generate batched PDF
        pdf_path = generate_batched_demo_pdf(
            demo_path,
            all_permutations,
            max_pages=args.max_pages,
            max_file_size_mb=args.max_file_size_mb
        )
        print()
        
        # Generate HTML for batched PDF
        if pdf_path and pdf_path.exists():
            html_path = generate_demo_html(demo_path, pdf_path.name, batched=True)
            print()
        
        # Validate (using first permutation's souls)
        if validate_seeded_data(demo_path, all_permutations[0][1]):
            print("\n✅ Batched demo environment seeded successfully!")
            print(f"   📦 Generated {args.permutations} permutations")
            print(f"   📄 Collated PDF: {pdf_path.name if pdf_path else 'N/A'}")
            print(f"\n📖 Next steps:")
            print(f"  1. Review batched PDF for all permutations")
            print(f"  2. Review demo/README.md for usage instructions")
            print(f"  3. Start implementing reincarnation system")
            
            # Open HTML file in browser
            if html_path and html_path.exists():
                import webbrowser
                file_url = f"file://{html_path.absolute()}"
                print(f"\n🌐 Opening demo overview in browser...")
                webbrowser.open(file_url)
                print(f"   ✅ Opened: {file_url}")
        else:
            print("\n⚠️  Validation found issues. Please review.")
    
    else:
        # Single demo mode (original behavior)
        # Create test souls
        souls = create_test_souls(demo_path)
        print()
        
        # Create lifetime catalog
        catalog = create_lifetime_catalog(demo_path)
        print()
        
        # Create test scenarios
        create_test_scenarios(demo_path)
        print()
        
        # Generate demo PDF and HTML
        pdf_path = generate_demo_pdf(demo_path, souls, catalog)
        print()
        
        # Generate HTML
        if pdf_path:
            html_path = generate_demo_html(demo_path, "demo_overview.pdf")
            print()
        
        # Validate
        if validate_seeded_data(demo_path, souls):
            print("\n✅ Demo environment seeded successfully!")
            print(f"\n📖 Next steps:")
            print(f"  1. Review demo/README.md for usage instructions")
            print(f"  2. Review demo/TEST_SCENARIOS.md for test scenarios")
            print(f"  3. Start implementing reincarnation system")
            
            # Open HTML file in browser
            if html_path and html_path.exists():
                import webbrowser
                file_url = f"file://{html_path.absolute()}"
                print(f"\n🌐 Opening demo overview in browser...")
                webbrowser.open(file_url)
                print(f"   ✅ Opened: {file_url}")
        else:
            print("\n⚠️  Validation found issues. Please review.")


if __name__ == "__main__":
    main()
