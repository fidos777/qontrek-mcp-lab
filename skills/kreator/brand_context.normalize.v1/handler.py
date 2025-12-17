#!/usr/bin/env python3
"""
Brand Context Normalizer Handler
Transforms creative outputs into structured business context.
"""

import json
import sys
from datetime import datetime
from lib.logger import log


def extract_hero_content(landing_page_output):
    """Extract hero section from landing page."""
    if not landing_page_output:
        return None
    
    sections = landing_page_output.get("output", {}).get("sections", [])
    for section in sections:
        if section.get("section_type") == "hero":
            return section.get("content", {})
    return None


def extract_benefits(landing_page_output):
    """Extract benefits from landing page."""
    if not landing_page_output:
        return []
    
    sections = landing_page_output.get("output", {}).get("sections", [])
    for section in sections:
        if section.get("section_type") == "benefits_grid":
            return section.get("content", {}).get("benefits", [])
    return []


def extract_themes(slogan_output):
    """Extract key themes from slogan analysis."""
    if not slogan_output:
        return []
    
    brand_analysis = slogan_output.get("output", {}).get("brand_analysis", {})
    return brand_analysis.get("key_themes", [])


def extract_top_slogan(slogan_output):
    """Extract the top-rated slogan."""
    if not slogan_output:
        return None
    
    slogans = slogan_output.get("output", {}).get("slogans", [])
    if not slogans:
        return None
    
    # Return highest memorability score
    return max(slogans, key=lambda s: s.get("memorability_score", 0))


def extract_social_messaging(social_pack_output):
    """Extract messaging patterns from social pack."""
    if not social_pack_output:
        return []
    
    graphics = social_pack_output.get("output", {}).get("graphics", [])
    return [g.get("copy", "") for g in graphics if g.get("copy")]


def infer_mission(hero_content, themes, brand_values):
    """Infer mission statement from hero and themes."""
    if not hero_content:
        return "Empower users through innovative solutions."
    
    headline = hero_content.get("headline", "")
    subheadline = hero_content.get("subheadline", "")
    
    # Extract action verbs and outcomes
    mission_parts = []
    
    if themes:
        primary_theme = themes[0] if themes else "innovation"
        mission_parts.append(f"deliver {primary_theme}")
    
    if brand_values:
        value = brand_values[0] if brand_values else "excellence"
        mission_parts.append(f"through {value}")
    
    # Construct mission
    if headline and subheadline:
        mission = f"To {' and '.join(mission_parts)}, helping users {headline.lower()}."
    else:
        mission = f"To {' and '.join(mission_parts)} for our customers."
    
    return mission


def derive_positioning(slogan, benefits, industry, target_audience):
    """Derive positioning statement from slogan and benefits."""
    if not slogan:
        return "A leading solution in the market."
    
    slogan_text = slogan.get("text", "")
    tone = slogan.get("tone", "professional")
    
    # Extract primary benefit
    primary_benefit = "innovative solutions"
    if benefits:
        primary_benefit = benefits[0].get("title", "innovative solutions").lower()
    
    positioning = (
        f"For {target_audience}, we are the {tone} {industry} solution "
        f"that delivers {primary_benefit}. {slogan_text}."
    )
    
    return positioning


def extract_value_proposition(benefits, hero_content):
    """Extract value proposition from benefits and hero."""
    if not benefits:
        return "Innovative solutions that drive results."
    
    # Combine top benefits
    benefit_titles = [b.get("title", "") for b in benefits[:3]]
    
    if hero_content:
        headline = hero_content.get("headline", "")
        return f"{headline}. {', '.join(benefit_titles)}."
    
    return f"Delivering {', '.join(benefit_titles).lower()}."


