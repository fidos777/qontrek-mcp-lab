import json
import os
import importlib.util
from pathlib import Path
from lib.logger import log

def load_skill_handler(skill_name):
    """Load a skill handler by skill name (e.g., 'generate_slogan')."""
    # Map skill name back to skill directory
    skill_map = {
        "generate_slogan": ("kreator", "brandpack.slogan.v1"),
        "generate_socialpack": ("kreator", "graphicgen.socialpack.v1"),
        "generate_landingpage": ("kreator", "pagegen.landingpage.v1"),
        "normalize_brand_context": ("kreator", "brand_context.normalize.v1"),
        "generate_branding": ("launchkit", "branding.generate.v1"),
        "generate_prd": ("launchkit", "prd.generate.v1"),
        "generate_pricing": ("launchkit", "pricing.generate.v1"),
        "generate_roadmap": ("launchkit", "roadmap.generate.v1"),
        "generate_pitchdeck": ("launchkit", "pitchdeck.generate.v1"),
        "generate_socialpack_launch": ("launchkit", "socialpack.generate.v1")
    }
    
    if skill_name not in skill_map:
        raise Exception(f"Unknown skill: {skill_name}")
    
    domain, skill_dir = skill_map[skill_name]
    handler_path = f"skills/{domain}/{skill_dir}/handler.py"
    
    if not os.path.exists(handler_path):
        raise Exception(f"Handler not found: {handler_path}")
    
    spec = importlib.util.spec_from_file_location("handler", handler_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def resolve_input(input_map: dict, workflow_input: dict, step_outputs: dict):
    """
    Resolves the variables in input_map using:
    - workflow_input (prefixed with "input.")
    - outputs from previous steps (referenced by step ID)
    """
    resolved = {}
    for key, source in input_map.items():
        parts = source.split(".")
        if parts[0] == "input":
            # direct workflow input
            resolved[key] = workflow_input.get(parts[1])
        else:
            # reference from previous step
            step_id = parts[0]
            field = parts[1]
            resolved[key] = step_outputs[step_id]["output"].get(field)
    return resolved

def run_workflow(workflow_id: str, workflow_input: dict):
    """
    Executes a workflow defined in:
    l6/workflows/{workflow_id}/workflow.json
    """
    wf_path = Path(f"l6/workflows/{workflow_id}/workflow.json")
    wf = json.loads(wf_path.read_text())
    
    step_outputs = {}
    errors = []
    
    log("info", "workflow_start", workflow=workflow_id)
    
    for step in wf["steps"]:
        step_id = step["id"]
        skill = step["skill"]
        input_map = step["input_map"]
        
        try:
            log("info", "workflow_step_start", workflow=workflow_id, step=step_id)
            
            arguments = resolve_input(input_map, workflow_input, step_outputs)
            
            # Load skill handler
            handler = load_skill_handler(skill)
            
            # Execute skill
            result = handler.run(arguments)
            
            # Standardize output
            step_outputs[step_id] = {
                "status": result.get("status"),
                "output": result.get("output"),
                "errors": result.get("errors", [])
            }
            
            log("info", "workflow_step_done", workflow=workflow_id, step=step_id)
            
        except Exception as e:
            error_msg = str(e)
            log("error", "workflow_step_error",
                workflow=workflow_id,
                step=step_id,
                error=error_msg)
            errors.append({"step": step_id, "error": error_msg})
            break
    
    status = "success" if len(errors) == 0 else "error"
    log("info", "workflow_complete", workflow=workflow_id, status=status)
    
    return {
        "workflow": workflow_id,
        "status": status,
        "outputs": step_outputs,
        "errors": errors
    }
