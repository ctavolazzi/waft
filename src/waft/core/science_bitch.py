"""
Science-Bitch: Full Scientific Method Command

Runs the complete scientific method workflow:
1. Form hypothesis
2. Design experiment
3. Capture initial state (A)
4. Run experiment
5. Collect data (C)
6. Capture final state (B)
7. Analyze results
8. Generate reports
"""

from pathlib import Path
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
import re
import subprocess
import platform
import markdown
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import scientific method tool
import sys

# Add project root to path for scientific_method_tool
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from scientific_method_tool import (
    Hypothesis,
    Variable,
    VariableType,
    ExperimentManager,
    ExperimentLoop,
    ExperimentAnalyzer,
    IterationConfig,
)


class ScienceBitchManager:
    """Manages the full scientific method workflow."""
    
    def __init__(self, project_path: Path):
        """
        Initialize Science-Bitch manager.
        
        Args:
            project_path: Path to project root
        """
        self.project_path = project_path
        self.science_path = project_path / "_science"
        self.science_path.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.science_path / "experiments").mkdir(exist_ok=True)
        (self.science_path / "data").mkdir(exist_ok=True)
        (self.science_path / "reports").mkdir(exist_ok=True)
        (self.science_path / "tools").mkdir(exist_ok=True)
        
        self.console = Console()
        self.experiment_manager = ExperimentManager(self.science_path / "experiments")
        self.analyzer = ExperimentAnalyzer()
        
    def run_interactive(self) -> Dict[str, Any]:
        """
        Run interactive scientific method workflow.
        
        Returns:
            Dictionary with results
        """
        self.console.print("\n[bold cyan]🔬 Science-Bitch: Full Scientific Method[/bold cyan]\n")
        
        # Step 1: Form hypothesis
        hypothesis = self._form_hypothesis()
        if not hypothesis:
            return {"success": False, "error": "Hypothesis creation cancelled"}
        
        # Step 2: Design experiment
        experiment_design = self._design_experiment(hypothesis)
        if not experiment_design:
            return {"success": False, "error": "Experiment design cancelled"}
        
        # Step 3: Run experiment
        results = self._run_experiment(hypothesis, experiment_design)
        if not results:
            return {"success": False, "error": "Experiment failed"}
        
        # Step 4: Analyze results
        analysis = self._analyze_results(hypothesis, results)
        
        # Step 5: Generate report
        report_path = self._generate_report(hypothesis, results, analysis)
        
        return {
            "success": True,
            "hypothesis": hypothesis.to_dict(),
            "results": results,
            "analysis": analysis.to_dict() if hasattr(analysis, 'to_dict') else str(analysis),
            "report_path": str(report_path) if report_path else None,
        }
    
    def _form_hypothesis(self) -> Optional[Hypothesis]:
        """Interactively form a hypothesis."""
        self.console.print("[bold]Step 1: Form Hypothesis[/bold]\n")
        
        # Get statement
        statement = self.console.input("[cyan]Hypothesis statement:[/cyan] ")
        if not statement:
            return None
        
        # Get prediction
        prediction = self.console.input("[cyan]Prediction:[/cyan] ")
        if not prediction:
            return None
        
        hypothesis = Hypothesis(statement=statement, prediction=prediction)
        
        # Add variables
        self.console.print("\n[dim]Add variables (press Enter to finish):[/dim]")
        while True:
            var_name = self.console.input("[cyan]Variable name:[/cyan] ")
            if not var_name:
                break
            
            var_type_str = self.console.input("[cyan]Type (independent/dependent/control):[/cyan] ")
            var_type_map = {
                "independent": VariableType.INDEPENDENT,
                "dependent": VariableType.DEPENDENT,
                "control": VariableType.CONTROL,
            }
            var_type = var_type_map.get(var_type_str.lower(), VariableType.INDEPENDENT)
            
            var_value_str = self.console.input("[cyan]Value:[/cyan] ")
            try:
                var_value = float(var_value_str) if var_value_str else 0.0
            except ValueError:
                var_value = 0.0
            
            var_desc = self.console.input("[cyan]Description:[/cyan] ")
            
            hypothesis.add_variable(Variable(
                name=var_name,
                type=var_type,
                value=var_value,
                description=var_desc or f"{var_name} variable"
            ))
        
        # Display hypothesis
        self.console.print("\n[green]✓[/green] Hypothesis created:")
        self._display_hypothesis(hypothesis)
        
        return hypothesis
    
    def _design_experiment(self, hypothesis: Hypothesis) -> Optional[Dict[str, Any]]:
        """Design experiment."""
        self.console.print("\n[bold]Step 2: Design Experiment[/bold]\n")
        
        # Create experiment
        experiment = self.experiment_manager.create_experiment(hypothesis)
        
        self.console.print(f"[green]✓[/green] Experiment created: {experiment.experiment_id}")
        
        # Get experiment function
        self.console.print("\n[yellow]→[/yellow] You'll need to provide an experiment function.")
        self.console.print("[dim]This function will be called to run the experiment.[/dim]")
        
        return {
            "experiment": experiment,
            "experiment_id": experiment.experiment_id,
        }
    
    def _run_experiment(
        self,
        hypothesis: Hypothesis,
        design: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Run experiment."""
        self.console.print("\n[bold]Step 3: Run Experiment[/bold]\n")
        
        experiment = design["experiment"]
        
        # For now, use a simple placeholder experiment function
        # In real usage, this would be provided by the user or loaded from a file
        def simple_experiment(exp):
            """Simple experiment function."""
            # This is a placeholder - real experiments would do actual work
            exp.data_collector.record("test_metric", 42.0)
            return {
                "success": True,
                "test_metric": 42.0,
                "prediction_match": True,
                "confidence": 0.75
            }
        
        # Capture initial state
        self.console.print("[yellow]→[/yellow] Capturing initial state (A)...")
        components = self._create_initial_components(hypothesis)
        initial_state = self.experiment_manager.capture_initial_state(experiment, components)
        self.console.print(f"[green]✓[/green] Initial state captured: {initial_state.state_hash[:8]}")
        
        # Run experiment
        self.console.print("[yellow]→[/yellow] Running experiment...")
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Running...", total=None)
            results = self.experiment_manager.run_experiment(
                experiment,
                simple_experiment,
                components
            )
            progress.update(task, completed=True)
        
        self.console.print(f"[green]✓[/green] Experiment completed")
        
        # Display results
        if results:
            self.console.print(f"\n[bold]Results:[/bold]")
            for key, value in results.items():
                self.console.print(f"  {key}: {value}")
        
        return results
    
    def _create_initial_components(self, hypothesis: Hypothesis) -> Dict[str, Any]:
        """Create initial components from hypothesis variables."""
        components = {}
        for var in hypothesis.variables:
            if var.type == VariableType.INDEPENDENT:
                components[var.name] = var.value
        return components
    
    def _analyze_results(
        self,
        hypothesis: Hypothesis,
        results: Dict[str, Any]
    ) -> Any:
        """Analyze experiment results."""
        self.console.print("\n[bold]Step 4: Analyze Results[/bold]\n")
        
        # Get experiment
        experiment = self.experiment_manager.get_experiment(results.get("experiment_id"))
        if not experiment:
            self.console.print("[red]❌ Experiment not found[/red]")
            return None
        
        # Analyze
        self.console.print("[yellow]→[/yellow] Analyzing results...")
        analysis = self.analyzer.analyze_experiment(hypothesis, experiment)
        
        # Display analysis
        self._display_analysis(analysis)
        
        return analysis
    
    def _generate_report(
        self,
        hypothesis: Hypothesis,
        results: Dict[str, Any],
        analysis: Any
    ) -> Optional[Path]:
        """Generate comprehensive research PDF report using academic paper template and print it."""
        self.console.print("\n[bold]Step 5: Generate Research Report[/bold]\n")
        
        self.console.print("[yellow]→[/yellow] Creating comprehensive research PDF...")
        
        # Create comprehensive report content
        report_content = self._create_comprehensive_report_content(hypothesis, results, analysis)
        
        # Save markdown backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_md = self.science_path / "reports" / f"experiment_report_{timestamp}.md"
        report_md.write_text(report_content)
        
        # Generate PDF using academic paper template (like generate_all_pdfs_comparison.py)
        try:
            import sys
            import subprocess
            import platform
            from pathlib import Path
            
            # Add project root to path
            project_root = self.project_path
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))
            
            # Import the academic paper generator
            from src.waft.templates.academic_paper import generate_academic_paper
            import markdown
            import re
            
            # Extract metadata from report content (similar to generate_all_pdfs_comparison.py)
            metadata = self._extract_metadata_from_content(report_content)
            
            # Process markdown content to HTML
            html_content = self._process_markdown_to_html(report_content, metadata)
            
            # Generate PDF filename
            pdf_filename = f"Science_Research_Report_{timestamp}.pdf"
            pdf_path = self.science_path / "reports" / pdf_filename
            
            self.console.print(f"[yellow]→[/yellow] Generating ArXiv-style academic PDF...")
            
            # Generate PDF using academic paper template
            generated_path = generate_academic_paper(
                title=metadata.get("title", f"Scientific Research Report: {hypothesis.statement[:50]}..."),
                content=html_content,
                output_path=pdf_path,
                abstract=metadata.get("abstract", ""),
                authors=metadata.get("authors", [{"name": "WAFT Research Team"}]),
                affiliations=metadata.get("affiliations"),
                email=metadata.get("email"),
                conference="arXiv",
                year=metadata.get("year", str(datetime.now().year)),
                references=metadata.get("references")
            )
            
            if generated_path and generated_path.exists():
                size = generated_path.stat().st_size / 1024  # KB
                self.console.print(f"[green]✓[/green] Research PDF generated: {generated_path}")
                self.console.print(f"[dim]   Size: {size:.1f} KB[/dim]")
                
                # Open PDF automatically
                self.console.print("[yellow]→[/yellow] Opening PDF...")
                system = platform.system()
                if system == "Darwin":  # macOS
                    subprocess.run(["open", str(generated_path)], check=False)
                elif system == "Windows":
                    subprocess.run(["start", str(generated_path)], shell=True, check=False)
                else:  # Linux
                    subprocess.run(["xdg-open", str(generated_path)], check=False)
                
                # Print PDF to material world (only if explicitly requested)
                # Note: Printing is now opt-in to prevent duplicate printing
                # User can print manually with: lpr {generated_path}
                self.console.print(f"[dim]💡 To print: lpr {generated_path}[/dim]")
                
                self.console.print(f"[green]✓[/green] PDF ready: {generated_path}")
                return generated_path
            else:
                self.console.print("[yellow]⚠️[/yellow]  PDF generation failed, markdown saved")
                return report_md
                
        except Exception as e:
            self.console.print(f"[red]❌[/red] PDF generation error: {e}")
            self.console.print(f"[dim]Markdown saved: {report_md}[/dim]")
            import traceback
            self.console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return report_md
    
    def _extract_metadata_from_content(self, content: str) -> Dict[str, Any]:
        """Extract metadata from report content (similar to generate_all_pdfs_comparison.py)."""
        metadata = {
            "title": "",
            "abstract": "",
            "authors": [],
            "affiliations": [],
            "email": None,
            "year": str(datetime.now().year),
            "references": []
        }
        
        lines = content.split('\n')
        
        # Try to extract YAML frontmatter first
        frontmatter = {}
        if lines and lines[0].strip() == '---':
            i = 1
            current_key = None
            current_value = []
            while i < len(lines) and lines[i].strip() != '---':
                line = lines[i]
                line_stripped = line.strip()
                
                # Check if this is a new key-value pair
                if ':' in line_stripped and not line_stripped.startswith('-') and not line_stripped.startswith(' '):
                    # Save previous key-value if exists
                    if current_key and current_value:
                        frontmatter[current_key] = '\n'.join(current_value).strip().strip('"').strip("'")
                    
                    # Start new key-value
                    key, value = line_stripped.split(':', 1)
                    current_key = key.strip().lower()
                    value_stripped = value.strip().strip('"').strip("'")
                    if value_stripped:
                        current_value = [value_stripped]
                    else:
                        current_value = []
                elif current_key:
                    # Continuation of current value (indented or list item)
                    if line_stripped.startswith('-') or line_stripped.startswith(' '):
                        current_value.append(line_stripped.lstrip('- ').strip().strip('"').strip("'"))
                    elif line_stripped:
                        current_value.append(line_stripped.strip().strip('"').strip("'"))
                
                i += 1
            
            # Save last key-value
            if current_key and current_value:
                frontmatter[current_key] = '\n'.join(current_value).strip().strip('"').strip("'")
        
        # Extract from frontmatter if available
        if frontmatter:
            metadata["title"] = frontmatter.get("title", "").strip().strip('"').strip("'")
            metadata["abstract"] = frontmatter.get("abstract", "").strip().strip('"').strip("'")
            
            # Handle authors (can be string or list in YAML)
            if "authors" in frontmatter:
                authors_value = frontmatter["authors"]
                if isinstance(authors_value, str):
                    authors_list = [a.strip() for a in re.split(r'[,\n]', authors_value) if a.strip()]
                    metadata["authors"] = [{"name": author} for author in authors_list]
                elif isinstance(authors_value, list):
                    metadata["authors"] = [{"name": str(a).strip()} for a in authors_value if str(a).strip()]
            
            metadata["email"] = frontmatter.get("email", "").strip().strip('"').strip("'") or None
            year_value = frontmatter.get("year", "")
            if year_value:
                metadata["year"] = str(year_value).strip().strip('"').strip("'")
        
        # Extract from markdown structure if not in frontmatter
        # Title: First H1
        if not metadata["title"]:
            for line in lines:
                if line.startswith('# ') and not line.startswith('##'):
                    metadata["title"] = line[2:].strip()
                    break
        
        # Abstract: Look for ## Abstract section
        if not metadata["abstract"]:
            in_abstract = False
            abstract_lines = []
            for line in lines:
                line_stripped = line.strip()
                if line_stripped.lower().startswith('## abstract'):
                    in_abstract = True
                    continue
                elif in_abstract:
                    if line_stripped.startswith('##') or line_stripped.startswith('---'):
                        break
                    if line_stripped:
                        abstract_lines.append(line_stripped)
            if abstract_lines:
                abstract_text = ' '.join(abstract_lines)
                abstract_text = re.sub(r'\*\*([^*]+)\*\*', r'\1', abstract_text)
                abstract_text = re.sub(r'\*([^*]+)\*', r'\1', abstract_text)
                metadata["abstract"] = abstract_text
        
        # Extract references from ## References section
        in_references = False
        for line in lines:
            line_stripped = line.strip()
            if line_stripped.lower().startswith('## references'):
                in_references = True
                continue
            elif in_references:
                if line_stripped.startswith('##') and not line_stripped.lower().startswith('## references'):
                    break
                if line_stripped and (line_stripped.startswith('[') or line_stripped[0].isdigit() or line_stripped.startswith('-')):
                    ref = re.sub(r'^[\d\.\-\s\)\[\]]+', '', line_stripped)
                    if ref and len(ref) > 10:
                        metadata["references"].append(ref)
        
        # Default values
        if not metadata["title"]:
            metadata["title"] = "Scientific Research Report"
        if not metadata["authors"]:
            metadata["authors"] = [{"name": "WAFT Research Team"}]
        
        return metadata
    
    def _process_markdown_to_html(self, content: str, metadata: Dict[str, Any]) -> str:
        """Process markdown content to HTML (similar to generate_all_pdfs_comparison.py)."""
        lines = content.split('\n')
        processed_lines = []
        
        # Skip YAML frontmatter
        skip_frontmatter = False
        if lines and lines[0].strip() == '---':
            skip_frontmatter = True
            i = 1
            while i < len(lines) and lines[i].strip() != '---':
                i += 1
            if i < len(lines):
                i += 1  # Skip closing ---
                lines = lines[i:]
        
        # Skip Abstract and References sections (handled by template)
        skip_abstract = False
        skip_references = False
        
        for line in lines:
            line_stripped = line.strip()
            line_lower = line_stripped.lower()
            
            # Skip Abstract section
            if line_lower.startswith('## abstract') or line_lower.startswith('# abstract'):
                skip_abstract = True
                continue
            elif skip_abstract:
                if line_stripped.startswith('##') or line_stripped.startswith('# ') or line_stripped.startswith('---'):
                    skip_abstract = False
                    if not line_lower.startswith('## abstract') and not line_lower.startswith('# abstract'):
                        continue
                else:
                    continue
            
            # Skip References section
            if line_lower.startswith('## references') or line_lower.startswith('# references'):
                skip_references = True
                continue
            elif skip_references:
                if line_stripped.startswith('##') and not line_lower.startswith('## references'):
                    skip_references = False
                    continue
                elif line_stripped.startswith('# ') and not line_lower.startswith('# references'):
                    skip_references = False
                    continue
                else:
                    continue
            
            if skip_abstract or skip_references:
                continue
            
            processed_lines.append(line)
        
        # Convert markdown to HTML
        processed_md = '\n'.join(processed_lines)
        html_content = markdown.markdown(
            processed_md,
            extensions=[
                'fenced_code',
                'tables',
                'nl2br',
                'extra',
                'codehilite',
                'md_in_html'
            ]
        )
        
        return html_content
    
    def _create_report_content(
        self,
        hypothesis: Hypothesis,
        results: Dict[str, Any],
        analysis: Any
    ) -> str:
        """Create report content."""
        content = f"""# Experiment Report

**Generated**: {datetime.now().isoformat()}

---

## Hypothesis

**Statement**: {hypothesis.statement}

**Prediction**: {hypothesis.prediction}

### Variables

"""
        for var in hypothesis.variables:
            content += f"- **{var.name}** ({var.type.value}): {var.value}\n"
            if var.description:
                content += f"  - {var.description}\n"
        
        content += f"""
---

## Results

"""
        for key, value in results.items():
            content += f"- **{key}**: {value}\n"
        
        content += f"""
---

## Analysis

"""
        if hasattr(analysis, 'verified'):
            content += f"**Verified**: {analysis.verified}\n"
        if hasattr(analysis, 'confidence'):
            content += f"**Confidence**: {analysis.confidence:.2%}\n"
        if hasattr(analysis, 'conclusions'):
            content += f"**Conclusions**: {analysis.conclusions}\n"
        
        content += """
---

## Conclusion

[Analysis conclusions and recommendations]

"""
        return content
    
    def _create_comprehensive_report_content(
        self,
        hypothesis: Hypothesis,
        results: Dict[str, Any],
        analysis: Any
    ) -> str:
        """Create comprehensive scientific research report content."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get experiment data if available
        experiment_id = results.get("experiment_id")
        experiment = None
        state_a = None
        state_b = None
        collected_data = None
        
        if experiment_id:
            experiment = self.experiment_manager.get_experiment(experiment_id)
            if experiment:
                # Get state snapshots
                state_a = experiment.initial_state
                state_b = experiment.final_state
                # Get collected data
                if hasattr(experiment, 'data_collector'):
                    collected_data = experiment.data_collector.get_all_data()
        
        content = f"""---
title: "Scientific Research Report: {hypothesis.statement[:80]}..."
authors:
  - name: "WAFT Research Team"
abstract: |
  This report documents a complete scientific method workflow, including hypothesis formation, experiment design, state capture, data collection, and analysis. The research follows rigorous scientific methodology with traceable evidence and reproducible results. Hypothesis: {hypothesis.statement}. Prediction: {hypothesis.prediction[:100]}...
year: "{datetime.now().year}"
conference: "arXiv"
email: "waft@example.com"
---

# Scientific Research Report

**Generated**: {timestamp}  
**Experiment ID**: {experiment_id or "N/A"}  
**Status**: Complete

---

## Abstract

This report documents a complete scientific method workflow, including hypothesis formation, experiment design, state capture, data collection, and analysis. The research follows rigorous scientific methodology with traceable evidence and reproducible results.

**Hypothesis**: {hypothesis.statement}

**Prediction**: {hypothesis.prediction}

---

## 1. Hypothesis

### Statement

**{hypothesis.statement}**

### Prediction

**{hypothesis.prediction}**

### Variables

"""
        
        # Independent variables
        independent_vars = [v for v in hypothesis.variables if v.type == VariableType.INDEPENDENT]
        if independent_vars:
            content += "#### Independent Variables\n\n"
            for var in independent_vars:
                content += f"- **{var.name}**: {var.value}"
                if var.description:
                    content += f" - {var.description}"
                content += "\n"
            content += "\n"
        
        # Dependent variables
        dependent_vars = [v for v in hypothesis.variables if v.type == VariableType.DEPENDENT]
        if dependent_vars:
            content += "#### Dependent Variables\n\n"
            for var in dependent_vars:
                content += f"- **{var.name}**: {var.value}"
                if var.description:
                    content += f" - {var.description}"
                content += "\n"
            content += "\n"
        
        # Control variables
        control_vars = [v for v in hypothesis.variables if v.type == VariableType.CONTROL]
        if control_vars:
            content += "#### Control Variables\n\n"
            for var in control_vars:
                content += f"- **{var.name}**: {var.value}"
                if var.description:
                    content += f" - {var.description}"
                content += "\n"
            content += "\n"
        
        content += f"""---

## 2. Experiment Design

### Experiment Structure

**Experiment ID**: {experiment_id or "N/A"}

**Design Methodology**: Systematic scientific method workflow

**Components Tracked**: {len(hypothesis.variables)} variables

### Experimental Procedure

1. **Initial State Capture (A)**: System state captured before experiment
2. **Experiment Execution**: Controlled experiment run with data collection
3. **Data Collection (C)**: Systematic measurement during experiment
4. **Final State Capture (B)**: System state captured after experiment
5. **Analysis**: Comparative analysis of states and data

---

## 3. State Capture

### Initial State (A)

"""
        
        if state_a:
            content += f"""**State Hash**: `{state_a.state_hash[:16]}...`

**Components Captured**: {len(state_a.components) if hasattr(state_a, 'components') else 0}

**Timestamp**: {state_a.timestamp if hasattr(state_a, 'timestamp') else 'N/A'}

#### Component Values

"""
            if hasattr(state_a, 'components'):
                for comp_name, comp_value in state_a.components.items():
                    content += f"- **{comp_name}**: {comp_value}\n"
        else:
            content += "*Initial state not captured*\n"
        
        content += "\n### Final State (B)\n\n"
        
        if state_b:
            content += f"""**State Hash**: `{state_b.state_hash[:16]}...`

**Components Captured**: {len(state_b.components) if hasattr(state_b, 'components') else 0}

**Timestamp**: {state_b.timestamp if hasattr(state_b, 'timestamp') else 'N/A'}

#### Component Values

"""
            if hasattr(state_b, 'components'):
                for comp_name, comp_value in state_b.components.items():
                    content += f"- **{comp_name}**: {comp_value}\n"
            
            # State comparison
            if state_a and hasattr(state_a, 'components') and hasattr(state_b, 'components'):
                content += "\n#### State Comparison\n\n"
                content += "**Changes Detected**:\n\n"
                all_keys = set(state_a.components.keys()) | set(state_b.components.keys())
                changes = []
                for key in all_keys:
                    val_a = state_a.components.get(key, "N/A")
                    val_b = state_b.components.get(key, "N/A")
                    if val_a != val_b:
                        changes.append(f"- **{key}**: {val_a} → {val_b}")
                
                if changes:
                    content += "\n".join(changes) + "\n"
                else:
                    content += "*No changes detected*\n"
        else:
            content += "*Final state not captured*\n"
        
        content += "\n---\n\n## 4. Data Collection (C)\n\n"
        
        if collected_data:
            content += "### Collected Data Series\n\n"
            for series_name, series_data in collected_data.items():
                content += f"#### {series_name}\n\n"
                if isinstance(series_data, list):
                    content += f"**Data Points**: {len(series_data)}\n\n"
                    content += "**Values**: "
                    if len(series_data) <= 10:
                        content += ", ".join([str(v) for v in series_data])
                    else:
                        content += ", ".join([str(v) for v in series_data[:5]]) + f" ... ({len(series_data) - 5} more)"
                    content += "\n\n"
                else:
                    content += f"**Value**: {series_data}\n\n"
        else:
            content += "*No data collected during experiment*\n"
        
        content += f"""---

## 5. Results

### Experimental Outcomes

"""
        
        for key, value in results.items():
            if key != "experiment_id":  # Skip internal IDs
                if isinstance(value, dict):
                    content += f"#### {key}\n\n"
                    for sub_key, sub_value in value.items():
                        content += f"- **{sub_key}**: {sub_value}\n"
                    content += "\n"
                else:
                    content += f"- **{key}**: {value}\n"
        
        content += "\n---\n\n## 6. Analysis\n\n"
        
        if hasattr(analysis, 'verified'):
            content += f"### Hypothesis Verification\n\n"
            content += f"**Status**: {'✅ Verified' if analysis.verified else '❌ Not Verified'}\n\n"
        
        if hasattr(analysis, 'confidence'):
            content += f"### Confidence Level\n\n"
            content += f"**Confidence**: {analysis.confidence:.2%}\n\n"
        
        if hasattr(analysis, 'conclusions'):
            content += f"### Conclusions\n\n"
            if isinstance(analysis.conclusions, str):
                content += f"{analysis.conclusions}\n\n"
            elif isinstance(analysis.conclusions, list):
                for conclusion in analysis.conclusions:
                    content += f"- {conclusion}\n"
                content += "\n"
            else:
                content += f"{analysis.conclusions}\n\n"
        
        if hasattr(analysis, 'to_dict'):
            analysis_dict = analysis.to_dict()
            if 'evidence' in analysis_dict:
                content += "### Evidence\n\n"
                for evidence_item in analysis_dict['evidence']:
                    content += f"- {evidence_item}\n"
                content += "\n"
        
        content += """---

## 7. Scientific Method Workflow

This research followed the complete scientific method:

1. **Observation**: Identified phenomenon or question
2. **Hypothesis Formation**: Created testable hypothesis with variables
3. **Experiment Design**: Designed controlled experiment
4. **State Capture (A)**: Captured initial system state
5. **Experiment Execution**: Ran experiment with data collection
6. **Data Collection (C)**: Systematically collected measurements
7. **State Capture (B)**: Captured final system state
8. **Analysis**: Compared states, analyzed data, verified hypothesis
9. **Conclusion**: Drew evidence-based conclusions

---

## 8. Reproducibility

### Experiment Parameters

All experiment parameters are documented above. To reproduce:

1. Use the same hypothesis statement and variables
2. Capture initial state (A) with same components
3. Run experiment with same procedure
4. Collect data (C) using same metrics
5. Capture final state (B) for comparison

### Data Availability

- **Experiment ID**: {experiment_id or "N/A"}
- **State Files**: Available in `_science/experiments/{experiment_id}/`
- **Data Files**: Available in `_science/data/{experiment_id}/`
- **Report**: This document

---

## 9. Conclusions and Recommendations

### Key Findings

"""
        
        if hasattr(analysis, 'conclusions'):
            if isinstance(analysis.conclusions, str):
                content += f"{analysis.conclusions}\n\n"
            elif isinstance(analysis.conclusions, list):
                for conclusion in analysis.conclusions:
                    content += f"- {conclusion}\n"
                content += "\n"
        
        content += """### Recommendations

Based on this research:

1. **Hypothesis Status**: The hypothesis was """ + ("verified" if (hasattr(analysis, 'verified') and analysis.verified) else "not verified") + """
2. **Confidence**: """ + (f"{analysis.confidence:.2%}" if hasattr(analysis, 'confidence') else "Not calculated") + """
3. **Next Steps**: Consider refining hypothesis or running additional experiments

---

## 10. Appendices

### A. Raw Data

All raw data is available in the experiment data files.

### B. State Snapshots

Complete state snapshots are available in the experiment state files.

### C. Methodology

This research used the Science-Bitch scientific method workflow tool, which implements:
- Systematic state capture
- Controlled data collection
- Evidence-based analysis
- Reproducible methodology

---

**Report Generated**: {timestamp}  
**Tool**: Science-Bitch Scientific Method Workflow  
**Version**: 1.0

---

## References

1. WAFT Repository: https://github.com/ctavolazzi/waft
2. Scientific Method Tool: `scientific_method_tool/`
3. Science-Bitch Command: `src/waft/core/science_bitch.py`
4. Experiment ID: {experiment_id or "N/A"}

---

*This is real research. This is real science. This is real evidence.* 🔬
"""
        
        return content
    
    def _display_hypothesis(self, hypothesis: Hypothesis) -> None:
        """Display hypothesis in a formatted table."""
        table = Table(title="Hypothesis", show_header=True)
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("Statement", hypothesis.statement)
        table.add_row("Prediction", hypothesis.prediction)
        
        self.console.print(table)
        
        if hypothesis.variables:
            var_table = Table(title="Variables", show_header=True)
            var_table.add_column("Name", style="cyan")
            var_table.add_column("Type", style="yellow")
            var_table.add_column("Value", style="green")
            var_table.add_column("Description", style="dim")
            
            for var in hypothesis.variables:
                var_table.add_row(
                    var.name,
                    var.type.value,
                    str(var.value),
                    var.description or ""
                )
            
            self.console.print("\n")
            self.console.print(var_table)
    
    def _display_analysis(self, analysis: Any) -> None:
        """Display analysis results."""
        table = Table(title="Analysis Results", show_header=True)
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        
        if hasattr(analysis, 'verified'):
            table.add_row("Verified", "✅ Yes" if analysis.verified else "❌ No")
        if hasattr(analysis, 'confidence'):
            table.add_row("Confidence", f"{analysis.confidence:.2%}")
        if hasattr(analysis, 'conclusions'):
            table.add_row("Conclusions", str(analysis.conclusions))
        
        self.console.print("\n")
        self.console.print(table)
    
    def generate_field_guide(self) -> Optional[Path]:
        """Generate field guide PDF using academic paper template and print it."""
        # Create field guide content
        guide_content = self._create_field_guide_content()
        guide_md = self.science_path / "reports" / "field_guide.md"
        guide_md.write_text(guide_content)
        
        # Generate PDF using academic paper template
        guide_pdf = self.science_path / "reports" / "field_guide.pdf"
        
        try:
            import sys
            # Add project root to path
            if str(self.project_path) not in sys.path:
                sys.path.insert(0, str(self.project_path))
            
            from src.waft.templates.academic_paper import generate_academic_paper
            
            # Extract metadata
            metadata = self._extract_metadata_from_content(guide_content)
            
            # Process markdown to HTML
            html_content = self._process_markdown_to_html(guide_content, metadata)
            
            # Generate PDF
            self.console.print("[yellow]→[/yellow] Generating ArXiv-style field guide PDF...")
            generated_path = generate_academic_paper(
                title=metadata.get("title", "Science-Bitch Field Guide"),
                content=html_content,
                output_path=guide_pdf,
                abstract=metadata.get("abstract", ""),
                authors=metadata.get("authors", [{"name": "WAFT Development Team"}]),
                affiliations=metadata.get("affiliations"),
                email=metadata.get("email"),
                conference="arXiv",
                year=metadata.get("year", str(datetime.now().year)),
                references=metadata.get("references")
            )
            
            if generated_path and generated_path.exists():
                size = generated_path.stat().st_size / 1024  # KB
                self.console.print(f"[green]✓[/green] Field guide PDF generated: {generated_path}")
                self.console.print(f"[dim]   Size: {size:.1f} KB[/dim]")
                
                # Open PDF
                system = platform.system()
                if system == "Darwin":  # macOS
                    subprocess.run(["open", str(generated_path)], check=False)
                elif system == "Windows":
                    subprocess.run(["start", str(generated_path)], shell=True, check=False)
                else:  # Linux
                    subprocess.run(["xdg-open", str(generated_path)], check=False)
                
                # Print PDF (opt-in to prevent duplicate printing)
                # User can print manually with: lpr {generated_path}
                self.console.print(f"[dim]💡 To print: lpr {generated_path}[/dim]")
                
                return generated_path
        
        except Exception as e:
            self.console.print(f"[yellow]⚠️[/yellow]  PDF generation failed: {e}")
            self.console.print(f"[dim]Markdown saved: {guide_md}[/dim]")
            import traceback
            self.console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return guide_md
        
        return guide_md if guide_md.exists() else None
    
    def generate_project_status_report(self) -> Optional[Path]:
        """Generate project status PDF using academic paper template and print it."""
        # Create project status content
        status_content = self._create_project_status_content()
        status_md = self.science_path / "reports" / "project_status.md"
        status_md.write_text(status_content)
        
        # Generate PDF using academic paper template
        status_pdf = self.science_path / "reports" / "project_status.pdf"
        
        try:
            import sys
            # Add project root to path
            if str(self.project_path) not in sys.path:
                sys.path.insert(0, str(self.project_path))
            
            from src.waft.templates.academic_paper import generate_academic_paper
            
            # Extract metadata
            metadata = self._extract_metadata_from_content(status_content)
            
            # Process markdown to HTML
            html_content = self._process_markdown_to_html(status_content, metadata)
            
            # Generate PDF
            self.console.print("[yellow]→[/yellow] Generating ArXiv-style project status PDF...")
            generated_path = generate_academic_paper(
                title=metadata.get("title", "Science-Bitch Project Status"),
                content=html_content,
                output_path=status_pdf,
                abstract=metadata.get("abstract", ""),
                authors=metadata.get("authors", [{"name": "WAFT Development Team"}]),
                affiliations=metadata.get("affiliations"),
                email=metadata.get("email"),
                conference="arXiv",
                year=metadata.get("year", str(datetime.now().year)),
                references=metadata.get("references")
            )
            
            if generated_path and generated_path.exists():
                size = generated_path.stat().st_size / 1024  # KB
                self.console.print(f"[green]✓[/green] Project status PDF generated: {generated_path}")
                self.console.print(f"[dim]   Size: {size:.1f} KB[/dim]")
                
                # Open PDF
                system = platform.system()
                if system == "Darwin":  # macOS
                    subprocess.run(["open", str(generated_path)], check=False)
                elif system == "Windows":
                    subprocess.run(["start", str(generated_path)], shell=True, check=False)
                else:  # Linux
                    subprocess.run(["xdg-open", str(generated_path)], check=False)
                
                # Print PDF (opt-in to prevent duplicate printing)
                # User can print manually with: lpr {generated_path}
                self.console.print(f"[dim]💡 To print: lpr {generated_path}[/dim]")
                
                return generated_path
        
        except Exception as e:
            self.console.print(f"[yellow]⚠️[/yellow]  PDF generation failed: {e}")
            self.console.print(f"[dim]Markdown saved: {status_md}[/dim]")
            import traceback
            self.console.print(f"[dim]{traceback.format_exc()}[/dim]")
            return status_md
        
        return status_md if status_md.exists() else None
    
    def _create_field_guide_content(self) -> str:
        """Create field guide content."""
        return f"""# Science-Bitch Field Guide

**Version**: 1.0  
**Date**: {datetime.now().strftime("%Y-%m-%d")}

---

## Overview

Science-Bitch is a command-line tool that implements the full scientific method workflow for hypothesis testing, experimentation, and evidence-based conclusions.

---

## Quick Start

```bash
# Run full interactive workflow
waft science-bitch

# Generate field guide (this document)
waft science-bitch --field-guide

# Generate project status report
waft science-bitch --report
```

---

## Scientific Method Workflow

### 1. Form Hypothesis

Create a testable hypothesis with:
- **Statement**: What you're testing
- **Prediction**: Expected outcome
- **Variables**: Independent, dependent, and control variables

### 2. Design Experiment

Design an experiment that:
- Tests your hypothesis
- Controls for confounding variables
- Collects measurable data

### 3. Capture Initial State (A)

Before running the experiment:
- Capture system state
- Record baseline measurements
- Document initial conditions

### 4. Run Experiment

Execute the experiment:
- Use controlled variables
- Collect data during execution
- Record all measurements

### 5. Collect Data (C)

During the experiment:
- Record all measurements
- Track dependent variables
- Note any observations

### 6. Capture Final State (B)

After the experiment:
- Capture final system state
- Compare with initial state
- Identify changes

### 7. Analyze Results

Analyze collected data:
- Verify or refute hypothesis
- Calculate confidence
- Draw conclusions

### 8. Generate Report

Create documentation:
- Experiment report
- Analysis results
- Recommendations

---

## Command Options

### `waft science-bitch`

Run full interactive workflow:
1. Form hypothesis interactively
2. Design experiment
3. Run experiment
4. Analyze results
5. Generate report

### `waft science-bitch --field-guide`

Generate this field guide as PDF.

### `waft science-bitch --report`

Generate project status report PDF.

---

## File Structure

```
_science/
├── README.md              # Overview and quick start
├── experiments/           # Experiment definitions
├── data/                  # Collected data (C)
├── reports/               # Generated reports
│   ├── field_guide.pdf    # This guide
│   ├── project_status.pdf # Status report
│   └── experiment_*.md    # Experiment reports
└── tools/                  # Helper utilities
```

---

## Integration

- **Scientific Method Tool**: Core functionality from `scientific_method_tool/`
- **PDF Generation**: Uses `waft.evolution.pdf_generator`
- **Work Effort**: Tracked in `WE-260112-az3z`
- **State Capture**: Automatic state snapshots
- **Data Collection**: Comprehensive data recording

---

## Best Practices

1. **Clear Hypotheses**: Make hypotheses specific and testable
2. **Control Variables**: Keep control variables constant
3. **Multiple Trials**: Run multiple experiments for reliability
4. **Document Everything**: Record all observations
5. **Analyze Thoroughly**: Don't skip the analysis step

---

## Troubleshooting

**Command not found**: Ensure you're in the project root and dependencies are installed.

**Import errors**: Run `uv pip install jinja2 weasyprint markdown`

**PDF generation fails**: Check that WeasyPrint is installed and working.

---

## Examples

See `scientific_method_tool/example_usage.py` for complete examples.

---

**For more information, see the work effort: WE-260112-az3z**

"""
    
    def _create_project_status_content(self) -> str:
        """Create project status content."""
        work_effort_path = self.project_path / "_work_efforts" / "WE-260112-az3z_science_bitch_command_full_scientific_method_cli"
        work_effort_index = work_effort_path / "WE-260112-az3z_index.md" if work_effort_path.exists() else None
        
        tickets = []
        if work_effort_index and work_effort_index.exists():
            content = work_effort_index.read_text()
            # Parse tickets from markdown table
            import re
            ticket_pattern = r'\| TKT-az3z-(\d+) \| (.+?) \| (\w+) \|'
            for match in re.finditer(ticket_pattern, content):
                tickets.append({
                    "id": f"TKT-az3z-{match.group(1)}",
                    "title": match.group(2),
                    "status": match.group(3)
                })
        
        completed = len([t for t in tickets if t["status"] == "completed"])
        total = len(tickets)
        
        return f"""# Science-Bitch Project Status

**Generated**: {datetime.now().isoformat()}  
**Work Effort**: WE-260112-az3z

---

## Project Goals

Create a comprehensive `/science-bitch` command that runs the full scientific method workflow:
- Hypothesis formation
- Experiment design
- State capture (A and B)
- Data collection (C)
- Analysis and reporting
- PDF generation for documentation

---

## Current Status

**Progress**: {completed}/{total} tickets completed ({completed/total*100 if total > 0 else 0:.0f}%)

### Completed ✅

- Created `_science/` folder structure
- Created `ScienceBitchManager` class
- Added `science-bitch` CLI command
- Created README and documentation structure

### In Progress 🚧

- Interactive hypothesis creation
- Experiment runner implementation
- PDF report generation
- Field guide PDF

### Planned 📋

- Tooling for experiment management
- End-to-end testing
- Enhanced error handling
- Additional documentation

---

## Existing Evidence

### Code Structure

- **Command**: `src/waft/core/science_bitch.py` - Main manager class
- **CLI**: `src/waft/main.py` - Command registration
- **Integration**: Uses `scientific_method_tool/` for core functionality
- **Storage**: `_science/` directory for experiments and data

### Documentation

- **README**: `_science/README.md` - Overview and quick start
- **Work Effort**: `WE-260112-az3z` - Tickets and progress tracking
- **Field Guide**: `_science/reports/field_guide.md` - Usage guide

### Tools

- **Scientific Method Tool**: Complete implementation in `scientific_method_tool/`
- **PDF Generator**: Available via `waft.evolution.pdf_generator`
- **State Capture**: Implemented in `scientific_method_tool/state_capture.py`
- **Data Collection**: Implemented in `scientific_method_tool/data_collection.py`

---

## Objectives & Actions

### Primary Objective

Build a fully functional, well-tooled, documented scientific method command with field guide PDF.

### Key Actions

1. **Complete Interactive Workflow** ✅
   - Form hypothesis interactively
   - Design experiments
   - Run experiments with state capture
   - Analyze results

2. **PDF Generation** 🚧
   - Field guide PDF
   - Project status PDF
   - Experiment report PDFs

3. **Tooling** 📋
   - Experiment management utilities
   - Data analysis helpers
   - Report generation scripts

4. **Documentation** ✅
   - README
   - Field guide
   - Work effort tracking

---

## Planned Next Steps

1. **Enhance Interactive Workflow**
   - Better variable input
   - Experiment function loading
   - Progress indicators

2. **Complete PDF Generation**
   - Fix PDF generation for field guide
   - Create project status PDF
   - Add experiment report PDFs

3. **Add Tooling**
   - Experiment list/status commands
   - Data visualization tools
   - Report templates

4. **Testing**
   - End-to-end workflow test
   - Error handling tests
   - Integration tests

5. **Documentation**
   - Complete field guide
   - Add examples
   - Troubleshooting guide

---

## Tickets

"""
        for ticket in tickets:
            status_emoji = {
                "completed": "✅",
                "in_progress": "🚧",
                "pending": "📋"
            }.get(ticket["status"], "❓")
            return f"""{status_emoji} **{ticket["id"]}**: {ticket["title"]} ({ticket["status"]})

"""
        
        return content + "\n---\n\n**For detailed ticket information, see the work effort index.**\n"

