"""
PDF Evolution System

Creates evolved PDFs using WAFT principles, Oracle insights, and context.
"""

from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

from ..pdf import PDF
from .science.oracle import TheOracle


class PDFEvolution:
    """
    Creates evolved PDFs using WAFT evolution principles.
    
    Uses Oracle for epistemic intelligence and WAFT principles:
    - "Part within the whole": PDF reflects current context within larger project
    - "As above, so below": PDF structure mirrors epistemic state
    - Evolution: PDF content evolves based on what system knows/doesn't know
    """
    
    def __init__(self, project_path: Path, oracle: Optional[TheOracle] = None):
        """
        Initialize PDF evolution system.
        
        Args:
            project_path: Path to project root
            oracle: Optional TheOracle instance (creates if None)
        """
        self.project_path = Path(project_path)
        
        # Initialize Oracle if not provided
        if oracle is None:
            try:
                self.oracle = TheOracle(self.project_path)
            except RuntimeError:
                # Oracle not available (Empirica not initialized)
                self.oracle = None
        else:
            self.oracle = oracle
    
    def evolve_pdf(
        self,
        context: Dict[str, Any],
        style: str = "clinical_standard",
        output_path: Optional[Path] = None
    ) -> Path:
        """
        Create an evolved PDF using WAFT principles.
        
        Args:
            context: Context dictionary with conversation, active files, etc.
            style: PDF style (default: clinical_standard)
            output_path: Optional output path (auto-generated if None)
        
        Returns:
            Path to generated PDF
        """
        # Determine PDF type based on context and Oracle state
        pdf_type = self._determine_pdf_type(context)
        
        # Get Oracle state if available
        oracle_state = None
        if self.oracle:
            try:
                oracle_state = self.oracle.get_epistemic_state()
                phase = self.oracle.get_epistemic_phase()
                oracle_state["epistemic_phase"] = phase
            except Exception:
                pass  # Oracle not available
        
        # Generate content
        content = self._generate_evolved_content(pdf_type, context, oracle_state)
        
        # Generate title
        title = self._generate_title(pdf_type, context, oracle_state)
        
        # Determine output path
        if output_path is None:
            output_path = self._generate_output_path(pdf_type, context)
        
        # Create PDF
        pdf = PDF.from_content(
            content=content,
            title=title,
            style=style,
            output_path=output_path
        )
        
        # Save PDF
        pdf_path = pdf.save()
        
        # Register in storage registry
        try:
            from ...utils import StorageRegistry, classify_content_type
            registry = StorageRegistry(self.project_path)
            # Get relative path for registry
            try:
                rel_path = pdf_path.relative_to(self.project_path)
            except ValueError:
                rel_path = Path(pdf_path.name)
            
            content_type = classify_content_type(rel_path)
            registry.register(
                str(rel_path),
                str(pdf_path),
                content_type
            )
        except Exception as e:
            # Non-critical, just log
            pass
        
        # Log to Oracle if available
        if self.oracle:
            try:
                self.oracle.log_insight(
                    f"Created evolved PDF: {pdf_path.name} (type: {pdf_type})",
                    impact=0.5
                )
            except Exception:
                pass  # Logging failed, continue
        
        return pdf_path
    
    def _determine_pdf_type(self, context: Dict[str, Any]) -> str:
        """
        Determine what type of PDF to create.
        
        Returns:
            PDF type: "conversation_summary" | "project_status" | "oracle_insights" | 
                     "work_effort" | "hybrid"
        """
        # Get Oracle phase if available
        phase = None
        if self.oracle:
            try:
                phase = self.oracle.get_epistemic_phase()
            except Exception:
                pass
        
        # Check conversation length
        conversation = context.get("conversation", [])
        conversation_length = len(conversation) if conversation else 0
        
        # Check for active work efforts
        work_efforts = context.get("work_efforts", [])
        has_work_efforts = len(work_efforts) > 0
        
        # Decision logic
        if phase == "Synthesis" or phase == "Evolution":
            if has_work_efforts:
                return "hybrid"  # Combine multiple sources
            else:
                return "oracle_insights"  # Focus on Oracle insights
        
        elif conversation_length > 20:
            return "conversation_summary"  # Long conversation needs summary
        
        elif has_work_efforts:
            return "work_effort"  # Active work efforts
        
        elif phase:
            return "oracle_insights"  # Use Oracle insights
        
        else:
            return "conversation_summary"  # Default to conversation summary
    
    def _generate_evolved_content(
        self,
        pdf_type: str,
        context: Dict[str, Any],
        oracle_state: Optional[Dict[str, Any]]
    ) -> str:
        """Generate markdown content for PDF based on type."""
        content_parts = []
        
        if pdf_type == "conversation_summary":
            content_parts.append(self._generate_conversation_summary(context))
        
        elif pdf_type == "project_status":
            content_parts.append(self._generate_project_status(context, oracle_state))
        
        elif pdf_type == "oracle_insights":
            content_parts.append(self._generate_oracle_insights(context, oracle_state))
        
        elif pdf_type == "work_effort":
            content_parts.append(self._generate_work_effort_summary(context))
        
        elif pdf_type == "hybrid":
            # Combine multiple sources
            content_parts.append(self._generate_conversation_summary(context))
            if oracle_state:
                content_parts.append(self._generate_oracle_insights(context, oracle_state))
            content_parts.append(self._generate_work_effort_summary(context))
        
        # Add "part within the whole" perspective
        content_parts.append(self._generate_part_within_whole(context, oracle_state))
        
        return "\n\n---\n\n".join(content_parts)
    
    def _generate_conversation_summary(self, context: Dict[str, Any]) -> str:
        """Generate conversation summary content."""
        conversation = context.get("conversation", [])
        
        content = "# Conversation Summary\n\n"
        content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if conversation:
            content += f"**Messages**: {len(conversation)}\n\n"
            content += "## Key Points\n\n"
            
            # Extract key points (simplified - in real implementation, use LLM)
            for i, msg in enumerate(conversation[:10], 1):  # First 10 messages
                if isinstance(msg, dict):
                    text = msg.get("content", "") or msg.get("text", "")
                elif isinstance(msg, str):
                    text = msg
                else:
                    continue
                
                if text and len(text) > 20:
                    # Truncate long messages
                    preview = text[:200] + "..." if len(text) > 200 else text
                    content += f"{i}. {preview}\n\n"
        else:
            content += "No conversation context available.\n\n"
        
        return content
    
    def _generate_project_status(self, context: Dict[str, Any], oracle_state: Optional[Dict[str, Any]]) -> str:
        """Generate project status content."""
        content = "# Project Status Report\n\n"
        content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if oracle_state:
            phase = oracle_state.get("epistemic_phase", "UNKNOWN")
            content += f"**Epistemic Phase**: {phase}\n\n"
            
            epistemic_state = oracle_state.get("epistemic_state", {})
            vectors = epistemic_state.get("vectors", {})
            foundation = vectors.get("foundation", {})
            know = foundation.get("know", 0.0) if foundation else 0.0
            uncertainty = vectors.get("uncertainty", 1.0)
            
            content += f"**Knowledge**: {know:.0%}\n"
            content += f"**Uncertainty**: {uncertainty:.0%}\n\n"
        
        active_files = context.get("active_files", [])
        if active_files:
            content += "## Active Files\n\n"
            for file_path in active_files[:10]:  # First 10 files
                content += f"- {file_path}\n"
            content += "\n"
        
        return content
    
    def _generate_oracle_insights(self, context: Dict[str, Any], oracle_state: Optional[Dict[str, Any]]) -> str:
        """Generate Oracle insights content."""
        content = "# Oracle Insights\n\n"
        content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        if not oracle_state or not self.oracle:
            content += "Oracle not available or not initialized.\n\n"
            return content
        
        phase = oracle_state.get("epistemic_phase", "UNKNOWN")
        content += f"**Epistemic Phase**: {phase}\n\n"
        
        # Get insights
        try:
            insights = self.oracle.get_insights(limit=10)
            if insights:
                content += "## Recent Insights\n\n"
                for insight in insights:
                    if isinstance(insight, dict):
                        text = insight.get("finding", "") or insight.get("text", "")
                        impact = insight.get("impact", 0.5)
                        content += f"- **{impact:.0%} impact**: {text}\n"
                    elif isinstance(insight, str):
                        content += f"- {insight}\n"
                content += "\n"
        except Exception:
            pass
        
        # Get unknowns
        try:
            unknowns = self.oracle.get_unknowns(limit=10)
            if unknowns:
                content += "## Open Questions\n\n"
                for unknown in unknowns:
                    if isinstance(unknown, dict):
                        text = unknown.get("unknown", "") or unknown.get("text", "")
                        content += f"- {text}\n"
                    elif isinstance(unknown, str):
                        content += f"- {unknown}\n"
                content += "\n"
        except Exception:
            pass
        
        return content
    
    def _generate_work_effort_summary(self, context: Dict[str, Any]) -> str:
        """Generate work effort summary content."""
        content = "# Work Effort Summary\n\n"
        content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        work_efforts = context.get("work_efforts", [])
        if work_efforts:
            content += f"**Active Work Efforts**: {len(work_efforts)}\n\n"
            for work_effort in work_efforts[:5]:  # First 5 work efforts
                content += f"- {work_effort}\n"
            content += "\n"
        else:
            content += "No active work efforts found.\n\n"
        
        return content
    
    def _generate_part_within_whole(
        self,
        context: Dict[str, Any],
        oracle_state: Optional[Dict[str, Any]]
    ) -> str:
        """Generate 'part within the whole' perspective section."""
        content = "# Part Within the Whole\n\n"
        content += "This document reflects the current work within the larger project context.\n\n"
        
        if oracle_state:
            phase = oracle_state.get("epistemic_phase", "UNKNOWN")
            content += f"**Current Phase**: {phase}\n\n"
            content += "The structure and content of this document mirror the current epistemic state, "
            content += "demonstrating the 'as above, so below' principle.\n\n"
        
        active_files = context.get("active_files", [])
        if active_files:
            content += "**Related Files**: This work connects to multiple files in the project, "
            content += "showing how individual components contribute to the whole.\n\n"
        
        return content
    
    def _generate_title(self, pdf_type: str, context: Dict[str, Any], oracle_state: Optional[Dict[str, Any]]) -> str:
        """Generate PDF title."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        
        if pdf_type == "conversation_summary":
            return f"Conversation Summary - {timestamp}"
        elif pdf_type == "project_status":
            return f"Project Status Report - {timestamp}"
        elif pdf_type == "oracle_insights":
            phase = oracle_state.get("epistemic_phase", "") if oracle_state else ""
            return f"Oracle Insights - {phase} - {timestamp}" if phase else f"Oracle Insights - {timestamp}"
        elif pdf_type == "work_effort":
            return f"Work Effort Summary - {timestamp}"
        elif pdf_type == "hybrid":
            return f"Evolved Document - {timestamp}"
        else:
            return f"Evolved PDF - {timestamp}"
    
    def _generate_output_path(self, pdf_type: str, context: Dict[str, Any]) -> Path:
        """Generate output path for PDF."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Use appropriate directory based on type
        if pdf_type == "work_effort":
            relative_path = Path("_work_efforts") / f"{pdf_type}_{timestamp}.pdf"
        elif pdf_type == "oracle_insights":
            relative_path = Path("_pyrite") / "oracle" / f"{pdf_type}_{timestamp}.pdf"
        else:
            relative_path = Path("_pyrite") / "evolved" / f"{pdf_type}_{timestamp}.pdf"
        
        # Use storage path resolver to route to external drive if available
        from ...utils import resolve_output_path
        return resolve_output_path(relative_path, self.project_path)
