"""
Scientist God: Scientific Research Management Entity

Manages the complete scientific research lifecycle:
- Hypothesis generation and testing
- Experiment design and execution  
- Data collection and analysis
- Whitepaper generation via Typst
- Integration with Oracle for epistemic tracking
- Publication-quality documentation

Unlike Chief Wiggum's "investigation methods," this uses actual rigor.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
import subprocess
from dataclasses import dataclass, field
from enum import Enum


class ExperimentStatus(Enum):
    """Status of a scientific experiment."""
    HYPOTHESIZED = "hypothesized"
    DESIGNED = "designed"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PUBLISHED = "published"


class EvidenceType(Enum):
    """Types of scientific evidence."""
    SOURCE_CODE = "source_code"
    TEST_OUTPUT = "test_output"
    TELEMETRY_DATA = "telemetry_data"
    BENCHMARK_RESULT = "benchmark_result"
    USER_STUDY = "user_study"
    COMPARATIVE_ANALYSIS = "comparative_analysis"


@dataclass
class Hypothesis:
    """A scientific hypothesis to be tested."""
    id: str
    statement: str
    created_at: datetime
    status: ExperimentStatus = ExperimentStatus.HYPOTHESIZED
    confidence: float = 0.0  # 0.0-1.0
    evidence_for: List[Dict[str, Any]] = field(default_factory=list)
    evidence_against: List[Dict[str, Any]] = field(default_factory=list)
    
    def add_evidence(self, evidence_type: EvidenceType, location: str, 
                     content: str, supports: bool = True):
        """Add evidence for or against the hypothesis."""
        evidence = {
            "type": evidence_type.value,
            "location": location,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        }
        
        if supports:
            self.evidence_for.append(evidence)
        else:
            self.evidence_against.append(evidence)
        
        # Update confidence based on evidence balance
        self._update_confidence()
    
    def _update_confidence(self):
        """Calculate confidence based on evidence."""
        total_evidence = len(self.evidence_for) + len(self.evidence_against)
        if total_evidence == 0:
            self.confidence = 0.0
        else:
            self.confidence = len(self.evidence_for) / total_evidence


@dataclass
class Experiment:
    """A scientific experiment."""
    id: str
    name: str
    hypothesis: Hypothesis
    methodology: str
    status: ExperimentStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    results: Dict[str, Any] = field(default_factory=dict)
    whitepaper_path: Optional[Path] = None


class ScientistGod:
    """
    Scientific Research Management Entity.
    
    Manages:
    - Hypothesis generation and tracking
    - Experiment design and execution
    - Evidence collection and analysis
    - Whitepaper generation (integrates with whitepaper_generator.py)
    - Integration with Oracle for epistemic tracking
    - Publication workflow
    
    Example:
        scientist = ScientistGod(project_path=Path("/path/to/project"))
        
        # Create hypothesis
        hyp = scientist.hypothesize(
            "WAFT genome system uses SHA-256 hashing",
            expected_confidence=0.8
        )
        
        # Design experiment
        exp = scientist.design_experiment(
            hypothesis=hyp,
            methodology="Inspect source code and run tests"
        )
        
        # Collect evidence
        scientist.collect_evidence(
            experiment=exp,
            evidence_type=EvidenceType.SOURCE_CODE,
            location="src/waft/base.py:105-141",
            content="def _compute_genome_id()...",
            supports=True
        )
        
        # Generate whitepaper
        scientist.generate_whitepaper(
            experiment=exp,
            title="WAFT Genome System Analysis"
        )
    """
    
    def __init__(
        self,
        project_path: Path,
        oracle=None,  # TheOracle instance for epistemic tracking
        whitepaper_generator_path: Optional[Path] = None,
    ):
        """
        Initialize Scientist God.
        
        Args:
            project_path: Path to project root
            oracle: Optional TheOracle instance
            whitepaper_generator_path: Path to whitepaper_generator.py
        """
        self.project_path = project_path
        self.oracle = oracle
        self.whitepaper_generator = whitepaper_generator_path or (
            project_path / "tools" / "whitepaper_generator.py"
        )
        
        # Create scientific workspace
        self.science_dir = project_path / ".science"
        self.science_dir.mkdir(exist_ok=True)
        
        self.hypotheses_dir = self.science_dir / "hypotheses"
        self.hypotheses_dir.mkdir(exist_ok=True)
        
        self.experiments_dir = self.science_dir / "experiments"
        self.experiments_dir.mkdir(exist_ok=True)
        
        self.whitepapers_dir = self.science_dir / "whitepapers"
        self.whitepapers_dir.mkdir(exist_ok=True)
        
        # Load existing state
        self.hypotheses: Dict[str, Hypothesis] = {}
        self.experiments: Dict[str, Experiment] = {}
        self._load_state()
    
    def hypothesize(
        self,
        statement: str,
        expected_confidence: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Hypothesis:
        """
        Generate a new scientific hypothesis.
        
        Args:
            statement: The hypothesis statement
            expected_confidence: Expected confidence level (0.0-1.0)
            metadata: Optional additional metadata
        
        Returns:
            Hypothesis object
        """
        hyp_id = f"hyp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        hypothesis = Hypothesis(
            id=hyp_id,
            statement=statement,
            created_at=datetime.now(),
            confidence=expected_confidence,
        )
        
        self.hypotheses[hyp_id] = hypothesis
        self._save_hypothesis(hypothesis)
        
        # Log to Oracle if available
        if self.oracle:
            self.oracle.log_finding(
                finding=f"Hypothesis: {statement}",
                impact=expected_confidence,
                context={"hypothesis_id": hyp_id}
            )
        
        return hypothesis
    
    def design_experiment(
        self,
        hypothesis: Hypothesis,
        name: str,
        methodology: str,
        investigation_techniques: Optional[List[str]] = None
    ) -> Experiment:
        """
        Design an experiment to test a hypothesis.
        
        Args:
            hypothesis: The hypothesis to test
            name: Experiment name
            methodology: Description of methodology
            investigation_techniques: List of techniques to use
        
        Returns:
            Experiment object
        """
        exp_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        experiment = Experiment(
            id=exp_id,
            name=name,
            hypothesis=hypothesis,
            methodology=methodology,
            status=ExperimentStatus.DESIGNED,
            created_at=datetime.now(),
        )
        
        if investigation_techniques:
            experiment.results["techniques"] = investigation_techniques
        
        self.experiments[exp_id] = experiment
        self._save_experiment(experiment)
        
        # Update hypothesis status
        hypothesis.status = ExperimentStatus.DESIGNED
        self._save_hypothesis(hypothesis)
        
        return experiment
    
    def run_experiment(
        self,
        experiment: Experiment,
        execute_fn: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Execute an experiment.
        
        Args:
            experiment: The experiment to run
            execute_fn: Optional function to execute the experiment
        
        Returns:
            Results dictionary
        """
        experiment.status = ExperimentStatus.RUNNING
        experiment.started_at = datetime.now()
        self._save_experiment(experiment)
        
        try:
            if execute_fn:
                results = execute_fn(experiment)
                experiment.results.update(results)
            
            experiment.status = ExperimentStatus.COMPLETED
            experiment.completed_at = datetime.now()
            
        except Exception as e:
            experiment.status = ExperimentStatus.FAILED
            experiment.results["error"] = str(e)
        
        finally:
            self._save_experiment(experiment)
        
        return experiment.results
    
    def collect_evidence(
        self,
        experiment: Experiment,
        evidence_type: EvidenceType,
        location: str,
        content: str,
        supports: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Collect evidence for an experiment's hypothesis.
        
        Args:
            experiment: The experiment
            evidence_type: Type of evidence
            location: Evidence location (file path, URL, etc.)
            content: Evidence content
            supports: Whether evidence supports hypothesis
            metadata: Optional metadata
        """
        experiment.hypothesis.add_evidence(
            evidence_type=evidence_type,
            location=location,
            content=content,
            supports=supports
        )
        
        # Store in experiment results
        if "evidence" not in experiment.results:
            experiment.results["evidence"] = []
        
        experiment.results["evidence"].append({
            "type": evidence_type.value,
            "location": location,
            "supports": supports,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        })
        
        self._save_hypothesis(experiment.hypothesis)
        self._save_experiment(experiment)
        
        # Log to Oracle
        if self.oracle:
            self.oracle.log_finding(
                finding=f"Evidence: {location}",
                impact=experiment.hypothesis.confidence,
                context={
                    "experiment_id": experiment.id,
                    "evidence_type": evidence_type.value,
                    "supports": supports,
                }
            )
    
    def generate_whitepaper(
        self,
        experiment: Experiment,
        title: str,
        author: str = "Technical Analyst",
        auto_populate: bool = True,
    ) -> Path:
        """
        Generate a whitepaper for an experiment.
        
        Uses the whitepaper_generator.py tool to create a professional
        publication-quality document.
        
        Args:
            experiment: The experiment to document
            title: Whitepaper title
            author: Author name
            auto_populate: Whether to auto-populate sections with evidence
        
        Returns:
            Path to whitepaper directory
        """
        # Create whitepaper project
        wp_dir = self.whitepapers_dir / experiment.id
        wp_dir.mkdir(exist_ok=True)
        
        # Initialize whitepaper
        try:
            result = subprocess.run(
                ["python3", str(self.whitepaper_generator), "init", title],
                cwd=wp_dir,
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Whitepaper init failed: {result.stderr}")
        
        except FileNotFoundError:
            print(f"⚠️ Whitepaper generator not found at {self.whitepaper_generator}")
            print("Creating basic structure manually...")
            self._create_basic_whitepaper_structure(wp_dir, experiment, title, author)
            return wp_dir
        
        # Auto-populate with experiment data
        if auto_populate:
            self._populate_whitepaper_sections(wp_dir, experiment)
        
        experiment.whitepaper_path = wp_dir
        self._save_experiment(experiment)
        
        return wp_dir
    
    def _populate_whitepaper_sections(
        self,
        wp_dir: Path,
        experiment: Experiment
    ):
        """Auto-populate whitepaper sections with experiment data."""
        sections_dir = wp_dir / "sections"
        
        # Abstract
        abstract_file = sections_dir / "01_abstract.typ"
        abstract_content = f"""#import "../whitepaper_functions.typ": callout, evidence, metric

= Abstract

This whitepaper presents an investigation of: *{experiment.hypothesis.statement}*

#callout(type: "success", title: "Hypothesis Confidence", [
  *Confidence:* {experiment.hypothesis.confidence:.1%}
  *Status:* {experiment.status.value}
  *Evidence Collected:* {len(experiment.hypothesis.evidence_for)} supporting, {len(experiment.hypothesis.evidence_against)} contradicting
])

