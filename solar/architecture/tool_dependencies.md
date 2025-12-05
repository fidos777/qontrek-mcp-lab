# Solar MCP Toolpack Tool Dependencies

## Overview

This document details the dependencies between tools in the Solar MCP Toolpack, including the dependency graph, validation order, schema chaining specifications, and integration requirements with external services.

---

## Dependency Graph

### Visual Dependency Map

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              TOOL DEPENDENCY GRAPH                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│                               ┌─────────────────────┐                                │
│                               │                     │                                │
│                               │     lead_intake     │                                │
│                               │                     │                                │
│                               │  ENTRY POINT        │                                │
│                               │  Upstream: None     │                                │
│                               │                     │                                │
│                               └──────────┬──────────┘                                │
│                                          │                                           │
│                                          │ Optional                                  │
│                                          │ (can skip)                                │
│                                          ▼                                           │
│                               ┌─────────────────────┐                                │
│                               │                     │                                │
│                               │   site_inspection   │                                │
│                               │                     │                                │
│                               │  Upstream:          │                                │
│                               │   • lead_intake     │                                │
│                               │     (OPTIONAL)      │                                │
│                               │                     │                                │
│                               └──────────┬──────────┘                                │
│                                          │                                           │
│                                          │ Optional                                  │
│                                          │ (uses defaults if skipped)                │
│                                          ▼                                           │
│                               ┌─────────────────────┐                                │
│                               │                     │                                │
│                               │    roi_calculator   │                                │
│                               │                     │                                │
│                               │  Upstream:          │                                │
│                               │   • site_inspection │                                │
│                               │     (OPTIONAL)      │                                │
│                               │   • lead_intake     │                                │
│                               │     (OPTIONAL)      │                                │
│                               │                     │                                │
│                               └──────────┬──────────┘                                │
│                                          │                                           │
│                                          │ REQUIRED                                  │
│                                          │ (must have ROI)                           │
│                                          ▼                                           │
│                               ┌─────────────────────┐                                │
│                               │                     │                                │
│                               │  quotation_builder  │                                │
│                               │                     │                                │
│                               │  Upstream:          │                                │
│                               │   • roi_calculator  │                                │
│                               │     (REQUIRED)      │                                │
│                               │                     │                                │
│                               │  EXIT POINT         │                                │
│                               │  Downstream: None   │                                │
│                               │                     │                                │
│                               └─────────────────────┘                                │
│                                                                                      │
│  ═══════════════════════════════════════════════════════════════════════════════════ │
│                                                                                      │
│  LEGEND:                                                                             │
│                                                                                      │
│    ──▶  Optional dependency (tool can proceed without it)                            │
│    ══▶  Required dependency (tool will fail without it)                              │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Dependency Matrix

#### Tool-to-Tool Dependencies

| Tool | lead_intake | site_inspection | roi_calculator | quotation_builder |
|------|:-----------:|:---------------:|:--------------:|:-----------------:|
| **lead_intake** | - | ↓ Optional | ↓ Optional | ↓ Optional |
| **site_inspection** | ↑ Optional | - | ↓ Optional | ↓ Optional |
| **roi_calculator** | ↑ Optional | ↑ Optional | - | ↓ **REQUIRED** |
| **quotation_builder** | ↑ Optional | ↑ Optional | ↑ **REQUIRED** | - |

#### External Service Dependencies

| Tool | Supabase DB | Supabase Storage | Qontrek Doc Factory | FireCrawl |
|------|:-----------:|:----------------:|:-------------------:|:---------:|
| **lead_intake** | REQUIRED | Optional | - | Optional |
| **site_inspection** | REQUIRED | REQUIRED | - | - |
| **roi_calculator** | REQUIRED | - | - | - |
| **quotation_builder** | REQUIRED | REQUIRED | REQUIRED | - |

---

## Validation Order

