#!/usr/bin/env python3
"""
LaunchKit Pitchdeck Generator - Production Version
Generates 9-slide investor pitch deck from brand and product context.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from lib.logger import log
from lib.llm_client import generate


def prepare_context(params: dict) -> dict:
    """Prepare context for LLM generation."""
    branding = params.get("branding", {})
    prd = params.get("prd", {})
    pricing = params.get("pricing", {})
    roadmap = params.get("roadmap", {})
    
    return {
        "brand_name": params.get("brand_name", ""),
        "mission": branding.get("mission_statement", ""),
        "vision": branding.get("vision_statement", ""),
        "value_prop": branding.get("value_prop_block", {}).get("headline", ""),
        "problem": prd.get("problem_statement", ""),
        "solution": prd.get("solution_overview", ""),
        "features": prd.get("feature_list", {}).get("mvp", []),
        "tiers": pricing.get("tiers", []),
        "business_model": pricing.get("billing_model", ""),
        "milestones": roadmap.get("milestones", [])
    }


def generate_slide_content(slide_type: str, context: dict) -> dict:
    """Generate content for a specific slide type."""
    
    slide_generators = {
        "cover": generate_cover_slide,
        "problem": generate_problem_slide,
        "solution": generate_solution_slide,
        "market": generate_market_slide,
        "product": generate_product_slide,
        "business_model": generate_business_model_slide,
        "roadmap": generate_roadmap_slide,
        "team": generate_team_slide,
        "ask": generate_ask_slide
    }
    
    generator = slide_generators.get(slide_type)
    if generator:
        return generator(context)
    
    return {
        "id": slide_type,
        "title": slide_type.replace("_", " ").title(),
        "subtitle": "",
        "bullets": [],
        "speaker_notes": ""
    }


def generate_cover_slide(context: dict) -> dict:
    """Generate cover slide."""
    return {
        "id": "cover",
        "title": context.get("brand_name", "Company Name"),
        "subtitle": context.get("value_prop", "Transforming the industry"),
        "bullets": [],
        "visual_concept": "Bold brand logo centered, gradient background",
        "speaker_notes": f"Welcome. Today I'm excited to share {context.get('brand_name')}, and how we're solving a critical problem in the market."
    }


def generate_problem_slide(context: dict) -> dict:
    """Generate problem slide."""
    problem_text = context.get("problem", "")
    
    # Extract key points from problem statement
    bullets = []
    for line in problem_text.split("\n"):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith("-")):
            bullets.append(line.lstrip("0123456789.-) "))
    
    if not bullets:
        bullets = [
            "Current solutions are inadequate",
            "Users face significant challenges",
            "Market opportunity is substantial"
        ]
    
    return {
        "id": "problem",
        "title": "The Problem",
        "subtitle": "A critical challenge facing the market",
        "bullets": bullets[:4],
        "visual_concept": "Problem icons or pain point illustrations",
        "speaker_notes": "The market faces a significant problem. " + problem_text[:200] + "..."
    }


def generate_solution_slide(context: dict) -> dict:
    """Generate solution slide."""
    solution_text = context.get("solution", "")
    
    bullets = [
        f"Introducing {context.get('brand_name')}",
        context.get("value_prop", "Our innovative approach"),
        "Built on cutting-edge technology",
        "Designed for real-world impact"
    ]
    
    return {
        "id": "solution",
        "title": "Our Solution",
        "subtitle": context.get("value_prop", ""),
        "bullets": bullets,
        "visual_concept": "Product screenshot or solution diagram",
        "speaker_notes": f"{context.get('brand_name')} solves this through {solution_text[:150]}..."
    }


def generate_market_slide(context: dict) -> dict:
    """Generate market opportunity slide."""
    prompt = f"""Generate market opportunity content for {context.get('brand_name')}.

Include:
- Total Addressable Market (TAM)
- Serviceable Addressable Market (SAM)
- Target market size
- Growth trends

