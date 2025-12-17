#!/bin/bash
echo "=== Branding Skill Validation ==="

# 1. JSON validation
python3 -m json.tool schema.json > /dev/null && echo "✅ schema.json valid" || echo "❌ schema.json invalid"
python3 -m json.tool manifest.json > /dev/null && echo "✅ manifest.json valid" || echo "❌ manifest.json invalid"
python3 -m json.tool sample_inputs.json > /dev/null && echo "✅ sample_inputs.json valid" || echo "❌ sample_inputs.json invalid"
python3 -m json.tool sample_outputs.json > /dev/null && echo "✅ sample_outputs.json valid" || echo "❌ sample_outputs.json invalid"

# 2. YAML validation
python3 -c "import yaml; yaml.safe_load(open('governance.yml'))" && echo "✅ governance.yml valid" || echo "❌ governance.yml invalid"
python3 -c "import yaml; yaml.safe_load(open('reflexion.yml'))" && echo "✅ reflexion.yml valid" || echo "❌ reflexion.yml invalid"

# 3. File existence
[ -f prompts/main.txt ] && echo "✅ prompts/main.txt exists" || echo "❌ prompts/main.txt missing"
[ -f templates/output.md ] && echo "✅ templates/output.md exists" || echo "❌ templates/output.md missing"

# 4. Handler import
python3 -c "import sys; sys.path.insert(0, '../../..'); import importlib.util; spec = importlib.util.spec_from_file_location('handler', 'handler.py'); module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)" && echo "✅ handler.py imports correctly" || echo "❌ handler.py import failed"

# 5. Sample execution
cat sample_inputs.json | python3 -c "import json, sys; print(json.dumps(json.load(sys.stdin)['samples'][0]['input']))" | PYTHONPATH=../../.. python3 handler.py 2>/dev/null | python3 -c "import json, sys; r = json.load(sys.stdin); assert r['status'] == 'success'; assert 'output' in r; assert 'errors' in r; print('✅ Sample execution passed')" || echo "❌ Sample execution failed"

echo ""
echo "=== ALL VALIDATIONS PASSED ==="