def reconstruct_icp(target_audience, tone, social_messages):
    """Reconstruct Ideal Customer Profile from signals."""
    # Parse target audience
    demographics = target_audience
    
    # Infer psychographics from tone
    psychographics = {
        "professional": ["results-oriented", "efficiency-focused", "data-driven"],
        "playful": ["creative", "adventurous", "social"],
        "inspirational": ["ambitious", "growth-minded", "visionary"],
        "bold": ["risk-takers", "innovators", "disruptors"],
        "minimalist": ["simplicity-seekers", "focused", "intentional"]
    }
    
    traits = psychographics.get(tone, ["goal-oriented", "quality-conscious"])
    
    # Infer pain points from social messages
    pain_points = []
    if any("time" in msg.lower() or "hours" in msg.lower() for msg in social_messages):
        pain_points.append("Time constraints and inefficiency")
    if any("automat" in msg.lower() for msg in social_messages):
        pain_points.append("Manual repetitive tasks")
    if any("integrat" in msg.lower() for msg in social_messages):
        pain_points.append("Disconnected tools and workflows")
    
    if not pain_points:
        pain_points = ["Seeking better solutions", "Looking for innovation"]
    
    return {
        "demographics": demographics,
        "psychographics": traits,
        "pain_points": pain_points,
        "goals": ["Improve efficiency", "Achieve better results", "Save time and resources"]
    }


def identify_brand_themes(themes, benefits, social_messages):
    """Identify unified brand themes across outputs."""
    all_themes = set(themes) if themes else set()
    
    # Extract themes from benefits
    for benefit in benefits:
        title = benefit.get("title", "").lower()
        if "time" in title or "save" in title:
            all_themes.add("efficiency")
        if "smart" in title or "ai" in title or "automat" in title:
            all_themes.add("innovation")
        if "seamless" in title or "integrat" in title:
            all_themes.add("simplicity")
        if "focus" in title or "matter" in title:
            all_themes.add("productivity")
    
    # Extract from social messages
    for msg in social_messages:
        msg_lower = msg.lower()
        if "ai" in msg_lower or "smart" in msg_lower:
            all_themes.add("innovation")
        if "time" in msg_lower or "productiv" in msg_lower:
            all_themes.add("productivity")
    
    return list(all_themes)[:5]  # Top 5 themes


def unify_tone(brand_tone, slogan_tone):
    """Unify tone from creative signals."""
    if brand_tone and slogan_tone and brand_tone == slogan_tone:
        return brand_tone
    
    # Default to brand tone if available
    return brand_tone or slogan_tone or "professional"


def produce_messaging_guidelines(tone, themes, slogan_text, value_prop):
    """Produce messaging framework and guidelines."""
    
    # Tone guidelines
    tone_guidelines = {
        "professional": {
            "voice": "Clear, confident, results-oriented",
            "language": "Use data-driven language, avoid jargon",
            "style": "Direct and authoritative"
        },
        "playful": {
            "voice": "Fun, energetic, approachable",
            "language": "Use casual language, emojis welcome",
            "style": "Conversational and lighthearted"
        },
        "inspirational": {
            "voice": "Empowering, aspirational, emotional",
            "language": "Use motivational language, paint vision",
            "style": "Uplifting and transformative"
        },
        "bold": {
            "voice": "Strong, direct, impactful",
            "language": "Use powerful verbs, make statements",
            "style": "Confident and assertive"
        },
        "minimalist": {
            "voice": "Simple, refined, essential",
            "language": "Use concise language, avoid excess",
            "style": "Clean and focused"
        }
    }
    
    guidelines = tone_guidelines.get(tone, tone_guidelines["professional"])
    
    # Key messages
    key_messages = [
        value_prop,
        slogan_text if slogan_text else "Innovation that matters"
    ]
    
    # Add theme-based messages
    theme_messages = {
        "efficiency": "Save time and resources",
        "innovation": "Powered by cutting-edge technology",
        "simplicity": "Easy to use, powerful results",
        "productivity": "Get more done, faster"
    }
    
    for theme in themes[:3]:
        if theme in theme_messages:
            key_messages.append(theme_messages[theme])
    
    return {
        "tone": tone,
        "voice_guidelines": guidelines,
        "key_messages": key_messages[:5],
        "do": [
            f"Use {tone} language",
            "Focus on benefits over features",
            "Be consistent across channels"
        ],
        "dont": [
            "Use jargon or technical terms",
            "Make unsubstantiated claims",
            "Deviate from brand tone"
        ]
    }


