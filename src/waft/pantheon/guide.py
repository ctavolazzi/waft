"""
The Guide: Pantheon Entity of Meta-Cognitive Guidance and Reasoning Evaluation

The Guide is the God of Meta-Cognitive Guidance - a timeless Entity that maintains
the fundamental principle of guided reasoning through iterative evaluation and
improvement. As a Force that Binds Reality Together, The Guide holds the Aspect
of Creation related to meta-cognitive oversight, reasoning quality assessment,
and the FVCU+Faithfulness taxonomy of evaluation.

Following "as above, so below" principles:
- As above: Pantheon god maintaining the celestial loop of guidance and evaluation
- So below: File-based system tracking guidance sessions, protocols, and reasoning chains

The Guide orchestrates a meta-cognitive loop between:
- Client LLM: Receives problem statements and produces reasoning
- Guide LLM: Provides instructions, evaluates reasoning quality using FVCU criteria
- Loop: Continues until quality threshold or max iterations reached
- Protocol: Contains reasoning chain + evaluation notes for "Why?" explanations

Storage:
- Sessions: _pantheon/guide/sessions/*.json
- Protocols: _pantheon/guide/protocols/*.json
- Session Index: _pantheon/guide/index.json
"""

from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
from pydantic import BaseModel, Field
import json


# ============================================================================
# Protocol Models (Pydantic)
# ============================================================================

class EvaluationScores(BaseModel):
    """
    Multi-criteria evaluation scores based on FVCU taxonomy + Faithfulness.

    Attributes:
        factuality: 0.0-1.0 - Grounded in query/external facts?
        validity: 0.0-1.0 - Logically/arithmetically correct?
        coherence: 0.0-1.0 - Preconditions satisfied by previous steps? (includes planning detection)
        utility: 0.0-1.0 - Contributes to correct final answer?
        faithfulness: 0.0-1.0 - Does claimed reasoning match actual computation?
        overall: Weighted average or composite score
    """
    factuality: float = Field(ge=0.0, le=1.0, description="Grounded in query/external facts")
    validity: float = Field(ge=0.0, le=1.0, description="Logically/arithmetically correct")
    coherence: float = Field(ge=0.0, le=1.0, description="Preconditions satisfied, no forward-looking planning")
    utility: float = Field(ge=0.0, le=1.0, description="Contributes to correct final answer")
    faithfulness: float = Field(ge=0.0, le=1.0, description="Claimed reasoning matches actual computation")
    overall: float = Field(ge=0.0, le=1.0, description="Composite quality score")


class Protocol(BaseModel):
    """
    Protocol: Complete record of a guidance session.

    Contains the full reasoning chain, evaluations, and metadata needed
    to answer "Why?" questions about the reasoning process.
    """
    session_id: str = Field(description="Unique session identifier")
    problem_statement: str = Field(description="Original problem to solve")
    reasoning_chain: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Step-by-step reasoning with instructions and traces"
    )
    evaluations: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Guide's evaluation notes with FVCU scores"
    )
    final_answer: str = Field(default="", description="Final answer produced")
    quality_score: float = Field(default=0.0, description="Overall quality (composite of FVCU)")
    iteration_count: int = Field(default=0, description="Number of iterations completed")
    evaluation_method: str = Field(
        default="critic_model",
        description="Evaluation approach used (critic_model, sequence_classifier, etc.)"
    )
    created: str = Field(default_factory=lambda: datetime.now().isoformat())
    completed: Optional[str] = Field(default=None, description="When session completed")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


# ============================================================================
# The Guide: Main Pantheon Entity
# ============================================================================

