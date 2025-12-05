# Solar MCP Toolpack Data Flows

## Overview

This document provides detailed data flow specifications for the Solar MCP Toolpack, including complete JSON input/output examples for each stage of the Lead → Site → ROI → Quote pipeline.

---

## Primary Data Flow: Lead to Quote

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                            LEAD-TO-QUOTE DATA FLOW                                    │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│   ┌─────────────┐        ┌─────────────┐        ┌─────────────┐        ┌───────────┐ │
│   │ LEAD_INTAKE │───────▶│    SITE_    │───────▶│    ROI_     │───────▶│ QUOTATION │ │
│   │             │        │ INSPECTION  │        │ CALCULATOR  │        │  BUILDER  │ │
│   └──────┬──────┘        └──────┬──────┘        └──────┬──────┘        └─────┬─────┘ │
│          │                      │                      │                     │       │
│          │                      │                      │                     │       │
│          ▼                      ▼                      ▼                     ▼       │
│   ┌─────────────┐        ┌─────────────┐        ┌─────────────┐        ┌───────────┐ │
│   │  lead_id    │        │inspection_id│        │   roi_id    │        │quotation_id│ │
│   │  lead_score │        │ usable_area │        │annual_savings│       │quote_number│ │
│   │  qual_status│        │ system_size │        │payback_years│        │ doc_urls  │ │
│   │ est_system  │        │ efficiency  │        │ projections │        │total_amount│ │
│   └─────────────┘        └─────────────┘        └─────────────┘        └───────────┘ │
│                                                                                       │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Stage 1: Lead Intake

### JSON Input Example

```json
{
  "customer_name": "Ahmad bin Abdullah",
  "address": "123 Jalan Maju, Taman Bahagia, 47810 Petaling Jaya, Selangor",
  "contact_phone": "+60123456789",
  "contact_email": "ahmad.abdullah@email.com",
  "whatsapp_number": "+60123456789",
  "property_type": "residential",
  "property_subtype": "terrace",
  "monthly_electricity_bill_myr": 650,
  "average_monthly_consumption_kwh": 1140,
  "budget_range": "30000_to_50000",
  "timeline": "within_3_months",
  "source": "facebook",
  "ownership_status": "owner",
  "preferred_contact_method": "whatsapp",
  "preferred_contact_time": "evening",
  "notes": "Interested in reducing electricity bills. Has 2-story terrace house with flat concrete roof."
}
```

### JSON Output Example

```json
{
  "lead_id": "550e8400-e29b-41d4-a716-446655440000",
  "lead_score": 78,
  "qualification_status": "hot",
  "score_breakdown": {
    "budget_score": 20,
    "timeline_score": 22,
    "property_score": 18,
    "engagement_score": 18
  },
  "estimated_system_size_kwp": 10.5,
  "estimated_monthly_savings_myr": 370,
  "assigned_agent": {
    "agent_id": "agt-001",
    "agent_name": "Sarah Tan",
    "agent_phone": "+60198765432"
  },
  "recommended_next_action": "Schedule site inspection within 48 hours",
  "can_trigger_site_inspection": true,
  "status": "new",
  "created_at": "2025-12-05T09:00:00Z"
}
```

---

## Stage 2: Site Inspection

### JSON Input Example

