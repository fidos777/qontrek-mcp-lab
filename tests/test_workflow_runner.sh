#!/bin/bash
# Test script for runner_v2.py (Phase B)

echo "=== Testing Workflow Runner V2 ==="
echo ""

# Test payload
TEST_PAYLOAD='{
  "brand_name": "TestBrand",
  "mission": "To deliver efficiency and help users reclaim time",
  "positioning": "The professional productivity solution",
  "value_proposition": "Reclaim 10+ hours every week",
  "icp": {
    "demographics": "Remote workers aged 25-40",
    "psychographics": ["results-oriented", "efficiency-focused"],
    "pain_points": ["Time constraints", "Manual tasks"],
    "goals": ["Increase productivity", "Reduce tools"]
  },
  "brand_themes": ["productivity", "efficiency", "simplicity"]
}'

# Test 1: LaunchKit happy path
echo "Test 1: Execute kuasaturbo.launchkit.v1 (full LaunchKit)"
echo "$TEST_PAYLOAD" | python3 l6/runner_v2.py kuasaturbo.launchkit.v1 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f\"  Status: {d['status']}\")
    print(f\"  Completed steps: {len(d['completed_steps'])}/{len(d['completed_steps']) + len(d['pending_steps']) + len(d['failed_steps'])}\")
    print(f\"  Steps: {', '.join(d['completed_steps'][:3])}{'...' if len(d['completed_steps']) > 3 else ''}\")
    if 'branding' in d['outputs']:
        print(f\"  ✓ Branding output exists\")
    if d['errors']:
        print(f\"  Errors: {len(d['errors'])}\")
except Exception as e:
    print(f\"  ERROR: {e}\")
"
echo ""

# Test 2: Followup-only workflow
echo "Test 2: Execute turbodrive.followup_only.v1 (minimal workflow)"
echo "$TEST_PAYLOAD" | python3 l6/runner_v2.py turbodrive.followup_only.v1 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f\"  Status: {d['status']}\")
    print(f\"  Completed steps: {', '.join(d['completed_steps'])}\")
    if d['status'] == 'success':
        print(f\"  ✓ Workflow completed successfully\")
except Exception as e:
    print(f\"  ERROR: {e}\")
"
echo ""

# Test 3: Invalid workflow ID
echo "Test 3: Invalid workflow ID"
echo '{}' | python3 l6/runner_v2.py invalid.workflow.id 2>&1 | \
  python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f\"  Status: {d['status']}\")
    if d['errors']:
        print(f\"  Error type: {d['errors'][0]['type']}\")
        if d['errors'][0]['type'] == 'unknown_workflow':
            print(f\"  ✓ Correctly identified unknown workflow\")
except Exception as e:
    print(f\"  ERROR: {e}\")
"
echo ""

# Test 4: Check workflow envelope structure
echo "Test 4: Validate envelope structure"
echo "$TEST_PAYLOAD" | python3 l6/runner_v2.py turbodrive.followup_only.v1 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    required = ['workflow_id', 'status', 'completed_steps', 'pending_steps', 'failed_steps', 'outputs', 'errors', 'trace_id', 'started_at', 'finished_at']
    missing = [f for f in required if f not in d]
    if not missing:
        print(f\"  ✓ All required envelope fields present\")
        print(f\"  Trace ID: {d['trace_id']}\")
    else:
        print(f\"  ✗ Missing fields: {', '.join(missing)}\")
except Exception as e:
    print(f\"  ERROR: {e}\")
"
echo ""

echo "=== All Workflow Tests Complete ==="
