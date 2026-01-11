"""
PDF Generation Metrics Collector

Core-level metrics collection for PDF generation to support evolution
with quality data. Metrics are collected optionally and stored in JSON
files for analysis and evolution tracking.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field, asdict


@dataclass
class PDFMetrics:
    """
    Comprehensive metrics for a single PDF generation.
    
    Captures all data needed for evolution and quality analysis.
    """
    # Identification
    pdf_id: str = ""  # SHA-256 hash of PDF content or path
    timestamp: datetime = field(default_factory=datetime.utcnow)
    generator_version: str = ""
    generator_genome_id: str = ""
    
    # Input metrics
    input_ideas_total: int = 0
    input_ideas_shown: int = 0
    input_ideas_importance_avg: float = 0.0
    input_ideas_importance_max: float = 0.0
    input_ideas_importance_min: float = 0.0
    chat_title: str = ""
    chat_summary_length: int = 0
    
    # Generation metrics
    generation_time_seconds: float = 0.0
    iterations_used: int = 0
    target_pages: int = 2
    actual_pages: int = 0
    constraint_satisfied: bool = False
    page_diff: int = 0  # abs(actual - target)
    
    # Output metrics
    pdf_path: Optional[str] = None
    pdf_size_bytes: int = 0
    html_size_bytes: int = 0
    pdf_exists: bool = False
    html_exists: bool = False
    
    # Styling metrics
    styling_genome_id: str = ""
    styling_scientific_name: str = ""
    font_family: str = ""
    font_size_body: float = 0.0
    font_size_h1: float = 0.0
    color_scheme: str = ""
    layout_density: str = ""
    margin_top: float = 0.0
    margin_bottom: float = 0.0
    margin_left: float = 0.0
    margin_right: float = 0.0
    
    # Fitness metrics
    fitness_readability: float = 0.0
    fitness_completeness: float = 0.0
    fitness_constraint: float = 0.0
    fitness_aesthetic: float = 0.0
    fitness_overall: float = 0.0
    
    # Conversion metrics
    png_conversion_attempted: bool = False
    png_conversion_success: bool = False
    png_count: int = 0
    png_dpi: int = 0
    png_total_size_bytes: int = 0
    
    # Content metrics
    content_words_total: int = 0
    content_words_page1: int = 0
    content_words_page2: int = 0
    content_density_words_per_page: float = 0.0
    content_paragraphs_total: int = 0
    content_lists_total: int = 0
    content_boxes_total: int = 0
    
    # Quality metrics
    quality_score: float = 0.0  # Computed from fitness + constraint
    quality_grade: str = ""  # "A", "B", "C", "D", "F"
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        data = asdict(self)
        # Convert datetime to ISO string
        if isinstance(data.get('timestamp'), datetime):
            data['timestamp'] = data['timestamp'].isoformat()
        return data
    
    def compute_quality_grade(self) -> str:
        """Compute letter grade from overall fitness."""
        overall = self.fitness_overall
        if overall >= 0.9:
            return "A"
        elif overall >= 0.8:
            return "B"
        elif overall >= 0.7:
            return "C"
        elif overall >= 0.6:
            return "D"
        else:
            return "F"
    
    def compute_quality_score(self) -> float:
        """Compute overall quality score (0.0-1.0)."""
        # Weighted combination of fitness and constraint satisfaction
        fitness_weight = 0.7
        constraint_weight = 0.3
        
        quality = (
            self.fitness_overall * fitness_weight +
            self.fitness_constraint * constraint_weight
        )
        return min(1.0, max(0.0, quality))


class PDFMetricsCollector:
    """
    Collects and stores PDF generation metrics for evolution tracking.
    
    Metrics are stored in JSON files organized by date for easy analysis.
    """
    
    def __init__(self, metrics_dir: Optional[Path] = None):
        """
        Initialize metrics collector.
        
        Args:
            metrics_dir: Directory to store metrics (default: _pyrite/metrics/pdf/)
        """
        if metrics_dir is None:
            # Default to project root if we can detect it
            metrics_dir = Path("_pyrite/metrics/pdf")
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        
        # Subdirectories
        self.daily_dir = self.metrics_dir / "daily"
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        
        self.aggregate_file = self.metrics_dir / "all_metrics.jsonl"
    
    def collect_metrics(
        self,
        result: Dict[str, Any],
        generation_start_time: datetime,
        styling_genome: Any,
        distilled_chat: Any,
        iterations: int = 1,
        png_info: Optional[Dict[str, Any]] = None,
        content_stats: Optional[Dict[str, Any]] = None,
    ) -> PDFMetrics:
        """
        Collect comprehensive metrics from PDF generation result.
        
        Args:
            result: Result dictionary from generate()
            generation_start_time: When generation started
            styling_genome: StylingGenome used
            distilled_chat: DistilledChat used
            iterations: Number of iterations used
            png_info: Optional PNG conversion info
            content_stats: Optional content statistics
        
        Returns:
            PDFMetrics object with all collected data
        """
        generation_time = (datetime.utcnow() - generation_start_time).total_seconds()
        
        # Compute PDF ID
        pdf_path = result.get("pdf_path")
        if pdf_path:
            pdf_id = self._compute_pdf_id(Path(pdf_path))
        else:
            pdf_id = hashlib.sha256(
                result.get("html_content", "").encode()
            ).hexdigest()[:16]
        
        # Get fitness metrics
        fitness = result.get("fitness_metrics", {})
        
        # Get styling info
        styling_genes = styling_genome.genes if hasattr(styling_genome, 'genes') else None
        
        # Build metrics
        metrics = PDFMetrics(
            pdf_id=pdf_id,
            timestamp=datetime.utcnow(),
            generator_version=result.get("generator_version", "V2"),
            generator_genome_id=result.get("generator_genome_id", ""),
            
            # Input
            input_ideas_total=distilled_chat.total_ideas if hasattr(distilled_chat, 'total_ideas') else 0,
            input_ideas_shown=result.get("ideas_shown", 0),
            input_ideas_importance_avg=self._compute_avg_importance(distilled_chat),
            input_ideas_importance_max=self._compute_max_importance(distilled_chat),
            input_ideas_importance_min=self._compute_min_importance(distilled_chat),
            chat_title=distilled_chat.title if hasattr(distilled_chat, 'title') else "",
            chat_summary_length=len(distilled_chat.summary) if hasattr(distilled_chat, 'summary') else 0,
            
            # Generation
            generation_time_seconds=generation_time,
            iterations_used=iterations,
            target_pages=result.get("target_pages", 2),
            actual_pages=result.get("page_count", 0),
            constraint_satisfied=result.get("constraint_satisfied", False),
            page_diff=abs(result.get("page_count", 0) - result.get("target_pages", 2)),
            
            # Output
            pdf_path=pdf_path,
            pdf_size_bytes=self._get_file_size(pdf_path) if pdf_path else 0,
            html_size_bytes=len(result.get("html_content", "")),
            pdf_exists=Path(pdf_path).exists() if pdf_path else False,
            html_exists=True,  # HTML is always generated
            
            # Styling
            styling_genome_id=styling_genome.genome_id if hasattr(styling_genome, 'genome_id') else "",
            styling_scientific_name=styling_genome.scientific_name if hasattr(styling_genome, 'scientific_name') else "",
            font_family=styling_genes.font.family if styling_genes and hasattr(styling_genes, 'font') else "",
            font_size_body=styling_genes.font.size_body if styling_genes and hasattr(styling_genes, 'font') else 0.0,
            font_size_h1=styling_genes.font.size_h1 if styling_genes and hasattr(styling_genes, 'font') else 0.0,
            color_scheme=styling_genes.color.scheme if styling_genes and hasattr(styling_genes, 'color') else "",
            layout_density=styling_genes.layout.density if styling_genes and hasattr(styling_genes, 'layout') else "",
            margin_top=styling_genes.margin.top if styling_genes and hasattr(styling_genes, 'margin') else 0.0,
            margin_bottom=styling_genes.margin.bottom if styling_genes and hasattr(styling_genes, 'margin') else 0.0,
            margin_left=styling_genes.margin.left if styling_genes and hasattr(styling_genes, 'margin') else 0.0,
            margin_right=styling_genes.margin.right if styling_genes and hasattr(styling_genes, 'margin') else 0.0,
            
            # Fitness
            fitness_readability=fitness.get("readability", 0.0),
            fitness_completeness=fitness.get("completeness", 0.0),
            fitness_constraint=fitness.get("constraint_satisfaction", 0.0),
            fitness_aesthetic=fitness.get("aesthetic_appeal", 0.0),
            fitness_overall=fitness.get("overall", 0.0),
            
            # Conversion
            png_conversion_attempted=bool(result.get("png_paths")),
            png_conversion_success=bool(result.get("png_paths")),
            png_count=len(result.get("png_paths", [])),
            png_dpi=png_info.get("dpi", 0) if png_info else 0,
            png_total_size_bytes=png_info.get("total_size_bytes", 0) if png_info else 0,
            
            # Content (from content_stats if provided)
            content_words_total=content_stats.get("words_total", 0) if content_stats else 0,
            content_words_page1=content_stats.get("words_page1", 0) if content_stats else 0,
            content_words_page2=content_stats.get("words_page2", 0) if content_stats else 0,
            content_density_words_per_page=content_stats.get("density", 0.0) if content_stats else 0.0,
            content_paragraphs_total=content_stats.get("paragraphs", 0) if content_stats else 0,
            content_lists_total=content_stats.get("lists", 0) if content_stats else 0,
            content_boxes_total=content_stats.get("boxes", 0) if content_stats else 0,
        )
        
        # Compute quality metrics
        metrics.quality_score = metrics.compute_quality_score()
        metrics.quality_grade = metrics.compute_quality_grade()
        
        return metrics
    
    def save_metrics(self, metrics: PDFMetrics) -> Path:
        """
        Save metrics to storage.
        
        Args:
            metrics: Metrics to save
        
        Returns:
            Path to saved metrics file
        """
        # Save to daily file (YYYY-MM-DD.jsonl)
        date_str = metrics.timestamp.strftime("%Y-%m-%d")
        daily_file = self.daily_dir / f"{date_str}.jsonl"
        
        with open(daily_file, "a") as f:
            f.write(json.dumps(metrics.to_dict(), default=str) + "\n")
        
        # Also append to aggregate file
        with open(self.aggregate_file, "a") as f:
            f.write(json.dumps(metrics.to_dict(), default=str) + "\n")
        
        return daily_file
    
    def _compute_pdf_id(self, pdf_path: Path) -> str:
        """Compute unique ID for PDF file."""
        if pdf_path.exists():
            return hashlib.sha256(pdf_path.read_bytes()).hexdigest()[:16]
        return hashlib.sha256(str(pdf_path).encode()).hexdigest()[:16]
    
    def _get_file_size(self, file_path: Optional[str]) -> int:
        """Get file size in bytes."""
        if file_path and Path(file_path).exists():
            return Path(file_path).stat().st_size
        return 0
    
    def _compute_avg_importance(self, distilled_chat: Any) -> float:
        """Compute average importance of ideas."""
        if not hasattr(distilled_chat, 'ideas') or not distilled_chat.ideas:
            return 0.0
        importances = [idea.importance for idea in distilled_chat.ideas if hasattr(idea, 'importance')]
        return sum(importances) / len(importances) if importances else 0.0
    
    def _compute_max_importance(self, distilled_chat: Any) -> float:
        """Compute max importance of ideas."""
        if not hasattr(distilled_chat, 'ideas') or not distilled_chat.ideas:
            return 0.0
        importances = [idea.importance for idea in distilled_chat.ideas if hasattr(idea, 'importance')]
        return max(importances) if importances else 0.0
    
    def _compute_min_importance(self, distilled_chat: Any) -> float:
        """Compute min importance of ideas."""
        if not hasattr(distilled_chat, 'ideas') or not distilled_chat.ideas:
            return 0.0
        importances = [idea.importance for idea in distilled_chat.ideas if hasattr(idea, 'importance')]
        return min(importances) if importances else 0.0
