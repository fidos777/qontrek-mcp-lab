"""
Idempotency Key Management

Prevents duplicate executions using idempotency keys.
"""

from typing import Optional, Dict, Any
from kuasaturbo.database.connection import get_db_connection


class IdempotencyManager:
    """Manages idempotency keys for duplicate prevention"""
    
    @staticmethod
    def check_idempotency_key(idempotency_key: str) -> Optional[Dict[str, Any]]:
        """
        Check if idempotency key exists
        
        Args:
            idempotency_key: Idempotency key from request header
        
        Returns:
            Existing transaction dict or None
        """
        if not idempotency_key:
            return None
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM transactions
            WHERE idempotency_key = ?
        """, (idempotency_key,))
        
        row = cursor.fetchone()
        
        if row:
            transaction = dict(row)
            print(f"[IdempotencyManager] Found existing transaction for key {idempotency_key}: {transaction['transaction_id']}")
            return transaction
        
        return None
    
    @staticmethod
    def is_duplicate_request(idempotency_key: str) -> bool:
        """
        Check if request is duplicate
        
        Args:
            idempotency_key: Idempotency key from request header
        
        Returns:
            True if duplicate
        """
        return IdempotencyManager.check_idempotency_key(idempotency_key) is not None
    
    @staticmethod
    def get_cached_response(idempotency_key: str) -> Optional[Dict[str, Any]]:
        """
        Get cached response for idempotent request
        
        Args:
            idempotency_key: Idempotency key
        
        Returns:
            Cached response data or None
        """
        transaction = IdempotencyManager.check_idempotency_key(idempotency_key)
        
        if not transaction:
            return None
        
        # Return transaction details as cached response
        return {
            "transaction_id": transaction['transaction_id'],
            "execution_id": transaction['execution_id'],
            "status": transaction['status'],
            "amount": transaction['amount'],
            "created_at": transaction['created_at'],
            "completed_at": transaction['completed_at'],
            "cached": True
        }
    
    @staticmethod
    def validate_idempotency_key(idempotency_key: Optional[str]) -> bool:
        """
        Validate idempotency key format
        
        Args:
            idempotency_key: Idempotency key to validate
        
        Returns:
            True if valid or None
        """
        if idempotency_key is None:
            return True
        
        # Must be non-empty string
        if not isinstance(idempotency_key, str) or len(idempotency_key) == 0:
            return False
        
        # Must be reasonable length (max 255 chars)
        if len(idempotency_key) > 255:
            return False
        
        return True