```json
{
  "lead_id": "550e8400-e29b-41d4-a716-446655440000",
  "roof_type": "concrete_flat",
  "roof_area_sqm": 85.5,
  "roof_orientation": "south",
  "roof_tilt_degrees": 5,
  "usable_area_sqm": 72.0,
  "shading_analysis": {
    "shading_factor": 0.12,
    "shading_sources": ["tree", "water_tank"],
    "morning_shade_hours": 1.5,
    "afternoon_shade_hours": 0
  },
  "panel_layout": {
    "rows": 4,
    "columns": 8,
    "total_panels": 32,
    "panel_model": "JA Solar JAM72S30-550/MR",
    "panel_wattage": 550,
    "layout_diagram_url": "https://storage.supabase.co/layouts/550e8400-layout.png"
  },
  "electrical_assessment": {
    "meter_type": "single_phase",
    "meter_rating_amps": 60,
    "meter_location": "front_of_house",
    "cable_run_distance_m": 15,
    "earthing_status": "adequate"
  },
  "structural_assessment": {
    "roof_condition": "good",
    "roof_age_years": 8,
    "load_bearing_adequate": true,
    "waterproofing_status": "intact"
  },
  "images": [
    {
      "url": "https://storage.supabase.co/inspections/550e8400-roof-overview.jpg",
      "image_type": "roof_overview",
      "description": "Aerial view of flat concrete roof"
    },
    {
      "url": "https://storage.supabase.co/inspections/550e8400-meter.jpg",
      "image_type": "meter",
      "description": "TNB single-phase meter, 60A rating"
    },
    {
      "url": "https://storage.supabase.co/inspections/550e8400-shading.jpg",
      "image_type": "shading_source",
      "description": "Tree causing partial morning shade"
    }
  ],
  "gps_coordinates": {
    "latitude": 3.1234,
    "longitude": 101.6789
  },
  "inspector_notes": "Good installation site. Minor shading from neighbor's tree in morning. Recommend trimming if possible. Roof access via internal staircase. Customer cooperative."
}
```

### JSON Output Example

```json
{
  "inspection_id": "660e8400-e29b-41d4-a716-446655440001",
  "lead_id": "550e8400-e29b-41d4-a716-446655440000",
  "usable_roof_area_sqm": 72.0,
  "recommended_system_size_kwp": 17.6,
  "recommended_panels": 32,
  "panel_layout": {
    "rows": 4,
    "columns": 8,
    "total_panels": 32,
    "panel_model": "JA Solar JAM72S30-550/MR",
    "panel_wattage": 550
  },
  "efficiency_factors": {
    "orientation_factor": 0.95,
    "tilt_factor": 0.98,
    "shading_factor": 0.88,
    "combined_efficiency": 0.82
  },
  "estimated_annual_generation_kwh": 23056,
  "installation_complexity": "simple",
  "complexity_factors": [],
  "special_requirements": [
    "Install conduit along external wall",
    "Consider tree trimming for optimal performance"
  ],
  "estimated_installation_days": 3,
  "inspector_id": "insp-001",
  "inspection_date": "2025-12-05",
  "inspection_duration_minutes": 90,
  "weather_conditions": "sunny",
  "next_step": "roi_calculator",
  "created_at": "2025-12-05T11:30:00Z"
}
```

---

## Stage 3: ROI Calculator

### JSON Input Example

```json
{
  "site_inspection_id": "660e8400-e29b-41d4-a716-446655440001",
  "system_size_kwp": 17.6,
  "monthly_bill_myr": 650,
  "tariff_rate_myr_kwh": 0.57,
  "installation_cost_per_kwp": 3800,
  "annual_degradation_rate": 0.005,
  "projection_years": 25,
  "discount_rate": 0.06,
  "electricity_price_escalation": 0.04,
  "self_consumption_ratio": 0.75,
  "nem_export_rate_myr_kwh": 0.31,
  "shading_factor": 0.12,
  "orientation_factor": 0.95,
  "location_factors": {
    "region": "central",
    "annual_irradiance_kwh_m2": 1650,
    "performance_ratio": 0.80
  },
  "financing_options": {
    "payment_method": "loan",
    "loan_amount_myr": 66880,
    "loan_term_years": 7,
    "interest_rate": 0.045,
    "down_payment_myr": 10000
  },
  "incentives": {
    "government_rebate_myr": 0,
    "tax_incentive_percentage": 0,
    "green_financing_rate_reduction": 0.005
  }
}
```

### JSON Output Example

