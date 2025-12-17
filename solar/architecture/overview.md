# Solar MCP Toolpack - Architecture Overview

## Purpose

The Solar MCP Toolpack provides a comprehensive set of tools for processing solar lead intake, site inspection, ROI calculation, roof assessment, and quotation generation. It integrates with FireCrawl brandpacks for document theming and is compatible with the Proposal Engine and Document Factory.

## Architecture Layers

### 1. Manifest Layer (B1.3)
- **File**: `solar/manifests/solar_mcp_manifest.json`
- **Purpose**: Defines the MCP server configuration, tool registry, and capabilities
- **Key Components**:
  - 5 tool definitions (lead_intake, site_inspection, roi, roof_check, quotation)
  - Schema references
  - FireCrawl brandpack integration
  - Health check configuration

### 2. Schema Layer
- **Location**: `solar/schemas/`
- **Purpose**: JSON Schema 2020 definitions for input validation
- **Schemas**:
  - `lead_intake.schema.json` - Customer lead information
  - `site_inspection.schema.json` - Site inspection data
  - `roi.schema.json` - ROI calculation inputs
  - `roof_check.schema.json` - Roof classification
  - `quotation.schema.json` - Quotation generation

### 3. Tool Definition Layer
- **Location**: `solar/tools/`
- **Purpose**: Tool metadata and input/output schemas
- **Tools**: 5 tool definition files

### 4. Handler Layer (B1.4)
- **Location**: `solar/handlers/`
- **Purpose**: Python handlers that process and transform data
- **Handlers**:
  - `handle_lead_intake.py` - Lead qualification and prioritization
  - `handle_site_inspection.py` - Inspection normalization
  - `handle_roi.py` - ROI calculations
  - `handle_roof_check.py` - Roof classification
  - `handle_quotation.py` - Quotation generation with brandpacks

### 5. Proposal Engine Integration (B1.5)
- **Purpose**: All handlers output `proposal_payload` compatible with Proposal Engine
- **Format**: Standardized JSON structure with `status: "ready_for_proposal"`
- **Brandpack Support**: FireCrawl brandpack integration for theming

## Data Flow

```
Lead Intake → Site Inspection → ROI Calculation → Roof Check → Quotation
```

1. **Lead Intake**: Parse customer info, calculate priority, estimate system size
2. **Site Inspection**: Process inspection data, estimate capacity
3. **ROI Calculation**: Calculate financial metrics
4. **Roof Check**: Classify roof and determine mounting
5. **Quotation**: Generate quotation with brandpack theming

## Key Features

- ✅ Lead prioritization scoring
- ✅ System size estimation
- ✅ ROI calculations (payback, savings, lifetime value)
- ✅ Roof type classification
- ✅ Mounting type determination
- ✅ FireCrawl brandpack integration
- ✅ Proposal Engine compatibility
- ✅ Document Factory compatibility
- ✅ Comprehensive error handling
- ✅ Console logging

## Integration Points

### Proposal Engine
All handlers output `proposal_payload` with:
- `status: "ready_for_proposal"`
- `vertical: "solar"`
- `customer_id` or `property_id`
- `next_steps` array

### Document Factory
Quotation handler outputs formatted data ready for document generation.

### FireCrawl Brandpacks
Quotation handler loads brandpacks from `brandpacks/_template/` and applies:
- Colors (primary, secondary, accent)
- Fonts
- Logo
- Style theme

## Testing (B1.6)

Test suite located at `solar/test/test_solar_mcp.json` includes:
- Individual tool tests
- Calculation validation tests
- Error handling tests
- End-to-end workflow tests

