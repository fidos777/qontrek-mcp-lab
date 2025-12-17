"""
Business Layer API Endpoints (Phase XVIII)

Provides REST API for consultant, reseller, and partner management.
"""

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional, List

from .consultants import ConsultantManager
from .resellers import ResellerManager
from .partners import PartnerManager
from kuasaturbo.auth.auth_service import validate_api_key


# Create router
business_router = APIRouter(prefix="/v1", tags=["business"])


# ============================================================
# REQUEST/RESPONSE MODELS
# ============================================================

class ConsultantCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    commission_rate: float = 10.0


class ConsultantUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    commission_rate: Optional[float] = None
    status: Optional[str] = None


class ResellerCreate(BaseModel):
    company_name: str
    contact_name: str
    email: str
    phone: Optional[str] = None
    tier: str = "bronze"


class ResellerUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tier: Optional[str] = None
    status: Optional[str] = None


class PartnerCreate(BaseModel):
    company_name: str
    contact_name: str
    email: str
    phone: Optional[str] = None
    partnership_type: str = "standard"


class PartnerUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    partnership_type: Optional[str] = None
    status: Optional[str] = None


class SaleRecord(BaseModel):
    amount: float


class ReferralRecord(BaseModel):
    revenue: float


# ============================================================
# CONSULTANT ENDPOINTS
# ============================================================

@business_router.post("/consultant")
async def create_consultant(
    data: ConsultantCreate,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Create new consultant"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    consultant_id = ConsultantManager.create_consultant(
        tenant_id=tenant.tenant_id,
        name=data.name,
        email=data.email,
        phone=data.phone,
        commission_rate=data.commission_rate
    )
    
    return {
        "consultant_id": consultant_id,
        "status": "created"
    }


