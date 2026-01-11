"""
DocumentBuilder Study Gym
=========================

A scientific method-based learning system for discovering how to use PDF tools.
The system observes, forms hypotheses, tests them, and learns from results.

Philosophy:
-----------
This is a "practice tool" where the system can:
1. Observe its own behavior
2. Form hypotheses about what works
3. Test those hypotheses
4. Record findings
5. Refine understanding

It's the Scientific Method applied to tool discovery.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import re

from .document_builder import DocumentBuilder, DocumentConfig, TemplateType


@dataclass
class Observation:
    """A single observation during a study session."""
    timestamp: str
    action: str
    result: Any
    notes: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Hypothesis:
    """A hypothesis formed during study."""
    statement: str
    reasoning: str
    assumptions: List[str]
    test_plan: str
    confidence: float = 0.5  # 0.0 to 1.0
    status: str = "pending"  # pending, testing, confirmed, refuted


@dataclass
class StudySession:
    """A complete study session with observations and hypotheses."""
    session_id: str
    challenge_config: Dict[str, Any]
    observations: List[Observation] = field(default_factory=list)
    hypotheses: List[Hypothesis] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)
    conclusions: List[str] = field(default_factory=list)
    start_time: str = ""
    end_time: str = ""


class StudyGym:
    """
    A gym for practicing and learning DocumentBuilder capabilities.
    
    Uses the Scientific Method:
    1. Observe - Watch what happens
    2. Question - What patterns do I see?
    3. Hypothesize - I think X causes Y
    4. Test - Try it and see
    5. Analyze - What did I learn?
    6. Conclude - What's true beyond reasonable doubt?
    """
    
    def __init__(self, output_dir: Path = Path("_work_efforts/study_gym")):
        """Initialize the study gym."""
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session: Optional[StudySession] = None
    
    def start_session(self, challenge_config: Dict[str, Any]) -> StudySession:
        """Start a new study session with a challenge configuration."""
        session_id = f"study_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.session = StudySession(
            session_id=session_id,
            challenge_config=challenge_config,
            start_time=datetime.now().isoformat()
        )
        
        return self.session
    
    def observe(self, action: str, result: Any, notes: str = "", **metrics) -> Observation:
        """Record an observation."""
        if not self.session:
            raise ValueError("No active session. Call start_session() first.")
        
        obs = Observation(
            timestamp=datetime.now().isoformat(),
            action=action,
            result=result,
            notes=notes,
            metrics=metrics
        )
        
        self.session.observations.append(obs)
        return obs
    
    def form_hypothesis(
        self,
        statement: str,
        reasoning: str,
        assumptions: List[str],
        test_plan: str,
        confidence: float = 0.5
    ) -> Hypothesis:
        """Form a hypothesis based on observations."""
        if not self.session:
            raise ValueError("No active session. Call start_session() first.")
        
        hypothesis = Hypothesis(
            statement=statement,
            reasoning=reasoning,
            assumptions=assumptions,
            test_plan=test_plan,
            confidence=confidence,
            status="pending"
        )
        
        self.session.hypotheses.append(hypothesis)
        return hypothesis
    
    def test_hypothesis(self, hypothesis: Hypothesis, test_result: Dict[str, Any]) -> None:
        """Test a hypothesis and update its status."""
        hypothesis.status = "testing"
        
        # Record test
        self.observe(
            action=f"test_hypothesis: {hypothesis.statement}",
            result=test_result,
            notes=f"Testing: {hypothesis.test_plan}"
        )
        
        # Evaluate result
        if test_result.get("confirmed", False):
            hypothesis.status = "confirmed"
            hypothesis.confidence = min(1.0, hypothesis.confidence + 0.2)
        elif test_result.get("refuted", False):
            hypothesis.status = "refuted"
            hypothesis.confidence = max(0.0, hypothesis.confidence - 0.3)
        else:
            hypothesis.status = "pending"
    
    def record_finding(self, finding: str) -> None:
        """Record a finding from observations."""
        if not self.session:
            raise ValueError("No active session.")
        
        self.session.findings.append(finding)
    
    def conclude(self, conclusion: str) -> None:
        """Record a conclusion reached beyond reasonable doubt."""
        if not self.session:
            raise ValueError("No active session.")
        
        self.session.conclusions.append(conclusion)
    
    def end_session(self) -> Path:
        """End the session and save results."""
        if not self.session:
            raise ValueError("No active session.")
        
        self.session.end_time = datetime.now().isoformat()
        
        # Save session data
        session_file = self.output_dir / f"{self.session.session_id}.json"
        session_data = {
            "session_id": self.session.session_id,
            "challenge_config": self.session.challenge_config,
            "start_time": self.session.start_time,
            "end_time": self.session.end_time,
            "observations": [
                {
                    "timestamp": obs.timestamp,
                    "action": obs.action,
                    "result": str(obs.result),
                    "notes": obs.notes,
                    "metrics": obs.metrics
                }
                for obs in self.session.observations
            ],
            "hypotheses": [
                {
                    "statement": h.statement,
                    "reasoning": h.reasoning,
                    "assumptions": h.assumptions,
                    "test_plan": h.test_plan,
                    "confidence": h.confidence,
                    "status": h.status
                }
                for h in self.session.hypotheses
            ],
            "findings": self.session.findings,
            "conclusions": self.session.conclusions
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # Generate summary report
        report_path = self._generate_summary_report()
        
        return report_path
    
    def _generate_summary_report(self) -> Path:
        """Generate a summary report of the study session."""
        if not self.session:
            raise ValueError("No active session.")
        
        # Create markdown report
        report_content = f"""# Study Session Report: {self.session.session_id}

