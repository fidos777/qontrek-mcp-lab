"""
Integration Smoke Tests (Phase XX-Lite)

VALIDATION-ONLY: Confirms all layers cooperate correctly.
No new features, no schema changes, no new endpoints.
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.platform.api_keys import APIKeyManager, APIKeyScopes
from kuasaturbo.resources.wallets import WalletManager
from kuasaturbo.resources.transactions import TransactionManager, TransactionStatus
from kuasaturbo.resources.execution_history import ExecutionHistoryManager
from kuasaturbo.resources.idempotency import IdempotencyManager
from kuasaturbo.business.consultants import ConsultantManager
from kuasaturbo.business.resellers import ResellerManager
from kuasaturbo.business.partners import PartnerManager
from kuasaturbo.logging.audit import AuditLogger
from kuasaturbo.logging.logger import generate_execution_id, generate_request_id
from kuasaturbo.database.connection import get_db_connection, init_database, DB_PATH, close_connection


class TestIntegrationFlows(unittest.TestCase):
    """Integration smoke tests for launch readiness"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize database"""
        close_connection()
        if DB_PATH.exists():
            DB_PATH.unlink()
        init_database()
    
    def test_full_execution_flow(self):
        """Test complete execution flow: API key → wallet → execution → audit"""
        print("\n[Integration] Testing full execution flow")
        
        # 1. Create API key with execute scope
        api_key = APIKeyManager.create_api_key(
            tenant_id="integration_tenant_1",
            scopes=["execute"]
        )
        key_data = APIKeyManager.validate_key(api_key)
        self.assertIsNotNone(key_data)
        
        # 2. Create wallet and add credits
        WalletManager.create_wallet("integration_tenant_1", 100.0)
        balance_before = WalletManager.get_balance("integration_tenant_1")
        self.assertEqual(balance_before, 100.0)
        
        # 3. Simulate service execution
        exec_id = generate_execution_id()
        tx_id = TransactionManager.create_transaction(
            tenant_id="integration_tenant_1",
            execution_id=exec_id,
            amount=10.0,
            service_id="lead_intake"
        )
        
        # 4. Execute transaction state machine
        TransactionManager.update_status(tx_id, TransactionStatus.EXECUTING)
        
        # Deduct credits
        success = WalletManager.safe_decrement("integration_tenant_1", 10.0, tx_id)
        self.assertTrue(success)
        
        # Complete transaction
        TransactionManager.update_status(tx_id, TransactionStatus.COMPLETED)
        
        # 5. Log execution history
        ExecutionHistoryManager.log_execution(
            execution_id=exec_id,
            tenant_id="integration_tenant_1",
            transaction_id=tx_id,
            service_id="lead_intake",
            status="COMPLETED",
            duration_ms=150.0
        )
        
        # 6. Verify credits deducted ONCE
        balance_after = WalletManager.get_balance("integration_tenant_1")
        self.assertEqual(balance_after, 90.0)
        
        # 7. Verify transaction created
        tx = TransactionManager.get_transaction(tx_id)
        self.assertEqual(tx['status'], TransactionStatus.COMPLETED.value)
        self.assertEqual(tx['amount'], 10.0)
        
        # 8. Verify execution history
        history = ExecutionHistoryManager.get_execution_history(exec_id)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['status'], "COMPLETED")
        
        print("[Integration] ✓ Full execution flow validated")
    
    def test_full_creative_flow(self):
        """Test creative generation flow with credits"""
        print("\n[Integration] Testing creative generation flow")
        
        # 1. Create API key
        api_key = APIKeyManager.create_api_key(
            tenant_id="integration_tenant_2",
            scopes=["execute"]
        )
        
        # 2. Create wallet
        WalletManager.create_wallet("integration_tenant_2", 50.0)
        
        # 3. Simulate creative generation
        exec_id = generate_execution_id()
        tx_id = TransactionManager.create_transaction(
            tenant_id="integration_tenant_2",
            execution_id=exec_id,
            amount=5.0,
            service_id="creative_thumbnail"
        )
        
        # Execute
        TransactionManager.update_status(tx_id, TransactionStatus.EXECUTING)
        WalletManager.safe_decrement("integration_tenant_2", 5.0, tx_id)
        TransactionManager.update_status(tx_id, TransactionStatus.COMPLETED)
        
        # Log
        ExecutionHistoryManager.log_execution(
            execution_id=exec_id,
            tenant_id="integration_tenant_2",
            transaction_id=tx_id,
            service_id="creative_thumbnail",
            status="COMPLETED"
        )
        
        # Verify
        balance = WalletManager.get_balance("integration_tenant_2")
        self.assertEqual(balance, 45.0)
        
        print("[Integration] ✓ Creative flow validated")
    
    def test_consultant_sale_flow(self):
        """Test consultant commission calculation"""
        print("\n[Integration] Testing consultant sale flow")
        
        # Create consultant with 15% commission
        consultant_id = ConsultantManager.create_consultant(
            tenant_id="integration_tenant_3",
            name="Test Consultant",
            email="consultant@test.com",
            commission_rate=15.0
        )
        
        # Record 2 sales
        ConsultantManager.record_sale(consultant_id, 1000.0)  # $150 commission
        ConsultantManager.record_sale(consultant_id, 500.0)   # $75 commission
        
        # Verify earnings
        summary = ConsultantManager.get_earnings_summary(consultant_id)
        self.assertEqual(summary['total_sales'], 2)
        self.assertEqual(summary['total_earnings'], 225.0)  # 15% of 1500
        self.assertEqual(summary['commission_rate'], 15.0)
        
        print("[Integration] ✓ Consultant flow validated")
    
    def test_reseller_credit_flow(self):
        """Test reseller tier-based commission"""
        print("\n[Integration] Testing reseller credit flow")
        
        # Create gold tier reseller (15% commission)
        reseller_id = ResellerManager.create_reseller(
            tenant_id="integration_tenant_4",
            company_name="Gold Reseller Inc",
            contact_name="Test Contact",
            email="reseller@test.com",
            tier="gold"
        )
        
        # Record sale
        ResellerManager.record_sale(reseller_id, 2000.0)  # $300 commission (15%)
        
        # Verify earnings
        summary = ResellerManager.get_earnings_summary(reseller_id)
        self.assertEqual(summary['total_sales'], 1)
        self.assertEqual(summary['total_earnings'], 300.0)
        self.assertEqual(summary['tier'], "gold")
        
        print("[Integration] ✓ Reseller flow validated")
    
    def test_partner_referral_flow(self):
        """Test partner revenue sharing"""
        print("\n[Integration] Testing partner referral flow")
        
        # Create enterprise partner (30% revenue share)
        partner_id = PartnerManager.create_partner(
            tenant_id="integration_tenant_5",
            company_name="Enterprise Partner LLC",
            contact_name="Test Partner",
            email="partner@test.com",
            partnership_type="enterprise"
        )
        
        # Record referral
        PartnerManager.record_referral(partner_id, 5000.0)  # $1500 revenue share (30%)
        
        # Verify revenue
        summary = PartnerManager.get_revenue_summary(partner_id)
        self.assertEqual(summary['total_referrals'], 1)
        self.assertEqual(summary['total_revenue'], 1500.0)
        self.assertEqual(summary['partnership_type'], "enterprise")
        
        print("[Integration] ✓ Partner flow validated")
    
    def test_invalid_api_key_rejected(self):
        """Test invalid API key rejection"""
        print("\n[Integration] Testing invalid API key rejection")
        
        # Try to validate random string
        invalid_key = "kuasa_invalid_random_key_12345"
        key_data = APIKeyManager.validate_key(invalid_key)
        
        self.assertIsNone(key_data)
        
        print("[Integration] ✓ Invalid key rejected")
    
    def test_revoked_key_rejected(self):
        """Test revoked key rejection"""
        print("\n[Integration] Testing revoked key rejection")
        
        # Create and revoke key
        api_key = APIKeyManager.create_api_key(
            tenant_id="integration_tenant_6",
            scopes=["read", "write"]
        )
        
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        APIKeyManager.revoke_key(key_data['key_id'])
        
        # Try to validate revoked key
        validated = APIKeyManager.validate_key(api_key)
        self.assertIsNone(validated)
        
        print("[Integration] ✓ Revoked key rejected")
    
    def test_insufficient_scope_rejected(self):
        """Test scope enforcement"""
        print("\n[Integration] Testing scope enforcement")
        
        # Create read-only key
        api_key = APIKeyManager.create_api_key(
            tenant_id="integration_tenant_7",
            scopes=["read"]
        )
        
        key_data = APIKeyManager.validate_key(api_key)
        
        # Check execute scope (should fail)
        has_execute = APIKeyManager.check_scope(key_data, APIKeyScopes.EXECUTE.value)
        self.assertFalse(has_execute)
        
        # Check read scope (should pass)
        has_read = APIKeyManager.check_scope(key_data, APIKeyScopes.READ.value)
        self.assertTrue(has_read)
        
        print("[Integration] ✓ Scope enforcement validated")
    
    def test_insufficient_credits_rejected(self):
        """Test insufficient credits protection"""
        print("\n[Integration] Testing insufficient credits protection")
        
        # Create wallet with 0 credits
        WalletManager.create_wallet("integration_tenant_8", 0.0)
        
        # Try to deduct credits
        tx_id = TransactionManager.generate_transaction_id()
        success = WalletManager.safe_decrement("integration_tenant_8", 10.0, tx_id)
        
        self.assertFalse(success)
        
        # Verify balance unchanged
        balance = WalletManager.get_balance("integration_tenant_8")
        self.assertEqual(balance, 0.0)
        
        print("[Integration] ✓ Insufficient credits blocked")
    
    def test_idempotency_prevents_double_charge(self):
        """Test idempotency key prevents double charging"""
        print("\n[Integration] Testing idempotency protection")
        
        # Create wallet
        WalletManager.create_wallet("integration_tenant_9", 100.0)
        
        # First execution with idempotency key
        exec_id_1 = generate_execution_id()
        idempotency_key = "test_idempotency_001"
        
        tx_id_1 = TransactionManager.create_transaction(
            tenant_id="integration_tenant_9",
            execution_id=exec_id_1,
            amount=10.0,
            idempotency_key=idempotency_key
        )
        
        TransactionManager.update_status(tx_id_1, TransactionStatus.EXECUTING)
        WalletManager.safe_decrement("integration_tenant_9", 10.0, tx_id_1)
        TransactionManager.update_status(tx_id_1, TransactionStatus.COMPLETED)
        
        # Check if duplicate
        is_duplicate = IdempotencyManager.is_duplicate_request(idempotency_key)
        self.assertTrue(is_duplicate)
        
        # Get cached response
        cached = IdempotencyManager.get_cached_response(idempotency_key)
        self.assertIsNotNone(cached)
        self.assertEqual(cached['transaction_id'], tx_id_1)
        self.assertTrue(cached['cached'])
        
        # Verify credits deducted only once
        balance = WalletManager.get_balance("integration_tenant_9")
        self.assertEqual(balance, 90.0)
        
        print("[Integration] ✓ Idempotency protection validated")
    
    def test_tenant_isolation_enforced(self):
        """Test multi-tenant isolation"""
        print("\n[Integration] Testing tenant isolation")
        
        # Create resources in tenant_a
        consultant_a = ConsultantManager.create_consultant(
            tenant_id="tenant_a",
            name="Consultant A",
            email="a@test.com"
        )
        
        reseller_a = ResellerManager.create_reseller(
            tenant_id="tenant_a",
            company_name="Reseller A",
            contact_name="Contact A",
            email="reseller_a@test.com"
        )
        
        # Create resources in tenant_b
        consultant_b = ConsultantManager.create_consultant(
            tenant_id="tenant_b",
            name="Consultant B",
            email="b@test.com"
        )
        
        # List consultants for tenant_a (should only see tenant_a's)
        consultants_a = ConsultantManager.list_consultants("tenant_a")
        self.assertEqual(len(consultants_a), 1)
        self.assertEqual(consultants_a[0]['consultant_id'], consultant_a)
        
        # List resellers for tenant_a (should only see tenant_a's)
        resellers_a = ResellerManager.list_resellers("tenant_a")
        self.assertEqual(len(resellers_a), 1)
        self.assertEqual(resellers_a[0]['reseller_id'], reseller_a)
        
        # List consultants for tenant_b (should only see tenant_b's)
        consultants_b = ConsultantManager.list_consultants("tenant_b")
        self.assertEqual(len(consultants_b), 1)
        self.assertEqual(consultants_b[0]['consultant_id'], consultant_b)
        
        print("[Integration] ✓ Tenant isolation enforced")
    
    def test_audit_trail_complete(self):
        """Test audit trail completeness"""
        print("\n[Integration] Testing audit trail")
        
        # Perform multiple operations
        request_id_1 = generate_request_id()
        exec_id_1 = generate_execution_id()
        
        AuditLogger.log_request(
            tenant_id="integration_tenant_10",
            request_id=request_id_1,
            execution_id=exec_id_1,
            endpoint="/v1/service/execute",
            method="POST",
            status_code=200,
            duration_ms=150.0
        )
        
        request_id_2 = generate_request_id()
        exec_id_2 = generate_execution_id()
        
        AuditLogger.log_request(
            tenant_id="integration_tenant_10",
            request_id=request_id_2,
            execution_id=exec_id_2,
            endpoint="/v1/creative/generate",
            method="POST",
            status_code=200,
            duration_ms=200.0
        )
        
        request_id_3 = generate_request_id()
        
        AuditLogger.log_request(
            tenant_id="integration_tenant_10",
            request_id=request_id_3,
            execution_id=None,
            endpoint="/v1/consultant",
            method="GET",
            status_code=200,
            duration_ms=50.0
        )
        
        # Query audit log
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM audit_log
            WHERE tenant_id = ?
        """, ("integration_tenant_10",))
        
        count = cursor.fetchone()[0]
        self.assertGreaterEqual(count, 3)
        
        # Verify metadata
        cursor.execute("""
            SELECT request_id, execution_id, endpoint, method, status_code
            FROM audit_log
            WHERE tenant_id = ?
            ORDER BY timestamp DESC
            LIMIT 3
        """, ("integration_tenant_10",))
        
        rows = cursor.fetchall()
        self.assertEqual(len(rows), 3)
        
        # Verify first entry
        self.assertEqual(rows[2][0], request_id_1)
        self.assertEqual(rows[2][1], exec_id_1)
        self.assertEqual(rows[2][2], "/v1/service/execute")
        self.assertEqual(rows[2][3], "POST")
        self.assertEqual(rows[2][4], 200)
        
        print("[Integration] ✓ Audit trail complete")


def run_tests():
    """Run all integration smoke tests"""
    print("\n" + "="*70)
    print("PHASE XX-LITE - INTEGRATION SMOKE TESTS")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test class
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationFlows))
    
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
    
    if result.wasSuccessful():
        print("\n✅ LANE 1 LAUNCH READY")
    else:
        print("\n❌ INTEGRATION ISSUES DETECTED")
    
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
