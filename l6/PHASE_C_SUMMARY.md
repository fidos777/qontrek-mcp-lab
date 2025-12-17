# PHASE C: BrandContext Normalization Layer - Summary

## Overview
Phase C introduces a **BrandContext Normalization Layer** that ensures all LaunchKit skills receive consistent, validated brand context. This layer sits between workflow inputs and skill execution, providing deterministic validation and transformation without modifying existing skills.

## Architecture

```
User Input → Normalizer → Runner V2 → Step Executor → Dispatcher → Skills
                ↓
         Validation & Transformation
                ↓
         BrandContext v2 Format
```

## Key Components

### 1. Brand Context Normalizer (`models/brand_context_normalizer.py`)
- **Purpose**: Validate and normalize brand context inputs
- **Type**: Deterministic, rule-based (NO LLM)
- **Functions**:
  - `normalize(raw_input: dict) -> dict`: Main normalization function
  - `to_legacy_format(normalized: dict) -> dict`: Backward compatibility helper

### 2. Integration Points

#### Runner V2 (`l6/runner_v2.py`)
- Calls normalizer BEFORE executing workflow steps
- Returns structured error if normalization fails
- Passes normalized context to all steps

#### Step Executor (`l6/step_executor.py`)
- Added `"normalized"` input mode
- Merges normalized context with step-specific inputs
- Maintains backward compatibility with `"direct"` and `"merged"` modes

#### Workflow Definitions
- `workflows/kuasaturbo.launchkit.v1.json`: First step uses `"input_mode": "normalized"`
- `workflows/turbodrive.followup_only.v1.json`: First step uses `"input_mode": "normalized"`

## Normalization Logic

### Required Fields Validation
The normalizer enforces BrandContext v2 schema requirements:

1. **Brand Identity** (at least one):
   - `brand_name` (primary identifier)
   - `tagline`
   - `story`
   - `values`

2. **Audience Definition** (at least one):
   - `icp` (with demographics, pain_points, or goals)
   - `segments`
   - `pain_points`

3. **Product Information** (optional but recommended):
   - `name`
   - `features`
   - `value_prop`
   - `pricing_model`

4. **Voice & Tone** (optional):
   - `tone`
   - `language`

### Error Handling
If validation fails, returns structured error:
```json
{
  "status": "error",
  "error": {
    "type": "brand_context_invalid",
    "missing_fields": ["brand_name", "icp (with demographics, pain_points, or goals)"]
  }
}
```

### Default Values
- Sets `metadata.version` to `"2.0"`
- Sets `metadata.source` to `"user_input"`
- Preserves all provided fields
- Does NOT generate missing content

## Backward Compatibility

### Legacy Format Support
The `to_legacy_format()` function converts BrandContext v2 to the format expected by existing skills:

```python
legacy = to_legacy_format(normalized_context)
# Returns: { "brand_name": "...", "mission": "...", "icp": {...}, ... }
```

This ensures existing LaunchKit skills continue working without modification.

## Input Modes

### Step Executor Input Modes
1. **"direct"**: Pass step input as-is (Phase A/B behavior)
2. **"merged"**: Merge workflow payload with step input (Phase B behavior)
3. **"normalized"**: Merge normalized context with step input (Phase C addition)

## Testing

### Test Suite (`tests/test_brand_context_normalizer.sh`)
6 comprehensive tests covering:
1. Basic normalization with valid input
2. Missing required fields detection
3. Runner integration with normalized context
4. Full LaunchKit workflow with normalization
5. Invalid context fails at normalization step
6. Legacy format conversion

**Result**: All tests passing ✓

## Files Changed

### New Files
- `models/brand_context_normalizer.py` (~400 lines)
- `tests/test_brand_context_normalizer.sh` (6 tests)
- `l6/PHASE_C_SUMMARY.md` (this file)
- `l6/PHASE_C_QUICKSTART.md` (quick reference)

### Modified Files
- `l6/runner_v2.py`: Added normalization step before workflow execution
- `l6/step_executor.py`: Added "normalized" input mode support
- `workflows/kuasaturbo.launchkit.v1.json`: First step uses normalized input
- `workflows/turbodrive.followup_only.v1.json`: First step uses normalized input

### Unchanged (No Breaking Changes)
- `l6/dispatcher_mvp.py`: No modifications
- All LaunchKit skills: No modifications
- `l6/envelope.py`: No modifications
- `l6/workflow_loader.py`: No modifications

## Phase C Constraints (All Met)

✅ **No LLM Generation**: Normalization is deterministic and rule-based
✅ **No Governance**: No governance.yml or policy enforcement
✅ **No Reflexion**: No reflexion.yml or quality scoring
✅ **No REST API**: No FastAPI or HTTP endpoints
✅ **No Async**: Synchronous execution only
✅ **No Versioning**: Simple version metadata only
✅ **No Skill Modifications**: Existing skills unchanged
✅ **Backward Compatible**: Legacy format support via `to_legacy_format()`
✅ **Strictly Additive**: Builds on Phase A/B without refactoring

## Success Criteria

✅ BrandContext normalizer exists and works
✅ Runner V2 applies normalization before workflow steps
✅ Workflows accept normalized input mode
✅ All tests pass (6/6)
✅ No breaking changes to Phase A or Phase B
✅ Structured error handling for invalid inputs
✅ Legacy format conversion for backward compatibility

## Next Steps (Phase D)

Phase C prepares the foundation for Phase D features:
- Workflow-level governance (not skill-level)
- Promotion flows (dev → staging → prod)
- Versioning and rollback
- Async execution patterns
- REST API layer

Phase C ensures all workflows start with validated, normalized brand context, making governance and quality control easier to implement in Phase D.

## How to Use

See `PHASE_C_QUICKSTART.md` for practical examples and usage patterns.
