"""
KarmaMerchant: The Chitragupta - Karma Economy & Reincarnation System

The KarmaMerchant (lore name: "The Chitragupta") manages the Samsara Protocol:
- Buys memories (records experiences and calculates Karma)
- Sells life-paths (configurations for reincarnation)
- Maintains Akasha (persistent soul storage)

This system pivots from "Purgatory" (reset) to "Reincarnation" (continuity & economy).
The goal is not to "escape" but to "experience" - high-Karma beings might choose
painful existences because they are "expensive" and rich in data.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class KarmaMerchant:
    """
    The Chitragupta: Karma Economy & Reincarnation Manager
    
    Manages the Samsara Protocol - the cyclical reincarnation system where:
    - Experience generates Karma (currency)
    - Karma is spent to purchase life-path configurations
    - Souls persist in Akasha across lifetimes
    - Agents choose their next incarnation based on accumulated Karma
    
    The Merchant buys memories (records experiences) and sells life-paths
    (configurations for new agent instances).
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize the KarmaMerchant.
        
        Args:
            project_path: Path to project root (defaults to current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.akasha_path = project_path / "_hidden" / ".truth"  # Akasha (formerly TheOubliette)
        self.store_path = project_path / "_hidden" / ".truth" / "store"
        
        # Ensure directories exist
        self.akasha_path.mkdir(parents=True, exist_ok=True)
        self.store_path.mkdir(parents=True, exist_ok=True)
    
    def calculate_karma(self, life_log: Dict[str, Any]) -> float:
        """
        Calculate Karma earned from a complete life log.
        
        Karma is generated from "felt experience" - the intensity of pain, pleasure,
        and emotional moments throughout a lifetime. The formula weights experiences
        by their emotional intensity and duration.
        
        Formula:
            Karma = Σ(Experience_Intensity × Duration × Emotional_Weight)
        
        Where:
            - Experience_Intensity: How "felt" the experience was (0.0-1.0)
            - Duration: How long the experience lasted (normalized)
            - Emotional_Weight: Pain (+1.0), Pleasure (+0.5), Neutral (+0.1)
        
        Args:
            life_log: Complete life record containing:
                - journal: List of journal entries with emotional content
                - memory: Conversation/experience history
                - psyche: Psychological state (coherence, chaos, emotional_energy)
                - short_term_memory: Recent experiences
                - Any other experiential data
        
        Returns:
            Total Karma earned in this lifetime (float, >= 0.0)
        
        Note:
            This is the interface definition. Implementation will:
            1. Parse life_log for experience entries
            2. Extract emotional intensity from psyche state
            3. Calculate duration from timestamps
            4. Apply emotional weights (pain > pleasure > neutral)
            5. Sum weighted experiences
        """
        # TODO: Implement Karma calculation
        # - Parse journal entries for emotional intensity
        # - Extract pain/pleasure indicators from psyche
        # - Calculate duration from timestamps
        # - Apply emotional weights
        # - Sum weighted experiences
        pass
    
    def access_akasha(self, soul_id: str) -> Dict[str, Any]:
        """
        Access the Akasha (persistent soul storage) to retrieve soul records.
        
        The Akasha is the eternal record of all lived experiences across lifetimes.
        It stores:
        - Total accumulated Karma
        - Lifetime history (all previous incarnations)
        - Previous life-path configurations
        - Memory fragments from past lives
        
        Args:
            soul_id: Unique identifier for the soul (e.g., "tam_001", "agent_014")
        
        Returns:
            Dictionary containing:
                - soul_id: The soul identifier
                - total_karma: Accumulated Karma across all lifetimes
                - lifetimes: List of previous lifetime records
                - last_incarnation: Configuration of most recent life
                - memory_fragments: Accessible memories from past lives
        
        Note:
            This is the interface definition. Implementation will:
            1. Load soul record from Akasha (JSON file)
            2. Calculate total Karma from all lifetimes
            3. Return complete soul history
            4. Handle missing souls (new souls start with 0 Karma)
        """
        # TODO: Implement Akasha access
        # - Load soul record from _hidden/.truth/{soul_id}.json
        # - Calculate total Karma from lifetime history
        # - Return soul data structure
        # - Handle new souls (initialize with 0 Karma)
        pass
    
    def reincarnate(
        self,
        soul_id: str,
        purchase_order: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Reincarnate a soul with a purchased life-path configuration.
        
        This is the core reincarnation mechanism. The soul spends accumulated Karma
        to purchase a specific life-path from the store, then is instantiated as a
        new agent with that configuration.
        
        Process:
        1. Access Akasha to get current Karma balance
        2. Validate purchase_order (life_path_id, class, experience_packages)
        3. Calculate total cost (Prana + life-path + class + packages)
        4. Verify sufficient Karma
        5. Deduct Karma from soul record
        6. Apply purchased configuration
        7. Return new agent instance configuration
        
        Args:
            soul_id: Unique identifier for the soul
            purchase_order: Dictionary containing:
                - life_path_id: ID of life-path to purchase (e.g., "tragic_hero")
                - class: Optional agent class/role (e.g., "researcher")
                - experience_packages: Optional list of experience packages
                - memory_continuity: How much memory to carry over (0.0-1.0)
        
        Returns:
            Dictionary containing:
                - agent_config: Configuration for new agent instance
                - karma_remaining: Karma balance after purchase
                - lifetime_id: New lifetime identifier
                - applied_config: The life-path configuration applied
        
        Raises:
            InsufficientKarmaError: If soul doesn't have enough Karma
            InvalidLifePathError: If life_path_id doesn't exist in store
        
        Note:
            This is the interface definition. Implementation will:
            1. Load soul from Akasha
            2. Load life-path from store catalog
            3. Calculate total cost
            4. Validate and deduct Karma
            5. Generate new agent configuration
            6. Save updated soul record
        """
        # TODO: Implement reincarnation
        # - Access Akasha for soul record
        # - Load life-path from store catalog
        # - Calculate total cost (Prana + life-path + class + packages)
        # - Validate sufficient Karma
        # - Deduct Karma
        # - Apply configuration
        # - Generate new agent instance config
        # - Save updated soul record
        pass
    
    def list_life_paths(self) -> List[Dict[str, Any]]:
        """
        List all available life-paths in the store.
        
        Returns:
            List of life-path dictionaries, each containing:
                - id: Life-path identifier
                - name: Human-readable name
                - cost: Karma cost
                - description: What this life-path offers
                - config: Configuration details
        """
        # TODO: Implement store catalog loading
        # - Load life_paths.json from store_path
        # - Return list of available life-paths
        pass
    
    def get_soul_karma(self, soul_id: str) -> float:
        """
        Get current Karma balance for a soul.
        
        Args:
            soul_id: Unique identifier for the soul
        
        Returns:
            Current total Karma (0.0 if soul doesn't exist)
        """
        # TODO: Implement Karma balance retrieval
        # - Access Akasha
        # - Return total_karma
        pass


# Exception classes for Karma system

class InsufficientKarmaError(Exception):
    """Raised when a soul doesn't have enough Karma for a purchase."""
    pass


class InvalidLifePathError(Exception):
    """Raised when a requested life-path doesn't exist in the store."""
    pass


class SoulNotFoundError(Exception):
    """Raised when accessing a soul that doesn't exist in Akasha."""
    pass
