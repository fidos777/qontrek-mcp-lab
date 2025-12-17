"""
KuasaTurbo Gateway Validators

Input validation for all endpoint requests.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.api.validators import validate_service_request as validate_service
from kuasaturbo.services.model_router import validate_model
from kuasaturbo.creative import engine as creative_engine


def validate_widget_id(widget_id: str) -> dict:
    """
    Validate widget ID exists
    
    Args:
        widget_id: Widget identifier
    
    Returns:
        {"valid": bool, "errors": list}
    """
    from l3.loader.widget_loader import load_widget
    
    try:
        load_widget(widget_id)
        return {"valid": True, "errors": []}
    except FileNotFoundError:
        return {"valid": False, "errors": [f"Widget not found: {widget_id}"]}
    except Exception as e:
        return {"valid": False, "errors": [f"Widget validation error: {str(e)}"]}


def validate_model_id(model_id: str) -> dict:
    """
    Validate model ID exists
    
    Args:
        model_id: Model identifier
    
    Returns:
        {"valid": bool, "errors": list}
    """
    if validate_model(model_id):
        return {"valid": True, "errors": []}
    else:
        return {"valid": False, "errors": [f"Model not found: {model_id}"]}


def validate_creative_task(task_type: str) -> dict:
    """
    Validate creative task type exists
    
    Args:
        task_type: Task type identifier
    
    Returns:
        {"valid": bool, "errors": list}
    """
    available_tasks = creative_engine.get_available_tasks()
    
    if task_type in available_tasks:
        return {"valid": True, "errors": []}
    else:
        return {
            "valid": False,
            "errors": [f"Task type not found: {task_type}. Available: {', '.join(available_tasks)}"]
        }


def validate_creative_style(style_id: str) -> dict:
    """
    Validate creative style exists
    
    Args:
        style_id: Style identifier
    
    Returns:
        {"valid": bool, "errors": list}
    """
    available_styles = creative_engine.get_available_styles()
    
    if style_id in available_styles:
        return {"valid": True, "errors": []}
    else:
        return {
            "valid": False,
            "errors": [f"Style not found: {style_id}. Available: {', '.join(available_styles)}"]
        }


def validate_creative_generation_request(payload: dict) -> dict:
    """
    Validate creative generation request
    
    Args:
        payload: Request payload
    
    Returns:
        {"valid": bool, "errors": list}
    """
    errors = []
    
    # Check required fields
    if 'task_type' not in payload:
        errors.append("Missing required field: task_type")
    
    if 'payload' not in payload:
        errors.append("Missing required field: payload")
    
    if errors:
        return {"valid": False, "errors": errors}
    
    # Validate task type
    task_validation = validate_creative_task(payload['task_type'])
    if not task_validation['valid']:
        errors.extend(task_validation['errors'])
    
    # Validate style if provided
    if 'style_override' in payload and payload['style_override']:
        style_validation = validate_creative_style(payload['style_override'])
        if not style_validation['valid']:
            errors.extend(style_validation['errors'])
    
    # Validate model if provided
    if 'model_override' in payload and payload['model_override']:
        model_validation = validate_model_id(payload['model_override'])
        if not model_validation['valid']:
            errors.extend(model_validation['errors'])
    
    if errors:
        return {"valid": False, "errors": errors}
    
    return {"valid": True, "errors": []}
