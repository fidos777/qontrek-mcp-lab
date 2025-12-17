"""
Test KuasaTurbo AI Client (Mock Mode)
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.services.ai_client import generate_output, get_supported_models, validate_model
from kuasaturbo.services.persona_loader import load_persona
from l8.loader.workflow_loader import load_workflow


def test_mock_mode_generates_output():
    """Test mock mode generates output"""
    workflow = load_workflow("content_idea_workflow.v1")
    persona = load_persona("zeyti_bbnu_creator.v1")
    prompt = "Generate content ideas"
    
    result = generate_output(prompt, workflow, persona, model="mock")
    
    assert isinstance(result, dict)
    assert len(result) > 0
    print("✓ Mock mode generates output")


def test_content_idea_output_structure():
    """Test content idea workflow output structure"""
    workflow = load_workflow("content_idea_workflow.v1")
    persona = load_persona("zeyti_bbnu_creator.v1")
    prompt = "Generate content ideas"
    
    result = generate_output(prompt, workflow, persona, model="mock")
    
    assert "ideas" in result
    assert isinstance(result["ideas"], list)
    assert len(result["ideas"]) == 10
    print("✓ Content idea output structure correct")


def test_caption_builder_output_structure():
    """Test caption builder workflow output structure"""
    workflow = load_workflow("caption_builder_workflow.v1")
    persona = load_persona("zeyti_bbnu_creator.v1")
    prompt = "Generate captions"
    
    result = generate_output(prompt, workflow, persona, model="mock")
    
    assert "captions" in result
    assert isinstance(result["captions"], list)
    assert len(result["captions"]) >= 3
    print("✓ Caption builder output structure correct")


def test_supported_models():
    """Test supported models list"""
    models = get_supported_models()
    assert "mock" in models
    assert isinstance(models, list)
    print("✓ Supported models list correct")


def test_validate_model():
    """Test model validation"""
    assert validate_model("mock") == True
    assert validate_model("invalid_model") == False
    print("✓ Model validation working")


if __name__ == "__main__":
    test_mock_mode_generates_output()
    test_content_idea_output_structure()
    test_caption_builder_output_structure()
    test_supported_models()
    test_validate_model()
    print("\n✅ All AI client tests passed")
