#!/usr/bin/env python3
"""
Test Suite: KuasaTurbo Auth Layer (Phase XV)

Tests multi-tenant authentication with API keys and JWT tokens.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.auth import tenant_loader, auth_service
from kuasaturbo.auth.models import Tenant


def test_load_tenants():
    """Test loading tenants from JSON"""
    print("\n[TEST] Loading tenants...")
    
    tenants = tenant_loader.load_tenants()
    
    assert isinstance(tenants, dict), "Tenants must be a dict"
    assert len(tenants) > 0, "Should have at least one tenant"
    assert "default" in tenants, "Should have default tenant"
    assert "voltek" in tenants, "Should have voltek tenant"
    
    print(f"  ✓ Loaded {len(tenants)} tenants")
    print("✓ Tenant loading works")


def test_get_tenant_by_id():
    """Test getting tenant by ID"""
    print("\n[TEST] Getting tenant by ID...")
    
    tenant = tenant_loader.get_tenant_by_id("voltek")
    
    assert tenant is not None, "Tenant should exist"
    assert isinstance(tenant, Tenant), "Should return Tenant object"
    assert tenant.tenant_id == "voltek"
    assert tenant.name == "Voltek Energy"
    assert "admin" in tenant.roles
    
    print(f"  ✓ Found tenant: {tenant.name}")
    print("✓ Get tenant by ID works")


def test_get_tenant_by_api_key_valid():
    """Test getting tenant by valid API key"""
    print("\n[TEST] Getting tenant by valid API key...")
    
    tenant = tenant_loader.get_tenant_by_api_key("VTK_DEV_KEY")
    
    assert tenant is not None, "Tenant should exist"
    assert tenant.tenant_id == "voltek"
    assert "VTK_DEV_KEY" in tenant.api_keys
    
    print(f"  ✓ API key matched tenant: {tenant.tenant_id}")
    print("✓ Get tenant by API key works")


def test_get_tenant_by_api_key_invalid():
    """Test getting tenant by invalid API key"""
    print("\n[TEST] Getting tenant by invalid API key...")
    
    tenant = tenant_loader.get_tenant_by_api_key("INVALID_KEY_XYZ")
    
    assert tenant is None, "Should return None for invalid key"
    
    print("  ✓ Invalid API key rejected")
    print("✓ Invalid API key handling works")


def test_validate_tenant_status():
    """Test tenant status validation"""
    print("\n[TEST] Validating tenant status...")
    
    # Active tenant
    active_tenant = tenant_loader.get_tenant_by_id("voltek")
    assert tenant_loader.validate_tenant_status(active_tenant) is True
    print("  ✓ Active tenant validated")
    
    # Inactive tenant
    inactive_tenant = tenant_loader.get_tenant_by_id("demo")
    assert tenant_loader.validate_tenant_status(inactive_tenant) is False
    print("  ✓ Inactive tenant rejected")
    
    print("✓ Tenant status validation works")


def test_validate_tenant_role():
    """Test tenant role validation"""
    print("\n[TEST] Validating tenant roles...")
    
    tenant = tenant_loader.get_tenant_by_id("voltek")
    
    # Valid roles
    assert tenant_loader.validate_tenant_role(tenant, "admin") is True
    assert tenant_loader.validate_tenant_role(tenant, "agent") is True
    print("  ✓ Valid roles accepted")
    
    # Invalid role
    assert tenant_loader.validate_tenant_role(tenant, "superuser") is False
    print("  ✓ Invalid role rejected")
    
    print("✓ Tenant role validation works")


def test_validate_api_key_success():
    """Test API key validation (success)"""
    print("\n[TEST] Validating API key (success)...")
    
    tenant = auth_service.validate_api_key("VTK_DEV_KEY")
    
    assert tenant is not None, "Should return tenant"
    assert tenant.tenant_id == "voltek"
    assert tenant.status == "active"
    
    print(f"  ✓ API key validated for tenant: {tenant.tenant_id}")
    print("✓ API key validation works")


def test_validate_api_key_failure():
    """Test API key validation (failure)"""
    print("\n[TEST] Validating API key (failure)...")
    
    tenant = auth_service.validate_api_key("INVALID_KEY")
    
    assert tenant is None, "Should return None for invalid key"
    
    print("  ✓ Invalid API key rejected")
    print("✓ API key rejection works")


def test_validate_api_key_inactive_tenant():
    """Test API key validation for inactive tenant"""
    print("\n[TEST] Validating API key (inactive tenant)...")
    
    tenant = auth_service.validate_api_key("DEMO_KEY")
    
    assert tenant is None, "Should return None for inactive tenant"
    
    print("  ✓ Inactive tenant API key rejected")
    print("✓ Inactive tenant handling works")


def test_generate_jwt_token_success():
    """Test JWT token generation (success)"""
    print("\n[TEST] Generating JWT token (success)...")
    
    token = auth_service.generate_jwt_token(
        tenant_id="voltek",
        user_id="test_user",
        role="admin",
        expires_in=3600
    )
    
    assert token is not None, "Should generate token"
    assert isinstance(token, str), "Token should be string"
    assert token.count('.') == 2, "JWT should have 3 parts"
    
    print(f"  ✓ JWT token generated: {token[:50]}...")
    print("✓ JWT token generation works")


def test_generate_jwt_token_invalid_tenant():
    """Test JWT token generation (invalid tenant)"""
    print("\n[TEST] Generating JWT token (invalid tenant)...")
    
    token = auth_service.generate_jwt_token(
        tenant_id="nonexistent",
        user_id="test_user",
        role="admin"
    )
    
    assert token is None, "Should return None for invalid tenant"
    
    print("  ✓ Invalid tenant rejected")
    print("✓ Invalid tenant handling works")


def test_generate_jwt_token_invalid_role():
    """Test JWT token generation (invalid role)"""
    print("\n[TEST] Generating JWT token (invalid role)...")
    
    token = auth_service.generate_jwt_token(
        tenant_id="voltek",
        user_id="test_user",
        role="superuser"  # Not in voltek's roles
    )
    
    assert token is None, "Should return None for invalid role"
    
    print("  ✓ Invalid role rejected")
    print("✓ Invalid role handling works")


def test_validate_jwt_token_success():
    """Test JWT token validation (success)"""
    print("\n[TEST] Validating JWT token (success)...")
    
    # Generate token
    token = auth_service.generate_jwt_token(
        tenant_id="voltek",
        user_id="test_user",
        role="admin"
    )
    
    # Validate token
    payload = auth_service.validate_jwt_token(token)
    
    assert payload is not None, "Should return payload"
    assert payload["tenant_id"] == "voltek"
    assert payload["user_id"] == "test_user"
    assert payload["role"] == "admin"
    
    print(f"  ✓ JWT token validated: tenant={payload['tenant_id']}, role={payload['role']}")
    print("✓ JWT token validation works")


def test_validate_jwt_token_invalid():
    """Test JWT token validation (invalid token)"""
    print("\n[TEST] Validating JWT token (invalid)...")
    
    payload = auth_service.validate_jwt_token("invalid.token.here")
    
    assert payload is None, "Should return None for invalid token"
    
    print("  ✓ Invalid JWT token rejected")
    print("✓ Invalid token handling works")


def test_check_role_permission():
    """Test role permission checking"""
    print("\n[TEST] Checking role permissions...")
    
    # Admin should have all permissions
    assert auth_service.check_role_permission("admin", "admin") is True
    assert auth_service.check_role_permission("admin", "agent") is True
    assert auth_service.check_role_permission("admin", "readonly") is True
    print("  ✓ Admin has all permissions")
    
    # Agent should not have admin permissions
    assert auth_service.check_role_permission("agent", "admin") is False
    assert auth_service.check_role_permission("agent", "agent") is True
    print("  ✓ Agent permissions correct")
    
    # Readonly should have limited permissions
    assert auth_service.check_role_permission("readonly", "admin") is False
    assert auth_service.check_role_permission("readonly", "readonly") is True
    print("  ✓ Readonly permissions correct")
    
    print("✓ Role permission checking works")


def test_get_tenant_context():
    """Test getting tenant context from API key"""
    print("\n[TEST] Getting tenant context...")
    
    context = auth_service.get_tenant_context("VTK_DEV_KEY")
    
    assert context is not None, "Should return context"
    assert context["tenant_id"] == "voltek"
    assert context["tenant_name"] == "Voltek Energy"
    assert "admin" in context["roles"]
    
    print(f"  ✓ Tenant context retrieved: {context['tenant_name']}")
    print("✓ Tenant context retrieval works")


def test_cross_tenant_isolation():
    """Test cross-tenant isolation (critical security test)"""
    print("\n[TEST] Testing cross-tenant isolation...")
    
    # Get two different tenants
    voltek_tenant = auth_service.validate_api_key("VTK_DEV_KEY")
    acme_tenant = auth_service.validate_api_key("ACME_API_KEY")
    
    assert voltek_tenant.tenant_id != acme_tenant.tenant_id
    print("  ✓ Different tenants have different IDs")
    
    # Generate tokens for each
    voltek_token = auth_service.generate_jwt_token(
        tenant_id="voltek",
        user_id="user1",
        role="admin"
    )
    
    acme_token = auth_service.generate_jwt_token(
        tenant_id="acme",
        user_id="user1",
        role="admin"
    )
    
    assert voltek_token != acme_token
    print("  ✓ Different tenants have different tokens")
    
    # Validate tokens
    voltek_payload = auth_service.validate_jwt_token(voltek_token)
    acme_payload = auth_service.validate_jwt_token(acme_token)
    
    assert voltek_payload["tenant_id"] == "voltek"
    assert acme_payload["tenant_id"] == "acme"
    print("  ✓ Tokens correctly identify their tenants")
    
    print("✓ Cross-tenant isolation verified")


def run_all_tests():
    """Run all auth layer tests"""
    print("=" * 60)
    print("KUASATURBO AUTH LAYER TEST SUITE (PHASE XV)")
    print("=" * 60)
    
    tests = [
        test_load_tenants,
        test_get_tenant_by_id,
        test_get_tenant_by_api_key_valid,
        test_get_tenant_by_api_key_invalid,
        test_validate_tenant_status,
        test_validate_tenant_role,
        test_validate_api_key_success,
        test_validate_api_key_failure,
        test_validate_api_key_inactive_tenant,
        test_generate_jwt_token_success,
        test_generate_jwt_token_invalid_tenant,
        test_generate_jwt_token_invalid_role,
        test_validate_jwt_token_success,
        test_validate_jwt_token_invalid,
        test_check_role_permission,
        test_get_tenant_context,
        test_cross_tenant_isolation
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n✗ {test.__name__} FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
