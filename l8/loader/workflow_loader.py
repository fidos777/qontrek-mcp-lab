#!/usr/bin/env python3
"""
KuasaTurbo Workflow Loader (L8)
Loads and validates stateless workflows - NO GOVERNANCE
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

# Forbidden keys that indicate governance contamination
FORBIDDEN_KEYS = [
    "governance",
    "governance_gate",
    "ledger",
    "ledger_commit",
    "audit",
    "sla",
    "drift",
    "exception",
    "multi_approval",
    "certification",
    "seal"
]

def get_workflows_dir() -> Path:
    """Get path to workflows directory."""
    return Path(__file__).parent.parent / "workflows"

def list_workflows() -> List[str]:
    """
    Return a list of workflow_ids from l8/workflows/
    
    Returns:
        List of workflow IDs (without .json extension)
    """
    workflows_dir = get_workflows_dir()
    if not workflows_dir.exists():
        print(f"[WorkflowLoader] Workflows directory not found: {workflows_dir}")
        return []
    
    workflow_files = list(workflows_dir.glob("*.json"))
    workflow_ids = [f.stem for f in workflow_files]
    
    print(f"[WorkflowLoader] Found {len(workflow_ids)} workflows")
    return sorted(workflow_ids)

def check_forbidden_keys(data: dict, path: str = "") -> List[str]:
    """
    Recursively check for forbidden governance keys.
    
    Args:
        data: Dictionary to check
        path: Current path in nested structure
        
    Returns:
        List of forbidden keys found with their paths
    """
    violations = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            
            # Check if key is forbidden
            if key in FORBIDDEN_KEYS:
                violations.append(current_path)
            
            # Recurse into nested structures
            if isinstance(value, (dict, list)):
                violations.extend(check_forbidden_keys(value, current_path))
    
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]"
            if isinstance(item, (dict, list)):
                violations.extend(check_forbidden_keys(item, current_path))
    
    return violations

def validate_workflow(workflow: dict) -> Tuple[bool, List[str]]:
    """
    Validate workflow dict against forbidden keys.
    
    Args:
        workflow: Workflow dictionary to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check for forbidden governance keys
    forbidden = check_forbidden_keys(workflow)
    if forbidden:
        errors.append(f"Forbidden governance keys found: {', '.join(forbidden)}")
        return False, errors
    
    # Validate required fields
    required_fields = ["id", "description", "version", "steps"]
    for field in required_fields:
        if field not in workflow:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Validate steps array
    if "steps" in workflow:
        if not isinstance(workflow["steps"], list):
            errors.append("'steps' must be an array")
        elif len(workflow["steps"]) == 0:
            errors.append("'steps' array cannot be empty")
    
    # Check if workflow is marked as stateless (KuasaTurbo requirement)
    if workflow.get("stateless") is not True:
        # Warning, not error - some workflows might not have this flag
        print(f"[WorkflowLoader] Warning: Workflow {workflow.get('id')} not explicitly marked as stateless")
    
    if errors:
        return False, errors
    
    return True, []

def load_workflow(workflow_id: str) -> dict:
    """
    Load and validate a workflow by workflow_id.
    
    Args:
        workflow_id: Workflow identifier (e.g., "content_idea_workflow.v1")
        
    Returns:
        Validated workflow dictionary
        
    Raises:
        FileNotFoundError: If workflow file not found
        ValueError: If workflow validation fails
    """
    workflows_dir = get_workflows_dir()
    workflow_path = workflows_dir / f"{workflow_id}.json"
    
    if not workflow_path.exists():
        raise FileNotFoundError(f"Workflow not found: {workflow_id}")
    
    print(f"[WorkflowLoader] Loading workflow: {workflow_id}")
    
    # Load JSON
    with open(workflow_path, 'r') as f:
        workflow = json.load(f)
    
    # Validate
    is_valid, errors = validate_workflow(workflow)
    
    if not is_valid:
        error_msg = f"Workflow validation failed for {workflow_id}:\n" + "\n".join(f"  - {e}" for e in errors)
        print(f"[WorkflowLoader] ERROR: {error_msg}")
        raise ValueError(error_msg)
    
    # Log success
    print(f"[WorkflowLoader] Workflow ID: {workflow.get('id')}")
    print(f"[WorkflowLoader] Description: {workflow.get('description')}")
    print(f"[WorkflowLoader] Steps: {len(workflow.get('steps', []))}")
    if "persona_id" in workflow:
        print(f"[WorkflowLoader] Persona: {workflow.get('persona_id')}")
    print(f"[WorkflowLoader] Stateless: {workflow.get('stateless', False)}")
    
    return workflow

def get_workflow_info(workflow_id: str) -> dict:
    """
    Get basic workflow information without full validation.
    
    Args:
        workflow_id: Workflow identifier
        
    Returns:
        Dictionary with basic workflow info
    """
    try:
        workflow = load_workflow(workflow_id)
        return {
            "workflow_id": workflow.get("id"),
            "description": workflow.get("description"),
            "version": workflow.get("version"),
            "step_count": len(workflow.get("steps", [])),
            "persona_id": workflow.get("persona_id"),
            "stateless": workflow.get("stateless", False)
        }
    except Exception as e:
        return {
            "workflow_id": workflow_id,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test loader
    print("=== Workflow Loader Test ===\n")
    
    workflows = list_workflows()
    print(f"\nFound {len(workflows)} workflows:")
    for w in workflows:
        print(f"  - {w}")
    
    if workflows:
        print(f"\nTesting load of first workflow: {workflows[0]}")
        try:
            workflow = load_workflow(workflows[0])
            print(f"✓ Successfully loaded {workflows[0]}")
        except Exception as e:
            print(f"✗ Failed to load {workflows[0]}: {e}")
