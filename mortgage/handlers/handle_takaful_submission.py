#!/usr/bin/env python3
"""
Takaful Submission Handler
Normalizes takaful insurance requirements and submission data.
"""

import json
import sys
import re
from datetime import datetime

def validate_ic_number(ic):
    """Validate Malaysian IC number format."""
    pattern = r'^[0-9]{6}-[0-9]{2}-[0-9]{4}$'
    return bool(re.match(pattern, ic))

def calculate_premium_estimate(coverage_amount, coverage_type, age, payment_method):
    """
    Calculate estimated Takaful premium.
    Simplified calculation for demonstration.
    """
    base_rate = 0.001  # 0.1% base rate
    
    # Adjust rate based on coverage type
    type_multipliers = {
        "mrta": 1.0,
        "mlta": 1.5,
        "fire": 0.3,
        "comprehensive": 2.0
    }
    multiplier = type_multipliers.get(coverage_type, 1.0)
    
    # Age adjustment
    age_factor = 1.0 + (max(0, age - 30) * 0.01)
    
    # Payment method adjustment
    payment_discounts = {
        "single": 0.95,  # 5% discount for single payment
        "annual": 1.0,
        "monthly": 1.05  # 5% premium for monthly
    }
    payment_factor = payment_discounts.get(payment_method, 1.0)
    
    annual_premium = coverage_amount * base_rate * multiplier * age_factor * payment_factor
    
    if payment_method == "single":
        return round(annual_premium * 10, 2)  # 10-year single premium estimate
    elif payment_method == "annual":
        return round(annual_premium, 2)
    else:  # monthly
        return round(annual_premium / 12, 2)

def handle_takaful_submission(input_data):
    """
    Process Takaful submission data.
    
    Args:
        input_data: Dictionary containing takaful submission information
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[Takaful Submission] Starting processing...")
    print(f"[Takaful Submission] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["customer_ic", "loan_amount", "property_value", "coverage_type"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[Takaful Submission] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate IC number format
    if not validate_ic_number(input_data["customer_ic"]):
        errors.append("Invalid customer IC number format. Expected: YYMMDD-PB-GGGG")
    
    # Validate beneficiary IC if provided
    if "beneficiary_ic" in input_data and input_data["beneficiary_ic"]:
        if not validate_ic_number(input_data["beneficiary_ic"]):
            errors.append("Invalid beneficiary IC number format")
    
    # Validate numeric fields
    if input_data["loan_amount"] <= 0:
        errors.append("Loan amount must be greater than 0")
    if input_data["property_value"] <= 0:
        errors.append("Property value must be greater than 0")
    
    # Validate coverage type
    valid_coverage_types = ["mrta", "mlta", "fire", "comprehensive"]
    if input_data["coverage_type"] not in valid_coverage_types:
        errors.append(f"Invalid coverage type. Must be one of: {', '.join(valid_coverage_types)}")
    
    if errors:
        print(f"[Takaful Submission] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract and normalize data
    customer_ic = input_data["customer_ic"]
    loan_amount = float(input_data["loan_amount"])
    property_value = float(input_data["property_value"])
    coverage_type = input_data["coverage_type"]
    payment_method = input_data.get("premium_payment_method", "annual")
    beneficiary_name = input_data.get("beneficiary_name", "")
    beneficiary_ic = input_data.get("beneficiary_ic", "")
    medical_declaration = input_data.get("medical_declaration", False)
    age = int(input_data.get("age", 30))
    
    print(f"[Takaful Submission] Processing for customer: {customer_ic}")
    print(f"[Takaful Submission] Loan: RM {loan_amount}, Property: RM {property_value}")
    print(f"[Takaful Submission] Coverage type: {coverage_type}, Payment: {payment_method}")
    
    # Determine coverage amount (typically loan amount or property value, whichever is lower)
    coverage_amount = min(loan_amount, property_value)
    print(f"[Takaful Submission] Coverage amount: RM {coverage_amount}")
    
    # Calculate premium estimate
    premium_estimate = calculate_premium_estimate(coverage_amount, coverage_type, age, payment_method)
    print(f"[Takaful Submission] Premium estimate: RM {premium_estimate} ({payment_method})")
    
    # Build beneficiary details
    beneficiary_details = {}
    if beneficiary_name:
        beneficiary_details["name"] = beneficiary_name
    if beneficiary_ic:
        beneficiary_details["ic"] = beneficiary_ic
    
    # Build normalized data
    normalized_data = {
        "customer_ic": customer_ic,
        "coverage_amount": coverage_amount,
        "coverage_type": coverage_type,
        "premium_estimate": premium_estimate,
        "payment_method": payment_method,
        "beneficiary_details": beneficiary_details if beneficiary_details else None,
        "medical_declaration": medical_declaration,
        "age": age,
        "takaful_form_fields": {
            "form_type": "TAKAFUL_SUBMISSION",
            "customer_details": {
                "ic": customer_ic,
                "age": age
            },
            "coverage_details": {
                "type": coverage_type,
                "amount": coverage_amount,
                "loan_amount": loan_amount,
                "property_value": property_value
            },
            "premium_details": {
                "estimated_premium": premium_estimate,
                "payment_method": payment_method
            },
            "beneficiary": beneficiary_details if beneficiary_details else None,
            "medical": {
                "declaration_completed": medical_declaration
            },
            "calculated_at": datetime.now().isoformat()
        }
    }
    
    # Build proposal payload for Proposal Engine
    proposal_payload = {
        "tool": "takaful_submission",
        "vertical": "mortgage-lppsa",
        "timestamp": datetime.now().isoformat(),
        "customer_id": customer_ic,
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": [
            "lawyer_intake",
            "property_checklist"
        ]
    }
    
    print(f"[Takaful Submission] Processing completed successfully")
    print(f"[Takaful Submission] Coverage: {coverage_type}, Premium: RM {premium_estimate}")
    
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
        
        # Process the submission
        result = handle_takaful_submission(input_data)
        
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

