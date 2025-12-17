"""
KuasaTurbo Service Router

Orchestrates service execution: widget → workflow → persona → AI generation
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.api.validators import load_service_registry
from kuasaturbo.services.prompt_builder import build_prompt
from kuasaturbo.services.ai_client import generate_output
from kuasaturbo.services.persona_loader import load_persona
from kuasaturbo.services.model_router import resolve_model
from l3.loader.widget_loader import load_widget
from l8.loader.workflow_loader import load_workflow


def execute_service(
    service_id: str,
    payload: dict,
    persona_override: str = None,
    model_override: str = None
) -> dict:
    """
    Execute a KuasaTurbo service
    
    Flow:
    1. Load service configuration
    2. Load widget, workflow, persona
    3. Build prompt from workflow + persona
    4. Generate AI output (mock or real)
    5. Return structured response
    
    Args:
        service_id: Service identifier
        payload: Widget field values
        persona_override: Optional persona override
        model_override: Optional model override
    
    Returns:
        {
            "status": "success",
            "service_id": str,
            "workflow_id": str,
            "persona_id": str,
            "output": dict,
            "metadata": dict
        }
    """
    # Load service registry
    registry = load_service_registry()
    service = registry['services'][service_id]
    
    # Load components
    widget = load_widget(service['widget_id'])
    workflow = load_workflow(service['workflow_id'])
    persona_id = persona_override or service['persona_id']
    persona = load_persona(persona_id)
    
    # Resolve model using priority order
    model = resolve_model(
        workflow=workflow,
        persona=persona,
        model_override=model_override
    )
    
    # Build prompt
    prompt_data = build_prompt(
        workflow=workflow,
        persona=persona,
        payload=payload
    )
    
    # Generate output
    output = generate_output(
        prompt=prompt_data['prompt'],
        workflow=workflow,
        persona=persona,
        model=model
    )
    
    # Build response
    return {
        "status": "success",
        "service_id": service_id,
        "workflow_id": workflow['id'],
        "persona_id": persona_id,
        "output": output,
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "widget_id": widget['widget_id'],
            "vertical": service['vertical'],
            "execution_mode": "mock"  # Always mock in Phase XII
        }
    }
