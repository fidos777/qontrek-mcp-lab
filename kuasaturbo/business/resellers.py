"""
Reseller Management

Handles reseller CRUD operations, tier management, and commission tracking.
"""

import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from kuasaturbo.database.connection import get_db_connection


class ResellerManager:
    """Manages reseller operations"""
    
    # Tier commission rates
    TIER_RATES = {
        "bronze": 5.0,
        "silver": 10.0,
        "gold": 15.0,
        "platinum": 20.0
    }
    
    @staticmethod
    def generate_reseller_id() -> str:
        """Generate unique reseller ID"""
        return f"res_{uuid.uuid4().hex[:12]}"
    
    @staticmethod
    def create_reseller(
        tenant_id: str,
        company_name: str,
        contact_name: str,
        email: str,
        phone: Optional[str] = None,
        tier: str = "bronze",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create new reseller
        
        Args:
            tenant_id: Tenant identifier
            company_name: Company name
            contact_name: Contact person name
            email: Contact email
            phone: Optional phone number
            tier: Reseller tier (bronze, silver, gold, platinum)
            metadata: Optional metadata
        
        Returns:
            Reseller ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        reseller_id = ResellerManager.generate_reseller_id()
        commission_rate = ResellerManager.TIER_RATES.get(tier, 5.0)
        metadata_json = json.dumps(metadata) if metadata else None
        
        try:
            cursor.execute("""
                INSERT INTO resellers (
                    reseller_id, tenant_id, company_name, contact_name,
                    email, phone, tier, commission_rate, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reseller_id, tenant_id, company_name, contact_name,
                email, phone, tier, commission_rate, metadata_json
            ))
            
            conn.commit()
            
            print(f"[ResellerManager] Created reseller {reseller_id} for tenant {tenant_id} (tier: {tier})")
            return reseller_id
        
        except Exception as e:
            conn.rollback()
            print(f"[ResellerManager] Error creating reseller: {e}")
            raise
    
    @staticmethod
    def get_reseller(reseller_id: str) -> Optional[Dict[str, Any]]:
        """Get reseller by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM resellers
            WHERE reseller_id = ?
        """, (reseller_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def list_resellers(
        tenant_id: str,
        status: Optional[str] = None,
        tier: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List resellers for tenant"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        conditions = ["tenant_id = ?"]
        params = [tenant_id]
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        if tier:
            conditions.append("tier = ?")
            params.append(tier)
        
        params.extend([limit, offset])
        
        query = f"""
            SELECT * FROM resellers
            WHERE {' AND '.join(conditions)}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    @staticmethod
    def update_reseller(
        reseller_id: str,
        company_name: Optional[str] = None,
        contact_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        tier: Optional[str] = None,
        status: Optional[str] = None
    ) -> bool:
        """Update reseller details"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            params = []
            
            if company_name is not None:
                updates.append("company_name = ?")
                params.append(company_name)
            if contact_name is not None:
                updates.append("contact_name = ?")
                params.append(contact_name)
            if email is not None:
                updates.append("email = ?")
                params.append(email)
            if phone is not None:
                updates.append("phone = ?")
                params.append(phone)
            if tier is not None:
                updates.append("tier = ?")
                params.append(tier)
                # Update commission rate based on tier
                updates.append("commission_rate = ?")
                params.append(ResellerManager.TIER_RATES.get(tier, 5.0))
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            
            if not updates:
                return False
            
            updates.append("updated_at = ?")
            params.append(datetime.utcnow().isoformat())
            params.append(reseller_id)
            
            query = f"UPDATE resellers SET {', '.join(updates)} WHERE reseller_id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            
            print(f"[ResellerManager] Updated reseller {reseller_id}")
            return cursor.rowcount > 0
        
        except Exception as e:
            conn.rollback()
            print(f"[ResellerManager] Error updating reseller: {e}")
            return False
    
    @staticmethod
    def delete_reseller(reseller_id: str) -> bool:
        """Delete reseller (soft delete)"""
        return ResellerManager.update_reseller(reseller_id, status="inactive")
    
    @staticmethod
    def record_sale(reseller_id: str, amount: float) -> bool:
        """Record sale and calculate commission"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            reseller = ResellerManager.get_reseller(reseller_id)
            if not reseller:
                return False
            
            commission = amount * (reseller['commission_rate'] / 100.0)
            
            cursor.execute("""
                UPDATE resellers
                SET total_earnings = total_earnings + ?,
                    total_sales = total_sales + 1,
                    updated_at = ?
                WHERE reseller_id = ?
            """, (commission, datetime.utcnow().isoformat(), reseller_id))
            
            conn.commit()
            
            print(f"[ResellerManager] Recorded sale for {reseller_id}: ${amount} (commission: ${commission})")
            return True
        
        except Exception as e:
            conn.rollback()
            print(f"[ResellerManager] Error recording sale: {e}")
            return False
    
    @staticmethod
    def get_earnings_summary(reseller_id: str) -> Dict[str, Any]:
        """Get earnings summary for reseller"""
        reseller = ResellerManager.get_reseller(reseller_id)
        
        if not reseller:
            return {}
        
        return {
            "reseller_id": reseller_id,
            "company_name": reseller['company_name'],
            "tier": reseller['tier'],
            "total_earnings": reseller['total_earnings'],
            "total_sales": reseller['total_sales'],
            "commission_rate": reseller['commission_rate'],
            "average_commission": reseller['total_earnings'] / reseller['total_sales'] if reseller['total_sales'] > 0 else 0.0,
            "status": reseller['status']
        }
