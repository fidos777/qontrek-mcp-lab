"""
KuasaTurbo REST Gateway (Phase XI)

Lightweight REST API for KuasaTurbo microservices.
Provides single endpoint for executing widget-workflow-persona chains.
"""

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import sys
import os

# Add parent directories to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.api.validators import validate_service_request
from kuasaturbo.api.router import execute_service
from kuasaturbo.shared.config import API_KEY

app = FastAPI(
    title="KuasaTurbo Gateway",
    description="Lightweight microservices platform for AI-powered business automation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ServiceRequest(BaseModel):
    """Request model for service execution"""
    service_id: str = Field(..., description="Service ID from registry")
    payload: Dict[str, Any] = Field(..., description="Widget field values")
    persona_override: Optional[str] = Field(None, description="Optional persona override")
    model_override: Optional[str] = Field(None, description="Optional model override")


class ServiceResponse(BaseModel):
    """Response model for service execution"""
    status: str
    service_id: str
    workflow_id: str
    persona_id: str
    output: Dict[str, Any]
    metadata: Dict[str, Any]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "KuasaTurbo Gateway",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "execute": "POST /v1/execute",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "components": {
            "api": "operational",
            "validators": "operational",
            "router": "operational"
        }
    }


@app.post("/v1/execute", response_model=ServiceResponse)
async def execute(
    request: ServiceRequest,
    x_api_key: str = Header(..., alias="X-API-Key")
):
    """
    Execute a KuasaTurbo microservice
    
    Flow:
    1. Validate API key
    2. Validate service request (service exists, required fields present)
    3. Load widget, workflow, persona
    4. Build prompt from workflow + persona
    5. Execute AI generation (mock or real)
    6. Return structured output
    """
    # Validate API key
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Validate request
    validation_result = validate_service_request(
        request.service_id,
        request.payload,
        request.persona_override,
        request.model_override
    )
    
    if not validation_result["valid"]:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Validation failed",
                "errors": validation_result["errors"]
            }
        )
    
    # Execute service
    try:
        result = execute_service(
            service_id=request.service_id,
            payload=request.payload,
            persona_override=request.persona_override,
            model_override=request.model_override
        )
        
        return ServiceResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Service execution failed",
                "message": str(e)
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
