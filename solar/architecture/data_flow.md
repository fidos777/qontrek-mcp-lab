# Solar MCP - Data Flow Documentation

## Overview

This document describes the data flow through the Solar MCP Toolpack, from lead intake to quotation generation.

## Flow Diagram

```
┌──────────────┐
│ Lead Intake  │ → Priority Score, System Size Estimate
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Site         │ → Roof Angle, Usable Area, Shading Score
│ Inspection   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ ROI          │ → System Size, Savings, Payback Period
│ Calculation  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Roof Check   │ → Roof Type, Mounting Type, Suitability
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Quotation    │ → Components, Pricing, Brandpack Theme
└──────────────┘
```

## Detailed Flow by Tool

### 1. Lead Intake Flow

**Input**:
```json
{
  "customer_name": "Ahmad bin Abdullah",
  "email": "ahmad@example.com",
  "phone": "+60123456789",
  "address": "No. 123, Jalan Test",
  "property_type": "residential",
  "monthly_bill": 500
}
```

**Processing Steps**:
1. Validate email and phone format
2. Calculate priority score (0-100)
3. Determine if high priority (score >= 50)
4. Estimate system size based on monthly bill
5. Classify property type

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "priority_score": 45,
    "is_high_priority": false,
    "estimated_system_size_kw": 3.0
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "next_steps": ["site_inspection", "roi", "roof_check"]
  }
}
```

### 2. Site Inspection Flow

**Input**:
```json
{
  "address": "No. 123, Jalan Test",
  "inspection_date": "2024-01-15",
  "roof_measurements": {
    "usable_area_sqm": 80,
    "angle_degrees": 15
  },
  "shading_obstacles": [...]
}
```

**Processing Steps**:
1. Validate inspection date
2. Estimate roof angle (from measurements or default)
3. Calculate usable area (accounting for shading)
4. Calculate shading score (0-100)
5. Estimate system capacity

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "roof_angle_degrees": 15,
    "usable_area_sqm": 80,
    "shading_score": 95,
    "estimated_system_capacity_kw": 13.3
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "next_steps": ["roi", "roof_check", "quotation"]
  }
}
```

### 3. ROI Calculation Flow

**Input**:
```json
{
  "monthly_bill": 500,
  "property_type": "residential",
  "system_size_kw": 5.0,
  "panel_efficiency": 0.2,
  "sunlight_hours_per_day": 4.5
}
```

**Processing Steps**:
1. Calculate system size (if not provided)
2. Calculate annual generation (kWh)
3. Calculate annual savings
4. Calculate upfront cost
5. Calculate payback period
6. Calculate lifetime savings
7. Build assumptions block

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "system_size_kw": 5.0,
    "annual_savings": 2400,
    "payback_period_years": 9.4,
    "upfront_cost": 22500,
    "lifetime_savings": 60000,
    "assumptions": {...}
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "next_steps": ["quotation"]
  }
}
```

### 4. Roof Check Flow

**Input**:
```json
{
  "roof_type": "metal",
  "roof_condition": "good",
  "roof_angle_degrees": 20
}
```

**Processing Steps**:
1. Validate roof type
2. Determine mounting type based on roof characteristics
3. Check roof suitability
4. Generate recommendations

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "roof_type": "metal",
    "mounting_type": "rail_mount",
    "is_suitable": true,
    "recommendations": ["Roof is suitable for solar installation"]
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "next_steps": ["quotation"]
  }
}
```

### 5. Quotation Flow

**Input**:
```json
{
  "customer_name": "Ahmad bin Abdullah",
  "address": "No. 123, Jalan Test",
  "system_size_kw": 5.0,
  "package_type": "standard",
  "roi_data": {...},
  "brandpack_id": "default"
}
```

**Processing Steps**:
1. Generate quotation number
2. Load brandpack from `brandpacks/_template/`
3. Get components based on package type
4. Calculate total cost
5. Build ROI summary
6. Apply brandpack theme
7. Generate validity date

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "quotation_number": "SOL-20240115123456",
    "total_cost": 22500,
    "components": [...],
    "brandpack_applied": "default"
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "branding": {
      "brandpack": {
        "colors": {...},
        "style": "modern"
      }
    }
  }
}
```

## End-to-End Flow

### Complete Solar Application

```
Step 1: Lead Intake
  → Customer qualified
  → Priority score calculated
  → System size estimated
  → Next: Site Inspection, ROI, Roof Check

Step 2: Site Inspection
  → Roof analyzed
  → Capacity estimated
  → Next: ROI, Roof Check, Quotation

Step 3: ROI Calculation
  → Financial metrics calculated
  → Payback period determined
  → Next: Quotation

Step 4: Roof Check
  → Roof classified
  → Mounting type determined
  → Next: Quotation

Step 5: Quotation
  → Components listed
  → Pricing calculated
  → Brandpack applied
  → Next: None (ready for proposal)
```

## FireCrawl Brandpack Integration

### Brandpack Loading
1. Handler checks for `brandpack_id` in input
2. Attempts to load from `brandpacks/_template/{brandpack_id}.json`
3. Falls back to default brandpack if not found
4. Applies colors, fonts, and style to proposal payload

### Brandpack Structure
```json
{
  "id": "voltek",
  "colors": {
    "primary": "#0066CC",
    "secondary": "#00AA44",
    "accent": "#FF6600"
  },
  "fonts": {
    "heading": "Arial, sans-serif",
    "body": "Arial, sans-serif"
  },
  "style": "modern"
}
```

## Error Handling Flow

```
Input → Validation → Error?
                    ├─ Yes → Return error response
                    └─ No → Processing → Error?
                                      ├─ Yes → Return error response
                                      └─ No → Return success response
```

**Error Response Format**:
```json
{
  "status": "error",
  "errors": ["Error message 1", "Error message 2"],
  "normalized_data": null,
  "proposal_payload": null
}
```

## Proposal Payload Structure

All handlers output a standardized `proposal_payload`:

```json
{
  "tool": "tool_name",
  "vertical": "solar",
  "timestamp": "2024-01-15T10:30:00",
  "customer_id": "customer@example.com",
  "data": { /* normalized_data */ },
  "status": "ready_for_proposal",
  "next_steps": ["next_tool_1", "next_tool_2"],
  "metadata": { /* tool-specific metadata */ },
  "branding": { /* brandpack data for quotation */ }
}
```

This structure ensures compatibility with the Proposal Engine and Document Factory.

