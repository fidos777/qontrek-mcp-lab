#!/usr/bin/env python3
"""
BrandContext Normalizer
Normalizes raw user input into BrandContext v2 format.
Deterministic, rule-based - NO LLM generation.
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple


# Load BrandContext v2 schema
SCHEMA_PATH = Path(__file__).parent / "brand_context_v2.json"
with open(SCHEMA_PATH, 'r') as f:
    BRAND_CONTEXT_V2_SCHEMA = json.load(f)


def normalize(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize raw input into BrandContext v2 format.
    
    Args:
        raw_input: Raw user input (may be incomplete or in old format)
        
    Returns:
        Either:
        - Normalized BrandContext v2 dict (if valid)
        - Error dict: {"status": "error", "error": {...}} (if invalid)
    """
    # Validate required fields
    is_valid, missing_fields = validate_required_fields(raw_input)
    
    if not is_valid:
        return {
            "status": "error",
            "error": {
                "type": "brand_context_invalid",
                "missing_fields": missing_fields,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }
        }
    
    # Build normalized context
    normalized = {
        "identity": normalize_identity(raw_input),
        "audience": normalize_audience(raw_input),
        "product": normalize_product(raw_input),
        "voice": normalize_voice(raw_input),
        "positioning": normalize_positioning(raw_input),
        "metadata": {
            "version": "2.0",
            "source": "user_input"
        }
    }
    
    return normalized


def validate_required_fields(raw_input: Dict[str, Any]) -> Tuple[bool, list]:
    """
    Validate that required fields are present.
    
    BrandContext v2 requires:
    - identity.name
    - At least one of: mission, value_proposition, or brand_themes
    - At least one audience field (icp, pain_points, or goals)
    
    Args:
        raw_input: Raw user input
        
    Returns:
        (is_valid: bool, missing_fields: list)
    """
    missing = []
    
    # Check brand_name (maps to identity.name)
    if not raw_input.get("brand_name"):
        missing.append("brand_name")
    
    # Check at least one identity field
    has_identity = any([
        raw_input.get("mission"),
        raw_input.get("value_proposition"),
        raw_input.get("brand_themes")
    ])
    
    if not has_identity:
        missing.append("mission or value_proposition or brand_themes")
    
    # Check at least one audience field
    icp = raw_input.get("icp", {})
    has_audience = any([
        icp.get("demographics"),
        icp.get("pain_points"),
        icp.get("goals"),
        raw_input.get("target_audience")
    ])
    
    if not has_audience:
        missing.append("icp (with demographics, pain_points, or goals)")
    
    return (len(missing) == 0, missing)