### Tool Execution Validation Sequence

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                            VALIDATION ORDER PER TOOL                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  PHASE 1: PRE-EXECUTION VALIDATION                                                   │
│  ─────────────────────────────────                                                   │
│                                                                                      │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  1. Schema Validation                                                        │  │
│    │     • JSON Schema validation against tool input schema                       │  │
│    │     • Type coercion (if schema allows)                                       │  │
│    │     • Required field check                                                   │  │
│    │     • Format validation (UUID, email, phone patterns)                        │  │
│    └──────────────────────────────────┬──────────────────────────────────────────┘  │
│                                       │                                              │
│                                       ▼                                              │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  2. Reference Validation                                                     │  │
│    │     • Verify referenced IDs exist in database                                │  │
│    │     • Check lead_id exists (if provided)                                     │  │
│    │     • Check site_inspection_id exists (if provided)                          │  │
│    │     • Check roi_calculation_id exists (REQUIRED for quotation_builder)       │  │
│    └──────────────────────────────────┬──────────────────────────────────────────┘  │
│                                       │                                              │
│                                       ▼                                              │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  3. Authorization Validation                                                 │  │
│    │     • Verify API key / Bearer token                                          │  │
│    │     • Check RLS policies (agent can access this lead?)                       │  │
│    │     • Rate limit check                                                       │  │
│    └──────────────────────────────────┬──────────────────────────────────────────┘  │
│                                       │                                              │
│                                       ▼                                              │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  4. Business Rule Validation                                                 │  │
│    │     • Cross-field consistency checks                                         │  │
│    │     • Domain-specific constraints                                            │  │
│    │     • Workflow state validation                                              │  │
│    └──────────────────────────────────┬──────────────────────────────────────────┘  │
│                                       │                                              │
│                                       ▼                                              │
│  PHASE 2: EXECUTION                                                                  │
│  ──────────────────                                                                  │
│                                                                                      │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  5. Tool Logic Execution                                                     │  │
│    │     • Execute core business logic                                            │  │
│    │     • Call external services if needed                                       │  │
│    │     • Persist results to database                                            │  │
│    └──────────────────────────────────┬──────────────────────────────────────────┘  │
│                                       │                                              │
│                                       ▼                                              │
│  PHASE 3: POST-EXECUTION VALIDATION                                                  │
│  ──────────────────────────────────                                                  │
│                                                                                      │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  6. Output Schema Validation                                                 │  │
│    │     • Validate output against response schema                                │  │
│    │     • Ensure all required output fields present                              │  │
│    │     • Sanitize sensitive data for logging                                    │  │
│    └──────────────────────────────────┬──────────────────────────────────────────┘  │
│                                       │                                              │
│                                       ▼                                              │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  7. Event Emission                                                           │  │
│    │     • Emit webhook event (if configured)                                     │  │
│    │     • Update audit log                                                       │  │
│    │     • Return response to caller                                              │  │
│    └─────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Per-Tool Validation Rules

#### lead_intake Validation

```yaml
validation:
  schema:
    - customer_name: required, string, 2-200 chars
    - address: required, string, 10-500 chars
    - contact_phone: optional, pattern "^\\+?[0-9\\-\\s]{8,20}$"
    - contact_email: optional, format email
    - property_type: optional, enum [residential, commercial, industrial]
    - monthly_electricity_bill_myr: optional, number, min 0
    - budget_range: optional, enum [below_15000, 15000_to_30000, ...]
    - timeline: optional, enum [immediate, within_1_month, ...]

  business_rules:
    - At least one contact method required (phone OR email OR whatsapp)
    - If property_type is "commercial", budget_range should be "above_50000"
    - Postcode must be valid Malaysian postcode (5 digits)

  references:
    - None (entry point tool)
```

#### site_inspection Validation

