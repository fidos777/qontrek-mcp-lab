#!/usr/bin/env python3
"""
Workflow Envelope Helpers
Builds standardized workflow result envelopes.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List


def create_workflow_envelope(
    workflow_id: str,
    status: str,
    completed_steps: List[str],
    pending_steps: List[str],
    failed_steps: List[str],
    outputs: Dict[str, Any],
    errors: List[Dict[str, Any]],
    started_at: str,
    finished_at: str = None
) -> Dict[str, Any]:
    """
    Create standardized workflow envelope.
    
    Args:
        workflow_id: Workflow identifier
        status: "success" | "partial" | "failed"
        completed_steps: List of completed step IDs
        pending_steps: List of pending step IDs
        failed_steps: List of failed step IDs
        outputs: Dict mapping step_id to output
        errors: List of error objects
        started_at: ISO 8601 start timestamp
        finished_at: ISO 8601 finish timestamp (optional)
        
    Returns:
        Workflow envelope dict
    """
    if finished_at is None:
        finished_at = datetime.now().isoformat() + "Z"
    
    return {
        "workflow_id": workflow_id,
        "status": status,
        "completed_steps": completed_steps,
        "pending_steps": pending_steps,
        "failed_steps": failed_steps,
        "outputs": outputs,
        "errors": errors,
        "trace_id": f"wf_{uuid.uuid4().hex[:8]}",
        "started_at": started_at,
        "finished_at": finished_at
    }


def determine_status(completed: List[str], failed: List[str], total: int) -> str:
    """
    Determine workflow status based on step results.
    
    Args:
        completed: List of completed step IDs
        failed: List of failed step IDs
        total: Total number of steps
        
    Returns:
        "success" | "partial" | "failed"
    """
    if len(failed) == 0 and len(completed) == total:
        return "success"
    elif len(completed) > 0 and len(failed) > 0:
        return "partial"
    elif len(failed) > 0 and len(completed) == 0:
        return "failed"
    else:
        return "partial"


def create_error(step_id: str, error_type: str, message: str) -> Dict[str, Any]:
    """
    Create standardized error object.
    
    Args:
        step_id: Step identifier
        error_type: "skill_error" | "validation_error" | "unknown"
        message: Human-readable error message
        
    Returns:
        Error dict
    """
    return {
        "step_id": step_id,
        "type": error_type,
        "message": message
    }
