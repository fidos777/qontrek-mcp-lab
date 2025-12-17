#!/usr/bin/env python3
"""
Roof Check Handler
Classifies roof type and determines appropriate mounting type.
"""

import json
import sys
from datetime import datetime

def determine_mounting_type(roof_type, roof_angle, roof_condition):
    """
    Determine appropriate mounting type based on roof characteristics.
    """
    mounting_map = {
        "metal": "rail_mount",
        "concrete": "ballast_mount",
        "shingle": "penetration_mount",
        "tile": "penetration_mount",
        "asphalt": "penetration_mount"
    }
    
    # Default mounting type
    mounting_type = mounting_map.get(roof_type, "rail_mount")
    
    # Adjust based on roof condition
    if roof_condition == "poor":
        mounting_type = "ballast_mount"  # Avoid penetration on poor roofs
    
    # Adjust for flat roofs (low angle)
    if roof_angle and roof_angle < 5:
        mounting_type = "ballast_mount"
    
    return mounting_type

def is_roof_suitable(roof_type, roof_condition, roof_age_years, structural_load):
    """
    Determine if roof is suitable for solar installation.
    """
    # Check roof condition
    if roof_condition == "poor":
        return False
    
    # Check roof age (very old roofs may not be suitable)
    if roof_age_years and roof_age_years > 30:
        return False
    
    # Check structural load capacity
    if structural_load and structural_load < 20:  # Minimum 20 kg/sqm
        return False
    
    # Unknown roof type needs inspection
    if roof_type == "unknown":
        return None  # Unknown - needs further assessment
    
    return True

def generate_recommendations(roof_type, roof_condition, roof_age_years, 
                             structural_load, accessibility, existing_installations):
    """
    Generate recommendations based on roof characteristics.
    """
    recommendations = []
    
    if roof_condition == "fair":
        recommendations.append("Consider roof repair before installation")
    
    if roof_age_years and roof_age_years > 20:
        recommendations.append("Roof may need replacement within system lifetime")
    
    if structural_load and structural_load < 30:
        recommendations.append("Structural assessment recommended")
    
    if accessibility == "difficult":
        recommendations.append("Consider accessibility improvements for maintenance")
    
    if existing_installations and "solar_panels" in existing_installations:
        recommendations.append("Existing solar installation detected - verify compatibility")
    
    if not recommendations:
        recommendations.append("Roof is suitable for solar installation")
    
    return recommendations

def handle_roof_check(input_data):
    """
    Process roof check data.
    
    Args:
        input_data: Dictionary containing roof information
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[Roof Check] Starting processing...")
    print(f"[Roof Check] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["roof_type"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[Roof Check] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate roof type
    valid_roof_types = ["metal", "concrete", "shingle", "tile", "asphalt", "unknown"]
    if input_data["roof_type"] not in valid_roof_types:
        errors.append(f"Invalid roof type. Must be one of: {', '.join(valid_roof_types)}")
    
    if errors:
        print(f"[Roof Check] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract and normalize data
    roof_type = input_data["roof_type"]
    roof_age_years = float(input_data.get("roof_age_years", 0)) if input_data.get("roof_age_years") else None
    roof_condition = input_data.get("roof_condition", "good")
    roof_angle = float(input_data.get("roof_angle_degrees", 0)) if input_data.get("roof_angle_degrees") else None
    roof_area_sqm = float(input_data.get("roof_area_sqm", 0)) if input_data.get("roof_area_sqm") else None
    structural_load = float(input_data.get("structural_load_capacity", 0)) if input_data.get("structural_load_capacity") else None
    existing_installations = input_data.get("existing_installations", [])
    accessibility = input_data.get("accessibility", "moderate")
    wind_zone = input_data.get("wind_zone", "medium")
    
    print(f"[Roof Check] Processing roof type: {roof_type}")
    print(f"[Roof Check] Condition: {roof_condition}, Age: {roof_age_years} years" if roof_age_years else f"[Roof Check] Condition: {roof_condition}")
    
    # Determine mounting type
    mounting_type = determine_mounting_type(roof_type, roof_angle, roof_condition)
    print(f"[Roof Check] Recommended mounting type: {mounting_type}")
    
    # Check if roof is suitable
    is_suitable = is_roof_suitable(roof_type, roof_condition, roof_age_years, structural_load)
    print(f"[Roof Check] Roof suitable: {is_suitable}")
    
    # Generate recommendations
    recommendations = generate_recommendations(
        roof_type, roof_condition, roof_age_years,
        structural_load, accessibility, existing_installations
    )
    print(f"[Roof Check] Recommendations: {len(recommendations)} items")
    
    # Build normalized data
    normalized_data = {
        "roof_type": roof_type,
        "mounting_type": mounting_type,
        "is_suitable": is_suitable,
        "recommendations": recommendations,
        "roof_check_form_fields": {
            "form_type": "ROOF_CHECK",
            "roof_characteristics": {
                "type": roof_type,
                "age_years": roof_age_years,
                "condition": roof_condition,
                "angle_degrees": roof_angle,
                "area_sqm": roof_area_sqm,
                "structural_load_kg_sqm": structural_load
            },
            "mounting_analysis": {
                "recommended_type": mounting_type,
                "accessibility": accessibility,
                "wind_zone": wind_zone
            },
            "suitability": {
                "is_suitable": is_suitable,
                "recommendations": recommendations
            },
            "existing_installations": existing_installations,
            "processed_at": datetime.now().isoformat()
        }
    }
    
    # Build proposal payload for Proposal Engine
    proposal_payload = {
        "tool": "roof_check",
        "vertical": "solar",
        "timestamp": datetime.now().isoformat(),
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": [
            "quotation"
        ],
        "metadata": {
            "roof_suitable": is_suitable,
            "mounting_type": mounting_type
        }
    }
    
    print(f"[Roof Check] Processing completed successfully")
    
    return {
        "status": "success",
        "normalized_data": normalized_data,
        "proposal_payload": proposal_payload,
        "errors": []
    }

def main():
    """Main entry point for command-line execution."""
    try:
        # Read input from stdin
        input_json = sys.stdin.read()
        input_data = json.loads(input_json)
        
        # Process the roof check
        result = handle_roof_check(input_data)
        
        # Output result as JSON
        print(json.dumps(result, indent=2))
        
    except json.JSONDecodeError as e:
        error_result = {
            "status": "error",
            "errors": [f"Invalid JSON input: {str(e)}"],
            "normalized_data": None,
            "proposal_payload": None
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)
    except Exception as e:
        error_result = {
            "status": "error",
            "errors": [f"Processing error: {str(e)}"],
            "normalized_data": None,
            "proposal_payload": None
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)

if __name__ == "__main__":
    main()