```yaml
validation:
  schema:
    - lead_id: optional, format uuid
    - roof_type: required, enum [concrete_flat, concrete_pitched, metal_deck, ...]
    - roof_area_sqm: required, number, range 10-10000
    - roof_orientation: optional, enum [north, south, east, west, ...]
    - roof_tilt_degrees: optional, number, range 0-60
    - shading_factor: optional, number, range 0-1
    - images: optional, array of {url: uri, image_type: enum}

  business_rules:
    - usable_area_sqm cannot exceed roof_area_sqm
    - shading_factor 0 = no shading, 1 = fully shaded
    - If roof_type is "metal_deck", check structural_assessment.load_bearing
    - panel_layout.total_panels must equal rows × columns

  references:
    - lead_id: OPTIONAL
      - If provided: verify exists in leads table
      - If not provided: create standalone inspection (manual lead entry later)
```

#### roi_calculator Validation

```yaml
validation:
  schema:
    - system_size_kwp: required, number, range 1-1000
    - site_inspection_id: optional, format uuid
    - monthly_bill_myr: optional, number, min 0
    - tariff_rate_myr_kwh: optional, number, default 0.57
    - installation_cost_per_kwp: optional, number, default 3800
    - projection_years: optional, integer, range 10-30, default 25
    - discount_rate: optional, number, range 0-0.25, default 0.06
    - shading_factor: optional, number, range 0-1, default 0
    - orientation_factor: optional, number, range 0.5-1.0, default 1.0

  business_rules:
    - If site_inspection_id provided, system_size should match ±20%
    - tariff_rate cannot be lower than nem_export_rate
    - loan_amount cannot exceed total_cost
    - loan_term_years typically 5-10 years for solar

  references:
    - site_inspection_id: OPTIONAL
      - If provided: fetch efficiency_factors, system_size recommendation
      - If not provided: use manual inputs with conservative defaults
    - lead_id: OPTIONAL (derived from inspection if provided)
      - If available: fetch monthly_bill for validation
```

#### quotation_builder Validation

```yaml
validation:
  schema:
    - roi_calculation_id: REQUIRED, format uuid
    - output_formats: optional, array, default ["pdf"]
    - template_id: optional, enum [standard, premium, commercial, minimal]
    - validity_days: optional, integer, range 7-90, default 30
    - custom_pricing.discount_percentage: optional, number, range 0-50
    - language: optional, enum [en, ms, zh], default "en"

  business_rules:
    - roi_calculation_id MUST exist and have complete financial_summary
    - discount_percentage > 20% requires approval_workflow
    - If template_id is "commercial", must have company details
    - validity_days cannot exceed 90 days

  references:
    - roi_calculation_id: REQUIRED
      - MUST exist in roi_calculations table
      - MUST have financial_summary.total_cost_myr populated
      - MUST have system_specifications populated
    - lead_id: AUTO-DERIVED from roi_calculation
      - Fetch customer details for document generation
```

---

## Schema Chaining

