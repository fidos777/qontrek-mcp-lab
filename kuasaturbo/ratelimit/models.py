"""
Rate Limiting Data Models

Pydantic models for rate limit configuration and state tracking.
"""

from pydantic import BaseModel, Field
from typing import Dict


class RateLimitConfig(BaseModel):
    """Rate limit configuration for an endpoint"""
    minute: int = Field(..., description="Requests allowed per minute")
    hour: int = Field(..., description="Requests allowed per hour")
    day: int = Field(..., description="Requests allowed per day")


class RateLimitUsage(BaseModel):
    """Current usage counters for a tenant-endpoint combination"""
    minute_count: int = Field(default=0, description="Requests in current minute")
    hour_count: int = Field(default=0, description="Requests in current hour")
    day_count: int = Field(default=0, description="Requests in current day")
    
    minute_reset_at: int = Field(..., description="Unix timestamp for minute window reset")
    hour_reset_at: int = Field(..., description="Unix timestamp for hour window reset")
    day_reset_at: int = Field(..., description="Unix timestamp for day window reset")


class RateLimitState(BaseModel):
    """Complete rate limit state for a tenant-endpoint"""
    tenant_id: str = Field(..., description="Tenant identifier")
    endpoint: str = Field(..., description="Endpoint key")
    usage: RateLimitUsage = Field(..., description="Current usage counters")


class RateLimitStore(BaseModel):
    """Root structure for ratelimit.json storage"""
    states: Dict[str, RateLimitState] = Field(default_factory=dict, description="Tenant-endpoint states")
    
    def get_key(self, tenant_id: str, endpoint: str) -> str:
        """Generate storage key for tenant-endpoint combination"""
        return f"{tenant_id}:{endpoint}"
