"""
Test Suite for Platform Layer (Phase XIX)

Tests API key lifecycle, scopes, rotation, and revocation.
"""

import os
import sys
import unittest
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.platform.api_keys import APIKeyManager, APIKeyScopes, APIKeyStatus
from kuasaturbo.database.connection import get_db_connection, init_database, DB_PATH


class TestAPIKeyManager(unittest.TestCase):
    """Test API key management"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize database"""
        from kuasaturbo.database.connection import close_connection
        
        # Close any existing connection
        close_connection()
        
        # Remove old database
        if DB_PATH.exists():
            DB_PATH.unlink()
        
        # Initialize fresh database
        init_database()
    
    def test_create_api_key(self):
        """Test API key creation"""
        print("\n[Test] Creating API key")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read", "write"]
        )
        
        self.assertIsNotNone(api_key)
        self.assertTrue(api_key.startswith("kuasa_"))
        
        # Verify key in database
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        self.assertIsNotNone(key_data)
        self.assertEqual(key_data['tenant_id'], "test_tenant_1")
        self.assertIn("read", key_data['scopes'])
        self.assertIn("write", key_data['scopes'])
        
        print(f"[Test] ✓ API key created: {key_data['key_id']}")
    
    def test_list_api_keys(self):
        """Test listing API keys"""
        print("\n[Test] Listing API keys")
        
        # Create multiple keys
        for i in range(3):
            APIKeyManager.create_api_key(
                tenant_id="test_tenant_2",
                scopes=["read"]
            )
        
        keys = APIKeyManager.list_keys("test_tenant_2")
        
        self.assertEqual(len(keys), 3)
        
        print(f"[Test] ✓ Listed {len(keys)} API keys")
    
    def test_get_api_key_details(self):
        """Test getting API key details"""
        print("\n[Test] Getting API key details")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["execute", "admin"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        
        self.assertIsNotNone(key_data)
        self.assertEqual(key_data['status'], APIKeyStatus.ACTIVE.value)
        self.assertIn("execute", key_data['scopes'])
        self.assertIn("admin", key_data['scopes'])
        
        print(f"[Test] ✓ Retrieved key details: {key_data['key_id']}")
    
    def test_rotate_api_key(self):
        """Test API key rotation"""
        print("\n[Test] Rotating API key")
        
        # Create original key
        old_api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read", "write", "execute"]
        )
        
        old_key_data = APIKeyManager.get_key_by_api_key(old_api_key)
        old_key_id = old_key_data['key_id']
        
        # Rotate key
        new_api_key = APIKeyManager.rotate_key(old_key_id)
        
        self.assertIsNotNone(new_api_key)
        self.assertNotEqual(old_api_key, new_api_key)
        
        # Verify old key is rotated
        old_key_data = APIKeyManager.get_key_by_id(old_key_id)
        self.assertEqual(old_key_data['status'], APIKeyStatus.ROTATED.value)
        
        # Verify new key is active
        new_key_data = APIKeyManager.get_key_by_api_key(new_api_key)
        self.assertEqual(new_key_data['status'], APIKeyStatus.ACTIVE.value)
        self.assertEqual(new_key_data['scopes'], old_key_data['scopes'])
        self.assertEqual(new_key_data['rotated_from'], old_key_id)
        
        print(f"[Test] ✓ Key rotated: {old_key_id} → {new_key_data['key_id']}")
    
    def test_revoke_api_key(self):
        """Test API key revocation"""
        print("\n[Test] Revoking API key")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        key_id = key_data['key_id']
        
        # Revoke key
        success = APIKeyManager.revoke_key(key_id)
        self.assertTrue(success)
        
        # Verify key is revoked
        key_data = APIKeyManager.get_key_by_id(key_id)
        self.assertEqual(key_data['status'], APIKeyStatus.REVOKED.value)
        self.assertIsNotNone(key_data['revoked_at'])
        
        print(f"[Test] ✓ Key revoked: {key_id}")
    
    def test_scope_read_allowed(self):
        """Test read scope allows GET operations"""
        print("\n[Test] Testing read scope (allowed)")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        
        # Check read scope
        has_read = APIKeyManager.check_scope(key_data, APIKeyScopes.READ.value)
        self.assertTrue(has_read)
        
        print(f"[Test] ✓ Read scope verified")
    
    def test_scope_read_denied_on_write(self):
        """Test read scope denies write operations"""
        print("\n[Test] Testing read scope (denied on write)")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        
        # Check write scope (should fail)
        has_write = APIKeyManager.check_scope(key_data, APIKeyScopes.WRITE.value)
        self.assertFalse(has_write)
        
        print(f"[Test] ✓ Write scope correctly denied")
    
    def test_scope_execute_allowed(self):
        """Test execute scope allows execution operations"""
        print("\n[Test] Testing execute scope (allowed)")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["execute"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        
        # Check execute scope
        has_execute = APIKeyManager.check_scope(key_data, APIKeyScopes.EXECUTE.value)
        self.assertTrue(has_execute)
        
        print(f"[Test] ✓ Execute scope verified")
    
    def test_scope_execute_denied_without_scope(self):
        """Test execute scope denied without proper scope"""
        print("\n[Test] Testing execute scope (denied)")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read", "write"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        
        # Check execute scope (should fail)
        has_execute = APIKeyManager.check_scope(key_data, APIKeyScopes.EXECUTE.value)
        self.assertFalse(has_execute)
        
        print(f"[Test] ✓ Execute scope correctly denied")
    
    def test_admin_scope_grants_all(self):
        """Test admin scope grants all permissions"""
        print("\n[Test] Testing admin scope (grants all)")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["admin"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        
        # Admin should grant all scopes
        self.assertTrue(APIKeyManager.check_scope(key_data, APIKeyScopes.READ.value))
        self.assertTrue(APIKeyManager.check_scope(key_data, APIKeyScopes.WRITE.value))
        self.assertTrue(APIKeyManager.check_scope(key_data, APIKeyScopes.EXECUTE.value))
        self.assertTrue(APIKeyManager.check_scope(key_data, APIKeyScopes.ADMIN.value))
        
        print(f"[Test] ✓ Admin scope grants all permissions")
    
    def test_multi_tenant_isolation(self):
        """Test multi-tenant isolation for API keys"""
        print("\n[Test] Testing multi-tenant isolation")
        
        # Create keys for different tenants
        key_a = APIKeyManager.create_api_key("tenant_a", ["read"])
        key_b = APIKeyManager.create_api_key("tenant_b", ["read"])
        
        # List keys for tenant_a
        keys_a = APIKeyManager.list_keys("tenant_a")
        
        # Should only see tenant_a's keys
        self.assertEqual(len(keys_a), 1)
        self.assertEqual(keys_a[0]['tenant_id'], "tenant_a")
        
        print(f"[Test] ✓ Tenant isolation verified")
    
    def test_revoked_key_cannot_access(self):
        """Test revoked key cannot access any endpoint"""
        print("\n[Test] Testing revoked key access")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read", "write", "execute", "admin"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        key_id = key_data['key_id']
        
        # Revoke key
        APIKeyManager.revoke_key(key_id)
        
        # Try to validate revoked key
        validated = APIKeyManager.validate_key(api_key)
        self.assertIsNone(validated)
        
        print(f"[Test] ✓ Revoked key access denied")
    
    def test_rotation_grace_period(self):
        """Test rotation grace period logic"""
        print("\n[Test] Testing rotation grace period")
        
        # Create and rotate key
        old_api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read"]
        )
        
        old_key_data = APIKeyManager.get_key_by_api_key(old_api_key)
        old_key_id = old_key_data['key_id']
        
        new_api_key = APIKeyManager.rotate_key(old_key_id)
        
        # Old key should still validate (within grace period)
        validated = APIKeyManager.validate_key(old_api_key)
        self.assertIsNotNone(validated)
        self.assertEqual(validated['status'], APIKeyStatus.ROTATED.value)
        
        # New key should also validate
        validated_new = APIKeyManager.validate_key(new_api_key)
        self.assertIsNotNone(validated_new)
        self.assertEqual(validated_new['status'], APIKeyStatus.ACTIVE.value)
        
        print(f"[Test] ✓ Grace period logic verified")
    
    def test_validate_key_updates_last_used(self):
        """Test that validation updates last_used_at"""
        print("\n[Test] Testing last_used_at update")
        
        api_key = APIKeyManager.create_api_key(
            tenant_id="test_tenant_1",
            scopes=["read"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        self.assertIsNone(key_data['last_used_at'])
        
        # Validate key (should update last_used_at)
        APIKeyManager.validate_key(api_key)
        
        # Check last_used_at is now set
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        self.assertIsNotNone(key_data['last_used_at'])
        
        print(f"[Test] ✓ last_used_at updated on validation")


def run_tests():
    """Run all platform layer tests"""
    print("\n" + "="*70)
    print("PHASE XIX - PLATFORM LAYER TEST SUITE")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test class
    suite.addTests(loader.loadTestsFromTestCase(TestAPIKeyManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
