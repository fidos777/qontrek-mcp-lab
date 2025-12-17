"""
KuasaTurbo Request Validators

Validates service requests against widget schemas and service registry.
"""

import sys
import os
import yaml
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from l3.loader.widget_loader import load_widget
from kuasaturbo.services.persona_loader import load_persona
from kuasaturbo.services.model_router import validate_model


# Get project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent


def load_service_registry():
    """Load service registry"""
    registry_path = PROJECT_ROOT / "services" / "service_registry.yaml"
    
    if not registry_path.exists():
        raise FileNotFoundError(f"Service registry not found: {registry_path}")
    
    with open(registry_path, 'r') as f:
        return yaml.safe_load(f)


def validate_service_request(service_id: str, payload: dict, persona_override: str = None, model_override: str = None) -> dict:
    """
    Validate service request
    
    Returns:
        {
            "valid": bool,
            "errors": list,
            "service": dict (if valid)
        }
    """
    errors = []
    
    # Load service registry
    try:
        registry = load_service_registry()
    except Exception as e:
        return {
            "valid": False,
            "errors": [f"Failed to load service registry: {str(e)}"]
        }
    
    # Check if service exists
    if service_id not in registry.get('services', {}):
        return {
            "valid": False,
            "errors": [f"Service not found: {service_id}"]
        }
    
    service = registry['services'][service_id]
    
    # Load widget
    widget_id = service['widget_id']
    try:
        widget = load_widget(widget_id)
    except Exception as e:
        errors.append(f"Failed to load widget {widget_id}: {str(e)}")
        return {"valid": False, "errors": errors}
    
    # Validate required fields
    for field in widget.get('fields', []):
        if field.get('required', False):
            field_id = field['id']
            if field_id not in payload:
                errors.append(f"Missing required field: {field_id}")
            elif not payload[field_id]:
                errors.append(f"Field cannot be empty: {field_id}")
    
    # Validate field types
    for field in widget.get('fields', []):
        field_id = field['id']
        if field_id in payload:
            field_type = field.get('type', 'text')
            value = payload[field_id]
            
            if field_type == 'number':
                if not isinstance(value, (int, float)):
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        errors.append(f"Field {field_id} must be a number")
            
            elif field_type == 'checkbox':
                if not isinstance(value, bool):
                    errors.append(f"Field {field_id} must be a boolean")
            
            elif field_type == 'select':
                options = field.get('options', [])
                if options and value not in options:
                    errors.append(f"Field {field_id} must be one of: {', '.join(options)}")
    
    # Validate persona override if provided
    if persona_override:
        try:
            load_persona(persona_override)
        except Exception as e:
            errors.append(f"Invalid persona override: {str(e)}")
    
    # Validate model override if provided
    if model_override:
        if not validate_model(model_override):
            errors.append(f"Invalid model override: {model_override}")
    
    if errors:
        return {"valid": False, "errors": errors}
    
    return {
        "valid": True,
        "errors": [],
        "service": service
    }
