#!/bin/bash
# Phase W: Widget Schema Tests

echo "=== Testing Widget Schema ==="
echo ""

PASSED=0
FAILED=0

# Test 1: Schema file exists
echo "Test 1: Schema file exists"
if [ -f "l3/schema/widget_schema.json" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Schema file found"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Schema file not found"
fi

# Test 2: Schema is valid JSON
echo "Test 2: Schema is valid JSON"
if python3 -c "import json; json.load(open('l3/schema/widget_schema.json'))" 2>/dev/null; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Schema is valid JSON"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Schema is invalid JSON"
fi

# Test 3: Schema has required properties
echo "Test 3: Schema has required properties"
required_props=$(python3 -c "
import json
schema = json.load(open('l3/schema/widget_schema.json'))
required = schema.get('required', [])
expected = ['widget_id', 'widget_name', 'vertical', 'description', 'fields', 'workflow']
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
schema = json.load(open('l3/schema/widget_schema.json'))
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

# Test 5: Schema rejects governance keys
echo "Test 5: Schema rejects governance keys"
governance_check=$(python3 -c "
import json
schema = json.load(open('l3/schema/widget_schema.json'))
# Check if 'not' clause exists to reject governance keys
if 'not' in schema:
    not_clause = schema['not']
    if 'anyOf' in not_clause:
        forbidden_keys = []
        for item in not_clause['anyOf']:
            if 'required' in item:
                forbidden_keys.extend(item['required'])
        # Check for key governance-related keys
        governance_keys = ['governance', 'governance_gate', 'ledger', 'audit']
        if any(k in forbidden_keys for k in governance_keys):
            print('OK')
        else:
            print('FAIL')
    else:
        print('FAIL')
else:
    print('FAIL')
" 2>/dev/null)

if [ "$governance_check" = "OK" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Governance keys properly rejected"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Governance keys not properly rejected"
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
