# Solar MCP Toolpack Data Flows

## Overview

This document describes the data flows between tools in the Solar MCP Toolpack, including input/output mappings, data transformations, and storage patterns.

## Primary Data Flow: Lead to Quote

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         LEAD-TO-QUOTE DATA FLOW                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ┌─────────────────┐                                                          │
│  │   LEAD_INTAKE   │                                                          │
│  │                 │                                                          │
│  │  Input:         │                                                          │
│  │  • customer_name│                                                          │
│  │  • address      │                                                          │
│  │  • contact_info │                                                          │
│  │  • bill_amount  │                                                          │
│  │                 │                                                          │
│  │  Output:        │                                                          │
│  │  • lead_id ─────┼────────────────────────────────────────────────┐        │
│  │  • lead_score   │                                                 │        │
│  │  • qualification│                                                 │        │
│  └────────┬────────┘                                                 │        │
│           │                                                          │        │
│           │ lead_id                                                  │        │
│           ▼                                                          │        │
│  ┌─────────────────┐                                                 │        │
│  │SITE_INSPECTION  │                                                 │        │
│  │                 │                                                 │        │
│  │  Input:         │                                                 │        │
│  │  • lead_id ◀────┼─────────────────────────────────────────────────┘        │
│  │  • roof_type    │                                                          │
│  │  • roof_area    │                                                          │
│  │  • orientation  │                                                          │
│  │  • shading      │                                                          │
│  │  • images[]     │                                                          │
│  │                 │                                                          │
│  │  Output:        │                                                          │
│  │  • inspection_id┼───────────────────────────────────────────┐             │
│  │  • usable_area  │                                            │             │
│  │  • system_size  │                                            │             │
│  │  • panel_count  │                                            │             │
│  │  • efficiency   │                                            │             │
│  └────────┬────────┘                                            │             │
│           │                                                      │             │
│           │ inspection_id + derived values                       │             │
│           ▼                                                      │             │
│  ┌─────────────────┐                                            │             │
│  │ ROI_CALCULATOR  │                                            │             │
│  │                 │                                            │             │
│  │  Input:         │                                            │             │
│  │  • inspection_id◀────────────────────────────────────────────┘             │
│  │  • system_size  │  (from inspection output)                                │
│  │  • shading      │  (from inspection output)                                │
│  │  • orientation  │  (from inspection output)                                │
│  │  • tariff_rate  │  (default or override)                                   │
│  │  • cost_per_kwp │  (default or override)                                   │
│  │                 │                                                          │
│  │  Output:        │                                                          │
│  │  • roi_id ──────┼───────────────────────────────────────────┐             │
│  │  • annual_gen   │                                            │             │
│  │  • savings      │                                            │             │
│  │  • payback      │                                            │             │
│  │  • npv/irr      │                                            │             │
│  │  • projections[]│                                            │             │
│  └────────┬────────┘                                            │             │
│           │                                                      │             │
│           │ roi_id + financial data                              │             │
│           ▼                                                      │             │
│  ┌─────────────────┐                                            │             │
│  │QUOTATION_BUILDER│                                            │             │
│  │                 │                                            │             │
│  │  Input:         │                                            │             │
│  │  • roi_id ◀─────┼────────────────────────────────────────────┘             │
│  │  • formats[]    │                                                          │
│  │  • template_id  │                                                          │
│  │  • sections[]   │                                                          │
│  │  • pricing      │  (optional overrides)                                    │
│  │                 │                                                          │
│  │  Output:        │                                                          │
│  │  • quotation_id │                                                          │
│  │  • quote_number │                                                          │
│  │  • document_urls│                                                          │
│  │  • total_amount │                                                          │
│  └─────────────────┘                                                          │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Data Transformation Details

### Lead Intake → Site Inspection

```json
// Lead Intake Output
{
  "lead_id": "550e8400-...",
  "customer_name": "Ahmad bin Abdullah",
  "address": "123 Jalan Maju, 47810 Petaling Jaya",
  "monthly_electricity_bill_myr": 650,
  "estimated_system_size_kwp": 10.5
}

// Transformed to Site Inspection Input
{
  "lead_id": "550e8400-...",  // Direct reference
  // Agent manually adds:
  "roof_type": "concrete_flat",
  "roof_area_sqm": 150.5,
  "roof_orientation": "south",
  "shading_factor": 0.15
}
```

**Transformation Notes:**
- `lead_id` passed directly as reference
- `estimated_system_size_kwp` used as guidance, not binding
- Site-specific data collected during physical inspection

### Site Inspection → ROI Calculator

```json
// Site Inspection Output
{
  "inspection_id": "660e8400-...",
  "lead_id": "550e8400-...",
  "usable_roof_area_sqm": 127.9,
  "recommended_system_size_kwp": 17.6,
  "recommended_panels": 32,
  "efficiency_factors": {
    "orientation_factor": 0.95,
    "tilt_factor": 0.98,
    "shading_factor": 0.85,
    "combined_efficiency": 0.79
  }
}

// Auto-transformed to ROI Calculator Input
{
  "site_inspection_id": "660e8400-...",  // Direct reference
  "system_size_kwp": 17.6,               // From inspection
  "shading_factor": 0.15,                // From inspection
  "orientation_factor": 0.95             // Calculated
  // Defaults applied for:
  // - tariff_rate_myr_kwh: 0.57
  // - installation_cost_per_kwp: 3800
}
```

