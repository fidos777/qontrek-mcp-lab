from l6.l6_runner import run_workflow
from mcp_server import call_skill

def dispatch(request_type: str, name: str, arguments: dict):
    """Determines whether to execute a SKILL or WORKFLOW."""
    if request_type == "workflow":
        return run_workflow(name, arguments)
    return call_skill(name, arguments)
