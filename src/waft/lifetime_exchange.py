"""
Lifetime Exchange: Trading Mechanism

The Lifetime Exchange allows beings to:
- Trade lifetimes
- Share skills
- Exchange memories
- Transfer knowledge

Uses karma as currency and facilitates knowledge transfer between beings.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import json
import hashlib


class ExchangeType(Enum):
    """Type of exchange."""
    LIFETIME = "lifetime"  # Trade lifetimes
    SKILL = "skill"  # Share skills
    MEMORY = "memory"  # Exchange memories
    KNOWLEDGE = "knowledge"  # Transfer knowledge


class LifetimeExchange:
    """
    The Lifetime Exchange - trading mechanism for beings.
    
    Allows beings to:
    - Trade lifetimes
    - Share skills
    - Exchange memories
    - Transfer knowledge
    
    Uses karma as currency.
    """
    
    def __init__(
        self,
        project_path: Optional[Path] = None,
        karma_market: Optional[Any] = None
    ):
        """
        Initialize the Lifetime Exchange.
        
        Args:
            project_path: Path to project root
            karma_market: KarmaMarket instance
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.exchange_path = project_path / "_hidden" / ".truth" / "exchange"
        self.exchange_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize KarmaMarket
        if karma_market is None:
            from .karma_market import KarmaMarket
            self.karma_market = KarmaMarket(project_path=project_path)
        else:
            self.karma_market = karma_market
    
    def list_offerings(
        self,
        exchange_type: Optional[ExchangeType] = None,
        being_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List available offerings on the exchange.
        
        Args:
            exchange_type: Optional filter by type
            being_id: Optional filter by being
            
        Returns:
            List of offerings
        """
        offerings_file = self.exchange_path / "offerings.json"
        if not offerings_file.exists():
            return []
        
        with open(offerings_file, "r") as f:
            all_offerings = json.load(f).get("offerings", [])
        
        # Filter
        offerings = all_offerings
        if exchange_type:
            offerings = [o for o in offerings if o.get("type") == exchange_type.value]
        if being_id:
            offerings = [o for o in offerings if o.get("being_id") == being_id]
        
        return offerings
    
    def create_offering(
        self,
        being_id: str,
        exchange_type: ExchangeType,
        offering_data: Dict[str, Any],
        karma_price: float
    ) -> Dict[str, Any]:
        """
        Create an offering on the exchange.
        
        Args:
            being_id: Being making the offering
            exchange_type: Type of offering
            offering_data: Data for the offering
            karma_price: Karma price
            
        Returns:
            Offering record
        """
        offering_id = f"offering_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.sha256(f'{being_id}{exchange_type.value}'.encode()).hexdigest()[:8]}"
        
        offering = {
            "offering_id": offering_id,
            "being_id": being_id,
            "type": exchange_type.value,
            "data": offering_data,
            "karma_price": karma_price,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Add to offerings
        offerings_file = self.exchange_path / "offerings.json"
        if offerings_file.exists():
            with open(offerings_file, "r") as f:
                data = json.load(f)
        else:
            data = {"offerings": []}
        
        data["offerings"].append(offering)
        
        with open(offerings_file, "w") as f:
            json.dump(data, f, indent=2)
        
        return offering
    
    def purchase_offering(
        self,
        offering_id: str,
        buyer_being_id: str
    ) -> Dict[str, Any]:
        """
        Purchase an offering from the exchange.
        
        Args:
            offering_id: Offering identifier
            buyer_being_id: Being making the purchase
            
        Returns:
            Purchase record
        """
        # Find offering
        offerings = self.list_offerings()
        offering = next((o for o in offerings if o["offering_id"] == offering_id), None)
        
        if not offering:
            raise ValueError(f"Offering not found: {offering_id}")
        
        if offering["status"] != "active":
            raise ValueError(f"Offering not active: {offering_id}")
        
        # Check karma balance
        current_karma = self.karma_market._get_soul_karma(buyer_being_id)
        if current_karma < offering["karma_price"]:
            from .karma import InsufficientKarmaError
            raise InsufficientKarmaError(
                f"Insufficient karma: {current_karma} < {offering['karma_price']}"
            )
        
        # Deduct karma
        self.karma_market._deduct_karma(
            buyer_being_id,
            offering["karma_price"],
            reason=f"Purchased offering: {offering_id}"
        )
        
        # Award karma to seller
        seller_being_id = offering["being_id"]
        self.karma_market._award_karma(
            seller_being_id,
            offering["karma_price"],
            reason=f"Sold offering: {offering_id}"
        )
        
        # Mark offering as sold
        offering["status"] = "sold"
        offering["sold_to"] = buyer_being_id
        offering["sold_at"] = datetime.now().isoformat()
        
        # Update offerings file
        offerings_file = self.exchange_path / "offerings.json"
        with open(offerings_file, "w") as f:
            json.dump({"offerings": offerings}, f, indent=2)
        
        return {
            "offering_id": offering_id,
            "buyer_being_id": buyer_being_id,
            "seller_being_id": seller_being_id,
            "karma_price": offering["karma_price"],
            "purchased_at": datetime.now().isoformat(),
            "offering_data": offering["data"]
        }
    
    def _award_karma(self, being_id: str, amount: float, reason: str = "") -> None:
        """Award karma to being."""
        # TODO: Implement actual karma award
        pass
