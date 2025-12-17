#!/usr/bin/env python3
"""
Vertical Pack Loader
Loads and validates L4 Vertical Pack definitions.
NO personality, NO behavior, NO business logic - structure only.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Tuple, List
import jsonschema


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
VERTICALS_DIR = PROJECT_ROOT / "verticals"
SCHEMA_PATH = VERTICALS_DIR / "spec" / "vertical_pack_schema.json"


def load_schema() -> Dict[str, Any]:
    """
    Load the vertical pack JSON schema.
    
    Returns:
        Schema dictionary
    """
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)


def validate_vertical(vertical_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a vertical pack against the schema.
    
    Args:
        vertical_dict: Vertical pack data
        
    Returns:
        (is_valid: bool, errors: List[str])
    """
    schema = load_schema()
    errors = []
    
    try:
        jsonschema.validate(vertical_dict, schema)
        
        # Additional validation: Check for behavioral skills (forbidden)
        forbidden_skill_patterns = [
            'persuasion', 'tone', 'emotional', 'personality',
            'behavior', 'style', 'voice', 'sentiment'
        ]
        
        skills = vertical_dict.get('skills', {})
        for skill_name, skill_id in skills.items():
            for pattern in forbidden_skill_patterns:
                if pattern in skill_name.lower() or pattern in skill_id.lower():
                    errors.append(
                        f"Behavioral skill detected: '{skill_name}' -> '{skill_id}'. "
                        f"Vertical packs must only contain functional skills. "
                        f"Behavioral skills belong in L5 Persona Packs."
                    )
        
        # Additional validation: Check widgets for logic (forbidden)
        widgets = vertical_dict.get('widgets', {})
        for widget_name, widget_def in widgets.items():
            # Check for forbidden properties
            forbidden_widget_props = ['logic', 'behavior', 'decision', 'chain', 'rules']
            for prop in forbidden_widget_props:
                if prop in widget_def:
                    errors.append(
                        f"Widget '{widget_name}' contains forbidden property '{prop}'. "
                        f"Widgets must be declarative UI only."
                    )
        
        # Additional validation: Check compliance for governance (forbidden)
        compliance = vertical_dict.get('compliance', {})
        if 'governance' in compliance or 'policies' in compliance:
            errors.append(
                "Compliance block contains governance/policies. "
                "Governance belongs in L7, not L4 vertical packs."
            )
        
        return (len(errors) == 0, errors)
        
    except jsonschema.ValidationError as e:
        errors.append(f"Schema validation error: {e.message}")
        if e.path:
            errors.append(f"  Path: {' -> '.join(str(p) for p in e.path)}")
        return (False, errors)
    except Exception as e:
        errors.append(f"Validation error: {str(e)}")
        return (False, errors)


def load_vertical(industry_code: str) -> Dict[str, Any]:
    """
    Load a vertical pack by industry code.
    
    Args:
        industry_code: Industry code (e.g., 'automotive', 'solar')
        
    Returns:
        Vertical pack dictionary
        
    Raises:
        FileNotFoundError: If vertical pack not found
        ValueError: If vertical pack is invalid
    """
    vertical_path = VERTICALS_DIR / industry_code / "vertical.yaml"
    
    if not vertical_path.exists():
        raise FileNotFoundError(
            f"Vertical pack not found: {industry_code}. "
            f"Expected at: {vertical_path}"
        )
    
    # Load YAML
    with open(vertical_path, 'r') as f:
        vertical_dict = yaml.safe_load(f)
    
    # Validate
    is_valid, errors = validate_vertical(vertical_dict)
    
    if not is_valid:
        error_msg = f"Invalid vertical pack '{industry_code}':\n"
        error_msg += "\n".join(f"  - {err}" for err in errors)
        raise ValueError(error_msg)
    
    print(f"[VerticalLoader] Loaded vertical: {industry_code}")
    print(f"[VerticalLoader] Industry: {vertical_dict['industry_identity']['industry_name']}")
    print(f"[VerticalLoader] Entities: {len(vertical_dict.get('entities', {}))}")
    print(f"[VerticalLoader] Skills: {len(vertical_dict.get('skills', {}))}")
    print(f"[VerticalLoader] Workflows: {len(vertical_dict.get('workflows', {}))}")
    
    return vertical_dict


def list_verticals() -> List[str]:
    """
    List all available vertical packs.
    
    Returns:
        List of industry codes
    """
    if not VERTICALS_DIR.exists():
        return []
    
    verticals = []
    for item in VERTICALS_DIR.iterdir():
        if item.is_dir() and item.name != 'spec':
            vertical_file = item / "vertical.yaml"
            if vertical_file.exists():
                verticals.append(item.name)
    
    return sorted(verticals)


def get_vertical_info(industry_code: str) -> Dict[str, Any]:
    """
    Get basic info about a vertical pack without full validation.
    
    Args:
        industry_code: Industry code
        
    Returns:
        Dictionary with industry_identity block
    """
    vertical = load_vertical(industry_code)
    return {
        "industry_code": industry_code,
        "industry_name": vertical['industry_identity']['industry_name'],
        "description": vertical['industry_identity']['description'],
        "icon": vertical['industry_identity'].get('icon', ''),
        "entity_count": len(vertical.get('entities', {})),
        "skill_count": len(vertical.get('skills', {})),
        "workflow_count": len(vertical.get('workflows', {})),
        "widget_count": len(vertical.get('widgets', {})),
        "status_count": len(vertical.get('statuses', []))
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 l6/vertical_loader.py <industry_code>")
        print("\nAvailable verticals:")
        for v in list_verticals():
            info = get_vertical_info(v)
            print(f"  - {v}: {info['industry_name']}")
        sys.exit(1)
    
    industry_code = sys.argv[1]
    
    try:
        vertical = load_vertical(industry_code)
        print("\n=== Vertical Pack Loaded Successfully ===")
        print(json.dumps(vertical, indent=2))
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
