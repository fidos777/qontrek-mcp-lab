#!/usr/bin/env python3
"""
Workflow Loader
Loads workflow definitions from JSON files.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


# Workflow directory
WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"


def load_workflow(workflow_id: str) -> Optional[Dict[str, Any]]:
    """
    Load workflow definition by ID.
    
    Args:
        workflow_id: Workflow identifier (e.g., "kuasaturbo.launchkit.v1")
        
    Returns:
        Workflow definition dict or None if not found
        
    Raises:
        FileNotFoundError: If workflow file doesn't exist
        json.JSONDecodeError: If workflow JSON is invalid
    """
    workflow_file = WORKFLOWS_DIR / f"{workflow_id}.json"
    
    if not workflow_file.exists():
        raise FileNotFoundError(f"Workflow not found: {workflow_id}")
    
    with open(workflow_file, 'r') as f:
        workflow = json.load(f)
    
    # Validate basic structure
    if "id" not in workflow:
        raise ValueError(f"Workflow missing 'id' field: {workflow_id}")
    
    if "steps" not in workflow:
        raise ValueError(f"Workflow missing 'steps' field: {workflow_id}")
    
    if workflow["id"] != workflow_id:
        raise ValueError(f"Workflow ID mismatch: expected {workflow_id}, got {workflow['id']}")
    
    return workflow


def list_workflows() -> list:
    """
    List all available workflow IDs.
    
    Returns:
        List of workflow IDs
    """
    if not WORKFLOWS_DIR.exists():
        return []
    
    workflows = []
    for file in WORKFLOWS_DIR.glob("*.json"):
        # Extract workflow ID from filename
        workflow_id = file.stem
        workflows.append(workflow_id)
    
    return sorted(workflows)


def validate_workflow(workflow: Dict[str, Any]) -> tuple:
    """
    Validate workflow structure.
    
    Args:
        workflow: Workflow definition dict
        
    Returns:
        (is_valid: bool, errors: list)
    """
    errors = []
    
    # Check required fields
    if "id" not in workflow:
        errors.append("Missing 'id' field")
    
    if "steps" not in workflow:
        errors.append("Missing 'steps' field")
    
    if "steps" in workflow:
        if not isinstance(workflow["steps"], list):
            errors.append("'steps' must be a list")
        else:
            for i, step in enumerate(workflow["steps"]):
                if "id" not in step:
                    errors.append(f"Step {i} missing 'id' field")
                if "skill_id" not in step:
                    errors.append(f"Step {i} missing 'skill_id' field")
    
    return (len(errors) == 0, errors)
