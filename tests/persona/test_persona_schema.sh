#!/bin/bash
# Phase F: Persona Pack Schema Tests

echo "=== Testing Persona Pack Schema ==="
echo ""

PASSED=0
FAILED=0

# Test 1: Schema file exists
echo "Test 1: Schema file exists"
if [ -f "l5/schema/persona_pack_schema.json" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Schema file found"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Schema file not found"
fi

# Test 2: Schema is valid JSON
echo "Test 2: Schema is valid JSON"
if python3 -c "import json; json.load(open('l5/schema/persona_pack_schema.json'))" 2>/dev/null; then
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
schema = json.load(open('l5/schema/persona_pack_schema.json'))
required = schema.get('required', [])
expected = ['identity', 'language_profile', 'tone', 'structure', 'persuasion', 'rhetoric_rules', 'channels', 'rubric_targets', 'constraints']
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
schema = json.load(open('l5/schema/persona_pack_schema.json'))
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

# Test 5: Rubric targets structure
echo "Test 5: Rubric targets structure"
rubric_check=$(python3 -c "
import json
schema = json.load(open('l5/schema/persona_pack_schema.json'))
rubric = schema['properties']['rubric_targets']
required = rubric.get('required', [])
expected = ['clarity', 'tone_consistency', 'persuasion_control', 'personalization', 'structure', 'compliance']
if all(f in required for f in expected):
    print('OK')
else:
    print('FAIL')
" 2>/dev/null)

if [ "$rubric_check" = "OK" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Rubric targets properly structured"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Rubric targets missing required fields"
fi

# Test 6: Language profile structure
echo "Test 6: Language profile structure"
lang_check=$(python3 -c "
import json
schema = json.load(open('l5/schema/persona_pack_schema.json'))
lang = schema['properties']['language_profile']
required = lang.get('required', [])
expected = ['primary_language', 'english_ratio', 'bbnu_ratio', 'code_switching_rules']
if all(f in required for f in expected):
    print('OK')
else:
    print('FAIL')
" 2>/dev/null)

if [ "$lang_check" = "OK" ]; then
  PASSED=$((PASSED + 1))
  echo "  ✓ Language profile properly structured"
else
  FAILED=$((FAILED + 1))
  echo "  ✗ Language profile missing required fields"
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
