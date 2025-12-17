# PHASE C: BrandContext Normalization - Quick Start

## What is Phase C?

Phase C adds a **normalization layer** that validates and transforms brand context inputs before workflow execution. This ensures all LaunchKit skills receive consistent, validated data.

## Quick Test

```bash
# Run all normalization tests
bash tests/test_brand_context_normalizer.sh
```

## Basic Usage

### 1. Direct Normalization

```python
from models.brand_context_normalizer import normalize

# Valid input
raw_input = {
    "brand_name": "TechCorp",
    "tagline": "Innovation Simplified",
    "icp": {
        "demographics": "Tech-savvy professionals aged 25-45",
        "pain_points": ["Complex workflows", "High costs"]
    },
    "product": {
        "name": "CloudFlow",
        "features": ["Real-time sync", "AI automation"]
    }
}

result = normalize(raw_input)
print(result["status"])  # "success"
print(result["normalized_context"]["identity"]["name"])  # "TechCorp"
```

### 2. Invalid Input Handling

```python
# Missing required fields
invalid_input = {
    "tagline": "Great Product"
    # Missing brand_name and audience fields
}

result = normalize(invalid_input)
print(result["status"])  # "error"
print(result["error"]["type"])  # "brand_context_invalid"
print(result["error"]["missing_fields"])  # ["brand_name", "icp (with demographics, pain_points, or goals)"]
```

### 3. Workflow Execution with Normalization

```bash
# Run LaunchKit workflow with normalization
python3 l6/runner_v2.py workflows/kuasaturbo.launchkit.v1.json '{
  "brand_name": "StartupX",
  "tagline": "Build Fast, Scale Faster",
  "icp": {
    "demographics": "Early-stage founders",
    "pain_points": ["Limited resources", "Time constraints"]
  },
  "product": {
    "name": "LaunchKit",
    "value_prop": "Complete startup toolkit in one platform"
  }
}'
```

## Input Modes

### "normalized" Mode (Phase C)
First step receives normalized + validated brand context:

```json
{
  "step_id": "branding",
  "skill_id": "launchkit.branding.generate.v1",
  "input_mode": "normalized",
  "input": {
    "additional_field": "value"
  }
}
```

Executor merges: `normalized_context + step.input`

### "merged" Mode (Phase B)
Step receives workflow payload + step input:

```json
{
  "step_id": "followup",
  "skill_id": "launchkit.prd.generate.v1",
  "input_mode": "merged",
  "input": {
    "focus": "technical_specs"
  }
}
```

Executor merges: `workflow_payload + step.input`

### "direct" Mode (Phase A)
Step receives only step input:

```json
{
  "step_id": "custom",
  "skill_id": "launchkit.pricing.generate.v1",
  "input_mode": "direct",
  "input": {
    "pricing_model": "freemium"
  }
}
```

Executor passes: `step.input` only

## Normalization Flow

```
┌─────────────────┐
│  User Input     │
│  (raw JSON)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Normalizer     │
│  - Validate     │
│  - Transform    │
│  - Add metadata │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌───────┐ ┌───────┐
│Success│ │ Error │
└───┬───┘ └───┬───┘
    │         │
    ▼         ▼
┌─────────┐ ┌─────────┐
│ Runner  │ │ Return  │
│ Executes│ │ Error   │
│ Workflow│ │ Envelope│
└─────────┘ └─────────┘
```

## Required Fields

### Minimum Valid Input

```json
{
  "brand_name": "MyBrand",
  "icp": {
    "demographics": "Target audience description"
  }
}
```

### Recommended Input

```json
{
  "brand_name": "MyBrand",
  "tagline": "Your tagline here",
  "story": "Brand story and mission",
  "values": ["Innovation", "Quality", "Trust"],
  "icp": {
    "demographics": "Target audience",
    "pain_points": ["Problem 1", "Problem 2"],
    "goals": ["Goal 1", "Goal 2"]
  },
  "product": {
    "name": "Product Name",
    "features": ["Feature 1", "Feature 2"],
    "value_prop": "Unique value proposition",
    "pricing_model": "subscription"
  },
  "voice": {
    "tone": "professional",
    "language": "en"
  }
}
```

## Error Examples

### Missing Brand Name
```json
{
  "status": "error",
  "error": {
    "type": "brand_context_invalid",
    "missing_fields": ["brand_name"]
  }
}
```

### Missing Audience
```json
{
  "status": "error",
  "error": {
    "type": "brand_context_invalid",
    "missing_fields": ["icp (with demographics, pain_points, or goals)"]
  }
}
```

