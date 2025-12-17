#!/usr/bin/env python3
"""
KuasaTurbo Widget Loader (L3)
Loads and validates lightweight widgets - NO GOVERNANCE
"""

import json
import os
import yaml
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

def get_schema_path() -> Path:
    """Get path to widget schema."""
    return Path(__file__).parent.parent / "schema" / "widget_schema.json"

def get_widgets_dir() -> Path:
    """Get path to widgets directory."""
    return Path(__file__).parent.parent / "widgets"

def load_schema() -> dict:
    """Load widget schema."""
    schema_path = get_schema_path()
    if not schema_path.exists():
        raise FileNotFoundError(f"Widget schema not found: {schema_path}")
    
    with open(schema_path, 'r') as f:
        return json.load(f)

def list_widgets() -> List[str]:
    """
    Return a list of widget_ids from l3/widgets/
    
    Returns:
        List of widget IDs (without .yaml extension)
    """
    widgets_dir = get_widgets_dir()
    if not widgets_dir.exists():
        print(f"[WidgetLoader] Widgets directory not found: {widgets_dir}")
        return []
    
    widget_files = list(widgets_dir.glob("*.yaml"))
    widget_ids = [f.stem for f in widget_files]
    
    print(f"[WidgetLoader] Found {len(widget_ids)} widgets")
    return sorted(widget_ids)

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

def validate_widget(widget: dict) -> Tuple[bool, List[str]]:
    """
    Validate widget dict against schema and forbidden keys.
    
    Args:
        widget: Widget dictionary to validate
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Check for forbidden governance keys
    forbidden = check_forbidden_keys(widget)
    if forbidden:
        errors.append(f"Forbidden governance keys found: {', '.join(forbidden)}")
        return False, errors
    
    # Validate required fields
    required_fields = ["widget_id", "widget_name", "vertical", "description", "fields", "workflow"]
    for field in required_fields:
        if field not in widget:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Validate fields array
    if "fields" in widget:
        if not isinstance(widget["fields"], list):
            errors.append("'fields' must be an array")
        elif len(widget["fields"]) == 0:
            errors.append("'fields' array cannot be empty")
        else:
            for i, field in enumerate(widget["fields"]):
                if not isinstance(field, dict):
                    errors.append(f"fields[{i}] must be an object")
                    continue
                
                field_required = ["id", "label", "type", "required"]
                for req in field_required:
                    if req not in field:
                        errors.append(f"fields[{i}] missing required property: {req}")
    
    # Validate workflow
    if "workflow" in widget:
        if not isinstance(widget["workflow"], dict):
            errors.append("'workflow' must be an object")
        else:
            if "trigger" not in widget["workflow"]:
                errors.append("workflow.trigger is required")
            if "persona" not in widget["workflow"]:
                errors.append("workflow.persona is required")
    
    # Check for additional properties at root level
    allowed_root_keys = [
        "widget_id", "widget_name", "vertical", "description",
        "fields", "validations", "workflow", "presentation", "metadata"
    ]
    for key in widget.keys():
        if key not in allowed_root_keys:
            errors.append(f"Additional property not allowed at root: {key}")
    
    if errors:
        return False, errors
    
    return True, []

def load_widget(widget_id: str) -> dict:
    """
    Load and validate a widget by widget_id.
    
    Args:
        widget_id: Widget identifier (e.g., "content_idea_widget.v1")
        
    Returns:
        Validated widget dictionary
        
    Raises:
        FileNotFoundError: If widget file not found
        ValueError: If widget validation fails
    """
    widgets_dir = get_widgets_dir()
    widget_path = widgets_dir / f"{widget_id}.yaml"
    
    if not widget_path.exists():
        raise FileNotFoundError(f"Widget not found: {widget_id}")
    
    print(f"[WidgetLoader] Loading widget: {widget_id}")
    
    # Load YAML
    with open(widget_path, 'r') as f:
        widget = yaml.safe_load(f)
    
    # Validate
    is_valid, errors = validate_widget(widget)
    
    if not is_valid:
        error_msg = f"Widget validation failed for {widget_id}:\n" + "\n".join(f"  - {e}" for e in errors)
        print(f"[WidgetLoader] ERROR: {error_msg}")
        raise ValueError(error_msg)
    
    # Log success
    print(f"[WidgetLoader] Widget ID: {widget.get('widget_id')}")
    print(f"[WidgetLoader] Name: {widget.get('widget_name')}")
    print(f"[WidgetLoader] Vertical: {widget.get('vertical')}")
    print(f"[WidgetLoader] Fields: {len(widget.get('fields', []))}")
    print(f"[WidgetLoader] Workflow: {widget.get('workflow', {}).get('trigger')}")
    print(f"[WidgetLoader] Persona: {widget.get('workflow', {}).get('persona')}")
    
    return widget

def get_widget_info(widget_id: str) -> dict:
    """
    Get basic widget information without full validation.
    
    Args:
        widget_id: Widget identifier
        
    Returns:
        Dictionary with basic widget info
    """
    try:
        widget = load_widget(widget_id)
        return {
            "widget_id": widget.get("widget_id"),
            "widget_name": widget.get("widget_name"),
            "vertical": widget.get("vertical"),
            "description": widget.get("description"),
            "field_count": len(widget.get("fields", [])),
            "workflow_trigger": widget.get("workflow", {}).get("trigger"),
            "persona": widget.get("workflow", {}).get("persona")
        }
    except Exception as e:
        return {
            "widget_id": widget_id,
            "error": str(e)
        }

if __name__ == "__main__":
    # Test loader
    print("=== Widget Loader Test ===\n")
    
    widgets = list_widgets()
    print(f"\nFound {len(widgets)} widgets:")
    for w in widgets:
        print(f"  - {w}")
    
    if widgets:
        print(f"\nTesting load of first widget: {widgets[0]}")
        try:
            widget = load_widget(widgets[0])
            print(f"✓ Successfully loaded {widgets[0]}")
        except Exception as e:
            print(f"✗ Failed to load {widgets[0]}: {e}")
