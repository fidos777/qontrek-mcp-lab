"""
KuasaTurbo Auth Models

Data models for authentication layer.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class Tenant(BaseModel):
    """Tenant model"""
    tenant_id: str = Field(..., description="Unique tenant identifier")
    name: str = Field(..., description="Tenant display name")
    status: str = Field(..., description="Tenant status (active/inactive)")
    roles: List[str] = Field(..., description="Available roles for this tenant")
    api_keys: List[str] = Field(..., description="Valid API keys for this tenant")
    jwt_secret: str = Field(..., description="JWT signing secret for this tenant")


class TokenRequest(BaseModel):
    """Token generation request"""
    api_key: str = Field(..., description="Valid API key")
    user_id: str = Field(..., description="User identifier")
    role: str = Field(..., description="Requested role")


class TokenResponse(BaseModel):
    """Token generation response"""
    tenant_id: str = Field(..., description="Tenant identifier")
    user_id: str = Field(..., description="User identifier")
    role: str = Field(..., description="Assigned role")
    token: str = Field(..., description="JWT token")
    expires_in: int = Field(3600, description="Token expiry in seconds")


class TenantInfo(BaseModel):
    """Tenant information response"""
    tenant_id: str = Field(..., description="Tenant identifier")
    name: str = Field(..., description="Tenant name")
    status: str = Field(..., description="Tenant status")
    roles: List[str] = Field(..., description="Available roles")