```json
{
  "roi_id": "770e8400-e29b-41d4-a716-446655440002",
  "site_inspection_id": "660e8400-e29b-41d4-a716-446655440001",
  "lead_id": "550e8400-e29b-41d4-a716-446655440000",
  "system_specifications": {
    "system_size_kwp": 17.6,
    "estimated_panels": 32,
    "panel_wattage": 550,
    "annual_generation_kwh": 23056,
    "specific_yield_kwh_kwp": 1310
  },
  "financial_summary": {
    "total_cost_myr": 66880,
    "first_year_savings_myr": 9862,
    "annual_savings_myr": 9862,
    "lifetime_savings_myr": 425340,
    "simple_payback_years": 6.8,
    "discounted_payback_years": 8.2,
    "npv_myr": 89450,
    "irr_percentage": 15.2,
    "roi_percentage": 536,
    "lcoe_myr_kwh": 0.116
  },
  "monthly_impact": {
    "current_bill_myr": 650,
    "estimated_new_bill_myr": 162,
    "monthly_savings_myr": 488,
    "loan_payment_myr": 920
  },
  "environmental_impact": {
    "carbon_offset_tonnes_year": 15.8,
    "lifetime_carbon_offset_tonnes": 356,
    "trees_equivalent": 732
  },
  "year_by_year_projection": [
    {
      "year": 1,
      "generation_kwh": 23056,
      "self_consumed_kwh": 17292,
      "exported_kwh": 5764,
      "self_consumption_savings_myr": 9856,
      "export_income_myr": 1787,
      "total_benefit_myr": 11643,
      "maintenance_cost_myr": 500,
      "net_benefit_myr": 11143,
      "cumulative_benefit_myr": 11143,
      "loan_payment_myr": 11040,
      "net_cash_flow_myr": 103
    },
    {
      "year": 2,
      "generation_kwh": 22941,
      "self_consumed_kwh": 17206,
      "exported_kwh": 5735,
      "self_consumption_savings_myr": 10203,
      "export_income_myr": 1778,
      "total_benefit_myr": 11981,
      "maintenance_cost_myr": 500,
      "net_benefit_myr": 11481,
      "cumulative_benefit_myr": 22624,
      "loan_payment_myr": 11040,
      "net_cash_flow_myr": 441
    },
    {
      "year": 5,
      "generation_kwh": 22601,
      "self_consumed_kwh": 16951,
      "exported_kwh": 5650,
      "self_consumption_savings_myr": 11132,
      "export_income_myr": 1752,
      "total_benefit_myr": 12884,
      "maintenance_cost_myr": 500,
      "net_benefit_myr": 12384,
      "cumulative_benefit_myr": 58456,
      "loan_payment_myr": 11040,
      "net_cash_flow_myr": 1344
    },
    {
      "year": 10,
      "generation_kwh": 22044,
      "self_consumed_kwh": 16533,
      "exported_kwh": 5511,
      "self_consumption_savings_myr": 13012,
      "export_income_myr": 1708,
      "total_benefit_myr": 14720,
      "maintenance_cost_myr": 500,
      "net_benefit_myr": 14220,
      "cumulative_benefit_myr": 126890,
      "loan_payment_myr": 0,
      "net_cash_flow_myr": 14220
    },
    {
      "year": 25,
      "generation_kwh": 19491,
      "self_consumed_kwh": 14618,
      "exported_kwh": 4873,
      "self_consumption_savings_myr": 22156,
      "export_income_myr": 1511,
      "total_benefit_myr": 23667,
      "maintenance_cost_myr": 500,
      "net_benefit_myr": 23167,
      "cumulative_benefit_myr": 425340,
      "loan_payment_myr": 0,
      "net_cash_flow_myr": 23167
    }
  ],
  "sensitivity_analysis": {
    "scenarios": {
      "conservative": {
        "generation_factor": 0.85,
        "price_escalation": 0.02,
        "payback_years": 8.5,
        "lifetime_savings_myr": 312000
      },
      "base": {
        "generation_factor": 1.0,
        "price_escalation": 0.04,
        "payback_years": 6.8,
        "lifetime_savings_myr": 425340
      },
      "optimistic": {
        "generation_factor": 1.1,
        "price_escalation": 0.06,
        "payback_years": 5.6,
        "lifetime_savings_myr": 567000
      }
    },
    "breakeven_analysis": {
      "breakeven_tariff_rate": 0.23,
      "breakeven_generation_kwh": 9800,
      "breakeven_utilization_percentage": 43
    }
  },
  "assumptions": {
    "tariff_rate_myr_kwh": 0.57,
    "nem_export_rate_myr_kwh": 0.31,
    "installation_cost_per_kwp": 3800,
    "annual_degradation_rate": 0.005,
    "discount_rate": 0.06,
    "electricity_price_escalation": 0.04,
    "annual_maintenance_cost": 500,
    "inverter_replacement_year": 12,
    "inverter_replacement_cost": 8000,
    "system_lifetime_years": 25
  },
  "next_step": "quotation_builder",
  "created_at": "2025-12-05T12:00:00Z"
}
```

