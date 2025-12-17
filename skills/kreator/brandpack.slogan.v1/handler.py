#!/usr/bin/env python3
"""
Brandpack Slogan Generator Handler
Generates brand slogans based on brand identity and positioning.
"""

import json
import sys
from datetime import datetime
import random
from lib.logger import log

def extract_themes(brand_values, industry):
    """Extract key themes from brand values and industry context."""
    themes = list(brand_values[:5])
    
    # Add industry-specific themes
    industry_themes = {
        "tech": ["innovation", "digital", "future"],
        "saas": ["efficiency", "productivity", "automation"],
        "fashion": ["style", "design", "expression"],
        "fitness": ["health", "transformation", "strength"],
        "food": ["quality", "taste", "experience"],
        "education": ["learning", "growth", "knowledge"]
    }
    
    industry_lower = industry.lower()
    for key, values in industry_themes.items():
        if key in industry_lower:
            themes.extend(values[:2])
            break
    
    return list(set(themes))[:5]

def calculate_memorability(text):
    """Calculate memorability score based on linguistic patterns."""
    score = 5.0
    words = text.split()
    
    # Length optimization (3-7 words ideal)
    if 3 <= len(words) <= 7:
        score += 2.0
    elif len(words) < 3:
        score += 1.0
    
    # Character count (10-40 ideal)
    char_count = len(text)
    if 10 <= char_count <= 40:
        score += 1.5
    
    # Alliteration check
    first_letters = [w[0].lower() for w in words if w]
    if len(first_letters) != len(set(first_letters)):
        score += 1.0
    
    # Rhythm (alternating syllable pattern)
    if len(words) >= 2:
        score += 0.5
    
    return min(10.0, round(score, 1))

def generate_slogans(brand_name, brand_values, tone, count):
    """Generate slogan variations based on brand and tone."""
    slogans = []
    themes = brand_values[:3]
    
    # Tone-specific patterns
    patterns = {
        "professional": [
            f"{themes[0].title()}, Delivered",
            f"Your {themes[0].title()} Partner",
            f"{themes[0].title()} You Can Trust",
            f"Excellence in {themes[0].title()}",
            f"Powering {themes[0].title()}"
        ],
        "playful": [
            f"{themes[0].title()} Made Fun",
            f"Get Your {themes[0].title()} On",
            f"{themes[0].title()} That Clicks",
            f"Seriously {themes[0].title()}",
            f"{themes[0].title()}, Reimagined"
        ],
        "inspirational": [
            f"Unlock Your {themes[0].title()}",
            f"Where {themes[0].title()} Meets {themes[1].title() if len(themes) > 1 else 'Excellence'}",
            f"Elevate Your {themes[0].title()}",
            f"Dream. {themes[0].title()}. Achieve.",
            f"Your {themes[0].title()} Journey Starts Here"
        ],
        "bold": [
            f"{themes[0].title()}. Amplified.",
            f"Own Your {themes[0].title()}",
            f"No Limits. Pure {themes[0].title()}.",
            f"{themes[0].title()} Without Compromise",
            f"Redefining {themes[0].title()}"
        ],
        "minimalist": [
            f"Simply {themes[0].title()}",
            f"{themes[0].title()}. Nothing More.",
            f"Essential {themes[0].title()}",
            f"Pure {themes[0].title()}",
            f"{themes[0].title()}, Refined"
        ]
    }
    
    # Get patterns for tone
    tone_patterns = patterns.get(tone, patterns["professional"])
    
    # Generate slogans
    for i in range(min(count, len(tone_patterns))):
        text = tone_patterns[i]
        slogans.append({
            "text": text,
            "tone": tone,
            "rationale": f"Emphasizes {themes[0]} with {tone} tone, creating clear brand association",
            "character_count": len(text),
            "memorability_score": calculate_memorability(text)
        })
    
    # Sort by memorability score
    slogans.sort(key=lambda x: x["memorability_score"], reverse=True)
    
    return slogans

def run(params: dict) -> dict:
    """
    Universal handler entrypoint for slogan generation.
    
    Args:
        params: Input parameters matching schema.json
        
    Returns:
        dict with status, output, errors
    """
    log("info", "brandpack_slogan_start", 
        brand_name=params.get("brand_name"),
        tone=params.get("tone"),
        count=params.get("count", 5))
    
    errors = []
    
    # Validate required fields
    required = ["brand_name", "industry", "target_audience", "brand_values", "tone"]
    for field in required:
        if field not in params:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        log("error", "brandpack_slogan_validation_failed", errors=errors)
        return {
            "status": "error",
            "errors": errors,
            "output": None
        }
    
    # Extract inputs
    brand_name = params["brand_name"]
    industry = params["industry"]
    target_audience = params["target_audience"]
    brand_values = params["brand_values"]
    tone = params["tone"]
    language = params.get("language", "en")
    count = params.get("count", 5)
    
    # Extract themes
    themes = extract_themes(brand_values, industry)
    log("info", "brandpack_slogan_themes_extracted", themes=themes)
    
    # Generate slogans
    slogans = generate_slogans(brand_name, brand_values, tone, count)
    
    # Build output
    output = {
        "slogans": slogans,
        "brand_analysis": {
            "key_themes": themes,
            "positioning_summary": f"{brand_name} positions as a {tone} brand focused on {', '.join(brand_values[:3])} for {target_audience}"
        },
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "language": language
        }
    }
    
    log("info", "brandpack_slogan_done", 
        slogan_count=len(slogans),
        themes=themes,
        top_score=slogans[0]['memorability_score'] if slogans else 0)
    
    return {
        "status": "success",
        "output": output,
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
        log("error", "brandpack_slogan_json_error", error=str(e))
        error_result = {
            "status": "error",
            "errors": [f"Invalid JSON input: {str(e)}"],
            "output": None
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)
    except Exception as e:
        log("error", "brandpack_slogan_fatal_error", error=str(e))
        error_result = {
            "status": "error",
            "errors": [f"Processing error: {str(e)}"],
            "output": None
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()
