# Signal Contracts Documentation

**Non-authoritative**  
**Interpretability only**  
**Signals ≠ verdicts**

## Overview

This document defines the payload contracts for signals emitted to the `demand_signals` table. These signals are purely observational and carry no decision-making authority.

## Signal Types

### 1. execution_volume
**Purpose**: Track execution activity levels  
**Payload Structure**:
```json
{
  "execution_class": "string",
  "runner_type": "string", 
  "volume_count": "number",
  "time_window": "string"
}
```

### 2. credit_usage
**Purpose**: Observe credit consumption patterns  
**Payload Structure**:
```json
{
  "estimated_credits": "number",
  "actual_credits": "number",
  "variance": "number",
  "execution_class": "string"
}
```

### 3. system_load
**Purpose**: Monitor system resource utilization  
**Payload Structure**:
```json
{
  "load_level": "string",
  "concurrent_executions": "number",
  "queue_depth": "number"
}
```

### 4. error_frequency
**Purpose**: Track error occurrence patterns  
**Payload Structure**:
```json
{
  "error_type": "string",
  "frequency": "number",
  "execution_class": "string",
  "time_window": "string"
}
```

### 5. manual_observation
**Purpose**: Human-generated observations  
**Payload Structure**:
```json
{
  "observer": "string",
  "observation_type": "string",
  "description": "string",
  "context": "object"
}
```

## Signal Emission Rules

1. **No Decision Logic**: Signals must not contain approval/rejection logic
2. **No Thresholds**: Signals must not define operational limits
3. **No Automation**: Signals must not trigger automated responses
4. **Descriptive Only**: Signals describe what happened, not what should happen

## Database Schema

Signals are stored in `public.demand_signals`:
- `id`: UUID PRIMARY KEY
- `signal_type`: TEXT (one of the types above)
- `payload`: JSONB (structured according to contracts)
- `created_at`: TIMESTAMPTZ

## Integration Points

Signals can be consumed by:
- `v_demand_trends` view for aggregation
- `v_proof_signal_context` view for correlation
- External monitoring systems (read-only)

## Constraints

- Maximum payload size: 64KB
- Signal retention: 90 days
- No foreign key constraints
- No triggers or automation