---

## Stage 4: Quotation Builder

### JSON Input Example

```json
{
  "roi_calculation_id": "770e8400-e29b-41d4-a716-446655440002",
  "output_formats": ["pdf", "docx"],
  "template_id": "standard",
  "include_sections": [
    "cover_page",
    "executive_summary",
    "system_overview",
    "technical_specs",
    "roi_analysis",
    "pricing_breakdown",
    "payment_schedule",
    "project_timeline",
    "warranty_info",
    "terms_conditions"
  ],
  "validity_days": 30,
  "custom_pricing": {
    "discount_percentage": 5,
    "discount_reason": "Early bird promotion - December 2025"
  },
  "branding": {
    "company_name": "SolarTech Malaysia Sdn Bhd",
    "logo_url": "https://storage.supabase.co/branding/solartech-logo.png",
    "primary_color": "#2563eb",
    "secondary_color": "#1e40af",
    "contact_email": "sales@solartech.my",
    "contact_phone": "+603-7890-1234",
    "website": "https://www.solartech.my"
  },
  "language": "en",
  "payment_schedule": {
    "milestones": [
      {
        "milestone": "deposit",
        "percentage": 30,
        "description": "Upon order confirmation"
      },
      {
        "milestone": "equipment_delivery",
        "percentage": 40,
        "description": "Upon delivery of equipment to site"
      },
      {
        "milestone": "completion",
        "percentage": 20,
        "description": "Upon installation completion"
      },
      {
        "milestone": "commissioning",
        "percentage": 10,
        "description": "Upon TNB approval and system commissioning"
      }
    ]
  },
  "special_conditions": [
    "Price valid for installations within Klang Valley only",
    "TNB NEM application to be handled by installer",
    "Standard installation assumes ground floor meter location"
  ]
}
```

### JSON Output Example

