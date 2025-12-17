"""
Test Suite for Resource Layer (Phase XVII-B)

Tests wallets, transactions, idempotency, and execution history.
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.resources.wallets import WalletManager
from kuasaturbo.resources.transactions import TransactionManager, TransactionStatus
from kuasaturbo.resources.idempotency import IdempotencyManager
from kuasaturbo.resources.execution_history import ExecutionHistoryManager
from kuasaturbo.database.connection import get_db_connection, init_database, DB_PATH
from kuasaturbo.logging.logger import generate_execution_id


class TestWalletManager(unittest.TestCase):
    """Test wallet management"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize database"""
        if DB_PATH.exists():
            DB_PATH.unlink()
        init_database()
    
    def test_create_wallet(self):
        """Test wallet creation"""
        print("\n[Test] Creating wallet")
        
        wallet_id = WalletManager.create_wallet("test_tenant_1", 100.0)
        
        self.assertIsNotNone(wallet_id)
        self.assertGreater(wallet_id, 0)
        
        print(f"[Test] ✓ Wallet created with ID {wallet_id}")
    
    def test_get_wallet(self):
        """Test getting wallet"""
        print("\n[Test] Getting wallet")
        
        WalletManager.create_wallet("test_tenant_2", 50.0)
        wallet = WalletManager.get_wallet("test_tenant_2")
        
        self.assertIsNotNone(wallet)
        self.assertEqual(wallet['tenant_id'], "test_tenant_2")
        self.assertEqual(wallet['balance'], 50.0)
        
        print(f"[Test] ✓ Retrieved wallet with balance {wallet['balance']}")
    
    def test_get_balance(self):
        """Test getting balance"""
        print("\n[Test] Getting balance")
        
        WalletManager.create_wallet("test_tenant_3", 75.5)
        balance = WalletManager.get_balance("test_tenant_3")
        
        self.assertEqual(balance, 75.5)
        
        print(f"[Test] ✓ Balance: {balance}")
    
    def test_add_credits(self):
        """Test adding credits"""
        print("\n[Test] Adding credits")
        
        WalletManager.create_wallet("test_tenant_4", 100.0)
        new_balance = WalletManager.add_credits("test_tenant_4", 50.0)
        
        self.assertEqual(new_balance, 150.0)
        
        print(f"[Test] ✓ New balance: {new_balance}")
    
    def test_safe_decrement_success(self):
        """Test successful credit deduction"""
        print("\n[Test] Safe decrement (success)")
        
        WalletManager.create_wallet("test_tenant_5", 100.0)
        success = WalletManager.safe_decrement("test_tenant_5", 30.0, "tx_test_001")
        
        self.assertTrue(success)
        
        balance = WalletManager.get_balance("test_tenant_5")
        self.assertEqual(balance, 70.0)
        
        print(f"[Test] ✓ Deducted 30.0, remaining: {balance}")
    
    def test_safe_decrement_insufficient(self):
        """Test credit deduction with insufficient balance"""
        print("\n[Test] Safe decrement (insufficient)")
        
        WalletManager.create_wallet("test_tenant_6", 10.0)
        success = WalletManager.safe_decrement("test_tenant_6", 50.0, "tx_test_002")
        
        self.assertFalse(success)
        
        balance = WalletManager.get_balance("test_tenant_6")
        self.assertEqual(balance, 10.0)
        
        print(f"[Test] ✓ Deduction blocked, balance unchanged: {balance}")
    
    def test_refund_credits(self):
        """Test credit refund"""
        print("\n[Test] Refunding credits")
        
        WalletManager.create_wallet("test_tenant_7", 50.0)
        new_balance = WalletManager.refund_credits("test_tenant_7", 25.0, "tx_test_003")
        
        self.assertEqual(new_balance, 75.0)
        
        print(f"[Test] ✓ Refunded 25.0, new balance: {new_balance}")


