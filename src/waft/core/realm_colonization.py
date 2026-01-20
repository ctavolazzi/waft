"""
Realm Colonization System: Military Scouting and Exploration

This system implements the colonization dynamic for new Realms (external drives):
1. Detect new environment (external drive plugged in)
2. Set up PrimeBeing of that Realm (instance of TheOne)
3. Form Tether through observation ("Observation Creates the Bridge")
4. Explore the Realm and document findings in .md files
5. Report back to Mission Control
6. Adversarial inspection using Avatar system (military vs tribe, outsider vs insider)
7. Assimilate data back to TheOne/ThePoint

The system mimics military scouting missions with adversarial discovery of gaps/holes.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import os
import shutil

from ..being import Being, BeingSystem
from ..reality import RealitySystem, RealityType
from ..pantheon.external_drive_realm import ExternalDriveRealm
from ..pantheon.mission_control import MissionControl, MissionStatus
from ..utils import detect_external_drive, get_external_drive_base, _validate_project_name
from .the_one_core_being import TheOneCoreBeing


class RealmScout(Being):
    """
    RealmScout: A Being specialized for scouting new Realms.
    
    RealmScouts are spawned to explore newly discovered Realms (external drives).
    They document findings, identify gaps/holes, and report back to Mission Control.
    """
    
    def __init__(
        self,
        being_id: str,
        reality_id: str,
        realm_name: str,
        realm_path: Path,
        parent_being_id: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize a RealmScout.
        
        Args:
            being_id: Unique identifier
            reality_id: Reality ID
            realm_name: Name of the Realm being scouted
            realm_path: Path to the Realm
            parent_being_id: Parent Being (usually TheOne)
            **kwargs: Additional Being parameters
        """
        # Initialize as Being with scouting skills
        skills = kwargs.get("skills", {})
        skills.update({
            "exploration": 10.0,
            "observation": 10.0,
            "documentation": 10.0,
            "analysis": 10.0,
            "military_scouting": 8.0,
            "adversarial_inspection": 7.0
        })
        kwargs["skills"] = skills
        
        super().__init__(
            being_id=being_id,
            reality_id=reality_id,
            parent_being_id=parent_being_id,
            custom_name=f"RealmScout-{realm_name}",
            **kwargs
        )
        
        self.realm_name = realm_name
        realm_path_obj = Path(realm_path)
        
        # CRITICAL: Validate realm_path (validation will be done by RealmColonizationSystem)
        # Store as-is for now, validation happens in _launch_scouting_mission
        self.realm_path = realm_path_obj
        self.scout_data: Dict[str, Any] = {
            "findings": [],
            "gaps_discovered": [],
            "holes_identified": [],
            "exploration_log": []
        }
    
    def explore_realm(self) -> Dict[str, Any]:
        """
        Explore the Realm and document findings.
        
        Returns:
            Exploration data
        """
        findings = []
        exploration_log = []
        
        if not self.realm_path.exists():
            return {
                "error": f"Realm path does not exist: {self.realm_path}",
                "findings": [],
                "exploration_log": []
            }
        
        # Explore directory structure
        exploration_log.append(f"Exploring Realm: {self.realm_name}")
        exploration_log.append(f"Path: {self.realm_path}")
        
        # Document directory structure
        dir_structure = self._document_directory_structure(self.realm_path)
        findings.append({
            "type": "directory_structure",
            "data": dir_structure,
            "timestamp": datetime.now().isoformat()
        })
        
        # Identify file types
        file_analysis = self._analyze_files(self.realm_path)
        findings.append({
            "type": "file_analysis",
            "data": file_analysis,
            "timestamp": datetime.now().isoformat()
        })
        
        # Check for existing WAFT structure
        waft_structure = self._check_waft_structure(self.realm_path)
        findings.append({
            "type": "waft_structure",
            "data": waft_structure,
            "timestamp": datetime.now().isoformat()
        })
        
        self.scout_data["findings"] = findings
        self.scout_data["exploration_log"] = exploration_log
        
        return {
            "findings": findings,
            "exploration_log": exploration_log
        }
    
    def _document_directory_structure(self, path: Path, max_depth: int = 3) -> Dict[str, Any]:
        """Document directory structure."""
        structure = {
            "root": str(path),
            "directories": [],
            "files": [],
            "total_size": 0
        }
        
        try:
            for item in path.iterdir():
                # CRITICAL: Skip symlinks
                if item.is_symlink():
                    continue
                
                if item.is_dir() and max_depth > 0:
                    structure["directories"].append({
                        "name": item.name,
                        "path": str(item),
                        "substructure": self._document_directory_structure(item, max_depth - 1)
                    })
                elif item.is_file():
                    size = item.stat().st_size
                    structure["files"].append({
                        "name": item.name,
                        "path": str(item),
                        "size": size,
                        "extension": item.suffix
                    })
                    structure["total_size"] += size
        except (PermissionError, OSError) as e:
            structure["error"] = str(e)
        
        return structure
    
    def _analyze_files(self, path: Path) -> Dict[str, Any]:
        """Analyze file types and patterns."""
        analysis = {
            "file_types": {},
            "total_files": 0,
            "total_size": 0,
            "patterns": []
        }
        
        try:
            for item in path.rglob("*"):
                # CRITICAL: Skip symlinks
                if item.is_symlink():
                    continue
                
                if item.is_file():
                    analysis["total_files"] += 1
                    size = item.stat().st_size
                    analysis["total_size"] += size
                    
                    ext = item.suffix.lower()
                    if ext:
                        analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
        except (PermissionError, OSError):
            pass
        
        return analysis
    
    def _check_waft_structure(self, path: Path) -> Dict[str, Any]:
        """Check for existing WAFT structure."""
        waft_structure = {
            "has_waft": False,
            "has_pantheon": False,
            "has_pyrite": False,
            "has_work_efforts": False,
            "structure_paths": {}
        }
        
        waft_dirs = ["_pantheon", "_pyrite", "_work_efforts", "_hidden"]
        
        for dir_name in waft_dirs:
            dir_path = path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                waft_structure["has_waft"] = True
                waft_structure["structure_paths"][dir_name] = str(dir_path)
                
                if dir_name == "_pantheon":
                    waft_structure["has_pantheon"] = True
                elif dir_name == "_pyrite":
                    waft_structure["has_pyrite"] = True
                elif dir_name == "_work_efforts":
                    waft_structure["has_work_efforts"] = True
        
        return waft_structure
    
    def write_findings_md(self, output_path: Path) -> Path:
        """
        Write findings to a markdown file.
        
        Args:
            output_path: Path to write findings
            
        Returns:
            Path to written file
        """
        md_content = f"""# Realm Exploration Report: {self.realm_name}

**Scout ID**: {self.being_id}  
**Realm Name**: {self.realm_name}  
**Realm Path**: {self.realm_path}  
**Exploration Date**: {datetime.now().isoformat()}

## Findings

"""
        
        for finding in self.scout_data.get("findings", []):
            md_content += f"### {finding['type'].replace('_', ' ').title()}\n\n"
            md_content += f"```json\n{json.dumps(finding['data'], indent=2)}\n```\n\n"
        
        md_content += "## Exploration Log\n\n"
        for log_entry in self.scout_data.get("exploration_log", []):
            md_content += f"- {log_entry}\n"
        
        md_content += "\n## Gaps Discovered\n\n"
        for gap in self.scout_data.get("gaps_discovered", []):
            md_content += f"- {gap}\n"
        
        md_content += "\n## Holes Identified\n\n"
        for hole in self.scout_data.get("holes_identified", []):
            md_content += f"- {hole}\n"
        
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(md_content, encoding="utf-8")
        except (IOError, OSError, PermissionError) as e:
            raise OSError(f"Failed to write findings to {output_path}: {e}")
        
        return output_path
    
    def adversarial_inspection(
        self,
        perspective: str = "military"
    ) -> Dict[str, Any]:
        """
        Perform adversarial inspection from different perspectives.
        
        Perspectives:
        - "military": Outsider, invader perspective (find weaknesses)
        - "tribe": Insider, indigenous perspective (find strengths)
        
        Args:
            perspective: Inspection perspective
            
        Returns:
            Inspection results
        """
        inspection = {
            "perspective": perspective,
            "timestamp": datetime.now().isoformat(),
            "gaps_discovered": [],
            "holes_identified": [],
            "vulnerabilities": [],
            "strengths": []
        }
        
        if perspective == "military":
            # Military/outsider perspective: Find weaknesses, gaps, vulnerabilities
            inspection["gaps_discovered"].append("Unknown security measures")
            inspection["gaps_discovered"].append("Unclear data organization")
            inspection["holes_identified"].append("Missing documentation")
            inspection["vulnerabilities"].append("No access control visible")
        elif perspective == "tribe":
            # Tribe/insider perspective: Find strengths, understand structure
            inspection["strengths"].append("Existing directory structure")
            inspection["strengths"].append("File organization patterns")
        
        self.scout_data["gaps_discovered"].extend(inspection["gaps_discovered"])
        self.scout_data["holes_identified"].extend(inspection["holes_identified"])
        
        return inspection


