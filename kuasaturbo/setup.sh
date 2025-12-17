#!/bin/bash

# KuasaTurbo Gateway Setup Script

echo "🔧 Setting up KuasaTurbo Gateway..."
echo "===================================="

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
REQUIRED_VERSION="3.11"

echo "✓ Detected Python: $PYTHON_VERSION"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.11+ required. Current: $PYTHON_VERSION"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found in project root."
    echo "Please run from project root where venv/ exists."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install fastapi==0.104.1 uvicorn==0.24.0 pydantic==1.10.13 pyyaml 'httpx<0.24'

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  ./kuasaturbo/server.sh"
echo ""
echo "Default configuration:"
echo "  API Key: kuasa123"
echo "  Host: 0.0.0.0"
echo "  Port: 8081"
echo ""
echo "To customize, set environment variables:"
echo "  export KUASATURBO_API_KEY=your_key"
echo "  export KUASATURBO_PORT=8082"