### Schema Reference Chain

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              SCHEMA CHAINING DIAGRAM                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   lead_intake.schema.json                                                            │
│   ┌──────────────────────────────────────────────────────────────────────────────┐  │
│   │  OUTPUT:                                                                      │  │
│   │  {                                                                            │  │
│   │    "lead_id": "uuid",                    ──────────┐                          │  │
│   │    "estimated_system_size_kwp": number   ──────────│─────┐                    │  │
│   │  }                                                 │     │                    │  │
│   └────────────────────────────────────────────────────│─────│────────────────────┘  │
│                                                        │     │                       │
│                                                        │     │                       │
│   site_inspection.schema.json                          │     │                       │
│   ┌────────────────────────────────────────────────────│─────│────────────────────┐  │
│   │  INPUT:                                            │     │                    │  │
│   │  {                                                 │     │                    │  │
│   │    "lead_id": "uuid"                      ◀────────┘     │                    │  │
│   │  }                                                       │                    │  │
│   │                                                          │                    │  │
│   │  OUTPUT:                                                 │                    │  │
│   │  {                                                       │                    │  │
│   │    "inspection_id": "uuid",              ──────────┐     │                    │  │
│   │    "recommended_system_size_kwp": number ──────────│─────│─┐                  │  │
│   │    "efficiency_factors": {               ──────────│─────│─│─┐                │  │
│   │      "shading_factor": number,                     │     │ │ │                │  │
│   │      "orientation_factor": number                  │     │ │ │                │  │
│   │    }                                               │     │ │ │                │  │
│   │  }                                                 │     │ │ │                │  │
│   └────────────────────────────────────────────────────│─────│─│─│────────────────┘  │
│                                                        │     │ │ │                   │
│                                                        │     │ │ │                   │
│   roi_calculator.schema.json                           │     │ │ │                   │
│   ┌────────────────────────────────────────────────────│─────│─│─│────────────────┐  │
│   │  INPUT:                                            │     │ │ │                │  │
│   │  {                                                 │     │ │ │                │  │
│   │    "site_inspection_id": "uuid"           ◀────────┘     │ │ │                │  │
│   │    "system_size_kwp": number              ◀──────────────┴─┘ │                │  │
│   │    "shading_factor": number               ◀──────────────────┘                │  │
│   │    "orientation_factor": number           ◀──────────────────┘                │  │
│   │  }                                                                            │  │
│   │                                                                               │  │
│   │  OUTPUT:                                                                      │  │
│   │  {                                                                            │  │
│   │    "roi_id": "uuid",                      ───────────────────┐                │  │
│   │    "financial_summary": {...}             ───────────────────│─┐              │  │
│   │    "system_specifications": {...}         ───────────────────│─│─┐            │  │
│   │  }                                                           │ │ │            │  │
│   └──────────────────────────────────────────────────────────────│─│─│────────────┘  │
│                                                                  │ │ │               │
│                                                                  │ │ │               │
│   quotation_builder.schema.json                                  │ │ │               │
│   ┌──────────────────────────────────────────────────────────────│─│─│────────────┐  │
│   │  INPUT:                                                      │ │ │            │  │
│   │  {                                                           │ │ │            │  │
│   │    "roi_calculation_id": "uuid"           ◀──────────────────┘ │ │            │  │
│   │  }                                                             │ │            │  │
│   │                                                                │ │            │  │
│   │  AUTO-RETRIEVED (via roi_calculation_id):                      │ │            │  │
│   │  {                                                             │ │            │  │
│   │    "financial_summary": {...}             ◀────────────────────┘ │            │  │
│   │    "system_specifications": {...}         ◀──────────────────────┘            │  │
│   │    "customer_details": {...}              ◀──── (via lead_id chain)           │  │
│   │  }                                                                            │  │
│   │                                                                               │  │
│   │  OUTPUT:                                                                      │  │
│   │  {                                                                            │  │
│   │    "quotation_id": "uuid",                                                    │  │
│   │    "quote_number": "string",                                                  │  │
│   │    "document_urls": {...}                                                     │  │
│   │  }                                                                            │  │
│   └───────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Field Mapping Specifications

