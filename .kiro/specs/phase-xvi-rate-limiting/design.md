# Design Document: Phase XVI - Rate Limiting Layer

## Executive Summary

This document provides the technical design for implementing a lightweight, per-tenant, per-endpoint rate limiting system for KuasaTurbo. The design maintains strict architectural boundaries by avoiding governance features while providing robust request throttling capabilities.

**Key Design Principles:**
- Lightweight and stateless (except counters)
- Mock storage only (JSON files)
- No governance contamination
- Transparent integration with existing endpoints
- Multi-tenant isolation

---

## Architecture Overview

### System Context

```
┌─────────────────────────────────────────────────────────────┐
│                    KuasaTurbo Platform                       │
│                                                              │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   Gateway    │─────▶│  Auth Layer  │                    │
│  │  (Phase XIV) │      │  (Phase XV)  │                    │
│  └──────┬───────┘      └──────┬───────┘                    │
│         │                     │                             │
│         │                     ▼                             │
│         │              ┌──────────────┐                     │
│         └─────────────▶│ Rate Limiter │◀─── NEW (Phase XVI)│
│                        │   (Phase XVI)│                     │
│                        └──────┬───────┘                     │
│                               │                             │
│                               ▼                             │
│                        ┌──────────────┐                     │
│                        │  Endpoints   │                     │
│                        │  Execution   │                     │
│                        └──────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

```
kuasaturbo/ratelimit/
├── __init__.py
├── config.py              # Load YAML configuration
├── counter.py             # Counter management & persistence
├── limiter.py             # Rate limit enforcement logic
├── models.py              # Data structures
├── config.yaml            # Rate limit configuration
└── ratelimit.json         # Runtime state (auto-generated)
```

---

## Data Models

### Configuration Model (YAML)

```yaml
# kuasaturbo/ratelimit/config.yaml

default_limits:
  per_minute: 60
  per_hour: 1000
  per_day: 10000

endpoint_limits:
  "/service/execute":
    per_minute: 10
    per_hour: 100
    per_day: 1000
  
  "/creative/generate":
    per_minute: 5
    per_hour: 50
    per_day: 500
  
  "/widgets":
    per_minute: 100
    per_hour: 1000
    per_day: 10000
  
  "/models/resolve":
    per_minute: 20
    per_hour: 200
    per_day: 2000

# Health and auth endpoints are unlimited (not rate limited)
unlimited_endpoints:
  - "/"
  - "/health"
  - "/auth/token"
  - "/auth/tenant"
```

### State Model (JSON)

```json
{
  "counters": {
    "voltek:/service/execute": {
      "minute": {
        "count": 5,
        "window_start": "2025-12-08T10:45:00Z"
      },
      "hour": {
        "count": 42,
        "window_start": "2025-12-08T10:00:00Z"
      },
      "day": {
        "count": 156,
        "window_start": "2025-12-08T00:00:00Z"
      }
    },
    "default:/creative/generate": {
      "minute": {
        "count": 2,
        "window_start": "2025-12-08T10:45:00Z"
      },
      "hour": {
        "count": 15,
        "window_start": "2025-12-08T10:00:00Z"
      },
      "day": {
        "count": 89,
        "window_start": "2025-12-08T00:00:00Z"
      }
    }
  },
  "last_updated": "2025-12-08T10:45:23Z"
}
```

### Python Data Models

```python
# kuasaturbo/ratelimit/models.py

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

@dataclass
class WindowCounter:
    """Counter for a specific time window"""
    count: int
    window_start: str  # ISO 8601 timestamp
    
@dataclass
class EndpointCounter:
    """Counters for all time windows of an endpoint"""
    minute: WindowCounter
    hour: WindowCounter
    day: WindowCounter

@dataclass
class RateLimitConfig:
    """Rate limit configuration for an endpoint"""
    per_minute: int
    per_hour: int
    per_day: int

@dataclass
class RateLimitResult:
    """Result of rate limit check"""
    allowed: bool
    tenant_id: str
    endpoint: str
    limit_type: Optional[str] = None  # "minute", "hour", "day"
    limit_value: Optional[int] = None
    current_count: Optional[int] = None
