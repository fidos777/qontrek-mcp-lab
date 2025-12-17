#!/bin/bash
# Test script for dispatcher_mvp.py

echo "=== Testing L6 Dispatcher MVP ==="
echo ""

# Test 1: List skills
echo "Test 1: List available skills"
python3 l6/dispatcher_mvp.py 2>&1 | grep "launchkit"
echo ""

# Test 2: Execute branding skill
echo "Test 2: Execute branding.generate.v1"
PAYLOAD='{"brand_name":"TestBrand","mission":"Test mission","value_proposition":"Test value","icp":{"demographics":"test","pain_points":["p1"],"goals":["g1"]},"brand_themes":["theme1"]}'
echo "$PAYLOAD" | python3 l6/dispatcher_mvp.py launchkit.branding.generate.v1 2>&1 | grep -v timestamp | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Status: {d['status']}\"); print(f\"Brand: {d.get('output',{}).get('brand_name','N/A')}\")"
echo ""

# Test 3: Execute PRD skill
echo "Test 3: Execute prd.generate.v1"
PAYLOAD='{"brand_name":"TestBrand","mission":"Test mission","value_proposition":"Test value","icp":{"demographics":"test","pain_points":["p1"],"goals":["g1"]}}'
echo "$PAYLOAD" | python3 l6/dispatcher_mvp.py launchkit.prd.generate.v1 2>&1 | grep -v timestamp | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Status: {d['status']}\"); print(f\"Brand: {d.get('output',{}).get('brand_name','N/A')}\")"
echo ""

# Test 4: Execute pricing skill
echo "Test 4: Execute pricing.generate.v1"
PAYLOAD='{"brand_name":"TestBrand","value_proposition":"Test value","icp":{"demographics":"test","pain_points":["p1"],"goals":["g1"]}}'
echo "$PAYLOAD" | python3 l6/dispatcher_mvp.py launchkit.pricing.generate.v1 2>&1 | grep -v timestamp | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Status: {d['status']}\"); print(f\"No hardcoded prices: {d.get('output',{}).get('metadata',{}).get('no_hardcoded_prices','N/A')}\")"
echo ""

# Test 5: Invalid skill
echo "Test 5: Invalid skill ID"
echo '{}' | python3 l6/dispatcher_mvp.py invalid.skill 2>&1 | grep -v timestamp | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Status: {d['status']}\"); print(f\"Error type: {d.get('error',{}).get('type','N/A')}\")"
echo ""

echo "=== All Tests Complete ==="
