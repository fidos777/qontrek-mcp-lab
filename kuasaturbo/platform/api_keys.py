"""
API Key Management (Phase XIX)

Handles API key lifecycle: create, rotate, revoke, validate, scope enforcement.
"""

import sqlite3
import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from enum import Enum

from kuasaturbo.database.connection import get_db_connection


class APIKeyScopes(Enum):
    """API key scope definitions"""
    READ = "read"           # GET-only access
    WRITE = "write"         # POST/PUT/PATCH access
    EXECUTE = "execute"     # /v1/service/execute + creative tasks
    ADMIN = "admin"         # Platform administration


class APIKeyStatus(Enum):
    """API key status"""
    ACTIVE = "active"
    REVOKED = "revoked"
    ROTATED = "rotated"


class APIKeyManager:
    """Manages API key lifecycle and validation"""
    
    GRACE_PERIOD_MINUTES = 10  # Grace period for rotated keys
    
    @staticmethod
    def generate_key_id() -> str:
        """Generate unique key ID"""
        return f"key_{secrets.token_hex(12)}"
    
    @staticmethod
    def generate_api_key() -> str:
        """Generate secure API key"""
        return f"kuasa_{secrets.token_urlsafe(32)}"
    
    @staticmethod
    def create_api_key(
        tenant_id: str,
        scopes: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create new API key
        
        Args:
            tenant_id: Tenant identifier
            scopes: List of scope strings (read, write, execute, admin)
            metadata: Optional metadata
        
        Returns:
            API key string
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        key_id = APIKeyManager.generate_key_id()
        api_key = APIKeyManager.generate_api_key()
        scopes_str = ",".join(scopes)
        
        cursor.execute("""
            INSERT INTO api_keys (
                key_id, tenant_id, api_key, scopes, status, metadata
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            key_id,
            tenant_id,
            api_key,
            scopes_str,
            APIKeyStatus.ACTIVE.value,
            str(metadata) if metadata else None
        ))
        
        conn.commit()
        # Don't close - using thread-local connection
        
        print(f"[APIKeyManager] Created API key {key_id} for tenant {tenant_id} with scopes: {scopes_str}")
        
        return api_key
    
    @staticmethod
    def get_key_by_api_key(api_key: str) -> Optional[Dict[str, Any]]:
        """
        Get key details by API key string
        
        Args:
            api_key: API key string
        
        Returns:
            Key details dict or None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                key_id, tenant_id, api_key, scopes, status,
                created_at, last_used_at, revoked_at, rotated_at, rotated_from
            FROM api_keys
            WHERE api_key = ?
        """, (api_key,))
        
        row = cursor.fetchone()
        
        
        if not row:
            return None
        
        return {
            'key_id': row[0],
            'tenant_id': row[1],
            'api_key': row[2],
            'scopes': row[3].split(',') if row[3] else [],
            'status': row[4],
            'created_at': row[5],
            'last_used_at': row[6],
            'revoked_at': row[7],
            'rotated_at': row[8],
            'rotated_from': row[9]
        }
    
    @staticmethod
    def get_key_by_id(key_id: str) -> Optional[Dict[str, Any]]:
        """
        Get key details by key ID
        
        Args:
            key_id: Key identifier
        
        Returns:
            Key details dict or None
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                key_id, tenant_id, api_key, scopes, status,
                created_at, last_used_at, revoked_at, rotated_at, rotated_from
            FROM api_keys
            WHERE key_id = ?
        """, (key_id,))
        
        row = cursor.fetchone()
        
        
        if not row:
            return None
        
        return {
            'key_id': row[0],
            'tenant_id': row[1],
            'api_key': row[2],
            'scopes': row[3].split(',') if row[3] else [],
            'status': row[4],
            'created_at': row[5],
            'last_used_at': row[6],
            'revoked_at': row[7],
            'rotated_at': row[8],
            'rotated_from': row[9]
        }
    
    @staticmethod
    def list_keys(
        tenant_id: str,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List API keys for tenant
        
        Args:
            tenant_id: Tenant identifier
            status: Optional status filter
            limit: Maximum results
            offset: Pagination offset
        
        Returns:
            List of key dicts
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT 
                    key_id, tenant_id, api_key, scopes, status,
                    created_at, last_used_at, revoked_at
                FROM api_keys
                WHERE tenant_id = ? AND status = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (tenant_id, status, limit, offset))
        else:
            cursor.execute("""
                SELECT 
                    key_id, tenant_id, api_key, scopes, status,
                    created_at, last_used_at, revoked_at
                FROM api_keys
                WHERE tenant_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (tenant_id, limit, offset))
        
        rows = cursor.fetchall()
        
        
        keys = []
        for row in rows:
            keys.append({
                'key_id': row[0],
                'tenant_id': row[1],
                'api_key': row[2][:20] + '...' if len(row[2]) > 20 else row[2],  # Masked
                'scopes': row[3].split(',') if row[3] else [],
                'status': row[4],
                'created_at': row[5],
                'last_used_at': row[6],
                'revoked_at': row[7]
            })
        
        return keys
    
    @staticmethod
    def validate_key(api_key: str) -> Optional[Dict[str, Any]]:
        """
        Validate API key and check status
        
        Args:
            api_key: API key string
        
        Returns:
            Key details if valid, None otherwise
        """
        key_data = APIKeyManager.get_key_by_api_key(api_key)
        
        if not key_data:
            return None
        
        # Check if revoked
        if key_data['status'] == APIKeyStatus.REVOKED.value:
            print(f"[APIKeyManager] Key {key_data['key_id']} is revoked")
            return None
        
        # Check if rotated (grace period)
        if key_data['status'] == APIKeyStatus.ROTATED.value:
            if key_data['rotated_at']:
                # Parse timestamp (SQLite returns UTC)
                rotated_at = datetime.fromisoformat(key_data['rotated_at'].replace(' ', 'T'))
                grace_expires = rotated_at + timedelta(minutes=APIKeyManager.GRACE_PERIOD_MINUTES)
                
                # Compare with current UTC time
                now = datetime.utcnow()
                
                if now > grace_expires:
                    print(f"[APIKeyManager] Key {key_data['key_id']} grace period expired")
                    return None
                
                print(f"[APIKeyManager] Key {key_data['key_id']} in grace period")
            else:
                # No rotated_at timestamp, reject
                print(f"[APIKeyManager] Key {key_data['key_id']} rotated but no timestamp")
                return None
        
        # Update last_used_at
        APIKeyManager.update_last_used(key_data['key_id'])
        
        return key_data
    
    @staticmethod
    def update_last_used(key_id: str) -> bool:
        """
        Update last_used_at timestamp
        
        Args:
            key_id: Key identifier
        
        Returns:
            Success boolean
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE api_keys
            SET last_used_at = CURRENT_TIMESTAMP
            WHERE key_id = ?
        """, (key_id,))
        
        conn.commit()
        success = cursor.rowcount > 0
        
        
        return success
    
    @staticmethod
    def rotate_key(key_id: str) -> Optional[str]:
        """
        Rotate API key (create new, mark old as rotated)
        
        Args:
            key_id: Key identifier to rotate
        
        Returns:
            New API key string or None
        """
        # Get existing key
        old_key = APIKeyManager.get_key_by_id(key_id)
        
        if not old_key:
            print(f"[APIKeyManager] Key {key_id} not found")
            return None
        
        if old_key['status'] != APIKeyStatus.ACTIVE.value:
            print(f"[APIKeyManager] Key {key_id} is not active (status: {old_key['status']})")
            return None
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Generate new key
            new_key_id = APIKeyManager.generate_key_id()
            new_api_key = APIKeyManager.generate_api_key()
            scopes_str = ",".join(old_key['scopes'])
            
            # Create new key
            cursor.execute("""
                INSERT INTO api_keys (
                    key_id, tenant_id, api_key, scopes, status, rotated_from
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (
                new_key_id,
                old_key['tenant_id'],
                new_api_key,
                scopes_str,
                APIKeyStatus.ACTIVE.value,
                key_id
            ))
            
            # Mark old key as rotated
            cursor.execute("""
                UPDATE api_keys
                SET status = ?, rotated_at = CURRENT_TIMESTAMP
                WHERE key_id = ?
            """, (APIKeyStatus.ROTATED.value, key_id))
            
            conn.commit()
            
            print(f"[APIKeyManager] Rotated key {key_id} → {new_key_id} (grace period: {APIKeyManager.GRACE_PERIOD_MINUTES} min)")
            
            return new_api_key
            
        except Exception as e:
            conn.rollback()
            print(f"[APIKeyManager] Error rotating key: {e}")
            return None
    
    @staticmethod
    def revoke_key(key_id: str) -> bool:
        """
        Revoke API key (permanent)
        
        Args:
            key_id: Key identifier
        
        Returns:
            Success boolean
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE api_keys
            SET status = ?, revoked_at = CURRENT_TIMESTAMP
            WHERE key_id = ? AND status != ?
        """, (APIKeyStatus.REVOKED.value, key_id, APIKeyStatus.REVOKED.value))
        
        conn.commit()
        success = cursor.rowcount > 0
        
        
        if success:
            print(f"[APIKeyManager] Revoked key {key_id}")
        else:
            print(f"[APIKeyManager] Key {key_id} not found or already revoked")
        
        return success
    
    @staticmethod
    def check_scope(key_data: Dict[str, Any], required_scope: str) -> bool:
        """
        Check if key has required scope
        
        Args:
            key_data: Key details dict
            required_scope: Required scope string
        
        Returns:
            True if scope present
        """
        scopes = key_data.get('scopes', [])
        
        # Admin scope grants all permissions
        if APIKeyScopes.ADMIN.value in scopes:
            return True
        
        return required_scope in scopes
    
    @staticmethod
    def get_scope_for_method(method: str) -> str:
        """
        Determine required scope for HTTP method
        
        Args:
            method: HTTP method (GET, POST, PUT, etc.)
        
        Returns:
            Required scope string
        """
        if method == "GET":
            return APIKeyScopes.READ.value
        elif method in ["POST", "PUT", "PATCH", "DELETE"]:
            return APIKeyScopes.WRITE.value
        else:
            return APIKeyScopes.READ.value