```json
{
  "schema_chains": {
    "lead_intake_to_site_inspection": {
      "mappings": [
        {
          "source": "lead_intake.output.lead_id",
          "target": "site_inspection.input.lead_id",
          "required": false,
          "transform": null
        },
        {
          "source": "lead_intake.output.address",
          "target": "site_inspection.input.gps_coordinates",
          "required": false,
          "transform": "geocode_address"
        }
      ],
      "defaults_if_skipped": {
        "lead_id": null
      }
    },

    "site_inspection_to_roi_calculator": {
      "mappings": [
        {
          "source": "site_inspection.output.inspection_id",
          "target": "roi_calculator.input.site_inspection_id",
          "required": false,
          "transform": null
        },
        {
          "source": "site_inspection.output.recommended_system_size_kwp",
          "target": "roi_calculator.input.system_size_kwp",
          "required": false,
          "transform": null
        },
        {
          "source": "site_inspection.output.efficiency_factors.shading_factor",
          "target": "roi_calculator.input.shading_factor",
          "required": false,
          "transform": "invert_factor"
        },
        {
          "source": "site_inspection.output.efficiency_factors.orientation_factor",
          "target": "roi_calculator.input.orientation_factor",
          "required": false,
          "transform": null
        }
      ],
      "defaults_if_skipped": {
        "site_inspection_id": null,
        "shading_factor": 0,
        "orientation_factor": 1.0,
        "system_size_kwp": "REQUIRED_MANUAL_INPUT"
      }
    },

    "roi_calculator_to_quotation_builder": {
      "mappings": [
        {
          "source": "roi_calculator.output.roi_id",
          "target": "quotation_builder.input.roi_calculation_id",
          "required": true,
          "transform": null
        }
      ],
      "auto_retrieved_fields": [
        "financial_summary.*",
        "system_specifications.*",
        "year_by_year_projection",
        "sensitivity_analysis",
        "lead.customer_name",
        "lead.address",
        "lead.contact_*"
      ],
      "defaults_if_skipped": "NOT_ALLOWED"
    }
  },

  "transforms": {
    "geocode_address": {
      "type": "api_call",
      "endpoint": "internal://geocoder",
      "fallback": null
    },
    "invert_factor": {
      "type": "formula",
      "expression": "1 - value",
      "description": "Convert shading loss factor to shading efficiency"
    }
  }
}
```

### Schema Compatibility Rules

```yaml
compatibility:
  version_policy: semver

  rules:
    - Adding optional fields: backward compatible (minor version bump)
    - Adding required fields: breaking change (major version bump)
    - Removing fields: breaking change (major version bump)
    - Changing field types: breaking change (major version bump)
    - Adding enum values: backward compatible (minor version bump)
    - Removing enum values: breaking change (major version bump)

  compatibility_matrix:
    lead_intake:
      v1.0.x:
        compatible_with:
          site_inspection: ["1.0.x", "1.1.x"]
          roi_calculator: ["1.0.x"]

    site_inspection:
      v1.0.x:
        compatible_with:
          roi_calculator: ["1.0.x"]

    roi_calculator:
      v1.0.x:
        compatible_with:
          quotation_builder: ["1.0.x"]

  deprecation:
    notice_period: 6 months
    sunset_period: 3 months after deprecation
    migration_guide_required: true
```

---

## Detailed Tool Dependencies

### 1. lead_intake

```yaml
tool: lead_intake
version: 1.0.0

dependencies:
  upstream:
    tools: []  # Entry point - no upstream dependencies

  downstream:
    tools:
      - name: site_inspection
        relationship: optional
        data_passed:
          - lead_id
          - address (for GPS lookup)
          - estimated_system_size_kwp (guidance only)
          - property_type (informs roof expectations)
        auto_trigger: false

  external:
    required:
      - service: supabase_database
        purpose: Store lead records
        tables: [leads, lead_interactions]
        operations: [INSERT, SELECT]

    optional:
      - service: supabase_storage
        purpose: Store uploaded documents (electricity bills)
        bucket: lead-attachments
        max_file_size: 5MB

      - service: firecrawl
        purpose: Enrich B2B leads with company data
        rate_limit: 100/hour

  internal:
    - component: lead_scoring_engine
      inputs: [budget, timeline, property_type, engagement]
      outputs: [lead_score, score_breakdown]

    - component: agent_assignment
      inputs: [region, property_type, lead_score]
      outputs: [assigned_agent_id, assigned_agent_name]

execution:
  timeout: 5s
  retry_policy:
    max_retries: 3
    backoff: exponential
    initial_delay: 500ms
  idempotent: false
  cacheable: false
  rate_limit:
    requests_per_minute: 100
    requests_per_day: 5000
```

