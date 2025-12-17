"""
KuasaTurbo Model Router

Routes requests to appropriate AI models based on:
1. Explicit override
2. Workflow preference
3. Persona default
4. Global default

All models run in MOCK MODE (no external API calls).
"""

import yaml
import os
from typing import Optional, Dict, Any, List
from pathlib import Path


# Get project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent


def load_model_registry() -> Dict[str, Any]:
    """Load model registry from config"""
    registry_path = PROJECT_ROOT / "config" / "model_registry.yaml"
    
    if not registry_path.exists():
        raise FileNotFoundError(f"Model registry not found: {registry_path}")
    
    with open(registry_path, 'r') as f:
        return yaml.safe_load(f)


def get_supported_models() -> List[str]:
    """
    Get list of all supported models
    
    Returns:
        List of model identifiers
    """
    registry = load_model_registry()
    return list(registry['models'].keys())


def validate_model(model: str) -> bool:
    """
    Check if model is supported
    
    Args:
        model: Model identifier
    
    Returns:
        True if model exists in registry, False otherwise
    """
    supported = get_supported_models()
    return model in supported


def get_model_info(model: str) -> Optional[Dict[str, Any]]:
    """
    Get model information from registry
    
    Args:
        model: Model identifier
    
    Returns:
        Model info dict or None if not found
    """
    registry = load_model_registry()
    return registry['models'].get(model)


def resolve_model(
    workflow: Dict[str, Any],
    persona: Dict[str, Any],
    model_override: Optional[str] = None
) -> str:
    """
    Resolve which model to use based on priority order:
    1. model_override (highest priority)
    2. workflow.preferred_model
    3. persona.default_model
    4. global default_model (lowest priority)
    
    Args:
        workflow: Workflow definition
        persona: Persona definition
        model_override: Optional explicit model override
    
    Returns:
        Model identifier to use
    """
    registry = load_model_registry()
    default_model = registry['default_model']
    
    # Priority 1: Explicit override
    if model_override:
        if validate_model(model_override):
            return model_override
        else:
            # Invalid override, fall through to next priority
            print(f"[ModelRouter] Invalid override '{model_override}', falling back")
    
    # Priority 2: Workflow preference
    if 'preferred_model' in workflow:
        preferred = workflow['preferred_model']
        if validate_model(preferred):
            return preferred
    
    # Priority 3: Persona default
    if 'default_model' in persona:
        persona_default = persona['default_model']
        if validate_model(persona_default):
            return persona_default
    
    # Priority 4: Global default
    return default_model


def get_provider(model: str) -> str:
    """
    Get provider for a model
    
    Args:
        model: Model identifier
    
    Returns:
        Provider name (openai, anthropic, google, groq, internal)
    """
    model_info = get_model_info(model)
    if model_info:
        return model_info['provider']
    return 'internal'  # Fallback to internal/mock