**Transformation Notes:**
- `site_inspection_id` enables data lineage
- Efficiency factors combined into adjustment multipliers
- Financial defaults can be overridden

### ROI Calculator → Quotation Builder

```json
// ROI Calculator Output
{
  "roi_id": "770e8400-...",
  "site_inspection_id": "660e8400-...",
  "financial_summary": {
    "total_cost_myr": 66880,
    "annual_savings_myr": 11340,
    "payback_period_years": 5.9,
    "lifetime_savings_myr": 425000
  },
  "system_specifications": {
    "system_size_kwp": 17.6,
    "estimated_panels": 32
  }
}

// Auto-transformed to Quotation Builder Input
{
  "roi_calculation_id": "770e8400-...",  // Direct reference
  "output_formats": ["pdf"],             // User specified
  "template_id": "standard"              // Default or user specified
  // Pricing pulled from ROI calculation
  // Customer details pulled from Lead via reference chain
}
```

**Transformation Notes:**
- Quote builder retrieves full customer details via reference chain
- Financial data embedded in quote document
- System specs included in technical section

## Data Storage Schema

### Database Tables

```sql
-- Leads Table
CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_name TEXT NOT NULL,
    address TEXT NOT NULL,
    contact_phone TEXT,
    contact_email TEXT,
    property_type TEXT,
    monthly_electricity_bill_myr DECIMAL,
    lead_score INTEGER,
    qualification_status TEXT,
    assigned_agent_id UUID REFERENCES agents(id),
    status TEXT DEFAULT 'new',
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Site Inspections Table
CREATE TABLE site_inspections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) NOT NULL,
    roof_type TEXT NOT NULL,
    roof_area_sqm DECIMAL NOT NULL,
    usable_area_sqm DECIMAL,
    roof_orientation TEXT,
    roof_tilt_degrees DECIMAL,
    shading_factor DECIMAL,
    panel_layout JSONB,
    efficiency_factors JSONB,
    recommended_system_size_kwp DECIMAL,
    recommended_panels INTEGER,
    images TEXT[],
    inspector_notes TEXT,
    inspector_id UUID REFERENCES agents(id),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ROI Calculations Table
CREATE TABLE roi_calculations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    site_inspection_id UUID REFERENCES site_inspections(id),
    lead_id UUID REFERENCES leads(id),
    system_size_kwp DECIMAL NOT NULL,
    total_cost_myr DECIMAL,
    estimated_annual_generation_kwh DECIMAL,
    annual_savings_myr DECIMAL,
    payback_period_years DECIMAL,
    npv_myr DECIMAL,
    irr_percentage DECIMAL,
    roi_percentage DECIMAL,
    year_by_year_projection JSONB,
    sensitivity_analysis JSONB,
    assumptions JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Quotations Table
CREATE TABLE quotations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    roi_calculation_id UUID REFERENCES roi_calculations(id) NOT NULL,
    lead_id UUID REFERENCES leads(id),
    quote_number TEXT UNIQUE NOT NULL,
    quote_version INTEGER DEFAULT 1,
    total_amount_myr DECIMAL NOT NULL,
    discount_myr DECIMAL DEFAULT 0,
    tax_myr DECIMAL DEFAULT 0,
    pricing_breakdown JSONB,
    valid_until DATE,
    document_urls JSONB,
    template_id TEXT,
    status TEXT DEFAULT 'draft',
    sent_at TIMESTAMPTZ,
    viewed_at TIMESTAMPTZ,
    response_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

### Data Relationships

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ENTITY RELATIONSHIP DIAGRAM                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌─────────────┐         ┌──────────────────┐                              │
│   │    leads    │────────<│  site_inspections │                              │
│   │             │   1:N   │                   │                              │
│   │ • id (PK)   │         │ • id (PK)         │                              │
│   │ • name      │         │ • lead_id (FK)    │                              │
│   │ • address   │         │ • roof_data       │                              │
│   │ • score     │         │ • recommendations │                              │
│   └──────┬──────┘         └─────────┬─────────┘                              │
│          │                          │                                        │
│          │                          │ 1:N                                    │
│          │                          ▼                                        │
│          │                ┌──────────────────┐                              │
│          │                │  roi_calculations │                              │
│          │         1:N    │                   │                              │
│          └───────────────>│ • id (PK)         │                              │
│                           │ • inspection_id   │                              │
│                           │ • lead_id (FK)    │                              │
│                           │ • financials      │                              │
│                           └─────────┬─────────┘                              │
│                                     │                                        │
│                                     │ 1:N                                    │
│                                     ▼                                        │
│                           ┌──────────────────┐                              │
│                           │    quotations    │                              │
│                           │                  │                              │
│                           │ • id (PK)        │                              │
│                           │ • roi_id (FK)    │                              │
│                           │ • lead_id (FK)   │                              │
│                           │ • documents      │                              │
│                           └──────────────────┘                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Partial Workflows

### Quick Estimate (Without Site Inspection)

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ lead_intake │────▶│  roi_calculator │────▶│ quotation_builder│
└─────────────┘     └─────────────────┘     └──────────────────┘
                            │
                            │ site_inspection_id = NULL
                            │ system_size = estimated from bill
                            ▼
                    ┌─────────────────┐
                    │  Defaults Used: │
                    │  • shading: 0   │
                    │  • orient: 1.0  │
                    │  • efficiency:  │
                    │    0.8 (generic)│
                    └─────────────────┘
```

