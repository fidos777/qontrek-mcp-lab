"""
Test KuasaTurbo Prompt Builder
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.services.prompt_builder import build_prompt
from kuasaturbo.services.persona_loader import load_persona
from l8.loader.workflow_loader import load_workflow


def test_build_prompt_structure():
    """Test prompt builder returns correct structure"""
    workflow = load_workflow("content_idea_workflow.v1")
    persona = load_persona("zeyti_bbnu_creator.v1")
    payload = {
        "topic": "AI automation",
        "audience": "SME owners",
        "platform": "tiktok"
    }
    
    result = build_prompt(workflow, persona, payload)
    
    assert "prompt" in result
    assert "system_context" in result
    assert "user_input" in result
    assert isinstance(result["prompt"], str)
    assert len(result["prompt"]) > 0
    print("✓ Prompt structure correct")


def test_prompt_includes_persona_context():
    """Test prompt includes persona information"""
    workflow = load_workflow("content_idea_workflow.v1")
    persona = load_persona("zeyti_bbnu_creator.v1")
    payload = {
        "topic": "AI automation",
        "audience": "SME owners",
        "platform": "tiktok"
    }
    
    result = build_prompt(workflow, persona, payload)
    
    assert "Zeyti" in result["system_context"]
    assert "playful" in result["system_context"].lower() or "creative" in result["system_context"].lower()
    print("✓ Persona context included")


def test_prompt_includes_payload_values():
    """Test prompt includes user input values"""
    workflow = load_workflow("content_idea_workflow.v1")
    persona = load_persona("zeyti_bbnu_creator.v1")
    payload = {
        "topic": "AI automation",
        "audience": "SME owners",
        "platform": "tiktok"
    }
    
    result = build_prompt(workflow, persona, payload)
    
    assert "AI automation" in result["prompt"]
    assert "SME owners" in result["prompt"]
    assert "tiktok" in result["prompt"]
    print("✓ Payload values included")


if __name__ == "__main__":
    test_build_prompt_structure()
    test_prompt_includes_persona_context()
    test_prompt_includes_payload_values()
    print("\n✅ All prompt builder tests passed")