### 2. site_inspection

```yaml
tool: site_inspection
version: 1.0.0

dependencies:
  upstream:
    tools:
      - name: lead_intake
        relationship: optional
        data_received:
          - lead_id (reference for linking)
          - address (verify GPS matches)
          - estimated_system_size_kwp (validation)
        fallback: Manual entry, create standalone inspection

  downstream:
    tools:
      - name: roi_calculator
        relationship: optional
        data_passed:
          - inspection_id
          - usable_roof_area_sqm
          - recommended_system_size_kwp
          - efficiency_factors.*
          - installation_complexity
        auto_trigger: false

  external:
    required:
      - service: supabase_database
        purpose: Store inspection records
        tables: [site_inspections]
        operations: [INSERT, SELECT, UPDATE]

      - service: supabase_storage
        purpose: Store inspection photos
        bucket: inspection-images
        max_file_size: 10MB
        allowed_types: [image/jpeg, image/png, image/webp]

  internal:
    - component: panel_layout_calculator
      inputs: [roof_area, orientation, shading, panel_wattage]
      outputs: [rows, columns, total_panels, layout_diagram]

    - component: system_sizing_engine
      inputs: [usable_area, panel_wattage, efficiency_factors]
      outputs: [recommended_system_size_kwp, recommended_panels]

    - component: complexity_analyzer
      inputs: [roof_type, structural_assessment, electrical_assessment]
      outputs: [installation_complexity, special_requirements]

execution:
  timeout: 10s
  retry_policy:
    max_retries: 2
    backoff: exponential
    initial_delay: 1000ms
  idempotent: true
  cacheable: false
  rate_limit:
    requests_per_minute: 30
    requests_per_day: 500
```

### 3. roi_calculator

```yaml
tool: roi_calculator
version: 1.0.0

dependencies:
  upstream:
    tools:
      - name: site_inspection
        relationship: optional
        data_received:
          - site_inspection_id
          - system_size_kwp
          - shading_factor
          - orientation_factor
          - tilt_factor
        fallback: Manual input with conservative defaults

      - name: lead_intake
        relationship: optional
        data_received:
          - monthly_electricity_bill_myr
          - property_type (for tariff lookup)
        fallback: Use default tariff rate (0.57 MYR/kWh)

  downstream:
    tools:
      - name: quotation_builder
        relationship: optional
        data_passed:
          - roi_id
          - financial_summary.*
          - system_specifications.*
          - year_by_year_projection
          - sensitivity_analysis
        auto_trigger: false

  external:
    required:
      - service: supabase_database
        purpose: Store ROI calculations
        tables: [roi_calculations]
        operations: [INSERT, SELECT]

  internal:
    - component: generation_estimator
      inputs: [system_size, irradiance, performance_ratio, efficiency_factors]
      outputs: [annual_generation_kwh, specific_yield]

    - component: financial_calculator
      inputs: [costs, savings, discount_rate, projection_years]
      outputs: [payback, npv, irr, roi, lcoe]

    - component: sensitivity_analyzer
      inputs: [base_calculation, variance_factors]
      outputs: [conservative, base, optimistic scenarios]

  reference_data:
    - name: tariff_rates
      source: solar://tariffs
      cache_ttl: 24h
      default_value: 0.57

    - name: irradiance_data
      source: static
      regions: [northern, central, eastern, southern, sabah, sarawak]
      default_value: 1600

execution:
  timeout: 5s
  retry_policy:
    max_retries: 2
    backoff: exponential
    initial_delay: 500ms
  idempotent: true
  cacheable: true
  cache_ttl: 3600s
  rate_limit:
    requests_per_minute: 60
    requests_per_day: 1000
```

### 4. quotation_builder

