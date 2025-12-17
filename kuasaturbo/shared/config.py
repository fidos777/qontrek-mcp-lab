"""
KuasaTurbo Configuration

Centralized configuration for KuasaTurbo Gateway.
"""

import os

# API Configuration
API_KEY = os.getenv("KUASATURBO_API_KEY", "kuasa123")
API_HOST = os.getenv("KUASATURBO_HOST", "0.0.0.0")
API_PORT = int(os.getenv("KUASATURBO_PORT", "8081"))

# Model Configuration
DEFAULT_MODEL = "mock"  # Default to mock mode
SUPPORTED_MODELS = ["mock", "gpt-4", "gpt-3.5-turbo", "claude-3"]

# Path Configuration
WIDGETS_PATH = "l3/widgets"
WORKFLOWS_PATH = "l8/workflows"
PERSONAS_PATH = "l5/personas"
SERVICE_REGISTRY_PATH = "services/service_registry.yaml"

# Execution Configuration
MAX_PROMPT_LENGTH = 4000
TIMEOUT_SECONDS = 30
