# Mortgage MCP Toolpack - Architecture Overview

## Purpose

The Mortgage MCP Toolpack provides a standardized set of tools for processing mortgage applications with LPPSA (Low Price Public Sector Housing) integration. It handles customer intake, Takaful insurance submissions, lawyer intake, and property validation.

## Architecture Layers

### 1. Manifest Layer (B2.3)
- **File**: `mortgage/manifests/mortgage_mcp_manifest.json`
- **Purpose**: Defines the MCP server configuration, tool registry, and capabilities
- **Key Components**:
  - Tool definitions and paths
  - Schema references
  - Health check configuration
  - Example requests

### 2. Schema Layer
- **Location**: `mortgage/schemas/`
- **Purpose**: JSON Schema 2020 definitions for input validation
- **Schemas**:
  - `lppsa_intake.schema.json` - Customer intake form
  - `takaful_submission.schema.json` - Takaful insurance requirements
  - `lawyer_intake.schema.json` - S&P and lawyer details
  - `property_checklist.schema.json` - Property validation

### 3. Tool Definition Layer
- **Location**: `mortgage/tools/`
- **Purpose**: Tool metadata and input/output schemas
- **Tools**:
  - `lppsa_intake.json`
  - `takaful_submission.json`
  - `lawyer_intake.json`
  - `property_checklist.json`

### 4. Handler Layer (B2.4)
- **Location**: `mortgage/handlers/`
- **Purpose**: Python handlers that process and transform data
- **Handlers**:
  - `handle_lppsa_intake.py` - Normalizes customer data
  - `handle_takaful_submission.py` - Processes Takaful requirements
  - `handle_lawyer_intake.py` - Captures legal documentation
  - `handle_property_checklist.py` - Validates property details

### 5. Proposal Engine Integration (B2.5)
- **Purpose**: All handlers output `proposal_payload` compatible with Proposal Engine
- **Format**: Standardized JSON structure with `status: "ready_for_proposal"`

## Data Flow

```
Input JSON → Schema Validation → Handler Processing → Normalized Data → Proposal Payload
```

1. **Input**: JSON data matching schema
2. **Validation**: Schema validation + business rule checks
3. **Transformation**: Data normalization and calculation
4. **Output**: Structured JSON with `normalized_data` and `proposal_payload`

## Key Features

- ✅ JSON Schema 2020 validation
- ✅ Malaysian IC number format validation
- ✅ DSR (Debt Service Ratio) calculation
- ✅ Property classification (new unit vs subsale)
- ✅ Panel lawyer verification
- ✅ Takaful premium estimation
- ✅ Proposal Engine compatibility
- ✅ Comprehensive error handling
- ✅ Console logging for debugging

## Integration Points

### Proposal Engine
All handlers output `proposal_payload` with:
- `status: "ready_for_proposal"`
- `vertical: "mortgage-lppsa"`
- `customer_id` or `property_id`
- `next_steps` array

### Document Factory
Handlers can be extended to generate documents using normalized data.

## Testing (B2.6)

Test suite located at `mortgage/test/test_mortgage_mcp.json` includes:
- Individual tool tests
- Error handling tests
- End-to-end workflow tests