```json
{
  "quotation_id": "880e8400-e29b-41d4-a716-446655440003",
  "quote_number": "QT-2025-00042",
  "quote_version": 1,
  "roi_calculation_id": "770e8400-e29b-41d4-a716-446655440002",
  "lead_id": "550e8400-e29b-41d4-a716-446655440000",
  "customer_details": {
    "name": "Ahmad bin Abdullah",
    "address": "123 Jalan Maju, Taman Bahagia, 47810 Petaling Jaya, Selangor",
    "phone": "+60123456789",
    "email": "ahmad.abdullah@email.com"
  },
  "system_summary": {
    "system_size_kwp": 17.6,
    "panel_count": 32,
    "panel_brand": "JA Solar",
    "panel_model": "JAM72S30-550/MR",
    "panel_wattage": 550,
    "inverter_brand": "Huawei",
    "inverter_model": "SUN2000-17KTL-M2",
    "inverter_capacity_kw": 17
  },
  "pricing_summary": {
    "subtotal_myr": 70400,
    "discount_myr": 3520,
    "discount_percentage": 5,
    "discount_reason": "Early bird promotion - December 2025",
    "net_amount_myr": 66880,
    "tax_myr": 0,
    "total_amount_myr": 66880,
    "price_per_kwp_myr": 3800
  },
  "pricing_breakdown": {
    "line_items": [
      {
        "item_code": "PNL-001",
        "description": "JA Solar 550W Mono PERC Panel",
        "category": "panels",
        "quantity": 32,
        "unit": "pcs",
        "unit_price_myr": 950,
        "total_myr": 30400
      },
      {
        "item_code": "INV-001",
        "description": "Huawei SUN2000-17KTL-M2 Inverter",
        "category": "inverter",
        "quantity": 1,
        "unit": "unit",
        "unit_price_myr": 12000,
        "total_myr": 12000
      },
      {
        "item_code": "MNT-001",
        "description": "Aluminum Mounting System (Flat Roof)",
        "category": "mounting",
        "quantity": 1,
        "unit": "set",
        "unit_price_myr": 8000,
        "total_myr": 8000
      },
      {
        "item_code": "CAB-001",
        "description": "DC/AC Cables, Conduits & Accessories",
        "category": "electrical",
        "quantity": 1,
        "unit": "lot",
        "unit_price_myr": 5000,
        "total_myr": 5000
      },
      {
        "item_code": "INS-001",
        "description": "Professional Installation (3 days)",
        "category": "installation",
        "quantity": 1,
        "unit": "lot",
        "unit_price_myr": 12000,
        "total_myr": 12000
      },
      {
        "item_code": "TNB-001",
        "description": "TNB NEM Application & Commissioning",
        "category": "services",
        "quantity": 1,
        "unit": "lot",
        "unit_price_myr": 3000,
        "total_myr": 3000
      }
    ]
  },
  "roi_highlights": {
    "annual_generation_kwh": 23056,
    "annual_savings_myr": 9862,
    "payback_years": 6.8,
    "roi_percentage": 536,
    "lifetime_savings_myr": 425340,
    "carbon_offset_tonnes_year": 15.8
  },
  "payment_schedule": [
    {
      "milestone": "deposit",
      "percentage": 30,
      "amount_myr": 20064,
      "description": "Upon order confirmation"
    },
    {
      "milestone": "equipment_delivery",
      "percentage": 40,
      "amount_myr": 26752,
      "description": "Upon delivery of equipment to site"
    },
    {
      "milestone": "completion",
      "percentage": 20,
      "amount_myr": 13376,
      "description": "Upon installation completion"
    },
    {
      "milestone": "commissioning",
      "percentage": 10,
      "amount_myr": 6688,
      "description": "Upon TNB approval and system commissioning"
    }
  ],
  "project_timeline": {
    "estimated_start_date": "2025-12-20",
    "estimated_completion_days": 21,
    "milestones": [
      {
        "phase": "Order Confirmation & Deposit",
        "duration_days": 1,
        "start_day": 1
      },
      {
        "phase": "Equipment Procurement",
        "duration_days": 10,
        "start_day": 2
      },
      {
        "phase": "Site Preparation",
        "duration_days": 1,
        "start_day": 12
      },
      {
        "phase": "Installation",
        "duration_days": 3,
        "start_day": 13
      },
      {
        "phase": "Testing & Quality Check",
        "duration_days": 1,
        "start_day": 16
      },
      {
        "phase": "TNB Application & Approval",
        "duration_days": 5,
        "start_day": 17
      },
      {
        "phase": "Commissioning & Handover",
        "duration_days": 1,
        "start_day": 21
      }
    ]
  },
  "warranty_info": {
    "panel_product_warranty_years": 12,
    "panel_performance_warranty_years": 25,
    "panel_performance_guarantee": "87.4% output at year 25",
    "inverter_warranty_years": 10,
    "workmanship_warranty_years": 5,
    "mounting_warranty_years": 10
  },
  "validity": {
    "quote_date": "2025-12-05",
    "valid_until": "2026-01-04",
    "validity_days": 30
  },
  "document_urls": {
    "pdf": "https://storage.supabase.co/quotations/QT-2025-00042.pdf",
    "docx": "https://storage.supabase.co/quotations/QT-2025-00042.docx"
  },
  "shareable_link": "https://quotes.solartech.my/v/QT-2025-00042",
  "qontrek_job_id": "qdf-abc123xyz",
  "status": "generated",
  "next_steps": [
    "Review quotation with customer",
    "Address any questions or concerns",
    "Collect signed acceptance and deposit",
    "Schedule installation date"
  ],
  "created_at": "2025-12-05T12:30:00Z",
  "created_by": "agt-001"
}
```