**Challenge:** {self.session.challenge_config.get('name', 'Unknown')}
**Start:** {self.session.start_time}
**End:** {self.session.end_time}

## Challenge Configuration

```json
{json.dumps(self.session.challenge_config, indent=2)}
```

## Observations ({len(self.session.observations)} total)

"""
        
        for i, obs in enumerate(self.session.observations, 1):
            report_content += f"""
### Observation {i}

- **Action:** {obs.action}
- **Result:** {obs.result}
- **Notes:** {obs.notes}
- **Metrics:** {json.dumps(obs.metrics, indent=2)}
- **Time:** {obs.timestamp}

"""
        
        report_content += f"""
## Hypotheses ({len(self.session.hypotheses)} total)

"""
        
        for i, hyp in enumerate(self.session.hypotheses, 1):
            report_content += f"""
### Hypothesis {i}: {hyp.statement}

- **Status:** {hyp.status}
- **Confidence:** {hyp.confidence:.2f}
- **Reasoning:** {hyp.reasoning}
- **Assumptions:**
"""
            for assumption in hyp.assumptions:
                report_content += f"  - {assumption}\n"
            
            report_content += f"- **Test Plan:** {hyp.test_plan}\n\n"
        
        report_content += f"""
## Findings ({len(self.session.findings)} total)

"""
        for finding in self.session.findings:
            report_content += f"- {finding}\n"
        
        report_content += f"""
## Conclusions ({len(self.session.conclusions)} total)

