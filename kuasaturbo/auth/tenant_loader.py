"""
KuasaTurbo Tenant Loader

Loads and manages tenant registry from mock JSON file.
"""

import json
import os
from typing import Dict, Optional
from pathlib import Path

from kuasaturbo.auth.models import Tenant


def get_tenants_file() -> Path:
    """Get path to tenants.json file"""
    return Path(__file__).parent / "tenants.json"


def load_tenants() -> Dict[str, Tenant]:
    """
    Load all tenants from tenants.json
    
    Returns:
        Dictionary of tenant_id -> Tenant objects
    """
    tenants_file = get_tenants_file()
    
    if not tenants_file.exists():
        raise FileNotFoundError(f"Tenants file not found: {tenants_file}")
    
    with open(tenants_file, 'r') as f:
        tenants_data = json.load(f)
    
    tenants = {}
    for tenant_id, tenant_dict in tenants_data.items():
        tenants[tenant_id] = Tenant(**tenant_dict)
    
    print(f"[TenantLoader] Loaded {len(tenants)} tenants")
    return tenants


def get_tenant_by_id(tenant_id: str) -> Optional[Tenant]:
    """
    Get tenant by tenant_id
    
    Args:
        tenant_id: Tenant identifier
    
    Returns:
        Tenant object or None if not found
    """
    tenants = load_tenants()
    return tenants.get(tenant_id)


def get_tenant_by_api_key(api_key: str) -> Optional[Tenant]:
    """
    Get tenant by API key
    
    Args:
        api_key: API key to lookup
    
    Returns:
        Tenant object or None if not found
    """
    tenants = load_tenants()
    
    for tenant in tenants.values():
        if api_key in tenant.api_keys:
            print(f"[TenantLoader] API key matched tenant: {tenant.tenant_id}")
            return tenant
    
    print(f"[TenantLoader] No tenant found for API key")
    return None


def validate_tenant_status(tenant: Tenant) -> bool:
    """
    Check if tenant is active
    
    Args:
        tenant: Tenant object
    
    Returns:
        True if tenant is active, False otherwise
    """
    return tenant.status == "active"


def validate_tenant_role(tenant: Tenant, role: str) -> bool:
    """
    Check if role is valid for tenant
    
    Args:
        tenant: Tenant object
        role: Role to validate
    
    Returns:
        True if role is valid for tenant, False otherwise
    """
    return role in tenant.roles


def get_all_tenants() -> Dict[str, Tenant]:
    """
    Get all tenants (for admin purposes)
    
    Returns:
        Dictionary of all tenants
    """
    return load_tenants()
