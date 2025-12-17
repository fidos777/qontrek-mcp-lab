#!/usr/bin/env python3
"""
LPPSA Intake Handler
Normalizes customer data into LPPSA form fields.
"""

import json
import sys
import re
from datetime import datetime

def validate_ic_number(ic):
    """Validate Malaysian IC number format."""
    pattern = r'^[0-9]{6}-[0-9]{2}-[0-9]{4}$'
    return bool(re.match(pattern, ic))

def calculate_dsr(income, loan_amount, loan_tenure_years, existing_loans=0):
    """Calculate Debt Service Ratio (DSR)."""
    monthly_loan_payment = (loan_amount * 0.04) / 12  # Simplified: 4% annual rate / 12 months
    total_monthly_commitments = monthly_loan_payment + existing_loans
    dsr = (total_monthly_commitments / income) * 100 if income > 0 else 0
    return round(dsr, 2)

def determine_eligibility(dsr, income, loan_amount, property_price):
    """Determine LPPSA eligibility status."""
    if dsr > 70:
        return "not_eligible"
    if income < 3000:
        return "not_eligible"
    if loan_amount > property_price * 0.9:
        return "not_eligible"
    if loan_amount > 300000:
        return "not_eligible"
    return "eligible"

def handle_lppsa_intake(input_data):
    """
    Process LPPSA intake data.
    
    Args:
        input_data: Dictionary containing customer intake information
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[LPPSA Intake] Starting processing...")
    print(f"[LPPSA Intake] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["customer_name", "ic_number", "income", "property_price", "loan_amount", "loan_tenure"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[LPPSA Intake] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate IC number format
    if not validate_ic_number(input_data["ic_number"]):
        errors.append("Invalid IC number format. Expected: YYMMDD-PB-GGGG")
    
    # Validate numeric fields
    if input_data["income"] <= 0:
        errors.append("Income must be greater than 0")
    if input_data["property_price"] <= 0:
        errors.append("Property price must be greater than 0")
    if input_data["loan_amount"] <= 0:
        errors.append("Loan amount must be greater than 0")
    if input_data["loan_tenure"] < 1 or input_data["loan_tenure"] > 35:
        errors.append("Loan tenure must be between 1 and 35 years")
    
    if errors:
        print(f"[LPPSA Intake] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract and normalize data
    customer_name = input_data["customer_name"].strip().upper()
    ic_number = input_data["ic_number"]
    income = float(input_data["income"])
    property_price = float(input_data["property_price"])
    loan_amount = float(input_data["loan_amount"])
    loan_tenure = int(input_data["loan_tenure"])
    existing_loans = float(input_data.get("existing_loans", 0))
    employment_type = input_data.get("employment_type", "private")
    marital_status = input_data.get("marital_status", "single")
    dependents = int(input_data.get("dependents", 0))
    
    print(f"[LPPSA Intake] Processing customer: {customer_name}")
    print(f"[LPPSA Intake] IC: {ic_number}, Income: RM {income}")
    print(f"[LPPSA Intake] Property: RM {property_price}, Loan: RM {loan_amount}, Tenure: {loan_tenure} years")
    
    # Calculate DSR
    dsr = calculate_dsr(income, loan_amount, loan_tenure, existing_loans)
    print(f"[LPPSA Intake] Calculated DSR: {dsr}%")
    
    # Determine eligibility
    eligibility = determine_eligibility(dsr, income, loan_amount, property_price)
    print(f"[LPPSA Intake] Eligibility status: {eligibility}")
    
    # Build normalized data
    normalized_data = {
        "applicant_name": customer_name,
        "ic_number": ic_number,
        "monthly_income": income,
        "property_value": property_price,
        "loan_requested": loan_amount,
        "loan_period_years": loan_tenure,
        "dsr_ratio": dsr,
        "eligibility_status": eligibility,
        "employment_type": employment_type,
        "marital_status": marital_status,
        "dependents": dependents,
        "existing_loans": existing_loans,
        "lppsa_form_fields": {
            "form_type": "LPPSA_APPLICATION",
            "applicant_details": {
                "name": customer_name,
                "ic": ic_number,
                "employment": employment_type,
                "marital_status": marital_status
            },
            "property_details": {
                "value": property_price,
                "loan_amount": loan_amount,
                "tenure": loan_tenure
            },
            "financial_details": {
                "income": income,
                "dsr": dsr,
                "existing_commitments": existing_loans
            },
            "eligibility": {
                "status": eligibility,
                "calculated_at": datetime.now().isoformat()
            }
        }
    }
    
    # Build proposal payload for Proposal Engine
    proposal_payload = {
        "tool": "lppsa_intake",
        "vertical": "mortgage-lppsa",
        "timestamp": datetime.now().isoformat(),
        "customer_id": ic_number,
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": [
            "takaful_submission",
            "property_checklist",
            "lawyer_intake"
        ]
    }
    
    print(f"[LPPSA Intake] Processing completed successfully")
    print(f"[LPPSA Intake] Eligibility: {eligibility}, DSR: {dsr}%")
    
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
        result = handle_lppsa_intake(input_data)
        
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

