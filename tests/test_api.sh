#!/bin/bash
# Phase D: API Test Suite
# Tests REST API endpoints with curl

API_URL="http://localhost:8080"
VALID_KEY="test123"
INVALID_KEY="wrong_key"

echo "=== Testing Phase D REST API ==="
echo ""

# Start API server in background
echo "Starting API server..."
export API_KEY="test123"
source venv/bin/activate
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8080 --log-level error > /tmp/api_server.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
  echo "✗ Failed to start API server"
  cat /tmp/api_server.log
  exit 1
fi

echo "✓ API server started (PID: $SERVER_PID)"
echo ""

# Cleanup function
cleanup() {
  echo ""
  echo "Stopping API server..."
  kill $SERVER_PID 2>/dev/null
  wait $SERVER_PID 2>/dev/null
  echo "✓ Server stopped"
}

# Register cleanup on exit
trap cleanup EXIT

# Track test results
PASSED=0
FAILED=0

# Test 1: Missing API key
response=$(curl -s -X POST "$API_URL/skills/execute" \
  -H "Content-Type: application/json" \
  -d '{"skill_id":"launchkit.branding.generate.v1","payload":{}}')

error_type=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', {}).get('type', 'unknown'))" 2>/dev/null)

if [ "$error_type" = "unauthorized" ]; then
  PASSED=$((PASSED + 1))
else
  FAILED=$((FAILED + 1))
fi

# Test 2: Invalid API key
response=$(curl -s -X POST "$API_URL/skills/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $INVALID_KEY" \
  -d '{"skill_id":"launchkit.branding.generate.v1","payload":{}}')

error_type=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', {}).get('type', 'unknown'))" 2>/dev/null)

if [ "$error_type" = "unauthorized" ]; then
  PASSED=$((PASSED + 1))
else
  FAILED=$((FAILED + 1))
fi

# Test 3: Valid skill execution
response=$(curl -s -X POST "$API_URL/skills/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $VALID_KEY" \
  -d '{
    "skill_id": "launchkit.branding.generate.v1",
    "payload": {
      "brand_name": "TestAPI",
      "mission": "Test mission",
      "value_proposition": "Test value prop",
      "brand_themes": ["Innovation", "Quality"],
      "icp": {
        "demographics": "Test audience"
      }
    }
  }')

status=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null)

if [ "$status" = "success" ]; then
  PASSED=$((PASSED + 1))
else
  FAILED=$((FAILED + 1))
fi

# Test 4: Valid workflow execution
response=$(curl -s -X POST "$API_URL/workflows/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $VALID_KEY" \
  -d '{
    "workflow_id": "turbodrive.followup_only.v1",
    "payload": {
      "brand_name": "TestAPI",
      "mission": "Test mission",
      "value_proposition": "Test value prop",
      "brand_themes": ["Innovation", "Quality"],
      "icp": {
        "demographics": "Test audience"
      }
    }
  }')

status=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null)

if [ "$status" = "success" ]; then
  PASSED=$((PASSED + 1))
else
  FAILED=$((FAILED + 1))
fi

# Test 5: Invalid skill ID
response=$(curl -s -X POST "$API_URL/skills/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $VALID_KEY" \
  -d '{
    "skill_id": "invalid.skill.id",
    "payload": {}
  }')

status=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null)
error_type=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('error', {}).get('type', 'unknown'))" 2>/dev/null)

if [ "$status" = "failed" ] && [ "$error_type" = "unknown_skill" ]; then
  PASSED=$((PASSED + 1))
else
  FAILED=$((FAILED + 1))
fi

# Test 6: Invalid workflow ID
response=$(curl -s -X POST "$API_URL/workflows/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $VALID_KEY" \
  -d '{
    "workflow_id": "invalid.workflow.id",
    "payload": {}
  }')

status=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null)
error_type=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('errors', [{}])[0].get('type', 'unknown'))" 2>/dev/null)

if [ "$status" = "failed" ] && [ "$error_type" = "unknown_workflow" ]; then
  PASSED=$((PASSED + 1))
else
  FAILED=$((FAILED + 1))
fi

# Test 7: Missing brand fields (normalization error)
response=$(curl -s -X POST "$API_URL/workflows/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $VALID_KEY" \
  -d '{
    "workflow_id": "kuasaturbo.launchkit.v1",
    "payload": {
      "tagline": "Missing required fields"
    }
  }')

status=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null)
error_type=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('errors', [{}])[0].get('type', 'unknown'))" 2>/dev/null)

if [ "$status" = "failed" ] && [ "$error_type" = "brand_context_invalid" ]; then
  PASSED=$((PASSED + 1))
else
  FAILED=$((FAILED + 1))
fi

# Test 8: Pure JSON output (no logging noise)
response=$(curl -s -X POST "$API_URL/skills/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $VALID_KEY" \
  -d '{
    "skill_id": "launchkit.branding.generate.v1",
    "payload": {
      "brand_name": "TestAPI",
      "mission": "Test mission",
      "value_proposition": "Test value prop",
      "brand_themes": ["Innovation"],
      "icp": {"demographics": "Test"}
    }
  }')

# Check if response is valid JSON (no logging mixed in)
if echo "$response" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
  PASSED=$((PASSED + 1))
else
  FAILED=$((FAILED + 1))
fi

echo ""
echo "=== Phase D API Tests Complete ==="
echo ""
if [ $FAILED -eq 0 ]; then
  echo "✅ PASS: All $PASSED tests passed"
  exit 0
else
  echo "❌ FAIL: $PASSED passed, $FAILED failed"
  exit 1
fi