---

## Data Transformation Details

### Lead Intake → Site Inspection

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                    LEAD INTAKE → SITE INSPECTION TRANSFORMATION                     │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  FROM lead_intake OUTPUT:              TO site_inspection INPUT:                    │
│  ─────────────────────────             ─────────────────────────                    │
│                                                                                     │
│  lead_id ─────────────────────────────▶ lead_id (direct reference)                 │
│                                                                                     │
│  address ─────────────────────────────▶ [GPS lookup for coordinates]               │
│                                                                                     │
│  estimated_system_size_kwp ───────────▶ [Guidance only, not binding]               │
│                                                                                     │
│  property_type ───────────────────────▶ [Informs roof_type expectations]           │
│                                                                                     │
│  MANUAL ENTRY REQUIRED:                                                             │
│  • roof_type (physical inspection)                                                  │
│  • roof_area_sqm (measured on-site)                                                 │
│  • roof_orientation (compass reading)                                               │
│  • shading_analysis (site observation)                                              │
│  • images[] (photos taken on-site)                                                  │
│  • electrical_assessment (meter inspection)                                         │
│  • structural_assessment (visual inspection)                                        │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### Site Inspection → ROI Calculator

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                   SITE INSPECTION → ROI CALCULATOR TRANSFORMATION                   │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  FROM site_inspection OUTPUT:          TO roi_calculator INPUT:                     │
│  ────────────────────────────          ────────────────────────                     │
│                                                                                     │
│  inspection_id ───────────────────────▶ site_inspection_id                          │
│                                                                                     │
│  recommended_system_size_kwp ─────────▶ system_size_kwp                             │
│                                                                                     │
│  efficiency_factors.shading_factor ───▶ shading_factor                              │
│                                                                                     │
│  efficiency_factors.orientation_factor▶ orientation_factor                          │
│                                                                                     │
│  efficiency_factors.tilt_factor ──────▶ [Incorporated into performance_ratio]       │
│                                                                                     │
│  gps_coordinates ─────────────────────▶ location_factors.region [derived]           │
│                                                                                     │
│  DEFAULTS APPLIED IF NOT PROVIDED:                                                  │
│  • tariff_rate_myr_kwh: 0.57                                                        │
│  • installation_cost_per_kwp: 3800                                                  │
│  • projection_years: 25                                                             │
│  • discount_rate: 0.06                                                              │
│  • annual_irradiance_kwh_m2: 1600                                                   │
│                                                                                     │
│  FROM LEAD (via inspection.lead_id):                                                │
│  • monthly_electricity_bill_myr                                                     │
│  • property_type → tariff_category lookup                                           │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### ROI Calculator → Quotation Builder

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                  ROI CALCULATOR → QUOTATION BUILDER TRANSFORMATION                  │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  FROM roi_calculator OUTPUT:           TO quotation_builder INPUT:                  │
│  ───────────────────────────           ───────────────────────────                  │
│                                                                                     │
│  roi_id ──────────────────────────────▶ roi_calculation_id [REQUIRED]               │
│                                                                                     │
│  AUTO-RETRIEVED VIA roi_id:                                                         │
│  • financial_summary.* ───────────────▶ pricing_summary, roi_highlights             │
│  • system_specifications.* ───────────▶ system_summary                              │
│  • year_by_year_projection ───────────▶ [Embedded in PDF charts]                    │
│  • sensitivity_analysis ──────────────▶ [Embedded in executive summary]             │
│                                                                                     │
│  AUTO-RETRIEVED VIA roi.lead_id:                                                    │
│  • customer_name ─────────────────────▶ customer_details.name                       │
│  • address ───────────────────────────▶ customer_details.address                    │
│  • contact_* ─────────────────────────▶ customer_details.*                          │
│                                                                                     │
│  DEFAULTS IF NOT PROVIDED:                                                          │
│  • output_formats: ["pdf"]                                                          │
│  • template_id: "standard"                                                          │
│  • validity_days: 30                                                                │
│  • language: "en"                                                                   │
│                                                                                     │
│  OPTIONAL OVERRIDES:                                                                │
│  • custom_pricing.discount_percentage                                               │
│  • custom_pricing.discount_reason                                                   │
│  • branding.* (company customization)                                               │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Database Storage Schema

