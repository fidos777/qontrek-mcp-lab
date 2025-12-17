#!/bin/bash
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SKILL_DIR"

echo "=== Pricing Generator Validation ==="
echo ""

echo "1. Validating schema.json..."
python3 -m json.tool schema.json > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "   ✅ schema.json valid"; else echo "   ❌ schema.json invalid"; exit 1; fi

echo "2. Validating manifest.json..."
python3 -m json.tool manifest.json > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "   ✅ manifest.json valid"; else echo "   ❌ manifest.json invalid"; exit 1; fi

echo "3. Validating sample_inputs.json..."
python3 -m json.tool sample_inputs.json > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "   ✅ sample_inputs.json valid"; else echo "   ❌ sample_inputs.json invalid"; exit 1; fi

echo "4. Validating sample_outputs.json..."
python3 -m json.tool sample_outputs.json > /dev/null 2>&1
if [ $? -eq 0 ]; then echo "   ✅ sample_outputs.json valid"; else echo "   ❌ sample_outputs.json invalid"; exit 1; fi

echo "5. Checking governance.yml..."
if [ -f governance.yml ]; then echo "   ✅ governance.yml exists"; else echo "   ❌ governance.yml missing"; exit 1; fi

echo "6. Checking reflexion.yml..."
if [ -f reflexion.yml ]; then echo "   ✅ reflexion.yml exists"; else echo "   ❌ reflexion.yml missing"; exit 1; fi

echo "7. Checking prompts/main.txt..."
if [ -f prompts/main.txt ]; then echo "   ✅ prompts/main.txt exists"; else echo "   ❌ prompts/main.txt missing"; exit 1; fi

echo "8. Checking templates/output.md..."
if [ -f templates/output.md ]; then echo "   ✅ templates/output.md exists"; else echo "   ❌ templates/output.md missing"; exit 1; fi

echo "9. Testing handler.py import..."
python3 -c "import sys; sys.path.insert(0, '../../..'); from skills.launchkit.pricing.generate.v1.handler import run" 2>/dev/null
if [ $? -eq 0 ]; then echo "   ✅ handler.py imports correctly"; else echo "   ❌ handler.py import failed"; exit 1; fi

echo "10. Testing sample execution..."
RESULT=$(cat sample_inputs.json | python3 handler.py 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   ✅ Sample execution passed"
    STATUS=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', ''))" 2>/dev/null)
    echo "   ✅ Status: $STATUS"
    
    # CRITICAL: Check for hardcoded prices
    HARDCODED=$(echo "$RESULT" | grep -E '\$[0-9]+' | wc -l)
    if [ "$HARDCODED" -eq 0 ]; then
        echo "   ✅ No hardcoded prices detected"
    else
        echo "   ❌ CRITICAL: Hardcoded prices found!"
        exit 1
    fi
    
    NO_HARDCODED=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('output', {}).get('metadata', {}).get('no_hardcoded_prices', False))" 2>/dev/null)
    echo "   ✅ No hardcoded prices flag: $NO_HARDCODED"
else
    echo "   ❌ Sample execution failed"
    exit 1
fi

echo ""
echo "=== ALL VALIDATIONS PASSED ==="
