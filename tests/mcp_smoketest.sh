#!/bin/bash

# MCP Smoke Test Script
# Tests the MCP server with all three kreator skills

set -e  # Exit on error

echo "=========================================="
echo "MCP Server Smoke Test"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to send JSON-RPC request
send_request() {
    local method=$1
    local params=$2
    local id=$3
    
    echo "{\"jsonrpc\":\"2.0\",\"id\":${id},\"method\":\"${method}\",\"params\":${params}}"
}

# Function to test a request
test_request() {
    local name=$1
    local method=$2
    local params=$3
    local id=$4
    
    echo -e "${YELLOW}Testing: ${name}${NC}"
    
    local request=$(send_request "$method" "$params" "$id")
    local response=$(echo "$request" | python3 mcp_server.py 2>/dev/null)
    
    if echo "$response" | grep -q '"result"'; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "Response: $response"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "Step 1: Testing initialize"
echo "-------------------------------------------"
test_request "Initialize" "initialize" '{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test-client","version":"1.0.0"}}' 1
echo ""

echo "Step 2: Testing tools/list"
echo "-------------------------------------------"
test_request "List Tools" "tools/list" '{}' 2
echo ""

echo "Step 3: Testing brandpack.slogan.v1"
echo "-------------------------------------------"
SLOGAN_INPUT='{
  "brand_name": "FlowMind",
  "industry": "SaaS/Productivity",
  "target_audience": "Remote workers and digital nomads aged 25-40",
  "brand_values": ["efficiency", "simplicity", "innovation", "focus"],
  "tone": "professional",
  "language": "en",
  "count": 5
}'
test_request "Generate Slogan" "tools/call" "{\"name\":\"generate_slogan\",\"arguments\":${SLOGAN_INPUT}}" 3
echo ""

echo "Step 4: Testing graphicgen.socialpack.v1"
echo "-------------------------------------------"
GRAPHICS_INPUT='{
  "campaign_name": "FlowMind Launch",
  "campaign_goal": "announcement",
  "message": "Introducing FlowMind - AI-powered productivity that adapts to how you work",
  "brand_identity": {
    "colors": ["#0066FF", "#00C9FF", "#1A1A1A", "#F5F5F5"],
    "fonts": ["Inter", "Space Grotesk"],
    "style": "modern"
  },
  "platforms": ["instagram", "linkedin", "twitter"],
  "content_type": "product",
  "variations": 3,
  "include_copy": true,
  "language": "en"
}'
test_request "Generate Social Graphics" "tools/call" "{\"name\":\"generate_social_graphics\",\"arguments\":${GRAPHICS_INPUT}}" 4
echo ""

echo "Step 5: Testing pagegen.landingpage.v1"
echo "-------------------------------------------"
LANDING_INPUT='{
  "page_title": "FlowMind - AI Productivity for Remote Teams",
  "page_goal": "signup",
  "product_name": "FlowMind",
  "value_proposition": "Reclaim 10+ hours every week with AI that automates your workflow",
  "target_audience": "Remote workers and distributed teams struggling with productivity",
  "key_benefits": [
    "Save 10+ hours per week on repetitive tasks",
    "Integrate with tools you already use",
    "AI that learns and adapts to your work style"
  ],
  "cta_primary": "Start Free Trial",
  "tone": "professional"
}'
test_request "Generate Landing Page" "tools/call" "{\"name\":\"generate_landing_page\",\"arguments\":${LANDING_INPUT}}" 5
echo ""

echo "=========================================="
echo "Test Results"
echo "=========================================="
echo -e "Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Failed: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed.${NC}"
    exit 1
fi
