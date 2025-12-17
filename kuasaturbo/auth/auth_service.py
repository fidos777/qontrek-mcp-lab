"""
KuasaTurbo Auth Service

Authentication and authorization services.
Supports API key validation and JWT token generation/validation.
"""

import json
import base64
import hmac
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from kuasaturbo.auth.tenant_loader import (
    get_tenant_by_api_key,
    get_tenant_by_id,
    validate_tenant_status,
    validate_tenant_role
)
from kuasaturbo.auth.models import Tenant


def validate_api_key(api_key: str) -> Optional[Tenant]:
    """
    Validate API key and return tenant
    
    Args:
        api_key: API key to validate
    
    Returns:
        Tenant object if valid, None otherwise
    """
    print(f"[AuthService] Validating API key")
    
    tenant = get_tenant_by_api_key(api_key)
    
    if not tenant:
        print(f"[AuthService] Invalid API key")
        return None
    
    if not validate_tenant_status(tenant):
        print(f"[AuthService] Tenant inactive: {tenant.tenant_id}")
        return None
    
    print(f"[AuthService] API key valid for tenant: {tenant.tenant_id}")
    return tenant


def generate_jwt_token(
    tenant_id: str,
    user_id: str,
    role: str,
    expires_in: int = 3600
) -> Optional[str]:
    """
    Generate JWT token (mock implementation)
    
    Args:
        tenant_id: Tenant identifier
        user_id: User identifier
        role: User role
        expires_in: Token expiry in seconds
    
    Returns:
        JWT token string or None if invalid
    """
    print(f"[AuthService] Generating JWT token for tenant: {tenant_id}")
    
    tenant = get_tenant_by_id(tenant_id)
    
    if not tenant:
        print(f"[AuthService] Tenant not found: {tenant_id}")
        return None
    
    if not validate_tenant_role(tenant, role):
        print(f"[AuthService] Invalid role for tenant: {role}")
        return None
    
    # Create JWT payload
    now = datetime.utcnow()
    exp = now + timedelta(seconds=expires_in)
    
    payload = {
        "tenant_id": tenant_id,
        "user_id": user_id,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp())
    }
    
    # Mock JWT signing (simplified for demo)
    # In production, use PyJWT library
    header = {"alg": "HS256", "typ": "JWT"}
    
    header_b64 = base64.urlsafe_b64encode(
        json.dumps(header).encode()
    ).decode().rstrip('=')
    
    payload_b64 = base64.urlsafe_b64encode(
        json.dumps(payload).encode()
    ).decode().rstrip('=')
    
    # Sign with tenant secret
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        tenant.jwt_secret.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    
    token = f"{header_b64}.{payload_b64}.{signature_b64}"
    
    print(f"[AuthService] JWT token generated successfully")
    return token


def validate_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate JWT token and return payload
    
    Args:
        token: JWT token string
    
    Returns:
        Token payload dict or None if invalid
    """
    print(f"[AuthService] Validating JWT token")
    
    try:
        # Split token
        parts = token.split('.')
        if len(parts) != 3:
            print(f"[AuthService] Invalid token format")
            return None
        
        header_b64, payload_b64, signature_b64 = parts
        
        # Decode payload
        # Add padding if needed
        payload_b64_padded = payload_b64 + '=' * (4 - len(payload_b64) % 4)
        payload_json = base64.urlsafe_b64decode(payload_b64_padded).decode()
        payload = json.loads(payload_json)
        
        # Check expiry
        now = int(datetime.utcnow().timestamp())
        if payload.get('exp', 0) < now:
            print(f"[AuthService] Token expired")
            return None
        
        # Get tenant
        tenant_id = payload.get('tenant_id')
        tenant = get_tenant_by_id(tenant_id)
        
        if not tenant:
            print(f"[AuthService] Tenant not found: {tenant_id}")
            return None
        
        # Verify signature
        message = f"{header_b64}.{payload_b64}"
        expected_signature = hmac.new(
            tenant.jwt_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
        
        expected_signature_b64 = base64.urlsafe_b64encode(
            expected_signature
        ).decode().rstrip('=')
        
        if signature_b64 != expected_signature_b64:
            print(f"[AuthService] Invalid token signature")
            return None
        
        print(f"[AuthService] JWT token valid for tenant: {tenant_id}")
        return payload
        
    except Exception as e:
        print(f"[AuthService] Token validation error: {str(e)}")
        return None


def check_role_permission(role: str, required_role: str) -> bool:
    """
    Check if role has required permission (mock hierarchy)
    
    Args:
        role: User's role
        required_role: Required role for action
    
    Returns:
        True if permission granted, False otherwise
    """
    # Simple role hierarchy (mock)
    role_hierarchy = {
        "admin": 3,
        "creator": 2,
        "agent": 2,
        "readonly": 1
    }
    
    user_level = role_hierarchy.get(role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level


def get_tenant_context(api_key: str) -> Optional[Dict[str, Any]]:
    """
    Get tenant context from API key
    
    Args:
        api_key: API key
    
    Returns:
        Tenant context dict or None
    """
    tenant = validate_api_key(api_key)
    
    if not tenant:
        return None
    
    return {
        "tenant_id": tenant.tenant_id,
        "tenant_name": tenant.name,
        "status": tenant.status,
        "roles": tenant.roles
    }