```

---

## Component Design

### 1. Configuration Loader (`config.py`)

**Responsibility:** Load and provide rate limit configurations

```python
class RateLimitConfig:
    """Loads and manages rate limit configuration"""
    
    def __init__(self, config_path: str = "kuasaturbo/ratelimit/config.yaml"):
        self.config_path = config_path
        self.default_limits = {}
        self.endpoint_limits = {}
        self.unlimited_endpoints = []
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file"""
        pass
    
    def get_limits(self, endpoint: str) -> Dict[str, int]:
        """Get rate limits for an endpoint"""
        # Returns: {"per_minute": X, "per_hour": Y, "per_day": Z}
        pass
    
    def is_unlimited(self, endpoint: str) -> bool:
        """Check if endpoint is unlimited"""
        pass
```

**Key Methods:**
- `get_limits(endpoint)` - Returns limit config for endpoint
- `is_unlimited(endpoint)` - Checks if endpoint bypasses rate limiting
- `_load_config()` - Loads YAML configuration on initialization

**Error Handling:**
- Missing config file → Use hardcoded defaults
- Invalid YAML → Log error and use defaults
- Missing endpoint config → Use default limits

---

### 2. Counter Manager (`counter.py`)

**Responsibility:** Manage request counters and persistence

```python
class CounterManager:
    """Manages rate limit counters with JSON persistence"""
    
    def __init__(self, storage_path: str = "kuasaturbo/ratelimit/ratelimit.json"):
        self.storage_path = storage_path
        self.counters: Dict[str, EndpointCounter] = {}
        self._load_state()
    
    def _load_state(self) -> None:
        """Load counter state from JSON file"""
        pass
    
    def _save_state(self) -> None:
        """Persist counter state to JSON file"""
        pass
    
    def _get_counter_key(self, tenant_id: str, endpoint: str) -> str:
        """Generate counter key: tenant_id:endpoint"""
        return f"{tenant_id}:{endpoint}"
    
    def _should_reset_window(self, window_start: str, window_type: str) -> bool:
        """Check if time window has expired"""
        pass
    
    def increment(self, tenant_id: str, endpoint: str) -> None:
        """Increment counter for tenant-endpoint combination"""
        pass
    
    def get_count(self, tenant_id: str, endpoint: str, window_type: str) -> int:
        """Get current count for a specific window"""
        pass
    
    def reset_if_needed(self, tenant_id: str, endpoint: str) -> None:
        """Reset counters if time windows have expired"""
        pass
```

**Key Algorithms:**

**Window Reset Logic:**
```python
def _should_reset_window(self, window_start: str, window_type: str) -> bool:
    """
    Determine if a time window has expired
    
    Logic:
    - minute: Reset if current minute != window start minute
    - hour: Reset if current hour != window start hour  
    - day: Reset if current day != window start day
    """
    now = datetime.utcnow()
    start = datetime.fromisoformat(window_start.replace('Z', '+00:00'))
    
    if window_type == "minute":
        return now.minute != start.minute or now.hour != start.hour
    elif window_type == "hour":
        return now.hour != start.hour or now.day != start.day
    elif window_type == "day":
        return now.day != start.day or now.month != start.month
    
    return False
```

**Counter Increment:**
```python
def increment(self, tenant_id: str, endpoint: str) -> None:
    """
    Increment counter with automatic window reset
    
    Steps:
    1. Generate counter key (tenant_id:endpoint)
    2. Check if counter exists, create if not
    3. Reset expired windows
    4. Increment all active windows
    5. Persist to JSON
    """
    key = self._get_counter_key(tenant_id, endpoint)
    
    # Auto-create counter if first request
    if key not in self.counters:
        self._create_counter(key)
    
    # Reset expired windows
    self.reset_if_needed(tenant_id, endpoint)
    
    # Increment all windows
    self.counters[key].minute.count += 1
    self.counters[key].hour.count += 1
    self.counters[key].day.count += 1
    
    # Persist
    self._save_state()
```

---

### 3. Rate Limiter (`limiter.py`)

**Responsibility:** Enforce rate limits and return results

```python
class RateLimiter:
    """Main rate limiting enforcement engine"""
    
    def __init__(self):
        self.config = RateLimitConfig()
        self.counter_manager = CounterManager()
    
    def check_limit(self, tenant_id: str, endpoint: str) -> RateLimitResult:
        """
        Check if request is within rate limits
        
        Returns RateLimitResult with:
        - allowed: True/False
        - limit_type: Which limit was exceeded (if any)
        - limit_value: The limit that was exceeded
        - current_count: Current request count
        """
        pass
    
    def _check_window(self, tenant_id: str, endpoint: str, 
                      window_type: str, limit: int) -> tuple[bool, int]:
        """Check a specific time window"""
        pass
```

**Rate Limit Check Algorithm:**

```python
def check_limit(self, tenant_id: str, endpoint: str) -> RateLimitResult:
    """
    Multi-window rate limit check
    
    Algorithm:
    1. Check if endpoint is unlimited → Allow
    2. Get rate limit config for endpoint
    3. Reset expired windows
    4. Check minute limit
    5. Check hour limit
    6. Check day limit
    7. If all pass → Increment counters and allow
    8. If any fail → Return rejection with details
    """
    
    # Step 1: Check unlimited
    if self.config.is_unlimited(endpoint):
        return RateLimitResult(allowed=True, tenant_id=tenant_id, endpoint=endpoint)
    
    # Step 2: Get limits
    limits = self.config.get_limits(endpoint)
    
    # Step 3: Reset expired windows
    self.counter_manager.reset_if_needed(tenant_id, endpoint)
    
    # Step 4-6: Check each window
    for window_type in ["minute", "hour", "day"]:
        limit_key = f"per_{window_type}"
        limit_value = limits[limit_key]
        current_count = self.counter_manager.get_count(tenant_id, endpoint, window_type)
        
        if current_count >= limit_value:
            return RateLimitResult(
                allowed=False,
                tenant_id=tenant_id,
                endpoint=endpoint,
                limit_type=window_type,
                limit_value=limit_value,
                current_count=current_count
            )
    
    # Step 7: All checks passed - increment and allow
    self.counter_manager.increment(tenant_id, endpoint)
    
    return RateLimitResult(allowed=True, tenant_id=tenant_id, endpoint=endpoint)
```

---

## Integration Design

### Gateway Integration

**Location:** `kuasaturbo/gateway/endpoints.py`

**Pattern:** Helper function called at the start of each endpoint

```python
from kuasaturbo.ratelimit.limiter import RateLimiter

# Initialize once at module level
rate_limiter = RateLimiter()

def check_rate_limit(tenant_id: str, endpoint: str) -> Optional[dict]:
    """
    Check rate limit and return error response if exceeded
    
    Returns:
    - None if allowed (proceed with request)
    - Error dict if rate limit exceeded (return immediately)
    """
    result = rate_limiter.check_limit(tenant_id, endpoint)
    
    if not result.allowed:
        return {
            "error": "rate_limit_exceeded",
            "message": f"Rate limit exceeded for {result.limit_type} window",
            "tenant_id": result.tenant_id,
            "endpoint": result.endpoint,
            "limit": result.limit_value,
            "window": result.limit_type,
            "current_count": result.current_count
        }
    
    return None
```

**Endpoint Integration Example:**

```python
@app.route("/service/execute", methods=["POST"])
def execute_service():
    """Execute a service with rate limiting"""
    
    # Step 1: Authenticate (existing)
    api_key = request.headers.get("X-API-Key")
    tenant = auth_service.validate_api_key(api_key)
    if not tenant:
        return jsonify({"error": "unauthorized"}), 401
    
    # Step 2: Rate limit check (NEW)
    rate_limit_error = check_rate_limit(tenant.tenant_id, "/service/execute")
    if rate_limit_error:
        return jsonify(rate_limit_error), 429
    
    # Step 3: Execute service (existing)
    # ... existing logic ...
```

**Endpoints to Integrate:**
- `/service/execute` - Service execution
- `/creative/generate` - Creative generation
- `/widgets` - Widget listing
- `/widgets/{widget_id}` - Widget details
- `/models/resolve` - Model resolution

**Endpoints to Skip:**
- `/` - Root
- `/health` - Health check
- `/auth/token` - Token generation
- `/auth/tenant` - Tenant info

---

## File Structure

```
kuasaturbo/
├── ratelimit/
│   ├── __init__.py           # Package initialization
│   ├── config.py             # Configuration loader (150 lines)
│   ├── counter.py            # Counter manager (200 lines)
│   ├── limiter.py            # Rate limiter (150 lines)
│   ├── models.py             # Data models (80 lines)
│   ├── config.yaml           # Rate limit configuration
│   └── ratelimit.json        # Runtime state (auto-generated)
│
├── gateway/
│   └── endpoints.py          # Updated with rate limiting
│
tests/kuasaturbo/
├── test_rate_limiter.py      # Rate limiter tests (300 lines)
└── run_all_tests.sh          # Updated test runner

kuasaturbo/
└── PHASE_XVI_RATE_LIMITING_SUMMARY.md
```

---

## Testing Strategy

### Test Coverage

**Unit Tests (`test_rate_limiter.py`):**

1. **Configuration Tests**
   - Load default configuration
   - Load endpoint-specific configuration
   - Handle missing config file
   - Identify unlimited endpoints

2. **Counter Tests**
   - Create new counter
   - Increment counter
   - Reset minute window
   - Reset hour window
   - Reset day window
   - Persist to JSON
   - Load from JSON
   - Handle missing JSON file

3. **Rate Limit Tests**
   - Allow request within limits
   - Block request exceeding minute limit
   - Block request exceeding hour limit
   - Block request exceeding day limit
   - Allow unlimited endpoints
   - Multi-tenant isolation

4. **Integration Tests**
   - Full request flow with rate limiting
   - Multiple tenants simultaneously
   - Window reset during operation
   - Error response format validation

### Test Data

```python
# Test configuration
TEST_CONFIG = {
    "default_limits": {
        "per_minute": 5,
        "per_hour": 20,
        "per_day": 100
    },
    "endpoint_limits": {
        "/test/endpoint": {
            "per_minute": 2,
            "per_hour": 10,
            "per_day": 50
        }
    },
    "unlimited_endpoints": ["/health"]
}
```

### Test Scenarios

**Scenario 1: Normal Operation**
```
Given: Tenant "voltek" with clean counters
When: 5 requests to /service/execute in same minute
Then: All 5 requests succeed
When: 6th request in same minute
Then: Request fails with 429
```

**Scenario 2: Window Reset**
```
Given: Tenant "voltek" with 5 requests in minute 1
When: Request arrives in minute 2
Then: Counter resets and request succeeds
```

**Scenario 3: Multi-Tenant Isolation**
```
Given: Tenant "voltek" has 10 requests (at limit)
When: Tenant "default" makes request
Then: Request succeeds (independent counters)
```

**Scenario 4: Endpoint-Specific Limits**
```
Given: /creative/generate has limit of 5/min
And: /widgets has limit of 100/min
When: 6 requests to /creative/generate
Then: 6th request fails
When: 50 requests to /widgets
Then: All succeed
```

---

## Error Handling

### Error Scenarios

1. **Missing Configuration File**
   - Action: Use hardcoded defaults
   - Log: Warning message
   - Continue: Yes

2. **Corrupted JSON State**
   - Action: Reset to empty state
   - Log: Error message
   - Continue: Yes

3. **File Write Failure**
   - Action: Log error, continue in-memory
   - Log: Error message
   - Continue: Yes (degraded mode)

4. **Invalid Timestamp**
   - Action: Reset window
   - Log: Warning message
   - Continue: Yes

### Error Response Format

```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded for minute window",
  "tenant_id": "voltek",
  "endpoint": "/service/execute",
  "limit": 10,
  "window": "minute",
  "current_count": 10
}
```

---

## Performance Considerations

### Optimization Strategies

1. **In-Memory Operations**
   - Keep all counters in memory
   - Only persist to disk on updates
   - No database queries

2. **Lazy Window Reset**
   - Reset windows on-demand (not background process)
   - Check window expiry during rate limit check
   - No cron jobs or timers

3. **Minimal File I/O**
   - Batch updates if possible
   - Use atomic writes
   - Handle concurrent access

4. **Fast Path for Unlimited Endpoints**
   - Check unlimited list first
   - Skip all counter logic
   - Return immediately

### Performance Targets

- Rate limit check: < 10ms
- Counter increment: < 5ms
- JSON persistence: < 20ms
- Total overhead: < 35ms per request

---

## Security Considerations

### Threat Model

1. **Rate Limit Bypass**
   - Mitigation: Validate tenant_id from auth layer
   - Mitigation: Use consistent counter keys
   - Mitigation: No client-side configuration

2. **Counter Manipulation**
   - Mitigation: Server-side counter management only
   - Mitigation: No API to reset counters
   - Mitigation: Atomic file operations

3. **Resource Exhaustion**
   - Mitigation: Limit counter storage size
   - Mitigation: Periodic cleanup of old counters
   - Mitigation: Default limits on all endpoints

4. **Cross-Tenant Interference**
   - Mitigation: Tenant ID in counter key
   - Mitigation: Separate counter objects
   - Mitigation: Test multi-tenant isolation

---

## Migration Plan

### Phase 1: Implementation (Day 1)
1. Create `kuasaturbo/ratelimit/` directory
2. Implement `models.py` (data structures)
3. Implement `config.py` (configuration loader)
4. Implement `counter.py` (counter management)
5. Implement `limiter.py` (rate limit enforcement)
6. Create `config.yaml` with default limits

### Phase 2: Integration (Day 1)
1. Update `kuasaturbo/gateway/endpoints.py`
2. Add `check_rate_limit()` helper function
3. Integrate with 5 main endpoints
4. Test basic functionality

### Phase 3: Testing (Day 2)
1. Create `tests/kuasaturbo/test_rate_limiter.py`
2. Implement 12+ test cases
3. Run full test suite (77+ existing tests)
4. Fix any issues

### Phase 4: Documentation (Day 2)
1. Create `PHASE_XVI_RATE_LIMITING_SUMMARY.md`
2. Document configuration options
3. Document integration patterns
4. Provide usage examples

---

## Rollback Plan

If issues arise:

1. **Remove rate limiting integration**
   - Comment out `check_rate_limit()` calls
   - Endpoints function normally
   - No data loss

2. **Disable specific endpoints**
   - Add to `unlimited_endpoints` list
   - Bypass rate limiting temporarily

3. **Adjust limits**
   - Edit `config.yaml`
   - Restart service
   - No code changes needed

---

## Future Enhancements (Out of Scope)

These features are explicitly NOT included in Phase XVI:

1. **Dynamic Limit Adjustment**
   - API to change limits at runtime
   - Per-tenant custom limits
   - Requires: Admin API (future phase)

2. **Rate Limit Analytics**
   - Dashboard showing usage patterns
   - Historical data analysis
   - Requires: Analytics layer (future phase)

3. **Distributed Rate Limiting**
   - Redis-based counters
   - Multi-server coordination
   - Requires: Production deployment (future phase)

4. **Burst Allowance**
   - Token bucket algorithm
   - Temporary limit increases
   - Requires: Advanced rate limiting (future phase)

5. **Cost-Based Limiting**
   - Different costs per endpoint
   - Budget-based throttling
   - Requires: Billing integration (future phase)

---

## Acceptance Checklist

Phase XVI is complete when:

- [ ] All 4 core modules implemented (`config.py`, `counter.py`, `limiter.py`, `models.py`)
- [ ] Configuration file created (`config.yaml`)
- [ ] 5 endpoints integrated with rate limiting
- [ ] 12+ test cases implemented and passing
- [ ] All 77+ existing tests still passing
- [ ] No governance features introduced
- [ ] Multi-tenant isolation verified
- [ ] Window reset logic working correctly
- [ ] Error responses properly formatted
- [ ] Documentation complete (`PHASE_XVI_RATE_LIMITING_SUMMARY.md`)

---

## References

- Phase XV: Multi-Tenant Auth Layer
- Phase XIV: Endpoint Layer
- KuasaTurbo Boundaries: `.kiro/steering/kuasaturbo-boundaries.md`
- Requirements: `.kiro/specs/phase-xvi-rate-limiting/requirements.md`

---

**Document Version:** 1.0.0  
**Last Updated:** December 8, 2025  
**Status:** Ready for Implementation  
**Estimated Effort:** 2 days
