"""
Execution History Management

Tracks execution history for audit and debugging.
"""

import json
from typing import Optional, Dict, Any, List
from kuasaturbo.database.connection import get_db_connection


class ExecutionHistoryManager:
    """Manages execution history records"""
    
    @staticmethod
    def log_execution(
        execution_id: str,
        tenant_id: str,
        transaction_id: str,
        service_id: str,
        status: str,
        persona_id: Optional[str] = None,
        model_id: Optional[str] = None,
        input_data: Optional[Dict[str, Any]] = None,
        output_data: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None,
        duration_ms: Optional[float] = None
    ) -> int:
        """
        Log execution to history
        
        Args:
            execution_id: Execution identifier
            tenant_id: Tenant identifier
            transaction_id: Transaction identifier
            service_id: Service identifier
            status: Execution status
            persona_id: Optional persona identifier
            model_id: Optional model identifier
            input_data: Optional input data
            output_data: Optional output data
            error_message: Optional error message
            duration_ms: Optional duration in milliseconds
        
        Returns:
            History entry ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        input_json = json.dumps(input_data) if input_data else None
        output_json = json.dumps(output_data) if output_data else None
        
        try:
            cursor.execute("""
                INSERT INTO execution_history (
                    execution_id, tenant_id, transaction_id, service_id,
                    persona_id, model_id, status, input_data, output_data,
                    error_message, duration_ms
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                execution_id, tenant_id, transaction_id, service_id,
                persona_id, model_id, status, input_json, output_json,
                error_message, duration_ms
            ))
            
            conn.commit()
            
            history_id = cursor.lastrowid
            print(f"[ExecutionHistory] Logged execution {execution_id} (history_id={history_id})")
            
            return history_id
        
        except Exception as e:
            conn.rollback()
            print(f"[ExecutionHistory] Error logging execution: {e}")
            raise
    
    @staticmethod
    def get_execution_history(execution_id: str) -> List[Dict[str, Any]]:
        """
        Get history for execution
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            List of history entries
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM execution_history
            WHERE execution_id = ?
            ORDER BY created_at ASC
        """, (execution_id,))
        
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_tenant_history(
        tenant_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get execution history for tenant
        
        Args:
            tenant_id: Tenant identifier
            limit: Maximum number of records
            offset: Offset for pagination
        
        Returns:
            List of history entries
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM execution_history
            WHERE tenant_id = ?
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (tenant_id, limit, offset))
        
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_transaction_history(transaction_id: str) -> List[Dict[str, Any]]:
        """
        Get history for transaction
        
        Args:
            transaction_id: Transaction identifier
        
        Returns:
            List of history entries
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM execution_history
            WHERE transaction_id = ?
            ORDER BY created_at ASC
        """, (transaction_id,))
        
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_statistics(tenant_id: str) -> Dict[str, Any]:
        """
        Get execution statistics for tenant
        
        Args:
            tenant_id: Tenant identifier
        
        Returns:
            Statistics dict
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total executions
        cursor.execute("""
            SELECT COUNT(*) as total FROM execution_history
            WHERE tenant_id = ?
        """, (tenant_id,))
        total = cursor.fetchone()[0]
        
        # Success count
        cursor.execute("""
            SELECT COUNT(*) as success FROM execution_history
            WHERE tenant_id = ? AND status = 'COMPLETED'
        """, (tenant_id,))
        success = cursor.fetchone()[0]
        
        # Failed count
        cursor.execute("""
            SELECT COUNT(*) as failed FROM execution_history
            WHERE tenant_id = ? AND status = 'FAILED'
        """, (tenant_id,))
        failed = cursor.fetchone()[0]
        
        # Average duration
        cursor.execute("""
            SELECT AVG(duration_ms) as avg_duration FROM execution_history
            WHERE tenant_id = ? AND duration_ms IS NOT NULL
        """, (tenant_id,))
        avg_duration = cursor.fetchone()[0] or 0.0
        
        return {
            "total_executions": total,
            "successful": success,
            "failed": failed,
            "success_rate": (success / total * 100) if total > 0 else 0.0,
            "average_duration_ms": round(avg_duration, 2)
        }