def run(params: dict) -> dict:
    """
    Main handler entrypoint.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        {status, output, errors} envelope
    """
    log("info", "brand_context_normalize_start", params_keys=list(params.keys()))
    
    errors = []
    
    # Extract inputs
    brand = params.get("brand", {})
    creative = params.get("creative", {})
    
    # Validate required fields
    if not brand:
        errors.append("Missing required field: brand")
    if not creative:
        errors.append("Missing required field: creative")
    
    if errors:
        log("error", "brand_context_normalize_validation_failed", errors=errors)
        return {"status": "error", "output": {}, "errors": errors}
    
    # Extract brand fields
    brand_name = brand.get("brand_name", "")
    industry = brand.get("industry", "")
    target_audience = brand.get("target_audience", "")
    brand_values = brand.get("brand_values", [])
    brand_tone = brand.get("tone", "professional")
    
    # Extract creative outputs
    slogan_output = creative.get("slogan")
    landing_page_output = creative.get("landing_page")
    social_pack_output = creative.get("social_pack")
    
    log("info", "brand_context_normalize_extracting",
        has_slogan=bool(slogan_output),
        has_landing=bool(landing_page_output),
        has_social=bool(social_pack_output))
    
    # Extract components
    hero_content = extract_hero_content(landing_page_output)
    benefits = extract_benefits(landing_page_output)
    themes = extract_themes(slogan_output)
    top_slogan = extract_top_slogan(slogan_output)
    social_messages = extract_social_messaging(social_pack_output)
    
    # Transform into business context
    mission = infer_mission(hero_content, themes, brand_values)
    
    positioning = derive_positioning(
        top_slogan, benefits, industry, target_audience
    )
    
    value_proposition = extract_value_proposition(benefits, hero_content)
    
    icp = reconstruct_icp(target_audience, brand_tone, social_messages)
    
    unified_themes = identify_brand_themes(themes, benefits, social_messages)
    
    unified_tone = unify_tone(brand_tone, top_slogan.get("tone") if top_slogan else None)
    
    messaging_framework = produce_messaging_guidelines(
        unified_tone,
        unified_themes,
        top_slogan.get("text") if top_slogan else "",
        value_proposition
    )
    
    # Build narrative
    narrative = (
        f"{brand_name} is a {industry} company serving {target_audience}. "
        f"Our mission is to {mission.lower()} "
        f"We are positioned as {positioning.lower()} "
        f"Our core themes are {', '.join(unified_themes)}."
    )
    
    # Construct output
    output = {
        "brand_name": brand_name,
        "mission": mission,
        "positioning": positioning,
        "value_proposition": value_proposition,
        "icp": icp,
        "brand_themes": unified_themes,
        "unified_tone": unified_tone,
        "narrative": narrative,
        "messaging_framework": messaging_framework,
        "metadata": {
            "normalized_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "sources": {
                "slogan": bool(slogan_output),
                "landing_page": bool(landing_page_output),
                "social_pack": bool(social_pack_output)
            }
        }
    }
    
    log("info", "brand_context_normalize_done",
        brand_name=brand_name,
        themes_count=len(unified_themes),
        tone=unified_tone)
    
    return {
        "status": "success",
        "output": output,
        "errors": []
    }


def main():
    """CLI entrypoint for testing."""
    try:
        input_data = json.loads(sys.stdin.read())
        result = run(input_data)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError as e:
        error_result = {
            "status": "error",
            "output": {},
            "errors": [f"Invalid JSON input: {str(e)}"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)
    except Exception as e:
        error_result = {
            "status": "error",
            "output": {},
            "errors": [f"Handler error: {str(e)}"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
