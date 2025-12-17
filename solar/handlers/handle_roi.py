#!/usr/bin/env python3
"""
Solar ROI Handler
Calculates solar ROI including system size, annual savings, payback period, and upfront cost.
"""

import json
import sys
from datetime import datetime

def calculate_system_size(monthly_bill, roof_area_sqm, system_size_kw_input, 
                         panel_efficiency, sunlight_hours, electricity_rate):
    """
    Calculate optimal system size based on bill or roof area.
    """
    if system_size_kw_input and system_size_kw_input > 0:
        return system_size_kw_input
    
    # Calculate from monthly bill
    monthly_kwh = monthly_bill / electricity_rate
    daily_kwh = monthly_kwh / 30
    system_size_kw = daily_kwh / sunlight_hours
    
    # If roof area provided, check if it can accommodate
    if roof_area_sqm and roof_area_sqm > 0:
        max_capacity_from_roof = roof_area_sqm / 6.0  # ~6 sqm per kW
        system_size_kw = min(system_size_kw, max_capacity_from_roof)
    
    # Round to nearest 0.5 kW
    system_size_kw = round(system_size_kw * 2) / 2
    
    # Minimum 3kW
    return max(3.0, system_size_kw)

def calculate_annual_generation(system_size_kw, sunlight_hours, panel_efficiency):
    """
    Calculate annual energy generation in kWh.
    """
    daily_generation = system_size_kw * sunlight_hours * panel_efficiency
    annual_generation = daily_generation * 365
    return round(annual_generation, 2)

def calculate_annual_savings(annual_generation, electricity_rate, monthly_bill):
    """
    Calculate annual savings.
    Assumes 80% self-consumption, 20% exported to grid.
    """
    # Self-consumption savings (at full rate)
    self_consumption = annual_generation * 0.8
    self_consumption_savings = self_consumption * electricity_rate
    
    # Export savings (at feed-in tariff rate, typically 0.21 MYR/kWh)
    export = annual_generation * 0.2
    feed_in_tariff = 0.21
    export_savings = export * feed_in_tariff
    
    total_savings = self_consumption_savings + export_savings
    
    # Cap savings at annual bill amount
    annual_bill = monthly_bill * 12
    total_savings = min(total_savings, annual_bill)
    
    return round(total_savings, 2)

def calculate_upfront_cost(system_size_kw, system_cost_per_watt):
    """
    Calculate upfront system cost.
    """
    cost = system_size_kw * 1000 * system_cost_per_watt  # Convert kW to watts
    return round(cost, 2)

def calculate_payback_period(upfront_cost, annual_savings):
    """
    Calculate payback period in years.
    """
    if annual_savings <= 0:
        return None
    payback = upfront_cost / annual_savings
    return round(payback, 2)

def calculate_lifetime_savings(annual_savings, system_lifetime_years=25):
    """
    Calculate lifetime savings over system lifetime.
    """
    lifetime_savings = annual_savings * system_lifetime_years
    return round(lifetime_savings, 2)