### Entity Relationship Diagram

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                           ENTITY RELATIONSHIP DIAGRAM                               │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   ┌──────────────────┐                                                              │
│   │      agents      │                                                              │
│   │                  │                                                              │
│   │  id (PK)         │                                                              │
│   │  name            │                                                              │
│   │  email           │                                                              │
│   │  role            │                                                              │
│   │  org_id (FK)     │──────────────────────┐                                       │
│   └────────┬─────────┘                      │                                       │
│            │                                │                                       │
│            │ 1:N                            │ N:1                                   │
│            ▼                                ▼                                       │
│   ┌──────────────────┐              ┌──────────────────┐                           │
│   │      leads       │              │  organizations   │                           │
│   │                  │              │                  │                           │
│   │  id (PK)         │              │  id (PK)         │                           │
│   │  customer_name   │              │  company_name    │                           │
│   │  address         │              │  branding        │                           │
│   │  lead_score      │              │  settings        │                           │
│   │  assigned_agent  │              └──────────────────┘                           │
│   │  org_id (FK)     │                                                              │
│   └────────┬─────────┘                                                              │
│            │                                                                        │
│            │ 1:N                                                                    │
│            ▼                                                                        │
│   ┌──────────────────┐                                                              │
│   │ site_inspections │                                                              │
│   │                  │                                                              │
│   │  id (PK)         │                                                              │
│   │  lead_id (FK)    │◀────────────────────┐                                        │
│   │  roof_type       │                     │                                        │
│   │  efficiency      │                     │                                        │
│   │  system_size     │                     │                                        │
│   └────────┬─────────┘                     │                                        │
│            │                               │                                        │
│            │ 1:N                           │                                        │
│            ▼                               │                                        │
│   ┌──────────────────┐                     │                                        │
│   │ roi_calculations │                     │                                        │
│   │                  │                     │                                        │
│   │  id (PK)         │                     │                                        │
│   │  inspection_id   │                     │                                        │
│   │  lead_id (FK)    │─────────────────────┤                                        │
│   │  financial_sum   │                     │                                        │
│   │  projections     │                     │                                        │
│   └────────┬─────────┘                     │                                        │
│            │                               │                                        │
│            │ 1:N                           │                                        │
│            ▼                               │                                        │
│   ┌──────────────────┐                     │                                        │
│   │   quotations     │                     │                                        │
│   │                  │                     │                                        │
│   │  id (PK)         │                     │                                        │
│   │  roi_id (FK)     │                     │                                        │
│   │  lead_id (FK)    │─────────────────────┘                                        │
│   │  quote_number    │                                                              │
│   │  total_amount    │                                                              │
│   │  document_urls   │                                                              │
│   │  status          │                                                              │
│   └──────────────────┘                                                              │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Webhook Event Payloads