Format as 4 bullet points.
"""
    
    market_text = generate(prompt, context, max_tokens=300)
    
    bullets = []
    for line in market_text.split("\n"):
        line = line.strip().lstrip("-*• ")
        if line and len(bullets) < 4:
            bullets.append(line)
    
    if len(bullets) < 4:
        bullets = [
            "TAM: $10B+ global market opportunity",
            "SAM: $2B serviceable market",
            "Growing 25% annually",
            "Early-stage market with high potential"
        ]
    
    return {
        "id": "market",
        "title": "Market Opportunity",
        "subtitle": "A large and growing market",
        "bullets": bullets,
        "visual_concept": "Market size chart or growth graph",
        "speaker_notes": "The market opportunity is substantial and growing rapidly."
    }


def generate_product_slide(context: dict) -> dict:
    """Generate product features slide."""
    features = context.get("features", [])
    
    bullets = features[:5] if features else [
        "Core feature 1",
        "Core feature 2",
        "Core feature 3",
        "Core feature 4"
    ]
    
    return {
        "id": "product",
        "title": "Product",
        "subtitle": "Key features and capabilities",
        "bullets": bullets,
        "visual_concept": "Product demo or feature showcase",
        "speaker_notes": f"Our product delivers {len(bullets)} core capabilities that directly address user needs."
    }


def generate_business_model_slide(context: dict) -> dict:
    """Generate business model slide."""
    tiers = context.get("tiers", [])
    business_model = context.get("business_model", "Subscription-based")
    
    bullets = [
        f"Model: {business_model}",
        f"Pricing tiers: {len(tiers)} options" if tiers else "Tiered pricing strategy",
        "Multiple revenue streams",
        "Scalable unit economics"
    ]
    
    # Add tier names if available
    if tiers:
        tier_names = [tier.get("name", "") for tier in tiers[:3]]
        if tier_names:
            bullets.append(f"Tiers: {', '.join(tier_names)}")
    
    return {
        "id": "business_model",
        "title": "Business Model",
        "subtitle": "How we make money",
        "bullets": bullets[:5],
        "visual_concept": "Revenue model diagram or pricing table",
        "speaker_notes": f"Our business model is {business_model}, with clear paths to profitability."
    }


def generate_roadmap_slide(context: dict) -> dict:
    """Generate traction and roadmap slide."""
    milestones = context.get("milestones", [])
    
    bullets = []
    if milestones:
        for milestone in milestones[:4]:
            if isinstance(milestone, dict):
                bullets.append(milestone.get("title", milestone.get("name", "")))
            else:
                bullets.append(str(milestone))
    
    if not bullets:
        bullets = [
            "Q1: MVP launch and initial users",
            "Q2: Product-market fit validation",
            "Q3: Scale and partnerships",
            "Q4: Revenue growth and expansion"
        ]
    
    return {
        "id": "roadmap",
        "title": "Traction & Roadmap",
        "subtitle": "Our path to scale",
        "bullets": bullets,
        "visual_concept": "Timeline or milestone chart",
        "speaker_notes": "We have a clear roadmap with measurable milestones."
    }


def generate_team_slide(context: dict) -> dict:
    """Generate team slide."""
    brand_name = context.get("brand_name", "Company")
    
    bullets = [
        "Experienced founding team",
        "Deep domain expertise",
        "Track record of execution",
        "Advisors from leading companies"
    ]
    
    return {
        "id": "team",
        "title": "Team",
        "subtitle": "The people building the future",
        "bullets": bullets,
        "visual_concept": "Team photos with titles",
        "speaker_notes": f"The {brand_name} team brings decades of combined experience in this space."
    }


def generate_ask_slide(context: dict) -> dict:
    """Generate investment ask slide."""
    bullets = [
        "Seeking: Seed/Series A funding",
        "Use of funds: Product, team, growth",
        "Projected milestones with funding",
        "Expected ROI and exit potential"
    ]
    
    return {
        "id": "ask",
        "title": "The Ask",
        "subtitle": "Join us in building the future",
        "bullets": bullets,
        "visual_concept": "Investment breakdown chart",
        "speaker_notes": "We're raising capital to accelerate growth and capture this market opportunity."
    }


def run(params: dict) -> dict:
    """
    Main handler entrypoint.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        {status, output, errors} envelope
    """
    log("info", "pitchdeck_generate_start", params_keys=list(params.keys()))
    
    errors = []
    
    # Validate required fields
    required = ["brand_name"]
    for field in required:
        if not params.get(field):
            errors.append(f"Missing required field: {field}")
    
    if errors:
        log("error", "pitchdeck_generate_validation_failed", errors=errors)
        return {"status": "error", "output": {}, "errors": errors}
    
    # Prepare context
    context = prepare_context(params)
    
    log("info", "pitchdeck_generate_processing", brand_name=context["brand_name"])
    
    try:
        # Generate 9-slide deck
        slide_types = [
            "cover", "problem", "solution", "market", 
            "product", "business_model", "roadmap", "team", "ask"
        ]
        
        slides = []
        for slide_type in slide_types:
            slide = generate_slide_content(slide_type, context)
            slides.append(slide)
        
        # Create deck outline
        deck_outline = [
            {"slide_number": i+1, "title": slide["title"], "purpose": slide.get("subtitle", "")}
            for i, slide in enumerate(slides)
        ]
        
        # Construct output
        output = {
            "brand_name": params.get("brand_name"),
            "deck_outline": deck_outline,
            "slides": slides,
            "total_slides": len(slides),
            "estimated_duration": "10-15 minutes",
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "2.0.0",
                "llm_powered": True,
                "slide_count": len(slides)
            }
        }
        
        log("info", "pitchdeck_generate_done",
            brand_name=params.get("brand_name"),
            slide_count=len(slides))
        
        return {
            "status": "success",
            "output": output,
            "errors": []
        }
        
    except Exception as e:
        log("error", "pitchdeck_generate_error", error=str(e))
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
