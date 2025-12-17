#!/usr/bin/env python3
"""
Persona Pack Loader
Loads and validates L5 Persona Pack definitions.
Personas define HOW agents speak/behave, NOT WHAT they do.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Tuple, List
import jsonschema


# Paths
PROJECT_ROOT = Path(__file__).parent.parent
PERSONAS_DIR = PROJECT_ROOT / "l5" / "personas"
SCHEMA_PATH = PROJECT_ROOT / "l5" / "schema" / "persona_pack_schema.json"


def load_schema() -> Dict[str, Any]:
    """
    Load the persona pack JSON schema.
    
    Returns:
        Schema dictionary
    """
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)


def validate_persona(persona_dict: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate a persona pack against the schema.
    
    Args:
        persona_dict: Persona pack data
        
    Returns:
        (is_valid: bool, errors: List[str])
    """
    schema = load_schema()
    errors = []
    
    try:
        jsonschema.validate(persona_dict, schema)
        
        # Additional validation: Check for forbidden keys (vertical/business logic)
        # Note: Check top-level and nested keys, but exclude rubric_targets.compliance
        forbidden_keys = [
            'vertical', 'verticals', 'industry', 'industries',
            'workflows', 'workflow', 'entities', 'entity',
            'skills', 'skill', 'governance', 'policies',
            'required_documents', 'pricing',
            'products', 'services'
        ]
        
        # Check top-level keys
        for key in forbidden_keys:
            if key in persona_dict:
                errors.append(
                    f"Forbidden key detected: '{key}'. "
                    f"Persona packs must NOT contain vertical/business logic. "
                    f"These belong in L4 Vertical Packs."
                )
        
        # Validate rubric_targets are in range 1-5
        rubric = persona_dict.get('rubric_targets', {})
        for metric, score in rubric.items():
            if not (1 <= score <= 5):
                errors.append(
                    f"Rubric target '{metric}' has invalid score {score}. "
                    f"Must be between 1 and 5."
                )
        
        # Validate language ratios sum to reasonable total
        lang_profile = persona_dict.get('language_profile', {})
        english_ratio = lang_profile.get('english_ratio', 0)
        bbnu_ratio = lang_profile.get('bbnu_ratio', 0)
        
        if english_ratio + bbnu_ratio > 100:
            errors.append(
                f"Language ratios exceed 100%: "
                f"english_ratio={english_ratio}, bbnu_ratio={bbnu_ratio}"
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


def load_persona(persona_id: str) -> Dict[str, Any]:
    """
    Load a persona pack by persona ID.
    
    Args:
        persona_id: Persona ID (e.g., 'izzara_friendly_consultant.v1')
        
    Returns:
        Persona pack dictionary
        
    Raises:
        FileNotFoundError: If persona pack not found
        ValueError: If persona pack is invalid
    """
    persona_path = PERSONAS_DIR / f"{persona_id}.yaml"
    
    if not persona_path.exists():
        raise FileNotFoundError(
            f"Persona pack not found: {persona_id}. "
            f"Expected at: {persona_path}"
        )
    
    # Load YAML
    with open(persona_path, 'r') as f:
        persona_dict = yaml.safe_load(f)
    
    # Validate
    is_valid, errors = validate_persona(persona_dict)
    
    if not is_valid:
        error_msg = f"Invalid persona pack '{persona_id}':\n"
        error_msg += "\n".join(f"  - {err}" for err in errors)
        raise ValueError(error_msg)
    
    print(f"[PersonaLoader] Loaded persona: {persona_id}")
    print(f"[PersonaLoader] Name: {persona_dict['identity']['persona_name']}")
    print(f"[PersonaLoader] Role: {persona_dict['identity']['role']}")
    print(f"[PersonaLoader] Tone: {persona_dict['tone']['primary_tone']}")
    print(f"[PersonaLoader] Language: {persona_dict['language_profile']['primary_language']}")
    
    return persona_dict


def list_personas() -> List[str]:
    """
    List all available persona packs.
    
    Returns:
        List of persona IDs
    """
    if not PERSONAS_DIR.exists():
        return []
    
    personas = []
    for item in PERSONAS_DIR.iterdir():
        if item.is_file() and item.suffix == '.yaml':
            # Remove .yaml extension
            persona_id = item.stem
            personas.append(persona_id)
    
    return sorted(personas)


def get_persona_metadata(persona_id: str) -> Dict[str, Any]:
    """
    Get basic metadata about a persona pack without full validation.
    
    Args:
        persona_id: Persona ID
        
    Returns:
        Dictionary with identity, language_profile, and tone
    """
    persona = load_persona(persona_id)
    return {
        "persona_id": persona_id,
        "identity": persona['identity'],
        "language_profile": persona['language_profile'],
        "tone": persona['tone'],
        "rubric_targets": persona['rubric_targets']
    }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 l5/persona_loader.py <persona_id>")
        print("\nAvailable personas:")
        for p in list_personas():
            try:
                meta = get_persona_metadata(p)
                print(f"  - {p}: {meta['identity']['persona_name']} ({meta['identity']['role']})")
            except:
                print(f"  - {p}: (error loading)")
        sys.exit(1)
    
    persona_id = sys.argv[1]
    
    try:
        persona = load_persona(persona_id)
        print("\n=== Persona Pack Loaded Successfully ===")
        print(json.dumps(persona, indent=2))
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
