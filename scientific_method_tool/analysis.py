"""
Experiment Analysis System

Analyzes experiment results to verify or refute hypotheses.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from datetime import datetime
import statistics

from .experiment import Experiment
from .experiment_loop import ExperimentResult
from .hypothesis import Hypothesis


@dataclass
class AnalysisResult:
    """Result of analyzing experiments."""
    hypothesis: Hypothesis
    verified: Optional[bool]
    confidence: float
    evidence: Dict[str, Any]
    conclusions: List[str]
    recommendations: List[str]
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())


class ExperimentAnalyzer:
    """Analyzes experiment results."""
    
    def analyze_experiment(
        self,
        experiment: Experiment,
        results: Dict[str, Any]
    ) -> AnalysisResult:
        """
        Analyze a single experiment.
        
        Args:
            experiment: Experiment instance
            results: Experiment results
        
        Returns:
            Analysis result
        """
        # Compare initial and final states
        state_analysis = {}
        if experiment.initial_state and experiment.final_state:
            state_analysis = self._analyze_state_changes(
                experiment.initial_state,
                experiment.final_state
            )
        
        # Analyze collected data
        data_analysis = {}
        if experiment.data_collector:
            data_analysis = self._analyze_data(experiment.data_collector)
        
        # Determine if hypothesis verified
        verified, confidence = self._verify_hypothesis(
            experiment.hypothesis,
            results,
            state_analysis,
            data_analysis
        )
        
        # Generate conclusions
        conclusions = self._generate_conclusions(
            experiment.hypothesis,
            verified,
            state_analysis,
            data_analysis
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            verified,
            confidence,
            state_analysis,
            data_analysis
        )
        
        return AnalysisResult(
            hypothesis=experiment.hypothesis,
            verified=verified,
            confidence=confidence,
            evidence={
                "state_analysis": state_analysis,
                "data_analysis": data_analysis,
                "results": results
            },
            conclusions=conclusions,
            recommendations=recommendations
        )
    
    def analyze_iteration_results(
        self,
        hypothesis: Hypothesis,
        results: List[ExperimentResult]
    ) -> AnalysisResult:
        """
        Analyze results from multiple iterations.
        
        Args:
            hypothesis: Original hypothesis
            results: List of experiment results
        
        Returns:
            Combined analysis result
        """
        # Aggregate results
        verified_count = sum(1 for r in results if r.hypothesis_verified is True)
        refuted_count = sum(1 for r in results if r.hypothesis_verified is False)
        total_count = len(results)
        
        # Calculate overall confidence
        confidences = [r.confidence for r in results if r.confidence > 0]
        avg_confidence = statistics.mean(confidences) if confidences else 0.0
        
        # Determine overall verification
        if total_count == 0:
            verified = None
            confidence = 0.0
        elif verified_count > refuted_count:
            verified = True
            confidence = avg_confidence * (verified_count / total_count)
        elif refuted_count > verified_count:
            verified = False
            confidence = avg_confidence * (refuted_count / total_count)
        else:
            verified = None
            confidence = avg_confidence * 0.5
        
        # Aggregate data
        aggregated_data = self._aggregate_data(results)
        
        # Generate conclusions
        conclusions = [
            f"Ran {total_count} experiments",
            f"Verified: {verified_count}, Refuted: {refuted_count}",
            f"Overall confidence: {confidence:.2f}"
        ]
        
        if verified is True:
            conclusions.append(f"Hypothesis VERIFIED with {confidence:.1%} confidence")
        elif verified is False:
            conclusions.append(f"Hypothesis REFUTED with {confidence:.1%} confidence")
        else:
            conclusions.append("Hypothesis INCONCLUSIVE - need more data")
        
        # Generate recommendations
        recommendations = []
        if verified is None:
            recommendations.append("Run more experiments with different variable values")
        elif verified is True and confidence < 0.8:
            recommendations.append("Increase confidence by running more experiments")
        elif verified is False:
            recommendations.append("Revise hypothesis based on refuting evidence")
        
        return AnalysisResult(
            hypothesis=hypothesis,
            verified=verified,
            confidence=confidence,
            evidence={
                "total_experiments": total_count,
                "verified_count": verified_count,
                "refuted_count": refuted_count,
                "aggregated_data": aggregated_data,
                "individual_results": [self._result_to_dict(r) for r in results]
            },
            conclusions=conclusions,
            recommendations=recommendations
        )
    
    def _analyze_state_changes(
        self,
        initial_state: Any,
        final_state: Any
    ) -> Dict[str, Any]:
        """Analyze changes between initial and final states."""
        # This would compare states and identify changes
        # Placeholder implementation
        return {
            "components_changed": [],
            "value_changes": {}
        }
    
    def _analyze_data(self, data_collector: Any) -> Dict[str, Any]:
        """Analyze collected data."""
        analysis = {}
        
        all_series = data_collector.get_all_series()
        for name, series in all_series.items():
            values = series.get_values()
            if values and isinstance(values[0], (int, float)):
                analysis[name] = {
                    "count": len(values),
                    "mean": statistics.mean(values),
                    "median": statistics.median(values),
                    "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
                    "min": min(values),
                    "max": max(values)
                }
        
        return analysis
    
    def _verify_hypothesis(
        self,
        hypothesis: Hypothesis,
        results: Dict[str, Any],
        state_analysis: Dict[str, Any],
        data_analysis: Dict[str, Any]
    ) -> tuple[Optional[bool], float]:
        """Verify or refute hypothesis."""
        # Simple verification logic
        # In a real implementation, this would analyze the prediction against results
        
        if "prediction_match" in results:
            verified = results["prediction_match"]
            confidence = results.get("confidence", 0.5)
            return verified, confidence
        
        # Default: inconclusive
        return None, 0.0
    
    def _generate_conclusions(
        self,
        hypothesis: Hypothesis,
        verified: Optional[bool],
        state_analysis: Dict[str, Any],
        data_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate conclusions from analysis."""
        conclusions = []
        
        if verified is True:
            conclusions.append(f"Hypothesis VERIFIED: {hypothesis.statement}")
        elif verified is False:
            conclusions.append(f"Hypothesis REFUTED: {hypothesis.statement}")
        else:
            conclusions.append(f"Hypothesis INCONCLUSIVE: {hypothesis.statement}")
        
        # Add data-based conclusions
        if data_analysis:
            conclusions.append(f"Collected data for {len(data_analysis)} metrics")
        
        return conclusions
    
    def _generate_recommendations(
        self,
        verified: Optional[bool],
        confidence: float,
        state_analysis: Dict[str, Any],
        data_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        if verified is None:
            recommendations.append("Run more experiments to gather sufficient data")
        elif confidence < 0.7:
            recommendations.append("Increase sample size or refine experimental design")
        
        return recommendations
    
    def _aggregate_data(self, results: List[ExperimentResult]) -> Dict[str, Any]:
        """Aggregate data across multiple experiments."""
        aggregated = {}
        
        for result in results:
            for metric, summary in result.data_summary.items():
                if metric not in aggregated:
                    aggregated[metric] = {
                        "values": [],
                        "count": 0
                    }
                
                if "mean" in summary:
                    aggregated[metric]["values"].append(summary["mean"])
                    aggregated[metric]["count"] += summary["count"]
        
        # Calculate aggregate statistics
        for metric, data in aggregated.items():
            if data["values"]:
                data["aggregate_mean"] = statistics.mean(data["values"])
                data["aggregate_stdev"] = statistics.stdev(data["values"]) if len(data["values"]) > 1 else 0.0
        
        return aggregated
    
    def _result_to_dict(self, result: ExperimentResult) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "experiment_id": result.experiment_id,
            "hypothesis_verified": result.hypothesis_verified,
            "confidence": result.confidence,
            "data_summary": result.data_summary
        }
