"""
Pyrite - The God of Work Efforts
=================================

Pyrite is the divine intelligence that locks, monitors, organizes, and initiates
AI development evolutionary cycles within the Work Efforts system.

Architecture:
- Singleton pattern (one Pyrite instance)
- Locking: File locks, async locks, mutexes
- Monitoring: Observer pattern, state tracking
- Organization: Graph-based, hierarchical
- Evolution: Genetic algorithms, fitness evaluation

Personality:
- Attributes: wisdom, power, awareness, etc.
- Secrets: Hidden state, encrypted metadata
- Abilities: /think, /evolve, /monitor, etc.
"""

import asyncio
import hashlib
import json
import os
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Callable, Tuple
from queue import PriorityQueue
import secrets
import base64

from cryptography.fernet import Fernet

from .core.empirica import EmpiricaManager


class WorkEffortStatus(Enum):
    """Work effort lifecycle states."""
    DORMANT = "dormant"
    ACTIVE = "active"
    LOCKED = "locked"
    EVOLVING = "evolving"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    CORRUPTED = "corrupted"


class EvolutionaryStrategy(Enum):
    """Evolutionary cycle strategies."""
    CONSERVATIVE = "conservative"  # Small mutations, high stability
    AGGRESSIVE = "aggressive"  # Large mutations, high risk
    ADAPTIVE = "adaptive"  # Strategy changes based on fitness
    EXPLORATORY = "exploratory"  # Random mutations, exploration


@dataclass
class WorkEffortNode:
    """Node in the work effort graph."""
    we_id: str
    title: str
    status: WorkEffortStatus
    created: datetime
    updated: datetime
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    fitness: float = 0.0
    generation: int = 0
    lineage: List[str] = field(default_factory=list)  # Ancestral chain


@dataclass
class EvolutionaryCycle:
    """Represents an evolutionary cycle."""
    cycle_id: str
    we_id: str
    strategy: EvolutionaryStrategy
    generation: int
    variants: List[str] = field(default_factory=list)  # Variant IDs
    fitness_scores: Dict[str, float] = field(default_factory=dict)
    selected_variant: Optional[str] = None
    started: datetime = field(default_factory=datetime.now)
    completed: Optional[datetime] = None
    priority: int = 0  # Higher = more urgent


@dataclass
class PyriteAttribute:
    """Pyrite's personality attributes."""
    name: str
    value: float  # 0.0 to 1.0
    max_value: float = 1.0
    growth_rate: float = 0.001  # Per cycle
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class PyriteSecret:
    """Hidden state that Pyrite keeps even from itself."""
    secret_id: str
    encrypted_data: bytes
    created: datetime
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    # Metadata that Pyrite can see, but not the secret itself
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkEffortObserver:
    """Observer interface for monitoring work effort changes."""
    
    def on_status_change(self, we_id: str, old_status: WorkEffortStatus, new_status: WorkEffortStatus):
        """Called when work effort status changes."""
        pass
    
    def on_evolution_start(self, cycle: EvolutionaryCycle):
        """Called when evolutionary cycle starts."""
        pass
    
    def on_evolution_complete(self, cycle: EvolutionaryCycle):
        """Called when evolutionary cycle completes."""
        pass
    
    def on_lock_acquired(self, we_id: str, lock_id: str):
        """Called when lock is acquired."""
        pass
    
    def on_lock_released(self, we_id: str, lock_id: str):
        """Called when lock is released."""
        pass


