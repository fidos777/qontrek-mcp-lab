"""
Rate Limit Service

Core rate limiting enforcement logic with automatic window resets.
Raises HTTPException(429) when limits are exceeded.
"""

from typing import Dict, Optional, Tuple
from fastapi import HTTPException

from .models import RateLimitConfig, RateLimitUsage, RateLimitStore
from .ratelimit_loader import (
    load_config,
    load_state,
    save_state,
    get_or_create_usage,
    reset_if_new_window
)


# Global state (loaded once at module import)
_config_cache: Optional[Dict[str, RateLimitConfig]] = None
_state_cache: Optional[RateLimitStore] = None


def _get_config() -> Dict[str, RateLimitConfig]:
    """Get cached configuration or load it"""
    global _config_cache
    if _config_cache is None:
        _config_cache = load_config()
    return _config_cache


def _get_state() -> RateLimitStore:
    """Get cached state or load it"""
    global _state_cache
    if _state_cache is None:
        _state_cache = load_state()
    return _state_cache


def _get_limits_for_endpoint(endpoint: str) -> RateLimitConfig:
    """
    Get rate limit configuration for an endpoint
    
    Args:
        endpoint: Endpoint key (e.g., "service_execute", "creative_generate")
    
    Returns:
        RateLimitConfig for the endpoint or default limits
    """
    config = _get_config()
    
    if endpoint in config:
        print(f"[RateLimitService] Using specific limits for {endpoint}")
        return config[endpoint]
    
    print(f"[RateLimitService] Using default limits for {endpoint}")
    return config.get("default", RateLimitConfig(minute=30, hour=500, day=5000))


def check_rate_limit(tenant_id: str, endpoint: str) -> Tuple[bool, Optional[str], Optional[int], Optional[int]]:
    """
    Check if request is within rate limits
    
    Args:
        tenant_id: Tenant identifier
        endpoint: Endpoint key
    
    Returns:
        Tuple of (allowed, window_type, limit_value, current_count)
        - allowed: True if within limits, False if exceeded
        - window_type: "minute", "hour", or "day" if exceeded, None if allowed
        - limit_value: The limit that was exceeded, None if allowed
        - current_count: Current count in the exceeded window, None if allowed
    """
    print(f"[RateLimitService] Checking rate limit for tenant={tenant_id}, endpoint={endpoint}")
    
    # Get configuration and state
    limits = _get_limits_for_endpoint(endpoint)
    store = _get_state()
    
    # Get or create usage counters
    usage = get_or_create_usage(store, tenant_id, endpoint)
    
    # Reset expired windows
    usage = reset_if_new_window(usage)
    
    # Check minute limit
    if usage.minute_count >= limits.minute:
        print(f"[RateLimitService] Minute limit exceeded: {usage.minute_count}/{limits.minute}")
        return False, "minute", limits.minute, usage.minute_count
    
    # Check hour limit
    if usage.hour_count >= limits.hour:
        print(f"[RateLimitService] Hour limit exceeded: {usage.hour_count}/{limits.hour}")
        return False, "hour", limits.hour, usage.hour_count
    
    # Check day limit
    if usage.day_count >= limits.day:
        print(f"[RateLimitService] Day limit exceeded: {usage.day_count}/{limits.day}")
        return False, "day", limits.day, usage.day_count
    
    # All checks passed - increment counters
    print(f"[RateLimitService] Rate limit check passed, incrementing counters")
    increment_usage(tenant_id, endpoint)
    
    return True, None, None, None


def increment_usage(tenant_id: str, endpoint: str) -> None:
    """
    Increment usage counters for a tenant-endpoint combination
    
    Args:
        tenant_id: Tenant identifier
        endpoint: Endpoint key
    """
    store = _get_state()
    usage = get_or_create_usage(store, tenant_id, endpoint)
    
    # Increment all windows
    usage.minute_count += 1
    usage.hour_count += 1
    usage.day_count += 1
    
    print(f"[RateLimitService] Incremented counters: minute={usage.minute_count}, hour={usage.hour_count}, day={usage.day_count}")
    
    # Persist to disk
    save_state(store)


def enforce_rate_limit(tenant_id: str, endpoint: str) -> None:
    """
    Enforce rate limit and raise HTTPException if exceeded
    
    This is the main function to call from endpoints.
    
    Args:
        tenant_id: Tenant identifier
        endpoint: Endpoint key (e.g., "service_execute", "creative_generate", "default")
    
    Raises:
        HTTPException: 429 status code if rate limit exceeded
    """
    allowed, window_type, limit_value, current_count = check_rate_limit(tenant_id, endpoint)
    
    if not allowed:
        error_response = {
            "error": "rate_limit_exceeded",
            "details": {
                "tenant_id": tenant_id,
                "endpoint": endpoint,
                "limit": limit_value,
                "window": window_type,
                "current_count": current_count
            }
        }
        
        print(f"[RateLimitService] Rate limit exceeded, raising 429")
        raise HTTPException(status_code=429, detail=error_response)
    
    print(f"[RateLimitService] Rate limit enforcement passed")


def reset_state_for_testing() -> None:
    """
    Reset global state cache for testing purposes
    
    WARNING: Only use in tests!
    """
    global _config_cache, _state_cache
    _config_cache = None
    _state_cache = None
    print("[RateLimitService] State cache reset for testing")
