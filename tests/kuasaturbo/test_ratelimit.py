"""
Test Suite for Rate Limiting Layer (Phase XVI)

Tests rate limit configuration, counter management, window resets,
enforcement, and multi-tenant isolation.
"""

import json
import os
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

# Add parent directory to path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.ratelimit.models import RateLimitConfig, RateLimitUsage, RateLimitState, RateLimitStore
from kuasaturbo.ratelimit.ratelimit_loader import (
    load_config,
    load_state,
    save_state,
    get_or_create_usage,
    reset_if_new_window
)
from kuasaturbo.ratelimit.ratelimit_service import (
    check_rate_limit,
    increment_usage,
    reset_state_for_testing
)


class TestRateLimitModels(unittest.TestCase):
    """Test rate limit data models"""
    
    def test_rate_limit_config_creation(self):
        """Test RateLimitConfig model creation"""
        print("\n[Test] Creating RateLimitConfig")
        
        config = RateLimitConfig(minute=10, hour=100, day=1000)
        
        self.assertEqual(config.minute, 10)
        self.assertEqual(config.hour, 100)
        self.assertEqual(config.day, 1000)
        print("[Test] ✓ RateLimitConfig created successfully")
    
    def test_rate_limit_usage_creation(self):
        """Test RateLimitUsage model creation"""
        print("\n[Test] Creating RateLimitUsage")
        
        now = int(time.time())
        usage = RateLimitUsage(
            minute_count=5,
            hour_count=50,
            day_count=500,
            minute_reset_at=now + 60,
            hour_reset_at=now + 3600,
            day_reset_at=now + 86400
        )
        
        self.assertEqual(usage.minute_count, 5)
        self.assertEqual(usage.hour_count, 50)
        self.assertEqual(usage.day_count, 500)
        print("[Test] ✓ RateLimitUsage created successfully")
    
    def test_rate_limit_state_creation(self):
        """Test RateLimitState model creation"""
        print("\n[Test] Creating RateLimitState")
        
        now = int(time.time())
        usage = RateLimitUsage(
            minute_count=0,
            hour_count=0,
            day_count=0,
            minute_reset_at=now + 60,
            hour_reset_at=now + 3600,
            day_reset_at=now + 86400
        )
        
        state = RateLimitState(
            tenant_id="test_tenant",
            endpoint="test_endpoint",
            usage=usage
        )
        
        self.assertEqual(state.tenant_id, "test_tenant")
        self.assertEqual(state.endpoint, "test_endpoint")
        self.assertEqual(state.usage.minute_count, 0)
        print("[Test] ✓ RateLimitState created successfully")


