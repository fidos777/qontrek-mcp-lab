# SPEC_TEMPLATE.md - KuasaTurbo L6 Skill Specification

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | `{domain}.{skill}.{version}` |
| **Domain** | `{domain}` (kreator, arkitek, mortgage, solar) |
| **Version** | `v1`, `v2`, etc. |
| **Owner** | Team or individual responsible |
| **Status** | `draft`, `review`, `approved`, `deprecated` |
| **Created** | YYYY-MM-DD |
| **Updated** | YYYY-MM-DD |

## Overview

Brief description of what this skill does and why it exists.

**Purpose**: One-sentence summary of the skill's primary function.

**Use Cases**:
- Use case 1
- Use case 2
- Use case 3

## Input Schema

### Required Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `field_name` | `string` | `minLength: 1, maxLength: 100` | Description of field |
| `field_name` | `integer` | `minimum: 0, maximum: 100` | Description of field |
| `field_name` | `array<string>` | `minItems: 1, maxItems: 10` | Description of field |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `field_name` | `string` | `"en"` | Description of field |
| `field_name` | `integer` | `5` | Description of field |

### Example Input

```json
{
  "required_field": "value",
  "optional_field": "value"
}
```

## Output Schema

### Success Response

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"success"` |
| `data` | `object` | Main output data |
| `errors` | `array` | Empty array |

### Error Response

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"error"` |
| `data` | `null` | No data on error |
| `errors` | `array<object>` | Array of error objects with `code`, `message`, `field` |

### Example Output

```json
{
  "status": "success",
  "data": {
    "result_field": "value"
  },
  "errors": []
}
```

## Logic Breakdown

### Step 1: Input Validation
- Validate required fields
- Check type constraints
- Validate business rules

### Step 2: Core Processing
- Main transformation logic
- Calculations or generation
- Data enrichment

### Step 3: Output Formatting
- Structure response
- Add metadata
- Return standardized format

## Handler Contract

```python
class SkillHandler(BaseHandler):
    """Handler for {skill_name}."""
    
    def run(self, params: dict) -> dict:
        """
        Execute the skill logic.
        
        Args:
            params: Validated input parameters
            
        Returns:
            dict with status, data, errors
        """
        # Implementation
        pass
```

## Dependencies

### Python Standard Library
- `json` - JSON processing
- `datetime` - Timestamp generation
- `re` - Pattern matching (if needed)

### External Libraries (if any)
- None (prefer standard library)

### Domain Dependencies
- List any domain-specific utilities or shared modules

## Performance Criteria

| Metric | Target | Notes |
|--------|--------|-------|
| **Execution Time** | < 3 seconds | 95th percentile |
| **Memory Usage** | < 100 MB | Peak usage |
| **Success Rate** | > 99% | For valid inputs |

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `VALIDATION_ERROR` | Input validation failed | Check input against schema |
| `PROCESSING_ERROR` | Core logic failed | Check logs for details |
| `RESOURCE_ERROR` | External resource unavailable | Retry or check configuration |

## Testing Strategy

### Unit Tests
- Test input validation
- Test core logic with various inputs
- Test error handling

### Property-Based Tests
- Generate random valid inputs
- Verify output structure
- Check invariants

### Integration Tests
- Test via MCP protocol
- Verify schema compliance
- Test error scenarios

## Sample Test Cases

### Test Case 1: Valid Input
```json
{
  "input": {
    "field": "value"
  },
  "expected_output": {
    "status": "success",
    "data": {
      "result": "expected"
    }
  }
}
```

### Test Case 2: Invalid Input
```json
{
  "input": {
    "field": ""
  },
  "expected_output": {
    "status": "error",
    "errors": [
      {
        "code": "VALIDATION_ERROR",
        "field": "field",
        "message": "Field cannot be empty"
      }
    ]
  }
}
```

## Implementation Checklist

- [ ] Create `schema.json` with JSON Schema Draft 2020-12
- [ ] Create `handler.py` extending `BaseHandler`
- [ ] Implement `run(params)` method
- [ ] Add input validation
- [ ] Add core processing logic
- [ ] Add error handling
- [ ] Create `sample_inputs.json`
- [ ] Create `sample_outputs.json`
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Update domain manifest
- [ ] Document in SKILL.md

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1 | YYYY-MM-DD | Initial implementation | Name |

## Notes

Additional notes, caveats, or future improvements.
