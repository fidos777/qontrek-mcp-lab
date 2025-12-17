"""
Test Suite for Logging Layer (Phase XVII-A)

Tests logger, audit, and middleware functionality.
"""

import os
import sys
import unittest
import sqlite3
import time
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.logging.logger import (
    generate_request_id,
    generate_execution_id,
    get_logger
)
from kuasaturbo.logging.audit import AuditLogger, init_audit_db
from kuasaturbo.database.connection import get_db_connection, DB_PATH


class TestIDGeneration(unittest.TestCase):
    """Test request and execution ID generation"""
    
    def test_generate_request_id(self):
        """Test request ID generation"""
        print("\n[Test] Generating request ID")
        
        request_id = generate_request_id()
        
        # Check format
        self.assertTrue(request_id.startswith("req_"))
        self.assertGreater(len(request_id), 20)
        
        # Check uniqueness
        request_id2 = generate_request_id()
        self.assertNotEqual(request_id, request_id2)
        
        print(f"[Test] ✓ Generated request ID: {request_id}")
    
    def test_generate_execution_id(self):
        """Test execution ID generation"""
        print("\n[Test] Generating execution ID")
        
        execution_id = generate_execution_id()
        
        # Check format
        self.assertTrue(execution_id.startswith("exec_"))
        self.assertGreater(len(execution_id), 20)
        
        # Check uniqueness
        execution_id2 = generate_execution_id()
        self.assertNotEqual(execution_id, execution_id2)
        
        print(f"[Test] ✓ Generated execution ID: {execution_id}")


class TestLogger(unittest.TestCase):
    """Test logger functionality"""
    
    def test_get_logger_basic(self):
        """Test basic logger creation"""
        print("\n[Test] Creating basic logger")
        
        logger = get_logger("test_module")
        
        self.assertIsNotNone(logger)
        
        # Test logging
        logger.info("Test log message")
        
        print("[Test] ✓ Logger created and logged successfully")
    
    def test_get_logger_with_context(self):
        """Test logger with tenant context"""
        print("\n[Test] Creating logger with context")
        
        logger = get_logger(
            "test_module",
            tenant_id="test_tenant",
            request_id="req_test_123",
            execution_id="exec_test_456"
        )
        
        self.assertIsNotNone(logger)
        
        # Test logging with context
        logger.info("Test log with context")
        
        print("[Test] ✓ Logger with context created successfully")
    
    def test_logger_levels(self):
        """Test different log levels"""
        print("\n[Test] Testing log levels")
        
        logger = get_logger("test_module", tenant_id="test_tenant")
        
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        print("[Test] ✓ All log levels working")


