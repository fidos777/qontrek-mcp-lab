#!/bin/bash
# Phase D: Setup script for API dependencies

echo "=== Phase D API Setup ==="
echo ""

# Check for python3.11
if command -v python3.11 &> /dev/null; then
  PYTHON_CMD="python3.11"
  echo "✓ Using python3.11"
elif command -v python3 &> /dev/null; then
  PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
  if [ "$PYTHON_VERSION" = "3.11" ]; then
    PYTHON_CMD="python3"
    echo "✓ Using python3 (version 3.11)"
  else
    echo "⚠ Warning: Python 3.11 not found, using python3 (version $PYTHON_VERSION)"
    echo "  Phase D requires Python 3.11 for FastAPI compatibility"
    PYTHON_CMD="python3"
  fi
else
  echo "✗ Error: Python 3 not found"
  exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
  echo "Creating virtual environment with $PYTHON_CMD..."
  $PYTHON_CMD -m venv venv
  echo "✓ Virtual environment created"
else
  echo "✓ Virtual environment already exists"
fi

# Install dependencies
echo "Installing dependencies..."
./venv/bin/pip install -q -r api/requirements.txt
echo "✓ Dependencies installed"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "To start the API server:"
echo "  ./api/server.sh"
echo ""
echo "To run API tests:"
echo "  bash tests/test_api.sh"
