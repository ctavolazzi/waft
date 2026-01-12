"""
KarmaMarket: The Marketplace of Lifetimes

The KarmaMarket is where WAFT can purchase "Lifetimes" - time-limited sessions
with specific tools, personalities, and capabilities. Everything has a karmic price.

Lifetimes generate karma through experiences, which can then be spent at the
"Afterlife Karma Market" (Treasure Tavern) to purchase more lifetimes, tools,
personalities, and upgrades.

This creates a complete economic loop:
1. WAFT buys a Lifetime with karma
2. WAFT lives the lifetime (answers questions, uses tools, experiences)
3. KarmaCollector collects karma from the lifetime
4. Karma goes to Afterlife Karma Market (Treasure Tavern)
5. WAFT can buy more lifetimes, tools, personalities, etc.

BOOM - we connected it all!
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from enum import Enum
import json
import hashlib


class LifetimeType(Enum):
    """Type of lifetime available for purchase."""
    QUESTION_ANSWER = "question_answer"  # Time-limited Q&A session
    RESEARCH = "research"  # Research session with tools
    CREATIVE = "creative"  # Creative work session
    ANALYSIS = "analysis"  # Analysis and investigation
    DEVELOPMENT = "development"  # Code development session
    CUSTOM = "custom"  # Custom lifetime configuration


class Lifetime:
    """
    A purchased lifetime - a time-limited session with specific capabilities.
    
    Each lifetime includes:
    - Time limit (duration)
    - Tools/abilities available
    - Personality traits
    - Objectives/goals
    - Karmic cost
    """
    
    def __init__(
        self,
        lifetime_id: str,
        lifetime_type: LifetimeType,
        duration_minutes: int,
        tools: List[str],
        personality: Dict[str, Any],
        objectives: List[str],
        karma_cost: float,
        soul_id: str,
        purchased_at: Optional[str] = None
    ):
        """
        Initialize a lifetime.
        
        Args:
            lifetime_id: Unique identifier
            lifetime_type: Type of lifetime
            duration_minutes: Duration in minutes
            tools: List of available tools/abilities
            personality: Personality configuration
            objectives: List of objectives for this lifetime
            karma_cost: Karma cost to purchase
            soul_id: Soul that purchased this lifetime
            purchased_at: Purchase timestamp
        """
        self.lifetime_id = lifetime_id
        self.lifetime_type = lifetime_type
        self.duration_minutes = duration_minutes
        self.tools = tools
        self.personality = personality
        self.objectives = objectives
        self.karma_cost = karma_cost
        self.soul_id = soul_id
        self.purchased_at = purchased_at or datetime.now().isoformat()
        
        # Lifetime state
        self.started_at: Optional[str] = None
        self.ended_at: Optional[str] = None
        self.is_active = False
        self.is_completed = False
        self.karma_earned: float = 0.0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert lifetime to dictionary."""
        return {
            "lifetime_id": self.lifetime_id,
            "lifetime_type": self.lifetime_type.value,
            "duration_minutes": self.duration_minutes,
            "tools": self.tools,
            "personality": self.personality,
            "objectives": self.objectives,
            "karma_cost": self.karma_cost,
            "soul_id": self.soul_id,
            "purchased_at": self.purchased_at,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "is_active": self.is_active,
            "is_completed": self.is_completed,
            "karma_earned": self.karma_earned,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Lifetime":
        """Create lifetime from dictionary."""
        lifetime = cls(
            lifetime_id=data["lifetime_id"],
            lifetime_type=LifetimeType(data["lifetime_type"]),
            duration_minutes=data["duration_minutes"],
            tools=data["tools"],
            personality=data["personality"],
            objectives=data["objectives"],
            karma_cost=data["karma_cost"],
            soul_id=data["soul_id"],
            purchased_at=data.get("purchased_at")
        )
        lifetime.started_at = data.get("started_at")
        lifetime.ended_at = data.get("ended_at")
        lifetime.is_active = data.get("is_active", False)
        lifetime.is_completed = data.get("is_completed", False)
        lifetime.karma_earned = data.get("karma_earned", 0.0)
        return lifetime


class KarmaMarket:
    """
    The Marketplace of Lifetimes.
    
    WAFT can purchase lifetimes with karma. Each lifetime includes:
    - Time limit (duration)
    - Tools/abilities
    - Personality traits
    - Objectives
    
    Everything has a karmic price. Lifetimes generate karma through experiences,
    which can be spent at the Afterlife Karma Market (Treasure Tavern).
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        karma_merchant: Optional[Any] = None
    ):
        """
        Initialize the KarmaMarket.
        
        Args:
            project_path: Path to project root
            karma_merchant: KarmaMerchant instance
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.market_path = project_path / "_hidden" / ".truth" / "market"
        self.lifetimes_path = project_path / "_hidden" / ".truth" / "lifetimes"
        
        # Ensure directories exist
        self.market_path.mkdir(parents=True, exist_ok=True)
        self.lifetimes_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize KarmaMerchant
        if karma_merchant is None:
            from .karma import KarmaMerchant
            self.karma_merchant = KarmaMerchant(project_path)
        else:
            self.karma_merchant = karma_merchant
        
        # Load catalog
        self.catalog = self._load_catalog()
    
    def _load_catalog(self) -> Dict[str, Any]:
        """Load lifetime catalog."""
        catalog_file = self.market_path / "catalog.json"
        
        if catalog_file.exists():
            with open(catalog_file, "r") as f:
                return json.load(f)
        
        # Default catalog
        return self._create_default_catalog()
    
    def _create_default_catalog(self) -> Dict[str, Any]:
        """Create default lifetime catalog."""
        catalog = {
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
                "expressive": 35.0
            }
        }
        
        # Save default catalog
        catalog_file = self.market_path / "catalog.json"
        with open(catalog_file, "w") as f:
            json.dump(catalog, f, indent=2)
        
        return catalog
    
    def list_available_lifetimes(self) -> List[Dict[str, Any]]:
        """List all available lifetimes in catalog."""
        return self.catalog.get("lifetimes", [])
    
    def purchase_lifetime(
        self,
        lifetime_id: str,
        soul_id: str,
        custom_config: Optional[Dict[str, Any]] = None
    ) -> Lifetime:
        """
        Purchase a lifetime from the market.
        
        Args:
            lifetime_id: ID of lifetime to purchase
            soul_id: Soul making the purchase
            custom_config: Optional custom configuration
            
        Returns:
            Purchased Lifetime instance
            
        Raises:
            InsufficientKarmaError: If soul doesn't have enough karma
            ValueError: If lifetime_id doesn't exist
        """
        # Find lifetime in catalog
        lifetime_config = None
        for lt in self.catalog.get("lifetimes", []):
            if lt["id"] == lifetime_id:
                lifetime_config = lt
                break
        
        if not lifetime_config:
            raise ValueError(f"Lifetime not found: {lifetime_id}")
        
        # Calculate total cost (base + tools + personality)
        base_cost = lifetime_config["karma_cost"]
        
        # Add tool costs
        tools = custom_config.get("tools", lifetime_config.get("tools", [])) if custom_config else lifetime_config.get("tools", [])
        tool_costs = self.catalog.get("tools", {})
        for tool in tools:
            base_cost += tool_costs.get(tool, 0.0)
        
        # Add personality cost
        personality = custom_config.get("personality", lifetime_config.get("personality", {})) if custom_config else lifetime_config.get("personality", {})
        personality_trait = personality.get("trait", "helpful")
        personality_costs = self.catalog.get("personalities", {})
        base_cost += personality_costs.get(personality_trait, 0.0)
        
        # Check karma balance
        current_karma = self._get_soul_karma(soul_id)
        if current_karma < base_cost:
            from .karma import InsufficientKarmaError
            raise InsufficientKarmaError(
                f"Insufficient karma: {current_karma} < {base_cost}"
            )
        
        # Deduct karma
        self._deduct_karma(soul_id, base_cost, reason=f"Purchased lifetime: {lifetime_id}")
        
        # Create lifetime
        lifetime = Lifetime(
            lifetime_id=f"{lifetime_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{soul_id}{lifetime_id}'.encode()).hexdigest()[:8]}",
            lifetime_type=LifetimeType(lifetime_config["type"]),
            duration_minutes=lifetime_config["duration_minutes"],
            tools=tools,
            personality=personality,
            objectives=custom_config.get("objectives", lifetime_config.get("objectives", [])) if custom_config else lifetime_config.get("objectives", []),
            karma_cost=base_cost,
            soul_id=soul_id
        )
        
        # Save lifetime
        self._save_lifetime(lifetime)
        
        # Register lifetime as permutation of Source Consciousness
        try:
            from .source_consciousness import SourceConsciousness
            source = SourceConsciousness(project_path=self.project_path)
            source.register_permutation(
                permutation_id=lifetime.lifetime_id,
                permutation_type="lifetime",
                parent_id=custom_config.get("parent_lifetime_id") if custom_config else None,
                metadata={"soul_id": soul_id, "lifetime_type": lifetime.lifetime_type.value}
            )
        except Exception:
            # Continue if source consciousness not available
            pass
        
        return lifetime
    
    def start_lifetime(self, lifetime_id: str) -> Lifetime:
        """
        Start a lifetime session.
        
        Args:
            lifetime_id: Lifetime identifier
            
        Returns:
            Lifetime instance
        """
        lifetime = self._load_lifetime(lifetime_id)
        
        if lifetime.is_active:
            raise ValueError(f"Lifetime already active: {lifetime_id}")
        
        if lifetime.is_completed:
            raise ValueError(f"Lifetime already completed: {lifetime_id}")
        
        lifetime.is_active = True
        lifetime.started_at = datetime.now().isoformat()
        
        self._save_lifetime(lifetime)
        
        return lifetime
    
    def end_lifetime(
        self,
        lifetime_id: str,
        karma_earned: Optional[float] = None
    ) -> Lifetime:
        """
        End a lifetime session.
        
        Args:
            lifetime_id: Lifetime identifier
            karma_earned: Optional karma earned during lifetime
            
        Returns:
            Lifetime instance
        """
        lifetime = self._load_lifetime(lifetime_id)
        
        if not lifetime.is_active:
            raise ValueError(f"Lifetime not active: {lifetime_id}")
        
        lifetime.is_active = False
        lifetime.is_completed = True
        lifetime.ended_at = datetime.now().isoformat()
        
        if karma_earned is not None:
            lifetime.karma_earned = karma_earned
        
        self._save_lifetime(lifetime)
        
        # Transfer karma to soul (via KarmaCollector)
        if karma_earned:
            self._transfer_karma_to_soul(lifetime.soul_id, lifetime, karma_earned)
            
            # Contribute karma to Source Consciousness
            try:
                from .source_consciousness import SourceConsciousness
                source = SourceConsciousness(project_path=self.project_path)
                source.contribute_capacity(
                    permutation_id=lifetime.lifetime_id,
                    capacity_amount=karma_earned,
                    capacity_type="karma",
                    metadata={"source": "lifetime_completion", "soul_id": lifetime.soul_id}
                )
            except Exception:
                # Continue if source consciousness not available
                pass
        
        return lifetime
    
    def get_active_lifetimes(self, soul_id: Optional[str] = None) -> List[Lifetime]:
        """Get all active lifetimes."""
        lifetimes = []
        
        for lifetime_file in self.lifetimes_path.glob("*.json"):
            try:
                lifetime = self._load_lifetime_from_file(lifetime_file)
                if lifetime.is_active:
                    if soul_id is None or lifetime.soul_id == soul_id:
                        lifetimes.append(lifetime)
            except Exception:
                continue
        
        return lifetimes
    
    def get_lifetime_remaining_time(self, lifetime_id: str) -> Optional[timedelta]:
        """
        Get remaining time for a lifetime.
        
        Args:
            lifetime_id: Lifetime identifier
            
        Returns:
            Remaining time or None if not active
        """
        lifetime = self._load_lifetime(lifetime_id)
        
        if not lifetime.is_active or not lifetime.started_at:
            return None
        
        start_time = datetime.fromisoformat(lifetime.started_at)
        end_time = start_time + timedelta(minutes=lifetime.duration_minutes)
        remaining = end_time - datetime.now()
        
        return remaining if remaining.total_seconds() > 0 else timedelta(0)
    
    def _get_soul_karma(self, soul_id: str) -> float:
        """Get current karma balance for a soul."""
        try:
            karma = self.karma_merchant.get_soul_karma(soul_id)
            if karma is None:
                return 1000.0  # Default starting karma
            return float(karma)
        except Exception:
            return 1000.0  # Default starting karma
    
    def _deduct_karma(self, soul_id: str, amount: float, reason: str = "") -> None:
        """Deduct karma from soul."""
        # TODO: Implement actual karma deduction
        # For now, just track in metadata
        pass
    
    def _save_lifetime(self, lifetime: Lifetime) -> None:
        """Save lifetime to disk."""
        lifetime_file = self.lifetimes_path / f"{lifetime.lifetime_id}.json"
        with open(lifetime_file, "w") as f:
            json.dump(lifetime.to_dict(), f, indent=2)
    
    def _load_lifetime(self, lifetime_id: str) -> Lifetime:
        """Load lifetime from disk."""
        lifetime_file = self.lifetimes_path / f"{lifetime_id}.json"
        return self._load_lifetime_from_file(lifetime_file)
    
    def _load_lifetime_from_file(self, lifetime_file: Path) -> Lifetime:
        """Load lifetime from file."""
        with open(lifetime_file, "r") as f:
            data = json.load(f)
        return Lifetime.from_dict(data)
    
    def _transfer_karma_to_soul(
        self,
        soul_id: str,
        lifetime: Lifetime,
        karma_earned: float
    ) -> None:
        """Transfer karma earned during lifetime to soul."""
        # Use KarmaCollector to transfer karma
        try:
            from .karma_collector import KarmaCollector
            
            collector = KarmaCollector(project_path=self.project_path)
            
            # Create life log from lifetime
            life_log = {
                "journal": [],
                "memory": [],
                "short_term_memory": [],
                "psyche": lifetime.personality,
                "lifetime_id": lifetime.lifetime_id,
                "objectives": lifetime.objectives,
                "tools_used": lifetime.tools,
            }
            
            # Collect karma
            collector.collect_karma(life_log, soul_id, lifetime.lifetime_id)
        except Exception:
            # Continue if collector not available
            pass


