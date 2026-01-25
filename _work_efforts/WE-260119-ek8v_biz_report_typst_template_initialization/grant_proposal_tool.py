#!/usr/bin/env python3
"""
🏆 GRANT PROPOSAL GENERATOR - The Evolutionary Pitch Machine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

A tool that LEVELS UP through use, evolving from a humble proposal
generator into a LEGENDARY grant-writing machine.

Features:
- XP system based on proposals generated
- Level progression with new abilities unlocked
- Evolution milestones (Common → Rare → Epic → Legendary)
- Toner-saver mode (because ink is expensive)
- Learns from critiques to improve future proposals

Usage:
    python grant_proposal_tool.py generate --project "My Project"
    python grant_proposal_tool.py status
    python grant_proposal_tool.py evolve
"""

import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional
from enum import Enum
import textwrap

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# RARITY & EVOLUTION SYSTEM
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class Rarity(Enum):
    COMMON = "Common"
    UNCOMMON = "Uncommon"
    RARE = "Rare"
    EPIC = "Epic"
    LEGENDARY = "Legendary"
    MYTHIC = "Mythic"  # Secret tier

RARITY_COLORS = {
    Rarity.COMMON: "#808080",      # Gray
    Rarity.UNCOMMON: "#1eff00",    # Green
    Rarity.RARE: "#0070dd",        # Blue
    Rarity.EPIC: "#a335ee",        # Purple
    Rarity.LEGENDARY: "#ff8000",   # Orange
    Rarity.MYTHIC: "#e6cc80",      # Gold
}