```yaml
tool: quotation_builder
version: 1.0.0

dependencies:
  upstream:
    tools:
      - name: roi_calculator
        relationship: REQUIRED
        data_received:
          - roi_calculation_id (MUST exist)
          - financial_summary.* (all fields)
          - system_specifications.* (all fields)
          - year_by_year_projection (for charts)
          - sensitivity_analysis (for summary)
        fallback: NONE - tool will fail without valid roi_calculation_id

  downstream:
    tools: []  # Terminal node

  external:
    required:
      - service: supabase_database
        purpose: Store quotation records
        tables: [quotations]
        operations: [INSERT, SELECT, UPDATE]

      - service: supabase_storage
        purpose: Store generated documents
        bucket: quotation-documents

      - service: qontrek_document_factory
        purpose: Generate PDF/DOCX/PPTX/XLSX documents
        api_endpoint: https://api.qontrek.com/v1/documents
        timeout: 30s
        retry_policy:
          max_retries: 3
          backoff: exponential
          initial_delay: 2000ms
        webhook_signature: HMAC-SHA256

  internal:
    - component: quote_number_generator
      format: "QT-{YYYY}-{NNNNN}"
      sequence_source: database

    - component: pricing_calculator
      inputs: [base_cost, discount, tax_rules]
      outputs: [subtotal, discount_amount, tax_amount, total]

    - component: template_selector
      inputs: [template_id, customer_type, language]
      outputs: [template_config, sections]

  reference_data:
    - name: document_templates
      source: solar://templates
      cache_ttl: 1h

    - name: equipment_catalog
      source: solar://equipment
      cache_ttl: 1h

    - name: company_branding
      source: organization settings
      cache_ttl: 24h

execution:
  timeout: 30s
  retry_policy:
    max_retries: 3
    backoff: exponential
    initial_delay: 2000ms
  idempotent: false
  cacheable: false
  async_supported: true
  rate_limit:
    requests_per_minute: 20
    requests_per_day: 200
```

---

## Failure Handling

### Dependency Failure Matrix

| Scenario | Affected Tool | Impact | Recovery Strategy |
|----------|--------------|--------|-------------------|
| Lead not found | site_inspection | Warning | Proceed without lead reference |
| Lead not found | roi_calculator | Warning | Use manual inputs |
| Inspection not found | roi_calculator | Warning | Use manual inputs with defaults |
| ROI not found | quotation_builder | **FAILURE** | Must create ROI first |
| Supabase DB down | All tools | **FAILURE** | Circuit breaker, retry later |
| Supabase Storage down | site_inspection | **FAILURE** | Cannot store images |
| Supabase Storage down | quotation_builder | **FAILURE** | Cannot store documents |
| Document Factory down | quotation_builder | Degraded | Queue for retry, notify user |
| Invalid schema | All tools | **FAILURE** | Return validation errors |
| Rate limit exceeded | All tools | **FAILURE** | Return 429, retry after cooldown |

### Circuit Breaker Configuration

```json
{
  "circuit_breakers": {
    "supabase": {
      "failure_threshold": 5,
      "reset_timeout_ms": 30000,
      "half_open_requests": 3,
      "fallback": {
        "action": "fail_fast",
        "message": "Database temporarily unavailable. Please retry."
      }
    },
    "qontrek_document_factory": {
      "failure_threshold": 3,
      "reset_timeout_ms": 60000,
      "half_open_requests": 1,
      "fallback": {
        "action": "queue_and_notify",
        "message": "Document generation queued. You will receive a notification when ready.",
        "queue_name": "document_generation_retry"
      }
    },
    "firecrawl": {
      "failure_threshold": 10,
      "reset_timeout_ms": 300000,
      "half_open_requests": 2,
      "fallback": {
        "action": "skip_enrichment",
        "message": "Lead enrichment skipped due to service unavailability."
      }
    }
  }
}
```

---

## Testing Dependencies

### Mock Service Configuration