def handle_roi(input_data):
    """
    Process ROI calculation.
    
    Args:
        input_data: Dictionary containing ROI calculation inputs
        
    Returns:
        Dictionary with normalized data and proposal payload
    """
    print("[ROI] Starting calculation...")
    print(f"[ROI] Input data received: {json.dumps(input_data, indent=2)}")
    
    errors = []
    
    # Validate required fields
    required_fields = ["monthly_bill", "property_type"]
    for field in required_fields:
        if field not in input_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        print(f"[ROI] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Validate monthly bill
    if input_data["monthly_bill"] <= 0:
        errors.append("Monthly bill must be greater than 0")
    
    # Validate property type
    valid_property_types = ["residential", "commercial", "industrial"]
    if input_data["property_type"] not in valid_property_types:
        errors.append(f"Invalid property type. Must be one of: {', '.join(valid_property_types)}")
    
    if errors:
        print(f"[ROI] Validation errors: {errors}")
        return {
            "status": "error",
            "errors": errors,
            "normalized_data": None,
            "proposal_payload": None
        }
    
    # Extract inputs with defaults
    monthly_bill = float(input_data["monthly_bill"])
    property_type = input_data["property_type"]
    roof_area_sqm = float(input_data.get("roof_area_sqm", 0))
    system_size_kw_input = float(input_data.get("system_size_kw", 0))
    panel_efficiency = float(input_data.get("panel_efficiency", 0.2))
    sunlight_hours = float(input_data.get("sunlight_hours_per_day", 4.5))
    electricity_rate = float(input_data.get("electricity_rate_per_kwh", 0.40))
    system_cost_per_watt = float(input_data.get("system_cost_per_watt", 4.5))
    maintenance_percentage = float(input_data.get("maintenance_cost_percentage", 0.01))
    inverter_warranty = int(input_data.get("inverter_warranty_years", 10))
    panel_warranty = int(input_data.get("panel_warranty_years", 25))
    
    print(f"[ROI] Monthly bill: RM {monthly_bill}, Property type: {property_type}")
    
    # Calculate system size
    system_size_kw = calculate_system_size(
        monthly_bill, roof_area_sqm, system_size_kw_input,
        panel_efficiency, sunlight_hours, electricity_rate
    )
    print(f"[ROI] System size: {system_size_kw} kW")
    
    # Calculate annual generation
    annual_generation = calculate_annual_generation(system_size_kw, sunlight_hours, panel_efficiency)
    print(f"[ROI] Annual generation: {annual_generation} kWh")
    
    # Calculate annual savings
    annual_savings = calculate_annual_savings(annual_generation, electricity_rate, monthly_bill)
    print(f"[ROI] Annual savings: RM {annual_savings}")
    
    # Calculate upfront cost
    upfront_cost = calculate_upfront_cost(system_size_kw, system_cost_per_watt)
    print(f"[ROI] Upfront cost: RM {upfront_cost}")
    
    # Calculate payback period
    payback_period = calculate_payback_period(upfront_cost, annual_savings)
    print(f"[ROI] Payback period: {payback_period} years" if payback_period else "[ROI] Payback period: N/A")
    
    # Calculate lifetime savings
    lifetime_savings = calculate_lifetime_savings(annual_savings)
    print(f"[ROI] Lifetime savings: RM {lifetime_savings}")
    
    # Build assumptions block
    assumptions = {
        "panel_efficiency": panel_efficiency,
        "sunlight_hours_per_day": sunlight_hours,
        "electricity_rate_per_kwh": electricity_rate,
        "system_cost_per_watt": system_cost_per_watt,
        "self_consumption_rate": 0.8,
        "export_rate": 0.2,
        "feed_in_tariff_per_kwh": 0.21,
        "maintenance_cost_percentage": maintenance_percentage,
        "system_lifetime_years": 25,
        "inverter_warranty_years": inverter_warranty,
        "panel_warranty_years": panel_warranty
    }
    
    # Build normalized data
    normalized_data = {
        "system_size_kw": system_size_kw,
        "annual_generation_kwh": annual_generation,
        "annual_savings": annual_savings,
        "payback_period_years": payback_period,
        "upfront_cost": upfront_cost,
        "lifetime_savings": lifetime_savings,
        "assumptions": assumptions,
        "roi_form_fields": {
            "form_type": "SOLAR_ROI_CALCULATION",
            "system_specs": {
                "size_kw": system_size_kw,
                "annual_generation_kwh": annual_generation
            },
            "financial_summary": {
                "upfront_cost": upfront_cost,
                "annual_savings": annual_savings,
                "payback_period_years": payback_period,
                "lifetime_savings": lifetime_savings
            },
            "assumptions": assumptions,
            "calculated_at": datetime.now().isoformat()
        }
    }
    
    # Build proposal payload for Proposal Engine
    proposal_payload = {
        "tool": "roi",
        "vertical": "solar",
        "timestamp": datetime.now().isoformat(),
        "data": normalized_data,
        "status": "ready_for_proposal",
        "next_steps": [
            "quotation"
        ],
        "metadata": {
            "system_size_kw": system_size_kw,
            "payback_years": payback_period
        }
    }
    
    print(f"[ROI] Calculation completed successfully")
    
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
        
        # Process the ROI calculation
        result = handle_roi(input_data)
        
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

