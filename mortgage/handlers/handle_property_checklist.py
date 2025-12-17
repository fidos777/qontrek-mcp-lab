#!/usr/bin/env python3
"""
Property Checklist Handler
Validates property details and determines if new unit or subsale.
"""

import json
import sys
import re
from datetime import datetime

def validate_ic_number(ic):
    """Validate Malaysian IC number format."""
    pattern = r'^[0-9]{6}-[0-9]{2}-[0-9]{4}$'
    return bool(re.match(pattern, ic))

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

def classify_property(input_data):
    """
    Classify property as new unit or subsale.
    
    Logic:
    - If registration_date exists and is recent (< 2 years), likely new unit
    - If first_owner_ic matches customer_ic, likely new unit
    - If completion_certificate is CCC/OC, likely new unit
    - If subsale_evidence exists, likely subsale
    - Default: check is_new_unit flag if provided
    """
    # Check explicit flag first
    if "is_new_unit" in input_data:
        return "new_unit" if input_data["is_new_unit"] else "subsale"
    
    # Check for subsale evidence
    if input_data.get("subsale_evidence"):
        return "subsale"
    
    # Check registration date
    if "registration_date" in input_data and input_data["registration_date"]:
        try:
            reg_date = datetime.strptime(input_data["registration_date"], "%Y-%m-%d")
            years_old = (datetime.now() - reg_date).days / 365
            if years_old < 2:
                return "new_unit"
        except ValueError:
            pass
    
    # Check completion certificate status
    completion_cert = input_data.get("completion_certificate", "")
    if completion_cert in ["ccc", "oc"]:
        return "new_unit"
    if completion_cert == "pending":
        return "new_unit"  # Likely new unit awaiting completion
    
    # Default to subsale if uncertain
    return "subsale"

def determine_required_documents(classification, property_type, completion_status):
    """Determine required documents based on property classification."""
    base_docs = [
        "IC Copy",
        "Income Documents",
        "Bank Statements"
    ]
    
    if classification == "new_unit":
        docs = base_docs + [
            "Booking Form",
            "Developer Sales & Purchase Agreement",
            "Letter of Offer from Developer"
        ]
        if completion_status in ["ccc", "oc"]:
            docs.append("Certificate of Completion (CCC/OC)")
        else:
            docs.append("Provisional Certificate (if available)")
    else:  # subsale
        docs = base_docs + [
            "Sale & Purchase Agreement (Subsale)",
            "Title Deed",
            "Consent to Transfer",
            "Valuation Report"
        ]
    
    if property_type in ["condominium", "apartment"]:
        docs.append("Strata Title")
    
    return docs

def handle_property_checklist(input_data):
    """
    Process property checklist data.
    
    Args:
        input_data: Dictionary containing property information
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[Property Checklist] Starting processing...")
    print(f"[Property Checklist] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["property_address", "property_type", "developer_name"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[Property Checklist] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate IC number if provided
    if "first_owner_ic" in input_data and input_data["first_owner_ic"]:
        if not validate_ic_number(input_data["first_owner_ic"]):
            errors.append("Invalid first owner IC number format")
    
    # Validate date format if provided
    if "registration_date" in input_data and input_data["registration_date"]:
        if not validate_date(input_data["registration_date"]):
            errors.append("Invalid registration date format. Expected: YYYY-MM-DD")
    
    # Validate property type
    valid_property_types = ["condominium", "apartment", "terrace", "semi_detached", "bungalow", "townhouse"]
    if input_data["property_type"] not in valid_property_types:
        errors.append(f"Invalid property type. Must be one of: {', '.join(valid_property_types)}")
    
    if errors:
        print(f"[Property Checklist] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract and normalize data
    property_address = input_data["property_address"].strip()
    property_type = input_data["property_type"]
    developer_name = input_data["developer_name"].strip()
    unit_number = input_data.get("unit_number", "")
    square_feet = float(input_data.get("square_feet", 0))
    completion_certificate = input_data.get("completion_certificate", "not_applicable")
    strata_title = input_data.get("strata_title", False)
    individual_title = input_data.get("individual_title", False)
    first_owner = input_data.get("first_owner", "")
    first_owner_ic = input_data.get("first_owner_ic", "")
    registration_date = input_data.get("registration_date", "")
    subsale_evidence = input_data.get("subsale_evidence", "")
    valuation_report = input_data.get("valuation_report", False)
    valuation_amount = float(input_data.get("valuation_amount", 0))
    
    print(f"[Property Checklist] Processing property: {property_address}")
    print(f"[Property Checklist] Type: {property_type}, Developer: {developer_name}")
    
    # Classify property
    classification = classify_property(input_data)
    print(f"[Property Checklist] Classification: {classification}")
    
    # Determine title status
    title_status = "unknown"
    if strata_title:
        title_status = "strata_title"
    elif individual_title:
        title_status = "individual_title"
    
    # Determine completion status
    completion_status = completion_certificate if completion_certificate != "not_applicable" else "n/a"
    
    # Determine valuation status
    valuation_status = "available" if valuation_report else "pending"
    if valuation_report and valuation_amount > 0:
        valuation_status = f"available_rm_{valuation_amount}"
    
    # Determine required documents
    required_docs = determine_required_documents(classification, property_type, completion_status)
    print(f"[Property Checklist] Required documents: {len(required_docs)} items")
    
    # Build normalized data
    normalized_data = {
        "property_address": property_address,
        "property_type": property_type,
        "classification": classification,
        "developer_name": developer_name,
        "unit_number": unit_number,
        "square_feet": square_feet,
        "title_status": title_status,
        "completion_status": completion_status,
        "valuation_status": valuation_status,
        "valuation_amount": valuation_amount if valuation_amount > 0 else None,
        "required_documents": required_docs,
        "property_form_fields": {
            "form_type": "PROPERTY_CHECKLIST",
            "property_details": {
                "address": property_address,
                "type": property_type,
                "unit_number": unit_number,
                "size_sqft": square_feet,
                "developer": developer_name
            },
            "classification": {
                "type": classification,
                "determined_at": datetime.now().isoformat()
            },
            "title_details": {
                "strata_title": strata_title,
                "individual_title": individual_title,
                "status": title_status
            },
            "completion_details": {
                "certificate": completion_certificate,
                "status": completion_status
            },
            "ownership_details": {
                "first_owner": first_owner,
                "first_owner_ic": first_owner_ic,
                "registration_date": registration_date
            },
            "valuation_details": {
                "report_available": valuation_report,
                "amount": valuation_amount if valuation_amount > 0 else None,
                "status": valuation_status
            },
            "subsale_evidence": subsale_evidence if subsale_evidence else None,
            "required_documents": required_docs,
            "processed_at": datetime.now().isoformat()
        }
    }
    
    # Build proposal payload for Proposal Engine
    proposal_payload = {
        "tool": "property_checklist",
        "vertical": "mortgage-lppsa",
        "timestamp": datetime.now().isoformat(),
        "property_id": property_address,
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": []
    }
    
    print(f"[Property Checklist] Processing completed successfully")
    print(f"[Property Checklist] Classification: {classification}, Documents: {len(required_docs)}")
    
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
        
        # Process the checklist
        result = handle_property_checklist(input_data)
        
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