```json
{
  "test_config": {
    "supabase": {
      "mock": true,
      "fixtures_path": "./test/fixtures/supabase",
      "tables": {
        "leads": "./test/fixtures/leads.json",
        "site_inspections": "./test/fixtures/inspections.json",
        "roi_calculations": "./test/fixtures/roi.json",
        "quotations": "./test/fixtures/quotations.json"
      }
    },
    "qontrek_document_factory": {
      "mock": true,
      "response": {
        "job_id": "mock-job-123",
        "status": "completed",
        "document_urls": {
          "pdf": "https://mock.storage/test.pdf",
          "docx": "https://mock.storage/test.docx"
        }
      }
    },
    "supabase_storage": {
      "mock": true,
      "response": {
        "url": "https://mock.storage/uploaded-file.jpg"
      }
    },
    "firecrawl": {
      "mock": true,
      "disabled": true
    }
  }
}
```

### Integration Test Chain

```javascript
describe('Full Tool Chain Integration', () => {

  it('should complete lead-to-quote workflow', async () => {
    // Stage 1: Create lead
    const leadResult = await invokeTool('lead_intake', {
      customer_name: 'Test Customer',
      address: '123 Test Street, 47810 Petaling Jaya',
      contact_email: 'test@example.com',
      monthly_electricity_bill_myr: 500,
      property_type: 'residential'
    });

    expect(leadResult.lead_id).toBeDefined();
    expect(leadResult.lead_score).toBeGreaterThan(0);

    // Stage 2: Create inspection
    const inspectionResult = await invokeTool('site_inspection', {
      lead_id: leadResult.lead_id,
      roof_type: 'concrete_flat',
      roof_area_sqm: 80,
      roof_orientation: 'south',
      shading_factor: 0.1
    });

    expect(inspectionResult.inspection_id).toBeDefined();
    expect(inspectionResult.recommended_system_size_kwp).toBeGreaterThan(0);

    // Stage 3: Calculate ROI
    const roiResult = await invokeTool('roi_calculator', {
      site_inspection_id: inspectionResult.inspection_id,
      system_size_kwp: inspectionResult.recommended_system_size_kwp
    });

    expect(roiResult.roi_id).toBeDefined();
    expect(roiResult.financial_summary.payback_period_years).toBeLessThan(15);

    // Stage 4: Generate quotation
    const quoteResult = await invokeTool('quotation_builder', {
      roi_calculation_id: roiResult.roi_id,
      output_formats: ['pdf']
    });

    expect(quoteResult.quotation_id).toBeDefined();
    expect(quoteResult.quote_number).toMatch(/^QT-\d{4}-\d{5}$/);
    expect(quoteResult.document_urls.pdf).toBeDefined();
  });

  it('should handle quick estimate workflow (skip inspection)', async () => {
    // Stage 1: Create lead
    const leadResult = await invokeTool('lead_intake', {
      customer_name: 'Quick Estimate Customer',
      address: '456 Quick Street, 50000 Kuala Lumpur',
      contact_phone: '+60123456789'
    });

    // Stage 2: Calculate ROI (without inspection)
    const roiResult = await invokeTool('roi_calculator', {
      system_size_kwp: 10,  // Manual input
      monthly_bill_myr: 400
    });

    expect(roiResult.roi_id).toBeDefined();
    // Should use default efficiency factors

    // Stage 3: Generate quotation
    const quoteResult = await invokeTool('quotation_builder', {
      roi_calculation_id: roiResult.roi_id
    });

    expect(quoteResult.quotation_id).toBeDefined();
  });

  it('should fail quotation without ROI', async () => {
    await expect(invokeTool('quotation_builder', {
      roi_calculation_id: 'non-existent-uuid'
    })).rejects.toThrow('ROI calculation not found');
  });

});
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2025-12-05 | Added validation order, schema chaining notes, detailed dependency specs |
| 1.0.0 | 2025-12-05 | Initial tool dependencies documentation |
