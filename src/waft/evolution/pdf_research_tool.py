"""
PDF Research Tool - Cross-PDF Analysis and Pattern Recognition

Enables research across multiple PDFs:
- Comparative analysis
- Trend identification
- Pattern recognition
- Knowledge accumulation
- Traceability and monitoring via TheObserver
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import hashlib
from collections import Counter, defaultdict

from ..core.science.observer import TheObserver
from ..core.agent.state import EvolutionaryEvent, EvolutionaryEventType


class PDFResearchTool:
    """
    Research tool for analyzing multiple PDFs.
    
    Features:
    - Cross-PDF comparison
    - Trend analysis
    - Pattern recognition
    - Knowledge accumulation
    """
    
    def __init__(self, research_db_path: Optional[Path] = None):
        """
        Initialize research tool.
        
        Args:
            research_db_path: Path to research database
        """
        self.research_db_path = research_db_path or Path("_work_efforts/pdf_research_db.json")
        self._load_db()
    
    def _load_db(self):
        """Load research database."""
        if self.research_db_path.exists():
            with open(self.research_db_path) as f:
                self.db = json.load(f)
        else:
            self.db = {
                "pdfs": [],
                "hypotheses": [],
                "findings": [],
                "knowledge": []
            }
    
    def compare_pdfs(
        self,
        pdf_paths: List[Path],
        metrics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Compare multiple PDFs.
        
        Args:
            pdf_paths: List of PDF paths to compare
            metrics: Optional list of metrics to compare
        
        Returns:
            Comparative analysis
        """
        comparison = {
            "compared_pdfs": len(pdf_paths),
            "metrics": {},
            "rankings": {},
            "insights": []
        }
        
        # Load PDF data from research database
        pdf_data = []
        for pdf_path in pdf_paths:
            pdf_info = next(
                (p for p in self.db.get("pdfs", []) if p.get("path") == str(pdf_path)),
                None
            )
            if pdf_info:
                pdf_data.append(pdf_info)
        
        if not pdf_data:
            return {"error": "No PDF data found in research database"}
        
        # Compare metrics
        if metrics is None:
            metrics = ["quality_score", "completeness", "structure"]
        
        for metric in metrics:
            values = [p.get(metric, 0) for p in pdf_data]
            comparison["metrics"][metric] = {
                "average": sum(values) / len(values) if values else 0,
                "min": min(values) if values else 0,
                "max": max(values) if values else 0,
                "std_dev": self._std_dev(values) if len(values) > 1 else 0
            }
        
        # Rankings
        quality_scores = [(p.get("quality_score", 0), p.get("title", "Unknown")) for p in pdf_data]
        quality_scores.sort(reverse=True)
        comparison["rankings"]["by_quality"] = quality_scores[:5]  # Top 5
        
        # Insights
        if len(pdf_data) >= 2:
            avg_quality = sum(p.get("quality_score", 0) for p in pdf_data) / len(pdf_data)
            best_quality = max(p.get("quality_score", 0) for p in pdf_data)
            
            comparison["insights"].append(
                f"Average quality: {avg_quality:.2f}, Best: {best_quality:.2f}"
            )
            
            # Identify common gaps
            all_gaps = []
            for p in pdf_data:
                all_gaps.extend(p.get("gaps", []))
            if all_gaps:
                gap_counts = Counter(all_gaps)
                common_gaps = gap_counts.most_common(3)
                comparison["insights"].append(
                    f"Common gaps: {', '.join([g[0] for g in common_gaps])}"
                )
        
        # Record comparison event to TheObserver
        self._record_event(
            event_type=EvolutionaryEventType.GYM_EVAL,
            operation="compare_pdfs",
            payload={
                "pdfs_compared": len(pdf_paths),
                "metrics_analyzed": metrics,
                "rankings_count": len(comparison.get("rankings", {})),
                "insights_count": len(comparison.get("insights", []))
            },
            fitness_metrics={
                "average_quality": comparison["metrics"].get("quality_score", {}).get("average", 0) if comparison["metrics"] else 0,
                "pdfs_compared": len(pdf_paths)
            }
        )
        
        return comparison
    
    def analyze_trends(
        self,
        time_period: str = "30 days",
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze trends over time.
        
        Args:
            time_period: Time period to analyze (e.g., "30 days", "7 days")
            category: Optional category filter
        
        Returns:
            Trend analysis
        """
        # Parse time period
        days = int(time_period.split()[0])
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter PDFs
        pdfs = [
            p for p in self.db.get("pdfs", [])
            if (not category or p.get("category") == category)
            and datetime.fromisoformat(p.get("timestamp", "2000-01-01")) >= cutoff_date
        ]
        
        if len(pdfs) < 2:
            return {"message": f"Need at least 2 PDFs in the last {days} days"}
        
        # Sort by timestamp
        pdfs.sort(key=lambda p: p.get("timestamp", ""))
        
        # Analyze quality trend
        qualities = [p.get("quality_score", 0) for p in pdfs]
        trend = "improving" if qualities[-1] > qualities[0] else "declining"
        
        # Calculate trend strength
        if len(qualities) >= 2:
            trend_strength = abs(qualities[-1] - qualities[0])
        else:
            trend_strength = 0
        
        analysis = {
            "time_period": time_period,
            "pdfs_analyzed": len(pdfs),
            "quality_trend": trend,
            "trend_strength": trend_strength,
            "average_quality": sum(qualities) / len(qualities),
            "quality_over_time": [
                {"date": p.get("timestamp", ""), "quality": p.get("quality_score", 0)}
                for p in pdfs
            ],
            "insights": []
        }
        
        # Generate insights
        if trend == "improving":
            analysis["insights"].append(f"Quality improving by {trend_strength:.2f} over {days} days")
        else:
            analysis["insights"].append(f"Quality declining by {abs(trend_strength):.2f} over {days} days")
        
        # Style trends
        styles = [p.get("style") for p in pdfs if p.get("style")]
        if styles:
            style_counts = Counter(styles)
            most_common_style = style_counts.most_common(1)[0][0]
            analysis["insights"].append(f"Most common style: {most_common_style}")
        
        return analysis
    
    def identify_patterns(
        self,
        category: Optional[str] = None,
        min_pdfs: int = 3
    ) -> Dict[str, Any]:
        """
        Identify patterns across PDFs.
        
        Args:
            category: Optional category filter
            min_pdfs: Minimum PDFs needed for pattern recognition
        
        Returns:
            Pattern analysis
        """
        pdfs = [
            p for p in self.db.get("pdfs", [])
            if not category or p.get("category") == category
        ]
        
        if len(pdfs) < min_pdfs:
            return {"message": f"Need at least {min_pdfs} PDFs to identify patterns"}
        
        patterns = {
            "styling_patterns": {},
            "quality_patterns": {},
            "content_patterns": {},
            "temporal_patterns": {}
        }
        
        # Styling patterns
        styles = [p.get("style") for p in pdfs if p.get("style")]
        if styles:
            style_counts = Counter(styles)
            patterns["styling_patterns"] = {
                "most_common": style_counts.most_common(1)[0] if style_counts else None,
                "distribution": dict(style_counts)
            }
        
        # Quality patterns
        qualities = [p.get("quality_score", 0) for p in pdfs]
        if qualities:
            patterns["quality_patterns"] = {
                "average": sum(qualities) / len(qualities),
                "range": (min(qualities), max(qualities)),
                "improving": qualities[-1] > qualities[0] if len(qualities) >= 2 else None
            }
        
        # Content patterns
        all_gaps = []
        all_suggestions = []
        for p in pdfs:
            all_gaps.extend(p.get("gaps", []))
            all_suggestions.extend(p.get("suggestions", []))
        
        if all_gaps:
            gap_counts = Counter(all_gaps)
            patterns["content_patterns"]["common_gaps"] = gap_counts.most_common(5)
        
        if all_suggestions:
            suggestion_counts = Counter(all_suggestions)
            patterns["content_patterns"]["common_suggestions"] = suggestion_counts.most_common(5)
        
        # Temporal patterns
        if len(pdfs) >= 2:
            pdfs_by_date = sorted(pdfs, key=lambda p: p.get("timestamp", ""))
            recent_qualities = [p.get("quality_score", 0) for p in pdfs_by_date[-5:]]
            older_qualities = [p.get("quality_score", 0) for p in pdfs_by_date[:-5]] if len(pdfs_by_date) > 5 else []
            
            if recent_qualities and older_qualities:
                recent_avg = sum(recent_qualities) / len(recent_qualities)
                older_avg = sum(older_qualities) / len(older_qualities)
                patterns["temporal_patterns"] = {
                    "recent_avg": recent_avg,
                    "older_avg": older_avg,
                    "change": recent_avg - older_avg
                }
        
        # Record pattern recognition event to TheObserver
        self._record_event(
            event_type=EvolutionaryEventType.GYM_EVAL,
            operation="identify_patterns",
            payload={
                "category": category,
                "pdfs_analyzed": len(pdfs),
                "patterns_found": {
                    "styling": bool(patterns.get("styling_patterns")),
                    "quality": bool(patterns.get("quality_patterns")),
                    "content": bool(patterns.get("content_patterns")),
                    "temporal": bool(patterns.get("temporal_patterns"))
                }
            },
            fitness_metrics={
                "average_quality": patterns.get("quality_patterns", {}).get("average", 0),
                "pdfs_analyzed": len(pdfs)
            }
        )
        
        return patterns
    
    def accumulate_knowledge(self) -> Dict[str, Any]:
        """
        Accumulate knowledge from all PDFs.
        
        Returns:
            Knowledge base summary
        """
        knowledge = {
            "total_pdfs": len(self.db.get("pdfs", [])),
            "total_hypotheses": len(self.db.get("hypotheses", [])),
            "total_findings": len(self.db.get("findings", [])),
            "knowledge_base": self.db.get("knowledge", []),
            "insights": []
        }
        
        # Extract insights from findings
        findings = self.db.get("findings", [])
        if findings:
            knowledge["insights"].extend(findings[-10:])  # Last 10 findings
        
        # Extract confirmed hypotheses
        hypotheses = self.db.get("hypotheses", [])
        confirmed = [h for h in hypotheses if h.get("test_result", {}).get("confirmed", False)]
        if confirmed:
            knowledge["insights"].append(f"{len(confirmed)} hypotheses confirmed")
        
        return knowledge
    
    def _std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
