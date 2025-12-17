"""
Consultant Management

Handles consultant CRUD operations, commission tracking, and earnings.
"""

import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from kuasaturbo.database.connection import get_db_connection


class ConsultantManager:
    """Manages consultant operations"""
    
    @staticmethod
    def generate_consultant_id() -> str:
        """Generate unique consultant ID"""
        return f"cons_{uuid.uuid4().hex[:12]}"
    
    @staticmethod
    def create_consultant(
        tenant_id: str,
        name: str,
        email: str,
        phone: Optional[str] = None,
        commission_rate: float = 10.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create new consultant
        
        Args:
            tenant_id: Tenant identifier
            name: Consultant name
            email: Consultant email
            phone: Optional phone number
            commission_rate: Commission rate (percentage)
            metadata: Optional metadata
        
        Returns:
            Consultant ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        consultant_id = ConsultantManager.generate_consultant_id()
        metadata_json = json.dumps(metadata) if metadata else None
        
        try:
            cursor.execute("""
                INSERT INTO consultants (
                    consultant_id, tenant_id, name, email, phone,
                    commission_rate, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                consultant_id, tenant_id, name, email, phone,
                commission_rate, metadata_json
            ))
            
            conn.commit()
            
            print(f"[ConsultantManager] Created consultant {consultant_id} for tenant {tenant_id}")
            return consultant_id
        
        except Exception as e:
            conn.rollback()
            print(f"[ConsultantManager] Error creating consultant: {e}")
            raise
    
    @staticmethod
    def get_consultant(consultant_id: str) -> Optional[Dict[str, Any]]:
        """Get consultant by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM consultants
            WHERE consultant_id = ?
        """, (consultant_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def list_consultants(
        tenant_id: str,
        status: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List consultants for tenant"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT * FROM consultants
                WHERE tenant_id = ? AND status = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (tenant_id, status, limit, offset))
        else:
            cursor.execute("""
                SELECT * FROM consultants
                WHERE tenant_id = ?
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (tenant_id, limit, offset))
        
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    @staticmethod
    def update_consultant(
        consultant_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        commission_rate: Optional[float] = None,
        status: Optional[str] = None
    ) -> bool:
        """Update consultant details"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if email is not None:
                updates.append("email = ?")
                params.append(email)
            if phone is not None:
                updates.append("phone = ?")
                params.append(phone)
            if commission_rate is not None:
                updates.append("commission_rate = ?")
                params.append(commission_rate)
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            
            if not updates:
                return False
            
            updates.append("updated_at = ?")
            params.append(datetime.utcnow().isoformat())
            params.append(consultant_id)
            
            query = f"UPDATE consultants SET {', '.join(updates)} WHERE consultant_id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            
            print(f"[ConsultantManager] Updated consultant {consultant_id}")
            return cursor.rowcount > 0
        
        except Exception as e:
            conn.rollback()
            print(f"[ConsultantManager] Error updating consultant: {e}")
            return False
    
    @staticmethod
    def delete_consultant(consultant_id: str) -> bool:
        """Delete consultant (soft delete by setting status to inactive)"""
        return ConsultantManager.update_consultant(consultant_id, status="inactive")
    
    @staticmethod
    def record_sale(consultant_id: str, amount: float) -> bool:
        """
        Record sale and calculate commission
        
        Args:
            consultant_id: Consultant identifier
            amount: Sale amount
        
        Returns:
            True if successful
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Get consultant
            consultant = ConsultantManager.get_consultant(consultant_id)
            if not consultant:
                return False
            
            # Calculate commission
            commission = amount * (consultant['commission_rate'] / 100.0)
            
            # Update earnings and sales count
            cursor.execute("""
                UPDATE consultants
                SET total_earnings = total_earnings + ?,
                    total_sales = total_sales + 1,
                    updated_at = ?
                WHERE consultant_id = ?
            """, (commission, datetime.utcnow().isoformat(), consultant_id))
            
            conn.commit()
            
            print(f"[ConsultantManager] Recorded sale for {consultant_id}: ${amount} (commission: ${commission})")
            return True
        
        except Exception as e:
            conn.rollback()
            print(f"[ConsultantManager] Error recording sale: {e}")
            return False
    
    @staticmethod
    def get_earnings_summary(consultant_id: str) -> Dict[str, Any]:
        """Get earnings summary for consultant"""
        consultant = ConsultantManager.get_consultant(consultant_id)
        
        if not consultant:
            return {}
        
        return {
            "consultant_id": consultant_id,
            "name": consultant['name'],
            "total_earnings": consultant['total_earnings'],
            "total_sales": consultant['total_sales'],
            "commission_rate": consultant['commission_rate'],
            "average_commission": consultant['total_earnings'] / consultant['total_sales'] if consultant['total_sales'] > 0 else 0.0,
            "status": consultant['status']
        }
