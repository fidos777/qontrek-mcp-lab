#!/usr/bin/env python3
"""
L6 Dispatcher MVP - Minimal Skill Execution Layer
Loads and executes LaunchKit skills with stable import pattern.
NO governance, NO reflexion, NO async - just reliable execution.
"""

import sys
import importlib.util
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Hardcoded skill registry (MVP - no auto-scan)
# Maps skill_id to handler file path
SKILL_REGISTRY = {
    "launchkit.branding.generate.v1": "skills/launchkit/branding.generate.v1/handler.py",
    "launchkit.prd.generate.v1": "skills/launchkit/prd.generate.v1/handler.py",
    "launchkit.pricing.generate.v1": "skills/launchkit/pricing.generate.v1/handler.py",
    "launchkit.roadmap.generate.v1": "skills/launchkit/roadmap.generate.v1/handler.py",
    "launchkit.pitchdeck.generate.v1": "skills/launchkit/pitchdeck.generate.v1/handler.py",
    "launchkit.socialpack.generate.v1": "skills/launchkit/socialpack.generate.v1/handler.py"
}


def load_skill(skill_id: str):
    """
    Dynamically import a skill handler module using file path.
    
    Args:
        skill_id: Skill identifier (e.g., "launchkit.branding.generate.v1")
        
    Returns:
        Module with run() or execute() function
        
    Raises:
        ValueError: If skill_id not in registry
        ImportError: If module cannot be imported
    """
    if skill_id not in SKILL_REGISTRY:
        raise ValueError(f"Unknown skill: {skill_id}. Available: {list(SKILL_REGISTRY.keys())}")
    
    handler_path = SKILL_REGISTRY[skill_id]
    full_path = PROJECT_ROOT / handler_path
    
    if not full_path.exists():
        raise ImportError(f"Handler file not found: {full_path}")
    
    try:
        # Load module from file path (handles dots in folder names)
        spec = importlib.util.spec_from_file_location(
            f"skill_{skill_id.replace('.', '_')}", 
            full_path
        )
        module = importlib.util.module_from_spec(spec)
        
        # Add to sys.modules to enable relative imports within the handler
        sys.modules[spec.name] = module
        
        # Execute the module
        spec.loader.exec_module(module)
        
        return module
    except Exception as e:
        raise ImportError(f"Failed to load {handler_path}: {str(e)}")


def execute_skill(skill_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a skill with given payload.
    
    Args:
        skill_id: Skill identifier
        payload: Input parameters for the skill
        
    Returns:
        Envelope:
        {
            "status": "success" | "failed",
            "output": {...} or None,
            "error": {...} or None
        }
    """
    try:
        # Load skill module
        module = load_skill(skill_id)
        
        # Find execution function (try run() first, then execute())
        if hasattr(module, 'run'):
            execute_fn = module.run
        elif hasattr(module, 'execute'):
            execute_fn = module.execute
        else:
            return {
                "status": "failed",
                "output": None,
                "error": {
                    "type": "missing_function",
                    "message": f"Module {skill_id} has no run() or execute() function"
                }
            }
        
        # Execute skill
        result = execute_fn(payload)
        
        # Normalize result to envelope format
        if isinstance(result, dict):
            # If result already has status/output/errors, use it
            if "status" in result:
                return {
                    "status": result.get("status"),
                    "output": result.get("output"),
                    "error": {"errors": result.get("errors", [])} if result.get("errors") else None
                }
            else:
                # Wrap raw result
                return {
                    "status": "success",
                    "output": result,
                    "error": None
                }
        else:
            return {
                "status": "success",
                "output": result,
                "error": None
            }
            
    except ValueError as e:
        # Unknown skill
        return {
            "status": "failed",
            "output": None,
            "error": {
                "type": "unknown_skill",
                "message": str(e)
            }
        }
    except ImportError as e:
        # Import failed
        return {
            "status": "failed",
            "output": None,
            "error": {
                "type": "import_error",
                "message": str(e)
            }
        }
    except Exception as e:
        # Execution error
        return {
            "status": "failed",
            "output": None,
            "error": {
                "type": "execution_error",
                "message": str(e),
                "exception": type(e).__name__
            }
        }


def list_skills() -> list:
    """Return list of available skill IDs."""
    return list(SKILL_REGISTRY.keys())


def get_skill_info(skill_id: str) -> Optional[Dict[str, Any]]:
    """
    Get basic info about a skill.
    
    Args:
        skill_id: Skill identifier
        
    Returns:
        Dict with skill info or None if not found
    """
    if skill_id not in SKILL_REGISTRY:
        return None
    
    return {
        "skill_id": skill_id,
        "module_path": SKILL_REGISTRY[skill_id],
        "available": True
    }


# CLI interface for testing
if __name__ == "__main__":
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python3 l6/dispatcher_mvp.py <skill_id> [payload_json]")
        print("\nAvailable skills:")
        for skill in list_skills():
            print(f"  - {skill}")
        sys.exit(1)
    
    skill_id = sys.argv[1]
    
    # Parse payload from stdin or command line
    if len(sys.argv) > 2:
        payload = json.loads(sys.argv[2])
    else:
        payload_str = sys.stdin.read()
        payload = json.loads(payload_str) if payload_str.strip() else {}
    
    # Execute
    result = execute_skill(skill_id, payload)
    
    # Output
    print(json.dumps(result, indent=2))
    
    # Exit code
    sys.exit(0 if result["status"] == "success" else 1)