### Multiple Missing Fields
```json
{
  "status": "error",
  "error": {
    "type": "brand_context_invalid",
    "missing_fields": [
      "brand_name",
      "icp (with demographics, pain_points, or goals)"
    ]
  }
}
```

## Legacy Format Conversion

For backward compatibility with existing skills:

```python
from models.brand_context_normalizer import normalize, to_legacy_format

# Normalize first
result = normalize(raw_input)
normalized = result["normalized_context"]

# Convert to legacy format
legacy = to_legacy_format(normalized)

# Legacy format structure:
# {
#   "brand_name": "...",
#   "mission": "...",
#   "icp": {...},
#   "product": {...},
#   "tone": "..."
# }
```

## Testing Patterns

### Test 1: Valid Normalization
```bash
echo '{
  "brand_name": "TestBrand",
  "icp": {"demographics": "Test audience"}
}' | python3 -c "
import sys, json
from models.brand_context_normalizer import normalize
result = normalize(json.load(sys.stdin))
print(json.dumps(result, indent=2))
"
```

### Test 2: Invalid Input
```bash
echo '{
  "tagline": "No brand name"
}' | python3 -c "
import sys, json
from models.brand_context_normalizer import normalize
result = normalize(json.load(sys.stdin))
assert result['status'] == 'error'
print('✓ Error handling works')
"
```

### Test 3: Workflow Integration
```bash
python3 l6/runner_v2.py workflows/kuasaturbo.launchkit.v1.json '{
  "brand_name": "TestBrand",
  "icp": {"demographics": "Test audience"}
}'
```

## Common Patterns

### Pattern 1: Minimal Input
Use when you have basic brand info:
```json
{
  "brand_name": "MyStartup",
  "icp": {
    "demographics": "Small business owners"
  }
}
```

### Pattern 2: Rich Input
Use when you have detailed brand context:
```json
{
  "brand_name": "MyStartup",
  "tagline": "Simplify Your Business",
  "story": "Founded to help small businesses thrive",
  "values": ["Simplicity", "Reliability", "Growth"],
  "icp": {
    "demographics": "Small business owners, 30-50 years old",
    "pain_points": ["Complex tools", "High costs", "Poor support"],
    "goals": ["Increase efficiency", "Reduce costs", "Scale operations"]
  },
  "product": {
    "name": "BusinessHub",
    "features": ["Invoicing", "CRM", "Analytics", "Automation"],
    "value_prop": "All-in-one business management platform",
    "pricing_model": "subscription"
  },
  "voice": {
    "tone": "professional",
    "language": "en"
  }
}
```

### Pattern 3: Incremental Enrichment
Start minimal, enrich over time:
```python
# Step 1: Initial input
context = {
    "brand_name": "MyStartup",
    "icp": {"demographics": "Small businesses"}
}

# Step 2: Add product info
context["product"] = {
    "name": "BusinessHub",
    "features": ["Invoicing", "CRM"]
}

# Step 3: Add voice
context["voice"] = {
    "tone": "professional",
    "language": "en"
}

# Normalize at any stage
result = normalize(context)
```

## Debugging

### Check Normalization Result
```python
from models.brand_context_normalizer import normalize
import json

result = normalize(your_input)
print(json.dumps(result, indent=2))

if result["status"] == "error":
    print("Missing fields:", result["error"]["missing_fields"])
else:
    print("Normalized successfully!")
```

### Check Workflow Execution
```bash
# Add debug output
python3 l6/runner_v2.py workflows/kuasaturbo.launchkit.v1.json '{...}' 2>&1 | grep -A5 "Normalization"
```

### Validate Against Schema
```python
import json
import jsonschema

# Load schema
with open("models/brand_context_v2.json") as f:
    schema = json.load(f)

# Validate normalized context
normalized = result["normalized_context"]
jsonschema.validate(normalized, schema)
print("✓ Schema validation passed")
```

## Next Steps

- **Phase D**: Workflow-level governance and promotion flows
- **Advanced**: Custom validation rules and business logic
- **Integration**: REST API layer for external systems

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| Normalizer | Validate & transform | `models/brand_context_normalizer.py` |
| Schema | BrandContext v2 spec | `models/brand_context_v2.json` |
| Runner | Workflow execution | `l6/runner_v2.py` |
| Tests | Validation suite | `tests/test_brand_context_normalizer.sh` |
| Workflows | LaunchKit definitions | `workflows/*.json` |

## Support

For issues or questions:
1. Check test suite: `bash tests/test_brand_context_normalizer.sh`
2. Review error messages in workflow envelope
3. Validate input against `brand_context_v2.json` schema
4. Check `PHASE_C_SUMMARY.md` for architecture details
