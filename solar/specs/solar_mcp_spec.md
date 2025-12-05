# Solar MCP Toolpack Specification

**Version:** 1.0.0
**Date:** 2025-12-05
**Status:** Draft
**Author:** Qontrek MCP Lab

---

## Table of Contents

1. [Problem Definition](#1-problem-definition)
2. [High-level Architecture](#2-high-level-architecture)
3. [Solar Use Cases](#3-solar-use-cases)
4. [Tools Overview](#4-tools-overview)

---

## 1. Problem Definition

### 1.1 Solar Agent Pain Points

Solar sales agents and field technicians face significant operational friction in their daily workflows:

| Pain Point | Description | Impact |
|------------|-------------|--------|
| **Manual Data Entry** | Agents re-enter the same customer data across 3-5 different systems | 2-3 hours/day wasted |
| **Inconsistent Site Assessments** | No standardized format for roof measurements, shading analysis, panel orientation | 15-20% quote revision rate |
| **Delayed Quotations** | Waiting for back-office to process ROI calculations and generate documents | 24-48 hour turnaround |
| **Lost Lead Context** | Customer information scattered across CRM, email, WhatsApp, spreadsheets | 30% lead follow-up failure |
| **Compliance Burden** | SEDA applications, loan documentation, permit filings require manual form filling | 4-6 hours per installation |

### 1.2 SME Operations Pain Points

Small and medium solar installation companies struggle with:

- **Fragmented Tech Stack**: Using 5-10 disconnected tools (CRM, CAD, accounting, project management)
- **No Single Source of Truth**: Customer data exists in multiple versions across systems
- **Manual Handoffs**: Information passed between sales, technical, and operations teams via email/chat
- **Scaling Bottlenecks**: Adding new agents requires extensive training on multiple systems
- **Reporting Gaps**: No unified view of pipeline, installation status, or financial metrics

### 1.3 Data Fragmentation Issues

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CURRENT STATE: DATA SILOS                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│   │   CRM    │    │  Excel   │    │  Email   │    │ WhatsApp │          │
│   │          │    │ Sheets   │    │          │    │          │          │
│   │ - Leads  │    │ - ROI    │    │ - Quotes │    │ - Photos │          │
│   │ - Status │    │ - Sizing │    │ - Follow │    │ - Voice  │          │
│   └────┬─────┘    └────┬─────┘    └────┬─────┘    └────┬─────┘          │
│        │               │               │               │                 │
│        └───────────────┴───────────────┴───────────────┘                 │
│                              ▼                                           │
│                   ❌ NO INTEGRATION                                      │
│                   ❌ MANUAL SYNC                                         │
│                   ❌ DATA CONFLICTS                                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Key Issues:**
- Customer records duplicated with conflicting information
- Site inspection data locked in photos without structured extraction
- ROI calculations stored in local spreadsheets, not linked to quotes
- No audit trail for compliance documentation

### 1.4 Why MCP Toolpacks Solve These Problems

The **Model Context Protocol (MCP)** enables AI agents to interact with external tools through a standardized interface. MCP Toolpacks solve solar industry pain points by:

| Solution | Benefit |
|----------|---------|
| **Unified Tool Interface** | Single protocol for all operations (site inspection, ROI, quotes, leads) |
| **Structured Data Flow** | Output from one tool feeds directly into the next |
| **Edge-Function Ready** | Tools can run on Supabase Edge, Cloudflare Workers, or locally |
| **LLM-Native Design** | Tools designed for AI agent orchestration, not just human UI |
| **Composable Architecture** | Tools can be combined in different workflows per business need |

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    FUTURE STATE: MCP TOOLPACK                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────────────────────────────────────────────────────────────┐  │
│   │                     SOLAR MCP TOOLPACK                            │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────┐ │  │
│   │  │    Lead     │─▶│    Site     │─▶│    ROI      │─▶│ Quotation│ │  │
│   │  │   Intake    │  │ Inspection  │  │ Calculator  │  │ Builder  │ │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘  └──────────┘ │  │
│   └──────────────────────────────────────────────────────────────────┘  │
│                              ▼                                           │
│                   ✅ SINGLE DATA MODEL                                   │
│                   ✅ AUTOMATIC CHAINING                                  │
│                   ✅ AUDIT TRAIL                                         │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. High-level Architecture

### 2.1 Tool-to-Tool Chaining

The Solar MCP Toolpack implements a **directed acyclic graph (DAG)** of tool dependencies:

```
                    ┌─────────────────┐
                    │   lead_intake   │
                    │                 │
                    │  Captures:      │
                    │  - Customer ID  │
                    │  - Address      │
                    │  - Contact info │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ site_inspection │
                    │                 │
                    │  Captures:      │
                    │  - Roof specs   │
                    │  - Panel layout │
                    │  - Shading data │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  roi_calculator │
                    │                 │
                    │  Calculates:    │
                    │  - System size  │
                    │  - Payback      │
                    │  - Savings      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │quotation_builder│
                    │                 │
                    │  Generates:     │
                    │  - Quote PDF    │
                    │  - Proposal     │
                    │  - Contract     │
                    └─────────────────┘
```

**Chaining Rules:**
- Each tool produces a `result_id` that can be referenced by downstream tools
- Tools validate that required upstream data exists before execution
- Partial chains are allowed (e.g., manual ROI input without site inspection)

### 2.2 Edge-Function Compatibility

All tools are designed to run on serverless edge environments:

| Requirement | Implementation |
|-------------|----------------|
| **Stateless Execution** | Each tool call is independent; state stored in Supabase |
| **Cold Start Optimization** | Tool logic < 50KB, no heavy dependencies |
| **Timeout Handling** | All operations complete within 10 seconds |
| **Memory Limits** | Peak memory usage < 128MB |

**Supported Runtimes:**
- Supabase Edge Functions (Deno)
- Cloudflare Workers (V8 isolates)
- Vercel Edge Functions (Node.js edge runtime)
- AWS Lambda@Edge

### 2.3 Supabase Integration Notes

The toolpack leverages Supabase as the primary data layer:

```sql
-- Core tables for Solar MCP Toolpack
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name TEXT NOT NULL,
    address TEXT NOT NULL,
    contact_phone TEXT,
    contact_email TEXT,
    status TEXT DEFAULT 'new',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE site_inspections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    roof_type TEXT,
    roof_area_sqm DECIMAL,
    roof_orientation TEXT,
    shading_factor DECIMAL,
    panel_layout JSONB,
    images TEXT[],
    inspector_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE roi_calculations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    site_inspection_id UUID REFERENCES site_inspections(id),
    system_size_kwp DECIMAL,
    estimated_annual_generation_kwh DECIMAL,
    monthly_savings_myr DECIMAL,
    payback_period_years DECIMAL,
    roi_percentage DECIMAL,
    assumptions JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE quotations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roi_calculation_id UUID REFERENCES roi_calculations(id),
    quote_number TEXT UNIQUE,
    total_amount_myr DECIMAL,
    valid_until DATE,
    document_urls JSONB,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT now()
);
```

**Row Level Security (RLS):**
- Agents can only access leads assigned to them
- Managers can view all records in their organization
- Audit logs capture all tool invocations

### 2.4 FireCrawl Brand Scraping (Optional)

For enhanced lead qualification, the toolpack can integrate with FireCrawl to:

- Scrape company websites for business context
- Extract existing solar installation photos (competitor analysis)
- Identify decision-maker contact information
- Assess business size and energy consumption indicators

```json
{
  "firecrawl_integration": {
    "enabled": false,
    "api_endpoint": "https://api.firecrawl.dev/v1/scrape",
    "use_cases": [
      "lead_enrichment",
      "competitor_analysis",
      "business_verification"
    ],
    "rate_limit": "100 requests/hour"
  }
}
```

### 2.5 MCP Request/Response Format Examples

**Standard MCP Tool Request:**

```json
{
  "jsonrpc": "2.0",
  "id": "req_abc123",
  "method": "tools/call",
  "params": {
    "name": "site_inspection",
    "arguments": {
      "lead_id": "550e8400-e29b-41d4-a716-446655440000",
      "roof_type": "concrete_flat",
      "roof_area_sqm": 150.5,
      "roof_orientation": "south",
      "shading_factor": 0.15,
      "panel_layout": {
        "rows": 4,
        "columns": 8,
        "panel_model": "JA Solar 550W"
      },
      "images": [
        "https://storage.example.com/inspections/roof_001.jpg",
        "https://storage.example.com/inspections/meter_001.jpg"
      ]
    }
  }
}
```

**Standard MCP Tool Response:**

```json
{
  "jsonrpc": "2.0",
  "id": "req_abc123",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Site inspection recorded successfully"
      }
    ],
    "data": {
      "inspection_id": "660e8400-e29b-41d4-a716-446655440001",
      "lead_id": "550e8400-e29b-41d4-a716-446655440000",
      "recommended_system_size_kwp": 17.6,
      "estimated_panels": 32,
      "usable_roof_area_sqm": 127.9,
      "next_step": "roi_calculator",
      "created_at": "2025-12-05T10:30:00Z"
    },
    "isError": false
  }
}
```

**Error Response:**

```json
{
  "jsonrpc": "2.0",
  "id": "req_abc123",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Validation failed: roof_area_sqm must be greater than 0"
      }
    ],
    "isError": true,
    "errorCode": "VALIDATION_ERROR",
    "errorDetails": {
      "field": "roof_area_sqm",
      "constraint": "positive_number",
      "received": -10
    }
  }
}
```

---

## 3. Solar Use Cases

### 3.1 Site Inspection Workflow

**Trigger:** Agent arrives at customer location for site survey

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    SITE INSPECTION WORKFLOW                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. Agent opens mobile app                                               │
│     └─▶ AI assistant activated                                          │
│                                                                          │
│  2. Agent takes photos of:                                               │
│     ├─▶ Roof surface (multiple angles)                                  │
│     ├─▶ Electrical meter                                                 │
│     ├─▶ Inverter location                                                │
│     └─▶ Surrounding shading objects                                      │
│                                                                          │
│  3. AI processes images via site_inspection tool:                        │
│     ├─▶ Roof type detection (tile/concrete/metal)                        │
│     ├─▶ Orientation estimation (compass heading)                         │
│     ├─▶ Shading analysis (trees, buildings)                              │
│     └─▶ Area calculation (from satellite overlay)                        │
│                                                                          │
│  4. Agent confirms/adjusts AI suggestions                                │
│     └─▶ Structured data saved to Supabase                                │
│                                                                          │
│  5. Automatic trigger: roi_calculator                                    │
│     └─▶ Preliminary ROI shown to agent in real-time                      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Roof Measurement to ROI Calculation

**Trigger:** Site inspection completed

**Data Flow:**

```json
{
  "site_inspection_output": {
    "roof_area_sqm": 150.5,
    "usable_area_sqm": 127.9,
    "roof_orientation": "south",
    "roof_tilt_degrees": 15,
    "shading_factor": 0.15,
    "recommended_panels": 32,
    "panel_model": "JA Solar 550W",
    "total_capacity_kwp": 17.6
  }
}
```

**ROI Calculator Processing:**

1. **Annual Generation Estimate**
   - Base: 1,400 kWh/kWp/year (Malaysia average)
   - Adjusted for orientation: -5% (south-facing penalty)
   - Adjusted for shading: -15%
   - Final: 17.6 kWp × 1,400 × 0.95 × 0.85 = **19,894 kWh/year**

2. **Financial Projections**
   - Current TNB rate: RM 0.57/kWh
   - Annual savings: 19,894 × 0.57 = **RM 11,340/year**
   - NEM export rate: RM 0.31/kWh (for excess generation)

3. **Payback Calculation**
   - System cost: RM 3,800/kWp × 17.6 = RM 66,880
   - Annual savings: RM 11,340
   - Simple payback: **5.9 years**

### 3.3 Lead Qualification to Quotation to Follow-up

**End-to-End Workflow:**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LEAD-TO-CLOSE WORKFLOW                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 1: LEAD INTAKE                                              │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │ • Customer submits inquiry (web form / WhatsApp / call)          │   │
│  │ • lead_intake tool captures:                                      │   │
│  │   - Name, address, phone, email                                   │   │
│  │   - Property type (residential/commercial)                        │   │
│  │   - Monthly electricity bill range                                │   │
│  │   - Preferred contact time                                        │   │
│  │ • Lead score calculated (0-100)                                   │   │
│  │ • High-score leads auto-assigned to agents                        │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 2: SITE INSPECTION                                          │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │ • Agent schedules site visit                                      │   │
│  │ • site_inspection tool captures technical data                    │   │
│  │ • Photos uploaded to Supabase Storage                             │   │
│  │ • Structured inspection report generated                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 3: ROI CALCULATION                                          │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │ • roi_calculator processes site data                              │   │
│  │ • Multiple scenarios generated:                                   │   │
│  │   - Conservative (80% efficiency)                                 │   │
│  │   - Standard (100% efficiency)                                    │   │
│  │   - Optimistic (120% with battery)                                │   │
│  │ • Sensitivity analysis on tariff changes                          │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 4: QUOTATION                                                │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │ • quotation_builder generates documents:                          │   │
│  │   - Professional PDF quote                                        │   │
│  │   - Executive summary (1-pager)                                   │   │
│  │   - Technical specifications                                      │   │
│  │   - Terms and conditions                                          │   │
│  │ • Documents stored in Supabase, URLs sent to agent                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 5: FOLLOW-UP                                                │   │
│  ├──────────────────────────────────────────────────────────────────┤   │
│  │ • Automated reminder: 3 days after quote sent                     │   │
│  │ • Agent receives AI-generated follow-up script                    │   │
│  │ • Customer objections logged and addressed                        │   │
│  │ • Quote revision if needed (loops back to Stage 4)                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.4 Compliance / SEDA / Loan Documentation Use Cases

**SEDA Application Workflow:**

The Sustainable Energy Development Authority (SEDA) Malaysia requires specific documentation for Net Energy Metering (NEM) applications:

| Document | Source Tool | Auto-Generated |
|----------|-------------|----------------|
| Form A: Application Form | lead_intake + site_inspection | Yes |
| Single Line Diagram | site_inspection | Template-based |
| Roof Layout Drawing | site_inspection | Yes |
| Equipment Specifications | quotation_builder | Yes |
| Contractor License | External (manual upload) | No |
| TNB Bill Copy | lead_intake (attachment) | No |

**Loan Documentation Workflow:**

For customers requiring financing:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    LOAN DOCUMENTATION FLOW                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  quotation_builder generates:                                            │
│                                                                          │
│  1. Proforma Invoice                                                     │
│     └─▶ Required by all banks                                           │
│                                                                          │
│  2. System Specifications                                                │
│     └─▶ Panel brand, inverter, warranty details                         │
│                                                                          │
│  3. ROI Summary (Bank-formatted)                                         │
│     └─▶ Payback analysis for loan approval                              │
│                                                                          │
│  4. Installation Timeline                                                │
│     └─▶ Milestone-based payment schedule                                │
│                                                                          │
│  Bank-specific templates supported:                                      │
│  • Maybank Green Financing                                               │
│  • CIMB Solar Loan                                                       │
│  • Public Bank Renewable Energy Loan                                     │
│  • HSBC Green Equipment Finance                                          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Tools Overview

### Tools Overview Table

| Tool | Purpose | Input | Output | Downstream Dependency |
|------|---------|-------|--------|----------------------|
| `site_inspection` | Capture technical details of installation site | Images, roof type, measurements, shading data | Normalized JSON with roof specs, panel layout, recommended system size | Feeds `roi_calculator` |
| `roi_calculator` | Estimate payback period, annual savings, and financial metrics | `site_inspection` output OR manual input | ROI model with projections, sensitivity analysis | Feeds `quotation_builder` |
| `lead_intake` | Capture and qualify customer information | Name, address, contact info, property details, electricity bill | Structured customer profile with lead score | Can trigger `site_inspection` |
| `quotation_builder` | Transform ROI model into professional quote documents | ROI model, customer details, pricing | PDF/DOCX/PPTX documents, quote URLs | Connects to Qontrek Document Factory |

### Tool Details

#### 4.1 site_inspection

```yaml
name: site_inspection
version: 1.0.0
description: |
  Captures technical details of a solar installation site including
  roof specifications, panel layout recommendations, and shading analysis.

input_schema:
  type: object
  required:
    - lead_id
    - roof_type
    - roof_area_sqm
  properties:
    lead_id:
      type: string
      format: uuid
    roof_type:
      type: string
      enum: [concrete_flat, concrete_pitched, metal_deck, clay_tile, asphalt_shingle]
    roof_area_sqm:
      type: number
      minimum: 10
    roof_orientation:
      type: string
      enum: [north, south, east, west, northeast, northwest, southeast, southwest]
    roof_tilt_degrees:
      type: number
      minimum: 0
      maximum: 60
    shading_factor:
      type: number
      minimum: 0
      maximum: 1
    panel_layout:
      type: object
    images:
      type: array
      items:
        type: string
        format: uri

output_schema:
  type: object
  properties:
    inspection_id:
      type: string
      format: uuid
    usable_roof_area_sqm:
      type: number
    recommended_system_size_kwp:
      type: number
    recommended_panels:
      type: integer
    next_step:
      type: string
```

#### 4.2 roi_calculator

```yaml
name: roi_calculator
version: 1.0.0
description: |
  Calculates return on investment, payback period, and financial
  projections for a solar installation based on site data.

input_schema:
  type: object
  required:
    - system_size_kwp
  properties:
    site_inspection_id:
      type: string
      format: uuid
    system_size_kwp:
      type: number
      minimum: 1
    monthly_bill_myr:
      type: number
    tariff_rate_myr_kwh:
      type: number
      default: 0.57
    installation_cost_per_kwp:
      type: number
      default: 3800
    annual_degradation_rate:
      type: number
      default: 0.005
    projection_years:
      type: integer
      default: 25

output_schema:
  type: object
  properties:
    roi_id:
      type: string
      format: uuid
    estimated_annual_generation_kwh:
      type: number
    annual_savings_myr:
      type: number
    total_cost_myr:
      type: number
    payback_period_years:
      type: number
    roi_percentage:
      type: number
    year_by_year_projection:
      type: array
```

#### 4.3 lead_intake

```yaml
name: lead_intake
version: 1.0.0
description: |
  Captures and qualifies customer information for solar installation
  leads, including contact details and property information.

input_schema:
  type: object
  required:
    - customer_name
    - address
  properties:
    customer_name:
      type: string
    address:
      type: string
    contact_phone:
      type: string
    contact_email:
      type: string
      format: email
    property_type:
      type: string
      enum: [residential, commercial, industrial]
    monthly_electricity_bill_myr:
      type: number
    preferred_contact_time:
      type: string
    notes:
      type: string

output_schema:
  type: object
  properties:
    lead_id:
      type: string
      format: uuid
    lead_score:
      type: integer
      minimum: 0
      maximum: 100
    qualification_status:
      type: string
      enum: [hot, warm, cold, disqualified]
    recommended_next_action:
      type: string
```

#### 4.4 quotation_builder

```yaml
name: quotation_builder
version: 1.0.0
description: |
  Generates professional quotation documents from ROI calculations,
  producing PDF, DOCX, or PPTX formats via Qontrek Document Factory.

input_schema:
  type: object
  required:
    - roi_calculation_id
  properties:
    roi_calculation_id:
      type: string
      format: uuid
    output_formats:
      type: array
      items:
        type: string
        enum: [pdf, docx, pptx]
      default: [pdf]
    template_id:
      type: string
      default: standard
    include_sections:
      type: array
      items:
        type: string
        enum: [executive_summary, technical_specs, roi_analysis, terms_conditions, payment_schedule]
    validity_days:
      type: integer
      default: 30
    custom_pricing:
      type: object

output_schema:
  type: object
  properties:
    quotation_id:
      type: string
      format: uuid
    quote_number:
      type: string
    total_amount_myr:
      type: number
    valid_until:
      type: string
      format: date
    document_urls:
      type: object
      properties:
        pdf:
          type: string
          format: uri
        docx:
          type: string
          format: uri
        pptx:
          type: string
          format: uri
```

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol - A standard for AI model interaction with external tools |
| **kWp** | Kilowatt-peak - Maximum power output of a solar system under standard test conditions |
| **NEM** | Net Energy Metering - Program allowing solar owners to export excess energy to the grid |
| **SEDA** | Sustainable Energy Development Authority Malaysia |
| **TNB** | Tenaga Nasional Berhad - Malaysia's national electricity utility |
| **ROI** | Return on Investment |
| **RLS** | Row Level Security - Supabase feature for data access control |

---

## Appendix B: Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial specification |
