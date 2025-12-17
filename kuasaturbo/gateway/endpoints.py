"""
KuasaTurbo Gateway Endpoints (Phase XIV)

Comprehensive REST API endpoints for KuasaTurbo platform.
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.gateway.validators import (
    validate_service,
    validate_widget_id,
    validate_model_id,
    validate_creative_generation_request
)
from kuasaturbo.gateway.router import (
    get_widgets_list,
    get_widget_details,
    execute_service_endpoint,
    get_models_list,
    get_model_details,
    resolve_model_endpoint,
    get_creative_tasks_list,
    get_creative_styles_list,
    execute_creative_generation
)
from kuasaturbo.shared.config import API_KEY
from kuasaturbo.auth.auth_service import validate_api_key, generate_jwt_token, validate_jwt_token, get_tenant_context
from kuasaturbo.auth.models import TokenRequest, TokenResponse, TenantInfo
from kuasaturbo.ratelimit import enforce_rate_limit
from kuasaturbo.business.endpoints import business_router
from kuasaturbo.platform.endpoints import platform_router

app = FastAPI(
    title="KuasaTurbo Gateway API",
    description="Comprehensive endpoint layer for KuasaTurbo microservices platform (Multi-Tenant)",
    version="3.0.0"
)

# Include routers
app.include_router(business_router)
app.include_router(platform_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# REQUEST/RESPONSE MODELS
# ============================================================

class ServiceExecuteRequest(BaseModel):
    """Request model for service execution"""
    service_id: str = Field(..., description="Service ID from registry")
    payload: Dict[str, Any] = Field(..., description="Widget field values")
    persona_override: Optional[str] = Field(None, description="Optional persona override")
    model_override: Optional[str] = Field(None, description="Optional model override")


class ModelResolveRequest(BaseModel):
    """Request model for model resolution"""
    workflow_id: Optional[str] = Field(None, description="Optional workflow ID")
    persona_id: Optional[str] = Field(None, description="Optional persona ID")
    model_override: Optional[str] = Field(None, description="Optional model override")


class CreativeGenerateRequest(BaseModel):
    """Request model for creative generation"""
    task_type: str = Field(..., description="Creative task type")
    payload: Dict[str, Any] = Field(..., description="Task-specific input data")
    persona_id: Optional[str] = Field(None, description="Optional persona ID")
    style_override: Optional[str] = Field(None, description="Optional style override")
    model_override: Optional[str] = Field(None, description="Optional model override")


# ============================================================
# AUTHENTICATION HELPER
# ============================================================

def authenticate_request(x_api_key: str) -> dict:
    """
    Authenticate request and return tenant context
    
    Args:
        x_api_key: API key from header
    
    Returns:
        Tenant context dict
    
    Raises:
        HTTPException: If authentication fails
    """
    tenant = validate_api_key(x_api_key)
    
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return {
        "tenant_id": tenant.tenant_id,
        "tenant_name": tenant.name,
        "roles": tenant.roles
    }


# ============================================================
# BASIC ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    """Root endpoint - API information"""
    print("[Endpoint] Root endpoint accessed")
    return {
        "service": "KuasaTurbo Gateway API",
        "version": "3.0.0",
        "phase": "XIX - Platform Layer",
        "status": "operational",
        "endpoints": {
            "basic": {
                "root": "GET /",
                "health": "GET /health"
            },
            "auth": {
                "token": "POST /auth/token",
                "tenant": "GET /auth/tenant"
            },
            "widgets": {
                "list": "GET /widgets",
                "details": "GET /widgets/{widget_id}"
            },
            "services": {
                "execute": "POST /service/execute"
            },
            "models": {
                "list": "GET /models",
                "details": "GET /models/{model_id}",
                "resolve": "POST /models/resolve"
            },
            "creative": {
                "tasks": "GET /creative/tasks",
                "styles": "GET /creative/styles",
                "generate": "POST /creative/generate"
            },
            "business": {
                "consultants": "POST/GET/PUT/DELETE /v1/consultant/*",
                "resellers": "POST/GET/PUT/DELETE /v1/reseller/*",
                "partners": "POST/GET/PUT/DELETE /v1/partner/*"
            },
            "platform": {
                "api_keys": "POST/GET /v1/admin/api-keys",
                "rotate": "POST /v1/admin/api-keys/rotate",
                "revoke": "POST /v1/admin/api-keys/revoke"
            }
        },
        "authentication": "Multi-tenant with API keys, JWT tokens, and scopes"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    print("[Endpoint] Health check accessed")
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "validators": "operational",
            "router": "operational",
            "auth": "operational",
            "widgets": "operational",
            "workflows": "operational",
            "personas": "operational",
            "models": "operational",
            "creative_engine": "operational"
        },
        "mode": "mock",
        "multi_tenant": True
    }


# ============================================================
# AUTHENTICATION ENDPOINTS
# ============================================================

@app.post("/auth/token", response_model=TokenResponse)
async def generate_token(request: TokenRequest):
    """
    Generate JWT token for authenticated user
    
    Flow:
    1. Validate API key
    2. Validate requested role
    3. Generate JWT token
    4. Return token with metadata
    """
    print(f"[Auth] Token generation requested")
    
    # Validate API key and get tenant
    tenant = validate_api_key(request.api_key)
    
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Validate role
    if request.role not in tenant.roles:
        raise HTTPException(
            status_code=403,
            detail=f"Role '{request.role}' not available for tenant '{tenant.tenant_id}'"
        )
    
    # Generate token
    token = generate_jwt_token(
        tenant_id=tenant.tenant_id,
        user_id=request.user_id,
        role=request.role,
        expires_in=3600
    )
    
    if not token:
        raise HTTPException(status_code=500, detail="Token generation failed")
    
    return TokenResponse(
        tenant_id=tenant.tenant_id,
        user_id=request.user_id,
        role=request.role,
        token=token,
        expires_in=3600
    )


@app.get("/auth/tenant", response_model=TenantInfo)
async def get_tenant_info(x_api_key: str = Header(..., alias="X-API-Key")):
    """
    Get tenant information from API key
    
    Returns tenant metadata without sensitive information
    """
    print(f"[Auth] Tenant info requested")
    
    tenant = validate_api_key(x_api_key)
    
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return TenantInfo(
        tenant_id=tenant.tenant_id,
        name=tenant.name,
        status=tenant.status,
        roles=tenant.roles
    )


# ============================================================
# WIDGET ENDPOINTS
# ============================================================

@app.get("/widgets")
async def list_widgets(x_api_key: str = Header(..., alias="X-API-Key")):
    """
    Get list of all available widgets
    
    Returns:
        List of widgets with metadata
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "default")
    
    try:
        result = get_widgets_list()
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to fetch widgets", "message": str(e)}
        )


