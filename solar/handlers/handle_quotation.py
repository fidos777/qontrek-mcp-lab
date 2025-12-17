#!/usr/bin/env python3
"""
Solar Quotation Handler
Generates quotation JSON payload with package options, ROI model, and brandpack theme.
"""

import json
import sys
import os
from datetime import datetime, timedelta

def load_brandpack(brandpack_id):
    """
    Load brandpack from brandpacks/_template/ directory.
    Returns default brandpack if not found.
    """
    # Default brandpack structure
    default_brandpack = {
        "id": "default",
        "name": "Default Solar Brandpack",
        "colors": {
            "primary": "#0066CC",
            "secondary": "#00AA44",
            "accent": "#FF6600",
            "background": "#FFFFFF",
            "text": "#333333"
        },
        "logo": None,
        "fonts": {
            "heading": "Arial, sans-serif",
            "body": "Arial, sans-serif"
        },
        "style": "modern"
    }
    
    # Try to load from brandpacks directory
    if brandpack_id:
        brandpack_path = f"brandpacks/_template/{brandpack_id}.json"
        if os.path.exists(brandpack_path):
            try:
                with open(brandpack_path, 'r') as f:
                    loaded_brandpack = json.load(f)
                    print(f"[Quotation] Loaded brandpack: {brandpack_id}")
                    return loaded_brandpack
            except Exception as e:
                print(f"[Quotation] Error loading brandpack {brandpack_id}: {e}, using default")
    
    print(f"[Quotation] Using default brandpack")
    return default_brandpack