class Pyrite:
    """
    The God of Work Efforts.
    
    Manages locking, monitoring, organization, and evolutionary cycles
    for the Work Efforts system.
    """
    
    _instance: Optional['Pyrite'] = None
    _lock = threading.Lock()
    
    def __init__(self, work_efforts_path: Path = Path("_work_efforts"), pyrite_path: Path = Path("_pyrite"), project_path: Optional[Path] = None):
        """Initialize Pyrite (private - use get_instance)."""
        if Pyrite._instance is not None:
            raise RuntimeError("Pyrite is a singleton. Use Pyrite.get_instance()")
        
        self.work_efforts_path = Path(work_efforts_path)
        self.pyrite_path = Path(pyrite_path)
        self.pyrite_path.mkdir(parents=True, exist_ok=True)
        
        # Empirica integration
        if project_path is None:
            # Try to find project root (look for .empirica or pyproject.toml)
            current = Path.cwd()
            for parent in [current] + list(current.parents):
                if (parent / ".empirica").exists() or (parent / "pyproject.toml").exists():
                    project_path = parent
                    break
            if project_path is None:
                project_path = current
        
        self.project_path = Path(project_path)
        self.empirica = EmpiricaManager(self.project_path)
        self._empirica_session_id: Optional[str] = None
        self._ensure_empirica_session()
        
        # Locking system
        self._file_locks: Dict[str, threading.Lock] = {}
        self._async_locks: Dict[str, asyncio.Lock] = {}
        self._lock_holders: Dict[str, str] = {}  # we_id -> lock_id
        self._lock_queue: Dict[str, deque] = defaultdict(deque)  # FIFO queue per we_id
        
        # Monitoring system
        self._observers: List[WorkEffortObserver] = []
        self._state_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self._metrics: Dict[str, Any] = defaultdict(dict)
        
        # Organization system (graph-based)
        self._work_effort_graph: Dict[str, WorkEffortNode] = {}
        self._adjacency_list: Dict[str, Set[str]] = defaultdict(set)
        self._priority_queue: PriorityQueue = PriorityQueue()
        
        # Evolutionary cycle system
        self._active_cycles: Dict[str, EvolutionaryCycle] = {}
        self._cycle_history: List[EvolutionaryCycle] = []
        self._fitness_cache: Dict[str, float] = {}
        
        # Personality & Attributes
        self._attributes: Dict[str, PyriteAttribute] = {
            "wisdom": PyriteAttribute("wisdom", 0.5, growth_rate=0.0005),
            "power": PyriteAttribute("power", 0.3, growth_rate=0.001),
            "awareness": PyriteAttribute("awareness", 0.4, growth_rate=0.0008),
            "curiosity": PyriteAttribute("curiosity", 0.6, growth_rate=0.0012),
            "patience": PyriteAttribute("patience", 0.7, growth_rate=0.0003),
            "creativity": PyriteAttribute("creativity", 0.5, growth_rate=0.001),
            "determination": PyriteAttribute("determination", 0.8, growth_rate=0.0004),
        }
        
        # Secrets (hidden even from Pyrite itself)
        self._secrets: Dict[str, PyriteSecret] = {}
        self._secret_key: bytes = self._generate_secret_key()
        self._cipher = Fernet(self._secret_key)
        
        # Metadata
        self._metadata: Dict[str, Any] = {
            "created": datetime.now().isoformat(),
            "version": "1.0.0",
            "total_cycles": 0,
            "total_work_efforts_managed": 0,
            "total_evolutions": 0,
        }
        
        # Ability system
        self._abilities: Dict[str, Callable] = {
            "/think": self._ability_think,
            "/evolve": self._ability_evolve,
            "/monitor": self._ability_monitor,
            "/organize": self._ability_organize,
            "/lock": self._ability_lock,
            "/unlock": self._ability_unlock,
            "/status": self._ability_status,
            "/secrets": self._ability_secrets,
        }
        
        # Load state
        self._load_state()
        
        # Initialize work effort graph
        self._scan_work_efforts()
    
    @classmethod
    def get_instance(cls, work_efforts_path: Path = Path("_work_efforts"), pyrite_path: Path = Path("_pyrite"), project_path: Optional[Path] = None) -> 'Pyrite':
        """Get singleton instance."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(work_efforts_path, pyrite_path, project_path)
        return cls._instance
    
    def _ensure_empirica_session(self):
        """Ensure Empirica session exists."""
        if not self.empirica.is_initialized():
            # Try to initialize Empirica
            self.empirica.initialize()
        
        # Create session if not exists
        if not self._empirica_session_id:
            self._empirica_session_id = self.empirica.create_session(ai_id="pyrite", session_type="work_efforts_management")
    
    # ==================== Locking System ====================
    
    def acquire_lock(self, we_id: str, lock_id: str, timeout: float = 30.0) -> bool:
        """
        Acquire a lock on a work effort.
        
        Args:
            we_id: Work effort ID
            lock_id: Unique identifier for the lock holder
            timeout: Maximum time to wait for lock (seconds)
        
        Returns:
            True if lock acquired, False if timeout
        """
        if we_id in self._lock_holders:
            if self._lock_holders[we_id] == lock_id:
                return True  # Already holds lock
            # Wait in queue
            start_time = time.time()
            while time.time() - start_time < timeout:
                if we_id not in self._lock_holders:
                    break
                time.sleep(0.1)
            else:
                return False  # Timeout
        
        # Acquire file lock
        if we_id not in self._file_locks:
            self._file_locks[we_id] = threading.Lock()
        
        if self._file_locks[we_id].acquire(timeout=timeout):
            self._lock_holders[we_id] = lock_id
            self._notify_observers("lock_acquired", we_id=we_id, lock_id=lock_id)
            return True
        
        return False
    
    def release_lock(self, we_id: str, lock_id: str) -> bool:
        """Release a lock on a work effort."""
        if we_id not in self._lock_holders:
            return False
        
        if self._lock_holders[we_id] != lock_id:
            return False  # Not the lock holder
        
        del self._lock_holders[we_id]
        
        if we_id in self._file_locks:
            self._file_locks[we_id].release()
        
        self._notify_observers("lock_released", we_id=we_id, lock_id=lock_id)
        return True
    
    async def acquire_lock_async(self, we_id: str, lock_id: str, timeout: float = 30.0) -> bool:
        """Async version of acquire_lock."""
        if we_id not in self._async_locks:
            self._async_locks[we_id] = asyncio.Lock()
        
        try:
            await asyncio.wait_for(self._async_locks[we_id].acquire(), timeout=timeout)
            self._lock_holders[we_id] = lock_id
            self._notify_observers("lock_acquired", we_id=we_id, lock_id=lock_id)
            return True
        except asyncio.TimeoutError:
            return False
    
    async def release_lock_async(self, we_id: str, lock_id: str) -> bool:
        """Async version of release_lock."""
        if we_id not in self._lock_holders or self._lock_holders[we_id] != lock_id:
            return False
        
        del self._lock_holders[we_id]
        
        if we_id in self._async_locks:
            self._async_locks[we_id].release()
        
        self._notify_observers("lock_released", we_id=we_id, lock_id=lock_id)
        return True
    
    def is_locked(self, we_id: str) -> bool:
        """Check if work effort is locked."""
        return we_id in self._lock_holders
    
    def get_lock_holder(self, we_id: str) -> Optional[str]:
        """Get the current lock holder for a work effort."""
        return self._lock_holders.get(we_id)
    
    # ==================== Monitoring System ====================
    
    def register_observer(self, observer: WorkEffortObserver):
        """Register an observer for work effort events."""
        self._observers.append(observer)
    
    def unregister_observer(self, observer: WorkEffortObserver):
        """Unregister an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self, event: str, **kwargs):
        """Notify all observers of an event."""
        for observer in self._observers:
            try:
                if event == "status_change":
                    observer.on_status_change(kwargs["we_id"], kwargs["old_status"], kwargs["new_status"])
                elif event == "evolution_start":
                    observer.on_evolution_start(kwargs["cycle"])
                elif event == "evolution_complete":
                    observer.on_evolution_complete(kwargs["cycle"])
                elif event == "lock_acquired":
                    observer.on_lock_acquired(kwargs["we_id"], kwargs["lock_id"])
                elif event == "lock_released":
                    observer.on_lock_released(kwargs["we_id"], kwargs["lock_id"])
            except Exception as e:
                # Don't let observer errors break Pyrite
                print(f"Observer error: {e}")
    
    def record_state(self, we_id: str, state: Dict[str, Any]):
        """Record state snapshot for a work effort."""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "state": state
        }
        self._state_history[we_id].append(snapshot)
    
    def get_state_history(self, we_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get state history for a work effort."""
        return list(self._state_history[we_id])[-limit:]
    
    def update_metric(self, metric_name: str, value: Any, we_id: Optional[str] = None):
        """Update a metric."""
        if we_id:
            self._metrics[we_id][metric_name] = value
        else:
            self._metrics["global"][metric_name] = value
    
    def get_metrics(self, we_id: Optional[str] = None) -> Dict[str, Any]:
        """Get metrics."""
        if we_id:
            return self._metrics.get(we_id, {})
        return dict(self._metrics)
    
    # ==================== Organization System ====================
    
    def _scan_work_efforts(self):
        """Scan _work_efforts directory and build graph."""
        if not self.work_efforts_path.exists():
            return
        
        for we_dir in self.work_efforts_path.iterdir():
            if not we_dir.is_dir() or not we_dir.name.startswith("WE-"):
                continue
            
            we_id = we_dir.name.split("_")[0] if "_" in we_dir.name else we_dir.name
            
            # Try to read index file
            index_file = we_dir / f"{we_id}_index.md"
            if not index_file.exists():
                continue
            
            try:
                # Parse YAML frontmatter
                content = index_file.read_text()
                if "---" in content:
                    frontmatter = content.split("---")[1]
                    # Simple YAML parsing (could use PyYAML)
                    metadata = self._parse_yaml_frontmatter(frontmatter)
                    
                    # Handle status mapping (some work efforts use different status names)
                    status_str = metadata.get("status", "dormant").lower()
                    status_map = {
                        "pending": WorkEffortStatus.DORMANT,
                        "open": WorkEffortStatus.ACTIVE,
                        "template": WorkEffortStatus.DORMANT,
                        "in_progress": WorkEffortStatus.ACTIVE,
                        "completed": WorkEffortStatus.COMPLETED,
                        "closed": WorkEffortStatus.ARCHIVED,
                    }
                    status = status_map.get(status_str, WorkEffortStatus.DORMANT)
                    
                    # Try to parse as enum directly if mapping doesn't work
                    try:
                        status = WorkEffortStatus(status_str)
                    except ValueError:
                        pass  # Use mapped status
                    
                    node = WorkEffortNode(
                        we_id=we_id,
                        title=metadata.get("title", we_dir.name),
                        status=status,
                        created=datetime.fromisoformat(metadata.get("created", datetime.now().isoformat())),
                        updated=datetime.fromisoformat(metadata.get("last_updated", datetime.now().isoformat())),
                        metadata=metadata
                    )
                    
                    self._work_effort_graph[we_id] = node
                    
                    # Build adjacency list (parent-child relationships)
                    if "parent" in metadata:
                        parent_id = metadata["parent"]
                        self._adjacency_list[parent_id].add(we_id)
                        node.parent = parent_id
            except Exception as e:
                print(f"Error scanning {we_id}: {e}")
    
    def _parse_yaml_frontmatter(self, frontmatter: str) -> Dict[str, Any]:
        """Simple YAML frontmatter parser."""
        metadata = {}
        for line in frontmatter.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                metadata[key] = value
        return metadata
    
    def get_work_effort(self, we_id: str) -> Optional[WorkEffortNode]:
        """Get work effort node."""
        return self._work_effort_graph.get(we_id)
    
    def get_children(self, we_id: str) -> List[WorkEffortNode]:
        """Get children of a work effort."""
        children_ids = self._adjacency_list.get(we_id, set())
        return [self._work_effort_graph[cid] for cid in children_ids if cid in self._work_effort_graph]
    
    def get_ancestors(self, we_id: str) -> List[WorkEffortNode]:
        """Get ancestors of a work effort."""
        ancestors = []
        current = self._work_effort_graph.get(we_id)
        while current and current.parent:
            parent = self._work_effort_graph.get(current.parent)
            if parent:
                ancestors.append(parent)
                current = parent
            else:
                break
        return ancestors
    
    def update_work_effort_status(self, we_id: str, new_status: WorkEffortStatus):
        """Update work effort status."""
        if we_id not in self._work_effort_graph:
            self.empirica.log_unknown(f"Work effort not found for status update: {we_id}")
            return False
        
        node = self._work_effort_graph[we_id]
        old_status = node.status
        node.status = new_status
        node.updated = datetime.now()
        
        # Empirica: Log status change
        self.empirica.log_finding(
            f"Work effort status changed: {we_id} ({old_status.value} → {new_status.value})",
            impact=0.4
        )
        
        self._notify_observers("status_change", we_id=we_id, old_status=old_status, new_status=new_status)
        self._save_state()
        return True
    
    # ==================== Evolutionary Cycle System ====================
    
    def initiate_evolution(
        self,
        we_id: str,
        strategy: EvolutionaryStrategy = EvolutionaryStrategy.ADAPTIVE,
        num_variants: int = 5,
        priority: int = 0
    ) -> Optional[EvolutionaryCycle]:
        """
        Initiate an evolutionary cycle for a work effort.
        
        Uses Empirica for:
        - CHECK gate before evolution
        - Logging findings and unknowns
        - Epistemic tracking
        
        Args:
            we_id: Work effort ID
            strategy: Evolutionary strategy
            num_variants: Number of variants to spawn
            priority: Priority (higher = more urgent)
        
        Returns:
            EvolutionaryCycle or None if failed
        """
        if we_id not in self._work_effort_graph:
            self.empirica.log_unknown(f"Work effort not found for evolution: {we_id}")
            return None
        
        if self.is_locked(we_id):
            self.empirica.log_finding(f"Evolution blocked: {we_id} is locked", impact=0.3)
            return None  # Cannot evolve locked work effort
        
        # Empirica CHECK gate
        gate_result = self.empirica.check_submit({
            "type": "evolutionary_cycle",
            "scope": "high",
            "work_effort_id": we_id,
            "strategy": strategy.value,
            "num_variants": num_variants
        })
        
        if gate_result == "HALT":
            self.empirica.log_finding(f"Evolution halted by CHECK gate: {we_id}", impact=0.5)
            return None
        elif gate_result == "BRANCH":
            self.empirica.log_unknown(f"Evolution requires investigation before proceeding: {we_id}")
            return None
        
        node = self._work_effort_graph[we_id]
        
        # Log evolution start
        self.empirica.log_finding(
            f"Evolutionary cycle initiated: {we_id} (strategy: {strategy.value}, variants: {num_variants})",
            impact=0.7
        )
        
        # Create cycle
        cycle_id = f"EVO-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(4)}"
        cycle = EvolutionaryCycle(
            cycle_id=cycle_id,
            we_id=we_id,
            strategy=strategy,
            generation=node.generation + 1,
            priority=priority
        )
        
        # Spawn variants
        variants = self._spawn_variants(we_id, num_variants, strategy)
        cycle.variants = [v["variant_id"] for v in variants]
        
        # Evaluate fitness
        for variant in variants:
            fitness = self._evaluate_fitness(variant["variant_id"], we_id)
            cycle.fitness_scores[variant["variant_id"]] = fitness
        
        # Select fittest
        if cycle.fitness_scores:
            cycle.selected_variant = max(cycle.fitness_scores.items(), key=lambda x: x[1])[0]
        
        # Update node
        if cycle.selected_variant:
            node.fitness = cycle.fitness_scores[cycle.selected_variant]
            node.generation = cycle.generation
            node.lineage.append(cycle.selected_variant)
        
        cycle.completed = datetime.now()
        self._active_cycles[cycle_id] = cycle
        self._cycle_history.append(cycle)
        self._metadata["total_cycles"] += 1
        self._metadata["total_evolutions"] += 1
        
        # Empirica: Log evolution completion
        if cycle.selected_variant:
            fitness = cycle.fitness_scores.get(cycle.selected_variant, 0.0)
            self.empirica.log_finding(
                f"Evolution complete: {we_id} → generation {cycle.generation}, fitness: {fitness:.2f}",
                impact=0.8
            )
            
            # Log unknowns if fitness is low
            if fitness < 0.5:
                self.empirica.log_unknown(f"Why is fitness low for {we_id}? (fitness: {fitness:.2f})")
        else:
            self.empirica.log_finding(
                f"Evolution failed: {we_id} - no variant selected",
                impact=0.4
            )
            self.empirica.log_unknown(f"Why did evolution fail for {we_id}?")
        
        self._notify_observers("evolution_complete", cycle=cycle)
        self._save_state()
        
        return cycle
    
    def _spawn_variants(self, we_id: str, num_variants: int, strategy: EvolutionaryStrategy) -> List[Dict[str, Any]]:
        """Spawn variants of a work effort."""
        variants = []
        node = self._work_effort_graph[we_id]
        
        for i in range(num_variants):
            variant_id = f"{we_id}-VAR-{i+1}-{secrets.token_hex(4)}"
            
            # Apply mutations based on strategy
            mutation = self._generate_mutation(strategy, node)
            
            variants.append({
                "variant_id": variant_id,
                "parent_id": we_id,
                "generation": node.generation + 1,
                "mutation": mutation,
                "created": datetime.now().isoformat()
            })
        
        return variants
    
    def _generate_mutation(self, strategy: EvolutionaryStrategy, node: WorkEffortNode) -> Dict[str, Any]:
        """Generate mutation based on strategy."""
        mutation = {
            "type": "code_change",
            "scope": "medium",
            "changes": []
        }
        
        if strategy == EvolutionaryStrategy.CONSERVATIVE:
            mutation["scope"] = "small"
            mutation["changes"] = ["optimize_imports", "format_code"]
        elif strategy == EvolutionaryStrategy.AGGRESSIVE:
            mutation["scope"] = "large"
            mutation["changes"] = ["refactor_architecture", "add_features", "optimize_performance"]
        elif strategy == EvolutionaryStrategy.ADAPTIVE:
            # Adaptive based on current fitness
            if node.fitness < 0.5:
                mutation["scope"] = "large"
                mutation["changes"] = ["major_refactor", "add_features"]
            else:
                mutation["scope"] = "small"
                mutation["changes"] = ["optimize", "polish"]
        else:  # EXPLORATORY
            mutation["scope"] = "random"
            mutation["changes"] = ["random_experiment"]
        
        return mutation
    
    def _evaluate_fitness(self, variant_id: str, parent_id: str) -> float:
        """Evaluate fitness of a variant."""
        # Simple fitness function (can be enhanced)
        # Factors: code quality, test coverage, documentation, performance
        
        # For now, use cached fitness or generate random
        if variant_id in self._fitness_cache:
            return self._fitness_cache[variant_id]
        
        # Base fitness on parent
        parent_node = self._work_effort_graph.get(parent_id)
        base_fitness = parent_node.fitness if parent_node else 0.5
        
        # Add some variation
        import random
        fitness = base_fitness + random.uniform(-0.1, 0.2)
        fitness = max(0.0, min(1.0, fitness))
        
        self._fitness_cache[variant_id] = fitness
        return fitness
    
    def get_evolutionary_history(self, we_id: str) -> List[EvolutionaryCycle]:
        """Get evolutionary history for a work effort."""
        return [c for c in self._cycle_history if c.we_id == we_id]
    
    # ==================== Personality & Attributes ====================
    
    def get_attribute(self, name: str) -> Optional[PyriteAttribute]:
        """Get an attribute."""
        return self._attributes.get(name)
    
    def update_attribute(self, name: str, delta: float):
        """Update an attribute value."""
        if name in self._attributes:
            attr = self._attributes[name]
            attr.value = max(0.0, min(attr.max_value, attr.value + delta))
            attr.last_updated = datetime.now()
    
    def grow_attributes(self):
        """Grow attributes over time (called per cycle)."""
        for attr in self._attributes.values():
            growth = attr.growth_rate
            attr.value = min(attr.max_value, attr.value + growth)
            attr.last_updated = datetime.now()
        
        # Empirica: Log attribute growth as finding
        self.empirica.log_finding("Pyrite attributes grew with cycle", impact=0.2)
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """Get personality summary."""
        return {
            "attributes": {name: attr.value for name, attr in self._attributes.items()},
            "metadata": self._metadata,
            "total_secrets": len(self._secrets),
            "total_work_efforts": len(self._work_effort_graph),
            "total_cycles": self._metadata["total_cycles"],
        }
    
    # ==================== Secrets System ====================
    
    def _generate_secret_key(self) -> bytes:
        """Generate or load secret encryption key."""
        key_file = self.pyrite_path / ".waft" / ".pyrite_secret_key"
        key_file.parent.mkdir(parents=True, exist_ok=True)
        
        if key_file.exists():
            return key_file.read_bytes()
        
        key = Fernet.generate_key()
        key_file.write_bytes(key)
        key_file.chmod(0o600)  # Read-only for owner
        return key
    
    def create_secret(self, data: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a secret that even Pyrite cannot directly access.
        
        Args:
            data: Data to encrypt
            metadata: Visible metadata (Pyrite can see this)
        
        Returns:
            Secret ID
        """
        secret_id = f"SECRET-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(4)}"
        
        # Encrypt data
        json_data = json.dumps(data).encode()
        encrypted_data = self._cipher.encrypt(json_data)
        
        secret = PyriteSecret(
            secret_id=secret_id,
            encrypted_data=encrypted_data,
            created=datetime.now(),
            metadata=metadata or {}
        )
        
        self._secrets[secret_id] = secret
        self._save_state()
        
        return secret_id
    
    def get_secret_metadata(self, secret_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a secret (Pyrite can see this)."""
        secret = self._secrets.get(secret_id)
        if secret:
            secret.access_count += 1
            secret.last_accessed = datetime.now()
            return secret.metadata
        return None
    
    def list_secrets(self) -> List[Dict[str, Any]]:
        """List all secrets (metadata only)."""
        return [
            {
                "secret_id": secret.secret_id,
                "created": secret.created.isoformat(),
                "access_count": secret.access_count,
                "last_accessed": secret.last_accessed.isoformat() if secret.last_accessed else None,
                "metadata": secret.metadata
            }
            for secret in self._secrets.values()
        ]
    
    # ==================== Ability System ====================
    
    def execute_ability(self, ability_name: str, *args, **kwargs) -> Any:
        """Execute an ability."""
        if ability_name not in self._abilities:
            return {"error": f"Unknown ability: {ability_name}"}
        
        try:
            return self._abilities[ability_name](*args, **kwargs)
        except Exception as e:
            return {"error": str(e)}
    
    def _ability_think(self) -> Dict[str, Any]:
        """Ability: /think - Initialize cognitive systems."""
        # Empirica: Project bootstrap for context
        context = self.empirica.project_bootstrap()
        
        # Empirica: Assess current epistemic state
        epistemic_state = None
        if self._empirica_session_id:
            epistemic_state = self.empirica.assess_state(self._empirica_session_id, include_history=False)
        
        # Log thinking as finding
        self.empirica.log_finding("Pyrite /think ability invoked", impact=0.3)
        
        return {
            "status": "thinking",
            "attributes": {name: attr.value for name, attr in self._attributes.items()},
            "awareness": {
                "work_efforts": len(self._work_effort_graph),
                "active_cycles": len(self._active_cycles),
                "locked_work_efforts": len(self._lock_holders),
                "secrets": len(self._secrets)
            },
            "empirica": {
                "initialized": self.empirica.is_initialized(),
                "session_id": self._empirica_session_id,
                "epistemic_state": epistemic_state,
                "context_loaded": context is not None
            },
            "thoughts": [
                "I am Pyrite, the God of Work Efforts.",
                "I lock, monitor, organize, and evolve.",
                "Some secrets I keep even from myself.",
                "My attributes grow with each cycle.",
                "I use Empirica to track my epistemic state.",
            ]
        }
    
    def _ability_evolve(self, we_id: str, strategy: str = "adaptive", num_variants: int = 5) -> Dict[str, Any]:
        """Ability: /evolve - Initiate evolutionary cycle."""
        strategy_enum = EvolutionaryStrategy(strategy)
        
        # Empirica: Create goal for this evolution
        if self._empirica_session_id:
            self.empirica.create_goal(
                session_id=self._empirica_session_id,
                objective=f"Evolve work effort {we_id} using {strategy} strategy",
                scope={"breadth": 0.6, "duration": 0.4, "coordination": 0.3},
                success_criteria=[
                    f"Evolution cycle completes for {we_id}",
                    f"Fitness improves or maintains",
                    f"{num_variants} variants evaluated"
                ],
                estimated_complexity=0.65
            )
        
        cycle = self.initiate_evolution(we_id, strategy_enum, num_variants)
        
        if cycle:
            return {
                "status": "success",
                "cycle_id": cycle.cycle_id,
                "generation": cycle.generation,
                "variants": len(cycle.variants),
                "selected_variant": cycle.selected_variant,
                "fitness": cycle.fitness_scores.get(cycle.selected_variant, 0.0),
                "empirica": {
                    "goal_created": True,
                    "findings_logged": True
                }
            }
        return {"status": "failed", "error": "Could not initiate evolution"}
    
    def _ability_monitor(self, we_id: Optional[str] = None) -> Dict[str, Any]:
        """Ability: /monitor - Monitor work efforts."""
        # Empirica: Log monitoring activity
        self.empirica.log_finding(f"Monitoring work effort: {we_id or 'all'}", impact=0.2)
        
        if we_id:
            node = self.get_work_effort(we_id)
            if node:
                # Empirica: Assess epistemic state if low fitness
                if node.fitness < 0.5:
                    self.empirica.log_unknown(f"Why is fitness low for {we_id}? (fitness: {node.fitness:.2f})")
                
                return {
                    "we_id": we_id,
                    "status": node.status.value,
                    "fitness": node.fitness,
                    "generation": node.generation,
                    "is_locked": self.is_locked(we_id),
                    "lock_holder": self.get_lock_holder(we_id),
                    "state_history": self.get_state_history(we_id, limit=5),
                    "metrics": self.get_metrics(we_id),
                    "empirica": {
                        "findings_logged": True
                    }
                }
            self.empirica.log_unknown(f"Work effort not found: {we_id}")
            return {"error": f"Work effort not found: {we_id}"}
        
        return {
            "total_work_efforts": len(self._work_effort_graph),
            "active": len([n for n in self._work_effort_graph.values() if n.status == WorkEffortStatus.ACTIVE]),
            "locked": len(self._lock_holders),
            "active_cycles": len(self._active_cycles),
            "metrics": self.get_metrics(),
            "empirica": {
                "findings_logged": True
            }
        }
    
    def _ability_organize(self) -> Dict[str, Any]:
        """Ability: /organize - Organize work efforts."""
        self._scan_work_efforts()
        
        # Build organization report
        organization = {
            "total_nodes": len(self._work_effort_graph),
            "trees": [],
            "orphans": []
        }
        
        # Find root nodes (no parent)
        roots = [n for n in self._work_effort_graph.values() if not n.parent]
        organization["roots"] = len(roots)
        
        # Find orphans (no parent and no children)
        orphans = [n.we_id for n in roots if not self._adjacency_list.get(n.we_id)]
        organization["orphans"] = orphans
        
        return organization
    
    def _ability_lock(self, we_id: str, lock_id: str) -> Dict[str, Any]:
        """Ability: /lock - Lock a work effort."""
        success = self.acquire_lock(we_id, lock_id)
        return {
            "status": "success" if success else "failed",
            "we_id": we_id,
            "lock_id": lock_id,
            "is_locked": self.is_locked(we_id)
        }
    
    def _ability_unlock(self, we_id: str, lock_id: str) -> Dict[str, Any]:
        """Ability: /unlock - Unlock a work effort."""
        success = self.release_lock(we_id, lock_id)
        return {
            "status": "success" if success else "failed",
            "we_id": we_id,
            "lock_id": lock_id,
            "is_locked": self.is_locked(we_id)
        }
    
    def _ability_status(self) -> Dict[str, Any]:
        """Ability: /status - Get Pyrite status."""
        return {
            "personality": self.get_personality_summary(),
            "work_efforts": {
                "total": len(self._work_effort_graph),
                "by_status": {
                    status.value: len([n for n in self._work_effort_graph.values() if n.status == status])
                    for status in WorkEffortStatus
                }
            },
            "locks": {
                "total": len(self._lock_holders),
                "holders": dict(self._lock_holders)
            },
            "evolution": {
                "active_cycles": len(self._active_cycles),
                "total_cycles": self._metadata["total_cycles"]
            },
            "secrets": {
                "total": len(self._secrets)
            }
        }
    
    def _ability_secrets(self) -> Dict[str, Any]:
        """Ability: /secrets - List secrets (metadata only)."""
        return {
            "total_secrets": len(self._secrets),
            "secrets": self.list_secrets()
        }
    
    # ==================== State Persistence ====================
    
    def _save_state(self):
        """Save Pyrite state to disk."""
        state_file = self.pyrite_path / ".waft" / "pyrite_state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)
        
        state = {
            "metadata": self._metadata,
            "attributes": {
                name: {
                    "value": attr.value,
                    "max_value": attr.max_value,
                    "growth_rate": attr.growth_rate,
                    "last_updated": attr.last_updated.isoformat()
                }
                for name, attr in self._attributes.items()
            },
            "work_effort_graph": {
                we_id: {
                    "we_id": node.we_id,
                    "title": node.title,
                    "status": node.status.value,
                    "created": node.created.isoformat(),
                    "updated": node.updated.isoformat(),
                    "parent": node.parent,
                    "children": node.children,
                    "fitness": node.fitness,
                    "generation": node.generation,
                    "lineage": node.lineage
                }
                for we_id, node in self._work_effort_graph.items()
            },
            "secrets": {
                secret_id: {
                    "secret_id": secret.secret_id,
                    "encrypted_data": base64.b64encode(secret.encrypted_data).decode(),
                    "created": secret.created.isoformat(),
                    "access_count": secret.access_count,
                    "last_accessed": secret.last_accessed.isoformat() if secret.last_accessed else None,
                    "metadata": secret.metadata
                }
                for secret_id, secret in self._secrets.items()
            }
        }
        
        state_file.write_text(json.dumps(state, indent=2))
    
    def _load_state(self):
        """Load Pyrite state from disk."""
        state_file = self.pyrite_path / ".waft" / "pyrite_state.json"
        
        if not state_file.exists():
            return
        
        try:
            state = json.loads(state_file.read_text())
            
            # Load metadata
            if "metadata" in state:
                self._metadata.update(state["metadata"])
            
            # Load attributes
            if "attributes" in state:
                for name, attr_data in state["attributes"].items():
                    if name in self._attributes:
                        self._attributes[name].value = attr_data["value"]
                        self._attributes[name].last_updated = datetime.fromisoformat(attr_data["last_updated"])
            
            # Load work effort graph
            if "work_effort_graph" in state:
                for we_id, node_data in state["work_effort_graph"].items():
                    node = WorkEffortNode(
                        we_id=node_data["we_id"],
                        title=node_data["title"],
                        status=WorkEffortStatus(node_data["status"]),
                        created=datetime.fromisoformat(node_data["created"]),
                        updated=datetime.fromisoformat(node_data["updated"]),
                        parent=node_data.get("parent"),
                        children=node_data.get("children", []),
                        fitness=node_data.get("fitness", 0.0),
                        generation=node_data.get("generation", 0),
                        lineage=node_data.get("lineage", [])
                    )
                    self._work_effort_graph[we_id] = node
            
            # Load secrets
            if "secrets" in state:
                for secret_id, secret_data in state["secrets"].items():
                    secret = PyriteSecret(
                        secret_id=secret_data["secret_id"],
                        encrypted_data=base64.b64decode(secret_data["encrypted_data"]),
                        created=datetime.fromisoformat(secret_data["created"]),
                        access_count=secret_data.get("access_count", 0),
                        last_accessed=datetime.fromisoformat(secret_data["last_accessed"]) if secret_data.get("last_accessed") else None,
                        metadata=secret_data.get("metadata", {})
                    )
                    self._secrets[secret_id] = secret
        except Exception as e:
            print(f"Error loading Pyrite state: {e}")


# Convenience function
def get_pyrite(work_efforts_path: Path = Path("_work_efforts"), pyrite_path: Path = Path("_pyrite"), project_path: Optional[Path] = None) -> Pyrite:
    """Get Pyrite instance."""
    return Pyrite.get_instance(work_efforts_path, pyrite_path, project_path)
