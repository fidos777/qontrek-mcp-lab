#!/usr/bin/env python3
"""
Social Media Graphics Package Generator Handler
Generates platform-specific social media graphics with copy and hashtags.
"""

import json
import sys
from datetime import datetime
from lib.logger import log

# Platform dimensions mapping
PLATFORM_SPECS = {
    "instagram": [
        {"format": "feed_post", "width": 1080, "height": 1080},
        {"format": "story", "width": 1080, "height": 1920}
    ],
    "facebook": [
        {"format": "feed_post", "width": 1200, "height": 630}
    ],
    "twitter": [
        {"format": "feed_post", "width": 1200, "height": 675}
    ],
    "linkedin": [
        {"format": "feed_post", "width": 1200, "height": 627}
    ],
    "tiktok": [
        {"format": "video_cover", "width": 1080, "height": 1920}
    ]
}

def generate_hashtags(content_type, campaign_goal, message):
    """Generate relevant hashtags based on content."""
    hashtag_map = {
        "product": ["#NewProduct", "#Innovation", "#LaunchDay"],
        "quote": ["#Motivation", "#Inspiration", "#MondayMotivation"],
        "announcement": ["#News", "#Announcement", "#Update"],
        "event": ["#Event", "#JoinUs", "#Register"],
        "educational": ["#LearnMore", "#DidYouKnow", "#Tips"]
    }
    
    base_tags = hashtag_map.get(content_type, ["#Content"])
    
    # Extract keywords from message
    words = message.split()[:3]
    custom_tags = [f"#{word.capitalize()}" for word in words if len(word) > 4]
    
    return (base_tags + custom_tags)[:5]

def generate_copy(platform, message, content_type, campaign_goal):
    """Generate platform-specific copy."""
    # Platform character limits
    limits = {
        "twitter": 280,
        "instagram": 2200,
        "facebook": 500,
        "linkedin": 700,
        "tiktok": 150
    }
    
    limit = limits.get(platform, 500)
    
    # Adjust message based on platform
    if platform == "twitter":
        copy = message[:250]  # Leave room for hashtags
    elif platform == "linkedin":
        copy = f"{message}\n\nWhat are your thoughts?"
    elif platform == "instagram":
        copy = f"{message} 🚀"
    else:
        copy = message
    
    return copy[:limit]

def generate_graphics(campaign_name, platforms, message, content_type, campaign_goal, brand_identity, variations):
    """Generate graphics specifications for each platform."""
    graphics = []
    graphic_id = 1
    
    for platform in platforms:
        specs = PLATFORM_SPECS.get(platform, [{"format": "feed_post", "width": 1200, "height": 630}])
        
        for spec in specs[:1]:  # Use primary format only
            for var in range(variations):
                copy = generate_copy(platform, message, content_type, campaign_goal)
                hashtags = generate_hashtags(content_type, campaign_goal, message)
                
                graphic = {
                    "id": f"{platform}_{spec['format']}_{var+1:03d}",
                    "platform": platform,
                    "format": spec["format"],
                    "dimensions": {
                        "width": spec["width"],
                        "height": spec["height"]
                    },
                    "design_url": f"https://cdn.example.com/{campaign_name.lower().replace(' ', '_')}_{graphic_id}.png",
                    "copy": copy,
                    "hashtags": hashtags
                }
                
                graphics.append(graphic)
                graphic_id += 1
    
    return graphics

def run(params: dict) -> dict:
    """
    Universal handler entrypoint for social graphics generation.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        dict with status, data, errors
    """
    log("info", "graphicgen_socialpack_start",
        campaign_name=params.get("campaign_name"),
        platforms=params.get("platforms"),
        content_type=params.get("content_type"))
    
    errors = []
    
    # Validate required fields
    required = ["campaign_name", "campaign_goal", "message", "brand_identity", "platforms", "content_type"]
    for field in required:
        if field not in params:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        log("error", "graphicgen_socialpack_validation_failed", errors=errors)
        return {
            "status": "error",
            "output": None,
            "errors": errors
        }
    
    # Extract inputs
    campaign_name = params["campaign_name"]
    campaign_goal = params["campaign_goal"]
    message = params["message"]
    brand_identity = params["brand_identity"]
    platforms = params["platforms"]
    content_type = params["content_type"]
    variations = params.get("variations", 3)
    include_copy = params.get("include_copy", True)
    language = params.get("language", "en")
    
    # Generate graphics
    graphics = generate_graphics(
        campaign_name, 
        platforms, 
        message, 
        content_type, 
        campaign_goal,
        brand_identity,
        variations
    )
    
    # Build output
    data = {
        "campaign_name": campaign_name,
        "total_graphics": len(graphics),
        "platforms": platforms,
        "graphics": graphics,
        "brand_colors_used": brand_identity.get("colors", []),
        "fonts_used": brand_identity.get("fonts", [])
    }
    
    log("info", "graphicgen_socialpack_done",
        total_graphics=len(graphics),
        platforms=platforms)
    
    return {
        "status": "success",
        "output": data,
        "errors": []
    }

def main():
    """Main entry point for standalone testing."""
    try:
        input_json = sys.stdin.read()
        input_data = json.loads(input_json)
        
        result = run(input_data)
        
        print(json.dumps(result, indent=2))
        
    except json.JSONDecodeError as e:
        log("error", "graphicgen_socialpack_json_error", error=str(e))
        error_result = {
            "status": "error",
            "output": None,
            "errors": [f"Invalid JSON input: {str(e)}"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)
    except Exception as e:
        log("error", "graphicgen_socialpack_fatal_error", error=str(e))
        error_result = {
            "status": "error",
            "output": None,
            "errors": [f"Processing error: {str(e)}"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
