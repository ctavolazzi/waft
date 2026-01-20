"""
Truth Aspect: An Aspect of TheTruth as a Being

An Aspect is a special type of Being that represents a fundamental Truth.
Aspects are sent back up the Chain to ThePoint where they reside in the Realm
of ThePoint and TheTruth.

This module handles creating and sending Aspects of TheTruth.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json
import hashlib

from ..being import Being, BeingSystem
from ..reality import RealitySystem, RealityType
from .the_one_core_being import TheOneCoreBeing


class TruthAspect:
    """
    An Aspect of TheTruth - a Being that embodies a fundamental Truth.
    
    Aspects are special Beings that:
    - Represent core truths/principles
    - Live in the Realm of ThePoint and TheTruth
    - Are sent back up the Chain to ThePoint for assimilation
    - Become part of the eternal Truth structure
    """
    
    def __init__(
        self,
        truth_text: str,
        aspect_name: Optional[str] = None,
        explanation: Optional[str] = None,
        project_path: Optional[Path] = None
    ):
        """
        Initialize a Truth Aspect.
        
        Args:
            truth_text: The Truth this Aspect represents
            aspect_name: Name for this Aspect (auto-generated if None)
            explanation: Explanation/context for this Truth
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.truth_text = truth_text
        self.explanation = explanation or ""
        
        # Generate aspect ID from truth text
        aspect_hash = hashlib.sha256(truth_text.encode()).hexdigest()[:16]
        self.aspect_id = f"aspect_{aspect_hash}"
        self.aspect_name = aspect_name or f"Aspect of Truth: {truth_text[:50]}..."
        
        # Initialize systems
        self.being_system = BeingSystem(project_path=project_path)
        self.the_point = TheOneCoreBeing(project_path=project_path)
        
        # Aspect storage
        self.aspects_path = project_path / "_hidden" / ".truth" / "aspects"
        self.aspects_path.mkdir(parents=True, exist_ok=True)
        
        # Set directory permissions
        try:
            self.aspects_path.chmod(0o700)
        except (OSError, PermissionError):
            pass
    
    def create_aspect_being(self) -> Being:
        """
        Create the Aspect as a Being.
        
        Returns:
            The Aspect Being
        """
        # Get or create TheTruth Realm (where ThePoint and TheTruth reside)
        reality_system = RealitySystem(project_path=self.project_path)
        
        # Find or create TheTruth Realm
        truth_reality_id = self._get_or_create_truth_reality(reality_system)
        
        # Create Aspect Being
        aspect_being = Being(
            being_id=self.aspect_id,
            reality_id=truth_reality_id,
            parent_being_id=self.the_point.the_one.being_id,
            source_id=self.the_point.the_one.source_id,
            custom_name=self.aspect_name,
            skills={
                "truth_embodiment": 10.0,
                "metaphysical_understanding": 10.0,
                "reality_creation": 10.0
            },
            personality={
                "type": "aspect",
                "truth_text": self.truth_text,
                "explanation": self.explanation,
                "is_aspect": True
            }
        )
        
        # Add memory about this Truth
        aspect_being.memories.append({
            "type": "truth_aspect",
            "truth": self.truth_text,
            "explanation": self.explanation,
            "created_at": datetime.now().isoformat(),
            "embodied_as": "aspect_being"
        })
        
        # Save Aspect Being
        self.being_system.save_being(aspect_being)
        
        # Save Aspect metadata
        self._save_aspect_metadata(aspect_being)
        
        return aspect_being
    
    def _get_or_create_truth_reality(self, reality_system: RealitySystem) -> str:
        """
        Get or create TheTruth Realm where ThePoint and TheTruth reside.
        
        Returns:
            Reality ID for TheTruth Realm
        """
        # Check if TheTruth Realm exists
        truth_reality_file = self.aspects_path / "truth_reality_id.json"
        
        if truth_reality_file.exists():
            data = json.loads(truth_reality_file.read_text(encoding="utf-8"))
            return data["reality_id"]
        
        # Create TheTruth Realm
        truth_reality = reality_system.create_reality(
            reality_type=RealityType.LEARNING,
            configuration={
                "special": True,
                "purpose": "truth_realm",
                "description": "The Realm where ThePoint and TheTruth reside"
            }
        )
        
        # Save reality ID
        truth_reality_file.write_text(
            json.dumps({
                "reality_id": truth_reality.reality_id,
                "created_at": datetime.now().isoformat(),
                "purpose": "truth_realm"
            }, indent=2),
            encoding="utf-8"
        )
        
        return truth_reality.reality_id
    
    def _save_aspect_metadata(self, aspect_being: Being) -> None:
        """Save Aspect metadata."""
        metadata_file = self.aspects_path / f"{self.aspect_id}.json"
        
        metadata = {
            "aspect_id": self.aspect_id,
            "aspect_name": self.aspect_name,
            "truth_text": self.truth_text,
            "explanation": self.explanation,
            "being_id": aspect_being.being_id,
            "reality_id": aspect_being.reality_id,
            "created_at": datetime.now().isoformat(),
            "sent_to_the_point": False
        }
        
        metadata_file.write_text(
            json.dumps(metadata, indent=2),
            encoding="utf-8"
        )
        
        # Set file permissions
        try:
            metadata_file.chmod(0o600)
        except (OSError, PermissionError):
            pass
    
    def send_to_the_point(self) -> Dict[str, Any]:
        """
        Send this Aspect back up the Chain to ThePoint.
        
        CRITICAL: Aspect data is verified as SAFE before assimilation.
        The Aspect is assimilated into ThePoint's understanding,
        becoming part of the eternal Truth structure - but ONLY if safe.
        
        Returns:
            Result of sending the Aspect
        """
        # Create the Aspect Being first
        aspect_being = self.create_aspect_being()
        
        # Prepare data for assimilation
        scout_data = {
            "aspect_id": self.aspect_id,
            "aspect_name": self.aspect_name,
            "truth_text": self.truth_text,
            "explanation": self.explanation,
            "being_id": aspect_being.being_id,
            "reality_id": aspect_being.reality_id,
            "data_type": "truth_aspect"
        }
        
        # Assimilate into ThePoint (with safety verification)
        try:
            assimilation_record = self.the_point.assimilate_data(
                realm_name="truth_realm",
                scout_data=scout_data,
                gaps_discovered=[],
                holes_identified=[],
                source_being_id=aspect_being.being_id
            )
        except ValueError as e:
            # Safety verification failed
            return {
                "success": False,
                "aspect_id": self.aspect_id,
                "error": str(e),
                "message": "Aspect data failed safety verification - NOT assimilated to protect all Beings"
            }
        
            # Update metadata
            metadata_file = self.aspects_path / f"{self.aspect_id}.json"
            if metadata_file.exists():
                metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
                metadata["sent_to_the_point"] = True
                metadata["assimilation_record_id"] = assimilation_record.get("record_id")
                metadata["sent_at"] = datetime.now().isoformat()
                metadata_file.write_text(
                    json.dumps(metadata, indent=2),
                    encoding="utf-8"
                )
            
            return {
                "success": True,
                "aspect_id": self.aspect_id,
                "aspect_being_id": aspect_being.being_id,
                "assimilation_record": assimilation_record,
                "message": f"Aspect '{self.aspect_name}' sent to ThePoint (verified safe)"
            }