**Use Case:** Customer wants ballpark estimate before committing to site visit

### Re-Quote (Updated Pricing)

```
┌─────────────────┐     ┌──────────────────┐
│  roi_calculator │────▶│ quotation_builder│
│  (existing)     │     │  (new version)   │
└─────────────────┘     └──────────────────┘
         │
         │ Same roi_id, different quote_number
         ▼
┌─────────────────────────────────────────┐
│  quotation.quote_version = 2            │
│  quotation.custom_pricing = {           │
│    "discount_percentage": 10,           │
│    "discount_reason": "Year-end promo"  │
│  }                                      │
└─────────────────────────────────────────┘
```

**Use Case:** Price negotiation, promotional offers

### Site Re-Inspection

```
┌──────────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ site_inspection  │────▶│  roi_calculator │────▶│ quotation_builder│
│ (new inspection) │     │  (recalculated) │     │  (supersedes old)│
└──────────────────┘     └─────────────────┘     └──────────────────┘
         │
         │ Same lead_id, new inspection_id
         │ Previous quote marked "superseded"
         ▼
┌─────────────────────────────────────────┐
│  Maintains audit trail:                 │
│  • Old inspection preserved             │
│  • Old quote preserved (status changed) │
│  • New chain created                    │
└─────────────────────────────────────────┘
```

**Use Case:** Customer made roof modifications, initial survey was inaccurate

## Data Validation Rules

### Cross-Tool Validation

| Source Field | Target Tool | Validation Rule |
|--------------|-------------|-----------------|
| `lead.monthly_bill_myr` | `roi_calculator` | If provided, must match consumption pattern |
| `inspection.system_size_kwp` | `roi_calculator` | Must be within 10% of ROI input if both present |
| `roi.total_cost_myr` | `quotation` | Quote total must equal ROI cost ± custom pricing |
| `inspection.images[]` | All downstream | URLs must be accessible Supabase storage links |

### Required Data by Stage

| Stage | Required Data | Optional Data |
|-------|--------------|---------------|
| Lead Intake | name, address | phone, email, bill, timeline |
| Site Inspection | lead_id, roof_type, roof_area | orientation, shading, images |
| ROI Calculator | system_size | inspection_id, custom tariffs |
| Quote Builder | roi_calculation_id | custom pricing, template |

## Event-Driven Updates

### Cascade Events

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EVENT CASCADE FLOW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────┐                                                        │
│  │ Lead Status      │                                                        │
│  │ Changed to       │                                                        │
│  │ "site_visit_     │                                                        │
│  │  completed"      │                                                        │
│  └────────┬─────────┘                                                        │
│           │                                                                  │
│           │ Triggers                                                         │
│           ▼                                                                  │
│  ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐    │
│  │ Webhook:         │────▶│ Auto-calculate   │────▶│ Notify agent:    │    │
│  │ inspection.      │     │ ROI if site data │     │ "ROI ready for   │    │
│  │ completed        │     │ is complete      │     │  review"         │    │
│  └──────────────────┘     └──────────────────┘     └──────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Webhook Payloads

```json
// lead.qualified event
{
  "event": "lead.qualified",
  "timestamp": "2025-12-05T10:30:00Z",
  "data": {
    "lead_id": "550e8400-...",
    "qualification_status": "hot",
    "lead_score": 85,
    "recommended_action": "Schedule site inspection within 48 hours"
  }
}

// quote.viewed event
{
  "event": "quote.viewed",
  "timestamp": "2025-12-05T14:00:00Z",
  "data": {
    "quotation_id": "880e8400-...",
    "quote_number": "QT-2025-00042",
    "lead_id": "550e8400-...",
    "viewed_by_ip": "203.xxx.xxx.xxx",
    "time_on_page_seconds": 180
  }
}
```

## Data Retention

| Data Type | Retention Period | Archive Policy |
|-----------|-----------------|----------------|
| Active leads | Indefinite | N/A |
| Lost/disqualified leads | 2 years | Move to archive table |
| Site inspections | Indefinite | N/A |
| ROI calculations | Indefinite | N/A |
| Generated documents | 7 years | Move to cold storage |
| Audit logs | 3 years | Compress and archive |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial data flows documentation |
