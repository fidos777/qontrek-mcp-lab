#!/bin/bash

# KuasaTurbo Test Suite Runner

echo "🧪 Running KuasaTurbo Test Suite"
echo "================================="
echo ""

# Change to test directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d "../../venv" ]; then
    source ../../venv/bin/activate
fi

# Track test results
FAILED=0

# Test 1: Gateway Health
echo "Test 1: Gateway Health"
python3 test_gateway_health.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 2: Validators
echo "Test 2: Validators"
python3 test_validators.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 3: Prompt Builder
echo "Test 3: Prompt Builder"
python3 test_prompt_builder.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 4: AI Client
echo "Test 4: AI Client"
python3 test_ai_client.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 5: Service Execution
echo "Test 5: Service Execution (End-to-End)"
python3 test_service_execution.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 6: Model Router
echo "Test 6: Model Router"
python3 test_model_router.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 7: Creative Engine
echo "Test 7: Creative Engine"
python3 test_creative_engine.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 8: Gateway Endpoints
echo "Test 8: Gateway Endpoints (Phase XIV)"
python3 test_endpoints.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 9: Auth Layer
echo "Test 9: Auth Layer (Phase XV)"
python3 test_auth_layer.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 10: Rate Limiting
echo "Test 10: Rate Limiting (Phase XVI)"
python3 test_ratelimit.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 11: Logging & Audit
echo "Test 11: Logging & Audit (Phase XVII-A)"
python3 test_logging.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 12: Resource Layer
echo "Test 12: Resource Layer (Phase XVII-B)"
python3 test_resources.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 13: Business Layer
echo "Test 13: Business Layer (Phase XVIII)"
python3 test_business.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 14: Platform Layer
echo "Test 14: Platform Layer (Phase XIX)"
python3 test_platform.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 15: Integration Smoke Tests
echo "Test 15: Integration Smoke Tests (Phase XX-Lite)"
python3 test_integration.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Test 16: LLM Provider Layer
echo "Test 16: LLM Provider Layer (Phase XXI)"
python3 test_llm.py
if [ $? -ne 0 ]; then
    FAILED=$((FAILED + 1))
fi
echo ""

# Summary
echo "================================="
if [ $FAILED -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ $FAILED test suite(s) failed"
    exit 1
fi
