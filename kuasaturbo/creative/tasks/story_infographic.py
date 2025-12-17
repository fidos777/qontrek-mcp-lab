"""
KuasaTurbo Creative Engine - Story Infographic Task

Generates mock single-image infographics.
"""

from typing import Dict, Any


def run(
    payload: dict,
    persona: dict,
    brand_profile: dict | None,
    style_profile: dict,
    model: str,
    mock_mode: bool = True
) -> Dict[str, Any]:
    """
    Generate story infographic (MOCK MODE)
    
    Args:
        payload: Input data (topic, style, etc.)
        persona: Persona definition
        brand_profile: Optional brand profile
        style_profile: Visual style configuration
        model: Model identifier
        mock_mode: Always True for Phase XIII
    
    Returns:
        Mock infographic structure
    """
    topic = payload.get("topic", "Process Overview")
    style = payload.get("style", "simple-clean")
    max_sections = payload.get("max_sections", 5)
    
    style_name = style_profile.get("name", "simple_clean")
    colors = style_profile.get("colors", ["#FFFFFF", "#145FC8"])
    
    # Generate mock sections
    sections = [
        {
            "title": "Step 1: Getting Started",
            "bullets": [
                "Gather required documents",
                "Complete initial form",
                "Submit application"
            ]
        },
        {
            "title": "Step 2: Review Process",
            "bullets": [
                "Application reviewed",
                "Verification checks",
                "Approval decision"
            ]
        },
        {
            "title": "Step 3: Completion",
            "bullets": [
                "Receive confirmation",
                "Access your account",
                "Start using service"
            ]
        }
    ]
    
    return {
        "image": {
            "id": "infographic_1",
            "title": topic,
            "sections": sections[:max_sections],
            "layout_type": "timeline",
            "icon_suggestions": ["document", "checkmark", "star"],
            "call_to_action_block": {
                "text": f"Learn more about {topic}",
                "button": "Get Started"
            },
            "colors": colors
        },
        "debug": {
            "model": model,
            "style": style_name,
            "mock": mock_mode,
            "topic": topic
        }
    }
