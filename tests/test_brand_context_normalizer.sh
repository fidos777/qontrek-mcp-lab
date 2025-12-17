#!/bin/bash
# Test script for brand_context_normalizer.py (Phase C)

echo "=== Testing BrandContext Normalizer ==="
echo ""

# Test 1: Basic normalization works
echo "Test 1: Basic normalization"
python3 -c "
import sys
sys.path.insert(0, '.')
from models.brand_context_normalizer import normalize

raw_input = {
    'brand_name': 'TestBrand',
    'mission': 'Test mission',
    'value_proposition': 'Test value prop',
    'icp': {
        'demographics': 'Test audience',
        'pain_points': ['Pain 1', 'Pain 2'],
        'goals': ['Goal 1', 'Goal 2']
    },
    'brand_themes': ['theme1', 'theme2']
}

result = normalize(raw_input)

if 'status' in result and result['status'] == 'error':
    print(f\"  ✗ Normalization failed: {result['error']['message']}\")
else:
    print(f\"  ✓ Normalization succeeded\")
    print(f\"  Identity.name: {result['identity']['name']}\")
    print(f\"  Audience fields: {len(result['audience'])}\")
    print(f\"  Product fields: {len(result['product'])}\")
    print(f\"  Voice.tone: {result['voice']['tone']}\")
"
echo ""

# Test 2: Missing required fields
echo "Test 2: Missing required fields"
python3 -c "
import sys
sys.path.insert(0, '.')
from models.brand_context_normalizer import normalize

raw_input = {
    'mission': 'Test mission'
}

result = normalize(raw_input)

if result.get('status') == 'error':
    print(f\"  ✓ Correctly identified error\")
    print(f\"  Error type: {result['error']['type']}\")
    print(f\"  Missing fields: {', '.join(result['error']['missing_fields'])}\")
else:
    print(f\"  ✗ Should have failed validation\")
"
echo ""

# Test 3: Runner respects normalized inputs
echo "Test 3: Runner with normalized context"
PAYLOAD='{
  "brand_name": "TestBrand",
  "mission": "Test mission",
  "value_proposition": "Test value prop",
  "icp": {
    "demographics": "Test audience",
    "pain_points": ["Pain 1"],
    "goals": ["Goal 1"]
  },
  "brand_themes": ["theme1"]
}'

echo "$PAYLOAD" | python3 l6/runner_v2.py turbodrive.followup_only.v1 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d['status'] == 'success':
        print(f\"  ✓ Workflow succeeded with normalized context\")
        print(f\"  Completed steps: {', '.join(d['completed_steps'])}\")
    else:
        print(f\"  ✗ Workflow failed: {d['status']}\")
        if d['errors']:
            print(f\"  Error: {d['errors'][0]['message']}\")
except Exception as e:
    print(f\"  ERROR: {e}\")
"
echo ""

# Test 4: LaunchKit workflow with normalization
echo "Test 4: Full LaunchKit with normalized context"
echo "$PAYLOAD" | python3 l6/runner_v2.py kuasaturbo.launchkit.v1 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f\"  Status: {d['status']}\")
    print(f\"  Completed: {len(d['completed_steps'])}/6 steps\")
    if d['status'] == 'success':
        print(f\"  ✓ Full LaunchKit succeeded with normalization\")
except Exception as e:
    print(f\"  ERROR: {e}\")
"
echo ""

# Test 5: Invalid context fails at normalization
echo "Test 5: Invalid context fails at normalization step"
INVALID_PAYLOAD='{
  "some_field": "value"
}'

echo "$INVALID_PAYLOAD" | python3 l6/runner_v2.py turbodrive.followup_only.v1 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d['status'] == 'failed' and 'brand_context_normalization' in d['failed_steps']:
        print(f\"  ✓ Correctly failed at normalization\")
        print(f\"  Error type: {d['errors'][0]['type']}\")
    else:
        print(f\"  ✗ Should have failed at normalization\")
        print(f\"  Status: {d['status']}\")
except Exception as e:
    print(f\"  ERROR: {e}\")
"
echo ""

# Test 6: Legacy format conversion
echo "Test 6: Legacy format conversion"
python3 -c "
import sys
sys.path.insert(0, '.')
from models.brand_context_normalizer import normalize, to_legacy_format

raw_input = {
    'brand_name': 'TestBrand',
    'mission': 'Test mission',
    'value_proposition': 'Test value prop',
    'icp': {
        'demographics': 'Test audience',
        'pain_points': ['Pain 1'],
        'goals': ['Goal 1']
    },
    'brand_themes': ['theme1', 'theme2']
}

normalized = normalize(raw_input)
legacy = to_legacy_format(normalized)

if legacy.get('brand_name') == 'TestBrand':
    print(f\"  ✓ Legacy format conversion works\")
    print(f\"  brand_name: {legacy['brand_name']}\")
    print(f\"  mission: {legacy.get('mission', 'N/A')}\")
    print(f\"  icp.demographics: {legacy.get('icp', {}).get('demographics', 'N/A')}\")
else:
    print(f\"  ✗ Legacy format conversion failed\")
"
echo ""

echo "=== All Normalization Tests Complete ==="