class TestAuditLogger(unittest.TestCase):
    """Test audit logger functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Initialize database before tests"""
        # Remove existing database
        if DB_PATH.exists():
            DB_PATH.unlink()
        
        # Initialize fresh database
        init_audit_db()
    
    def test_log_request_basic(self):
        """Test basic request logging"""
        print("\n[Test] Logging basic request")
        
        audit_id = AuditLogger.log_request(
            tenant_id="test_tenant",
            request_id="req_test_001",
            endpoint="/test/endpoint",
            method="GET",
            status_code=200,
            duration_ms=45.5
        )
        
        self.assertIsNotNone(audit_id)
        self.assertGreater(audit_id, 0)
        
        print(f"[Test] ✓ Request logged with audit_id={audit_id}")
    
    def test_log_request_with_execution(self):
        """Test request logging with execution context"""
        print("\n[Test] Logging request with execution context")
        
        audit_id = AuditLogger.log_request(
            tenant_id="test_tenant",
            request_id="req_test_002",
            endpoint="/service/execute",
            method="POST",
            status_code=200,
            duration_ms=150.3,
            execution_id="exec_test_001",
            persona_id="izzara",
            model_id="gpt-4",
            metadata={"service_id": "lead_intake"}
        )
        
        self.assertIsNotNone(audit_id)
        
        print(f"[Test] ✓ Request with execution logged (audit_id={audit_id})")
    
    def test_log_request_with_error(self):
        """Test request logging with error"""
        print("\n[Test] Logging request with error")
        
        audit_id = AuditLogger.log_request(
            tenant_id="test_tenant",
            request_id="req_test_003",
            endpoint="/service/execute",
            method="POST",
            status_code=500,
            duration_ms=25.1,
            error_message="Internal server error"
        )
        
        self.assertIsNotNone(audit_id)
        
        print(f"[Test] ✓ Error request logged (audit_id={audit_id})")
    
    def test_get_tenant_logs(self):
        """Test retrieving tenant logs"""
        print("\n[Test] Retrieving tenant logs")
        
        # Log multiple requests
        for i in range(5):
            AuditLogger.log_request(
                tenant_id="tenant_query_test",
                request_id=f"req_query_{i}",
                endpoint=f"/test/endpoint/{i}",
                method="GET",
                status_code=200
            )
        
        # Retrieve logs
        logs = AuditLogger.get_tenant_logs("tenant_query_test", limit=10)
        
        self.assertGreaterEqual(len(logs), 5)
        self.assertEqual(logs[0]['tenant_id'], "tenant_query_test")
        
        print(f"[Test] ✓ Retrieved {len(logs)} logs for tenant")
    
    def test_get_request_log(self):
        """Test retrieving specific request log"""
        print("\n[Test] Retrieving specific request log")
        
        request_id = "req_specific_test"
        
        # Log request
        AuditLogger.log_request(
            tenant_id="test_tenant",
            request_id=request_id,
            endpoint="/test/specific",
            method="POST",
            status_code=201
        )
        
        # Retrieve log
        log = AuditLogger.get_request_log(request_id)
        
        self.assertIsNotNone(log)
        self.assertEqual(log['request_id'], request_id)
        self.assertEqual(log['status_code'], 201)
        
        print(f"[Test] ✓ Retrieved log for request {request_id}")
    
    def test_get_execution_logs(self):
        """Test retrieving execution logs"""
        print("\n[Test] Retrieving execution logs")
        
        execution_id = "exec_multi_test"
        
        # Log multiple requests for same execution
        for i in range(3):
            AuditLogger.log_request(
                tenant_id="test_tenant",
                request_id=f"req_exec_{i}",
                endpoint=f"/test/step/{i}",
                method="POST",
                status_code=200,
                execution_id=execution_id
            )
            time.sleep(0.01)  # Small delay to ensure ordering
        
        # Retrieve logs
        logs = AuditLogger.get_execution_logs(execution_id)
        
        self.assertEqual(len(logs), 3)
        self.assertEqual(logs[0]['execution_id'], execution_id)
        
        print(f"[Test] ✓ Retrieved {len(logs)} logs for execution")


class TestDatabaseIntegration(unittest.TestCase):
    """Test database integration"""
    
    def test_database_connection(self):
        """Test database connection"""
        print("\n[Test] Testing database connection")
        
        conn = get_db_connection()
        
        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)
        
        print("[Test] ✓ Database connection established")
    
    def test_audit_table_exists(self):
        """Test audit_log table exists"""
        print("\n[Test] Checking audit_log table")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='audit_log'
        """)
        
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'audit_log')
        
        print("[Test] ✓ audit_log table exists")
    
    def test_audit_indexes_exist(self):
        """Test audit_log indexes exist"""
        print("\n[Test] Checking audit_log indexes")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND tbl_name='audit_log'
        """)
        
        indexes = cursor.fetchall()
        index_names = [idx[0] for idx in indexes]
        
        self.assertIn('idx_audit_tenant', index_names)
        self.assertIn('idx_audit_request', index_names)
        self.assertIn('idx_audit_execution', index_names)
        self.assertIn('idx_audit_timestamp', index_names)
        
        print(f"[Test] ✓ Found {len(indexes)} indexes")


def run_tests():
    """Run all logging tests"""
    print("\n" + "="*70)
    print("PHASE XVII-A - LOGGING & AUDIT TEST SUITE")
    print("="*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestIDGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestAuditLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseIntegration))
    
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