class TestTransactionManager(unittest.TestCase):
    """Test transaction management"""
    
    def test_generate_transaction_id(self):
        """Test transaction ID generation"""
        print("\n[Test] Generating transaction ID")
        
        tx_id = TransactionManager.generate_transaction_id()
        
        self.assertTrue(tx_id.startswith("tx_"))
        self.assertGreater(len(tx_id), 20)
        
        print(f"[Test] ✓ Generated: {tx_id}")
    
    def test_create_transaction(self):
        """Test transaction creation"""
        print("\n[Test] Creating transaction")
        
        exec_id = generate_execution_id()
        tx_id = TransactionManager.create_transaction(
            tenant_id="test_tenant",
            execution_id=exec_id,
            amount=10.0,
            service_id="lead_intake"
        )
        
        self.assertIsNotNone(tx_id)
        
        # Verify transaction
        tx = TransactionManager.get_transaction(tx_id)
        self.assertEqual(tx['status'], TransactionStatus.PENDING.value)
        self.assertEqual(tx['amount'], 10.0)
        
        print(f"[Test] ✓ Transaction created: {tx_id}")
    
    def test_transaction_state_machine(self):
        """Test transaction state transitions"""
        print("\n[Test] Testing state machine")
        
        exec_id = generate_execution_id()
        tx_id = TransactionManager.create_transaction(
            tenant_id="test_tenant",
            execution_id=exec_id,
            amount=5.0
        )
        
        # PENDING → EXECUTING
        success = TransactionManager.update_status(tx_id, TransactionStatus.EXECUTING)
        self.assertTrue(success)
        
        tx = TransactionManager.get_transaction(tx_id)
        self.assertEqual(tx['status'], TransactionStatus.EXECUTING.value)
        
        # EXECUTING → COMPLETED
        success = TransactionManager.update_status(tx_id, TransactionStatus.COMPLETED)
        self.assertTrue(success)
        
        tx = TransactionManager.get_transaction(tx_id)
        self.assertEqual(tx['status'], TransactionStatus.COMPLETED.value)
        self.assertIsNotNone(tx['completed_at'])
        
        print(f"[Test] ✓ State transitions: PENDING → EXECUTING → COMPLETED")
    
    def test_invalid_state_transition(self):
        """Test invalid state transition"""
        print("\n[Test] Testing invalid transition")
        
        exec_id = generate_execution_id()
        tx_id = TransactionManager.create_transaction(
            tenant_id="test_tenant",
            execution_id=exec_id,
            amount=5.0
        )
        
        # PENDING → COMPLETED (invalid, must go through EXECUTING)
        success = TransactionManager.update_status(tx_id, TransactionStatus.COMPLETED)
        self.assertFalse(success)
        
        tx = TransactionManager.get_transaction(tx_id)
        self.assertEqual(tx['status'], TransactionStatus.PENDING.value)
        
        print(f"[Test] ✓ Invalid transition blocked")
    
    def test_failed_to_refunded(self):
        """Test FAILED → REFUNDED transition"""
        print("\n[Test] Testing FAILED → REFUNDED")
        
        exec_id = generate_execution_id()
        tx_id = TransactionManager.create_transaction(
            tenant_id="test_tenant",
            execution_id=exec_id,
            amount=5.0
        )
        
        # PENDING → EXECUTING → FAILED
        TransactionManager.update_status(tx_id, TransactionStatus.EXECUTING)
        TransactionManager.update_status(tx_id, TransactionStatus.FAILED, "Test error")
        
        # FAILED → REFUNDED
        success = TransactionManager.update_status(tx_id, TransactionStatus.REFUNDED)
        self.assertTrue(success)
        
        tx = TransactionManager.get_transaction(tx_id)
        self.assertEqual(tx['status'], TransactionStatus.REFUNDED.value)
        
        print(f"[Test] ✓ FAILED → REFUNDED successful")


