#!/usr/bin/env python3
"""
LaunchKit Branding Generator - Production Version
Uses LLM client for intelligent, context-aware brand content generation.
"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path
from lib.logger import log
from lib.llm_client import generate


def load_prompt(skill_dir: str, prompt_name: str) -> str:
    """Load prompt template from prompts/ directory."""
    prompt_path = Path(skill_dir) / "prompts" / f"{prompt_name}.txt"
    if prompt_path.exists():
        return prompt_path.read_text()
    return ""


def load_template(skill_dir: str, template_name: str) -> str:
    """Load output template from templates/ directory."""
    template_path = Path(skill_dir) / "templates" / f"{template_name}.md"
    if template_path.exists():
        return template_path.read_text()
    return ""


def prepare_context(params: dict) -> dict:
    """Prepare context for LLM generation."""
    icp = params.get("icp", {})
    
    return {
        "brand_name": params.get("brand_name", ""),
        "mission": params.get("mission", ""),
        "positioning": params.get("positioning", ""),
        "value_proposition": params.get("value_proposition", ""),
        "icp_demographics": icp.get("demographics", ""),
        "icp_pain_points": ", ".join(icp.get("pain_points", [])),
        "icp_goals": ", ".join(icp.get("goals", [])),
        "brand_themes": ", ".join(params.get("brand_themes", [])),
        "unified_tone": params.get("unified_tone", "professional"),
        "messaging_framework": params.get("messaging_framework", {})
    }


def generate_brand_story(context: dict, skill_dir: str) -> str:
    """Generate brand story using LLM."""
    prompt = f"""Generate a compelling 2-3 paragraph brand story for {context['brand_name']}.

Mission: {context['mission']}
Themes: {context['brand_themes']}
Target: {context['icp_demographics']}

Create an emotional narrative that:
- Explains why the brand exists
- Connects to customer transformation
- Reflects the core themes
- Is authentic and engaging
"""
    
    return generate(prompt, context, max_tokens=500)


def generate_vision_statement(context: dict) -> str:
    """Generate vision statement using LLM."""
    prompt = f"""Generate a one-sentence vision statement for {context['brand_name']}.

Mission: {context['mission']}
Themes: {context['brand_themes']}

The vision should be:
- Future-oriented
- Aspirational
- Aligned with themes
- Clear and memorable
"""
    
    return generate(prompt, context, max_tokens=100)


def generate_value_prop_block(context: dict) -> dict:
    """Generate structured value proposition block."""
    value_prop = context.get("value_proposition", "")
    pain_points = context.get("icp_pain_points", "").split(", ")
    goals = context.get("icp_goals", "").split(", ")
    
    # Parse value prop into headline
    parts = value_prop.split(".")
    headline = parts[0].strip() if parts else value_prop
    subheadline = " ".join(parts[1:]).strip() if len(parts) > 1 else ""
    
    # Generate bullets addressing pain points and goals
    bullets = []
    for goal in goals[:3]:
        if goal:
            bullets.append(f"✓ {goal}")
    
    for pain in pain_points[:2]:
        if pain:
            bullets.append(f"✓ Eliminate {pain.lower()}")
    
    return {
        "headline": headline,
        "subheadline": subheadline,
        "bullets": bullets[:5]
    }


def generate_tone_guide(context: dict) -> dict:
    """Generate comprehensive tone guide."""
    tone = context.get("unified_tone", "professional")
    messaging = context.get("messaging_framework", {})
    voice_guidelines = messaging.get("voice_guidelines", {})
    
    # Tone-specific examples
    tone_examples = {
        "professional": {
            "good": ["Increase productivity by 40%", "Data-driven insights", "Proven results"],
            "bad": ["Super awesome!", "You'll love this!", "Amazing stuff"]
        },
        "playful": {
            "good": ["Make work fun again", "Your productivity sidekick", "Work smarter, play harder"],
            "bad": ["Synergize workflows", "Optimize KPIs", "Enterprise-grade"]
        },
        "inspirational": {
            "good": ["Transform your potential", "Unlock your greatness", "Dream bigger"],
            "bad": ["Basic features", "Standard package", "Normal results"]
        },
        "bold": {
            "good": ["Disrupt the status quo", "Break the mold", "Lead the revolution"],
            "bad": ["Maybe consider", "Possibly helpful", "Might work"]
        },
        "minimalist": {
            "good": ["Simple. Powerful.", "Less is more", "Essential tools only"],
            "bad": ["Feature-packed!", "Tons of options!", "Everything included"]
        }
    }
    
    examples = tone_examples.get(tone, tone_examples["professional"])
    
    return {
        "tone": tone,
        "voice": voice_guidelines.get("voice", "Clear and confident"),
        "language": voice_guidelines.get("language", "Use clear, accessible language"),
        "style": voice_guidelines.get("style", "Direct and engaging"),
        "do": messaging.get("do", ["Be clear", "Focus on benefits", "Stay consistent"]),
        "dont": messaging.get("dont", ["Use jargon", "Make false claims", "Deviate from tone"]),
        "examples": examples
    }


def generate_taglines(context: dict) -> list:
    """Generate tagline variations using LLM."""
    prompt = f"""Generate 7 tagline variations for {context['brand_name']}.

