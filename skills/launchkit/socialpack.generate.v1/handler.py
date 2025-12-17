#!/usr/bin/env python3
"""
LaunchKit Social Pack Generator - Production Version
Generates strategic launch content for social channels.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from lib.logger import log
from lib.llm_client import generate


def prepare_context(params: dict) -> dict:
    """Prepare context for LLM generation."""
    messaging = params.get("messaging_framework", {})
    
    return {
        "brand_name": params.get("brand_name", ""),
        "value_proposition": params.get("value_proposition", ""),
        "key_messages": ", ".join(messaging.get("key_messages", [])),
        "tone": params.get("unified_tone", "professional"),
        "launch_date": params.get("launch_date", ""),
        "target_audience": params.get("target_audience", "")
    }


def generate_hooks(context: dict) -> list:
    """Generate attention-grabbing hooks."""
    prompt = f"""Generate 7 attention-grabbing social media hooks for {context['brand_name']}.

Value Prop: {context['value_proposition']}
Tone: {context['tone']}

Create hooks that:
- Stop the scroll
- Create curiosity
- Promise value
- Match the tone

Format: One hook per line, 10-15 words each.
"""
    
    hooks_text = generate(prompt, context, max_tokens=400)
    
    hooks = []
    for line in hooks_text.strip().split("\n"):
        line = line.strip().lstrip("0123456789.-*• ")
        if line and len(line.split()) <= 20:
            hooks.append({
                "text": line,
                "character_count": len(line),
                "platform": "universal"
            })
    
    return hooks[:7]


def generate_announcements(context: dict) -> list:
    """Generate launch announcement posts."""
    brand_name = context.get("brand_name", "")
    value_prop = context.get("value_proposition", "")
    
    announcements = []
    
    # Twitter/X announcement
    announcements.append({
        "platform": "twitter",
        "content": f"🚀 Introducing {brand_name}!\n\n{value_prop}\n\nJoin the waitlist → [link]\n\n#{brand_name} #Launch",
        "character_count": len(f"🚀 Introducing {brand_name}!\n\n{value_prop}\n\nJoin the waitlist → [link]\n\n#{brand_name} #Launch"),
        "hashtags": [f"#{brand_name}", "#Launch", "#ProductLaunch"]
    })
    
    # LinkedIn announcement
    announcements.append({
        "platform": "linkedin",
        "content": f"We're thrilled to announce the launch of {brand_name}! 🎉\n\n{value_prop}\n\nAfter months of development, we're ready to help you transform your workflow.\n\nLearn more: [link]\n\n#{brand_name} #ProductLaunch #Innovation",
        "character_count": len(f"We're thrilled to announce the launch of {brand_name}! 🎉\n\n{value_prop}"),
        "hashtags": [f"#{brand_name}", "#ProductLaunch", "#Innovation"]
    })
    
    # Instagram announcement
    announcements.append({
        "platform": "instagram",
        "content": f"✨ {brand_name} is here! ✨\n\n{value_prop}\n\nTap the link in bio to get started.\n\n#{brand_name} #Launch #NewProduct",
        "character_count": len(f"✨ {brand_name} is here! ✨\n\n{value_prop}"),
        "hashtags": [f"#{brand_name}", "#Launch", "#NewProduct"]
    })
    
    return announcements


def generate_teasers(context: dict) -> list:
    """Generate pre-launch teaser posts."""
    brand_name = context.get("brand_name", "")
    
    teasers = [
        {
            "timing": "7 days before",
            "content": f"Something big is coming... 👀\n\n{brand_name} launches next week.\n\nGet ready.",
            "platform": "universal"
        },
        {
            "timing": "3 days before",
            "content": f"3 days until {brand_name} changes everything.\n\nAre you ready?",
            "platform": "universal"
        },
        {
            "timing": "1 day before",
            "content": f"Tomorrow. {brand_name} launches.\n\nSet your reminders 🔔",
            "platform": "universal"
        },
        {
            "timing": "Launch day morning",
            "content": f"Today's the day! {brand_name} launches in a few hours.\n\nStay tuned...",
            "platform": "universal"
        }
    ]
    
    return teasers


def generate_faqs(context: dict) -> list:
    """Generate FAQ posts."""
    brand_name = context.get("brand_name", "")
    value_prop = context.get("value_proposition", "")
    
    faqs = [
        {
            "question": f"What is {brand_name}?",
            "answer": value_prop,
            "format": "carousel_slide_1"
        },
        {
            "question": "Who is it for?",
            "answer": f"{brand_name} is perfect for {context.get('target_audience', 'professionals')} looking to level up.",
            "format": "carousel_slide_2"
        },
        {
            "question": "How much does it cost?",
            "answer": f"{brand_name} offers flexible pricing plans to fit your needs. Check our website for details.",
            "format": "carousel_slide_3"
        },
        {
            "question": "When can I start?",
            "answer": "Sign up today and start immediately. No credit card required for the trial.",
            "format": "carousel_slide_4"
        },
        {
            "question": "What makes it different?",
            "answer": f"{brand_name} combines innovation with simplicity—built for real users, not just features.",
            "format": "carousel_slide_5"
        }
    ]
    
    return faqs


def generate_cta_variants(context: dict) -> list:
    """Generate call-to-action variations."""
    brand_name = context.get("brand_name", "")
    
    ctas = [
        {"text": f"Try {brand_name} free →", "urgency": "low", "style": "direct"},
        {"text": "Get started in 60 seconds", "urgency": "medium", "style": "benefit"},
        {"text": "Join 1,000+ early users today", "urgency": "medium", "style": "social_proof"},
        {"text": "Limited spots available—claim yours", "urgency": "high", "style": "scarcity"},
        {"text": "See it in action (2-min demo)", "urgency": "low", "style": "demo"},
        {"text": "Start your free trial now", "urgency": "medium", "style": "trial"},
        {"text": "Transform your workflow today", "urgency": "medium", "style": "transformation"}
    ]
    
    return ctas


def generate_countdown(context: dict) -> list:
    """Generate countdown sequence."""
    brand_name = context.get("brand_name", "")
    launch_date = context.get("launch_date", "soon")
    
    countdown = [
        {"days_before": 7, "message": f"7 days until {brand_name} 🚀", "visual": "7 in bold"},
        {"days_before": 5, "message": f"5 days to go! {brand_name} is almost here", "visual": "5 in bold"},
        {"days_before": 3, "message": f"3 days left. The countdown is real ⏰", "visual": "3 in bold"},
        {"days_before": 2, "message": f"48 hours until launch 🎯", "visual": "2 in bold"},
        {"days_before": 1, "message": f"Tomorrow! {brand_name} launches 🔥", "visual": "1 in bold"},
        {"days_before": 0, "message": f"🚀 {brand_name} is LIVE! 🚀", "visual": "LIVE animation"}
    ]
    
    return countdown


def run(params: dict) -> dict:
    """
    Main handler entrypoint.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        {status, output, errors} envelope
    """
    log("info", "socialpack_generate_start", params_keys=list(params.keys()))
    
    errors = []
    
    # Validate required fields
    required = ["brand_name", "value_proposition"]
    for field in required:
        if not params.get(field):
            errors.append(f"Missing required field: {field}")
    
    if errors:
        log("error", "socialpack_generate_validation_failed", errors=errors)
        return {"status": "error", "output": {}, "errors": errors}
    
    # Prepare context
    context = prepare_context(params)
    
    log("info", "socialpack_generate_processing", brand_name=context["brand_name"])
    
    try:
        # Generate social content components
        hooks = generate_hooks(context)
        announcements = generate_announcements(context)
        teasers = generate_teasers(context)
        faqs = generate_faqs(context)
        cta_variants = generate_cta_variants(context)
        countdown = generate_countdown(context)
        
        # Construct output
        output = {
            "brand_name": params.get("brand_name"),
            "hooks": hooks,
            "launch_announcements": announcements,
            "teaser_posts": teasers,
            "faq_posts": faqs,
            "cta_variants": cta_variants,
            "countdown_sequence": countdown,
            "content_calendar": {
                "pre_launch": len(teasers) + len(countdown),
                "launch_day": len(announcements),
                "post_launch": len(faqs) + len(cta_variants)
            },
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "2.0.0",
                "llm_powered": True,
                "total_assets": len(hooks) + len(announcements) + len(teasers) + len(faqs) + len(cta_variants) + len(countdown)
            }
        }
        
        log("info", "socialpack_generate_done",
            brand_name=params.get("brand_name"),
            hooks_count=len(hooks),
            total_assets=output["metadata"]["total_assets"])
        
        return {
            "status": "success",
            "output": output,
            "errors": []
        }
        
    except Exception as e:
        log("error", "socialpack_generate_error", error=str(e))
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
