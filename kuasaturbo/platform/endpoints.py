"""
Platform Layer API Endpoints (Phase XIX)

Provides REST API for API key management and platform administration.
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional, List

from .api_keys import APIKeyManager, APIKeyScopes
from kuasaturbo.auth.auth_service import validate_api_key


# Create router
platform_router = APIRouter(prefix="/v1/admin", tags=["platform"])


# ============================================================
# REQUEST/RESPONSE MODELS
# ============================================================

class APIKeyCreate(BaseModel):
    scopes: List[str] = Field(..., description="List of scopes: read, write, execute, admin")
    metadata: Optional[dict] = None


class APIKeyRotate(BaseModel):
    key_id: str = Field(..., description="Key ID to rotate")


class APIKeyRevoke(BaseModel):
    key_id: str = Field(..., description="Key ID to revoke")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def require_admin_scope(x_api_key: str) -> dict:
    """
    Validate API key and require admin scope
    
    Args:
        x_api_key: API key from header
    
    Returns:
        Tenant context dict
    
    Raises:
        HTTPException: If authentication or authorization fails
    """
    # Validate tenant
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Validate key and check admin scope
    key_data = APIKeyManager.validate_key(x_api_key)
    if not key_data:
        raise HTTPException(status_code=401, detail="Invalid or expired API key")
    
    if not APIKeyManager.check_scope(key_data, APIKeyScopes.ADMIN.value):
        raise HTTPException(
            status_code=403,
            detail="Admin scope required for platform operations"
        )
    
    return {
        "tenant_id": tenant.tenant_id,
        "tenant_name": tenant.name,
        "key_id": key_data['key_id']
    }


# ============================================================
# API KEY ENDPOINTS
# ============================================================

@platform_router.post("/api-keys")
async def create_api_key(
    data: APIKeyCreate,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Create new API key
    
    Requires: admin scope
    """
    context = require_admin_scope(x_api_key)
    
    # Validate scopes
    valid_scopes = [s.value for s in APIKeyScopes]
    for scope in data.scopes:
        if scope not in valid_scopes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid scope: {scope}. Valid scopes: {valid_scopes}"
            )
    
    # Create key
    api_key = APIKeyManager.create_api_key(
        tenant_id=context['tenant_id'],
        scopes=data.scopes,
        metadata=data.metadata
    )
    
    # Get key details
    key_data = APIKeyManager.get_key_by_api_key(api_key)
    
    return {
        "key_id": key_data['key_id'],
        "api_key": api_key,
        "scopes": key_data['scopes'],
        "status": "created",
        "tenant_id": context['tenant_id']
    }


@platform_router.get("/api-keys")
async def list_api_keys(
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    List API keys for tenant
    
    Requires: admin scope
    """
    context = require_admin_scope(x_api_key)
    
    keys = APIKeyManager.list_keys(
        tenant_id=context['tenant_id'],
        status=status,
        limit=limit,
        offset=offset
    )
    
    return {
        "keys": keys,
        "count": len(keys),
        "tenant_id": context['tenant_id']
    }


@platform_router.get("/api-keys/{key_id}")
async def get_api_key(
    key_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Get API key details
    
    Requires: admin scope
    """
    context = require_admin_scope(x_api_key)
    
    key_data = APIKeyManager.get_key_by_id(key_id)
    
    if not key_data:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Verify tenant ownership
    if key_data['tenant_id'] != context['tenant_id']:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Mask API key
    key_data['api_key'] = key_data['api_key'][:20] + '...' if len(key_data['api_key']) > 20 else key_data['api_key']
    
    return key_data


@platform_router.post("/api-keys/rotate")
async def rotate_api_key(
    data: APIKeyRotate,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Rotate API key (create new, mark old as rotated with grace period)
    
    Requires: admin scope
    """
    context = require_admin_scope(x_api_key)
    
    # Verify ownership
    key_data = APIKeyManager.get_key_by_id(data.key_id)
    if not key_data or key_data['tenant_id'] != context['tenant_id']:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Rotate key
    new_api_key = APIKeyManager.rotate_key(data.key_id)
    
    if not new_api_key:
        raise HTTPException(
            status_code=400,
            detail="Key rotation failed. Key may not be active."
        )
    
    # Get new key details
    new_key_data = APIKeyManager.get_key_by_api_key(new_api_key)
    
    return {
        "old_key_id": data.key_id,
        "new_key_id": new_key_data['key_id'],
        "new_api_key": new_api_key,
        "status": "rotated",
        "grace_period_minutes": APIKeyManager.GRACE_PERIOD_MINUTES,
        "message": f"Old key will remain valid for {APIKeyManager.GRACE_PERIOD_MINUTES} minutes"
    }


@platform_router.post("/api-keys/revoke")
async def revoke_api_key(
    data: APIKeyRevoke,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Revoke API key (permanent, cannot be reactivated)
    
    Requires: admin scope
    """
    context = require_admin_scope(x_api_key)
    
    # Verify ownership
    key_data = APIKeyManager.get_key_by_id(data.key_id)
    if not key_data or key_data['tenant_id'] != context['tenant_id']:
        raise HTTPException(status_code=404, detail="API key not found")
    
    # Prevent self-revocation
    if key_data['api_key'] == x_api_key:
        raise HTTPException(
            status_code=400,
            detail="Cannot revoke the API key currently in use"
        )
    
    # Revoke key
    success = APIKeyManager.revoke_key(data.key_id)
    
    if not success:
        raise HTTPException(
            status_code=400,
            detail="Key revocation failed. Key may already be revoked."
        )
    
    return {
        "key_id": data.key_id,
        "status": "revoked",
        "message": "API key has been permanently revoked"
    }
