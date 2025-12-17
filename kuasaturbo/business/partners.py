"""
Partner Management

Handles partner CRUD operations, revenue sharing, and referral tracking.
"""

import json
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from kuasaturbo.database.connection import get_db_connection


class PartnerManager:
    """Manages partner operations"""
    
    # Partnership type revenue share rates
    PARTNERSHIP_RATES = {
        "standard": 10.0,
        "premium": 20.0,
        "enterprise": 30.0,
        "strategic": 40.0
    }
    
    @staticmethod
    def generate_partner_id() -> str:
        """Generate unique partner ID"""
        return f"part_{uuid.uuid4().hex[:12]}"
    
    @staticmethod
    def create_partner(
        tenant_id: str,
        company_name: str,
        contact_name: str,
        email: str,
        phone: Optional[str] = None,
        partnership_type: str = "standard",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create new partner
        
        Args:
            tenant_id: Tenant identifier
            company_name: Company name
            contact_name: Contact person name
            email: Contact email
            phone: Optional phone number
            partnership_type: Partnership type (standard, premium, enterprise, strategic)
            metadata: Optional metadata
        
        Returns:
            Partner ID
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        partner_id = PartnerManager.generate_partner_id()
        revenue_share_rate = PartnerManager.PARTNERSHIP_RATES.get(partnership_type, 10.0)
        metadata_json = json.dumps(metadata) if metadata else None
        
        try:
            cursor.execute("""
                INSERT INTO partners (
                    partner_id, tenant_id, company_name, contact_name,
                    email, phone, partnership_type, revenue_share_rate, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                partner_id, tenant_id, company_name, contact_name,
                email, phone, partnership_type, revenue_share_rate, metadata_json
            ))
            
            conn.commit()
            
            print(f"[PartnerManager] Created partner {partner_id} for tenant {tenant_id} (type: {partnership_type})")
            return partner_id
        
        except Exception as e:
            conn.rollback()
            print(f"[PartnerManager] Error creating partner: {e}")
            raise
    
    @staticmethod
    def get_partner(partner_id: str) -> Optional[Dict[str, Any]]:
        """Get partner by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM partners
            WHERE partner_id = ?
        """, (partner_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def list_partners(
        tenant_id: str,
        status: Optional[str] = None,
        partnership_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List partners for tenant"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        conditions = ["tenant_id = ?"]
        params = [tenant_id]
        
        if status:
            conditions.append("status = ?")
            params.append(status)
        if partnership_type:
            conditions.append("partnership_type = ?")
            params.append(partnership_type)
        
        params.extend([limit, offset])
        
        query = f"""
            SELECT * FROM partners
            WHERE {' AND '.join(conditions)}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    @staticmethod
    def update_partner(
        partner_id: str,
        company_name: Optional[str] = None,
        contact_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        partnership_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> bool:
        """Update partner details"""
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
            if partnership_type is not None:
                updates.append("partnership_type = ?")
                params.append(partnership_type)
                # Update revenue share rate based on type
                updates.append("revenue_share_rate = ?")
                params.append(PartnerManager.PARTNERSHIP_RATES.get(partnership_type, 10.0))
            if status is not None:
                updates.append("status = ?")
                params.append(status)
            
            if not updates:
                return False
            
            updates.append("updated_at = ?")
            params.append(datetime.utcnow().isoformat())
            params.append(partner_id)
            
            query = f"UPDATE partners SET {', '.join(updates)} WHERE partner_id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            
            print(f"[PartnerManager] Updated partner {partner_id}")
            return cursor.rowcount > 0
        
        except Exception as e:
            conn.rollback()
            print(f"[PartnerManager] Error updating partner: {e}")
            return False
    
    @staticmethod
    def delete_partner(partner_id: str) -> bool:
        """Delete partner (soft delete)"""
        return PartnerManager.update_partner(partner_id, status="inactive")
    
    @staticmethod
    def record_referral(partner_id: str, revenue: float) -> bool:
        """Record referral and calculate revenue share"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            partner = PartnerManager.get_partner(partner_id)
            if not partner:
                return False
            
            revenue_share = revenue * (partner['revenue_share_rate'] / 100.0)
            
            cursor.execute("""
                UPDATE partners
                SET total_revenue = total_revenue + ?,
                    total_referrals = total_referrals + 1,
                    updated_at = ?
                WHERE partner_id = ?
            """, (revenue_share, datetime.utcnow().isoformat(), partner_id))
            
            conn.commit()
            
            print(f"[PartnerManager] Recorded referral for {partner_id}: ${revenue} (share: ${revenue_share})")
            return True
        
        except Exception as e:
            conn.rollback()
            print(f"[PartnerManager] Error recording referral: {e}")
            return False
    
    @staticmethod
    def get_revenue_summary(partner_id: str) -> Dict[str, Any]:
        """Get revenue summary for partner"""
        partner = PartnerManager.get_partner(partner_id)
        
        if not partner:
            return {}
        
        return {
            "partner_id": partner_id,
            "company_name": partner['company_name'],
            "partnership_type": partner['partnership_type'],
            "total_revenue": partner['total_revenue'],
            "total_referrals": partner['total_referrals'],
            "revenue_share_rate": partner['revenue_share_rate'],
            "average_revenue": partner['total_revenue'] / partner['total_referrals'] if partner['total_referrals'] > 0 else 0.0,
            "status": partner['status']
        }
