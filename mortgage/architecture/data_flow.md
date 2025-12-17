# Mortgage MCP - Data Flow Documentation

## Overview

This document describes the data flow through the Mortgage MCP Toolpack, from input to proposal-ready output.

## Flow Diagram

```
┌─────────────────┐
│  Input JSON     │
│  (Raw Data)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Schema          │
│ Validation      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Handler         │
│ Processing      │
│ - Parse         │
│ - Transform     │
│ - Calculate     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Normalized      │
│ Data            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Proposal        │
│ Payload         │
└─────────────────┘
```

## Detailed Flow by Tool

### 1. LPPSA Intake Flow

**Input**:
```json
{
  "customer_name": "Ahmad bin Abdullah",
  "ic_number": "850101-01-0101",
  "income": 5000,
  "property_price": 250000,
  "loan_amount": 200000,
  "loan_tenure": 30
}
```

**Processing Steps**:
1. Validate IC number format
2. Validate numeric fields (income, property_price, loan_amount, tenure)
3. Normalize customer name (uppercase)
4. Calculate DSR (Debt Service Ratio)
5. Determine eligibility status
6. Build LPPSA form fields

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "applicant_name": "AHMAD BIN ABDULLAH",
    "dsr_ratio": 15.5,
    "eligibility_status": "eligible",
    "lppsa_form_fields": { ... }
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "next_steps": ["takaful_submission", "property_checklist", "lawyer_intake"]
  }
}
```

### 2. Takaful Submission Flow

**Input**:
```json
{
  "customer_ic": "850101-01-0101",
  "loan_amount": 200000,
  "property_value": 250000,
  "coverage_type": "mrta"
}
```

**Processing Steps**:
1. Validate IC number
2. Determine coverage amount (min of loan_amount and property_value)
3. Calculate premium estimate based on:
   - Coverage type (MRTA, MLTA, Fire, Comprehensive)
   - Customer age
   - Payment method (single, annual, monthly)
4. Build beneficiary details
5. Build Takaful form fields

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "coverage_amount": 200000,
    "premium_estimate": 200.00,
    "takaful_form_fields": { ... }
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "next_steps": ["lawyer_intake", "property_checklist"]
  }
}
```

### 3. Lawyer Intake Flow

**Input**:
```json
{
  "customer_ic": "850101-01-0101",
  "property_address": "No. 123, Jalan Test",
  "snp_date": "2024-01-15",
  "lawyer_firm_name": "Test & Associates",
  "is_panel_lawyer": true
}
```

**Processing Steps**:
1. Validate IC number
2. Validate date formats (S&P date, completion date)
3. Validate email and phone (if provided)
4. Build lawyer details object
5. Build vendor details (if provided)
6. Generate S&P reference number (if not provided)
7. Verify panel lawyer status

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "snp_reference": "SNP-2024-001",
    "panel_approved": true,
    "legal_form_fields": { ... }
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "next_steps": ["property_checklist"]
  }
}
```

### 4. Property Checklist Flow

**Input**:
```json
{
  "property_address": "No. 123, Jalan Test",
  "property_type": "condominium",
  "developer_name": "Developer ABC",
  "is_new_unit": true
}
```

**Processing Steps**:
1. Validate property type
2. Classify property (new unit vs subsale) based on:
   - Explicit `is_new_unit` flag
   - Registration date
   - Completion certificate status
   - Subsale evidence
3. Determine title status (strata vs individual)
4. Determine completion status
5. Determine valuation status
6. Generate required documents list

**Output**:
```json
{
  "status": "success",
  "normalized_data": {
    "classification": "new_unit",
    "title_status": "strata_title",
    "required_documents": ["Booking Form", "S&P Agreement", ...],
    "property_form_fields": { ... }
  },
  "proposal_payload": {
    "status": "ready_for_proposal",
    "next_steps": []
  }
}
```

## End-to-End Flow

### Complete Mortgage Application

```
Step 1: LPPSA Intake
  → Customer eligibility determined
  → DSR calculated
  → Next: Takaful, Property, Lawyer

Step 2: Takaful Submission
  → Coverage amount determined
  → Premium calculated
  → Next: Lawyer, Property

Step 3: Lawyer Intake
  → S&P details captured
  → Panel status verified
  → Next: Property

Step 4: Property Checklist
  → Property classified
  → Documents list generated
  → Next: None (ready for proposal)
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
  "vertical": "mortgage-lppsa",
  "timestamp": "2024-01-15T10:30:00",
  "customer_id": "850101-01-0101",
  "data": { /* normalized_data */ },
  "status": "ready_for_proposal",
  "next_steps": ["next_tool_1", "next_tool_2"]
}
```

This structure ensures compatibility with the Proposal Engine.

