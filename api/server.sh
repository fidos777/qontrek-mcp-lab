#!/bin/bash
# Phase D: Start API server

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
  echo "[INFO] Creating virtual environment..."
  python3 -m venv venv
  echo "[INFO] Installing dependencies..."
  ./venv/bin/pip install -q -r api/requirements.txt
fi

# Activate venv
source venv/bin/activate

# Set default API key if not provided
if [ -z "$API_KEY" ]; then
  export API_KEY="test123"
  echo "[INFO] Using default API_KEY=test123 for development"
fi

# Start uvicorn server
echo "[INFO] Starting LaunchKit API server on http://0.0.0.0:8080"
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8080 --log-level warning