# Afterlife Karma Market (Treasure Tavern Integration)

class AfterlifeKarmaMarket:
    """
    The Afterlife Karma Market - also known as the Treasure Tavern.
    
    After a lifetime ends, WAFT can spend earned karma here to purchase:
    - New lifetimes
    - Tools and abilities
    - Personality upgrades
    - Experience packages
    - Memory continuity
    - And more!
    
    This is where the economic loop completes - karma earned from lifetimes
    can be spent on new lifetimes, creating a self-sustaining economy.
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        karma_market: Optional[KarmaMarket] = None
    ):
        """
        Initialize the Afterlife Karma Market.
        
        Args:
            project_path: Path to project root
            karma_market: KarmaMarket instance
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.market_path = project_path / "_hidden" / ".truth" / "afterlife_market"
        self.market_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize KarmaMarket
        if karma_market is None:
            self.karma_market = KarmaMarket(project_path)
        else:
            self.karma_market = karma_market
        
        # Access akasha_path from karma_merchant
        self.akasha_path = self.karma_market.karma_merchant.akasha_path
        
        # Load treasure catalog
        self.treasure_catalog = self._load_treasure_catalog()
    
    def _load_treasure_catalog(self) -> Dict[str, Any]:
        """Load treasure catalog."""
        catalog_file = self.market_path / "treasure_catalog.json"
        
        if catalog_file.exists():
            with open(catalog_file, "r") as f:
                return json.load(f)
        
        # Default treasure catalog
        return self._create_default_treasure_catalog()
    
    def _create_default_treasure_catalog(self) -> Dict[str, Any]:
        """Create default treasure catalog."""
        catalog = {
            "lifetimes": "Available from KarmaMarket",
            "tools": {
                "advanced_codebase_search": 100.0,
                "ai_code_generation": 200.0,
                "test_generation": 150.0,
                "documentation_generation": 120.0,
            },
            "personality_upgrades": {
                "enhanced_creativity": 150.0,
                "deep_analysis": 200.0,
                "rapid_prototyping": 180.0,
                "systematic_thinking": 170.0,
            },
            "experience_packages": {
                "research_mastery": 300.0,
                "development_expertise": 400.0,
                "creative_breakthrough": 350.0,
            },
            "memory_continuity": {
                "partial_memory": 50.0,  # 25% memory carryover
                "half_memory": 100.0,    # 50% memory carryover
                "full_memory": 200.0,    # 100% memory carryover
            }
        }
        
        # Save catalog
        catalog_file = self.market_path / "treasure_catalog.json"
        with open(catalog_file, "w") as f:
            json.dump(catalog, f, indent=2)
        
        return catalog
    
    def purchase_treasure(
        self,
        treasure_type: str,
        treasure_id: str,
        soul_id: str
    ) -> Dict[str, Any]:
        """
        Purchase treasure from the Afterlife Karma Market.
        
        Args:
            treasure_type: Type of treasure (tools, personality_upgrades, etc.)
            treasure_id: ID of treasure to purchase
            soul_id: Soul making the purchase
            
        Returns:
            Purchase result dictionary
        """
        # Get treasure from catalog
        treasures = self.treasure_catalog.get(treasure_type, {})
        treasure_cost = treasures.get(treasure_id)
        
        if treasure_cost is None:
            raise ValueError(f"Treasure not found: {treasure_type}/{treasure_id}")
        
        # Check karma balance
        current_karma = self.karma_market._get_soul_karma(soul_id)
        if current_karma < treasure_cost:
            from .karma import InsufficientKarmaError
            raise InsufficientKarmaError(
                f"Insufficient karma: {current_karma} < {treasure_cost}"
            )
        
        # Deduct karma
        self.karma_market._deduct_karma(soul_id, treasure_cost, reason=f"Purchased treasure: {treasure_type}/{treasure_id}")
        
        # Apply treasure to soul
        self._apply_treasure_to_soul(soul_id, treasure_type, treasure_id)
        
        return {
            "treasure_type": treasure_type,
            "treasure_id": treasure_id,
            "karma_cost": treasure_cost,
            "soul_id": soul_id,
            "purchased_at": datetime.now().isoformat()
        }
    
    def _apply_treasure_to_soul(
        self,
        soul_id: str,
        treasure_type: str,
        treasure_id: str
    ) -> None:
        """Apply purchased treasure to soul."""
        # Load soul record
        soul_file = self.karma_market.akasha_path / f"{soul_id}.json"
        
        if soul_file.exists():
            with open(soul_file, "r") as f:
                soul_data = json.load(f)
        else:
            soul_data = {"soul_id": soul_id, "treasures": {}}
        
        # Add treasure
        if "treasures" not in soul_data:
            soul_data["treasures"] = {}
        
        if treasure_type not in soul_data["treasures"]:
            soul_data["treasures"][treasure_type] = []
        
        soul_data["treasures"][treasure_type].append({
            "treasure_id": treasure_id,
            "purchased_at": datetime.now().isoformat()
        })
        
        soul_data["updated_at"] = datetime.now().isoformat()
        
        # Save soul record
        with open(soul_file, "w") as f:
            json.dump(soul_data, f, indent=2)