class TestIdempotencyManager(unittest.TestCase):
    """Test idempotency management"""
    
    def test_check_idempotency_key_not_found(self):
        """Test checking non-existent key"""
        print("\n[Test] Checking non-existent idempotency key")
        
        result = IdempotencyManager.check_idempotency_key("nonexistent_key")
        
        self.assertIsNone(result)
        
        print(f"[Test] ✓ Key not found (as expected)")
    
    def test_check_idempotency_key_found(self):
        """Test checking existing key"""
        print("\n[Test] Checking existing idempotency key")
        
        exec_id = generate_execution_id()
        idempotency_key = "test_idempotency_001"
        
        # Create transaction with idempotency key
        tx_id = TransactionManager.create_transaction(
            tenant_id="test_tenant",
            execution_id=exec_id,
            amount=5.0,
            idempotency_key=idempotency_key
        )
        
        # Check key
        result = IdempotencyManager.check_idempotency_key(idempotency_key)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['transaction_id'], tx_id)
        
        print(f"[Test] ✓ Found transaction: {tx_id}")
    
    def test_is_duplicate_request(self):
        """Test duplicate request detection"""
        print("\n[Test] Testing duplicate detection")
        
        exec_id = generate_execution_id()
        idempotency_key = "test_idempotency_002"
        
        # First request
        is_dup = IdempotencyManager.is_duplicate_request(idempotency_key)
        self.assertFalse(is_dup)
        
        # Create transaction
        TransactionManager.create_transaction(
            tenant_id="test_tenant",
            execution_id=exec_id,
            amount=5.0,
            idempotency_key=idempotency_key
        )
        
        # Second request (duplicate)
        is_dup = IdempotencyManager.is_duplicate_request(idempotency_key)
        self.assertTrue(is_dup)
        
        print(f"[Test] ✓ Duplicate detected")
    
    def test_get_cached_response(self):
        """Test getting cached response"""
        print("\n[Test] Getting cached response")
        
        exec_id = generate_execution_id()
        idempotency_key = "test_idempotency_003"
        
        # Create transaction
        tx_id = TransactionManager.create_transaction(
            tenant_id="test_tenant",
            execution_id=exec_id,
            amount=5.0,
            idempotency_key=idempotency_key
        )
        
        # Get cached response
        cached = IdempotencyManager.get_cached_response(idempotency_key)
        
        self.assertIsNotNone(cached)
        self.assertEqual(cached['transaction_id'], tx_id)
        self.assertTrue(cached['cached'])
        
        print(f"[Test] ✓ Retrieved cached response")


class TestExecutionHistoryManager(unittest.TestCase):
    """Test execution history management"""
    
    def test_log_execution(self):
        """Test logging execution"""
        print("\n[Test] Logging execution")
        
        exec_id = generate_execution_id()
        tx_id = TransactionManager.generate_transaction_id()
        
        history_id = ExecutionHistoryManager.log_execution(
            execution_id=exec_id,
            tenant_id="test_tenant",
            transaction_id=tx_id,
            service_id="lead_intake",
            status="COMPLETED",
            persona_id="izzara",
            model_id="gpt-4",
            duration_ms=145.3
        )
        
        self.assertIsNotNone(history_id)
        self.assertGreater(history_id, 0)
        
        print(f"[Test] ✓ Execution logged (history_id={history_id})")
    
    def test_get_execution_history(self):
        """Test retrieving execution history"""
        print("\n[Test] Retrieving execution history")
        
        exec_id = generate_execution_id()
        tx_id = TransactionManager.generate_transaction_id()
        
        # Log multiple entries
        for i in range(3):
            ExecutionHistoryManager.log_execution(
                execution_id=exec_id,
                tenant_id="test_tenant",
                transaction_id=tx_id,
                service_id=f"service_{i}",
                status="COMPLETED"
            )
        
        # Retrieve history
        history = ExecutionHistoryManager.get_execution_history(exec_id)
        
        self.assertEqual(len(history), 3)
        
        print(f"[Test] ✓ Retrieved {len(history)} history entries")
    
    def test_get_statistics(self):
        """Test getting execution statistics"""
        print("\n[Test] Getting execution statistics")
        
        tenant_id = "stats_test_tenant"
        
        # Log some executions
        for i in range(10):
            exec_id = generate_execution_id()
            tx_id = TransactionManager.generate_transaction_id()
            status = "COMPLETED" if i < 8 else "FAILED"
            
            ExecutionHistoryManager.log_execution(
                execution_id=exec_id,
                tenant_id=tenant_id,
                transaction_id=tx_id,
                service_id="test_service",
                status=status,
                duration_ms=100.0 + i * 10
            )
        
        # Get statistics
        stats = ExecutionHistoryManager.get_statistics(tenant_id)
        
        self.assertEqual(stats['total_executions'], 10)
        self.assertEqual(stats['successful'], 8)
        self.assertEqual(stats['failed'], 2)
        self.assertEqual(stats['success_rate'], 80.0)
        self.assertGreater(stats['average_duration_ms'], 0)
        
        print(f"[Test] ✓ Statistics: {stats}")


def run_tests():
    """Run all resource layer tests"""
    print("\n" + "="*70)
    print("PHASE XVII-B - RESOURCE LAYER TEST SUITE")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestWalletManager))
    suite.addTests(loader.loadTestsFromTestCase(TestTransactionManager))
    suite.addTests(loader.loadTestsFromTestCase(TestIdempotencyManager))
    suite.addTests(loader.loadTestsFromTestCase(TestExecutionHistoryManager))
    
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