def generate_quotation_number():
    """Generate unique quotation number."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"SOL-{timestamp}"

def get_package_components(package_type, system_size_kw):
    """
    Get components based on package type and system size.
    """
    base_components = []
    
    # Calculate number of panels (assuming 400W panels)
    panel_wattage = 400
    num_panels = int((system_size_kw * 1000) / panel_wattage)
    
    # Panels
    base_components.append({
        "type": "panel",
        "brand": "SolarTech",
        "model": "ST-400W",
        "quantity": num_panels,
        "unit_price": 800,
        "total_price": num_panels * 800
    })
    
    # Inverter (one per system, or multiple for large systems)
    if system_size_kw <= 10:
        inverter_count = 1
        inverter_model = "ST-Inverter-5kW"
        inverter_price = 3500
    elif system_size_kw <= 20:
        inverter_count = 1
        inverter_model = "ST-Inverter-10kW"
        inverter_price = 6000
    else:
        inverter_count = int((system_size_kw / 10) + 0.5)
        inverter_model = "ST-Inverter-10kW"
        inverter_price = 6000
    
    base_components.append({
        "type": "inverter",
        "brand": "SolarTech",
        "model": inverter_model,
        "quantity": inverter_count,
        "unit_price": inverter_price,
        "total_price": inverter_count * inverter_price
    })
    
    # Mounting system
    mounting_price_per_kw = 500
    base_components.append({
        "type": "mounting",
        "brand": "SolarMount",
        "model": "SM-Rail-System",
        "quantity": 1,
        "unit_price": system_size_kw * mounting_price_per_kw,
        "total_price": system_size_kw * mounting_price_per_kw
    })
    
    # Monitoring system
    base_components.append({
        "type": "monitoring",
        "brand": "SolarMonitor",
        "model": "SM-Pro",
        "quantity": 1,
        "unit_price": 1500,
        "total_price": 1500
    })
    
    # Warranty
    warranty_years = 10
    if package_type == "premium":
        warranty_years = 25
    
    base_components.append({
        "type": "warranty",
        "brand": "SolarTech",
        "model": f"{warranty_years}-Year Warranty",
        "quantity": 1,
        "unit_price": 0,  # Included in package
        "total_price": 0
    })
    
    # Add premium components for premium package
    if package_type == "premium":
        base_components.append({
            "type": "monitoring",
            "brand": "SolarMonitor",
            "model": "SM-Premium",
            "quantity": 1,
            "unit_price": 500,
            "total_price": 500
        })
    
    return base_components

def calculate_total_cost(components):
    """Calculate total cost from components."""
    return sum(comp.get("total_price", 0) for comp in components)

def handle_quotation(input_data):
    """
    Process quotation generation.
    
    Args:
        input_data: Dictionary containing quotation information
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[Quotation] Starting generation...")
    print(f"[Quotation] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["customer_name", "address", "system_size_kw", "package_type"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[Quotation] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate system size
    if input_data["system_size_kw"] <= 0:
        errors.append("System size must be greater than 0")
    
    # Validate package type
    valid_package_types = ["basic", "standard", "premium", "custom"]
    if input_data["package_type"] not in valid_package_types:
        errors.append(f"Invalid package type. Must be one of: {', '.join(valid_package_types)}")
    
    if errors:
        print(f"[Quotation] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract inputs
    customer_name = input_data["customer_name"].strip()
    address = input_data["address"].strip()
    system_size_kw = float(input_data["system_size_kw"])
    package_type = input_data["package_type"]
    roi_data = input_data.get("roi_data", {})
    brandpack_id = input_data.get("brandpack_id", "default")
    validity_days = int(input_data.get("validity_days", 30))
    installation_timeline_weeks = int(input_data.get("installation_timeline_weeks", 4))
    warranty_years = int(input_data.get("warranty_years", 10))
    
    print(f"[Quotation] Generating quotation for: {customer_name}")
    print(f"[Quotation] System size: {system_size_kw} kW, Package: {package_type}")
    
    # Generate quotation number
    quotation_number = generate_quotation_number()
    print(f"[Quotation] Quotation number: {quotation_number}")
    
    # Load brandpack
    brandpack = load_brandpack(brandpack_id)
    
    # Get components
    components = get_package_components(package_type, system_size_kw)
    if input_data.get("components"):
        # Use provided components if available
        components = input_data["components"]
    
    # Calculate total cost
    total_cost = calculate_total_cost(components)
    print(f"[Quotation] Total cost: RM {total_cost}")
    
    # Build ROI summary
    roi_summary = {
        "upfront_cost": roi_data.get("upfront_cost", total_cost),
        "annual_savings": roi_data.get("annual_savings", 0),
        "payback_period_years": roi_data.get("payback_period_years", 0),
        "lifetime_savings": roi_data.get("lifetime_savings", 0)
    }
    
    # Calculate validity date
    validity_date = (datetime.now() + timedelta(days=validity_days)).strftime("%Y-%m-%d")
    
    # Build normalized data
    normalized_data = {
        "quotation_number": quotation_number,
        "customer_name": customer_name,
        "address": address,
        "system_size_kw": system_size_kw,
        "package_type": package_type,
        "total_cost": total_cost,
        "roi_summary": roi_summary,
        "components": components,
        "brandpack_applied": brandpack_id,
        "validity_date": validity_date,
        "installation_timeline_weeks": installation_timeline_weeks,
        "warranty_years": warranty_years,
        "quotation_form_fields": {
            "form_type": "SOLAR_QUOTATION",
            "quotation_details": {
                "number": quotation_number,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "validity_date": validity_date,
                "customer_name": customer_name,
                "address": address
            },
            "system_specs": {
                "size_kw": system_size_kw,
                "package_type": package_type,
                "warranty_years": warranty_years
            },
            "pricing": {
                "total_cost": total_cost,
                "components": components
            },
            "roi_summary": roi_summary,
            "timeline": {
                "installation_weeks": installation_timeline_weeks
            },
            "branding": {
                "brandpack_id": brandpack_id,
                "colors": brandpack.get("colors", {}),
                "style": brandpack.get("style", "modern")
            },
            "generated_at": datetime.now().isoformat()
        }
    }
    
    # Build proposal payload for Proposal Engine with brandpack
    proposal_payload = {
        "tool": "quotation",
        "vertical": "solar",
        "timestamp": datetime.now().isoformat(),
        "customer_id": customer_name,
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": [],
        "metadata": {
            "quotation_number": quotation_number,
            "total_cost": total_cost,
            "system_size_kw": system_size_kw
        },
        "branding": {
            "brandpack": brandpack,
            "applied_at": datetime.now().isoformat()
        },
        "version": "1.0"
    }
    
    print(f"[Quotation] Quotation generated successfully")
    print(f"[Quotation] Brandpack: {brandpack_id}, Total: RM {total_cost}")
    
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
        
        # Process the quotation
        result = handle_quotation(input_data)
        
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

