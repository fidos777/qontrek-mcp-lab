#!/usr/bin/env python3
"""
Landing Page Generator Handler
Generates conversion-optimized landing page structures.
"""

import json
import sys
from datetime import datetime
from lib.logger import log

def generate_hero_section(value_proposition, cta_primary, cta_secondary):
    """Generate hero section content."""
    # Extract headline from value proposition (first part)
    parts = value_proposition.split(' with ')
    headline = parts[0] if parts else value_proposition[:50]
    
    return {
        "section_id": "hero",
        "section_type": "hero",
        "content": {
            "headline": headline,
            "subheadline": value_proposition,
            "cta_primary": cta_primary,
            "cta_secondary": cta_secondary
        }
    }

def generate_benefits_section(key_benefits):
    """Generate benefits grid section."""
    return {
        "section_id": "benefits",
        "section_type": "benefits_grid",
        "content": {
            "headline": "Why Choose Us",
            "benefits": [
                {
                    "title": benefit.split(' ')[0:3],
                    "description": benefit
                }
                for benefit in key_benefits
            ]
        }
    }

def generate_features_section(features):
    """Generate features showcase section."""
    if not features:
        return None
    
    return {
        "section_id": "features",
        "section_type": "feature_showcase",
        "content": {
            "headline": "Powerful Features",
            "features": [
                {
                    "name": f["name"],
                    "headline": f["name"],
                    "description": f["description"]
                }
                for f in features
            ]
        }
    }

def generate_social_proof_section(social_proof):
    """Generate social proof section."""
    if not social_proof:
        return None
    
    testimonials = social_proof.get("testimonials", [])
    if not testimonials:
        return None
    
    return {
        "section_id": "testimonial",
        "section_type": "testimonial",
        "content": testimonials[0] if testimonials else {}
    }

def generate_faq_section():
    """Generate FAQ section."""
    return {
        "section_id": "faq",
        "section_type": "faq",
        "content": {
            "headline": "Frequently Asked Questions",
            "questions": [
                {
                    "question": "How does it work?",
                    "answer": "Simple and intuitive process designed for ease of use."
                },
                {
                    "question": "Is it secure?",
                    "answer": "Yes, we use industry-standard security measures."
                },
                {
                    "question": "How long does it take?",
                    "answer": "Most users see results within the first week."
                }
            ]
        }
    }

def generate_final_cta_section(cta_primary, product_name):
    """Generate final call-to-action section."""
    return {
        "section_id": "final_cta",
        "section_type": "call_to_action",
        "content": {
            "headline": f"Ready to Get Started with {product_name}?",
            "subheadline": "Join thousands of satisfied users today",
            "cta_primary": cta_primary,
            "trust_signals": ["Free trial", "No credit card required", "Cancel anytime"]
        }
    }

def run(params: dict) -> dict:
    """
    Universal handler entrypoint for landing page generation.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        dict with status, data, errors
    """
    log("info", "pagegen_landingpage_start",
        page_title=params.get("page_title"),
        page_goal=params.get("page_goal"),
        tone=params.get("tone"))
    
    errors = []
    
    # Validate required fields
    required = ["page_title", "page_goal", "product_name", "value_proposition", 
                "target_audience", "key_benefits", "cta_primary", "tone"]
    for field in required:
        if field not in params:
            errors.append(f"Missing required field: {field}")
    
    # Validate key_benefits count
    if "key_benefits" in params:
        benefits_count = len(params["key_benefits"])
        if benefits_count < 3 or benefits_count > 6:
            errors.append(f"key_benefits must have 3-6 items, got {benefits_count}")
    
    if errors:
        log("error", "pagegen_landingpage_validation_failed", errors=errors)
        return {
            "status": "error",
            "output": None,
            "errors": errors
        }
    
    # Extract inputs
    page_title = params["page_title"]
    page_goal = params["page_goal"]
    product_name = params["product_name"]
    value_proposition = params["value_proposition"]
    target_audience = params["target_audience"]
    key_benefits = params["key_benefits"]
    cta_primary = params["cta_primary"]
    cta_secondary = params.get("cta_secondary")
    tone = params["tone"]
    features = params.get("features", [])
    social_proof = params.get("social_proof", {})
    include_faq = params.get("include_faq", True)
    include_video = params.get("include_video", False)
    
    # Build sections
    sections = []
    
    # 1. Hero section (always first)
    sections.append(generate_hero_section(value_proposition, cta_primary, cta_secondary))
    
    # 2. Benefits section
    sections.append(generate_benefits_section(key_benefits))
    
    # 3. Features section (if provided)
    features_section = generate_features_section(features)
    if features_section:
        sections.append(features_section)
    
    # 4. Social proof (if provided)
    social_section = generate_social_proof_section(social_proof)
    if social_section:
        sections.append(social_section)
    
    # 5. FAQ section (if enabled)
    if include_faq:
        sections.append(generate_faq_section())
    
    # 6. Final CTA (always last)
    sections.append(generate_final_cta_section(cta_primary, product_name))
    
    # Build metadata
    meta = {
        "description": value_proposition[:160],
        "keywords": [product_name.lower(), page_goal.replace('_', ' ')]
    }
    
    # Build conversion elements
    conversion_elements = {
        "primary_cta_count": len([s for s in sections if "cta_primary" in str(s)]),
        "form_fields": ["email", "full_name"],
        "trust_signals": ["Free trial", "No credit card required"]
    }
    
    # Build output
    data = {
        "page_title": page_title,
        "sections": sections,
        "meta": meta,
        "conversion_elements": conversion_elements
    }
    
    log("info", "pagegen_landingpage_done",
        section_count=len(sections),
        page_goal=page_goal)
    
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
        log("error", "pagegen_landingpage_json_error", error=str(e))
        error_result = {
            "status": "error",
            "output": None,
            "errors": [f"Invalid JSON input: {str(e)}"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)
    except Exception as e:
        log("error", "pagegen_landingpage_fatal_error", error=str(e))
        error_result = {
            "status": "error",
            "output": None,
            "errors": [f"Processing error: {str(e)}"]
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