class RealmColonizationSystem:
    """
    Realm Colonization System: Manages colonization of new Realms.
    
    Handles:
    - Drive detection
    - PrimeBeing creation for Realms
    - Tether formation
    - Scouting missions
    - Reporting to Mission Control
    - Data assimilation
    """
    
    def __init__(self, project_path: Optional[Path] = None):
        """
        Initialize Realm Colonization System.
        
        Args:
            project_path: Project root path
        """
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)
        
        self.project_path = project_path
        self.being_system = BeingSystem(project_path=project_path)
        self.reality_system = RealitySystem(project_path=project_path)
        self.external_drive_realm = ExternalDriveRealm(project_path=project_path)
        self.mission_control = MissionControl(project_path=project_path)
        self.the_one_core = TheOneCoreBeing(project_path=project_path)
        
        # Colonization state
        self.colonization_path = project_path / "_pantheon" / "realm_colonization"
        self.colonization_path.mkdir(parents=True, exist_ok=True)
        self.colonized_realms_file = self.colonization_path / "colonized_realms.json"
        self._ensure_colonization_state()
    
    def _validate_realm_path(self, realm_path: Path, expected_base: Path) -> bool:
        """
        Validate realm_path is safe and within expected base.
        
        CRITICAL: Security validation to prevent path traversal attacks.
        
        Args:
            realm_path: Path to validate
            expected_base: Expected base directory
            
        Returns:
            True if valid, False otherwise
        """
        try:
            resolved = realm_path.resolve()
            base_resolved = expected_base.resolve()
            
            # Must be within base
            if not str(resolved).startswith(str(base_resolved)):
                return False
            
            # Check for symlinks
            if resolved.is_symlink():
                return False
            
            # Check path components for traversal
            for part in realm_path.parts:
                if part == '..':
                    return False
            
            # Check for null bytes
            if '\x00' in str(realm_path):
                return False
            
            return True
        except (OSError, ValueError):
            return False
    
    def _ensure_colonization_state(self) -> None:
        """Ensure colonization state file exists."""
        if not self.colonized_realms_file.exists():
            state = {
                "colonized_realms": [],
                "scouting_missions": [],
                "created_at": datetime.now().isoformat(),
                "last_update": datetime.now().isoformat()
            }
            try:
                self.colonized_realms_file.write_text(
                    json.dumps(state, indent=2),
                    encoding="utf-8"
                )
            except (IOError, OSError, PermissionError) as e:
                # Log error but don't crash - state file will be created on first use
                pass
    
    def detect_and_colonize_realm(
        self,
        drive_name: str = "Easystore",
        realm_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Detect a new external drive and colonize it as a Realm.
        
        Steps:
        1. Detect external drive
        2. Create PrimeBeing for Realm (instance of TheOne)
        3. Form Tether through observation
        4. Launch scouting mission
        5. Report to Mission Control
        
        Args:
            drive_name: Name of external drive
            realm_name: Name for the Realm (auto-generated if None)
            
        Returns:
            Colonization result
        """
        # Track created resources for cleanup on failure
        created_resources = {
            "realm_name": None,
            "realm_storage_path": None,
            "prime_being_id": None,
            "tether_id": None,
            "mission_id": None,
            "scout_id": None,
            "realm_reality_id": None,
            "scout_reality_id": None
        }
        
        try:
            # Step 1: Detect external drive
            drive_path = detect_external_drive(drive_name)
            if not drive_path:
                return {
                    "success": False,
                    "error": f"External drive '{drive_name}' not detected"
                }
            
            # Step 2: Get base path
            base_path = get_external_drive_base()
            if not base_path:
                return {
                    "success": False,
                    "error": "Could not create external drive base path"
                }
            
            # Generate realm name if not provided
            if realm_name is None:
                realm_name = f"Realm_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # CRITICAL: Validate realm_name
            if not _validate_project_name(realm_name):
                return {
                    "success": False,
                    "error": f"Invalid realm_name: {realm_name} (contains unsafe characters)"
                }
            
            created_resources["realm_name"] = realm_name
            
            # Register realm
            realm_result = self.external_drive_realm.register_realm(realm_name)
            if not realm_result.get("success"):
                return realm_result
            
            realm_storage_path = Path(realm_result["realm"]["realm_storage_path"])
            created_resources["realm_storage_path"] = realm_storage_path
            
            # CRITICAL: Validate realm_storage_path
            if not self._validate_realm_path(realm_storage_path, base_path):
                return {
                    "success": False,
                    "error": f"Invalid realm_storage_path: {realm_storage_path} (path traversal or symlink detected)"
                }
            
            # Step 3: Create PrimeBeing for Realm (instance of TheOne)
            prime_being = self._create_realm_prime_being(realm_name, realm_storage_path)
            created_resources["prime_being_id"] = prime_being.being_id
            
            # Step 4: Form Tether through observation
            observation_data = {
                "realm_name": realm_name,
                "realm_path": str(realm_storage_path),
                "drive_name": drive_name,
                "drive_path": str(drive_path),
                "observed_at": datetime.now().isoformat()
            }
            
            tether = self.the_one_core.form_tether(
                realm_name=realm_name,
                realm_path=realm_storage_path,
                prime_being_id=prime_being.being_id,
                observation_data=observation_data
            )
            created_resources["tether_id"] = tether["tether_id"]
            
            # Step 5: Launch scouting mission
            scouting_result = self._launch_scouting_mission(
                realm_name=realm_name,
                realm_path=realm_storage_path,
                prime_being_id=prime_being.being_id
            )
            created_resources["scout_id"] = scouting_result.get("scout_id")
            
            # Step 6: Report to Mission Control
            mission_id = f"realm_scout_{realm_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            created_resources["mission_id"] = mission_id
            self.mission_control.register_mission(mission_id)
            self.mission_control.update_status(
                mission_id=mission_id,
                status="active",
                progress=0.5,
                telemetry={
                    "realm_name": realm_name,
                    "realm_path": str(realm_storage_path),
                    "tether_id": tether["tether_id"],
                    "scout_id": scouting_result.get("scout_id"),
                    "findings_count": len(scouting_result.get("findings", []))
                }
            )
            
            # Update colonization state
            try:
                state = json.loads(self.colonized_realms_file.read_text(encoding="utf-8"))
                state["colonized_realms"].append({
                    "realm_name": realm_name,
                    "realm_path": str(realm_storage_path),
                    "prime_being_id": prime_being.being_id,
                    "tether_id": tether["tether_id"],
                    "mission_id": mission_id,
                    "colonized_at": datetime.now().isoformat()
                })
                state["last_update"] = datetime.now().isoformat()
                self.colonized_realms_file.write_text(
                    json.dumps(state, indent=2),
                    encoding="utf-8"
                )
            except (IOError, OSError, PermissionError, json.JSONDecodeError) as e:
                # Cleanup on state update failure
                self._cleanup_partial_colonization(created_resources)
                return {
                    "success": False,
                    "error": f"Failed to update colonization state: {e}"
                }
            
            return {
                "success": True,
                "realm_name": realm_name,
                "realm_path": str(realm_storage_path),
                "prime_being_id": prime_being.being_id,
                "tether_id": tether["tether_id"],
                "mission_id": mission_id,
                "scouting_result": scouting_result
            }
        except Exception as e:
            # Cleanup on any failure
            self._cleanup_partial_colonization(created_resources)
            return {
                "success": False,
                "error": f"Colonization failed: {e}"
            }
    
    def _create_realm_prime_being(
        self,
        realm_name: str,
        realm_path: Path
    ) -> Being:
        """Create PrimeBeing for a Realm (instance of TheOne)."""
        # CRITICAL: Validate realm_name
        if not _validate_project_name(realm_name):
            raise ValueError(f"Invalid realm_name: {realm_name} (contains unsafe characters)")
        
        # Get TheOne as parent
        the_one = self.being_system.get_or_create_the_one()
        
        # Create Reality for this Realm
        try:
            realm_reality = self.reality_system.create_reality(
                reality_type=RealityType.LEARNING,
                configuration={
                    "realm_name": realm_name,
                    "realm_path": str(realm_path),
                    "special": True,
                    "purpose": "realm_colonization"
                }
            )
        except Exception as e:
            raise OSError(f"Failed to create realm reality: {e}")
        
        # Create PrimeBeing (instance of TheOne for this Realm)
        prime_being_id = f"prime_being_{realm_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            # Spawn being (spawn_being generates ID automatically, so we'll create directly)
            prime_being = Being(
                being_id=prime_being_id,
                reality_id=realm_reality.reality_id,
                parent_being_id=the_one.being_id,
                custom_name=f"PrimeBeing-{realm_name}",
                skills={
                    "realm_governance": 10.0,
                    "tether_management": 10.0,
                    "coordination": 10.0
                }
            )
            # Save the being
            self.being_system.save_being(prime_being)
        except Exception as e:
            raise OSError(f"Failed to create prime being: {e}")
        
        return prime_being
    
    def _launch_scouting_mission(
        self,
        realm_name: str,
        realm_path: Path,
        prime_being_id: str
    ) -> Dict[str, Any]:
        """Launch a scouting mission to explore the Realm."""
        # CRITICAL: Validate realm_name
        if not _validate_project_name(realm_name):
            raise ValueError(f"Invalid realm_name: {realm_name} (contains unsafe characters)")
        
        # CRITICAL: Validate realm_path
        base_path = get_external_drive_base()
        if base_path and not self._validate_realm_path(realm_path, base_path):
            raise ValueError(f"Invalid realm_path: {realm_path} (path traversal or symlink detected)")
        
        # Create Reality for scouting
        scout_reality = self.reality_system.create_reality(
            reality_type=RealityType.LEARNING,
            configuration={
                "realm_name": realm_name,
                "purpose": "realm_scouting",
                "mission_type": "exploration"
            }
        )
        
        # Create RealmScout
        scout_id = f"realm_scout_{realm_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        scout = RealmScout(
            being_id=scout_id,
            reality_id=scout_reality.reality_id,
            realm_name=realm_name,
            realm_path=realm_path,
            parent_being_id=prime_being_id
        )
        
        # Save scout
        self.being_system.save_being(scout)
        
        # Explore Realm
        exploration_result = scout.explore_realm()
        
        # Perform adversarial inspection (military perspective)
        military_inspection = scout.adversarial_inspection(perspective="military")
        
        # Perform adversarial inspection (tribe perspective)
        tribe_inspection = scout.adversarial_inspection(perspective="tribe")
        
        # Write findings to .md file
        findings_path = realm_path / "exploration" / f"scout_report_{scout_id}.md"
        scout.write_findings_md(findings_path)
        
        # Report back to Mission Control
        self._report_to_mission_control(
            realm_name=realm_name,
            scout=scout,
            exploration_result=exploration_result,
            military_inspection=military_inspection,
            tribe_inspection=tribe_inspection
        )
        
        # Assimilate data back to TheOneCoreBeing (with safety verification)
        # CRITICAL: Data is verified as SAFE before assimilation
        try:
            self.the_one_core.assimilate_data(
                realm_name=realm_name,
                scout_data={
                    "exploration_result": exploration_result,
                    "military_inspection": military_inspection,
                    "tribe_inspection": tribe_inspection,
                    "scout_id": scout_id
                },
                gaps_discovered=scout.scout_data.get("gaps_discovered", []),
                holes_identified=scout.scout_data.get("holes_identified", []),
                source_being_id=scout_id
            )
        except ValueError as e:
            # Safety verification failed - log but don't crash
            # The scouting mission still succeeded, but data wasn't assimilated
            return {
                "scout_id": scout_id,
                "findings": exploration_result.get("findings", []),
                "gaps_discovered": scout.scout_data.get("gaps_discovered", []),
                "holes_identified": scout.scout_data.get("holes_identified", []),
                "findings_path": str(findings_path) if findings_path else None,
                "assimilation_failed": True,
                "assimilation_error": str(e),
                "message": "Scouting completed, but data failed safety verification - NOT assimilated to protect all Beings"
            }
        
        return {
            "scout_id": scout_id,
            "findings": exploration_result.get("findings", []),
            "gaps_discovered": scout.scout_data.get("gaps_discovered", []),
            "holes_identified": scout.scout_data.get("holes_identified", []),
            "findings_path": str(findings_path) if findings_path else None,
            "assimilated": True
        }
    
    def _cleanup_partial_colonization(self, created_resources: Dict[str, Any]) -> None:
        """
        Clean up resources created during partial colonization failure.
        
        Args:
            created_resources: Dictionary tracking created resources
        """
        try:
            # Remove from colonization state if added
            if created_resources.get("realm_name"):
                try:
                    state = json.loads(self.colonized_realms_file.read_text(encoding="utf-8"))
                    state["colonized_realms"] = [
                        r for r in state["colonized_realms"]
                        if r.get("realm_name") != created_resources["realm_name"]
                    ]
                    state["last_update"] = datetime.now().isoformat()
                    self.colonized_realms_file.write_text(
                        json.dumps(state, indent=2),
                        encoding="utf-8"
                    )
                except Exception:
                    pass  # Ignore cleanup errors
            
            # Note: We don't delete beings, realities, or tethers as they may be referenced elsewhere
            # The system is designed to be resilient to partial failures
        except Exception:
            # Ignore cleanup errors - better to leave orphaned resources than crash
            pass
    
    def _report_to_mission_control(
        self,
        realm_name: str,
        scout: RealmScout,
        exploration_result: Dict[str, Any],
        military_inspection: Dict[str, Any],
        tribe_inspection: Dict[str, Any]
    ) -> None:
        """Report scouting results to Mission Control."""
        # Find mission for this realm
        try:
            state = json.loads(self.colonized_realms_file.read_text(encoding="utf-8"))
            realm_info = next(
                (r for r in state["colonized_realms"] if r["realm_name"] == realm_name),
                None
            )
            
            if realm_info:
                mission_id = realm_info.get("mission_id")
                if mission_id:
                    self.mission_control.update_status(
                        mission_id=mission_id,
                        status="active",
                        progress=1.0,
                        telemetry={
                            "realm_name": realm_name,
                            "scout_id": scout.being_id,
                            "findings_count": len(exploration_result.get("findings", [])),
                            "gaps_discovered": len(scout.scout_data.get("gaps_discovered", [])),
                            "holes_identified": len(scout.scout_data.get("holes_identified", [])),
                            "military_inspection": military_inspection,
                            "tribe_inspection": tribe_inspection
                        }
                    )
        except (IOError, OSError, json.JSONDecodeError):
            # Ignore errors in reporting - not critical
            pass