class TheGuide:
    """
    The Guide: Pantheon Entity (Timeless Force that Binds Reality Together)

    Entity of Meta-Cognitive Guidance - a timeless Entity that maintains the
    principle of guided reasoning through iterative evaluation and improvement.
    The Guide holds the Aspect of Creation related to meta-cognitive oversight,
    which should not change until evidence collected by Beings proves that
    change is needed.

    The Guide orchestrates a meta-cognitive loop between Client LLM and Guide LLM:
    1. Guide provides instruction/guidance
    2. Client produces reasoning trace
    3. Guide evaluates using FVCU+Faithfulness criteria
    4. Loop continues until quality threshold or max iterations
    5. Protocol generated for "Why?" explanations

    Provides:
    - Meta-cognitive guidance loop
    - FVCU+Faithfulness evaluation (Factuality, Validity, Coherence, Utility, Faithfulness)
    - Self-rewarding (Guide evaluates its own instructions)
    - Self-correction (Guide revises instructions if quality is low)
    - Partial context identification (premise finding)
    - Test-time scaling (majority voting)
    - Integration with TheReasoner for trace storage
    - Protocol generation for "Why?" explanations

    Storage:
    - Sessions: _pantheon/guide/sessions/
    - Protocols: _pantheon/guide/protocols/
    - Index: _pantheon/guide/index.json
    """

    def __init__(
        self,
        project_path: Optional[Path] = None,
        client_llm: Optional[Any] = None,
        guide_llm_config: Optional[Dict[str, Any]] = None,
        evaluation_config: Optional[Dict[str, Any]] = None,
        enable_self_rewarding: bool = False,
        enable_self_correction: bool = False
    ):
        """
        Initialize The Guide.

        Args:
            project_path: Path to project root (default: current directory)
            client_llm: OpenHands LLM instance for client reasoning
            guide_llm_config: Configuration for Guide LLM (model, api_key, etc.)
            evaluation_config: Configuration for evaluation system
            enable_self_rewarding: Enable Guide to evaluate its own instructions
            enable_self_correction: Enable Guide to revise instructions if quality is low
        """
        # Project path setup
        if project_path is None:
            project_path = Path.cwd()
        else:
            project_path = Path(project_path)

        self.project_path = project_path
        self.pantheon_path = project_path / "_pantheon"
        self.guide_path = self.pantheon_path / "guide"

        # Ensure directory structure exists
        self.guide_path.mkdir(parents=True, exist_ok=True)
        (self.guide_path / "sessions").mkdir(parents=True, exist_ok=True)
        (self.guide_path / "protocols").mkdir(parents=True, exist_ok=True)

        # Index file
        self.index_file = self.guide_path / "index.json"
        self.index = self._load_index()

        # LLM configuration
        self.client_llm = client_llm
        self.guide_llm_config = guide_llm_config or {}
        self.guide_llm = None  # Will be created when needed

        # Evaluation configuration
        self.evaluation_config = evaluation_config or {}

        # Feature flags
        self.enable_self_rewarding = enable_self_rewarding
        self.enable_self_correction = enable_self_correction

        # TheReasoner integration (lazy initialization)
        self._reasoner = None

    def _load_index(self) -> Dict[str, Any]:
        """Load session index."""
        if self.index_file.exists():
            try:
                return json.loads(self.index_file.read_text())
            except Exception:
                return {"sessions": [], "last_updated": None}
        return {"sessions": [], "last_updated": None}

    def _save_index(self) -> None:
        """Save session index."""
        self.index["last_updated"] = datetime.now().isoformat()
        self.index_file.write_text(json.dumps(self.index, indent=2))

    @property
    def reasoner(self):
        """Lazy initialization of TheReasoner."""
        if self._reasoner is None:
            try:
                from .reasoner import TheReasoner
            except ImportError:
                # Fallback to absolute import if relative import fails
                import sys
                import importlib.util
                reasoner_path = self.pantheon_path.parent / "pantheon" / "reasoner.py"
                if reasoner_path.exists():
                    spec = importlib.util.spec_from_file_location("reasoner", reasoner_path)
                    reasoner_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(reasoner_module)
                    TheReasoner = reasoner_module.TheReasoner
                else:
                    # TheReasoner not available, create a mock
                    class TheReasoner:
                        def __init__(self, project_path):
                            self.project_path = project_path
                        def create_trace(self, decision, reasoning, context=None, parent_trace_id=None):
                            return f"mock_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        def get_recent_traces(self, limit=10):
                            return []
            self._reasoner = TheReasoner(project_path=self.project_path)
        return self._reasoner

    def _create_guide_llm(self):
        """
        Create Guide LLM from configuration.

        Returns:
            OpenHands LLM instance for Guide (or compatible mock)
        """
        # Check if we have a demo/mock model specified
        model = self.guide_llm_config.get("model", "anthropic/claude-sonnet-4-5-20250929")

        # If model is "demo" or "mock", just return a copy of client_llm
        if "demo" in model.lower() or "mock" in model.lower():
            return self.client_llm

        try:
            from openhands.sdk import LLM
        except ImportError:
            raise ImportError(
                "OpenHands SDK not installed. Install with: pip install openhands-sdk"
            )

        # Create Guide LLM from config
        api_key = self.guide_llm_config.get("api_key")
        base_url = self.guide_llm_config.get("base_url")

        return LLM(
            model=model,
            api_key=api_key,
            base_url=base_url
        )

    def _guidance_loop(
        self,
        problem_statement: str,
        max_iterations: int = 10,
        quality_threshold: float = 0.8,
        use_partial_context: bool = True,
        test_time_scaling: int = 1
    ) -> Tuple[str, Protocol]:
        """
        Core guidance loop: Guide instructs, Client reasons, Guide evaluates, repeat.

        Args:
            problem_statement: Problem to solve
            max_iterations: Maximum number of iterations
            quality_threshold: Quality score threshold for termination
            use_partial_context: Use partial context for efficiency
            test_time_scaling: Number of samples for majority voting (1 = no scaling)

        Returns:
            Tuple of (final_answer, protocol)
        """
        # Create session ID
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Initialize Guide LLM if needed
        if self.guide_llm is None:
            self.guide_llm = self._create_guide_llm()

        # Initialize storage for reasoning chain and evaluations
        reasoning_chain = []
        evaluations = []
        previous_trace_id = None

        # Main guidance loop
        for iteration in range(1, max_iterations + 1):
            # Step 1: Guide generates instruction
            instruction = self._generate_instruction(
                problem_statement=problem_statement,
                iteration=iteration,
                previous_steps=reasoning_chain,
                previous_evaluations=evaluations
            )

            # Optional: Self-rewarding (Guide evaluates its own instruction)
            if self.enable_self_rewarding:
                self_eval = self._evaluate_guide_instruction(
                    instruction=instruction,
                    previous_iterations=reasoning_chain,
                    guide_llm=self.guide_llm
                )

                # Optional: Self-correction (Guide revises instruction if quality is low)
                if self.enable_self_correction and self_eval.get("quality_score", 1.0) < 0.7:
                    instruction = self._self_correct_instruction(
                        instruction=instruction,
                        evaluation=self_eval,
                        guide_llm=self.guide_llm
                    )

            # Step 2: Client LLM produces reasoning trace
            reasoning_trace = self._generate_reasoning_trace(
                problem_statement=problem_statement,
                instruction=instruction,
                previous_steps=reasoning_chain
            )

            # Store reasoning step
            reasoning_step = {
                "iteration": iteration,
                "instruction": instruction,
                "reasoning_trace": reasoning_trace,
                "timestamp": datetime.now().isoformat()
            }
            reasoning_chain.append(reasoning_step)

            # Step 3: Guide evaluates reasoning using FVCU+Faithfulness
            if test_time_scaling > 1:
                evaluation = self._evaluate_with_majority_voting(
                    reasoning_trace=reasoning_trace,
                    previous_steps=reasoning_chain[:-1],  # Exclude current step
                    guide_llm=self.guide_llm,
                    num_samples=test_time_scaling
                )
            else:
                evaluation = self._evaluate_with_fvcu(
                    reasoning_trace=reasoning_trace,
                    previous_steps=reasoning_chain[:-1],
                    guide_llm=self.guide_llm,
                    use_partial_context=use_partial_context
                )

            evaluations.append(evaluation)

            # Step 4: Create trace in TheReasoner
            trace_id = self.reasoner.create_trace(
                decision=f"Iteration {iteration}: {instruction[:100]}",
                reasoning=reasoning_trace,
                context={
                    "iteration": iteration,
                    "quality_score": evaluation["scores"]["overall"],
                    "session_id": session_id
                },
                parent_trace_id=previous_trace_id
            )
            previous_trace_id = trace_id

            # Step 5: Check termination
            scores = EvaluationScores(**evaluation["scores"])
            should_terminate, termination_reason = self._check_termination(
                iteration=iteration,
                evaluation_scores=scores,
                max_iterations=max_iterations,
                quality_threshold=quality_threshold,
                guide_assessment=evaluation
            )

            if should_terminate:
                break

        # Generate final answer from Client LLM
        final_answer = self._generate_final_answer(
            problem_statement=problem_statement,
            reasoning_chain=reasoning_chain
        )

        # Calculate overall quality score
        if evaluations:
            quality_score = sum(e["scores"]["overall"] for e in evaluations) / len(evaluations)
        else:
            quality_score = 0.0

        # Generate Protocol
        protocol = self._generate_protocol(
            session_id=session_id,
            problem_statement=problem_statement,
            reasoning_chain=reasoning_chain,
            evaluations=evaluations,
            final_answer=final_answer,
            quality_score=quality_score,
            iteration_count=len(reasoning_chain)
        )

        return final_answer, protocol

    def _generate_instruction(
        self,
        problem_statement: str,
        iteration: int,
        previous_steps: List[Dict[str, Any]],
        previous_evaluations: List[Dict[str, Any]]
    ) -> str:
        """Generate meta-cognitive instruction from Guide LLM."""
        if iteration == 1:
            # First iteration: introduce the problem
            prompt = f"""You are a meta-cognitive guide. Your role is to provide clear, actionable instructions to help solve this problem step-by-step.

Problem: {problem_statement}

Provide the first instruction to begin solving this problem. Focus on breaking down the problem and identifying what needs to be done first."""
        else:
            # Subsequent iterations: build on previous work
            context = self._format_previous_steps(previous_steps, previous_evaluations)
            prompt = f"""You are a meta-cognitive guide helping solve this problem:

Problem: {problem_statement}

Previous steps and evaluations:
{context}

Based on the previous work and evaluations, provide the next instruction to continue solving this problem. Address any weaknesses identified in the evaluations."""

        response = self.guide_llm.complete(prompt)
        return response.strip()

    def _generate_reasoning_trace(
        self,
        problem_statement: str,
        instruction: str,
        previous_steps: List[Dict[str, Any]]
    ) -> str:
        """Generate reasoning trace from Client LLM."""
        if not self.client_llm:
            raise ValueError("Client LLM not configured")

        context = ""
        if previous_steps:
            context = "\n\nPrevious reasoning:\n" + "\n".join(
                f"Step {s['iteration']}: {s['reasoning_trace'][:200]}..."
                for s in previous_steps[-3:]  # Last 3 steps for context
            )

        prompt = f"""Problem: {problem_statement}

Instruction: {instruction}{context}

Follow the instruction and show your reasoning step-by-step with clear intermediate steps."""

        response = self.client_llm.complete(prompt)
        return response.strip()

    def _generate_final_answer(
        self,
        problem_statement: str,
        reasoning_chain: List[Dict[str, Any]]
    ) -> str:
        """Generate final answer from Client LLM based on reasoning chain."""
        if not self.client_llm:
            raise ValueError("Client LLM not configured")

        reasoning_summary = "\n\n".join(
            f"Step {s['iteration']}: {s['reasoning_trace']}"
            for s in reasoning_chain
        )

        prompt = f"""Problem: {problem_statement}

Reasoning chain:
{reasoning_summary}

Based on this reasoning, provide a clear, concise final answer to the problem."""

        response = self.client_llm.complete(prompt)
        return response.strip()

    def _format_previous_steps(
        self,
        previous_steps: List[Dict[str, Any]],
        previous_evaluations: List[Dict[str, Any]]
    ) -> str:
        """Format previous steps and evaluations for context."""
        formatted = []
        for step, eval_data in zip(previous_steps, previous_evaluations):
            formatted.append(f"""
Step {step['iteration']}:
  Instruction: {step['instruction']}
  Reasoning: {step['reasoning_trace'][:200]}...
  Scores: Factuality={eval_data['scores']['factuality']:.2f}, Validity={eval_data['scores']['validity']:.2f}, Coherence={eval_data['scores']['coherence']:.2f}, Utility={eval_data['scores']['utility']:.2f}, Faithfulness={eval_data['scores']['faithfulness']:.2f}
  Strengths: {', '.join(eval_data.get('strengths', [])[:2])}
  Weaknesses: {', '.join(eval_data.get('weaknesses', [])[:2])}
""")
        return "\n".join(formatted)

    def _evaluate_with_fvcu(
        self,
        reasoning_trace: str,
        previous_steps: List[Dict[str, Any]],
        guide_llm: Any,
        use_partial_context: bool = True
    ) -> Dict[str, Any]:
        """
        Evaluate reasoning trace using FVCU+Faithfulness criteria.

        Uses critic model approach (LLM-as-a-judge) to evaluate:
        - Factuality: Grounded in query/external facts?
        - Validity: Logically/arithmetically correct?
        - Coherence: Preconditions satisfied? (detects forward-looking planning)
        - Utility: Contributes to correct final answer?
        - Faithfulness: Does claimed reasoning match actual computation?

        Args:
            reasoning_trace: Client's reasoning to evaluate
            previous_steps: Previous reasoning steps (for context)
            guide_llm: Guide LLM instance
            use_partial_context: Whether to identify premises for partial context

        Returns:
            Evaluation dictionary with FVCU scores and rationale
        """
        # Build context from previous steps
        context = ""
        if previous_steps:
            context = "Previous reasoning:\n" + "\n".join(
                f"Step {s['iteration']}: {s['reasoning_trace']}"
                for s in previous_steps[-3:]  # Last 3 steps
            )

        # FVCU+Faithfulness evaluation prompt (critic model)
        evaluation_prompt = f"""You are a meta-cognitive evaluator using the FVCU+Faithfulness taxonomy to assess reasoning quality.

{context}

Current reasoning to evaluate:
{reasoning_trace}

Evaluate this reasoning step-by-step across 5 dimensions (score each 0.0-1.0):

1. **Factuality** (0.0-1.0): Is the reasoning grounded in the query or external facts?
2. **Validity** (0.0-1.0): Is the reasoning logically and arithmetically correct?
3. **Coherence** (0.0-1.0): Are all preconditions satisfied by previous steps? Does it show forward-looking planning (bad) or build only on established facts (good)?
4. **Utility** (0.0-1.0): Does this contribute to the correct final answer?
5. **Faithfulness** (0.0-1.0): Does the claimed reasoning match actual computation? Is there any unfaithful reasoning where claimed steps don't actually occur?

Provide your evaluation in this exact JSON format:
{{
  "factuality": <score>,
  "validity": <score>,
  "coherence": <score>,
  "utility": <score>,
  "faithfulness": <score>,
  "overall": <average_score>,
  "rationale": "<explanation>",
  "strengths": ["<strength1>", "<strength2>"],
  "weaknesses": ["<weakness1>", "<weakness2>"],
  "recommendations": ["<recommendation1>", "<recommendation2>"],
  "should_continue": <true/false>,
  "planning_detected": <true/false>,
  "unfaithful_reasoning_detected": <true/false>
}}"""

        response = guide_llm.complete(evaluation_prompt)

        # Parse JSON response
        try:
            # Extract JSON from response (handle markdown code blocks)
            response_text = response.strip()
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            evaluation = json.loads(response_text)

            # Ensure all scores are present
            required_scores = ["factuality", "validity", "coherence", "utility", "faithfulness"]
            for score_name in required_scores:
                if score_name not in evaluation:
                    evaluation[score_name] = 0.5  # Default to neutral

            # Calculate overall if missing
            if "overall" not in evaluation:
                evaluation["overall"] = sum(
                    evaluation.get(s, 0.5) for s in required_scores
                ) / len(required_scores)

            # Wrap scores in proper structure
            return {
                "iteration": len(previous_steps) + 1,
                "scores": {
                    "factuality": evaluation["factuality"],
                    "validity": evaluation["validity"],
                    "coherence": evaluation["coherence"],
                    "utility": evaluation["utility"],
                    "faithfulness": evaluation["faithfulness"],
                    "overall": evaluation["overall"]
                },
                "rationale": evaluation.get("rationale", ""),
                "strengths": evaluation.get("strengths", []),
                "weaknesses": evaluation.get("weaknesses", []),
                "recommendations": evaluation.get("recommendations", []),
                "should_continue": evaluation.get("should_continue", True),
                "planning_detected": evaluation.get("planning_detected", False),
                "unfaithful_reasoning_detected": evaluation.get("unfaithful_reasoning_detected", False)
            }

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            # Fallback to neutral scores if parsing fails
            return {
                "iteration": len(previous_steps) + 1,
                "scores": {
                    "factuality": 0.5,
                    "validity": 0.5,
                    "coherence": 0.5,
                    "utility": 0.5,
                    "faithfulness": 0.5,
                    "overall": 0.5
                },
                "rationale": f"Evaluation parsing failed: {str(e)}",
                "strengths": [],
                "weaknesses": ["Evaluation could not be parsed"],
                "recommendations": ["Retry evaluation"],
                "should_continue": True,
                "planning_detected": False,
                "unfaithful_reasoning_detected": False
            }

    def _identify_premises(
        self,
        step: Dict[str, Any],
        previous_steps: List[Dict[str, Any]],
        guide_llm: Any
    ) -> List[int]:
        """
        Identify which previous steps are premises for the current step.

        This enables partial context evaluation - only considering relevant
        previous steps instead of the full history.

        Args:
            step: Current reasoning step
            previous_steps: All previous steps
            guide_llm: Guide LLM instance

        Returns:
            List of indices indicating which previous steps are premises
        """
        # TODO: Implement in Quest 8 (Partial Context Identification)
        pass

    def _evaluate_with_majority_voting(
        self,
        reasoning_trace: str,
        previous_steps: List[Dict[str, Any]],
        guide_llm: Any,
        num_samples: int = 3
    ) -> Dict[str, Any]:
        """
        Test-time scaling: Evaluate using majority voting across multiple samples.

        Args:
            reasoning_trace: Client's reasoning to evaluate
            previous_steps: Previous reasoning steps
            guide_llm: Guide LLM instance
            num_samples: Number of evaluation samples to generate

        Returns:
            Aggregated evaluation via majority voting
        """
        # TODO: Implement in Quest 9 (Test-Time Scaling)
        pass

    def _evaluate_guide_instruction(
        self,
        instruction: str,
        previous_iterations: List[Dict[str, Any]],
        guide_llm: Any
    ) -> Dict[str, Any]:
        """
        Self-rewarding: Guide evaluates its own instruction quality.

        Args:
            instruction: Instruction Guide is about to send to Client
            previous_iterations: Previous guidance iterations
            guide_llm: Guide LLM instance

        Returns:
            Self-evaluation with quality score and recommendations
        """
        # TODO: Implement in Quest 10 (Self-Rewarding)
        pass

    def _self_correct_instruction(
        self,
        instruction: str,
        evaluation: Dict[str, Any],
        guide_llm: Any
    ) -> str:
        """
        Self-correction: Guide revises instruction if quality is low.

        Args:
            instruction: Original instruction
            evaluation: Self-evaluation results
            guide_llm: Guide LLM instance

        Returns:
            Revised instruction
        """
        # TODO: Implement in Quest 11 (Self-Correction)
        pass

    def _check_termination(
        self,
        iteration: int,
        evaluation_scores: EvaluationScores,
        max_iterations: int,
        quality_threshold: float,
        guide_assessment: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, str]:
        """
        Check if guidance loop should terminate.

        Termination conditions:
        - Quality score >= threshold
        - Iteration count >= max_iterations
        - Guide explicitly says "sufficient"
        - User interrupt (if async)

        Args:
            iteration: Current iteration number
            evaluation_scores: FVCU evaluation scores
            max_iterations: Maximum allowed iterations
            quality_threshold: Quality score threshold
            guide_assessment: Optional Guide's self-assessment

        Returns:
            Tuple of (should_terminate, reason)
        """
        # Check max iterations
        if iteration >= max_iterations:
            return True, f"Maximum iterations ({max_iterations}) reached"

        # Check quality threshold (overall score)
        if evaluation_scores.overall >= quality_threshold:
            return True, f"Quality threshold ({quality_threshold}) achieved: {evaluation_scores.overall:.2f}"

        # Check validity + utility complementarity (both should be high for termination)
        if evaluation_scores.validity >= quality_threshold and evaluation_scores.utility >= quality_threshold:
            return True, f"Validity ({evaluation_scores.validity:.2f}) and Utility ({evaluation_scores.utility:.2f}) thresholds achieved"

        # Check if Guide assessment says not to continue
        if guide_assessment and not guide_assessment.get("should_continue", True):
            return True, "Guide assessment indicates sufficient progress"

        # Otherwise, continue
        return False, "Continuing guidance loop"

    def _generate_protocol(
        self,
        session_id: str,
        problem_statement: str,
        reasoning_chain: List[Dict[str, Any]],
        evaluations: List[Dict[str, Any]],
        final_answer: str,
        quality_score: float,
        iteration_count: int,
        evaluation_method: str = "critic_model"
    ) -> Protocol:
        """
        Generate Protocol from guidance session.

        Args:
            session_id: Unique session identifier
            problem_statement: Original problem
            reasoning_chain: Step-by-step reasoning
            evaluations: Evaluation notes with FVCU scores
            final_answer: Final answer produced
            quality_score: Overall quality score
            iteration_count: Number of iterations
            evaluation_method: Evaluation approach used

        Returns:
            Protocol instance
        """
        return Protocol(
            session_id=session_id,
            problem_statement=problem_statement,
            reasoning_chain=reasoning_chain,
            evaluations=evaluations,
            final_answer=final_answer,
            quality_score=quality_score,
            iteration_count=iteration_count,
            evaluation_method=evaluation_method,
            completed=datetime.now().isoformat()
        )

    def _save_session(self, protocol: Protocol) -> None:
        """
        Save session to storage.

        Args:
            protocol: Protocol to save
        """
        # Save full session
        session_file = self.guide_path / "sessions" / f"{protocol.session_id}.json"
        session_file.write_text(protocol.model_dump_json(indent=2))

        # Save protocol (for quick "Why?" lookups)
        protocol_file = self.guide_path / "protocols" / f"{protocol.session_id}.json"
        protocol_file.write_text(protocol.model_dump_json(indent=2))

        # Update index
        self.index["sessions"].append({
            "session_id": protocol.session_id,
            "problem_summary": protocol.problem_statement[:100],
            "created": protocol.created,
            "completed": protocol.completed,
            "iterations": protocol.iteration_count,
            "quality_score": protocol.quality_score
        })
        self._save_index()

    def solve(
        self,
        problem_statement: str,
        max_iterations: int = 10,
        quality_threshold: float = 0.8,
        use_partial_context: bool = True,
        test_time_scaling: int = 1
    ) -> Tuple[str, Protocol]:
        """
        Solve a problem using meta-cognitive guidance loop.

        Main entry point for The Guide. Orchestrates:
        1. Guide provides instructions
        2. Client reasons
        3. Guide evaluates with FVCU+Faithfulness
        4. Loop until quality threshold or max iterations
        5. Generate Protocol for "Why?" explanations

        Args:
            problem_statement: Problem to solve
            max_iterations: Maximum number of iterations (default: 10)
            quality_threshold: Quality score threshold for termination (default: 0.8)
            use_partial_context: Use partial context for efficiency (default: True)
            test_time_scaling: Number of samples for majority voting (default: 1, no scaling)

        Returns:
            Tuple of (final_answer, protocol)

        Example:
            >>> guide = TheGuide(
            ...     project_path=Path.cwd(),
            ...     client_llm=client_llm,
            ...     guide_llm_config={"model": "...", "api_key": "..."}
            ... )
            >>> answer, protocol = guide.solve(
            ...     problem_statement="How do I implement OAuth2?",
            ...     max_iterations=10,
            ...     quality_threshold=0.8
            ... )
        """
        # Create session ID
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Run guidance loop
        final_answer, protocol = self._guidance_loop(
            problem_statement=problem_statement,
            max_iterations=max_iterations,
            quality_threshold=quality_threshold,
            use_partial_context=use_partial_context,
            test_time_scaling=test_time_scaling
        )

        # Save session
        self._save_session(protocol)

        return final_answer, protocol

    def explain(self, session_id: str) -> str:
        """
        Generate "Why?" explanation from Protocol.

        Loads the Protocol and formats the reasoning chain as a narrative,
        including evaluation notes and FVCU scores.

        Args:
            session_id: Session identifier to explain

        Returns:
            Formatted explanation string

        Example:
            >>> explanation = guide.explain(protocol.session_id)
            >>> print(explanation)
        """
        # Load Protocol
        protocol = self.get_protocol(session_id)
        if not protocol:
            return f"Session {session_id} not found"

        # Build explanation narrative
        explanation = f"""
# Meta-Cognitive Guidance Explanation

## Problem Statement
{protocol.problem_statement}

## Reasoning Chain ({protocol.iteration_count} iterations)
"""

        # Add each reasoning step with evaluation
        for step, evaluation in zip(protocol.reasoning_chain, protocol.evaluations):
            iteration = step["iteration"]
            explanation += f"""
### Iteration {iteration}

**Instruction:**
{step["instruction"]}

**Reasoning:**
{step["reasoning_trace"]}

**Evaluation (FVCU+Faithfulness):**
- Factuality: {evaluation["scores"]["factuality"]:.2f} - Grounded in facts?
- Validity: {evaluation["scores"]["validity"]:.2f} - Logically correct?
- Coherence: {evaluation["scores"]["coherence"]:.2f} - Preconditions satisfied?
- Utility: {evaluation["scores"]["utility"]:.2f} - Contributes to answer?
- Faithfulness: {evaluation["scores"]["faithfulness"]:.2f} - Claimed reasoning matches computation?
- **Overall: {evaluation["scores"]["overall"]:.2f}**

**Rationale:** {evaluation["rationale"]}

**Strengths:** {", ".join(evaluation.get("strengths", []))}

**Weaknesses:** {", ".join(evaluation.get("weaknesses", []))}

**Recommendations:** {", ".join(evaluation.get("recommendations", []))}

"""

        # Add final answer and summary
        explanation += f"""
## Final Answer
{protocol.final_answer}

## Summary
- **Total Iterations:** {protocol.iteration_count}
- **Overall Quality Score:** {protocol.quality_score:.2f}
- **Evaluation Method:** {protocol.evaluation_method}
- **Completed:** {protocol.completed}

---
*Generated by TheGuide - Meta-Cognitive Guidance System*
"""

        return explanation.strip()

    def get_protocol(self, session_id: str) -> Optional[Protocol]:
        """
        Load a Protocol by session ID.

        Args:
            session_id: Session identifier

        Returns:
            Protocol instance or None if not found
        """
        protocol_file = self.guide_path / "protocols" / f"{session_id}.json"
        if protocol_file.exists():
            try:
                protocol_data = json.loads(protocol_file.read_text())
                return Protocol(**protocol_data)
            except Exception:
                return None
        return None

    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent guidance sessions.

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of session summaries
        """
        sessions = self.index.get("sessions", [])
        return sorted(
            sessions,
            key=lambda s: s.get("created", ""),
            reverse=True
        )[:limit]

    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get summary of all guidance sessions.

        Returns:
            Dictionary with session statistics
        """
        sessions_dir = self.guide_path / "sessions"
        protocols_dir = self.guide_path / "protocols"

        session_count = len(list(sessions_dir.glob("session_*.json"))) if sessions_dir.exists() else 0
        protocol_count = len(list(protocols_dir.glob("session_*.json"))) if protocols_dir.exists() else 0

        return {
            "total_sessions": session_count,
            "total_protocols": protocol_count,
            "indexed_sessions": len(self.index.get("sessions", [])),
            "last_updated": self.index.get("last_updated")
        }