class TestRateLimitLoader(unittest.TestCase):
    """Test rate limit configuration and state loading"""
    
    def test_load_default_config(self):
        """Test loading default configuration"""
        print("\n[Test] Loading default configuration")
        
        config = load_config()
        
        self.assertIn("default", config)
        self.assertIsInstance(config["default"], RateLimitConfig)
        self.assertGreater(config["default"].minute, 0)
        self.assertGreater(config["default"].hour, 0)
        self.assertGreater(config["default"].day, 0)
        print(f"[Test] ✓ Loaded config with {len(config)} endpoint configurations")
    
    def test_load_endpoint_specific_config(self):
        """Test loading endpoint-specific configuration"""
        print("\n[Test] Loading endpoint-specific configuration")
        
        config = load_config()
        
        self.assertIn("service_execute", config)
        self.assertIn("creative_generate", config)
        
        service_config = config["service_execute"]
        self.assertEqual(service_config.minute, 20)
        self.assertEqual(service_config.hour, 200)
        self.assertEqual(service_config.day, 2000)
        
        creative_config = config["creative_generate"]
        self.assertEqual(creative_config.minute, 10)
        self.assertEqual(creative_config.hour, 100)
        self.assertEqual(creative_config.day, 1000)
        
        print("[Test] ✓ Endpoint-specific configurations loaded correctly")
    
    def test_initialize_empty_state(self):
        """Test initializing empty rate limit state"""
        print("\n[Test] Initializing empty state")
        
        # Clean up any existing state file
        state_path = Path(__file__).parent.parent.parent / "kuasaturbo" / "ratelimit" / "ratelimit.json"
        if state_path.exists():
            state_path.unlink()
        
        store = load_state()
        
        self.assertIsInstance(store, RateLimitStore)
        self.assertEqual(len(store.states), 0)
        print("[Test] ✓ Empty state initialized successfully")
    
    def test_get_or_create_usage(self):
        """Test getting or creating usage counters"""
        print("\n[Test] Getting or creating usage counters")
        
        store = RateLimitStore(states={})
        usage = get_or_create_usage(store, "test_tenant", "test_endpoint")
        
        self.assertIsInstance(usage, RateLimitUsage)
        self.assertEqual(usage.minute_count, 0)
        self.assertEqual(usage.hour_count, 0)
        self.assertEqual(usage.day_count, 0)
        self.assertGreater(usage.minute_reset_at, 0)
        self.assertGreater(usage.hour_reset_at, 0)
        self.assertGreater(usage.day_reset_at, 0)
        
        # Verify state was stored
        key = store.get_key("test_tenant", "test_endpoint")
        self.assertIn(key, store.states)
        
        print("[Test] ✓ Usage counters created successfully")
    
    def test_save_and_load_state(self):
        """Test saving and loading state"""
        print("\n[Test] Saving and loading state")
        
        # Create test state
        store = RateLimitStore(states={})
        usage = get_or_create_usage(store, "test_tenant", "test_endpoint")
        usage.minute_count = 5
        usage.hour_count = 50
        usage.day_count = 500
        
        # Save state
        save_state(store)
        
        # Load state
        loaded_store = load_state()
        
        key = loaded_store.get_key("test_tenant", "test_endpoint")
        self.assertIn(key, loaded_store.states)
        
        loaded_usage = loaded_store.states[key].usage
        self.assertEqual(loaded_usage.minute_count, 5)
        self.assertEqual(loaded_usage.hour_count, 50)
        self.assertEqual(loaded_usage.day_count, 500)
        
        print("[Test] ✓ State saved and loaded successfully")


class TestWindowReset(unittest.TestCase):
    """Test time window reset logic"""
    
    def test_no_reset_needed(self):
        """Test that counters are not reset when windows are active"""
        print("\n[Test] Testing no reset needed")
        
        now = int(time.time())
        usage = RateLimitUsage(
            minute_count=5,
            hour_count=50,
            day_count=500,
            minute_reset_at=now + 30,  # 30 seconds in future
            hour_reset_at=now + 1800,  # 30 minutes in future
            day_reset_at=now + 43200   # 12 hours in future
        )
        
        updated_usage = reset_if_new_window(usage)
        
        # Counts should remain unchanged
        self.assertEqual(updated_usage.minute_count, 5)
        self.assertEqual(updated_usage.hour_count, 50)
        self.assertEqual(updated_usage.day_count, 500)
        
        print("[Test] ✓ No reset performed (windows still active)")
    
    def test_minute_window_reset(self):
        """Test minute window reset"""
        print("\n[Test] Testing minute window reset")
        
        now = int(time.time())
        usage = RateLimitUsage(
            minute_count=10,
            hour_count=50,
            day_count=500,
            minute_reset_at=now - 1,   # 1 second in past (expired)
            hour_reset_at=now + 1800,  # Still active
            day_reset_at=now + 43200   # Still active
        )
        
        updated_usage = reset_if_new_window(usage)
        
        # Minute count should be reset
        self.assertEqual(updated_usage.minute_count, 0)
        # Other counts should remain
        self.assertEqual(updated_usage.hour_count, 50)
        self.assertEqual(updated_usage.day_count, 500)
        # Reset time should be updated
        self.assertGreater(updated_usage.minute_reset_at, now)
        
        print("[Test] ✓ Minute window reset successfully")
    
    def test_hour_window_reset(self):
        """Test hour window reset"""
        print("\n[Test] Testing hour window reset")
        
        now = int(time.time())
        usage = RateLimitUsage(
            minute_count=5,
            hour_count=100,
            day_count=500,
            minute_reset_at=now + 30,
            hour_reset_at=now - 1,     # 1 second in past (expired)
            day_reset_at=now + 43200
        )
        
        updated_usage = reset_if_new_window(usage)
        
        # Hour count should be reset
        self.assertEqual(updated_usage.hour_count, 0)
        # Other counts should remain
        self.assertEqual(updated_usage.minute_count, 5)
        self.assertEqual(updated_usage.day_count, 500)
        # Reset time should be updated
        self.assertGreater(updated_usage.hour_reset_at, now)
        
        print("[Test] ✓ Hour window reset successfully")
    
    def test_day_window_reset(self):
        """Test day window reset"""
        print("\n[Test] Testing day window reset")
        
        now = int(time.time())
        usage = RateLimitUsage(
            minute_count=5,
            hour_count=50,
            day_count=1000,
            minute_reset_at=now + 30,
            hour_reset_at=now + 1800,
            day_reset_at=now - 1       # 1 second in past (expired)
        )
        
        updated_usage = reset_if_new_window(usage)
        
        # Day count should be reset
        self.assertEqual(updated_usage.day_count, 0)
        # Other counts should remain
        self.assertEqual(updated_usage.minute_count, 5)
        self.assertEqual(updated_usage.hour_count, 50)
        # Reset time should be updated
        self.assertGreater(updated_usage.day_reset_at, now)
        
        print("[Test] ✓ Day window reset successfully")


