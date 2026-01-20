"""
Evolve UI Monitor API routes - Track and monitor /evolve-a-ui command executions.
"""

from fastapi import APIRouter, Request, HTTPException, status
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import re
import logging

from ...utils import _validate_path_in_storage

logger = logging.getLogger(__name__)

router = APIRouter()

# Sensitive file patterns to exclude
SENSITIVE_PATTERNS = [
    re.compile(r'\.env$', re.IGNORECASE),
    re.compile(r'\.key$', re.IGNORECASE),
    re.compile(r'\.pem$', re.IGNORECASE),
    re.compile(r'secrets?\.', re.IGNORECASE),
    re.compile(r'\.secret$', re.IGNORECASE),
    re.compile(r'\.token$', re.IGNORECASE),
]

# Excluded directories
EXCLUDED_DIRS = {'node_modules', '.git', '__pycache__', '.venv', 'venv', '.env'}

# Timestamp pattern: YYYYMMDD_HHMMSS
TIMESTAMP_PATTERN = re.compile(r'(\d{8}_\d{6})')


class Artifacts(BaseModel):
    """Artifacts for a run."""
    html: List[str] = []
    context_analysis: Optional[str] = None
    design_doc: Optional[str] = None
    requirements: Optional[str] = None
    wireframe: Optional[str] = None
    screenshots: List[str] = []
    case_files: List[str] = []


class EvolveUIRun(BaseModel):
    """Evolve UI run data."""
    run_id: str
    timestamp: str
    phase: str
    artifacts: Artifacts
    context: Optional[str] = None


class EvolveUIRunsResponse(BaseModel):
    """Response model for evolve UI runs."""
    runs: List[EvolveUIRun]
    total: int


def is_sensitive_file(filename: str) -> bool:
    """Check if file matches sensitive patterns."""
    return any(pattern.search(filename) for pattern in SENSITIVE_PATTERNS)


def validate_timestamp(timestamp: str) -> bool:
    """Validate timestamp format and reasonable date."""
    if not TIMESTAMP_PATTERN.match(timestamp):
        return False
    
    try:
        year = int(timestamp[:4])
        month = int(timestamp[4:6])
        day = int(timestamp[6:8])
        
        # Reasonable date check
        if year < 2020 or year > 2030:
            return False
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        
        # Not in future
        date = datetime(year, month, day, 
                       int(timestamp[9:11]), int(timestamp[11:13]), int(timestamp[13:15]))
        if date > datetime.now():
            return False
        
        return True
    except (ValueError, IndexError):
        return False


def determine_phase(artifacts: Artifacts) -> str:
    """Determine phase from artifacts."""
    if artifacts.html:
        return "Complete"
    if len(artifacts.screenshots) > 1:
        return "Development"
    if artifacts.wireframe:
        return "Wireframe"
    if artifacts.requirements:
        return "Requirements"
    if artifacts.design_doc:
        return "Analysis"
    return "Unknown"


