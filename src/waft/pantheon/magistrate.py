"""
Magistrate: God of Precedent and Body of Proof

The Magistrate organizes case files into Precedent categories,
building a Body of Proof over time that can be referenced repeatedly.

Following "as above, so below" principles:
- As above: Pantheon god organizing celestial law
- So below: File-based system organizing proof cases
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import re


class Precedent:
    """A precedent - a categorized case file that establishes proof."""
    
    def __init__(
        self,
        case_id: str,
        case_path: Path,
        category: str,
        subcategory: Optional[str] = None,
        claim: Optional[str] = None,
        verdict: Optional[str] = None,
        confidence: Optional[float] = None,
        tags: Optional[List[str]] = None,
        created_at: Optional[str] = None
    ):
        """
        Initialize a precedent.
        
        Args:
            case_id: Unique identifier for the case
            case_path: Path to the case file
            category: Main category (e.g., "verification", "architecture", "security")
            subcategory: Optional subcategory for finer organization
            claim: The claim that was proven/disproven
            verdict: PROVEN/DISPROVEN/INCONCLUSIVE
            confidence: Confidence level (0.0-1.0)
            tags: List of tags for searching
            created_at: ISO timestamp when case was created
        """
        self.case_id = case_id
        self.case_path = case_path
        self.category = category
        self.subcategory = subcategory
        self.claim = claim
        self.verdict = verdict
        self.confidence = confidence
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert precedent to dictionary."""
        return {
            "case_id": self.case_id,
            "case_path": str(self.case_path),
            "category": self.category,
            "subcategory": self.subcategory,
            "claim": self.claim,
            "verdict": self.verdict,
            "confidence": self.confidence,
            "tags": self.tags,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Precedent":
        """Create precedent from dictionary."""
        return cls(
            case_id=data["case_id"],
            case_path=Path(data["case_path"]),
            category=data["category"],
            subcategory=data.get("subcategory"),
            claim=data.get("claim"),
            verdict=data.get("verdict"),
            confidence=data.get("confidence"),
            tags=data.get("tags", []),
            created_at=data.get("created_at")
        )


class BodyOfProof:
    """The Body of Proof - organized collection of precedents."""
    
    def __init__(self, precedents: Optional[List[Precedent]] = None):
        """
        Initialize Body of Proof.
        
        Args:
            precedents: List of precedents (default: empty)
        """
        self.precedents = precedents or []
        self._index_by_category: Dict[str, List[Precedent]] = {}
        self._index_by_tag: Dict[str, List[Precedent]] = {}
        self._rebuild_indexes()
    
    def add_precedent(self, precedent: Precedent):
        """Add a precedent to the Body of Proof."""
        self.precedents.append(precedent)
        self._rebuild_indexes()
    
    def _rebuild_indexes(self):
        """Rebuild category and tag indexes."""
        self._index_by_category = {}
        self._index_by_tag = {}
        
        for precedent in self.precedents:
            # Index by category
            category_key = precedent.category
            if precedent.subcategory:
                category_key = f"{precedent.category}/{precedent.subcategory}"
            
            if category_key not in self._index_by_category:
                self._index_by_category[category_key] = []
            self._index_by_category[category_key].append(precedent)
            
            # Index by tag
            for tag in precedent.tags:
                if tag not in self._index_by_tag:
                    self._index_by_tag[tag] = []
                self._index_by_tag[tag].append(precedent)
    
    def get_by_category(self, category: str, subcategory: Optional[str] = None) -> List[Precedent]:
        """Get precedents by category."""
        key = category
        if subcategory:
            key = f"{category}/{subcategory}"
        return self._index_by_category.get(key, [])
    
    def get_by_tag(self, tag: str) -> List[Precedent]:
        """Get precedents by tag."""
        return self._index_by_tag.get(tag, [])
    
    def search(self, query: str) -> List[Precedent]:
        """Search precedents by claim, tags, or case_id."""
        query_lower = query.lower()
        results = []
        
        for precedent in self.precedents:
            # Search in claim
            if precedent.claim and query_lower in precedent.claim.lower():
                results.append(precedent)
                continue
            
            # Search in tags
            if any(query_lower in tag.lower() for tag in precedent.tags):
                results.append(precedent)
                continue
            
            # Search in case_id
            if query_lower in precedent.case_id.lower():
                results.append(precedent)
                continue
        
        return results
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Body of Proof to dictionary."""
        return {
            "precedents": [p.to_dict() for p in self.precedents],
            "total_count": len(self.precedents),
            "categories": list(self._index_by_category.keys()),
            "tags": list(self._index_by_tag.keys())
        }


class Magistrate:
    """
    Magistrate: God of Precedent and Body of Proof
    
    Organizes case files from _work_efforts/proof_cases/ into Precedent categories,
    building a Body of Proof that can be referenced repeatedly.
    
    Storage:
    - Precedents: _pantheon/magistrate/precedents/ (JSON files)
    - Body of Proof: _pantheon/magistrate/body_of_proof.json
    - Index: _pantheon/magistrate/index.json
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize the Magistrate.
        
        Args:
            project_path: Path to project root (default: current directory)
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.magistrate_path = self.pantheon_path / "magistrate"
        self.precedents_path = self.magistrate_path / "precedents"
        self.proof_cases_path = project_path / "_work_efforts" / "proof_cases"
        
        # Create directory structure
        self.magistrate_path.mkdir(parents=True, exist_ok=True)
        self.precedents_path.mkdir(parents=True, exist_ok=True)
        
        # Body of Proof
        self.body_of_proof = BodyOfProof()
        
        # Load existing precedents
        self._load_precedents()
    
    def _load_precedents(self):
        """Load existing precedents from disk."""
        body_of_proof_file = self.magistrate_path / "body_of_proof.json"
        
        if body_of_proof_file.exists():
            try:
                with open(body_of_proof_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.body_of_proof = BodyOfProof([
                        Precedent.from_dict(p) for p in data.get("precedents", [])
                    ])
            except (json.JSONDecodeError, KeyError) as e:
                # If corrupted, start fresh
                self.body_of_proof = BodyOfProof()
    
    def _save_body_of_proof(self):
        """Save Body of Proof to disk."""
        body_of_proof_file = self.magistrate_path / "body_of_proof.json"
        
        with open(body_of_proof_file, "w", encoding="utf-8") as f:
            json.dump(self.body_of_proof.to_dict(), f, indent=2)
    
    def _parse_case_file(self, case_path: Path) -> Dict[str, Any]:
        """
        Parse a case file to extract metadata.
        
        Args:
            case_path: Path to case file
            
        Returns:
            Dictionary with extracted metadata
        """
        metadata = {
            "case_id": None,
            "claim": None,
            "verdict": None,
            "confidence": None,
            "date": None
        }
        
        try:
            with open(case_path, "r", encoding="utf-8") as f:
                content = f.read()
                
                # Extract case ID
                case_id_match = re.search(r'\*\*Case ID\*\*:\s*([^\n]+)', content)
                if case_id_match:
                    metadata["case_id"] = case_id_match.group(1).strip()
                
                # Extract claim
                claim_match = re.search(r'\*\*Claim\*\*:\s*([^\n]+)', content)
                if claim_match:
                    metadata["claim"] = claim_match.group(1).strip()
                
                # Extract verdict
                verdict_match = re.search(r'\*\*Verdict\*\*:\s*([^\n]+)', content)
                if verdict_match:
                    metadata["verdict"] = verdict_match.group(1).strip()
                
                # Extract confidence
                confidence_match = re.search(r'\*\*Confidence\*\*:\s*([0-9.]+)%', content)
                if confidence_match:
                    metadata["confidence"] = float(confidence_match.group(1)) / 100.0
                
                # Extract date
                date_match = re.search(r'\*\*Date\*\*:\s*([^\n]+)', content)
                if date_match:
                    metadata["date"] = date_match.group(1).strip()
        
        except (IOError, OSError, UnicodeDecodeError):
            # If file can't be read, return minimal metadata
            pass
        
        return metadata
    
    def _infer_category(self, case_path: Path, claim: Optional[str] = None) -> tuple[str, Optional[str]]:
        """
        Infer category and subcategory from case file.
        
        Args:
            case_path: Path to case file
            claim: Optional claim text for better inference
            
        Returns:
            Tuple of (category, subcategory)
        """
        # Default category
        category = "general"
        subcategory = None
        
        # Infer from filename
        filename_lower = case_path.stem.lower()
        
        # Common patterns
        if "security" in filename_lower or "vulnerability" in filename_lower:
            category = "security"
        elif "architecture" in filename_lower or "structure" in filename_lower:
            category = "architecture"
        elif "verification" in filename_lower or "proof" in filename_lower:
            category = "verification"
        elif "template" in filename_lower or "pdf" in filename_lower:
            category = "templates"
        elif "integration" in filename_lower:
            category = "integration"
        elif "performance" in filename_lower:
            category = "performance"
        elif "bug" in filename_lower or "error" in filename_lower:
            category = "bugs"
        
        # Infer from claim if available
        if claim:
            claim_lower = claim.lower()
            if "security" in claim_lower or "vulnerability" in claim_lower:
                category = "security"
            elif "architecture" in claim_lower:
                category = "architecture"
            elif "template" in claim_lower or "pdf" in claim_lower:
                category = "templates"
            elif "integration" in claim_lower:
                category = "integration"
        
        return category, subcategory
    
    def organize_case_file(
        self,
        case_path: Path,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Precedent:
        """
        Organize a case file into a Precedent.
        
        Args:
            case_path: Path to case file (relative to proof_cases or absolute)
            category: Optional category (will be inferred if not provided)
            subcategory: Optional subcategory
            tags: Optional list of tags
            
        Returns:
            Created Precedent
        """
        # Resolve case path
        if not case_path.is_absolute():
            case_path = self.proof_cases_path / case_path
        else:
            # Ensure it's within proof_cases
            if not str(case_path).startswith(str(self.proof_cases_path)):
                raise ValueError(f"Case file must be in {self.proof_cases_path}")
        
        if not case_path.exists():
            raise FileNotFoundError(f"Case file not found: {case_path}")
        
        # Parse case file
        metadata = self._parse_case_file(case_path)
        
        # Infer category if not provided
        if not category:
            category, subcategory = self._infer_category(
                case_path,
                metadata.get("claim")
            )
        
        # Create precedent
        case_id = metadata.get("case_id") or case_path.stem
        precedent = Precedent(
            case_id=case_id,
            case_path=case_path.relative_to(self.project_path),
            category=category,
            subcategory=subcategory,
            claim=metadata.get("claim"),
            verdict=metadata.get("verdict"),
            confidence=metadata.get("confidence"),
            tags=tags or [],
            created_at=metadata.get("date")
        )
        
        # Add to Body of Proof
        self.body_of_proof.add_precedent(precedent)
        
        # Save precedent file
        precedent_file = self.precedents_path / f"{case_id}.json"
        with open(precedent_file, "w", encoding="utf-8") as f:
            json.dump(precedent.to_dict(), f, indent=2)
        
        # Save Body of Proof
        self._save_body_of_proof()
        
        return precedent
    
    def organize_all_cases(
        self,
        auto_categorize: bool = True,
        default_tags: Optional[List[str]] = None
    ) -> List[Precedent]:
        """
        Organize all case files in proof_cases directory.
        
        Args:
            auto_categorize: Automatically infer categories (default: True)
            default_tags: Default tags to apply to all cases
            
        Returns:
            List of created Precedents
        """
        if not self.proof_cases_path.exists():
            return []
        
        precedents = []
        case_files = list(self.proof_cases_path.glob("case_*.md"))
        
        for case_file in case_files:
            # Skip if already organized
            case_id = case_file.stem
            precedent_file = self.precedents_path / f"{case_id}.json"
            if precedent_file.exists():
                continue
            
            try:
                precedent = self.organize_case_file(
                    case_file,
                    tags=default_tags
                )
                precedents.append(precedent)
            except Exception as e:
                # Log error but continue
                print(f"Error organizing {case_file}: {e}")
        
        return precedents
    
    def get_precedent(self, case_id: str) -> Optional[Precedent]:
        """Get a precedent by case ID."""
        for precedent in self.body_of_proof.precedents:
            if precedent.case_id == case_id:
                return precedent
        return None
    
    def get_precedents_by_category(
        self,
        category: str,
        subcategory: Optional[str] = None
    ) -> List[Precedent]:
        """Get precedents by category."""
        return self.body_of_proof.get_by_category(category, subcategory)
    
    def get_precedents_by_tag(self, tag: str) -> List[Precedent]:
        """Get precedents by tag."""
        return self.body_of_proof.get_by_tag(tag)
    
    def search_precedents(self, query: str) -> List[Precedent]:
        """Search precedents by query."""
        return self.body_of_proof.search(query)
    
    def get_body_of_proof_summary(self) -> Dict[str, Any]:
        """Get summary of Body of Proof."""
        return {
            "total_precedents": len(self.body_of_proof.precedents),
            "categories": {
                cat: len(precedents)
                for cat, precedents in self.body_of_proof._index_by_category.items()
            },
            "tags": {
                tag: len(precedents)
                for tag, precedents in self.body_of_proof._index_by_tag.items()
            },
            "verdicts": self._count_verdicts()
        }
    
    def _count_verdicts(self) -> Dict[str, int]:
        """Count precedents by verdict."""
        counts = {"PROVEN": 0, "DISPROVEN": 0, "INCONCLUSIVE": 0, "UNKNOWN": 0}
        
        for precedent in self.body_of_proof.precedents:
            verdict = precedent.verdict or "UNKNOWN"
            if verdict.upper() in counts:
                counts[verdict.upper()] += 1
            else:
                counts["UNKNOWN"] += 1
        
        return counts
    
    def update_precedent(
        self,
        case_id: str,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Precedent]:
        """
        Update a precedent's metadata.
        
        Args:
            case_id: Case ID to update
            category: New category (optional)
            subcategory: New subcategory (optional)
            tags: New tags (optional, replaces existing)
            
        Returns:
            Updated Precedent or None if not found
        """
        precedent = self.get_precedent(case_id)
        if not precedent:
            return None
        
        # Update fields
        if category is not None:
            precedent.category = category
        if subcategory is not None:
            precedent.subcategory = subcategory
        if tags is not None:
            precedent.tags = tags
        
        # Rebuild indexes
        self.body_of_proof._rebuild_indexes()
        
        # Save
        precedent_file = self.precedents_path / f"{case_id}.json"
        with open(precedent_file, "w", encoding="utf-8") as f:
            json.dump(precedent.to_dict(), f, indent=2)
        
        self._save_body_of_proof()
        
        return precedent