class TestRateLimitEnforcement(unittest.TestCase):
    """Test rate limit enforcement logic"""
    
    def setUp(self):
        """Reset state before each test"""
        reset_state_for_testing()
        
        # Clean up state file
        state_path = Path(__file__).parent.parent.parent / "kuasaturbo" / "ratelimit" / "ratelimit.json"
        if state_path.exists():
            state_path.unlink()
    
    def test_allow_request_within_limits(self):
        """Test that requests within limits are allowed"""
        print("\n[Test] Testing request within limits")
        
        allowed, window, limit, count = check_rate_limit("test_tenant", "default")
        
        self.assertTrue(allowed)
        self.assertIsNone(window)
        self.assertIsNone(limit)
        self.assertIsNone(count)
        
        print("[Test] ✓ Request allowed within limits")
    
    def test_exceed_minute_limit(self):
        """Test exceeding minute limit"""
        print("\n[Test] Testing minute limit exceeded")
        
        # Make requests up to the limit (default is 30/minute)
        for i in range(30):
            allowed, _, _, _ = check_rate_limit("test_tenant", "default")
            self.assertTrue(allowed, f"Request {i+1} should be allowed")
        
        # Next request should be blocked
        allowed, window, limit, count = check_rate_limit("test_tenant", "default")
        
        self.assertFalse(allowed)
        self.assertEqual(window, "minute")
        self.assertEqual(limit, 30)
        self.assertEqual(count, 30)
        
        print("[Test] ✓ Minute limit enforced correctly")
    
    def test_exceed_hour_limit(self):
        """Test exceeding hour limit (simulated)"""
        print("\n[Test] Testing hour limit exceeded")
        
        # Manually set hour count to limit
        store = load_state()
        usage = get_or_create_usage(store, "test_tenant_hour", "default")
        usage.hour_count = 500  # Default hour limit
        save_state(store)
        
        # Reset cache to pick up changes
        reset_state_for_testing()
        
        # Next request should be blocked
        allowed, window, limit, count = check_rate_limit("test_tenant_hour", "default")
        
        self.assertFalse(allowed)
        self.assertEqual(window, "hour")
        self.assertEqual(limit, 500)
        
        print("[Test] ✓ Hour limit enforced correctly")
    
    def test_exceed_day_limit(self):
        """Test exceeding day limit (simulated)"""
        print("\n[Test] Testing day limit exceeded")
        
        # Manually set day count to limit
        store = load_state()
        usage = get_or_create_usage(store, "test_tenant_day", "default")
        usage.day_count = 5000  # Default day limit
        save_state(store)
        
        # Reset cache to pick up changes
        reset_state_for_testing()
        
        # Next request should be blocked
        allowed, window, limit, count = check_rate_limit("test_tenant_day", "default")
        
        self.assertFalse(allowed)
        self.assertEqual(window, "day")
        self.assertEqual(limit, 5000)
        
        print("[Test] ✓ Day limit enforced correctly")
    
    def test_multi_tenant_isolation(self):
        """Test that tenants have independent rate limits"""
        print("\n[Test] Testing multi-tenant isolation")
        
        # Tenant A makes requests up to limit
        for i in range(30):
            allowed, _, _, _ = check_rate_limit("tenant_a", "default")
            self.assertTrue(allowed)
        
        # Tenant A should be blocked
        allowed_a, _, _, _ = check_rate_limit("tenant_a", "default")
        self.assertFalse(allowed_a)
        
        # Tenant B should still be allowed
        allowed_b, _, _, _ = check_rate_limit("tenant_b", "default")
        self.assertTrue(allowed_b)
        
        print("[Test] ✓ Multi-tenant isolation verified")
    
    def test_multi_endpoint_isolation(self):
        """Test that endpoints have independent rate limits"""
        print("\n[Test] Testing multi-endpoint isolation")
        
        # Make requests to service_execute (limit: 20/minute)
        for i in range(20):
            allowed, _, _, _ = check_rate_limit("test_tenant", "service_execute")
            self.assertTrue(allowed)
        
        # service_execute should be blocked
        allowed_service, _, _, _ = check_rate_limit("test_tenant", "service_execute")
        self.assertFalse(allowed_service)
        
        # creative_generate should still be allowed (different endpoint)
        allowed_creative, _, _, _ = check_rate_limit("test_tenant", "creative_generate")
        self.assertTrue(allowed_creative)
        
        print("[Test] ✓ Multi-endpoint isolation verified")
    
    def test_endpoint_specific_limits(self):
        """Test that endpoint-specific limits are applied"""
        print("\n[Test] Testing endpoint-specific limits")
        
        # creative_generate has limit of 10/minute
        for i in range(10):
            allowed, _, _, _ = check_rate_limit("test_tenant", "creative_generate")
            self.assertTrue(allowed, f"Request {i+1} should be allowed")
        
        # 11th request should be blocked
        allowed, window, limit, count = check_rate_limit("test_tenant", "creative_generate")
        
        self.assertFalse(allowed)
        self.assertEqual(window, "minute")
        self.assertEqual(limit, 10)
        
        print("[Test] ✓ Endpoint-specific limits applied correctly")