def scan_ui_evolution_directory(project_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Scan _genetics/ui_evolution/ for evolve-a-ui runs.
    
    Returns dict mapping run_id to run data.
    """
    ui_evolution_dir = project_path / "_genetics" / "ui_evolution"
    work_efforts_dir = project_path / "_work_efforts"
    proof_cases_dir = work_efforts_dir / "proof_cases"
    
    runs: Dict[str, Dict[str, Any]] = {}
    
    if not ui_evolution_dir.exists():
        logger.warning(f"UI evolution directory not found: {ui_evolution_dir}")
        return runs
    
    try:
        # Scan for HTML files matching pattern
        for file_path in ui_evolution_dir.iterdir():
            if not file_path.is_file():
                continue
            
            filename = file_path.name
            
            # Skip sensitive files
            if is_sensitive_file(filename):
                continue
            
            # Extract timestamp from filename
            match = TIMESTAMP_PATTERN.search(filename)
            if not match:
                continue
            
            timestamp = match.group(1)
            if not validate_timestamp(timestamp):
                logger.warning(f"Invalid timestamp in filename: {filename}")
                continue
            
            # Validate path
            try:
                relative_path = file_path.relative_to(project_path)
                if not _validate_path_in_storage(relative_path, project_path):
                    logger.warning(f"Invalid path: {relative_path}")
                    continue
            except ValueError:
                logger.warning(f"Path not relative to project: {file_path}")
                continue
            
            # Initialize run if not exists
            if timestamp not in runs:
                runs[timestamp] = {
                    'run_id': timestamp,
                    'timestamp': timestamp,
                    'artifacts': {
                        'html': [],
                        'context_analysis': None,
                        'design_doc': None,
                        'requirements': None,
                        'wireframe': None,
                        'screenshots': [],
                        'case_files': [],
                    },
                    'context': None,
                }
            
            # Categorize file
            if filename.endswith('_evolved_ui.html') or filename.endswith('_evolved_dashboard.html'):
                runs[timestamp]['artifacts']['html'].append(str(relative_path))
            elif filename.endswith('_context_analysis.md'):
                runs[timestamp]['artifacts']['context_analysis'] = str(relative_path)
                # Try to read context summary
                try:
                    content = file_path.read_text(encoding='utf-8')[:500]
                    runs[timestamp]['context'] = content
                except (IOError, PermissionError, UnicodeDecodeError) as e:
                    logger.warning(f"Could not read context analysis: {e}")
    
    except (PermissionError, OSError) as e:
        logger.error(f"Error scanning UI evolution directory: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error scanning directory: {str(e)}"
        )
    
    # Scan work_efforts for related files
    if work_efforts_dir.exists():
        try:
            for file_path in work_efforts_dir.iterdir():
                if not file_path.is_file():
                    continue
                
                filename = file_path.name
                
                # Skip sensitive files
                if is_sensitive_file(filename):
                    continue
                
                # Extract timestamp
                match = TIMESTAMP_PATTERN.search(filename)
                if not match:
                    continue
                
                timestamp = match.group(1)
                if timestamp not in runs:
                    continue
                
                # Validate path
                try:
                    relative_path = file_path.relative_to(project_path)
                    if not _validate_path_in_storage(relative_path, project_path):
                        continue
                except ValueError:
                    continue
                
                # Categorize file
                if 'ui_design_doc' in filename.lower() and filename.endswith('.md'):
                    runs[timestamp]['artifacts']['design_doc'] = str(relative_path)
                elif 'ui_requirements' in filename.lower() or 'ui_technical_requirements' in filename.lower():
                    if filename.endswith('.md'):
                        runs[timestamp]['artifacts']['requirements'] = str(relative_path)
                elif 'wireframe' in filename.lower() and filename.endswith('.png'):
                    runs[timestamp]['artifacts']['wireframe'] = str(relative_path)
                elif filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    runs[timestamp]['artifacts']['screenshots'].append(str(relative_path))
        
        except (PermissionError, OSError) as e:
            logger.warning(f"Error scanning work_efforts: {e}")
    
    # Scan proof_cases for case files
    if proof_cases_dir.exists():
        try:
            for file_path in proof_cases_dir.iterdir():
                if not file_path.is_file():
                    continue
                
                filename = file_path.name
                
                # Skip sensitive files
                if is_sensitive_file(filename):
                    continue
                
                # Extract timestamp
                match = TIMESTAMP_PATTERN.search(filename)
                if not match:
                    continue
                
                timestamp = match.group(1)
                if timestamp not in runs:
                    continue
                
                # Validate path
                try:
                    relative_path = file_path.relative_to(project_path)
                    if not _validate_path_in_storage(relative_path, project_path):
                        continue
                except ValueError:
                    continue
                
                if filename.startswith('case_') and filename.endswith('.md'):
                    runs[timestamp]['artifacts']['case_files'].append(str(relative_path))
        
        except (PermissionError, OSError) as e:
            logger.warning(f"Error scanning proof_cases: {e}")
    
    # Determine phase for each run
    for run_id, run_data in runs.items():
        artifacts = Artifacts(**run_data['artifacts'])
        run_data['phase'] = determine_phase(artifacts)
    
    return runs


@router.get("/evolve-ui-runs", response_model=EvolveUIRunsResponse)
async def get_evolve_ui_runs(request: Request):
    """
    Get all evolve-a-ui runs.
    
    Scans _genetics/ui_evolution/ and _work_efforts/ for runs and artifacts.
    """
    project_path: Path = request.app.state.project_path
    
    try:
        runs_dict = scan_ui_evolution_directory(project_path)
        
        # Convert to response models
        runs_list = []
        for run_id, run_data in sorted(runs_dict.items(), reverse=True):
            artifacts = Artifacts(**run_data['artifacts'])
            run = EvolveUIRun(
                run_id=run_data['run_id'],
                timestamp=run_data['timestamp'],
                phase=run_data['phase'],
                artifacts=artifacts,
                context=run_data.get('context')
            )
            runs_list.append(run)
        
        return EvolveUIRunsResponse(runs=runs_list, total=len(runs_list))
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting evolve UI runs: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving runs: {str(e)}"
        )