"""
        for conclusion in self.session.conclusions:
            report_content += f"- {conclusion}\n"
        
        # Save report
        report_path = self.output_dir / f"{self.session.session_id}_report.md"
        report_path.write_text(report_content)
        
        return report_path


class ChallengeGenerator:
    """
    Generates "mad lib" style challenges for the study gym.
    
    Challenges are variable obstacle courses that test different
    aspects of DocumentBuilder capabilities.
    """
    
    @staticmethod
    def generate_challenge(template_name: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a challenge from a template with variables filled in.
        
        Args:
            template_name: Name of challenge template
            variables: Variables to fill in the template
            
        Returns:
            Challenge configuration dictionary
        """
        templates = ChallengeGenerator._get_templates()
        
        if template_name not in templates:
            raise ValueError(f"Unknown template: {template_name}. Available: {list(templates.keys())}")
        
        template = templates[template_name].copy()
        challenge = {}
        
        # Fill in variables recursively
        def fill_variables(obj, vars_dict):
            if isinstance(obj, dict):
                return {k: fill_variables(v, vars_dict) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [fill_variables(item, vars_dict) for item in obj]
            elif isinstance(obj, str):
                # Replace {variable} patterns
                result = obj
                for key, value in vars_dict.items():
                    result = result.replace(f"{{{key}}}", str(value))
                return result
            else:
                return obj
        
        challenge = fill_variables(template, variables)
        challenge['variables_used'] = variables
        
        return challenge
    
    @staticmethod
    def _get_templates() -> Dict[str, Dict[str, Any]]:
        """Get available challenge templates."""
        return {
            "page_constraint": {
                "name": "Page Constraint Challenge",
                "description": "Create a document with exactly {target_pages} pages",
                "objective": "Discover how to control page count",
                "constraints": {
                    "exact_pages": "{target_pages}",
                    "printer_friendly": True
                },
                "content_template": "{content}",
                "variables": ["target_pages", "content"]
            },
            "content_fitting": {
                "name": "Content Fitting Challenge",
                "description": "Fit {content_length} words into {max_pages} pages",
                "objective": "Learn how content length affects page count",
                "constraints": {
                    "max_pages": "{max_pages}"
                },
                "content_template": "{content}",
                "variables": ["content_length", "max_pages", "content"]
            },
            "style_exploration": {
                "name": "Style Exploration Challenge",
                "description": "Create {document_type} with {style_features}",
                "objective": "Explore different styling options",
                "constraints": {},
                "content_template": "{content}",
                "variables": ["document_type", "style_features", "content"]
            },
            "multi_document": {
                "name": "Multi-Document Challenge",
                "description": "Create a collection with {num_docs} documents, each {target_pages} pages",
                "objective": "Learn DocumentCollection capabilities",
                "constraints": {
                    "per_document_pages": "{target_pages}"
                },
                "content_template": "{content}",
                "variables": ["num_docs", "target_pages", "content"]
            },
            "printer_friendly": {
                "name": "Printer-Friendly Challenge",
                "description": "Create printer-friendly version with {specific_requirements}",
                "objective": "Master printer-friendly conversion",
                "constraints": {
                    "printer_friendly": True,
                    "exact_pages": "{target_pages}"
                },
                "content_template": "{content}",
                "variables": ["specific_requirements", "target_pages", "content"]
            }
        }
    
    @staticmethod
    def list_templates() -> List[str]:
        """List available challenge templates."""
        return list(ChallengeGenerator._get_templates().keys())


def run_study_session(challenge_config: Dict[str, Any], output_dir: Optional[Path] = None) -> StudySession:
    """
    Run a complete study session following the Scientific Method.
    
    This is the main entry point for the study gym.
    """
    if output_dir is None:
        output_dir = Path("_work_efforts/study_gym")
    gym = StudyGym(output_dir=output_dir)
    session = gym.start_session(challenge_config)
    
    print("=" * 60)
    print("🔬 Study Gym Session Started")
    print("=" * 60)
    print(f"Challenge: {challenge_config.get('name', 'Unknown')}")
    print(f"Objective: {challenge_config.get('objective', 'Learn')}")
    print()
    
    # Phase 1: OBSERVE - Try to create the document
    print("📊 PHASE 1: OBSERVE")
    print("-" * 60)
    
    try:
        # Attempt to create document based on challenge
        result = _attempt_challenge(challenge_config, gym)
        gym.observe(
            action="initial_attempt",
            result=result,
            notes="First attempt to meet challenge requirements",
            success=result.get("success", False),
            pages=result.get("pages", 0)
        )
    except Exception as e:
        gym.observe(
            action="initial_attempt",
            result={"error": str(e)},
            notes="Initial attempt failed",
            success=False
        )
        result = {"error": str(e)}
    
    # Phase 2: QUESTION - What patterns do we see?
    print()
    print("❓ PHASE 2: QUESTION")
    print("-" * 60)
    
    # Analyze observations
    observations = session.observations
    if observations:
        last_obs = observations[-1]
        print(f"Last observation: {last_obs.action}")
        print(f"Result: {last_obs.result}")
    
    # Phase 3: HYPOTHESIZE - Form initial hypothesis
    print()
    print("💡 PHASE 3: HYPOTHESIZE")
    print("-" * 60)
    
    # Form hypothesis based on what we observed
    if observations:
        hypothesis = _form_initial_hypothesis(observations, challenge_config, gym)
        print(f"Hypothesis: {hypothesis.statement}")
        print(f"Reasoning: {hypothesis.reasoning}")
    
    # Phase 4: TEST - Test the hypothesis
    print()
    print("🧪 PHASE 4: TEST")
    print("-" * 60)
    
    if session.hypotheses:
        hypothesis = session.hypotheses[-1]
        test_result = _test_hypothesis(hypothesis, challenge_config, gym)
        gym.test_hypothesis(hypothesis, test_result)
        print(f"Test result: {test_result}")
    
    # Phase 5: ANALYZE - What did we learn?
    print()
    print("📈 PHASE 5: ANALYZE")
    print("-" * 60)
    
    findings = _analyze_results(session, gym)
    for finding in findings:
        gym.record_finding(finding)
        print(f"Finding: {finding}")
    
    # Phase 6: CONCLUDE - What's true?
    print()
    print("✅ PHASE 6: CONCLUDE")
    print("-" * 60)
    
    conclusions = _form_conclusions(session, gym)
    for conclusion in conclusions:
        gym.conclude(conclusion)
        print(f"Conclusion: {conclusion}")
    
    # End session and save
    print()
    print("💾 Saving session...")
    report_path = gym.end_session()
    
    print()
    print("=" * 60)
    print("🎓 Study Session Complete!")
    print("=" * 60)
    print(f"📄 Report saved: {report_path}")
    print()
    
    return session


def _attempt_challenge(challenge_config: Dict[str, Any], gym: StudyGym) -> Dict[str, Any]:
    """Attempt to meet the challenge requirements."""
    constraints = challenge_config.get("constraints", {})
    content = challenge_config.get("content_template", "<p>Test content</p>")
    
    # Fill in content template if it has variables
    if "{" in content and "}" in content:
        # Simple variable replacement
        content = content.format(**challenge_config.get("variables_used", {}))
    
    # Create document
    output_path = gym.output_dir / f"challenge_attempt_{datetime.now().strftime('%H%M%S')}.pdf"
    
    builder_kwargs = {
        "title": challenge_config.get("name", "Challenge Document"),
        "content": content,
        "output_path": output_path,
        "printer_friendly": constraints.get("printer_friendly", False)
    }
    
    # Add page constraints if specified
    if "exact_pages" in constraints:
        builder_kwargs["exact_pages"] = int(constraints["exact_pages"])
    if "max_pages" in constraints:
        builder_kwargs["max_pages"] = int(constraints["max_pages"])
    if "min_pages" in constraints:
        builder_kwargs["min_pages"] = int(constraints["min_pages"])
    
    try:
        doc = DocumentBuilder.field_guide(**builder_kwargs)
        final_path = doc.save()
        
        # Check page count
        from pypdf import PdfReader
        reader = PdfReader(str(final_path))
        page_count = len(reader.pages)
        
        return {
            "success": True,
            "path": str(final_path),
            "pages": page_count,
            "constraints_met": _check_constraints(page_count, constraints)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "constraints_met": False
        }


def _check_constraints(page_count: int, constraints: Dict[str, Any]) -> bool:
    """Check if page count meets constraints."""
    if "exact_pages" in constraints:
        return page_count == int(constraints["exact_pages"])
    if "max_pages" in constraints:
        return page_count <= int(constraints["max_pages"])
    if "min_pages" in constraints:
        return page_count >= int(constraints["min_pages"])
    return True


def _form_initial_hypothesis(
    observations: List[Observation],
    challenge_config: Dict[str, Any],
    gym: StudyGym
) -> Hypothesis:
    """Form an initial hypothesis based on observations."""
    if not observations:
        return gym.form_hypothesis(
            statement="I need to observe first before forming a hypothesis",
            reasoning="No observations yet",
            assumptions=["I need data to form hypotheses"],
            test_plan="Make an observation first",
            confidence=1.0
        )
    
    last_obs = observations[-1]
    result = last_obs.result
    
    # Analyze what happened
    if isinstance(result, dict):
        if result.get("success"):
            pages = result.get("pages", 0)
            constraints_met = result.get("constraints_met", False)
            
            if not constraints_met:
                statement = f"Adjusting CSS (font size, margins, spacing) will help meet page constraints"
                reasoning = f"Document has {pages} pages but constraints not met. CSS adjustments can control page count."
                assumptions = [
                    "CSS affects page count",
                    "Font size reduction reduces pages",
                    "Margin reduction increases content per page"
                ]
                test_plan = "Try reducing font size and margins, then regenerate"
            else:
                statement = f"Current approach successfully creates {pages}-page documents"
                reasoning = f"Successfully created document meeting constraints"
                assumptions = ["Current method works"]
                test_plan = "Try with different content to verify"
        else:
            statement = "There was an error that needs investigation"
            reasoning = f"Error occurred: {result.get('error', 'Unknown')}"
            assumptions = ["Error is fixable"]
            test_plan = "Investigate error and retry"
    else:
        statement = "Need to analyze the result more carefully"
        reasoning = "Result format unexpected"
        assumptions = ["Result can be analyzed"]
        test_plan = "Examine result structure"
    
    return gym.form_hypothesis(
        statement=statement,
        reasoning=reasoning,
        assumptions=assumptions,
        test_plan=test_plan,
        confidence=0.6
    )


def _test_hypothesis(
    hypothesis: Hypothesis,
    challenge_config: Dict[str, Any],
    gym: StudyGym
) -> Dict[str, Any]:
    """Test a hypothesis by attempting the challenge again with adjustments."""
    # Try to implement the test plan
    test_result = {
        "tested": True,
        "confirmed": False,
        "refuted": False,
        "notes": ""
    }
    
    # Re-attempt with hypothesis in mind
    try:
        result = _attempt_challenge(challenge_config, gym)
        
        if result.get("success") and result.get("constraints_met"):
            test_result["confirmed"] = True
            test_result["notes"] = "Hypothesis confirmed - approach works"
        elif result.get("success"):
            test_result["notes"] = "Partial success - needs refinement"
        else:
            test_result["refuted"] = True
            test_result["notes"] = f"Hypothesis refuted - error: {result.get('error')}"
    except Exception as e:
        test_result["refuted"] = True
        test_result["notes"] = f"Test failed: {e}"
    
    return test_result


def _analyze_results(session: StudySession, gym: StudyGym) -> List[str]:
    """Analyze results and form findings."""
    findings = []
    
    # Analyze observations
    successful_attempts = [
        obs for obs in session.observations
        if isinstance(obs.result, dict) and obs.result.get("success")
    ]
    
    if successful_attempts:
        findings.append(f"Successfully created {len(successful_attempts)} document(s)")
        
        # Analyze page counts
        page_counts = [
            obs.result.get("pages", 0)
            for obs in successful_attempts
            if "pages" in obs.result
        ]
        if page_counts:
            findings.append(f"Page counts observed: {page_counts}")
    
    # Analyze hypotheses
    confirmed = [h for h in session.hypotheses if h.status == "confirmed"]
    refuted = [h for h in session.hypotheses if h.status == "refuted"]
    
    if confirmed:
        findings.append(f"{len(confirmed)} hypothesis(es) confirmed")
    if refuted:
        findings.append(f"{len(refuted)} hypothesis(es) refuted")
    
    return findings


def _form_conclusions(session: StudySession, gym: StudyGym) -> List[str]:
    """Form conclusions based on all evidence."""
    conclusions = []
    
    # Look at confirmed hypotheses
    confirmed = [h for h in session.hypotheses if h.status == "confirmed"]
    
    for hyp in confirmed:
        if hyp.confidence >= 0.7:
            conclusions.append(f"Beyond reasonable doubt: {hyp.statement}")
    
    # Look at successful attempts
    successful = [
        obs for obs in session.observations
        if isinstance(obs.result, dict) and obs.result.get("success") and obs.result.get("constraints_met")
    ]
    
    if successful:
        conclusions.append(f"Successfully met challenge requirements {len(successful)} time(s)")
    
    if not conclusions:
        conclusions.append("More study needed to form definitive conclusions")
    
    return conclusions