Themes: {context['brand_themes']}
Value Prop: {context['value_proposition']}
Tone: {context['unified_tone']}

Create taglines that are:
- Memorable and concise (3-7 words)
- Theme-based, value-based, and action-oriented
- Unique to this brand
- Emotionally resonant

Format: One tagline per line
"""
    
    taglines_text = generate(prompt, context, max_tokens=300)
    
    # Parse taglines
    taglines = []
    for i, line in enumerate(taglines_text.strip().split("\n")[:7], 1):
        line = line.strip().lstrip("0123456789.-) ")
        if line:
            taglines.append({
                "text": line,
                "type": "theme-based" if i <= 3 else "value-based" if i <= 5 else "action-oriented",
                "rationale": f"Emphasizes {context['brand_themes'].split(',')[0] if i <= 3 else 'value proposition'}"
            })
    
    return taglines


def run(params: dict) -> dict:
    """
    Main handler entrypoint.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        {status, output, errors} envelope
    """
    log("info", "branding_generate_start", params_keys=list(params.keys()))
    
    errors = []
    
    # Validate required fields
    required = ["brand_name", "mission", "value_proposition", "icp", "brand_themes"]
    for field in required:
        if not params.get(field):
            errors.append(f"Missing required field: {field}")
    
    if errors:
        log("error", "branding_generate_validation_failed", errors=errors)
        return {"status": "error", "output": {}, "errors": errors}
    
    # Get skill directory for loading prompts/templates
    skill_dir = Path(__file__).parent
    
    # Prepare context
    context = prepare_context(params)
    
    log("info", "branding_generate_processing",
        brand_name=context["brand_name"],
        themes_count=len(params.get("brand_themes", [])))
    
    try:
        # Generate components using LLM
        brand_story = generate_brand_story(context, str(skill_dir))
        vision_statement = generate_vision_statement(context)
        value_prop_block = generate_value_prop_block(context)
        tone_guide = generate_tone_guide(context)
        taglines = generate_taglines(context)
        
        # Construct output
        output = {
            "brand_name": params.get("brand_name"),
            "brand_story": brand_story,
            "mission_statement": params.get("mission"),
            "vision_statement": vision_statement,
            "positioning_statement": params.get("positioning"),
            "value_prop_block": value_prop_block,
            "tone_guide": tone_guide,
            "taglines": taglines,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "2.0.0",
                "llm_powered": True,
                "components": 7
            }
        }
        
        log("info", "branding_generate_done",
            brand_name=params.get("brand_name"),
            taglines_count=len(taglines))
        
        return {
            "status": "success",
            "output": output,
            "errors": []
        }
        
    except Exception as e:
        log("error", "branding_generate_error", error=str(e))
        return {
            "status": "error",
            "output": {},
            "errors": [f"Generation error: {str(e)}"]
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
