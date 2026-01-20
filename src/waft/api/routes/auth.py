"""
Authentication endpoints for WAFT API.

Provides secure handshake and token management for local API access.
"""

from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from ..auth import get_or_create_token, verify_token

router = APIRouter()
security = HTTPBearer(auto_error=False)


class HandshakeRequest(BaseModel):
    """Handshake request model."""

    client_name: str | None = None
    client_version: str | None = None


class HandshakeResponse(BaseModel):
    """Handshake response model."""

    token: str
    api_version: str
    endpoints: dict
    message: str


class TokenVerifyResponse(BaseModel):
    """Token verification response."""

    valid: bool
    message: str


@router.post("/auth/handshake", response_model=HandshakeResponse)
async def handshake(request: Request, handshake_req: HandshakeRequest = HandshakeRequest()):
    """
    Perform secure handshake with API.

    Returns a token for authenticated requests.
    This is a one-time setup for local development.
    """
    project_path: Path = request.app.state.project_path

    # Generate or get existing token
    token = get_or_create_token(project_path)

    return HandshakeResponse(
        token=token,
        api_version="0.1.0",
        endpoints={
            "health": "/api/health",
            "projects": "/api/projects",
            "work_efforts": "/api/work-efforts",
            "state": "/api/state",
            "docs": "/docs",
        },
        message=f"Handshake successful. Use token for authenticated requests. Client: {handshake_req.client_name or 'Unknown'}",
    )


@router.get("/auth/verify", response_model=TokenVerifyResponse)
async def verify_token_endpoint(
    request: Request, credentials: HTTPAuthorizationCredentials | None = Depends(security)
):
    """
    Verify if a token is valid.
    """
    project_path: Path = request.app.state.project_path

    if not credentials:
        return TokenVerifyResponse(valid=False, message="No token provided")

    is_valid = verify_token(credentials, project_path)

    return TokenVerifyResponse(
        valid=is_valid, message="Token is valid" if is_valid else "Token is invalid"
    )


@router.get("/auth/info")
async def auth_info(request: Request):
    """
    Get authentication information (public endpoint).
    """
    return {
        "auth_required": False,  # For now, auth is optional
        "auth_type": "bearer_token",
        "handshake_endpoint": "/api/auth/handshake",
        "verify_endpoint": "/api/auth/verify",
    }
