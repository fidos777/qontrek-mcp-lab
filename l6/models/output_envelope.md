# L6 Universal Output Envelope

## Overview

All L6 skills and workflows MUST return outputs using this standardized envelope format. This ensures consistency across the entire KuasaTurbo L6 ecosystem.

## Standard Output Format

```json
{
  "status": "success" | "error",
  "output": {},
  "meta": {
    "skill": "string",
    "version": "string",
    "generated_at": "ISO8601 timestamp"
  },
  "errors": []
}
```

## Field Specifications

### `status` (required)
- **Type**: `string`
- **Values**: `"success"` | `"error"`
- **Description**: Indicates whether the skill execution succeeded or failed

### `output` (required)
- **Type**: `object` | `null`
- **Description**: Contains the actual skill output data
- **Rules**:
  - MUST be `null` when `status` is `"error"`
  - MUST be a valid object when `status` is `"success"`
  - Structure is skill-specific but must be documented in SKILL.md

### `meta` (required)
- **Type**: `object`
- **Description**: Metadata about the skill execution
- **Properties**:
  - `skill` (string, required): Skill identifier (e.g., `"generate_slogan"`)
  - `version` (string, required): Skill version (e.g., `"1.0.0"`)
  - `generated_at` (string, required): ISO 8601 timestamp of execution

### `errors` (required)
- **Type**: `array<string>`
- **Description**: Array of error messages
- **Rules**:
  - MUST be empty array `[]` when `status` is `"success"`
  - MUST contain at least one error message when `status` is `"error"`
  - Each error should be a clear, actionable message

## Examples

### Success Response

```json
{
  "status": "success",
  "output": {
    "slogans": [
      {
        "text": "Innovation Delivered",
        "score": 9.5
      }
    ],
    "brand_analysis": {
      "themes": ["innovation", "reliability"]
    }
  },
  "meta": {
    "skill": "generate_slogan",
    "version": "1.0.0",
    "generated_at": "2025-12-07T14:30:00.000Z"
  },
  "errors": []
}
```

### Error Response

```json
{
  "status": "error",
  "output": null,
  "meta": {
    "skill": "generate_slogan",
    "version": "1.0.0",
    "generated_at": "2025-12-07T14:30:00.000Z"
  },
  "errors": [
    "Missing required field: brand_name",
    "Missing required field: industry"
  ]
}
```

## Workflow Output Format

Workflows return a modified envelope that includes all step outputs:

```json
{
  "workflow": "workflow_id",
  "status": "success" | "error",
  "outputs": {
    "step_id_1": {
      "status": "success",
      "output": {},
      "errors": []
    },
    "step_id_2": {
      "status": "success",
      "output": {},
      "errors": []
    }
  },
  "errors": []
}
```

## Migration Guide

### For Existing Skills

Skills currently returning `{status, output, errors}` are already compliant. Add `meta` field:

```python
from datetime import datetime

def run(params: dict) -> dict:
    # ... existing logic ...
    
    return {
        "status": "success",
        "output": result_data,
        "meta": {
            "skill": "skill_name",
            "version": "1.0.0",
            "generated_at": datetime.now().isoformat()
        },
        "errors": []
    }
```

### For New Skills

Use this template:

```python
#!/usr/bin/env python3
import json
import sys
from datetime import datetime
from lib.logger import log

SKILL_NAME = "skill_name"
SKILL_VERSION = "1.0.0"

def run(params: dict) -> dict:
    """Universal handler entrypoint."""
    log("info", f"{SKILL_NAME}_start")
    
    errors = []
    
    # Validation
    required = ["field1", "field2"]
    for field in required:
        if field not in params:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        log("error", f"{SKILL_NAME}_validation_failed", errors=errors)
        return {
            "status": "error",
            "output": null,
            "meta": {
                "skill": SKILL_NAME,
                "version": SKILL_VERSION,
                "generated_at": datetime.now().isoformat()
            },
            "errors": errors
        }
    
    # Processing logic
    try:
        result = process_data(params)
        
        log("info", f"{SKILL_NAME}_done")
        
        return {
            "status": "success",
            "output": result,
            "meta": {
                "skill": SKILL_NAME,
                "version": SKILL_VERSION,
                "generated_at": datetime.now().isoformat()
            },
            "errors": []
        }
    except Exception as e:
        log("error", f"{SKILL_NAME}_error", error=str(e))
        return {
            "status": "error",
            "output": None,
            "meta": {
                "skill": SKILL_NAME,
                "version": SKILL_VERSION,
                "generated_at": datetime.now().isoformat()
            },
            "errors": [f"Processing error: {str(e)}"]
        }
```

## Validation Rules

1. **Status Consistency**: If `status` is `"error"`, `output` MUST be `null` and `errors` MUST be non-empty
2. **Timestamp Format**: `generated_at` MUST be valid ISO 8601 format
3. **Version Format**: `version` SHOULD follow semantic versioning (e.g., "1.0.0")
4. **Error Messages**: Each error MUST be a non-empty string with actionable information
5. **Output Structure**: When `status` is `"success"`, `output` MUST NOT be `null`

## Benefits

- **Consistency**: All skills return data in the same format
- **Debugging**: `meta` field provides execution context
- **Error Handling**: Standardized error reporting
- **Monitoring**: Easy to track skill versions and execution times
- **Composability**: Workflows can reliably process skill outputs
- **Documentation**: Clear contract for skill consumers

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-07 | Initial envelope specification |
