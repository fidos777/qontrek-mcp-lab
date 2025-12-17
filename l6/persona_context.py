#!/usr/bin/env python3
"""
Persona Context Helper
Minimal integration layer between L5 Persona Packs and L6 Engine.
Provides persona context for execution without modifying core engine logic.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from l5.persona_loader import load_persona, list_personas


def get_persona_context(persona_id: str) -> Dict[str, Any]:
    """
    Get persona context ready for L6 execution.
    
    This function loads a persona pack and returns a dictionary
    that can be attached to execution context (e.g., ctx["persona"]).
    
    Args:
        persona_id: Persona ID (e.g., 'izzara_friendly_consultant.v1')
        
    Returns:
        Dictionary with persona context ready for execution
        
    Example:
        >>> ctx = {}
        >>> ctx["persona"] = get_persona_context("izzara_friendly_consultant.v1")
        >>> # Now ctx["persona"] contains all behavioral rules
    """
    persona = load_persona(persona_id)
    
    # Return full persona pack - L6 engine can use what it needs
    return {
        "persona_id": persona_id,
        "identity": persona['identity'],
        "language_profile": persona['language_profile'],
        "tone": persona['tone'],
        "structure": persona['structure'],
        "persuasion": persona['persuasion'],
        "rhetoric_rules": persona['rhetoric_rules'],
        "channels": persona.get('channels', {}),
        "rubric_targets": persona['rubric_targets'],
        "constraints": persona['constraints']
    }


def get_available_personas() -> Dict[str, Dict[str, str]]:
    """
    Get list of available personas with basic info.
    
    Returns:
        Dictionary mapping persona_id to basic info
        
    Example:
        >>> personas = get_available_personas()
        >>> print(personas.keys())
        dict_keys(['izzara_friendly_consultant.v1', ...])
    """
    personas = {}
    
    for persona_id in list_personas():
        try:
            persona = load_persona(persona_id)
            personas[persona_id] = {
                "name": persona['identity']['persona_name'],
                "role": persona['identity']['role'],
                "description": persona['identity']['description'],
                "avatar": persona['identity'].get('avatar', ''),
                "primary_tone": persona['tone']['primary_tone'],
                "primary_language": persona['language_profile']['primary_language']
            }
        except Exception as e:
            print(f"[PersonaContext] Warning: Could not load {persona_id}: {e}")
    
    return personas


def get_persona_for_channel(persona_id: str, channel: str) -> Dict[str, Any]:
    """
    Get persona context with channel-specific adaptations.
    
    Args:
        persona_id: Persona ID
        channel: Channel name ('whatsapp', 'email', 'chat')
        
    Returns:
        Persona context with channel adaptations applied
    """
    context = get_persona_context(persona_id)
    
    # Apply channel-specific overrides if available
    if channel in context['channels']:
        context['channel_config'] = context['channels'][channel]
        context['active_channel'] = channel
    
    return context


def validate_persona_exists(persona_id: str) -> bool:
    """
    Check if a persona exists without loading it.
    
    Args:
        persona_id: Persona ID
        
    Returns:
        True if persona exists, False otherwise
    """
    return persona_id in list_personas()


if __name__ == "__main__":
    # Demo usage
    print("=== Persona Context Helper Demo ===\n")
    
    print("Available Personas:")
    personas = get_available_personas()
    for pid, info in personas.items():
        print(f"  {info['avatar']} {info['name']} - {info['role']}")
    
    print("\n" + "="*50 + "\n")
    
    # Example: Get context for Izzara
    if personas:
        first_persona = list(personas.keys())[0]
        print(f"Loading context for: {first_persona}\n")
        
        context = get_persona_context(first_persona)
        print(f"Persona ID: {context['persona_id']}")
        print(f"Name: {context['identity']['persona_name']}")
        print(f"Tone: {context['tone']['primary_tone']}")
        print(f"Language: {context['language_profile']['primary_language']}")
        print(f"English Ratio: {context['language_profile']['english_ratio']}%")
        print(f"BBNU Ratio: {context['language_profile']['bbnu_ratio']}%")
        print(f"\nRubric Targets:")
        for metric, score in context['rubric_targets'].items():
            print(f"  - {metric}: {score}/5")
