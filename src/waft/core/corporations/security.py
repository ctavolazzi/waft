"""
Security Utilities for Corporations System

Path validation, input sanitization, and secure file operations.
"""

import os
import re
from pathlib import Path
from typing import Optional
from decimal import Decimal, InvalidOperation


def validate_corp_id(corp_id: str) -> bool:
    """
    Validate corporation ID for security.
    
    CRITICAL: Rejects path traversal, null bytes, and invalid characters.
    
    Args:
        corp_id: Corporation ID to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not corp_id:
        return False
    
    # Reject path traversal
    if '..' in corp_id or '/' in corp_id or '\\' in corp_id:
        return False
    
    # Reject null bytes
    if '\x00' in corp_id:
        return False
    
    # Reject control characters
    if any(ord(c) < 32 and c not in '\t\n\r' for c in corp_id):
        return False
    
    # Only allow safe filename characters (alphanumeric, underscore, hyphen)
    if not re.match(r'^[a-zA-Z0-9_-]+$', corp_id):
        return False
    
    return True


def validate_path_in_project(path: Path, project_path: Path) -> bool:
    """
    Validate path is within project directory.
    
    CRITICAL: Security validation to prevent path traversal.
    
    Args:
        path: Path to validate
        project_path: Project root path
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Reject absolute paths outside project
        if path.is_absolute():
            # Check if absolute path is within project
            try:
                resolved = path.resolve()
                project_resolved = project_path.resolve()
                return str(resolved).startswith(str(project_resolved))
            except (OSError, RuntimeError):
                return False
        
        # Reject path traversal
        if '..' in path.parts:
            return False
        
        # Reject null bytes
        if '\x00' in str(path):
            return False
        
        # Resolve and check
        resolved = (project_path / path).resolve()
        project_resolved = project_path.resolve()
        
        # Check path is within project
        if not str(resolved).startswith(str(project_resolved)):
            return False
        
        return True
    except (OSError, ValueError, RuntimeError):
        return False


def validate_financial_amount(
    amount: Decimal,
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
    allow_negative: bool = False
) -> bool:
    """
    Validate financial amount.
    
    Args:
        amount: Amount to validate
        min_amount: Minimum allowed amount
        max_amount: Maximum allowed amount
        allow_negative: Whether negative amounts are allowed
        
    Returns:
        True if valid, False otherwise
    """
    try:
        # Convert to Decimal if not already
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        
        # Check for negative
        if not allow_negative and amount < 0:
            return False
        
        # Check minimum
        if min_amount is not None and amount < min_amount:
            return False
        
        # Check maximum
        if max_amount is not None and amount > max_amount:
            return False
        
        # Check for reasonable bounds (prevent overflow)
        max_reasonable = Decimal("1e12")  # $1 trillion
        if abs(amount) > max_reasonable:
            return False
        
        return True
    except (InvalidOperation, ValueError, TypeError):
        return False


def write_secure_file(path: Path, content: str, encoding: str = "utf-8") -> None:
    """
    Write file with secure permissions.
    
    Sets file permissions to 0o600 (read/write owner only).
    
    Args:
        path: File path
        content: File content
        encoding: File encoding
    """
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    path.write_text(content, encoding=encoding)
    
    # Set restrictive permissions (owner read/write only)
    try:
        os.chmod(path, 0o600)
    except OSError:
        # If chmod fails, log but don't fail (may be on Windows or permission issue)
        pass


def read_secure_json(path: Path, max_size: int = 10 * 1024 * 1024) -> dict:
    """
    Read JSON file with size limits and error handling.
    
    Args:
        path: JSON file path
        max_size: Maximum file size in bytes (default: 10MB)
        
    Returns:
        Parsed JSON data
        
    Raises:
        ValueError: If file too large or invalid JSON
        IOError: If file read fails
    """
    import json
    
    # Check file size
    if path.exists():
        file_size = path.stat().st_size
        if file_size > max_size:
            raise ValueError(f"File too large: {file_size} bytes (max: {max_size})")
    
    # Read file
    try:
        content = path.read_text(encoding="utf-8")
    except IOError as e:
        raise IOError(f"Failed to read file {path}: {e}")
    
    # Parse JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {path}: {e}")


def set_directory_permissions(path: Path) -> None:
    """
    Set secure directory permissions (0o700).
    
    Args:
        path: Directory path
    """
    try:
        os.chmod(path, 0o700)
    except OSError:
        # If chmod fails, log but don't fail
        pass
