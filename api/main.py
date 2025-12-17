#!/usr/bin/env python3
"""
Phase D: Runtime REST API (MVP)
Minimal FastAPI layer exposing dispatcher and runner_v2.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from api.config import API_KEY
from l6.dispatcher_mvp import execute_skill
from l6.runner_v2 import execute_workflow


# FastAPI app
app = FastAPI(
    title="LaunchKit API",
    description="Phase D: Runtime REST API for skills and workflows",
    version="1.0.0"
)

# CORS - simple wildcard for MVP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request models
class SkillExecuteRequest(BaseModel):
    skill_id: str
    payload: Dict[str, Any]


class WorkflowExecuteRequest(BaseModel):
    workflow_id: str
    payload: Dict[str, Any]


# Auth dependency
def verify_api_key(x_api_key: str = Header(None)) -> None:
    """Verify API key from header."""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "failed",
                "error": {
                    "type": "unauthorized",
                    "message": "Missing X-API-Key header"
                }
            }
        )
    
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={
                "status": "failed",
                "error": {
                    "type": "unauthorized",
                    "message": "Invalid API key"
                }
            }
        )


@app.post("/skills/execute")
async def execute_skill_endpoint(
    request: SkillExecuteRequest,
    x_api_key: str = Header(None)
) -> JSONResponse:
    """
    Execute a skill via dispatcher.
    
    Request:
        {
            "skill_id": "launchkit.branding.generate.v1",
            "payload": {...}
        }
    
    Response: Exact envelope from dispatcher_mvp
    """
    # Verify auth
    verify_api_key(x_api_key)
    
    # Execute skill
    result = execute_skill(request.skill_id, request.payload)
    
    # Return envelope as-is
    return JSONResponse(content=result)


@app.post("/workflows/execute")
async def execute_workflow_endpoint(
    request: WorkflowExecuteRequest,
    x_api_key: str = Header(None)
) -> JSONResponse:
    """
    Execute a workflow via runner_v2.
    
    Request:
        {
            "workflow_id": "kuasaturbo.launchkit.v1",
            "payload": {...}
        }
    
    Response: Exact workflow envelope from runner_v2
    """
    # Verify auth
    verify_api_key(x_api_key)
    
    # Execute workflow
    result = execute_workflow(request.workflow_id, request.payload)
    
    # Return envelope as-is
    return JSONResponse(content=result)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "phase": "D"}


# Custom exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Return consistent error envelopes."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
