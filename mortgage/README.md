# Mortgage MCP Toolpack

**Version**: 0.1.0  
**Vertical**: mortgage-lppsa  
**Owner**: Qontrek

## Overview

The Mortgage MCP Toolpack provides a complete set of tools for processing mortgage applications with LPPSA (Low Price Public Sector Housing) integration. It handles customer intake, Takaful insurance submissions, lawyer intake, and property validation.

## Quick Start

### Test a Handler

```bash
# Test LPPSA Intake
echo '{
  "customer_name": "Ahmad bin Abdullah",
  "ic_number": "850101-01-0101",
  "income": 5000,
  "property_price": 250000,
  "loan_amount": 200000,
  "loan_tenure": 30
}' | python3 mortgage/handlers/handle_lppsa_intake.py

# Test Takaful Submission
echo '{
  "customer_ic": "850101-01-0101",
  "loan_amount": 200000,
  "property_value": 250000,
  "coverage_type": "mrta"
}' | python3 mortgage/handlers/handle_takaful_submission.py

# Test Lawyer Intake
echo '{
  "customer_ic": "850101-01-0101",
  "property_address": "No. 123, Jalan Test",
  "snp_date": "2024-01-15",
  "lawyer_firm_name": "Test & Associates"
}' | python3 mortgage/handlers/handle_lawyer_intake.py

# Test Property Checklist
echo '{
  "property_address": "No. 123, Jalan Test",
  "property_type": "condominium",
  "developer_name": "Developer ABC",
  "is_new_unit": true
}' | python3 mortgage/handlers/handle_property_checklist.py
```

## Tools

### 1. lppsa_intake
Normalizes customer data into LPPSA form fields.

**Features**:
- IC number validation
- DSR (Debt Service Ratio) calculation
- Eligibility determination
- Income and loan validation

### 2. takaful_submission
Normalizes Takaful insurance requirements and submission data.

**Features**:
- Coverage amount calculation
- Premium estimation
- Beneficiary handling
- Medical declaration processing

### 3. lawyer_intake
Captures Sale & Purchase (S&P) agreement details and panel lawyer information.

**Features**:
- S&P date validation
- Panel lawyer verification
- Vendor details capture
- Legal document tracking

### 4. property_checklist
Validates property details and determines if new unit or subsale.

**Features**:
- Property classification (new unit vs subsale)
- Title status determination
- Completion certificate validation
- Required documents list generation

## File Structure

```
mortgage/
├── manifests/
│   └── mortgage_mcp_manifest.json    # MCP manifest (B2.3)
├── schemas/
│   ├── lppsa_intake.schema.json
│   ├── takaful_submission.schema.json
│   ├── lawyer_intake.schema.json
│   └── property_checklist.schema.json
├── tools/
│   ├── lppsa_intake.json
│   ├── takaful_submission.json
│   ├── lawyer_intake.json
│   └── property_checklist.json
├── handlers/
│   ├── handle_lppsa_intake.py
│   ├── handle_takaful_submission.py
│   ├── handle_lawyer_intake.py
│   └── handle_property_checklist.py
├── test/
│   └── test_mortgage_mcp.json       # Test suite (B2.6)
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
    "vertical": "mortgage-lppsa",
    "timestamp": "2024-01-15T10:30:00",
    "customer_id": "850101-01-0101",
    "data": { /* normalized_data */ },
    "next_steps": ["next_tool_1", "next_tool_2"]
  }
}
```

## Testing

See `test/test_mortgage_mcp.json` for the complete test suite including:
- Individual tool tests
- Error handling tests
- End-to-end workflow tests

## Documentation

- **Architecture Overview**: `architecture/overview.md`
- **Data Flow**: `architecture/data_flow.md`
- **Dependencies**: `architecture/dependencies.md`

## Implementation Status

✅ **B2.3** - Mortgage MCP Manifest created  
✅ **B2.4** - LPPSA Tool Handlers implemented  
✅ **B2.5** - Proposal Engine integration ready  
✅ **B2.6** - Test suite created

## License

Copyright © 2024 Qontrek. All rights reserved.