def normalize_identity(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize identity section.
    
    Maps:
    - brand_name → name
    - mission → mission
    - tagline → tagline
    - brand_story → story
    - brand_themes → values
    """
    identity = {
        "name": raw_input.get("brand_name", "")
    }
    
    # Optional fields
    if raw_input.get("tagline"):
        identity["tagline"] = raw_input["tagline"]
    
    if raw_input.get("brand_story"):
        identity["story"] = raw_input["brand_story"]
    
    if raw_input.get("mission"):
        identity["mission"] = raw_input["mission"]
    
    if raw_input.get("vision"):
        identity["vision"] = raw_input["vision"]
    
    # Map brand_themes to values
    if raw_input.get("brand_themes"):
        identity["values"] = raw_input["brand_themes"]
    
    return identity


def normalize_audience(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize audience section.
    
    Maps:
    - icp.demographics → demographics
    - icp.psychographics → psychographics
    - icp.pain_points → pain_points
    - icp.goals → goals
    - target_audience → icp (if icp not present)
    """
    audience = {}
    
    icp = raw_input.get("icp", {})
    
    # Demographics
    if icp.get("demographics"):
        audience["demographics"] = icp["demographics"]
    elif raw_input.get("target_audience"):
        audience["icp"] = raw_input["target_audience"]
    
    # Psychographics
    if icp.get("psychographics"):
        # Handle both string and array
        if isinstance(icp["psychographics"], list):
            audience["psychographics"] = ", ".join(icp["psychographics"])
        else:
            audience["psychographics"] = icp["psychographics"]
    
    # Pain points
    if icp.get("pain_points"):
        audience["pain_points"] = icp["pain_points"]
    
    # Goals
    if icp.get("goals"):
        audience["goals"] = icp["goals"]
    
    # Segments
    if icp.get("segments"):
        audience["segments"] = icp["segments"]
    
    return audience


def normalize_product(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize product section.
    
    Maps:
    - brand_name → name (if product_name not present)
    - value_proposition → value_prop
    - product_type → category
    - platform → platform
    """
    product = {}
    
    # Product name (default to brand name)
    if raw_input.get("product_name"):
        product["name"] = raw_input["product_name"]
    elif raw_input.get("brand_name"):
        product["name"] = raw_input["brand_name"]
    
    # Value proposition
    if raw_input.get("value_proposition"):
        product["value_prop"] = raw_input["value_proposition"]
    
    # Features
    if raw_input.get("features"):
        product["features"] = raw_input["features"]
    
    # Pricing model
    if raw_input.get("pricing_model"):
        product["pricing_model"] = raw_input["pricing_model"]
    elif raw_input.get("business_model_type"):
        product["pricing_model"] = raw_input["business_model_type"]
    
    # Category
    if raw_input.get("product_type"):
        product["category"] = raw_input["product_type"]
    elif raw_input.get("industry"):
        product["category"] = raw_input["industry"]
    
    # Platform
    if raw_input.get("platform"):
        product["platform"] = raw_input["platform"]
    
    return product


def normalize_voice(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize voice section.
    
    Maps:
    - unified_tone → tone
    - tone → tone
    - language → language
    """
    voice = {}
    
    # Tone
    if raw_input.get("unified_tone"):
        voice["tone"] = raw_input["unified_tone"]
    elif raw_input.get("tone"):
        voice["tone"] = raw_input["tone"]
    else:
        # Default tone
        voice["tone"] = "professional"
    
    # Language
    if raw_input.get("language"):
        voice["language"] = raw_input["language"]
    
    # Style
    if raw_input.get("style"):
        voice["style"] = raw_input["style"]
    
    return voice


def normalize_positioning(raw_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize positioning section.
    
    Maps:
    - positioning → statement
    - differentiators → differentiators
    - competitors → competitors
    """
    positioning = {}
    
    # Positioning statement
    if raw_input.get("positioning"):
        positioning["statement"] = raw_input["positioning"]
    
    # Differentiators
    if raw_input.get("differentiators"):
        positioning["differentiators"] = raw_input["differentiators"]
    
    # Competitors
    if raw_input.get("competitors"):
        positioning["competitors"] = raw_input["competitors"]
    
    return positioning


def get_normalized_field(normalized_context: Dict[str, Any], field_path: str, default: Any = None) -> Any:
    """
    Get a field from normalized context using dot notation.
    
    Args:
        normalized_context: Normalized BrandContext v2
        field_path: Dot-separated path (e.g., "identity.name")
        default: Default value if not found
        
    Returns:
        Field value or default
    """
    parts = field_path.split(".")
    current = normalized_context
    
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return default
    
    return current


# Backward compatibility helpers
def to_legacy_format(normalized_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert normalized BrandContext v2 back to legacy format for skills.
    
    This allows skills to continue using old field names while we transition.
    
    Args:
        normalized_context: Normalized BrandContext v2
        
    Returns:
        Legacy format dict
    """
    legacy = {}
    
    # Identity → top-level fields
    identity = normalized_context.get("identity", {})
    legacy["brand_name"] = identity.get("name", "")
    
    if identity.get("mission"):
        legacy["mission"] = identity["mission"]
    
    if identity.get("vision"):
        legacy["vision"] = identity["vision"]
    
    if identity.get("tagline"):
        legacy["tagline"] = identity["tagline"]
    
    if identity.get("story"):
        legacy["brand_story"] = identity["story"]
    
    if identity.get("values"):
        legacy["brand_themes"] = identity["values"]
    
    # Audience → icp
    audience = normalized_context.get("audience", {})
    legacy["icp"] = {}
    
    if audience.get("demographics"):
        legacy["icp"]["demographics"] = audience["demographics"]
    elif audience.get("icp"):
        legacy["icp"]["demographics"] = audience["icp"]
    
    if audience.get("psychographics"):
        # Convert back to array if needed
        psycho = audience["psychographics"]
        if isinstance(psycho, str):
            legacy["icp"]["psychographics"] = [p.strip() for p in psycho.split(",")]
        else:
            legacy["icp"]["psychographics"] = psycho
    
    if audience.get("pain_points"):
        legacy["icp"]["pain_points"] = audience["pain_points"]
    
    if audience.get("goals"):
        legacy["icp"]["goals"] = audience["goals"]
    
    # Product → top-level fields
    product = normalized_context.get("product", {})
    
    if product.get("value_prop"):
        legacy["value_proposition"] = product["value_prop"]
    
    if product.get("category"):
        legacy["product_type"] = product["category"]
    
    if product.get("platform"):
        legacy["platform"] = product["platform"]
    
    if product.get("pricing_model"):
        legacy["business_model_type"] = product["pricing_model"]
    
    # Voice → top-level fields
    voice = normalized_context.get("voice", {})
    
    if voice.get("tone"):
        legacy["unified_tone"] = voice["tone"]
    
    # Positioning → top-level field
    positioning = normalized_context.get("positioning", {})
    
    if positioning.get("statement"):
        legacy["positioning"] = positioning["statement"]
    
    return legacy
