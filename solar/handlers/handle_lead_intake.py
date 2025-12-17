#!/usr/bin/env python3
"""
Solar Lead Intake Handler
Parses customer information, classifies commercial vs residential, and flags high-priority leads.
"""

import json
import sys
import re
from datetime import datetime

def validate_email(email):
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate Malaysian phone number."""
    pattern = r'^\+?60[0-9]{9,10}$'
    return bool(re.match(pattern, phone))

def calculate_priority_score(monthly_bill, property_type):
    """
    Calculate priority score for lead.
    Higher score = higher priority.
    """
    base_score = 0
    
    # Monthly bill factor (higher bill = higher priority)
    if monthly_bill >= 1000:
        base_score += 50
    elif monthly_bill >= 500:
        base_score += 30
    elif monthly_bill >= 200:
        base_score += 15
    else:
        base_score += 5
    
    # Property type factor (commercial/industrial = higher priority)
    if property_type == "industrial":
        base_score += 30
    elif property_type == "commercial":
        base_score += 20
    else:  # residential
        base_score += 10
    
    return min(base_score, 100)  # Cap at 100

def estimate_system_size(monthly_bill, property_type):
    """
    Estimate solar system size based on monthly bill.
    Simplified calculation: bill / (rate * days * hours)
    """
    # Average rate per kWh
    rate_per_kwh = 0.40
    
    # Average daily usage estimate
    daily_usage_kwh = (monthly_bill / rate_per_kwh) / 30
    
    # System size needed (accounting for 80% self-consumption)
    system_size_kw = daily_usage_kwh / 4.5  # 4.5 hours average sunlight
    
    # Round to nearest 0.5 kW
    system_size_kw = round(system_size_kw * 2) / 2
    
    # Minimum 3kW, maximum based on property type
    min_size = 3.0
    if property_type == "industrial":
        max_size = 1000.0
    elif property_type == "commercial":
        max_size = 500.0
    else:  # residential
        max_size = 50.0
    
    return max(min_size, min(system_size_kw, max_size))

def handle_lead_intake(input_data):
    """
    Process solar lead intake data.
    
    Args:
        input_data: Dictionary containing lead information
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[Lead Intake] Starting processing...")
    print(f"[Lead Intake] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["customer_name", "email", "phone", "address", "property_type", "monthly_bill"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[Lead Intake] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate email
    if not validate_email(input_data["email"]):
        errors.append("Invalid email format")
    
    # Validate phone
    if not validate_phone(input_data["phone"]):
        errors.append("Invalid phone format. Expected: +60XXXXXXXXX")
    
    # Validate monthly bill
    if input_data["monthly_bill"] <= 0:
        errors.append("Monthly bill must be greater than 0")
    
    # Validate property type
    valid_property_types = ["residential", "commercial", "industrial"]
    if input_data["property_type"] not in valid_property_types:
        errors.append(f"Invalid property type. Must be one of: {', '.join(valid_property_types)}")
    
    if errors:
        print(f"[Lead Intake] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract and normalize data
    customer_name = input_data["customer_name"].strip()
    email = input_data["email"].strip().lower()
    phone = input_data["phone"]
    address = input_data["address"].strip()
    property_type = input_data["property_type"]
    monthly_bill = float(input_data["monthly_bill"])
    roof_type = input_data.get("roof_type", "unknown")
    roof_area_sqm = float(input_data.get("roof_area_sqm", 0))
    priority_notes = input_data.get("priority_notes", "")
    source = input_data.get("source", "website")
    
    print(f"[Lead Intake] Processing lead for: {customer_name}")
    print(f"[Lead Intake] Property type: {property_type}, Monthly bill: RM {monthly_bill}")
    
    # Calculate priority score
    priority_score = calculate_priority_score(monthly_bill, property_type)
    is_high_priority = priority_score >= 50
    
    print(f"[Lead Intake] Priority score: {priority_score}, High priority: {is_high_priority}")
    
    # Estimate system size
    estimated_system_size_kw = estimate_system_size(monthly_bill, property_type)
    print(f"[Lead Intake] Estimated system size: {estimated_system_size_kw} kW")
    
    # Build normalized data
    normalized_data = {
        "customer_name": customer_name,
        "email": email,
        "phone": phone,
        "address": address,
        "property_type": property_type,
        "monthly_bill": monthly_bill,
        "priority_score": priority_score,
        "is_high_priority": is_high_priority,
        "estimated_system_size_kw": estimated_system_size_kw,
        "roof_type": roof_type,
        "roof_area_sqm": roof_area_sqm if roof_area_sqm > 0 else None,
        "source": source,
        "lead_form_fields": {
            "form_type": "SOLAR_LEAD_INTAKE",
            "customer_details": {
                "name": customer_name,
                "email": email,
                "phone": phone,
                "address": address
            },
            "property_details": {
                "type": property_type,
                "monthly_bill": monthly_bill,
                "roof_type": roof_type,
                "roof_area": roof_area_sqm if roof_area_sqm > 0 else None
            },
            "lead_qualification": {
                "priority_score": priority_score,
                "is_high_priority": is_high_priority,
                "estimated_system_size_kw": estimated_system_size_kw,
                "source": source,
                "notes": priority_notes
            },
            "processed_at": datetime.now().isoformat()
        }
    }
    
    # Build proposal payload for Proposal Engine
    proposal_payload = {
        "tool": "lead_intake",
        "vertical": "solar",
        "timestamp": datetime.now().isoformat(),
        "customer_id": email,
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": [
            "site_inspection",
            "roi",
            "roof_check"
        ],
        "metadata": {
            "priority": "high" if is_high_priority else "normal",
            "estimated_value": estimated_system_size_kw * 4500  # Rough estimate
        }
    }
    
    print(f"[Lead Intake] Processing completed successfully")
    print(f"[Lead Intake] Priority: {'HIGH' if is_high_priority else 'NORMAL'}, System size: {estimated_system_size_kw} kW")
    
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
        
        # Process the intake
        result = handle_lead_intake(input_data)
        
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

