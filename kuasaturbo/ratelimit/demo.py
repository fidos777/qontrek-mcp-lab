#!/usr/bin/env python3
"""
Rate Limiting Demo Script

Demonstrates rate limiting functionality with visual output.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.ratelimit.ratelimit_service import check_rate_limit, reset_state_for_testing
from pathlib import Path


def demo_basic_rate_limiting():
    """Demonstrate basic rate limiting"""
    print("\n" + "="*70)
    print("DEMO 1: Basic Rate Limiting")
    print("="*70)
    print("Endpoint: service_execute (limit: 20/minute)")
    print()
    
    # Clean state
    reset_state_for_testing()
    state_file = Path(__file__).parent / "ratelimit.json"
    if state_file.exists():
        state_file.unlink()
    
    tenant_id = "demo_tenant"
    endpoint = "service_execute"
    
    # Make 22 requests
    for i in range(1, 23):
        allowed, window, limit, count = check_rate_limit(tenant_id, endpoint)
        
        if allowed:
            print(f"  Request {i:2d}: ✅ ALLOWED")
        else:
            print(f"  Request {i:2d}: ❌ BLOCKED - {window} limit ({count}/{limit})")
    
    print()


def demo_multi_tenant_isolation():
    """Demonstrate multi-tenant isolation"""
    print("\n" + "="*70)
    print("DEMO 2: Multi-Tenant Isolation")
    print("="*70)
    print("Two tenants making requests to same endpoint")
    print()
    
    # Clean state
    reset_state_for_testing()
    state_file = Path(__file__).parent / "ratelimit.json"
    if state_file.exists():
        state_file.unlink()
    
    endpoint = "creative_generate"  # 10/minute limit
    
    # Tenant A makes 10 requests (hits limit)
    print("Tenant A:")
    for i in range(1, 12):
        allowed, window, limit, count = check_rate_limit("tenant_a", endpoint)
        if allowed:
            print(f"  Request {i:2d}: ✅ ALLOWED")
        else:
            print(f"  Request {i:2d}: ❌ BLOCKED - {window} limit ({count}/{limit})")
    
    print()
    
    # Tenant B makes requests (should be allowed - independent counters)
    print("Tenant B (independent counters):")
    for i in range(1, 6):
        allowed, window, limit, count = check_rate_limit("tenant_b", endpoint)
        if allowed:
            print(f"  Request {i:2d}: ✅ ALLOWED")
        else:
            print(f"  Request {i:2d}: ❌ BLOCKED - {window} limit ({count}/{limit})")
    
    print()


def demo_endpoint_specific_limits():
    """Demonstrate endpoint-specific limits"""
    print("\n" + "="*70)
    print("DEMO 3: Endpoint-Specific Limits")
    print("="*70)
    print("Same tenant, different endpoints with different limits")
    print()
    
    # Clean state
    reset_state_for_testing()
    state_file = Path(__file__).parent / "ratelimit.json"
    if state_file.exists():
        state_file.unlink()
    
    tenant_id = "demo_tenant"
    
    # Creative generate: 10/minute
    print("creative_generate (10/minute):")
    for i in range(1, 12):
        allowed, window, limit, count = check_rate_limit(tenant_id, "creative_generate")
        if allowed:
            print(f"  Request {i:2d}: ✅ ALLOWED")
        else:
            print(f"  Request {i:2d}: ❌ BLOCKED - {window} limit ({count}/{limit})")
    
    print()
    
    # Service execute: 20/minute (independent counter)
    print("service_execute (20/minute - independent counter):")
    for i in range(1, 6):
        allowed, window, limit, count = check_rate_limit(tenant_id, "service_execute")
        if allowed:
            print(f"  Request {i:2d}: ✅ ALLOWED")
        else:
            print(f"  Request {i:2d}: ❌ BLOCKED - {window} limit ({count}/{limit})")
    
    print()


def demo_summary():
    """Print summary"""
    print("\n" + "="*70)
    print("RATE LIMITING SUMMARY")
    print("="*70)
    print()
    print("✅ Per-tenant isolation: Each tenant has independent counters")
    print("✅ Per-endpoint isolation: Each endpoint has independent counters")
    print("✅ Endpoint-specific limits: Different endpoints have different limits")
    print("✅ Multi-window enforcement: Minute, hour, and day limits")
    print("✅ JSON persistence: State saved to ratelimit.json")
    print("✅ Automatic window resets: No cron jobs required")
    print()
    print("Configuration:")
    print("  - service_execute: 20/min, 200/hr, 2000/day")
    print("  - creative_generate: 10/min, 100/hr, 1000/day")
    print("  - default: 30/min, 500/hr, 5000/day")
    print()
    print("="*70)
    print()


if __name__ == "__main__":
    print("\n🚀 KuasaTurbo Rate Limiting Demo")
    print("Phase XVI - Rate Limiting Layer")
    
    demo_basic_rate_limiting()
    demo_multi_tenant_isolation()
    demo_endpoint_specific_limits()
    demo_summary()
    
    print("✅ Demo complete!")
    print()
