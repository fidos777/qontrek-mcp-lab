"""
KuasaTurbo Persona Loader (Simplified)

Loads lightweight persona definitions for KuasaTurbo microservices.
"""

import json
import os
from typing import Dict, Any
from pathlib import Path


# Get project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent


def load_persona(persona_id: str) -> Dict[str, Any]:
    """
    Load simplified persona definition
    
    Args:
        persona_id: Persona identifier (e.g., "izzara_friendly_consultant.v1")
    
    Returns:
        Persona dictionary with simplified schema
    """
    persona_path = PROJECT_ROOT / "l5" / "personas_kuasaturbo" / f"{persona_id}.json"
    
    if not persona_path.exists():
        raise FileNotFoundError(f"Persona not found: {persona_path}")
    
    with open(persona_path, 'r') as f:
        persona = json.load(f)
    
    # Validate required fields
    required_fields = ['persona_id', 'persona_name', 'role', 'traits', 'tone_style', 'language']
    for field in required_fields:
        if field not in persona:
            raise ValueError(f"Persona missing required field: {field}")
    
    return persona


def list_personas() -> list:
    """List all available personas"""
    persona_dir = PROJECT_ROOT / "l5" / "personas_kuasaturbo"
    
    if not persona_dir.exists():
        return []
    
    personas = []
    for filename in os.listdir(persona_dir):
        if filename.endswith('.json'):
            persona_id = filename.replace('.json', '')
            personas.append(persona_id)
    
    return sorted(personas)