### lead.created

```json
{
  "event": "lead.created",
  "timestamp": "2025-12-05T09:00:00Z",
  "data": {
    "lead_id": "550e8400-e29b-41d4-a716-446655440000",
    "customer_name": "Ahmad bin Abdullah",
    "source": "facebook",
    "assigned_agent_id": "agt-001"
  }
}
```

### lead.qualified

```json
{
  "event": "lead.qualified",
  "timestamp": "2025-12-05T09:00:15Z",
  "data": {
    "lead_id": "550e8400-e29b-41d4-a716-446655440000",
    "qualification_status": "hot",
    "lead_score": 78,
    "recommended_action": "Schedule site inspection within 48 hours"
  }
}
```

### inspection.completed

```json
{
  "event": "inspection.completed",
  "timestamp": "2025-12-05T11:30:00Z",
  "data": {
    "inspection_id": "660e8400-e29b-41d4-a716-446655440001",
    "lead_id": "550e8400-e29b-41d4-a716-446655440000",
    "recommended_system_size_kwp": 17.6,
    "installation_complexity": "simple",
    "inspector_id": "insp-001"
  }
}
```

### quote.generated

```json
{
  "event": "quote.generated",
  "timestamp": "2025-12-05T12:30:00Z",
  "data": {
    "quotation_id": "880e8400-e29b-41d4-a716-446655440003",
    "quote_number": "QT-2025-00042",
    "lead_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount_myr": 66880,
    "valid_until": "2026-01-04",
    "document_urls": {
      "pdf": "https://storage.supabase.co/quotations/QT-2025-00042.pdf",
      "docx": "https://storage.supabase.co/quotations/QT-2025-00042.docx"
    },
    "shareable_link": "https://quotes.solartech.my/v/QT-2025-00042"
  }
}
```

### quote.viewed

```json
{
  "event": "quote.viewed",
  "timestamp": "2025-12-05T14:00:00Z",
  "data": {
    "quotation_id": "880e8400-e29b-41d4-a716-446655440003",
    "quote_number": "QT-2025-00042",
    "lead_id": "550e8400-e29b-41d4-a716-446655440000",
    "viewer_ip": "203.xxx.xxx.xxx",
    "time_on_page_seconds": 245,
    "sections_viewed": ["executive_summary", "pricing_breakdown", "roi_analysis"]
  }
}
```

### quote.accepted

```json
{
  "event": "quote.accepted",
  "timestamp": "2025-12-05T16:30:00Z",
  "data": {
    "quotation_id": "880e8400-e29b-41d4-a716-446655440003",
    "quote_number": "QT-2025-00042",
    "lead_id": "550e8400-e29b-41d4-a716-446655440000",
    "accepted_amount_myr": 66880,
    "deposit_due_myr": 20064,
    "estimated_installation_date": "2025-12-20"
  }
}
```

---

## Data Retention Policy

| Data Type | Retention Period | Archive Policy |
|-----------|-----------------|----------------|
| Active leads | Indefinite | N/A |
| Lost/disqualified leads | 2 years | Move to archive table |
| Site inspections | Indefinite | N/A |
| ROI calculations | Indefinite | N/A |
| Quotation records | Indefinite | N/A |
| Generated documents | 7 years | Move to cold storage |
| Inspection images | 5 years | Compress and archive |
| Webhook logs | 90 days | Delete |
| Audit logs | 3 years | Compress and archive |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2025-12-05 | Added comprehensive JSON examples for all stages |
| 1.0.0 | 2025-12-05 | Initial data flows documentation |