@business_router.get("/consultant/{consultant_id}")
async def get_consultant(
    consultant_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Get consultant details"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    consultant = ConsultantManager.get_consultant(consultant_id)
    if not consultant:
        raise HTTPException(status_code=404, detail="Consultant not found")
    
    # Verify tenant ownership
    if consultant['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return consultant


@business_router.get("/consultant")
async def list_consultants(
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """List consultants"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    consultants = ConsultantManager.list_consultants(
        tenant_id=tenant.tenant_id,
        status=status,
        limit=limit,
        offset=offset
    )
    
    return {
        "consultants": consultants,
        "count": len(consultants)
    }


@business_router.put("/consultant/{consultant_id}")
async def update_consultant(
    consultant_id: str,
    data: ConsultantUpdate,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Update consultant"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Verify ownership
    consultant = ConsultantManager.get_consultant(consultant_id)
    if not consultant or consultant['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Consultant not found")
    
    success = ConsultantManager.update_consultant(
        consultant_id=consultant_id,
        name=data.name,
        email=data.email,
        phone=data.phone,
        commission_rate=data.commission_rate,
        status=data.status
    )
    
    return {"status": "updated" if success else "failed"}


@business_router.delete("/consultant/{consultant_id}")
async def delete_consultant(
    consultant_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Delete consultant"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Verify ownership
    consultant = ConsultantManager.get_consultant(consultant_id)
    if not consultant or consultant['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Consultant not found")
    
    success = ConsultantManager.delete_consultant(consultant_id)
    return {"status": "deleted" if success else "failed"}


@business_router.post("/consultant/{consultant_id}/sale")
async def record_consultant_sale(
    consultant_id: str,
    data: SaleRecord,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Record sale for consultant"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Verify ownership
    consultant = ConsultantManager.get_consultant(consultant_id)
    if not consultant or consultant['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Consultant not found")
    
    success = ConsultantManager.record_sale(consultant_id, data.amount)
    return {"status": "recorded" if success else "failed"}


@business_router.get("/consultant/{consultant_id}/earnings")
async def get_consultant_earnings(
    consultant_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Get consultant earnings summary"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Verify ownership
    consultant = ConsultantManager.get_consultant(consultant_id)
    if not consultant or consultant['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Consultant not found")
    
    summary = ConsultantManager.get_earnings_summary(consultant_id)
    return summary


# ============================================================
# RESELLER ENDPOINTS
# ============================================================

@business_router.post("/reseller")
async def create_reseller(
    data: ResellerCreate,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Create new reseller"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    reseller_id = ResellerManager.create_reseller(
        tenant_id=tenant.tenant_id,
        company_name=data.company_name,
        contact_name=data.contact_name,
        email=data.email,
        phone=data.phone,
        tier=data.tier
    )
    
    return {
        "reseller_id": reseller_id,
        "status": "created"
    }


@business_router.get("/reseller/{reseller_id}")
async def get_reseller(
    reseller_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Get reseller details"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    reseller = ResellerManager.get_reseller(reseller_id)
    if not reseller:
        raise HTTPException(status_code=404, detail="Reseller not found")
    
    if reseller['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return reseller


@business_router.get("/reseller")
async def list_resellers(
    status: Optional[str] = None,
    tier: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """List resellers"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    resellers = ResellerManager.list_resellers(
        tenant_id=tenant.tenant_id,
        status=status,
        tier=tier,
        limit=limit,
        offset=offset
    )
    
    return {
        "resellers": resellers,
        "count": len(resellers)
    }


@business_router.put("/reseller/{reseller_id}")
async def update_reseller(
    reseller_id: str,
    data: ResellerUpdate,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Update reseller"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    reseller = ResellerManager.get_reseller(reseller_id)
    if not reseller or reseller['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Reseller not found")
    
    success = ResellerManager.update_reseller(
        reseller_id=reseller_id,
        company_name=data.company_name,
        contact_name=data.contact_name,
        email=data.email,
        phone=data.phone,
        tier=data.tier,
        status=data.status
    )
    
    return {"status": "updated" if success else "failed"}


@business_router.delete("/reseller/{reseller_id}")
async def delete_reseller(
    reseller_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Delete reseller"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    reseller = ResellerManager.get_reseller(reseller_id)
    if not reseller or reseller['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Reseller not found")
    
    success = ResellerManager.delete_reseller(reseller_id)
    return {"status": "deleted" if success else "failed"}


@business_router.post("/reseller/{reseller_id}/sale")
async def record_reseller_sale(
    reseller_id: str,
    data: SaleRecord,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Record sale for reseller"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    reseller = ResellerManager.get_reseller(reseller_id)
    if not reseller or reseller['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Reseller not found")
    
    success = ResellerManager.record_sale(reseller_id, data.amount)
    return {"status": "recorded" if success else "failed"}


@business_router.get("/reseller/{reseller_id}/earnings")
async def get_reseller_earnings(
    reseller_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Get reseller earnings summary"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    reseller = ResellerManager.get_reseller(reseller_id)
    if not reseller or reseller['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Reseller not found")
    
    summary = ResellerManager.get_earnings_summary(reseller_id)
    return summary


# ============================================================
# PARTNER ENDPOINTS
# ============================================================

@business_router.post("/partner")
async def create_partner(
    data: PartnerCreate,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Create new partner"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    partner_id = PartnerManager.create_partner(
        tenant_id=tenant.tenant_id,
        company_name=data.company_name,
        contact_name=data.contact_name,
        email=data.email,
        phone=data.phone,
        partnership_type=data.partnership_type
    )
    
    return {
        "partner_id": partner_id,
        "status": "created"
    }


@business_router.get("/partner/{partner_id}")
async def get_partner(
    partner_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Get partner details"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    partner = PartnerManager.get_partner(partner_id)
    if not partner:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    if partner['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return partner


@business_router.get("/partner")
async def list_partners(
    status: Optional[str] = None,
    partnership_type: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """List partners"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    partners = PartnerManager.list_partners(
        tenant_id=tenant.tenant_id,
        status=status,
        partnership_type=partnership_type,
        limit=limit,
        offset=offset
    )
    
    return {
        "partners": partners,
        "count": len(partners)
    }


@business_router.put("/partner/{partner_id}")
async def update_partner(
    partner_id: str,
    data: PartnerUpdate,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Update partner"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    partner = PartnerManager.get_partner(partner_id)
    if not partner or partner['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    success = PartnerManager.update_partner(
        partner_id=partner_id,
        company_name=data.company_name,
        contact_name=data.contact_name,
        email=data.email,
        phone=data.phone,
        partnership_type=data.partnership_type,
        status=data.status
    )
    
    return {"status": "updated" if success else "failed"}


@business_router.delete("/partner/{partner_id}")
async def delete_partner(
    partner_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Delete partner"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    partner = PartnerManager.get_partner(partner_id)
    if not partner or partner['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    success = PartnerManager.delete_partner(partner_id)
    return {"status": "deleted" if success else "failed"}


@business_router.post("/partner/{partner_id}/referral")
async def record_partner_referral(
    partner_id: str,
    data: ReferralRecord,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Record referral for partner"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    partner = PartnerManager.get_partner(partner_id)
    if not partner or partner['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    success = PartnerManager.record_referral(partner_id, data.revenue)
    return {"status": "recorded" if success else "failed"}


@business_router.get("/partner/{partner_id}/revenue")
async def get_partner_revenue(
    partner_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """Get partner revenue summary"""
    tenant = validate_api_key(x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    partner = PartnerManager.get_partner(partner_id)
    if not partner or partner['tenant_id'] != tenant.tenant_id:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    summary = PartnerManager.get_revenue_summary(partner_id)
    return summary
