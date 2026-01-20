"""
Final Report Generator

Generates comprehensive final report PDFs using the Science Textbook LaTeX template.
Integrates WAFT lore and philosophy for meaningful, useful documentation.
"""

import platform
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


class FinalReportGenerator:
    """
    Generates final reports using the Science Textbook LaTeX template.

    WAFT Philosophy: "Don't just build agents. Breed them."
    This report documents the evolution of the system, capturing knowledge
    for the scientific mission: "The Physics of Artificial Cognition."
    """

    def __init__(self, project_path: Path):
        """Initialize final report generator."""
        self.project_path = Path(project_path)
        self.template_path = self.project_path / "_science_textbook" / "stb-template.tex"
        self.output_dir = self.project_path / "_work_efforts"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def gather_session_data(self) -> dict[str, Any]:
        """
        Gather comprehensive session data with WAFT context.

        Returns:
            Dictionary with all session data
        """
        data = {
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "project_path": str(self.project_path),
            "project_name": self.project_path.name,
        }

        # Git information
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-15", "--decorate"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                commits = result.stdout.strip().split("\n")
                data["recent_commits"] = commits
                data["commit_count"] = len(commits)
        except:
            pass

        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                status_lines = result.stdout.strip().split("\n")
                data["git_status"] = [s for s in status_lines if s.strip()]
                data["modified_files"] = len([s for s in status_lines if s.startswith("M")])
                data["new_files"] = len(
                    [s for s in status_lines if s.startswith("??") or s.startswith("A")]
                )
        except:
            pass

        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                data["git_branch"] = result.stdout.strip()
        except:
            pass

        # Check for checkpoints
        checkpoint_files = list(self.output_dir.glob("CHECKPOINT_*.md"))
        data["checkpoints"] = []
        for f in sorted(checkpoint_files, reverse=True)[:5]:
            checkpoint_data = {"name": f.name, "path": str(f)}
            try:
                content = f.read_text()[:500]  # First 500 chars
                # Extract summary if available
                if "## Summary" in content:
                    summary_match = re.search(
                        r"## Summary\s*\n\n(.*?)(?=\n##|\Z)", content, re.DOTALL
                    )
                    if summary_match:
                        checkpoint_data["summary"] = summary_match.group(1).strip()[:200]
            except:
                pass
            data["checkpoints"].append(checkpoint_data)

        # Check for assumption validations
        validation_files = list(self.output_dir.glob("ASSUMPTIONS_VALIDATION_*.md"))
        data["assumption_validations"] = []
        for f in sorted(validation_files, reverse=True)[:5]:
            validation_data = {"name": f.name}
            try:
                content = f.read_text()
                # Count assumptions
                assumption_count = len(re.findall(r"### Assumption \d+", content))
                validation_data["assumption_count"] = assumption_count
            except:
                pass
            data["assumption_validations"].append(validation_data)

        # Check for work efforts
        work_effort_dirs = [
            d for d in self.output_dir.iterdir() if d.is_dir() and d.name.startswith("WE-")
        ]
        data["work_efforts"] = []
        for d in sorted(work_effort_dirs, key=lambda x: x.stat().st_mtime, reverse=True)[:10]:
            we_data = {"name": d.name}
            # Try to read index file
            index_file = d / f"{d.name}_index.md"
            if not index_file.exists():
                index_file = d / "index.md"
            if index_file.exists():
                try:
                    content = index_file.read_text()[:1000]
                    # Extract status
                    status_match = re.search(r"\*\*Status\*\*:\s*(\w+)", content)
                    if status_match:
                        we_data["status"] = status_match.group(1)
                    # Extract objective
                    obj_match = re.search(
                        r"\*\*Objective\*\*:\s*\n\n(.*?)(?=\n\n|\Z)", content, re.DOTALL
                    )
                    if obj_match:
                        we_data["objective"] = obj_match.group(1).strip()[:150]
                except:
                    pass
            data["work_efforts"].append(we_data)

        # Check devlog
        devlog_path = self.output_dir / "devlog.md"
        if devlog_path.exists():
            devlog_content = devlog_path.read_text()
            # Extract recent entries with better parsing
            lines = devlog_content.split("\n")
            recent_entries = []
            current_entry = []
            for line in lines:
                if line.startswith("## ") and " - " in line:
                    if current_entry:
                        recent_entries.append("\n".join(current_entry))
                    current_entry = [line]
                elif current_entry:
                    current_entry.append(line)
            if current_entry:
                recent_entries.append("\n".join(current_entry))

            data["devlog_entries"] = []
            for entry in recent_entries[:5]:
                entry_data = {"content": entry[:500]}
                # Extract title
                title_match = re.search(r"^## (.+?)(?:\s+-|$)", entry, re.MULTILINE)
                if title_match:
                    entry_data["title"] = title_match.group(1).strip()
                # Extract status
                status_match = re.search(r"\*\*Status\*\*:\s*([^\n]+)", entry)
                if status_match:
                    entry_data["status"] = status_match.group(1).strip()
                data["devlog_entries"].append(entry_data)

        # Calculate summary metrics
        data["metrics"] = {
            "checkpoints_count": len(data.get("checkpoints", [])),
            "validations_count": len(data.get("assumption_validations", [])),
            "work_efforts_count": len(data.get("work_efforts", [])),
            "commits_count": data.get("commit_count", 0),
            "modified_files": data.get("modified_files", 0),
            "new_files": data.get("new_files", 0),
        }

        return data

    def format_latex_content(
        self, data: dict[str, Any], title: str = "Final Report", subtitle: str | None = None
    ) -> str:
        """
        Format data into LaTeX content with WAFT lore integration.

        Args:
            data: Session data dictionary
            title: Report title
            subtitle: Optional subtitle

        Returns:
            LaTeX content string
        """
        if subtitle is None:
            subtitle = f"Session Report - {data.get('date', datetime.now().strftime('%Y-%m-%d'))}"

        # Read template
        if not self.template_path.exists():
            raise FileNotFoundError(f"Science Textbook template not found: {self.template_path}")

        template_content = self.template_path.read_text()

        # Replace title and metadata
        template_content = template_content.replace(
            r"\title{Science Textbook}", f"\\title{{{self._escape_latex(title)}}}"
        )
        template_content = template_content.replace(
            r"\newcommand{\booksubtitle}{A Latex Template for a Science Textbook}",
            f"\\newcommand{{\\booksubtitle}}{{{self._escape_latex(subtitle)}}}",
        )
        template_content = template_content.replace(
            r"\author{Author Name}", r"\author{WAFT Development System}"
        )
        template_content = template_content.replace(
            r"\newcommand{\authorsubtitle}{City, Country}",
            r"\newcommand{\authorsubtitle}{Wave Agent Framework \& Tools}",
        )

        # Find where mainmatter starts
        mainmatter_pos = template_content.find(r"\mainmatter")
        if mainmatter_pos == -1:
            raise ValueError("Template missing \\mainmatter")

        # Find where backmatter starts (end of main content)
        backmatter_pos = template_content.find(r"\backmatter")
        if backmatter_pos == -1:
            # If no backmatter, find end of document
            backmatter_pos = template_content.find(r"\end{document}")
            if backmatter_pos == -1:
                raise ValueError("Template missing \\end{document}")

        # Replace preface with WAFT-specific preface
        preface_start = template_content.find(r"\chapter*{Preface}")
        if preface_start != -1:
            preface_end = template_content.find(r"\tableofcontents", preface_start)
            if preface_end != -1:
                waft_preface = self._generate_waft_preface(data)
                template_content = (
                    template_content[:preface_start] + waft_preface + template_content[preface_end:]
                )

        # Generate report content
        report_content = self._generate_report_chapters(data)

        # Replace everything between \mainmatter and \backmatter with our content
        template_content = (
            template_content[: mainmatter_pos + len(r"\mainmatter")]
            + "\n"
            + report_content
            + "\n"
            + template_content[backmatter_pos:]
        )

        return template_content

    def _generate_waft_preface(self, data: dict[str, Any]) -> str:
        """Generate WAFT-specific preface with lore and context."""
        return (
            r"""
\chapter*{Preface}

This report documents a development session within the \textbf{Wave Agent Framework \& Tools} (WAFT), a scientific instrument for studying the physics of artificial cognition through directed evolution of self-modifying AI agents.

\section*{The WAFT Mission}

WAFT's tagline is: \textit{``Don't just build agents. Breed them.''} The framework serves a scientific mission to produce data for future research on \textit{``The Physics of Artificial Cognition.''} Every development session contributes to this mission by evolving the system's capabilities, documenting decisions, and capturing knowledge for the phylogenetic record.

\section*{What This Report Contains}

This document captures:
\begin{itemize}
\item \textbf{Session Evolution}: What was built, modified, and learned
\item \textbf{Work Progress}: Active work efforts and their status
\item \textbf{Technical Decisions}: Architecture choices and implementation details
\item \textbf{Assumption Validation}: Evidence-based verification of critical assumptions
\item \textbf{Documentation Artifacts}: Checkpoints, devlog entries, and verification traces
\item \textbf{Next Steps}: Recommendations for continued evolution
\end{itemize}

\section*{Session Context}

This session occurred on \textbf{"""
            + data.get("date", "unknown date")
            + r"""} took place in the \texttt{"""
            + self._escape_latex(data.get("project_name", "waft"))
            + r"""} project. The system recorded """
            + str(data.get("metrics", {}).get("commits_count", 0))
            + r""" commits, """
            + str(data.get("metrics", {}).get("work_efforts_count", 0))
            + r""" work efforts, and """
            + str(data.get("metrics", {}).get("checkpoints_count", 0))
            + r""" checkpoints during this period.

\section*{The Scientific Record}

Every session contributes to WAFT's evolutionary record. This report serves as a knowledge artifact, preserving the context, decisions, and outcomes of this development cycle for future analysis and system evolution.

\vspace{\fill}

\textit{Generated by WAFT Development System}\\
\textit{Part of the scientific mission: ``The Physics of Artificial Cognition''}
"""
        )

    def _generate_report_chapters(self, data: dict[str, Any]) -> str:
        """Generate LaTeX chapters from data."""
        chapters = []

        # Chapter 1: Executive Summary
        chapters.append(r"\chapter{Executive Summary}")
        chapters.append(self._format_executive_summary(data))

        # Chapter 2: Session Recap
        chapters.append(r"\chapter{Session Recap}")
        chapters.append(self._format_session_recap(data))

        # Chapter 3: Work Progress
        chapters.append(r"\chapter{Work Progress}")
        chapters.append(self._format_work_progress(data))

        # Chapter 4: Technical Details
        chapters.append(r"\chapter{Technical Details}")
        chapters.append(self._format_technical_details(data))

        # Chapter 5: Assumptions \& Validation
        chapters.append(r"\chapter{Assumptions \& Validation}")
        chapters.append(self._format_assumptions(data))

        # Chapter 6: Documentation
        chapters.append(r"\chapter{Documentation}")
        chapters.append(self._format_documentation(data))

        # Chapter 7: Next Steps
        chapters.append(r"\chapter{Next Steps \& Recommendations}")
        chapters.append(self._format_next_steps(data))

        return "\n\n".join(chapters)

    def _format_executive_summary(self, data: dict[str, Any]) -> str:
        """Format executive summary chapter with metrics."""
        content = [
            r"\section{Session Overview}",
            f"This report documents the development session on {data.get('date', 'unknown date')} at {data.get('time', 'unknown time')}.",
            "",
            r"\section{Key Metrics}",
            r"\begin{itemize}",
            f"\\item \\textbf{{Commits}}: {data.get('metrics', {}).get('commits_count', 0)}",
            f"\\item \\textbf{{Work Efforts}}: {data.get('metrics', {}).get('work_efforts_count', 0)}",
            f"\\item \\textbf{{Checkpoints}}: {data.get('metrics', {}).get('checkpoints_count', 0)}",
            f"\\item \\textbf{{Assumption Validations}}: {data.get('metrics', {}).get('validations_count', 0)}",
            f"\\item \\textbf{{Files Modified}}: {data.get('metrics', {}).get('modified_files', 0)}",
            f"\\item \\textbf{{New Files}}: {data.get('metrics', {}).get('new_files', 0)}",
            r"\end{itemize}",
            "",
        ]

        if data.get("recent_commits"):
            content.extend(
                [
                    r"\section{Key Accomplishments}",
                    r"Recent commits indicate the following work:",
                    r"\begin{itemize}",
                ]
            )
            for commit in data["recent_commits"][:8]:
                commit_msg = commit.split(" ", 1)[1] if " " in commit else commit
                # Clean up commit message
                commit_msg = commit_msg.split("(")[0].strip()  # Remove branch info
                content.append(f"\\item {self._escape_latex(commit_msg)}")
            content.append(r"\end{itemize}")

        return "\n".join(content)

    def _format_session_recap(self, data: dict[str, Any]) -> str:
        """Format session recap chapter."""
        content = [
            r"\section{Session Information}",
            r"\begin{description}",
            f"\\item[Date] {data.get('date', 'unknown')}",
            f"\\item[Time] {data.get('time', 'unknown')}",
            f"\\item[Project] {self._escape_latex(data.get('project_name', 'waft'))}",
            f"\\item[Path] \\texttt{{{self._escape_latex(str(data.get('project_path', '')))}}}",
        ]

        if data.get("git_branch"):
            content.append(f"\\item[Branch] {self._escape_latex(data.get('git_branch'))}")

        content.extend(
            [
                r"\end{description}",
                "",
            ]
        )

        if data.get("checkpoints"):
            content.extend(
                [
                    r"\section{Checkpoints Created}",
                    r"Checkpoints serve as snapshots of progress and decision points:",
                    r"\begin{itemize}",
                ]
            )
            for checkpoint in data["checkpoints"]:
                checkpoint_name = checkpoint.get("name", "Unknown")
                summary = checkpoint.get("summary", "")
                if summary:
                    content.append(
                        f"\\item \\textbf{{{self._escape_latex(checkpoint_name)}}}: {self._escape_latex(summary)}"
                    )
                else:
                    content.append(f"\\item {self._escape_latex(checkpoint_name)}")
            content.append(r"\end{itemize}")

        return "\n".join(content)

    def _format_work_progress(self, data: dict[str, Any]) -> str:
        """Format work progress chapter."""
        content = [
            r"\section{Active Work Efforts}",
        ]

        if data.get("work_efforts"):
            content.append(r"\begin{description}")
            for we in data["work_efforts"]:
                we_name = we.get("name", "Unknown")
                status = we.get("status", "Unknown")
                objective = we.get("objective", "")

                item = f"\\item[\\textbf{{{self._escape_latex(we_name)}}}]"
                item += f" Status: \\textit{{{self._escape_latex(status)}}}"
                if objective:
                    item += f"\\\\ {self._escape_latex(objective)}"
                content.append(item)
            content.append(r"\end{description}")
        else:
            content.append("No active work efforts found.")

        if data.get("git_status"):
            content.extend(
                [
                    "",
                    r"\section{Current Git Status}",
                    r"The following files have been modified or are untracked:",
                    r"\begin{verbatim}",
                ]
            )
            content.extend(data["git_status"][:25])  # Limit to 25 lines
            content.append(r"\end{verbatim}")

        return "\n".join(content)

    def _format_technical_details(self, data: dict[str, Any]) -> str:
        """Format technical details chapter."""
        content = [
            r"\section{Implementation Summary}",
            "This section documents technical implementation details and architecture decisions made during this session.",
            "",
        ]

        if data.get("recent_commits"):
            content.extend(
                [
                    r"\section{Recent Commits}",
                    r"The following commits were made during this session:",
                    r"\begin{itemize}",
                ]
            )
            for commit in data["recent_commits"][:12]:
                commit_msg = commit.split(" ", 1)[1] if " " in commit else commit
                commit_msg = commit_msg.split("(")[0].strip()
                content.append(f"\\item {self._escape_latex(commit_msg)}")
            content.append(r"\end{itemize}")

        return "\n".join(content)

    def _format_assumptions(self, data: dict[str, Any]) -> str:
        """Format assumptions chapter."""
        content = [
            r"\section{Assumption Validation Reports}",
            "Assumption validation ensures evidence-based decision making. The following validation reports were created:",
            "",
        ]

        if data.get("assumption_validations"):
            content.append(r"\begin{description}")
            for validation in data["assumption_validations"]:
                val_name = validation.get("name", "Unknown")
                count = validation.get("assumption_count", 0)
                item = f"\\item[\\textbf{{{self._escape_latex(val_name)}}}]"
                if count > 0:
                    item += f" {count} assumptions validated"
                content.append(item)
            content.append(r"\end{description}")
        else:
            content.append("No assumption validation reports found.")

        return "\n".join(content)

    def _format_documentation(self, data: dict[str, Any]) -> str:
        """Format documentation chapter."""
        content = [
            r"\section{Documentation Artifacts}",
            "This session generated the following documentation artifacts:",
            "",
        ]

        if data.get("checkpoints"):
            content.extend(
                [
                    r"\subsection{Checkpoints}",
                    r"Checkpoints provide decision snapshots:",
                    r"\begin{itemize}",
                ]
            )
            for checkpoint in data["checkpoints"]:
                checkpoint_name = checkpoint.get("name", "Unknown")
                content.append(f"\\item {self._escape_latex(checkpoint_name)}")
            content.append(r"\end{itemize}")

        if data.get("devlog_entries"):
            content.extend(
                [
                    "",
                    r"\subsection{Recent Devlog Entries}",
                    r"The development log records key activities:",
                    r"\begin{description}",
                ]
            )
            for entry in data["devlog_entries"][:5]:
                title = entry.get("title", "Unknown Entry")
                status = entry.get("status", "")
                item = f"\\item[\\textbf{{{self._escape_latex(title)}}}]"
                if status:
                    item += f" Status: \\textit{{{self._escape_latex(status)}}}"
                content.append(item)
            content.append(r"\end{description}")

        return "\n".join(content)

    def _format_next_steps(self, data: dict[str, Any]) -> str:
        """Format next steps chapter."""
        content = [
            r"\section{Immediate Actions}",
            "Based on the work completed in this session, the following immediate actions are recommended:",
            "",
            r"\begin{itemize}",
            r"\item Review and integrate completed work efforts",
            r"\item Address any pending assumption validations",
            r"\item Continue development on active work efforts",
            r"\item Update documentation as needed",
            r"\end{itemize}",
            "",
            r"\section{Future Considerations}",
            "For continued evolution of the WAFT system:",
            "",
            r"\begin{itemize}",
            r"\item Monitor system health and epistemic coverage",
            r"\item Track fitness metrics and evolutionary progress",
            r"\item Document patterns and insights for the scientific record",
            r"\item Continue building toward the mission: ``The Physics of Artificial Cognition''",
            r"\end{itemize}",
        ]

        return "\n".join(content)

    def _escape_latex(self, text: str) -> str:
        """Escape LaTeX special characters."""
        if not text:
            return ""
        replacements = {
            "\\": r"\textbackslash{}",
            "{": r"\{",
            "}": r"\}",
            "$": r"\$",
            "&": r"\&",
            "%": r"\%",
            "#": r"\#",
            "^": r"\textasciicircum{}",
            "_": r"\_",
            "~": r"\textasciitilde{}",
        }
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        return text

    def generate_report(
        self,
        title: str = "Final Report",
        subtitle: str | None = None,
        output_name: str | None = None,
    ) -> Path:
        """
        Generate final report PDF.

        Args:
            title: Report title
            subtitle: Optional subtitle
            output_name: Optional output filename (without extension)

        Returns:
            Path to generated PDF
        """
        # Gather data
        print("📊 Gathering session data...")
        data = self.gather_session_data()

        # Format LaTeX
        print("📝 Formatting LaTeX content...")
        latex_content = self.format_latex_content(data, title, subtitle)

        # Generate output name
        if output_name is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            safe_title = "".join(
                c if c.isalnum() or c in ("-", "_") else "_" for c in title.lower()
            )
            output_name = f"FINAL_REPORT_{timestamp}_{safe_title}"

        tex_file = self.output_dir / f"{output_name}.tex"
        pdf_file = self.output_dir / f"{output_name}.pdf"

        # Write LaTeX file
        print(f"💾 Writing LaTeX file: {tex_file}")
        tex_file.write_text(latex_content, encoding="utf-8")

        # Copy index style file
        ist_file = self.template_path.parent / "stb-template.ist"
        if ist_file.exists():
            output_ist = self.output_dir / f"{output_name}.ist"
            import shutil

            shutil.copy(ist_file, output_ist)

        # Copy booksvg.pdf if it exists
        booksvg_file = self.template_path.parent / "booksvg.pdf"
        if booksvg_file.exists():
            import shutil

            shutil.copy(booksvg_file, self.output_dir / "booksvg.pdf")

        # Compile LaTeX
        print("🔨 Compiling LaTeX to PDF...")
        try:
            from ..templates.latex.compiler import LaTeXCompiler

            compiler = LaTeXCompiler(compiler="pdflatex")
            pdf_path = compiler.compile_file(
                tex_file,
                pdf_file,
                runs=2,  # Two runs for TOC
            )
        except (ImportError, RuntimeError) as e:
            # Fallback to direct pdflatex
            print(f"⚠️  Using fallback compilation method: {e}")
            result = subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-output-directory",
                    str(self.output_dir),
                    str(tex_file),
                ],
                cwd=str(self.output_dir),
                capture_output=True,
                text=True,
                timeout=60,
            )
            # Check if PDF was generated even if returncode != 0 (warnings are OK)
            if not pdf_file.exists() and result.returncode != 0:
                print(f"LaTeX output: {result.stdout}")
                print(f"LaTeX errors: {result.stderr}")
                raise RuntimeError(f"LaTeX compilation failed: {result.stderr or result.stdout}")

            # Second run for TOC
            subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-output-directory",
                    str(self.output_dir),
                    str(tex_file),
                ],
                cwd=str(self.output_dir),
                capture_output=True,
                text=True,
                timeout=60,
            )

            if not pdf_file.exists():
                raise RuntimeError("PDF not generated")
            pdf_path = pdf_file

        print(f"✅ PDF generated: {pdf_path}")

        # Open PDF
        print("📖 Opening PDF in default viewer...")
        self._open_pdf(pdf_path)

        return pdf_path

    def _open_pdf(self, pdf_path: Path):
        """Open PDF in default viewer."""
        try:
            if platform.system() == "Darwin":  # macOS
                subprocess.run(["open", str(pdf_path)], check=True)
            elif platform.system() == "Windows":
                subprocess.run(["start", str(pdf_path)], shell=True, check=True)
            else:  # Linux
                subprocess.run(["xdg-open", str(pdf_path)], check=True)
        except subprocess.CalledProcessError:
            print(f"⚠️  Could not automatically open PDF. Please open manually: {pdf_path}")
        except Exception as e:
            print(f"⚠️  Error opening PDF: {e}")
            print(f"   PDF location: {pdf_path}")
