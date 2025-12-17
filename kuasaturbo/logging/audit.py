"""
Audit Logger

Logs all API requests and executions to SQLite database.
"""

import json
import sqlite3
from datetime import datetime
from typing import Optional, Dict, Any

from kuasaturbo.database.connection import get_db_connection


class AuditLogger:
    """Audit logger for API requests and executions"""
    
    @staticmethod
    def log_request(
        tenant_id: str,
        request_id: str,
        endpoint: str,
        method: str,
        status_code: int,
        duration_ms: Optional[float] = None,
        execution_id: Optional[str] = None,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
        persona_id: Optional[str] = None,
        model_id: Optional[str] = None,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Log API request to audit table
        
        Args:
            tenant_id: Tenant identifier
            request_id: Request identifier
            endpoint: API endpoint path
            method: HTTP method
            status_code: HTTP status code
            duration_ms: Request duration in milliseconds
            execution_id: Optional execution identifier
            user_agent: Optional user agent string
            ip_address: Optional client IP address
            persona_id: Optional persona identifier
            model_id: Optional model identifier
            error_message: Optional error message
            metadata: Optional additional metadata
        
        Returns:
            Audit log entry ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None
        
        cursor.execute("""
            INSERT INTO audit_log (
                timestamp, tenant_id, request_id, execution_id,
                endpoint, method, status_code, duration_ms,
                user_agent, ip_address, persona_id, model_id,
                error_message, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp, tenant_id, request_id, execution_id,
            endpoint, method, status_code, duration_ms,
            user_agent, ip_address, persona_id, model_id,
            error_message, metadata_json
        ))
        
        conn.commit()
        
        audit_id = cursor.lastrowid
        print(f"[AuditLogger] Logged request {request_id} for tenant {tenant_id} (audit_id={audit_id})")
        
        return audit_id
    
    @staticmethod
    def get_tenant_logs(
        tenant_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> list:
        """
        Get audit logs for a tenant
        
        Args:
            tenant_id: Tenant identifier
            limit: Maximum number of records
            offset: Offset for pagination
        
        Returns:
            List of audit log entries
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM audit_log
            WHERE tenant_id = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """, (tenant_id, limit, offset))
        
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    @staticmethod
    def get_request_log(request_id: str) -> Optional[Dict[str, Any]]:
        """
        Get audit log for a specific request
        
        Args:
            request_id: Request identifier
        
        Returns:
            Audit log entry or None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM audit_log
            WHERE request_id = ?
            LIMIT 1
        """, (request_id,))
        
        row = cursor.fetchone()
        
        return dict(row) if row else None
    
    @staticmethod
    def get_execution_logs(execution_id: str) -> list:
        """
        Get all audit logs for an execution
        
        Args:
            execution_id: Execution identifier
        
        Returns:
            List of audit log entries
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM audit_log
            WHERE execution_id = ?
            ORDER BY timestamp ASC
        """, (execution_id,))
        
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]


def init_audit_db():
    """Initialize audit database"""
    from kuasaturbo.database.connection import init_database
    init_database()
