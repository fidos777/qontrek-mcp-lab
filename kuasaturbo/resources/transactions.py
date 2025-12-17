"""
Transaction State Machine

Manages transaction lifecycle: PENDING → EXECUTING → COMPLETED/FAILED/REFUNDED
"""

import json
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
from kuasaturbo.database.connection import get_db_connection


class TransactionStatus(str, Enum):
    """Transaction status states"""
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class TransactionManager:
    """Manages transaction lifecycle and state transitions"""
    
    @staticmethod
    def generate_transaction_id() -> str:
        """
        Generate unique transaction ID
        
        Returns:
            Transaction ID in format: tx_YYYYMMDDHHMMSS_uuid
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        short_uuid = str(uuid.uuid4())[:8]
        return f"tx_{timestamp}_{short_uuid}"
    
    @staticmethod
    def create_transaction(
        tenant_id: str,
        execution_id: str,
        amount: float,
        service_id: Optional[str] = None,
        persona_id: Optional[str] = None,
        model_id: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create new transaction in PENDING state
        
        Args:
            tenant_id: Tenant identifier
            execution_id: Execution identifier
            amount: Transaction amount
            service_id: Optional service identifier
            persona_id: Optional persona identifier
            model_id: Optional model identifier
            idempotency_key: Optional idempotency key
            metadata: Optional metadata
        
        Returns:
            Transaction ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        transaction_id = TransactionManager.generate_transaction_id()
        metadata_json = json.dumps(metadata) if metadata else None
        
        try:
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_id, tenant_id, execution_id, idempotency_key,
                    amount, status, service_id, persona_id, model_id, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                transaction_id, tenant_id, execution_id, idempotency_key,
                amount, TransactionStatus.PENDING.value,
                service_id, persona_id, model_id, metadata_json
            ))
            
            conn.commit()
            
            print(f"[TransactionManager] Created transaction {transaction_id} for {tenant_id} (PENDING)")
            return transaction_id
        
        except Exception as e:
            conn.rollback()
            print(f"[TransactionManager] Error creating transaction: {e}")
            raise
    
    @staticmethod
    def get_transaction(transaction_id: str) -> Optional[Dict[str, Any]]:
        """
        Get transaction by ID
        
        Args:
            transaction_id: Transaction identifier
        
        Returns:
            Transaction dict or None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM transactions
            WHERE transaction_id = ?
        """, (transaction_id,))
        
        row = cursor.fetchone()
        
        return dict(row) if row else None
    
    @staticmethod
    def update_status(
        transaction_id: str,
        new_status: TransactionStatus,
        error_message: Optional[str] = None
    ) -> bool:
        """
        Update transaction status
        
        Args:
            transaction_id: Transaction identifier
            new_status: New status
            error_message: Optional error message
        
        Returns:
            True if successful
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get current transaction
            transaction = TransactionManager.get_transaction(transaction_id)
            if not transaction:
                print(f"[TransactionManager] Transaction not found: {transaction_id}")
                return False
            
            current_status = TransactionStatus(transaction['status'])
            
            # Validate state transition
            if not TransactionManager._is_valid_transition(current_status, new_status):
                print(f"[TransactionManager] Invalid transition: {current_status} → {new_status}")
                return False
            
            # Update status
            completed_at = datetime.utcnow().isoformat() if new_status in [
                TransactionStatus.COMPLETED,
                TransactionStatus.FAILED,
                TransactionStatus.REFUNDED
            ] else None
            
            cursor.execute("""
                UPDATE transactions
                SET status = ?, error_message = ?, updated_at = ?, completed_at = ?
                WHERE transaction_id = ?
            """, (
                new_status.value,
                error_message,
                datetime.utcnow().isoformat(),
                completed_at,
                transaction_id
            ))
            
            conn.commit()
            
            print(f"[TransactionManager] Updated {transaction_id}: {current_status} → {new_status}")
            return True
        
        except Exception as e:
            conn.rollback()
            print(f"[TransactionManager] Error updating status: {e}")
            return False
    
    @staticmethod
    def _is_valid_transition(current: TransactionStatus, new: TransactionStatus) -> bool:
        """
        Validate state transition
        
        Valid transitions:
        - PENDING → EXECUTING
        - EXECUTING → COMPLETED
        - EXECUTING → FAILED
        - FAILED → REFUNDED
        
        Args:
            current: Current status
            new: New status
        
        Returns:
            True if transition is valid
        """
        valid_transitions = {
            TransactionStatus.PENDING: [TransactionStatus.EXECUTING],
            TransactionStatus.EXECUTING: [TransactionStatus.COMPLETED, TransactionStatus.FAILED],
            TransactionStatus.FAILED: [TransactionStatus.REFUNDED],
            TransactionStatus.COMPLETED: [],  # Terminal state
            TransactionStatus.REFUNDED: []    # Terminal state
        }
        
        return new in valid_transitions.get(current, [])
    
    @staticmethod
    def get_tenant_transactions(
        tenant_id: str,
        status: Optional[TransactionStatus] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get transactions for tenant
        
        Args:
            tenant_id: Tenant identifier
            status: Optional status filter
            limit: Maximum number of records
            offset: Offset for pagination
        
        Returns:
            List of transactions
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT * FROM transactions
                WHERE tenant_id = ? AND status = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (tenant_id, status.value, limit, offset))
        else:
            cursor.execute("""
                SELECT * FROM transactions
                WHERE tenant_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (tenant_id, limit, offset))
        
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_execution_transaction(execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Get transaction for execution
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            Transaction dict or None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM transactions
            WHERE execution_id = ?
            LIMIT 1
        """, (execution_id,))
        
        row = cursor.fetchone()
        
        return dict(row) if row else None
