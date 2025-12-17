"""
KuasaTurbo Creative Engine - Thumbnail Task

Generates mock thumbnail variations for YouTube/TikTok/Shorts.
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
    Generate thumbnail variations (MOCK MODE)
    
    Args:
        payload: Input data (title, mood, platform, etc.)
        persona: Persona definition
        brand_profile: Optional brand profile
        style_profile: Visual style configuration
        model: Model identifier
        mock_mode: Always True for Phase XIII
    
    Returns:
        Mock thumbnail variations
    """
    title = payload.get("title", "Untitled Video")
    mood = payload.get("mood", "energetic")
    platform = payload.get("platform", "youtube")
    variation_count = payload.get("variation_count", 3)
    
    style_name = style_profile.get("name", "energetic")
    colors = style_profile.get("colors", ["#FE4800", "#262A3B"])
    
    # Generate mock thumbnails
    thumbnails = []
    for i in range(variation_count):
        thumbnails.append({
            "variation_id": f"thumb_{i+1}",
            "headline_text": f"{title[:30]}..." if len(title) > 30 else title,
            "emoji_or_accent": "🔥" if mood == "energetic" else "✨",
            "dominant_colors": colors[:2],
            "layout_hint": ["left_face_right_text", "center_text", "split_diagonal"][i % 3],
            "aspect_ratio": "16:9",
            "platform": platform
        })
    
    return {
        "images": thumbnails,
        "debug": {
            "model": model,
            "style": style_name,
            "mock": mock_mode,
            "persona": persona.get("persona_name", "unknown")
        }
    }
