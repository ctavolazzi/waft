"""
Custom API exceptions.
"""

from fastapi import HTTPException, status


class ProjectNotFoundError(HTTPException):
    """Exception raised when project is not found."""
    def __init__(self, project_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found: {project_id}"
        )


class WorkEffortNotFoundError(HTTPException):
    """Exception raised when work effort is not found."""
    def __init__(self, work_effort_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Work effort not found: {work_effort_id}"
        )


class ValidationError(HTTPException):
    """Exception raised for validation errors."""
    def __init__(self, message: str, detail: dict = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail or {"message": message}
        )


class ConflictError(HTTPException):
    """Exception raised for conflict errors (e.g., duplicate IDs)."""
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message
        )
