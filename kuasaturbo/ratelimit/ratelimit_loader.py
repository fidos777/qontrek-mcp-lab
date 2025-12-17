"""
Rate Limit Loader

Handles configuration loading and state persistence for rate limiting.
JSON-based storage only - NO database.
"""

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

import yaml

from .models import RateLimitConfig, RateLimitUsage, RateLimitState, RateLimitStore


# File paths
RATELIMIT_DIR = Path(__file__).parent
CONFIG_PATH = RATELIMIT_DIR / "default_config.yaml"
STATE_PATH = RATELIMIT_DIR / "ratelimit.json"


def load_config() -> Dict[str, RateLimitConfig]:
    """
    Load rate limit configuration from YAML file
    
    Returns:
        Dict mapping endpoint keys to RateLimitConfig objects
    """
    print(f"[RateLimitLoader] Loading config from {CONFIG_PATH}")
    
    if not CONFIG_PATH.exists():
        print(f"[RateLimitLoader] Config file not found, using hardcoded defaults")
        return {
            "default": RateLimitConfig(minute=30, hour=500, day=5000),
            "service_execute": RateLimitConfig(minute=20, hour=200, day=2000),
            "creative_generate": RateLimitConfig(minute=10, hour=100, day=1000)
        }
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            raw_config = yaml.safe_load(f)
        
        configs = {}
        for key, limits in raw_config.items():
            configs[key] = RateLimitConfig(**limits)
        
        print(f"[RateLimitLoader] Loaded {len(configs)} endpoint configurations")
        return configs
    
    except Exception as e:
        print(f"[RateLimitLoader] Error loading config: {e}")
        print(f"[RateLimitLoader] Falling back to hardcoded defaults")
        return {
            "default": RateLimitConfig(minute=30, hour=500, day=5000)
        }


def load_state() -> RateLimitStore:
    """
    Load rate limit state from JSON file
    
    Returns:
        RateLimitStore with current state or empty store if file doesn't exist
    """
    print(f"[RateLimitLoader] Loading state from {STATE_PATH}")
    
    if not STATE_PATH.exists():
        print(f"[RateLimitLoader] State file not found, initializing empty store")
        return RateLimitStore(states={})
    
    try:
        with open(STATE_PATH, 'r') as f:
            data = json.load(f)
        
        store = RateLimitStore(**data)
        print(f"[RateLimitLoader] Loaded {len(store.states)} rate limit states")
        return store
    
    except Exception as e:
        print(f"[RateLimitLoader] Error loading state: {e}")
        print(f"[RateLimitLoader] Initializing empty store")
        return RateLimitStore(states={})


def save_state(store: RateLimitStore) -> None:
    """
    Persist rate limit state to JSON file
    
    Args:
        store: RateLimitStore to persist
    """
    try:
        # Ensure directory exists
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # Write atomically using temp file
        temp_path = STATE_PATH.with_suffix('.tmp')
        with open(temp_path, 'w') as f:
            # Support both Pydantic v1 and v2
            if hasattr(store, 'model_dump'):
                data = store.model_dump()
            else:
                data = store.dict()
            json.dump(data, f, indent=2)
        
        # Atomic rename
        temp_path.replace(STATE_PATH)
        
        print(f"[RateLimitLoader] Saved {len(store.states)} rate limit states")
    
    except Exception as e:
        print(f"[RateLimitLoader] Error saving state: {e}")


def get_or_create_usage(store: RateLimitStore, tenant_id: str, endpoint: str) -> RateLimitUsage:
    """
    Get existing usage or create new usage counters
    
    Args:
        store: RateLimitStore to query
        tenant_id: Tenant identifier
        endpoint: Endpoint key
    
    Returns:
        RateLimitUsage for the tenant-endpoint combination
    """
    key = store.get_key(tenant_id, endpoint)
    
    if key in store.states:
        return store.states[key].usage
    
    # Create new usage with current time windows
    now = int(time.time())
    now_dt = datetime.fromtimestamp(now, tz=timezone.utc)
    
    # Calculate window reset times
    minute_reset = int(datetime(now_dt.year, now_dt.month, now_dt.day, 
                                 now_dt.hour, now_dt.minute, 0, tzinfo=timezone.utc).timestamp()) + 60
    hour_reset = int(datetime(now_dt.year, now_dt.month, now_dt.day, 
                              now_dt.hour, 0, 0, tzinfo=timezone.utc).timestamp()) + 3600
    day_reset = int(datetime(now_dt.year, now_dt.month, now_dt.day, 
                             0, 0, 0, tzinfo=timezone.utc).timestamp()) + 86400
    
    usage = RateLimitUsage(
        minute_count=0,
        hour_count=0,
        day_count=0,
        minute_reset_at=minute_reset,
        hour_reset_at=hour_reset,
        day_reset_at=day_reset
    )
    
    # Store new state
    state = RateLimitState(tenant_id=tenant_id, endpoint=endpoint, usage=usage)
    store.states[key] = state
    
    print(f"[RateLimitLoader] Created new usage for {key}")
    return usage


def reset_if_new_window(usage: RateLimitUsage) -> RateLimitUsage:
    """
    Reset counters if time windows have expired
    
    Args:
        usage: Current usage counters
    
    Returns:
        Updated usage with reset counters if needed
    """
    now = int(time.time())
    now_dt = datetime.fromtimestamp(now, tz=timezone.utc)
    
    # Check and reset minute window
    if now >= usage.minute_reset_at:
        usage.minute_count = 0
        usage.minute_reset_at = int(datetime(now_dt.year, now_dt.month, now_dt.day,
                                             now_dt.hour, now_dt.minute, 0, 
                                             tzinfo=timezone.utc).timestamp()) + 60
        print(f"[RateLimitLoader] Reset minute window")
    
    # Check and reset hour window
    if now >= usage.hour_reset_at:
        usage.hour_count = 0
        usage.hour_reset_at = int(datetime(now_dt.year, now_dt.month, now_dt.day,
                                           now_dt.hour, 0, 0, 
                                           tzinfo=timezone.utc).timestamp()) + 3600
        print(f"[RateLimitLoader] Reset hour window")
    
    # Check and reset day window
    if now >= usage.day_reset_at:
        usage.day_count = 0
        usage.day_reset_at = int(datetime(now_dt.year, now_dt.month, now_dt.day,
                                          0, 0, 0, 
                                          tzinfo=timezone.utc).timestamp()) + 86400
        print(f"[RateLimitLoader] Reset day window")
    
    return usage
