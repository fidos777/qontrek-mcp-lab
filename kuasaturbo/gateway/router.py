"""
KuasaTurbo Gateway Router

Routing logic for all endpoints.
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.api.router import execute_service
from kuasaturbo.api.validators import load_service_registry
from kuasaturbo.services.model_router import get_supported_models, get_model_info
from kuasaturbo.creative import engine as creative_engine
from l3.loader.widget_loader import load_widget, list_widgets


def get_widgets_list() -> dict:
    """
    Get list of all available widgets
    
    Returns:
        {
            "widgets": [
                {
                    "widget_id": str,
                    "name": str,
                    "vertical": str,
                    "description": str
                }
            ],
            "count": int
        }
    """
    print("[Endpoint] Fetching widgets list")
    
    widget_ids = list_widgets()
    
    widget_list = []
    for widget_id in widget_ids:
        try:
            widget = load_widget(widget_id)
            widget_list.append({
                "widget_id": widget['widget_id'],
                "name": widget['widget_name'],
                "vertical": widget['vertical'],
                "description": widget.get('description', '')
            })
        except Exception as e:
            print(f"[Endpoint] Warning: Failed to load widget {widget_id}: {str(e)}")
    
    return {
        "widgets": widget_list,
        "count": len(widget_list)
    }


def get_widget_details(widget_id: str) -> dict:
    """
    Get detailed widget information
    
    Args:
        widget_id: Widget identifier
    
    Returns:
        Widget metadata including fields, workflow, persona
    """
    print(f"[Endpoint] Fetching widget details: {widget_id}")
    
    widget = load_widget(widget_id)
    
    return {
        "widget_id": widget['widget_id'],
        "widget_name": widget['widget_name'],
        "vertical": widget['vertical'],
        "description": widget.get('description', ''),
        "fields": widget.get('fields', []),
        "workflow": widget.get('workflow', {}),
        "presentation": widget.get('presentation', {})
    }


def execute_service_endpoint(
    service_id: str,
    payload: dict,
    persona_override: str = None,
    model_override: str = None
) -> dict:
    """
    Execute service (wrapper around existing execute_service)
    
    Args:
        service_id: Service identifier
        payload: Widget field values
        persona_override: Optional persona override
        model_override: Optional model override
    
    Returns:
        Service execution result
    """
    print(f"[Endpoint] Executing service: {service_id}")
    
    return execute_service(
        service_id=service_id,
        payload=payload,
        persona_override=persona_override,
        model_override=model_override
    )


def get_models_list() -> dict:
    """
    Get list of all available models
    
    Returns:
        {
            "models": [
                {
                    "model_id": str,
                    "provider": str,
                    "description": str
                }
            ],
            "count": int
        }
    """
    print("[Endpoint] Fetching models list")
    
    models = get_supported_models()
    
    model_list = []
    for model_id in models:
        model_info = get_model_info(model_id)
        if model_info:
            model_list.append({
                "model_id": model_id,
                "provider": model_info.get('provider', 'unknown'),
                "description": model_info.get('description', '')
            })
    
    return {
        "models": model_list,
        "count": len(model_list)
    }


def get_model_details(model_id: str) -> dict:
    """
    Get detailed model information
    
    Args:
        model_id: Model identifier
    
    Returns:
        Model metadata
    """
    print(f"[Endpoint] Fetching model details: {model_id}")
    
    model_info = get_model_info(model_id)
    
    if not model_info:
        raise ValueError(f"Model not found: {model_id}")
    
    return {
        "model_id": model_id,
        **model_info
    }


def resolve_model_endpoint(
    workflow_id: str = None,
    persona_id: str = None,
    model_override: str = None
) -> dict:
    """
    Resolve which model to use based on priority
    
    Args:
        workflow_id: Optional workflow ID
        persona_id: Optional persona ID
        model_override: Optional model override
    
    Returns:
        {
            "model": str,
            "resolution_source": str,
            "priority_order": list
        }
    """
    print("[Endpoint] Resolving model")
    
    from kuasaturbo.services.model_router import resolve_model
    from l8.loader.workflow_loader import load_workflow
    from kuasaturbo.services.persona_loader import load_persona
    
    # Load workflow and persona if provided
    workflow = {}
    persona = {}
    
    if workflow_id:
        try:
            workflow = load_workflow(workflow_id)
        except Exception:
            pass
    
    if persona_id:
        try:
            persona = load_persona(persona_id)
        except Exception:
            pass
    
    # Resolve model
    model = resolve_model(
        workflow=workflow,
        persona=persona,
        model_override=model_override
    )
    
    # Determine resolution source
    resolution_source = "global_default"
    if model_override:
        resolution_source = "override"
    elif workflow.get('preferred_model'):
        resolution_source = "workflow"
    elif persona.get('default_model'):
        resolution_source = "persona"
    
    return {
        "model": model,
        "resolution_source": resolution_source,
        "priority_order": ["override", "workflow", "persona", "global_default"]
    }


def get_creative_tasks_list() -> dict:
    """
    Get list of all available creative tasks
    
    Returns:
        {
            "tasks": [
                {
                    "task_type": str,
                    "description": str,
                    "preferred_model": str,
                    "default_style": str
                }
            ],
            "count": int
        }
    """
    print("[Endpoint] Fetching creative tasks list")
    
    tasks = creative_engine.get_available_tasks()
    
    task_list = []
    for task_type in tasks:
        try:
            task_config = creative_engine.resolve_creative_task(task_type)
            task_list.append({
                "task_type": task_type,
                "description": task_config.get('description', ''),
                "preferred_model": task_config.get('preferred_model', 'mock'),
                "default_style": task_config.get('default_style', 'simple_clean')
            })
        except Exception as e:
            print(f"[Endpoint] Warning: Failed to load task {task_type}: {str(e)}")
    
    return {
        "tasks": task_list,
        "count": len(task_list)
    }


def get_creative_styles_list() -> dict:
    """
    Get list of all available creative styles
    
    Returns:
        {
            "styles": [
                {
                    "style_id": str,
                    "name": str,
                    "colors": list,
                    "usage": list
                }
            ],
            "count": int
        }
    """
    print("[Endpoint] Fetching creative styles list")
    
    styles = creative_engine.get_available_styles()
    
    style_list = []
    for style_id in styles:
        try:
            style_profile = creative_engine.load_style_profile(style_id)
            style_list.append({
                "style_id": style_id,
                "name": style_profile.get('name', style_id),
                "colors": style_profile.get('colors', []),
                "usage": style_profile.get('usage', [])
            })
        except Exception as e:
            print(f"[Endpoint] Warning: Failed to load style {style_id}: {str(e)}")
    
    return {
        "styles": style_list,
        "count": len(style_list)
    }


def execute_creative_generation(
    task_type: str,
    payload: dict,
    persona_id: str = None,
    style_override: str = None,
    model_override: str = None
) -> dict:
    """
    Execute creative generation task
    
    Args:
        task_type: Task type identifier
        payload: Task-specific input data
        persona_id: Optional persona ID
        style_override: Optional style override
        model_override: Optional model override
    
    Returns:
        Creative generation result
    """
    print(f"[Endpoint] Executing creative generation: {task_type}")
    
    from kuasaturbo.services.persona_loader import load_persona
    
    # Load persona or use default
    persona = {"persona_name": "System", "role": "Generator"}
    if persona_id:
        try:
            persona = load_persona(persona_id)
        except Exception as e:
            print(f"[Endpoint] Warning: Failed to load persona {persona_id}, using default: {str(e)}")
    
    # Execute generation
    result = creative_engine.execute_generation(
        task_type=task_type,
        payload=payload,
        persona=persona,
        brand_profile=None,
        style_override=style_override,
        model_override=model_override,
        mock_mode=True
    )
    
    # Add execution metadata
    result['execution'] = {
        "timestamp": datetime.now().isoformat(),
        "task_type": task_type,
        "persona_id": persona_id or "default",
        "mode": "mock"
    }
    
    return result