class TestRateLimitIntegration(unittest.TestCase):
    """Integration tests for rate limiting"""
    
    def setUp(self):
        """Reset state before each test"""
        reset_state_for_testing()
        
        # Clean up state file
        state_path = Path(__file__).parent.parent.parent / "kuasaturbo" / "ratelimit" / "ratelimit.json"
        if state_path.exists():
            state_path.unlink()
    
    def test_full_request_flow(self):
        """Test complete request flow with rate limiting"""
        print("\n[Test] Testing full request flow")
        
        tenant_id = "integration_test_tenant"
        endpoint = "service_execute"
        
        # Make several requests
        for i in range(5):
            allowed, _, _, _ = check_rate_limit(tenant_id, endpoint)
            self.assertTrue(allowed, f"Request {i+1} should be allowed")
        
        # Verify state was persisted
        store = load_state()
        key = store.get_key(tenant_id, endpoint)
        self.assertIn(key, store.states)
        
        state = store.states[key]
        self.assertEqual(state.tenant_id, tenant_id)
        self.assertEqual(state.endpoint, endpoint)
        self.assertEqual(state.usage.minute_count, 5)
        self.assertEqual(state.usage.hour_count, 5)
        self.assertEqual(state.usage.day_count, 5)
        
        print("[Test] ✓ Full request flow completed successfully")
    
    def test_concurrent_tenant_requests(self):
        """Test multiple tenants making requests simultaneously"""
        print("\n[Test] Testing concurrent tenant requests")
        
        tenants = ["tenant_1", "tenant_2", "tenant_3"]
        
        # Each tenant makes 5 requests
        for tenant in tenants:
            for i in range(5):
                allowed, _, _, _ = check_rate_limit(tenant, "default")
                self.assertTrue(allowed)
        
        # Verify each tenant has independent counters
        store = load_state()
        for tenant in tenants:
            key = store.get_key(tenant, "default")
            self.assertIn(key, store.states)
            self.assertEqual(store.states[key].usage.minute_count, 5)
        
        print("[Test] ✓ Concurrent tenant requests handled correctly")


def run_tests():
    """Run all rate limit tests"""
    print("\n" + "="*70)
    print("PHASE XVI - RATE LIMITING LAYER TEST SUITE")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimitModels))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimitLoader))
    suite.addTests(loader.loadTestsFromTestCase(TestWindowReset))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimitEnforcement))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimitIntegration))
    
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