@app.get("/widgets/{widget_id}")
async def get_widget(
    widget_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Get detailed widget information
    
    Args:
        widget_id: Widget identifier
    
    Returns:
        Widget metadata including fields, workflow, persona
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "default")
    
    # Validate widget exists
    validation = validate_widget_id(widget_id)
    if not validation["valid"]:
        raise HTTPException(status_code=404, detail={"errors": validation["errors"]})
    
    try:
        result = get_widget_details(widget_id)
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to fetch widget details", "message": str(e)}
        )


# ============================================================
# SERVICE EXECUTION ENDPOINT
# ============================================================

@app.post("/service/execute")
async def execute_service(
    request: ServiceExecuteRequest,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Execute a KuasaTurbo microservice
    
    Flow:
    1. Authenticate request (multi-tenant)
    2. Rate limit check
    3. Validate service request
    4. Load widget, workflow, persona
    5. Build prompt and execute AI generation
    6. Return structured output with tenant context
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "service_execute")
    
    # Validate request
    validation_result = validate_service(
        request.service_id,
        request.payload,
        request.persona_override,
        request.model_override
    )
    
    if not validation_result["valid"]:
        raise HTTPException(
            status_code=400,
            detail={"error": "Validation failed", "errors": validation_result["errors"]}
        )
    
    # Execute service
    try:
        result = execute_service_endpoint(
            service_id=request.service_id,
            payload=request.payload,
            persona_override=request.persona_override,
            model_override=request.model_override
        )
        # Add tenant context to result
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Service execution failed", "message": str(e)}
        )


# ============================================================
# MODEL ENDPOINTS
# ============================================================

@app.get("/models")
async def list_models(x_api_key: str = Header(..., alias="X-API-Key")):
    """
    Get list of all available models
    
    Returns:
        List of models with metadata
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "default")
    
    try:
        result = get_models_list()
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to fetch models", "message": str(e)}
        )


@app.get("/models/{model_id}")
async def get_model(
    model_id: str,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Get detailed model information
    
    Args:
        model_id: Model identifier
    
    Returns:
        Model metadata
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "default")
    
    # Validate model exists
    validation = validate_model_id(model_id)
    if not validation["valid"]:
        raise HTTPException(status_code=404, detail={"errors": validation["errors"]})
    
    try:
        result = get_model_details(model_id)
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to fetch model details", "message": str(e)}
        )


@app.post("/models/resolve")
async def resolve_model(
    request: ModelResolveRequest,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Resolve which model to use based on priority order
    
    Priority: override → workflow → persona → global default
    
    Returns:
        {
            "model": str,
            "resolution_source": str,
            "priority_order": list
        }
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "default")
    
    try:
        result = resolve_model_endpoint(
            workflow_id=request.workflow_id,
            persona_id=request.persona_id,
            model_override=request.model_override
        )
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Model resolution failed", "message": str(e)}
        )


# ============================================================
# CREATIVE ENGINE ENDPOINTS
# ============================================================

@app.get("/creative/tasks")
async def list_creative_tasks(x_api_key: str = Header(..., alias="X-API-Key")):
    """
    Get list of all available creative tasks
    
    Returns:
        List of creative tasks with metadata
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "default")
    
    try:
        result = get_creative_tasks_list()
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to fetch creative tasks", "message": str(e)}
        )


@app.get("/creative/styles")
async def list_creative_styles(x_api_key: str = Header(..., alias="X-API-Key")):
    """
    Get list of all available creative styles
    
    Returns:
        List of creative styles with metadata
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "default")
    
    try:
        result = get_creative_styles_list()
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Failed to fetch creative styles", "message": str(e)}
        )


@app.post("/creative/generate")
async def generate_creative(
    request: CreativeGenerateRequest,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Execute creative generation task
    
    Supports:
    - Thumbnail generation
    - Product renders
    - Story infographics
    - Car visualizations
    - Image cleanup
    
    All operations run in MOCK MODE (no external API calls)
    """
    # Authenticate request
    tenant_context = authenticate_request(x_api_key)
    
    # Rate limit check
    enforce_rate_limit(tenant_context["tenant_id"], "creative_generate")
    
    # Validate request
    validation_result = validate_creative_generation_request(request.dict())
    if not validation_result["valid"]:
        raise HTTPException(
            status_code=400,
            detail={"error": "Validation failed", "errors": validation_result["errors"]}
        )
    
    # Execute generation
    try:
        result = execute_creative_generation(
            task_type=request.task_type,
            payload=request.payload,
            persona_id=request.persona_id,
            style_override=request.style_override,
            model_override=request.model_override
        )
        # Add tenant context
        result["tenant"] = tenant_context
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Creative generation failed", "message": str(e)}
        )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8082)
