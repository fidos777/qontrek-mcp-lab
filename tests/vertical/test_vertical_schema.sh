#!/bin/bash
# Phase E: Vertical Pack Schema Tests

echo "=== Testing Vertical Pack Schema ==="
echo ""

PASSED=0
FAILED=0

# Test 1: Schema file exists
echo "Test 1: Schema file exists"
if [ -f "verticals/spec/vertical_pack_schema.json" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Schema file found"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Schema file not found"
fi

# Test 2: Schema is valid JSON
echo "Test 2: Schema is valid JSON"
if python3 -c "import json; json.load(open('verticals/spec/vertical_pack_schema.json'))" 2>/dev/null; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Schema is valid JSON"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Schema is invalid JSON"
fi

# Test 3: Schema has required top-level properties
echo "Test 3: Schema has required properties"
required_props=$(python3 -c "
import json
schema = json.load(open('verticals/spec/vertical_pack_schema.json'))
required = schema.get('required', [])
expected = ['industry_identity', 'entities', 'skills', 'workflows', 'compliance', 'statuses']
missing = [p for p in expected if p not in required]
if missing:
    print('Missing: ' + ', '.join(missing))
else:
    print('OK')
" 2>/dev/null)

if [ "$required_props" = "OK" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ All required properties defined"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ $required_props"
fi

# Test 4: Schema forbids additional properties
echo "Test 4: Schema forbids additional properties"
additional_props=$(python3 -c "
import json
schema = json.load(open('verticals/spec/vertical_pack_schema.json'))
if schema.get('additionalProperties') == False:
    print('OK')
else:
    print('FAIL')
" 2>/dev/null)

if [ "$additional_props" = "OK" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Additional properties forbidden"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Additional properties not properly restricted"
fi

# Test 5: Industry identity has required fields
echo "Test 5: Industry identity structure"
identity_check=$(python3 -c "
import json
schema = json.load(open('verticals/spec/vertical_pack_schema.json'))
identity = schema['properties']['industry_identity']
required = identity.get('required', [])
expected = ['industry_name', 'industry_code', 'description']
if all(f in required for f in expected):
    print('OK')
else:
    print('FAIL')
" 2>/dev/null)

if [ "$identity_check" = "OK" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Industry identity properly structured"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Industry identity missing required fields"
fi

echo ""
echo "=== Schema Tests Complete ==="
echo ""
if [ $FAILED -eq 0 ]; then
  echo "✅ PASS: All $PASSED tests passed"
  exit 0
else
  echo "❌ FAIL: $PASSED passed, $FAILED failed"
  exit 1
fi
