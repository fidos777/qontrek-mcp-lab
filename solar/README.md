# Solar MCP Toolpack

**Version**: 0.1.0  
**Vertical**: solar  
**Owner**: Qontrek

## Overview

The Solar MCP Toolpack provides a complete set of tools for processing solar lead intake, site inspection, ROI calculation, roof assessment, and quotation generation. It integrates with FireCrawl brandpacks for document theming and is compatible with the Proposal Engine and Document Factory.

## Quick Start

### Test a Handler

```bash
# Test Lead Intake
echo '{
  "customer_name": "Ahmad bin Abdullah",
  "email": "ahmad@example.com",
  "phone": "+60123456789",
  "address": "No. 123, Jalan Test, Kuala Lumpur",
  "property_type": "residential",
  "monthly_bill": 500
}' | python3 solar/handlers/handle_lead_intake.py

# Test Site Inspection
echo '{
  "address": "No. 123, Jalan Test, Kuala Lumpur",
  "inspection_date": "2024-01-15",
  "roof_measurements": {
    "usable_area_sqm": 80,
    "angle_degrees": 15
  }
}' | python3 solar/handlers/handle_site_inspection.py

# Test ROI Calculation
echo '{
  "monthly_bill": 500,
  "property_type": "residential",
  "system_size_kw": 5.0
}' | python3 solar/handlers/handle_roi.py

# Test Roof Check
echo '{
  "roof_type": "metal",
  "roof_condition": "good"
}' | python3 solar/handlers/handle_roof_check.py

# Test Quotation
echo '{
  "customer_name": "Ahmad bin Abdullah",
  "address": "No. 123, Jalan Test, Kuala Lumpur",
  "system_size_kw": 5.0,
  "package_type": "standard",
  "roi_data": {
    "upfront_cost": 22500,
    "annual_savings": 2400
  }
}' | python3 solar/handlers/handle_quotation.py
```

## Tools

### 1. lead_intake
Parses customer information and flags high-priority leads.

**Features**:
- Email and phone validation
- Priority score calculation (0-100)
- System size estimation
- Property type classification

### 2. site_inspection
Processes site inspection data including images and measurements.

**Features**:
- Roof angle estimation
- Usable area calculation
- Shading score calculation
- System capacity estimation

### 3. roi
Calculates solar ROI including financial metrics.

**Features**:
- System size calculation
- Annual savings calculation
- Payback period calculation
- Lifetime savings calculation
- Assumptions block

### 4. roof_check
Classifies roof type and determines mounting type.

**Features**:
- Roof type classification
- Mounting type determination
- Suitability assessment
- Recommendations generation

### 5. quotation
Generates quotation with brandpack theming.

**Features**:
- Component listing
- Pricing calculation
- FireCrawl brandpack integration
- ROI summary embedding

## File Structure

```
solar/
├── manifests/
│   └── solar_mcp_manifest.json    # MCP manifest (B1.3)
├── schemas/
│   ├── lead_intake.schema.json
│   ├── site_inspection.schema.json
│   ├── roi.schema.json
│   ├── roof_check.schema.json
│   └── quotation.schema.json
├── tools/
│   ├── lead_intake.json
│   ├── site_inspection.json
│   ├── roi.json
│   ├── roof_check.json
│   └── quotation.json
├── handlers/
│   ├── handle_lead_intake.py
│   ├── handle_site_inspection.py
│   ├── handle_roi.py
│   ├── handle_roof_check.py
│   └── handle_quotation.py
├── test/
│   └── test_solar_mcp.json       # Test suite (B1.6)
├── architecture/
│   ├── overview.md
│   ├── data_flow.md
│   └── dependencies.md
└── README.md
```

## Requirements

- Python 3.8 or higher
- No external dependencies (uses Python standard library only)

## Proposal Engine Integration

All handlers output a `proposal_payload` compatible with the Proposal Engine:

```json
{
  "status": "ready_for_proposal",
  "proposal_payload": {
    "tool": "tool_name",
    "vertical": "solar",
    "timestamp": "2024-01-15T10:30:00",
    "customer_id": "customer@example.com",
    "data": { /* normalized_data */ },
    "next_steps": ["next_tool_1", "next_tool_2"]
  }
}
```

## FireCrawl Brandpack Integration

The quotation handler supports FireCrawl brandpacks:

1. Loads brandpack from `brandpacks/_template/{brandpack_id}.json`
2. Applies colors, fonts, and style to proposal payload
3. Falls back to default brandpack if not found

## Testing

See `test/test_solar_mcp.json` for the complete test suite including:
- Individual tool tests
- Calculation validation tests
- Error handling tests
- End-to-end workflow tests

## Documentation

- **Architecture Overview**: `architecture/overview.md`
- **Data Flow**: `architecture/data_flow.md`
- **Dependencies**: `architecture/dependencies.md`

## Implementation Status

✅ **B1.3** - Solar MCP Manifest created  
✅ **B1.4** - Solar Tool Handlers implemented  
✅ **B1.5** - Proposal Engine integration ready  
✅ **B1.6** - Test suite created

## License

Copyright © 2024 Qontrek. All rights reserved.

