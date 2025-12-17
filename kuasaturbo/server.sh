#!/bin/bash

# KuasaTurbo Gateway Server Startup Script

echo "🚀 Starting KuasaTurbo Gateway..."
echo "================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check Python version
PYTHON_VERSION=$(python3 --version)
echo "✓ Python: $PYTHON_VERSION"

# Set environment variables
export KUASATURBO_API_KEY="${KUASATURBO_API_KEY:-kuasa123}"
export KUASATURBO_HOST="${KUASATURBO_HOST:-0.0.0.0}"
export KUASATURBO_PORT="${KUASATURBO_PORT:-8081}"

echo "✓ API Key: $KUASATURBO_API_KEY"
echo "✓ Host: $KUASATURBO_HOST"
echo "✓ Port: $KUASATURBO_PORT"
echo ""
echo "📡 Starting server..."
echo "================================"

# Start FastAPI server
cd "$(dirname "$0")/.."
python3 -m uvicorn kuasaturbo.api.gateway:app \
    --host "$KUASATURBO_HOST" \
    --port "$KUASATURBO_PORT" \
    --reload

# Note: --reload enables auto-reload on code changes (dev mode)
# For production, remove --reload flag
