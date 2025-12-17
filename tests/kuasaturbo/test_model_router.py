"""
Test KuasaTurbo Model Router
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from kuasaturbo.services.model_router import (
    get_supported_models,
    validate_model,
    get_model_info,
    resolve_model,
    get_provider
)


def test_get_supported_models():
    """Test listing supported models"""
    models = get_supported_models()
    assert isinstance(models, list)
    assert len(models) == 5
    assert "chatgpt-5.1" in models
    assert "claude-3.7" in models
    assert "gemini-3.0" in models
    assert "groq-llama3.2" in models
    assert "mock" in models
    print("✓ Supported models list correct")


def test_validate_model():
    """Test model validation"""
    assert validate_model("chatgpt-5.1") == True
    assert validate_model("claude-3.7") == True
    assert validate_model("mock") == True
    assert validate_model("invalid-model") == False
    assert validate_model("gpt-4") == False
    print("✓ Model validation working")


def test_get_model_info():
    """Test getting model information"""
    info = get_model_info("chatgpt-5.1")
    assert info is not None
    assert info["provider"] == "openai"
    assert info["mode"] == "text"
    assert "reasoning" in info["supports"]
    
    info = get_model_info("invalid-model")
    assert info is None
    print("✓ Model info retrieval working")


def test_get_provider():
    """Test getting provider for model"""
    assert get_provider("chatgpt-5.1") == "openai"
    assert get_provider("claude-3.7") == "anthropic"
    assert get_provider("gemini-3.0") == "google"
    assert get_provider("groq-llama3.2") == "groq"
    assert get_provider("mock") == "internal"
    assert get_provider("invalid") == "internal"  # Fallback
    print("✓ Provider resolution working")


def test_resolve_model_with_override():
    """Test model resolution with explicit override"""
    workflow = {"id": "test_workflow.v1"}
    persona = {"persona_id": "test_persona.v1"}
    
    # Override should win
    model = resolve_model(workflow, persona, model_override="claude-3.7")
    assert model == "claude-3.7"
    print("✓ Model override priority working")


def test_resolve_model_with_workflow_preference():
    """Test model resolution with workflow preference"""
    workflow = {
        "id": "test_workflow.v1",
        "preferred_model": "gemini-3.0"
    }
    persona = {"persona_id": "test_persona.v1"}
    
    # Workflow preference should be used
    model = resolve_model(workflow, persona)
    assert model == "gemini-3.0"
    print("✓ Workflow preferred_model working")


def test_resolve_model_with_persona_default():
    """Test model resolution with persona default"""
    workflow = {"id": "test_workflow.v1"}
    persona = {
        "persona_id": "test_persona.v1",
        "default_model": "groq-llama3.2"
    }
    
    # Persona default should be used
    model = resolve_model(workflow, persona)
    assert model == "groq-llama3.2"
    print("✓ Persona default_model working")


def test_resolve_model_fallback_to_global():
    """Test model resolution fallback to global default"""
    workflow = {"id": "test_workflow.v1"}
    persona = {"persona_id": "test_persona.v1"}
    
    # Should fall back to global default
    model = resolve_model(workflow, persona)
    assert model == "chatgpt-5.1"  # Global default
    print("✓ Global default fallback working")


def test_resolve_model_priority_order():
    """Test complete priority order"""
    workflow = {
        "id": "test_workflow.v1",
        "preferred_model": "gemini-3.0"
    }
    persona = {
        "persona_id": "test_persona.v1",
        "default_model": "groq-llama3.2"
    }
    
    # Override beats all
    model = resolve_model(workflow, persona, model_override="claude-3.7")
    assert model == "claude-3.7"
    
    # Without override, workflow preference wins
    model = resolve_model(workflow, persona)
    assert model == "gemini-3.0"
    
    # Without workflow preference, persona default wins
    workflow_no_pref = {"id": "test_workflow.v1"}
    model = resolve_model(workflow_no_pref, persona)
    assert model == "groq-llama3.2"
    
    # Without any, global default
    persona_no_default = {"persona_id": "test_persona.v1"}
    model = resolve_model(workflow_no_pref, persona_no_default)
    assert model == "chatgpt-5.1"
    
    print("✓ Complete priority order working")


def test_resolve_model_invalid_override_fallback():
    """Test that invalid override falls through to next priority"""
    workflow = {
        "id": "test_workflow.v1",
        "preferred_model": "gemini-3.0"
    }
    persona = {"persona_id": "test_persona.v1"}
    
    # Invalid override should fall through to workflow preference
    model = resolve_model(workflow, persona, model_override="invalid-model")
    assert model == "gemini-3.0"
    print("✓ Invalid override fallback working")


if __name__ == "__main__":
    test_get_supported_models()
    test_validate_model()
    test_get_model_info()
    test_get_provider()
    test_resolve_model_with_override()
    test_resolve_model_with_workflow_preference()
    test_resolve_model_with_persona_default()
    test_resolve_model_fallback_to_global()
    test_resolve_model_priority_order()
    test_resolve_model_invalid_override_fallback()
    print("\n✅ All model router tests passed")
