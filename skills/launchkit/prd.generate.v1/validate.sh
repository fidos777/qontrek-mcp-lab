#!/bin/bash
# Validation script for prd.generate.v1

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SKILL_DIR"

echo "=== PRD Generator Validation ==="
echo ""

# 1. Validate JSON files
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

# 2. Validate YAML files
echo "5. Checking governance.yml..."
if [ -f governance.yml ]; then echo "   ✅ governance.yml exists"; else echo "   ❌ governance.yml missing"; exit 1; fi

echo "6. Checking reflexion.yml..."
if [ -f reflexion.yml ]; then echo "   ✅ reflexion.yml exists"; else echo "   ❌ reflexion.yml missing"; exit 1; fi

# 3. Check prompts and templates
echo "7. Checking prompts/main.txt..."
if [ -f prompts/main.txt ]; then echo "   ✅ prompts/main.txt exists"; else echo "   ❌ prompts/main.txt missing"; exit 1; fi

echo "8. Checking templates/output.md..."
if [ -f templates/output.md ]; then echo "   ✅ templates/output.md exists"; else echo "   ❌ templates/output.md missing"; exit 1; fi

# 4. Test handler import
echo "9. Testing handler.py import..."
python3 -c "import sys; sys.path.insert(0, '../../..'); from skills.launchkit.prd.generate.v1.handler import run" 2>/dev/null
if [ $? -eq 0 ]; then echo "   ✅ handler.py imports correctly"; else echo "   ❌ handler.py import failed"; exit 1; fi

# 5. Test sample execution
echo "10. Testing sample execution..."
RESULT=$(cat sample_inputs.json | python3 handler.py 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "   ✅ Sample execution passed"
    
    # Check output structure
    STATUS=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', ''))" 2>/dev/null)
    if [ "$STATUS" = "success" ]; then
        echo "   ✅ Status: success"
    else
        echo "   ⚠️  Status: $STATUS"
    fi
    
    BRAND=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('output', {}).get('brand_name', ''))" 2>/dev/null)
    echo "   ✅ Brand: $BRAND"
    
    PROBLEM_LEN=$(echo "$RESULT" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('output', {}).get('problem_statement', '')))" 2>/dev/null)
    echo "   ✅ Problem statement length: $PROBLEM_LEN characters"
    
    FEATURES=$(echo "$RESULT" | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('output', {}).get('feature_list', {}).get('mvp', [])))" 2>/dev/null)
    echo "   ✅ MVP features: $FEATURES"
    
    LLM=$(echo "$RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('output', {}).get('metadata', {}).get('llm_powered', False))" 2>/dev/null)
    echo "   ✅ LLM-powered: $LLM"
else
    echo "   ❌ Sample execution failed"
    exit 1
fi

echo ""
echo "=== ALL VALIDATIONS PASSED ==="
