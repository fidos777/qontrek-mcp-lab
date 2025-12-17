#!/usr/bin/env python3
"""
Workflow Runner V2 - Minimal Workflow Execution Layer
Orchestrates multi-step workflows using dispatcher_mvp.
NO governance, NO reflexion, NO async - just reliable execution.
"""

import sys
import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from l6.workflow_loader import load_workflow, validate_workflow
from l6.step_executor import execute_step, check_dependencies
from l6.envelope import create_workflow_envelope, determine_status, create_error
from models.brand_context_normalizer import normalize, to_legacy_format


def execute_workflow(workflow_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a workflow by ID.
    
    Args:
        workflow_id: Workflow identifier (e.g., "kuasaturbo.launchkit.v1")
        payload: Input payload for the workflow
        
    Returns:
        Workflow envelope:
        {
            "workflow_id": str,
            "status": "success" | "partial" | "failed",
            "completed_steps": [str],
            "pending_steps": [str],
            "failed_steps": [str],
            "outputs": {step_id: output},
            "errors": [error],
            "trace_id": str,
            "started_at": str,
            "finished_at": str
        }
    """
    started_at = datetime.now().isoformat() + "Z"
    
    # Initialize tracking
    completed_steps = []
    pending_steps = []
    failed_steps = []
    outputs = {}
    errors = []
    
    try:
        # Load workflow definition
        workflow = load_workflow(workflow_id)
        
        # Validate workflow
        is_valid, validation_errors = validate_workflow(workflow)
        if not is_valid:
            return create_workflow_envelope(
                workflow_id=workflow_id,
                status="failed",
                completed_steps=[],
                pending_steps=[],
                failed_steps=[],
                outputs={},
                errors=[create_error("workflow", "validation_error", f"Invalid workflow: {', '.join(validation_errors)}")],
                started_at=started_at
            )
        
        # PHASE C: Normalize brand context
        normalized_result = normalize(payload)
        
        # Check if normalization failed
        if isinstance(normalized_result, dict) and normalized_result.get("status") == "error":
            return create_workflow_envelope(
                workflow_id=workflow_id,
                status="failed",
                completed_steps=[],
                pending_steps=[],
                failed_steps=["brand_context_normalization"],
                outputs={},
                errors=[create_error(
                    "brand_context_normalization",
                    normalized_result["error"]["type"],
                    normalized_result["error"]["message"]
                )],
                started_at=started_at
            )
        
        # Convert normalized context back to legacy format for skills
        # This maintains backward compatibility with existing skills
        normalized_payload = to_legacy_format(normalized_result)
        
        steps = workflow.get("steps", [])
        total_steps = len(steps)
        
        # Initialize pending steps
        pending_steps = [step["id"] for step in steps]
        
        # Execute steps in order
        for step in steps:
            step_id = step.get("id")
            
            # Check dependencies
            deps_satisfied, missing_deps = check_dependencies(step, completed_steps)
            
            if not deps_satisfied:
                # Dependencies not satisfied, mark as failed
                failed_steps.append(step_id)
                pending_steps.remove(step_id)
                errors.append(create_error(
                    step_id,
                    "dependency_error",
                    f"Missing dependencies: {', '.join(missing_deps)}"
                ))
                continue
            
            # Execute step with normalized payload
            result = execute_step(step, normalized_payload, outputs)
            
            # Process result
            if result.get("status") == "success":
                # Step succeeded
                completed_steps.append(step_id)
                pending_steps.remove(step_id)
                outputs[step_id] = result.get("output")
            
            else:
                # Step failed
                failed_steps.append(step_id)
                pending_steps.remove(step_id)
                
                # Extract error
                error = result.get("error", {})
                if isinstance(error, dict):
                    error_type = error.get("type", "unknown")
                    error_message = error.get("message", "Unknown error")
                    
                    # Check for errors array (from skill handler)
                    if "errors" in error and isinstance(error["errors"], list):
                        error_message = "; ".join(error["errors"])
                else:
                    error_type = "unknown"
                    error_message = str(error)
                
                errors.append(create_error(step_id, error_type, error_message))
                
                # Stop execution on first failure (fail-fast for Phase B)
                break
        
        # Determine final status
        status = determine_status(completed_steps, failed_steps, total_steps)
        
        # Create envelope
        return create_workflow_envelope(
            workflow_id=workflow_id,
            status=status,
            completed_steps=completed_steps,
            pending_steps=pending_steps,
            failed_steps=failed_steps,
            outputs=outputs,
            errors=errors,
            started_at=started_at
        )
        
    except FileNotFoundError as e:
        # Workflow not found
        return create_workflow_envelope(
            workflow_id=workflow_id,
            status="failed",
            completed_steps=[],
            pending_steps=[],
            failed_steps=[],
            outputs={},
            errors=[create_error("workflow", "unknown_workflow", str(e))],
            started_at=started_at
        )
    
    except Exception as e:
        # Unexpected error
        return create_workflow_envelope(
            workflow_id=workflow_id,
            status="failed",
            completed_steps=completed_steps,
            pending_steps=pending_steps,
            failed_steps=failed_steps,
            outputs=outputs,
            errors=[create_error("workflow", "execution_error", str(e))],
            started_at=started_at
        )


# CLI interface for testing
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 l6/runner_v2.py <workflow_id> [payload_json]")
        print("\nExample:")
        print("  cat payload.json | python3 l6/runner_v2.py kuasaturbo.launchkit.v1")
        sys.exit(1)
    
    workflow_id = sys.argv[1]
    
    # Parse payload from stdin or command line
    if len(sys.argv) > 2:
        payload = json.loads(sys.argv[2])
    else:
        payload_str = sys.stdin.read()
        payload = json.loads(payload_str) if payload_str.strip() else {}
    
    # Execute workflow
    result = execute_workflow(workflow_id, payload)
    
    # Output
    print(json.dumps(result, indent=2))
    
    # Exit code
    sys.exit(0 if result["status"] == "success" else 1)