*Methodology:* {experiment.methodology}

*Key Findings:*
"""
        
        # Add evidence summaries
        for i, evidence in enumerate(experiment.hypothesis.evidence_for[:5], 1):
            abstract_content += f"\n{i}. Evidence from {evidence['location']}"
        
        with open(abstract_file, 'w') as f:
            f.write(abstract_content)
        
        # Findings section with all evidence
        findings_file = sections_dir / "30_findings.typ"
        findings_content = """#import "../whitepaper_functions.typ": callout, evidence, metric

= Findings

== Evidence Summary

"""
        
        for i, evid in enumerate(experiment.hypothesis.evidence_for, 1):
            findings_content += f"""
=== Evidence {i}: {evid['type']}

#evidence("{evid['location']}", [
  {evid['content'][:500]}...
])

"""
        
        with open(findings_file, 'w') as f:
            f.write(findings_content)
    
    def compile_whitepaper(
        self,
        experiment: Experiment,
        section_id: Optional[str] = None
    ) -> Optional[Path]:
        """
        Compile whitepaper to PDF.
        
        Args:
            experiment: The experiment
            section_id: Optional specific section to compile
        
        Returns:
            Path to compiled PDF
        """
        if not experiment.whitepaper_path:
            print(f"❌ No whitepaper initialized for experiment {experiment.id}")
            return None
        
        try:
            if section_id:
                # Compile specific section
                result = subprocess.run(
                    ["python3", str(self.whitepaper_generator), "compile-section", section_id],
                    cwd=experiment.whitepaper_path,
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                
                pdf_path = experiment.whitepaper_path / "section_pdfs" / f"{section_id}.pdf"
            else:
                # Compile complete document
                result = subprocess.run(
                    ["python3", str(self.whitepaper_generator), "compile-all"],
                    cwd=experiment.whitepaper_path,
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                
                # Find the generated PDF
                pdf_files = list(experiment.whitepaper_path.glob("*_COMPLETE.pdf"))
                pdf_path = pdf_files[0] if pdf_files else None
            
            if result.returncode == 0 and pdf_path and pdf_path.exists():
                print(f"✅ Whitepaper compiled: {pdf_path}")
                
                # Auto-open
                subprocess.run(["open", str(pdf_path)])
                
                return pdf_path
            else:
                print(f"❌ Compilation failed: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Compilation error: {e}")
            return None
    
    def publish(
        self,
        experiment: Experiment,
        publish_to: str = "local",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Publish experiment results.
        
        Args:
            experiment: The experiment to publish
            publish_to: Publication target (local, arxiv, github, etc.)
            metadata: Optional publication metadata
        
        Returns:
            Publication details
        """
        if experiment.status != ExperimentStatus.COMPLETED:
            raise ValueError(f"Experiment must be completed to publish (status: {experiment.status.value})")
        
        experiment.status = ExperimentStatus.PUBLISHED
        
        publication = {
            "experiment_id": experiment.id,
            "hypothesis": experiment.hypothesis.statement,
            "confidence": experiment.hypothesis.confidence,
            "published_at": datetime.now().isoformat(),
            "published_to": publish_to,
            "whitepaper_path": str(experiment.whitepaper_path) if experiment.whitepaper_path else None,
            "metadata": metadata or {}
        }
        
        # Save publication record
        pub_file = self.science_dir / "publications.jsonl"
        with open(pub_file, 'a') as f:
            f.write(json.dumps(publication) + "\n")
        
        self._save_experiment(experiment)
        
        return publication
    
    def status(self) -> Dict[str, Any]:
        """Get status of all scientific work."""
        return {
            "hypotheses": {
                "total": len(self.hypotheses),
                "by_status": self._count_by_status(self.hypotheses.values(), "status"),
            },
            "experiments": {
                "total": len(self.experiments),
                "by_status": self._count_by_status(self.experiments.values(), "status"),
                "with_whitepapers": sum(1 for e in self.experiments.values() if e.whitepaper_path),
            },
            "whitepapers": len(list(self.whitepapers_dir.glob("*/"))),
        }
    
    def _count_by_status(self, items, status_attr: str) -> Dict[str, int]:
        """Count items by status."""
        counts = {}
        for item in items:
            status = getattr(item, status_attr).value
            counts[status] = counts.get(status, 0) + 1
        return counts
    
    def _save_hypothesis(self, hypothesis: Hypothesis):
        """Save hypothesis to disk."""
        file_path = self.hypotheses_dir / f"{hypothesis.id}.json"
        with open(file_path, 'w') as f:
            json.dump({
                "id": hypothesis.id,
                "statement": hypothesis.statement,
                "created_at": hypothesis.created_at.isoformat(),
                "status": hypothesis.status.value,
                "confidence": hypothesis.confidence,
                "evidence_for": hypothesis.evidence_for,
                "evidence_against": hypothesis.evidence_against,
            }, f, indent=2)
    
    def _save_experiment(self, experiment: Experiment):
        """Save experiment to disk."""
        file_path = self.experiments_dir / f"{experiment.id}.json"
        with open(file_path, 'w') as f:
            json.dump({
                "id": experiment.id,
                "name": experiment.name,
                "hypothesis_id": experiment.hypothesis.id,
                "methodology": experiment.methodology,
                "status": experiment.status.value,
                "created_at": experiment.created_at.isoformat(),
                "started_at": experiment.started_at.isoformat() if experiment.started_at else None,
                "completed_at": experiment.completed_at.isoformat() if experiment.completed_at else None,
                "results": experiment.results,
                "whitepaper_path": str(experiment.whitepaper_path) if experiment.whitepaper_path else None,
            }, f, indent=2)
    
    def _load_state(self):
        """Load existing hypotheses and experiments."""
        # Load hypotheses
        for hyp_file in self.hypotheses_dir.glob("*.json"):
            with open(hyp_file) as f:
                data = json.load(f)
                hypothesis = Hypothesis(
                    id=data["id"],
                    statement=data["statement"],
                    created_at=datetime.fromisoformat(data["created_at"]),
                    status=ExperimentStatus(data["status"]),
                    confidence=data["confidence"],
                    evidence_for=data.get("evidence_for", []),
                    evidence_against=data.get("evidence_against", []),
                )
                self.hypotheses[hypothesis.id] = hypothesis
        
        # Load experiments
        for exp_file in self.experiments_dir.glob("*.json"):
            with open(exp_file) as f:
                data = json.load(f)
                hypothesis = self.hypotheses.get(data["hypothesis_id"])
                if hypothesis:
                    experiment = Experiment(
                        id=data["id"],
                        name=data["name"],
                        hypothesis=hypothesis,
                        methodology=data["methodology"],
                        status=ExperimentStatus(data["status"]),
                        created_at=datetime.fromisoformat(data["created_at"]),
                        started_at=datetime.fromisoformat(data["started_at"]) if data.get("started_at") else None,
                        completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
                        results=data.get("results", {}),
                        whitepaper_path=Path(data["whitepaper_path"]) if data.get("whitepaper_path") else None,
                    )
                    self.experiments[experiment.id] = experiment
    
    def _create_basic_whitepaper_structure(
        self,
        wp_dir: Path,
        experiment: Experiment,
        title: str,
        author: str
    ):
        """Create basic whitepaper structure when generator unavailable."""
        (wp_dir / "sections").mkdir(exist_ok=True)
        
        # Create basic README
        readme = wp_dir / "README.md"
        with open(readme, 'w') as f:
            f.write(f"""# {title}

**Experiment:** {experiment.name}
**Hypothesis:** {experiment.hypothesis.statement}
**Author:** {author}
**Status:** {experiment.status.value}

## Evidence

""")
            for evidence in experiment.hypothesis.evidence_for:
                f.write(f"- {evidence['type']}: {evidence['location']}\n")


