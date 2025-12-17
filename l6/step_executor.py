#!/usr/bin/env python3
"""
Step Executor
Executes a single workflow step via dispatcher_mvp.
"""

from typing import Dict, Any
from l6.dispatcher_mvp import execute_skill


def execute_step(
    step: Dict[str, Any],
    workflow_payload: Dict[str, Any],
    previous_outputs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Execute a single workflow step.
    
    Args:
        step: Step definition with id, skill_id, input_mode, depends_on
        workflow_payload: Original workflow input payload
        previous_outputs: Dict mapping step_id to output from previous steps
        
    Returns:
        Step result envelope: {status, output, error, step_id, skill_id}
    """
    step_id = step.get("id")
    skill_id = step.get("skill_id")
    input_mode = step.get("input_mode", "direct")
    depends_on = step.get("depends_on", [])
    
    # Prepare skill payload based on input_mode
    if input_mode == "direct":
        # Pass workflow payload directly
        skill_payload = workflow_payload.copy()
    
    elif input_mode == "normalized":
        # Pass normalized payload directly (Phase C)
        # Normalized payload is already in the correct format
        skill_payload = workflow_payload.copy()
    
    elif input_mode == "merged":
        # Merge workflow payload with outputs from dependencies
        skill_payload = workflow_payload.copy()
        
        # Add outputs from dependencies
        for dep_step_id in depends_on:
            if dep_step_id in previous_outputs:
                dep_output = previous_outputs[dep_step_id]
                
                # Merge dependency output into payload
                # Simple strategy: add as nested object with step_id as key
                skill_payload[dep_step_id] = dep_output
    
    else:
        # Unknown input_mode, use direct
        skill_payload = workflow_payload.copy()
    
    # Execute skill via dispatcher
    try:
        result = execute_skill(skill_id, skill_payload)
        
        # Add step metadata
        result["step_id"] = step_id
        result["skill_id"] = skill_id
        
        return result
        
    except Exception as e:
        # Execution failed
        return {
            "status": "failed",
            "output": None,
            "error": {
                "type": "execution_error",
                "message": str(e)
            },
            "step_id": step_id,
            "skill_id": skill_id
        }


def check_dependencies(
    step: Dict[str, Any],
    completed_steps: list
) -> tuple:
    """
    Check if step dependencies are satisfied.
    
    Args:
        step: Step definition
        completed_steps: List of completed step IDs
        
    Returns:
        (satisfied: bool, missing: list)
    """
    depends_on = step.get("depends_on", [])
    
    missing = []
    for dep in depends_on:
        if dep not in completed_steps:
            missing.append(dep)
    
    return (len(missing) == 0, missing)
