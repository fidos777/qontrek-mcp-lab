#!/usr/bin/env python3
"""
Lawyer Intake Handler
Captures Sale & Purchase (S&P) agreement details and panel lawyer information.
"""

import json
import sys
import re
from datetime import datetime

def validate_ic_number(ic):
    """Validate Malaysian IC number format."""
    pattern = r'^[0-9]{6}-[0-9]{2}-[0-9]{4}$'
    return bool(re.match(pattern, ic))

def validate_email(email):
    """Basic email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate Malaysian phone number."""
    pattern = r'^\+?60[0-9]{9,10}$'
    return bool(re.match(pattern, phone))

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

def handle_lawyer_intake(input_data):
    """
    Process lawyer intake data.
    
    Args:
        input_data: Dictionary containing lawyer and S&P information
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[Lawyer Intake] Starting processing...")
    print(f"[Lawyer Intake] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["customer_ic", "property_address", "snp_date", "lawyer_firm_name"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[Lawyer Intake] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate IC number format
    if not validate_ic_number(input_data["customer_ic"]):
        errors.append("Invalid customer IC number format. Expected: YYMMDD-PB-GGGG")
    
    # Validate vendor IC if provided
    if "vendor_ic" in input_data and input_data["vendor_ic"]:
        if not validate_ic_number(input_data["vendor_ic"]):
            errors.append("Invalid vendor IC number format")
    
    # Validate email if provided
    if "lawyer_email" in input_data and input_data["lawyer_email"]:
        if not validate_email(input_data["lawyer_email"]):
            errors.append("Invalid lawyer email format")
    
    # Validate phone if provided
    if "lawyer_contact" in input_data and input_data["lawyer_contact"]:
        if not validate_phone(input_data["lawyer_contact"]):
            errors.append("Invalid lawyer contact format. Expected: +60XXXXXXXXX")
    
    # Validate date format
    if not validate_date(input_data["snp_date"]):
        errors.append("Invalid S&P date format. Expected: YYYY-MM-DD")
    
    if "completion_date" in input_data and input_data["completion_date"]:
        if not validate_date(input_data["completion_date"]):
            errors.append("Invalid completion date format. Expected: YYYY-MM-DD")
    
    if errors:
        print(f"[Lawyer Intake] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract and normalize data
    customer_ic = input_data["customer_ic"]
    property_address = input_data["property_address"].strip()
    snp_date = input_data["snp_date"]
    lawyer_firm_name = input_data["lawyer_firm_name"].strip()
    lawyer_name = input_data.get("lawyer_name", "").strip()
    lawyer_contact = input_data.get("lawyer_contact", "")
    lawyer_email = input_data.get("lawyer_email", "")
    snp_number = input_data.get("snp_number", "")
    vendor_name = input_data.get("vendor_name", "").strip()
    vendor_ic = input_data.get("vendor_ic", "")
    purchase_price = float(input_data.get("purchase_price", 0))
    completion_date = input_data.get("completion_date", "")
    is_panel_lawyer = input_data.get("is_panel_lawyer", False)
    
    print(f"[Lawyer Intake] Processing for customer: {customer_ic}")
    print(f"[Lawyer Intake] Property: {property_address}")
    print(f"[Lawyer Intake] S&P Date: {snp_date}, Lawyer Firm: {lawyer_firm_name}")
    print(f"[Lawyer Intake] Panel Lawyer: {is_panel_lawyer}")
    
    # Build lawyer details
    lawyer_details = {
        "firm_name": lawyer_firm_name,
        "is_panel": is_panel_lawyer
    }
    if lawyer_name:
        lawyer_details["lawyer_name"] = lawyer_name
    if lawyer_contact:
        lawyer_details["contact"] = lawyer_contact
    if lawyer_email:
        lawyer_details["email"] = lawyer_email
    
    # Build vendor details
    vendor_details = {}
    if vendor_name:
        vendor_details["name"] = vendor_name
    if vendor_ic:
        vendor_details["ic"] = vendor_ic
    
    # Build normalized data
    normalized_data = {
        "customer_ic": customer_ic,
        "property_address": property_address,
        "snp_reference": snp_number if snp_number else f"SNP-{customer_ic}-{snp_date}",
        "snp_date": snp_date,
        "lawyer_firm": lawyer_firm_name,
        "lawyer_details": lawyer_details,
        "vendor_details": vendor_details if vendor_details else None,
        "purchase_price": purchase_price,
        "completion_date": completion_date,
        "panel_approved": is_panel_lawyer,
        "legal_form_fields": {
            "form_type": "LAWYER_INTAKE",
            "customer_details": {
                "ic": customer_ic
            },
            "property_details": {
                "address": property_address,
                "purchase_price": purchase_price
            },
            "snp_details": {
                "reference": snp_number if snp_number else f"SNP-{customer_ic}-{snp_date}",
                "date": snp_date,
                "completion_date": completion_date
            },
            "lawyer_details": lawyer_details,
            "vendor_details": vendor_details if vendor_details else None,
            "panel_status": {
                "is_panel": is_panel_lawyer,
                "status": "approved" if is_panel_lawyer else "pending_verification"
            },
            "processed_at": datetime.now().isoformat()
        }
    }
    
    # Build proposal payload for Proposal Engine
    proposal_payload = {
        "tool": "lawyer_intake",
        "vertical": "mortgage-lppsa",
        "timestamp": datetime.now().isoformat(),
        "customer_id": customer_ic,
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": [
            "property_checklist"
        ]
    }
    
    print(f"[Lawyer Intake] Processing completed successfully")
    print(f"[Lawyer Intake] Panel Status: {'Approved' if is_panel_lawyer else 'Pending Verification'}")
    
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
        result = handle_lawyer_intake(input_data)
        
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

