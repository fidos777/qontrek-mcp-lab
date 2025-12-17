#!/usr/bin/env python3
"""
Site Inspection Handler
Processes site inspection data including images, address, and utility bill.
Estimates roof angle, usable area, and shading score.
"""

import json
import sys
import re
from datetime import datetime

def validate_date(date_str):
    """Validate date format YYYY-MM-DD."""
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def estimate_roof_angle(roof_measurements):
    """Estimate roof angle from measurements or use default."""
    if roof_measurements and "angle_degrees" in roof_measurements:
        return float(roof_measurements["angle_degrees"])
    # Default angle for Malaysia (tropical climate)
    return 15.0

def calculate_usable_area(roof_measurements, shading_obstacles):
    """
    Calculate usable roof area accounting for shading obstacles.
    """
    if roof_measurements and "usable_area_sqm" in roof_measurements:
        base_area = float(roof_measurements["usable_area_sqm"])
    elif roof_measurements and "total_area_sqm" in roof_measurements:
        # Assume 80% of total area is usable
        base_area = float(roof_measurements["total_area_sqm"]) * 0.8
    else:
        return None
    
    # Reduce area based on shading impact
    shading_reduction = 0
    if shading_obstacles:
        for obstacle in shading_obstacles:
            impact = obstacle.get("impact", "low")
            if impact == "high":
                shading_reduction += 0.15
            elif impact == "medium":
                shading_reduction += 0.10
            else:
                shading_reduction += 0.05
    
    usable_area = base_area * (1 - min(shading_reduction, 0.5))  # Max 50% reduction
    return round(usable_area, 2)

def calculate_shading_score(shading_obstacles):
    """
    Calculate shading score (0-100, higher = less shading).
    """
    if not shading_obstacles:
        return 100
    
    score = 100
    for obstacle in shading_obstacles:
        impact = obstacle.get("impact", "low")
        if impact == "high":
            score -= 20
        elif impact == "medium":
            score -= 10
        else:
            score -= 5
    
    return max(0, min(100, score))

def estimate_system_capacity(usable_area_sqm, shading_score):
    """
    Estimate system capacity based on usable area and shading.
    Assumes ~6 sqm per kW (including spacing).
    """
    if usable_area_sqm is None:
        return None
    
    # Base capacity
    base_capacity = usable_area_sqm / 6.0
    
    # Adjust for shading (reduce capacity if high shading)
    shading_factor = shading_score / 100.0
    capacity = base_capacity * shading_factor
    
    return round(capacity, 2)

def handle_site_inspection(input_data):
    """
    Process site inspection data.
    
    Args:
        input_data: Dictionary containing inspection information
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[Site Inspection] Starting processing...")
    print(f"[Site Inspection] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["address", "inspection_date"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[Site Inspection] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate date format
    if not validate_date(input_data["inspection_date"]):
        errors.append("Invalid inspection date format. Expected: YYYY-MM-DD")
    
    if errors:
        print(f"[Site Inspection] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract and normalize data
    address = input_data["address"].strip()
    inspection_date = input_data["inspection_date"]
    inspector_name = input_data.get("inspector_name", "")
    images = input_data.get("images", [])
    utility_bill = input_data.get("utility_bill", {})
    roof_measurements = input_data.get("roof_measurements", {})
    shading_obstacles = input_data.get("shading_obstacles", [])
    
    print(f"[Site Inspection] Processing inspection for: {address}")
    print(f"[Site Inspection] Date: {inspection_date}, Images: {len(images)}")
    
    # Estimate roof angle
    roof_angle = estimate_roof_angle(roof_measurements)
    print(f"[Site Inspection] Estimated roof angle: {roof_angle} degrees")
    
    # Calculate usable area
    usable_area_sqm = calculate_usable_area(roof_measurements, shading_obstacles)
    print(f"[Site Inspection] Usable area: {usable_area_sqm} sqm" if usable_area_sqm else "[Site Inspection] Usable area: Not available")
    
    # Calculate shading score
    shading_score = calculate_shading_score(shading_obstacles)
    print(f"[Site Inspection] Shading score: {shading_score}/100")
    
    # Estimate system capacity
    estimated_capacity_kw = estimate_system_capacity(usable_area_sqm, shading_score) if usable_area_sqm else None
    if estimated_capacity_kw:
        print(f"[Site Inspection] Estimated system capacity: {estimated_capacity_kw} kW")
    
    # Build normalized data
    normalized_data = {
        "address": address,
        "inspection_date": inspection_date,
        "inspector_name": inspector_name,
        "roof_angle_degrees": roof_angle,
        "usable_area_sqm": usable_area_sqm,
        "shading_score": shading_score,
        "estimated_system_capacity_kw": estimated_capacity_kw,
        "image_count": len(images),
        "inspection_form_fields": {
            "form_type": "SITE_INSPECTION",
            "inspection_details": {
                "address": address,
                "date": inspection_date,
                "inspector": inspector_name
            },
            "roof_analysis": {
                "angle_degrees": roof_angle,
                "usable_area_sqm": usable_area_sqm,
                "orientation": roof_measurements.get("orientation"),
                "total_area_sqm": roof_measurements.get("total_area_sqm")
            },
            "shading_analysis": {
                "score": shading_score,
                "obstacles_count": len(shading_obstacles),
                "obstacles": shading_obstacles
            },
            "utility_info": utility_bill,
            "images": images,
            "system_estimate": {
                "capacity_kw": estimated_capacity_kw
            },
            "processed_at": datetime.now().isoformat()
        }
    }
    
    print("[Site Inspection] Inspection normalized successfully")
    
    # Build proposal payload for Proposal Engine
    proposal_payload = {
        "tool": "site_inspection",
        "vertical": "solar",
        "timestamp": datetime.now().isoformat(),
        "property_id": address,
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": [
            "roi",
            "roof_check",
            "quotation"
        ],
        "metadata": {
            "inspection_complete": True,
            "estimated_capacity_kw": estimated_capacity_kw
        }
    }
    
    print(f"[Site Inspection] Processing completed successfully")
    
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
        
        # Process the inspection
        result = handle_site_inspection(input_data)
        
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

