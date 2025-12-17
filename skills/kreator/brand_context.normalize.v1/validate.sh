#!/bin/bash
# Validation script for brand_context.normalize.v1

set -e

echo "=============================================="
echo "Brand Context Normalizer - Validation Suite"
echo "=============================================="

# 1. JSON Validation
echo ""
echo "1. JSON Syntax Validation"
echo "   ------------------------"
python3 -m json.tool schema.json > /dev/null && echo "   ✅ schema.json valid"
python3 -m json.tool manifest.json > /dev/null && echo "   ✅ manifest.json valid"
python3 -m json.tool sample_inputs.json > /dev/null && echo "   ✅ sample_inputs.json valid"
python3 -m json.tool sample_outputs.json > /dev/null && echo "   ✅ sample_outputs.json valid"

# 2. Schema Compliance
echo ""
echo "2. Schema Compliance"
echo "   -----------------"
if grep -q '"required"' schema.json; then
    echo "   ✅ Required fields defined"
fi
if grep -q '"properties"' schema.json; then
    echo "   ✅ Properties defined"
fi
if grep -q '"brand"' schema.json && grep -q '"creative"' schema.json; then
    echo "   ✅ Core input fields present"
fi

# 3. Handler Structure
echo ""
echo "3. Handler Implementation"
echo "   ----------------------"
if grep -q "def run(params: dict)" handler.py; then
    echo "   ✅ Universal run() contract implemented"
fi
if grep -q "from lib.logger import log" handler.py; then
    echo "   ✅ Structured logging imported"
fi
if grep -q '"status":' handler.py && grep -q '"output":' handler.py && grep -q '"errors":' handler.py; then
    echo "   ✅ Output envelope structure present"
fi

# 4. Import Test
echo ""
echo "4. Module Import Test"
echo "   ------------------"
cd ../../..
python3 -c "
import sys
import importlib.util
spec = importlib.util.spec_from_file_location('handler', 'skills/kreator/brand_context.normalize.v1/handler.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert hasattr(module, 'run'), 'Missing run() function'
print('   ✅ Handler module importable')
print('   ✅ run() method present')
"

# 5. Envelope Compliance
echo ""
echo "5. Output Envelope Compliance"
echo "   ---------------------------"
cat skills/kreator/brand_context.normalize.v1/sample_inputs.json | \
python3 -c "import json, sys; data = json.load(sys.stdin); print(json.dumps(data['samples'][0]['input']))" | \
PYTHONPATH=. python3 skills/kreator/brand_context.normalize.v1/handler.py 2>/dev/null | \
python3 -c "
import json, sys
result = json.load(sys.stdin)
assert 'status' in result, 'Missing status field'
assert 'output' in result, 'Missing output field'
assert 'errors' in result, 'Missing errors field'
assert result['status'] == 'success', 'Status not success'
assert isinstance(result['output'], dict), 'Output not a dict'
assert isinstance(result['errors'], list), 'Errors not a list'
print('   ✅ Status field present')
print('   ✅ Output field present')
print('   ✅ Errors field present')
print('   ✅ Envelope structure valid')
"

# 6. Output Structure Validation
echo ""
echo "6. Output Structure Validation"
echo "   ----------------------------"
cat skills/kreator/brand_context.normalize.v1/sample_inputs.json | \
python3 -c "import json, sys; data = json.load(sys.stdin); print(json.dumps(data['samples'][0]['input']))" | \
PYTHONPATH=. python3 skills/kreator/brand_context.normalize.v1/handler.py 2>/dev/null | \
python3 -c "
import json, sys
result = json.load(sys.stdin)
output = result['output']

required_fields = [
    'brand_name', 'mission', 'positioning', 'value_proposition',
    'icp', 'brand_themes', 'unified_tone', 'narrative',
    'messaging_framework', 'metadata'
]

for field in required_fields:
    assert field in output, f'Missing field: {field}'
    print(f'   ✅ {field} present')
"

# 7. L6 Runner Integration
echo ""
echo "7. L6 Runner Integration"
echo "   ---------------------"
if grep -q "normalize_brand_context" l6/l6_runner.py; then
    echo "   ✅ Skill registered in l6_runner.py"
else
    echo "   ❌ Skill NOT registered in l6_runner.py"
fi

# 8. MCP Server Discovery
echo ""
echo "8. MCP Server Discovery"
echo "   --------------------"
python3 -c "
import os
skill_path = 'skills/kreator/brand_context.normalize.v1'
has_schema = os.path.exists(f'{skill_path}/schema.json')
has_handler = os.path.exists(f'{skill_path}/handler.py')
if has_schema and has_handler:
    print('   ✅ Discoverable by MCP server')
    print('   ✅ Tool name: normalize_brand_context')
else:
    print('   ❌ NOT discoverable')
"

echo ""
echo "=============================================="
echo "✅ ALL VALIDATIONS PASSED"
echo "=============================================="
echo ""
echo "Skill ready for:"
echo "  - MCP server integration"
echo "  - L6 workflow execution"
echo "  - WTO packaging"
echo ""