RARITY_XP_THRESHOLDS = {
    Rarity.COMMON: 0,
    Rarity.UNCOMMON: 100,
    Rarity.RARE: 500,
    Rarity.EPIC: 2000,
    Rarity.LEGENDARY: 10000,
    Rarity.MYTHIC: 50000,
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ABILITIES UNLOCKED AT EACH LEVEL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LEVEL_ABILITIES = {
    1: ["Basic Proposal Generation", "Toner Saver Mode"],
    3: ["Executive Summary Auto-Gen"],
    5: ["Budget Breakdown Tables"],
    7: ["Timeline Generator"],
    10: ["Skepticism Addresser"],
    15: ["Funder Psychology Insights"],
    20: ["Multi-Format Export (PDF, MD, HTML)"],
    25: ["Critique Self-Analysis"],
    30: ["Proposal A/B Testing"],
    40: ["Grant Database Integration"],
    50: ["🔥 LEGENDARY: The Perfect Pitch"],
    75: ["⚡ MYTHIC: Grants Write Themselves"],
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TOOL STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class ToolState:
    """Persistent state for the evolving tool."""
    name: str = "Grant Proposal Generator"
    version: str = "1.0.0"
    xp: int = 0
    level: int = 1
    proposals_generated: int = 0
    critiques_addressed: int = 0
    toner_saved_ml: float = 0.0  # Milliliters of toner saved
    genome_hash: str = ""
    evolution_history: list = field(default_factory=list)
    unlocked_abilities: list = field(default_factory=lambda: ["Basic Proposal Generation", "Toner Saver Mode"])
    created_at: str = ""
    last_used: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.genome_hash:
            self.genome_hash = self._compute_genome()
    
    def _compute_genome(self) -> str:
        """Compute genome hash based on current state."""
        state_str = f"{self.name}:{self.version}:{self.level}:{self.xp}"
        return hashlib.sha256(state_str.encode()).hexdigest()[:16]
    
    @property
    def rarity(self) -> Rarity:
        """Determine current rarity based on XP."""
        for rarity in reversed(list(Rarity)):
            if self.xp >= RARITY_XP_THRESHOLDS[rarity]:
                return rarity
        return Rarity.COMMON
    
    @property
    def xp_to_next_level(self) -> int:
        """XP needed for next level."""
        return self.level * 50  # Each level needs level * 50 XP
    
    @property
    def xp_progress(self) -> float:
        """Progress to next level (0.0 - 1.0)."""
        level_start_xp = sum((i * 50) for i in range(1, self.level))
        xp_in_level = self.xp - level_start_xp
        return min(1.0, xp_in_level / self.xp_to_next_level)
    
    def gain_xp(self, amount: int, reason: str = "") -> dict:
        """Gain XP and potentially level up."""
        old_level = self.level
        old_rarity = self.rarity
        
        self.xp += amount
        
        # Check for level up
        level_ups = []
        while self.xp >= sum((i * 50) for i in range(1, self.level + 1)):
            self.level += 1
            level_ups.append(self.level)
            
            # Check for new abilities
            if self.level in LEVEL_ABILITIES:
                for ability in LEVEL_ABILITIES[self.level]:
                    if ability not in self.unlocked_abilities:
                        self.unlocked_abilities.append(ability)
        
        # Record evolution
        if old_rarity != self.rarity:
            self.evolution_history.append({
                "timestamp": datetime.now().isoformat(),
                "event": "EVOLUTION",
                "from_rarity": old_rarity.value,
                "to_rarity": self.rarity.value,
                "xp": self.xp,
            })
        
        # Update genome
        self.genome_hash = self._compute_genome()
        self.last_used = datetime.now().isoformat()
        
        return {
            "xp_gained": amount,
            "reason": reason,
            "old_level": old_level,
            "new_level": self.level,
            "level_ups": level_ups,
            "old_rarity": old_rarity,
            "new_rarity": self.rarity,
            "evolved": old_rarity != self.rarity,
        }

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROPOSAL TEMPLATES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TYPST_TONER_SAVER_TEMPLATE = '''// {title} - Grant Proposal
// Generated by: {tool_name} (Level {level} {rarity})
// Genome: {genome}
// Toner Saver Mode: ENABLED

#set document(
  title: "{title}",
  author: "{author}",
)

#set page(
  paper: "us-letter",
  margin: (x: 1in, y: 1in),
  header: context {{
    if counter(page).get().first() > 1 [
      #text(size: 9pt, fill: rgb("#666666"))[{title} #h(1fr) {date}]
      #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    ]
  }},
  footer: context [
    #line(length: 100%, stroke: 0.5pt + rgb("#cccccc"))
    #v(4pt)
    #text(size: 9pt, fill: rgb("#666666"))[
      #h(1fr) Page #counter(page).display() #h(1fr)
    ]
  ],
)

#set text(font: "Georgia", size: 11pt)
#set par(justify: true, leading: 0.65em)
#set heading(numbering: none)

// Title
#align(center)[
  #v(0.3in)
  #text(size: 24pt, weight: "bold")[{project_name}]
  #v(0.1in)
  #text(size: 14pt)[{subtitle}]
  #v(0.2in)
  #text(size: 11pt, fill: rgb("#666666"))[{date}]
]

#v(0.3in)

= Quick Facts

#table(
  columns: (auto, 1fr),
  stroke: 0.5pt + rgb("#cccccc"),
  inset: 8pt,
  [*Project*], [{project_name}],
  [*Researcher*], [{author}],
  [*Ask*], [{funding_ask}],
  [*Timeline*], [{timeline}],
  [*Status*], [{status}],
)

#pagebreak()

= Executive Summary

{executive_summary}

= The Problem

{problem_statement}

= Our Solution

{solution}

= What We Need

{needs}

= Timeline & Milestones

{timeline_details}

= Budget Breakdown

{budget}

= Why Fund This?

{why_fund}

= About the Team

{team}

= Contact

{contact}

#v(0.5in)

#align(center)[
  #line(length: 30%, stroke: 0.5pt + rgb("#999999"))
  #v(0.1in)
  #text(size: 9pt, fill: rgb("#666666"))[
    Generated by {tool_name} (Level {level} {rarity})
    
    Genome: {genome}
  ]
]
'''

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GRANT PROPOSAL GENERATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class GrantProposalGenerator:
    """The evolving grant proposal tool."""
    
    STATE_FILE = Path(__file__).parent / ".grant_tool_state.json"
    
    def __init__(self):
        self.state = self._load_state()
    
    def _load_state(self) -> ToolState:
        """Load or create tool state."""
        if self.STATE_FILE.exists():
            with open(self.STATE_FILE) as f:
                data = json.load(f)
                return ToolState(**data)
        return ToolState()
    
    def _save_state(self):
        """Persist tool state."""
        with open(self.STATE_FILE, "w") as f:
            json.dump(asdict(self.state), f, indent=2)
    
    def generate_proposal(
        self,
        project_name: str,
        author: str = "Unknown",
        funding_ask: str = "TBD",
        problem: str = "",
        solution: str = "",
        output_path: Optional[Path] = None,
    ) -> Path:
        """Generate a grant proposal and gain XP."""
        
        # Fill in template
        content = TYPST_TONER_SAVER_TEMPLATE.format(
            title=f"{project_name} - Grant Proposal",
            tool_name=self.state.name,
            level=self.state.level,
            rarity=self.state.rarity.value,
            genome=self.state.genome_hash,
            project_name=project_name,
            subtitle="Community Support & Resource Request",
            author=author,
            date=datetime.now().strftime("%B %Y"),
            funding_ask=funding_ask,
            timeline="See Timeline section",
            status="Seeking Support",
            executive_summary=problem or "[Describe your project's core value proposition]",
            problem_statement=problem or "[Describe the problem you're solving]",
            solution=solution or "[Describe your solution]",
            needs="[List what you need: hardware, compute, expertise]",
            timeline_details="[Phase 1, Phase 2, Phase 3 with dates]",
            budget="[Breakdown of how funds/resources will be used]",
            why_fund="[Why should someone support this project?]",
            team="[Who is working on this?]",
            contact="[How to reach you]",
        )
        
        # Determine output path
        if output_path is None:
            safe_name = project_name.lower().replace(" ", "_")[:30]
            output_path = Path(f"{safe_name}_proposal.typ")
        
        # Write file
        output_path.write_text(content)
        
        # Gain XP
        xp_result = self.state.gain_xp(25, f"Generated proposal: {project_name}")
        self.state.proposals_generated += 1
        self.state.toner_saved_ml += 2.5  # Estimate: 2.5ml saved per toner-saver doc
        
        self._save_state()
        
        return output_path, xp_result
    
    def address_critique(self, critique_count: int = 1):
        """Gain XP for addressing critiques."""
        xp_result = self.state.gain_xp(
            critique_count * 15,
            f"Addressed {critique_count} critique(s)"
        )
        self.state.critiques_addressed += critique_count
        self._save_state()
        return xp_result
    
    def show_status(self) -> str:
        """Display current tool status."""
        rarity = self.state.rarity
        progress_bar_len = 20
        filled = int(self.state.xp_progress * progress_bar_len)
        bar = "█" * filled + "░" * (progress_bar_len - filled)
        
        # Next rarity threshold
        next_rarity = None
        for r in Rarity:
            if RARITY_XP_THRESHOLDS[r] > self.state.xp:
                next_rarity = r
                break
        
        next_rarity_xp = RARITY_XP_THRESHOLDS[next_rarity] if next_rarity else "MAX"
        
        status = f"""
╔══════════════════════════════════════════════════════════════╗
║  🏆 GRANT PROPOSAL GENERATOR                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Rarity: [{rarity.value.upper():^10}]                                    ║
║  Level:  {self.state.level:<3}                                            ║
║  XP:     {self.state.xp:,} / {next_rarity_xp}                              
║                                                              ║
║  Progress: [{bar}] {self.state.xp_progress*100:.1f}%              ║
║                                                              ║
║  Genome:  {self.state.genome_hash}                            ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  STATS                                                       ║
╠══════════════════════════════════════════════════════════════╣
║  Proposals Generated: {self.state.proposals_generated:<5}                            ║
║  Critiques Addressed: {self.state.critiques_addressed:<5}                            ║
║  Toner Saved:         {self.state.toner_saved_ml:.1f} ml                          ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  UNLOCKED ABILITIES                                          ║
╠══════════════════════════════════════════════════════════════╣
"""
        for ability in self.state.unlocked_abilities:
            status += f"║  ✓ {ability:<54} ║\n"
        
        # Show next unlock
        next_abilities = []
        for lvl, abilities in sorted(LEVEL_ABILITIES.items()):
            if lvl > self.state.level:
                for a in abilities:
                    if a not in self.state.unlocked_abilities:
                        next_abilities.append((lvl, a))
                break
        
        if next_abilities:
            status += "║                                                              ║\n"
            status += "║  NEXT UNLOCK                                                 ║\n"
            for lvl, ability in next_abilities[:2]:
                status += f"║  → Level {lvl}: {ability:<44} ║\n"
        
        status += """╚══════════════════════════════════════════════════════════════╝
"""
        return status
    
    def show_evolution_history(self) -> str:
        """Show evolution timeline."""
        if not self.state.evolution_history:
            return "No evolutions yet. Keep generating proposals!"
        
        history = "\n🧬 EVOLUTION HISTORY\n" + "=" * 40 + "\n"
        for event in self.state.evolution_history:
            history += f"\n{event['timestamp'][:10]}: {event['from_rarity']} → {event['to_rarity']} (XP: {event['xp']:,})"
        return history


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    parser = argparse.ArgumentParser(
        description="🏆 Grant Proposal Generator - The Evolving Pitch Machine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
            python grant_proposal_tool.py generate --project "WAFT" --author "ctavolazzi"
            python grant_proposal_tool.py status
            python grant_proposal_tool.py history
            python grant_proposal_tool.py critique --count 3
        """)
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a proposal")
    gen_parser.add_argument("--project", "-p", required=True, help="Project name")
    gen_parser.add_argument("--author", "-a", default="Unknown", help="Author name")
    gen_parser.add_argument("--ask", default="TBD", help="Funding ask")
    gen_parser.add_argument("--output", "-o", help="Output file path")
    
    # Status command
    subparsers.add_parser("status", help="Show tool status")
    
    # History command
    subparsers.add_parser("history", help="Show evolution history")
    
    # Critique command
    crit_parser = subparsers.add_parser("critique", help="Log addressed critiques")
    crit_parser.add_argument("--count", "-c", type=int, default=1, help="Number of critiques addressed")
    
    args = parser.parse_args()
    
    tool = GrantProposalGenerator()
    
    if args.command == "generate":
        output_path = Path(args.output) if args.output else None
        path, xp_result = tool.generate_proposal(
            project_name=args.project,
            author=args.author,
            funding_ask=args.ask,
            output_path=output_path,
        )
        print(f"\n✅ Proposal generated: {path}")
        print(f"📈 +{xp_result['xp_gained']} XP")
        if xp_result['level_ups']:
            print(f"🎉 LEVEL UP! Now level {xp_result['new_level']}")
        if xp_result['evolved']:
            print(f"🌟 EVOLVED! {xp_result['old_rarity'].value} → {xp_result['new_rarity'].value}")
        print(tool.show_status())
    
    elif args.command == "status":
        print(tool.show_status())
    
    elif args.command == "history":
        print(tool.show_evolution_history())
    
    elif args.command == "critique":
        xp_result = tool.address_critique(args.count)
        print(f"\n✅ Logged {args.count} critique(s) addressed")
        print(f"📈 +{xp_result['xp_gained']} XP")
        if xp_result['level_ups']:
            print(f"🎉 LEVEL UP! Now level {xp_result['new_level']}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