# Example usage function
def example_waft_analysis():
    """Example: Using Scientist God to analyze WAFT."""
    scientist = ScientistGod(project_path=Path("/path/to/waft"))
    
    # 1. Hypothesize
    hyp = scientist.hypothesize(
        statement="WAFT genome system uses SHA-256 hashing for deterministic agent identification",
        expected_confidence=0.8
    )
    
    # 2. Design experiment
    exp = scientist.design_experiment(
        hypothesis=hyp,
        name="WAFT Genome System Verification",
        methodology="Inspect source code, run tests, verify hash computation",
        investigation_techniques=[
            "Source code inspection",
            "Test execution (pytest)",
            "Database query verification"
        ]
    )
    
    # 3. Collect evidence
    scientist.collect_evidence(
        experiment=exp,
        evidence_type=EvidenceType.SOURCE_CODE,
        location="src/waft/base.py:105-141",
        content="""
def _compute_genome_id(self) -> str:
    components = []
    code_hash = self._get_code_hash()
    components.append(code_hash)
    
    config_json = json.dumps(self.config, sort_keys=True, default=str)
    config_hash = hashlib.sha256(config_json.encode()).hexdigest()
    components.append(config_hash)
    
    combined = "|".join(components)
    genome_id = hashlib.sha256(combined.encode()).hexdigest()
    return genome_id
        """,
        supports=True
    )
    
    scientist.collect_evidence(
        experiment=exp,
        evidence_type=EvidenceType.TEST_OUTPUT,
        location="pytest tests/test_genome.py",
        content="5 passed in 0.23s - genome_id computation verified",
        supports=True
    )
    
    # 4. Generate whitepaper
    wp_dir = scientist.generate_whitepaper(
        experiment=exp,
        title="WAFT Genome System Analysis",
        author="Dr. Aria Vex",
        auto_populate=True
    )
    
    # 5. Compile whitepaper
    pdf_path = scientist.compile_whitepaper(exp)
    
    # 6. Publish
    publication = scientist.publish(
        experiment=exp,
        publish_to="github",
        metadata={"repo": "waft-analysis", "branch": "main"}
    )
    
    print(f"✅ Analysis complete!")
    print(f"   Hypothesis confidence: {hyp.confidence:.1%}")
    print(f"   Whitepaper: {pdf_path}")
    print(f"   Published: {publication['published_at']}")


if __name__ == "__main__":
    # Run example
    example_waft_analysis()
