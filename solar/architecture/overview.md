# Solar MCP Toolpack Architecture Overview

## Introduction

The Solar MCP Toolpack is a domain-specific collection of Model Context Protocol (MCP) tools designed for the Malaysian solar installation sales and operations market. This document provides a comprehensive overview of the solar vertical architecture, toolchain flow, and integration points with the Qontrek Engine.

---

## Solar Vertical Overview

### Purpose

The Solar vertical enables AI agents to automate the complete solar sales cycle—from lead capture through quotation delivery—using structured, schema-validated tools that integrate with enterprise backend systems.

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Lead Management** | Capture, score, and qualify solar prospects |
| **Site Assessment** | Technical evaluation of installation sites |
| **Financial Modeling** | ROI calculations with 25-year projections |
| **Document Generation** | Professional quotes in PDF/DOCX/PPTX/XLSX |

### Market Context (Malaysia)

- **Currency**: Malaysian Ringgit (MYR)
- **Tariff Provider**: TNB (Tenaga Nasional Berhad)
- **Default Tariff Rate**: RM 0.57/kWh
- **NEM Export Rate**: RM 0.31/kWh
- **Average Installation Cost**: RM 3,800/kWp
- **Solar Irradiance**: ~1,600 kWh/m²/year

---

## System Architecture

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              AI AGENT LAYER                                       │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                        LLM (Claude, GPT, etc.)                              │  │
│  │                                                                             │  │
│  │    • Natural language understanding     • Context management                │  │
│  │    • Tool selection & orchestration     • Multi-turn conversations          │  │
│  └─────────────────────────────────┬───────────────────────────────────────────┘  │
│                                    │ MCP Protocol (JSON-RPC 2.0)                  │
│                                    ▼                                              │
├───────────────────────────────────────────────────────────────────────────────────┤
│                           MCP TOOLPACK LAYER                                      │
│  ┌────────────────────────────────────────────────────────────────────────────┐  │
│  │                        Solar MCP Server                                     │  │
│  │                                                                             │  │
│  │   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌────────────┐  │  │
│  │   │  lead_intake │   │    site_     │   │     roi_     │   │ quotation_ │  │  │
│  │   │              │   │  inspection  │   │  calculator  │   │   builder  │  │  │
│  │   │   (B1.1)     │   │    (B1.2)    │   │    (B1.3)    │   │   (B1.4)   │  │  │
│  │   └──────┬───────┘   └───────┬──────┘   └───────┬──────┘   └──────┬─────┘  │  │
│  │          │                   │                  │                 │        │  │
│  │          └───────────────────┴──────────────────┴─────────────────┘        │  │
│  │                                      │                                      │  │
│  └──────────────────────────────────────┼──────────────────────────────────────┘  │
│                                         │                                         │
├─────────────────────────────────────────┼─────────────────────────────────────────┤
│                          QONTREK ENGINE LAYER                                     │
│                                         │                                         │
│    ┌────────────────────────────────────┼────────────────────────────────────┐   │
│    │                                    ▼                                     │   │
│    │  ┌──────────────┐   ┌───────────────────┐   ┌─────────────────────────┐ │   │
│    │  │   Supabase   │   │      Qontrek      │   │       FireCrawl         │ │   │
│    │  │              │   │  Document Factory │   │      (Optional)         │ │   │
│    │  │ ┌──────────┐ │   │                   │   │                         │ │   │
│    │  │ │ Postgres │ │   │  • PDF Rendering  │   │  • Web Scraping         │ │   │
│    │  │ │   + RLS  │ │   │  • DOCX Templates │   │  • Lead Enrichment      │ │   │
│    │  │ ├──────────┤ │   │  • PPTX Slides    │   │  • Competitor Analysis  │ │   │
│    │  │ │ Storage  │ │   │  • XLSX Reports   │   │                         │ │   │
│    │  │ ├──────────┤ │   │                   │   └─────────────────────────┘ │   │
│    │  │ │Edge Func │ │   │  API: /v1/docs    │                               │   │
│    │  │ └──────────┘ │   └───────────────────┘                               │   │
│    │  └──────────────┘                                                        │   │
│    └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## Toolchain Flow Diagram

### Primary Workflow: Full Sales Cycle

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           SOLAR SALES TOOLCHAIN FLOW                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│    ENTRY POINT                                                                       │
│         │                                                                            │
│         ▼                                                                            │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  STAGE 1: LEAD_INTAKE                                                        │  │
│    │                                                                              │  │
│    │  INPUT                           PROCESS                  OUTPUT             │  │
│    │  ┌─────────────────┐             ┌───────────┐           ┌───────────────┐  │  │
│    │  │ • customer_name │────────────▶│ Scoring   │──────────▶│ • lead_id     │  │  │
│    │  │ • address       │             │ Engine    │           │ • lead_score  │  │  │
│    │  │ • contact_info  │             │           │           │ • qual_status │  │  │
│    │  │ • monthly_bill  │             │ ┌───────┐ │           │ • est_system  │  │  │
│    │  │ • property_type │             │ │Supabase│ │           │ • next_action │  │  │
│    │  │ • timeline      │             │ └───────┘ │           └───────┬───────┘  │  │
│    │  └─────────────────┘             └───────────┘                   │          │  │
│    └─────────────────────────────────────────────────────────────────┬┘          │  │
│                                                                      │            │  │
│                                                       lead_id ───────┘            │  │
│                                                                                   │  │
│                                                       ▼                           │  │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  STAGE 2: SITE_INSPECTION                                                    │  │
│    │                                                                              │  │
│    │  INPUT                           PROCESS                  OUTPUT             │  │
│    │  ┌─────────────────┐             ┌───────────┐           ┌───────────────┐  │  │
│    │  │ • lead_id       │────────────▶│ Layout &  │──────────▶│ • inspect_id  │  │  │
│    │  │ • roof_type     │             │ Sizing    │           │ • usable_area │  │  │
│    │  │ • roof_area_sqm │             │ Calculator│           │ • system_size │  │  │
│    │  │ • orientation   │             │           │           │ • panel_count │  │  │
│    │  │ • shading_info  │             │ ┌───────┐ │           │ • efficiency  │  │  │
│    │  │ • images[]      │             │ │Storage│ │           │ • complexity  │  │  │
│    │  │ • electrical    │             │ └───────┘ │           └───────┬───────┘  │  │
│    │  └─────────────────┘             └───────────┘                   │          │  │
│    └─────────────────────────────────────────────────────────────────┬┘          │  │
│                                                                      │            │  │
│                                                inspection_id + ──────┘            │  │
│                                                efficiency_factors                 │  │
│                                                       ▼                           │  │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  STAGE 3: ROI_CALCULATOR                                                     │  │
│    │                                                                              │  │
│    │  INPUT                           PROCESS                  OUTPUT             │  │
│    │  ┌─────────────────┐             ┌───────────┐           ┌───────────────┐  │  │
│    │  │ • inspection_id │────────────▶│ Financial │──────────▶│ • roi_id      │  │  │
│    │  │ • system_size   │             │ Engine    │           │ • annual_gen  │  │  │
│    │  │ • tariff_rate   │             │           │           │ • savings     │  │  │
│    │  │ • cost_per_kwp  │             │ ┌───────┐ │           │ • payback_yrs │  │  │
│    │  │ • shading_factor│             │ │ Cache │ │           │ • NPV/IRR     │  │  │
│    │  │ • financing     │             │ │ (1hr) │ │           │ • projections │  │  │
│    │  │ • proj_years    │             │ └───────┘ │           └───────┬───────┘  │  │
│    │  └─────────────────┘             └───────────┘                   │          │  │
│    └─────────────────────────────────────────────────────────────────┬┘          │  │
│                                                                      │            │  │
│                                                  roi_calculation_id ─┘            │  │
│                                                  [REQUIRED]                       │  │
│                                                       ▼                           │  │
│    ┌─────────────────────────────────────────────────────────────────────────────┐  │
│    │  STAGE 4: QUOTATION_BUILDER                                                  │  │
│    │                                                                              │  │
│    │  INPUT                           PROCESS                  OUTPUT             │  │
│    │  ┌─────────────────┐             ┌───────────┐           ┌───────────────┐  │  │
│    │  │ • roi_calc_id   │────────────▶│ Qontrek   │──────────▶│ • quote_id    │  │  │
│    │  │ • output_formats│             │ Document  │           │ • quote_num   │  │  │
│    │  │ • template_id   │             │ Factory   │           │ • doc_urls{}  │  │  │
│    │  │ • sections[]    │             │           │           │ • total_amt   │  │  │
│    │  │ • custom_pricing│             │ ┌───────┐ │           │ • validity    │  │  │
│    │  │ • branding      │             │ │Webhook│ │           │ • share_link  │  │  │
│    │  │ • language      │             │ └───────┘ │           └───────────────┘  │  │
│    │  └─────────────────┘             └───────────┘                              │  │
│    └─────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                      │
│    EXIT POINT (Terminal Node)                                                        │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

### Alternative Workflows

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                           ALTERNATIVE WORKFLOW PATHS                                │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  1. QUICK ESTIMATE (Skip Site Inspection)                                           │
│     ────────────────────────────────────────                                        │
│                                                                                     │
│     lead_intake ──────────────────▶ roi_calculator ──────────▶ quotation_builder   │
│                                           │                                         │
│                                    Uses defaults:                                   │
│                                    • efficiency = 0.8                               │
│                                    • shading = 0                                    │
│                                    • orientation = 1.0                              │
│                                                                                     │
│  2. RE-QUOTE (Price Revision)                                                       │
│     ─────────────────────────                                                       │
│                                                                                     │
│     [existing roi_calculator] ──────────────────▶ quotation_builder                │
│                                                          │                          │
│                                                   Creates new version:              │
│                                                   • Same roi_id                     │
│                                                   • New quote_number                │
│                                                   • Custom pricing applied          │
│                                                                                     │
│  3. SITE RE-INSPECTION (Updated Assessment)                                         │
│     ───────────────────────────────────────                                         │
│                                                                                     │
│     site_inspection ──────▶ roi_calculator ──────▶ quotation_builder               │
│     (new inspection)        (recalculated)         (supersedes old)                │
│           │                                                                         │
│     Same lead_id, new inspection_id                                                │
│     Old quote status → "superseded"                                                │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Integration Points with Qontrek Engine

### 1. Supabase Integration (Primary Data Layer)

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                        SUPABASE INTEGRATION ARCHITECTURE                            │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                           POSTGRESQL DATABASE                                │   │
│  │                                                                              │   │
│  │   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │   │
│  │   │    leads     │    │    site_     │    │     roi_     │    │quotations│  │   │
│  │   │              │◀───│  inspections │◀───│ calculations │◀───│          │  │   │
│  │   │ • customer   │    │              │    │              │    │ • pricing│  │   │
│  │   │ • scoring    │    │ • roof_data  │    │ • financials │    │ • docs   │  │   │
│  │   │ • assignment │    │ • images     │    │ • projections│    │ • status │  │   │
│  │   └──────────────┘    └──────────────┘    └──────────────┘    └──────────┘  │   │
│  │         │                    │                   │                  │        │   │
│  │         └────────────────────┴───────────────────┴──────────────────┘        │   │
│  │                                      │                                       │   │
│  │                           Row-Level Security (RLS)                           │   │
│  │                                      │                                       │   │
│  │                     ┌────────────────┴────────────────┐                      │   │
│  │                     │                                 │                      │   │
│  │              ┌──────▼──────┐                   ┌──────▼──────┐               │   │
│  │              │   agents    │                   │organizations│               │   │
│  │              │             │                   │             │               │   │
│  │              │ • user_id   │                   │ • company   │               │   │
│  │              │ • role      │                   │ • settings  │               │   │
│  │              │ • region    │                   │ • branding  │               │   │
│  │              └─────────────┘                   └─────────────┘               │   │
│  │                                                                              │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                            STORAGE BUCKETS                                   │   │
│  │                                                                              │   │
│  │   ┌──────────────────────┐              ┌──────────────────────┐            │   │
│  │   │  inspection-images   │              │ quotation-documents  │            │   │
│  │   │                      │              │                      │            │   │
│  │   │  • roof_overview.jpg │              │  • QT-2025-00042.pdf │            │   │
│  │   │  • meter_photo.jpg   │              │  • QT-2025-00042.docx│            │   │
│  │   │  • shading_source.jpg│              │  • QT-2025-00042.pptx│            │   │
│  │   └──────────────────────┘              └──────────────────────┘            │   │
│  │                                                                              │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
└────────────────────────────────────────────────────────────────────────────────────┘
```

**Connection Details:**

| Parameter | Value |
|-----------|-------|
| Environment Variable | `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY` |
| Connection Pool | PgBouncer (managed) |
| Region | Singapore (ap-southeast-1) |
| RLS Enabled | Yes |

### 2. Qontrek Document Factory Integration

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                     QONTREK DOCUMENT FACTORY INTEGRATION                            │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  quotation_builder                         Qontrek Document Factory                 │
│        │                                            │                               │
│        │  1. POST /v1/documents                     │                               │
│        │     {                                      │                               │
│        │       "template_id": "standard",           │                               │
│        │       "format": ["pdf", "docx"],           │                               │
│        │       "data": { ... },                     │                               │
│        │       "callback_url": "..."                │                               │
│        │     }                                      │                               │
│        ├────────────────────────────────────────────▶                               │
│        │                                            │                               │
│        │  2. Response (Immediate)                   │                               │
│        │     {                                      │                               │
│        │       "job_id": "qdf-xxx",                 │                               │
│        │       "status": "processing"               │                               │
│        │     }                                      │                               │
│        ◀────────────────────────────────────────────┤                               │
│        │                                            │                               │
│        │  3. Webhook POST (Async)                   │                               │
│        │     X-Qontrek-Signature: sha256=...        │                               │
│        │     {                                      │                               │
│        │       "event": "document.ready",           │                               │
│        │       "job_id": "qdf-xxx",                 │                               │
│        │       "document_urls": {                   │                               │
│        │         "pdf": "https://...",              │                               │
│        │         "docx": "https://..."              │                               │
│        │       }                                    │                               │
│        │     }                                      │                               │
│        ◀────────────────────────────────────────────┤                               │
│        │                                            │                               │
└────────┴────────────────────────────────────────────┴───────────────────────────────┘
```

**API Configuration:**

| Parameter | Value |
|-----------|-------|
| Endpoint | `https://api.qontrek.com/v1/documents` |
| Authentication | Bearer Token (`QONTREK_API_KEY`) |
| Timeout | 30 seconds |
| Retry Policy | 3 retries with exponential backoff |
| Webhook Signature | HMAC-SHA256 (`X-Qontrek-Signature`) |

**Available Templates:**

| Template ID | Use Case | Output Formats |
|-------------|----------|----------------|
| `standard` | General residential | PDF, DOCX |
| `premium` | High-value clients | PDF, DOCX, PPTX |
| `commercial` | B2B / Industrial | PDF, DOCX, XLSX |
| `minimal` | Quick estimates | PDF |

### 3. Webhook Events System

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│                              WEBHOOK EVENT FLOW                                     │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  Tool Execution                    Event Bus                    External Systems    │
│        │                              │                               │             │
│        │  lead.created               │                               │             │
│        ├─────────────────────────────▶                               │             │
│        │                              │                               │             │
│        │  lead.qualified              │                               │             │
│        ├─────────────────────────────▶  ─────────────────────────────▶  CRM        │
│        │                              │                               │             │
│        │  inspection.completed        │                               │             │
│        ├─────────────────────────────▶  ─────────────────────────────▶  Scheduler  │
│        │                              │                               │             │
│        │  quote.generated             │                               │             │
│        ├─────────────────────────────▶  ─────────────────────────────▶  Analytics  │
│        │                              │                               │             │
│        │  quote.viewed                │                               │             │
│        ├─────────────────────────────▶  ─────────────────────────────▶  Sales Ops  │
│        │                              │                               │             │
│        │  quote.accepted              │                               │             │
│        ├─────────────────────────────▶  ─────────────────────────────▶  ERP        │
│        │                              │                               │             │
└────────┴──────────────────────────────┴───────────────────────────────┴─────────────┘
```

**Webhook Payload Structure:**

```json
{
  "event": "quote.generated",
  "timestamp": "2025-12-05T10:30:00Z",
  "signature": "sha256=...",
  "data": {
    "quotation_id": "880e8400-e29b-41d4-a716-446655440003",
    "quote_number": "QT-2025-00042",
    "lead_id": "550e8400-e29b-41d4-a716-446655440000",
    "total_amount_myr": 66880,
    "document_urls": {
      "pdf": "https://storage.supabase.co/..."
    }
  }
}
```

---

## Design Principles

### 1. Stateless Tool Execution

Each tool invocation is self-contained with no session state:

```
INPUT ──▶ VALIDATION ──▶ EXECUTION ──▶ OUTPUT
                              │
                              ▼
                         [Supabase]
                        (Persistent State)
```

### 2. Schema-First Design

All tools defined by JSON Schema before implementation:

```
schemas/                          tools/
├── lead_intake.schema.json   →   ├── lead_intake.json
├── site_inspection.schema.json → ├── site_inspection.json
├── roi_calculator.schema.json →  ├── roi_calculator.json
└── quotation_builder.schema.json → └── quotation_builder.json
```

### 3. Tool Chaining via UUID References

```json
{
  "lead_id": "550e8400-e29b-41d4-a716-446655440000",
  "inspection_id": "660e8400-e29b-41d4-a716-446655440001",
  "roi_id": "770e8400-e29b-41d4-a716-446655440002",
  "quotation_id": "880e8400-e29b-41d4-a716-446655440003"
}
```

### 4. Edge-Function Compatibility

| Constraint | Limit | Design Accommodation |
|------------|-------|---------------------|
| Cold start | < 500ms | Minimal dependencies |
| Execution | < 10s per tool | Async for heavy ops |
| Memory | < 128MB | Streaming for files |
| Bundle | < 50KB | Tree-shaking |

---

## Security Architecture

### Authentication & Authorization

```
┌──────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────┐
│  Client  │───▶│  API Gateway │───▶│  MCP Server │───▶│ Supabase │
└──────────┘    └──────────────┘    └─────────────┘    └──────────┘
                      │                    │
               Bearer Token           Service Key
               Validation              (RLS Bypass)
                      │                    │
                      ▼                    ▼
              ┌──────────────┐     ┌───────────────┐
              │   Supabase   │     │  Row-Level    │
              │     Auth     │     │   Security    │
              └──────────────┘     └───────────────┘
```

### Data Protection Matrix

| Data Type | Protection |
|-----------|------------|
| Customer PII | Encrypted at rest, masked in logs |
| API Keys | Environment variables only |
| Documents | Signed URLs with expiration |
| Webhooks | HMAC-SHA256 verification |

---

## Environment Configuration

### Required Variables

```bash
# Supabase (Required)
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...

# Qontrek Document Factory (Required for quotes)
QONTREK_API_KEY=qk_...

# Optional
FIRECRAWL_API_KEY=fc_...
QONTREK_WEBHOOK_SECRET=whsec_...
LOG_LEVEL=info
```

### MCP Server Configuration

```json
{
  "mcpServers": {
    "solar": {
      "command": "npx",
      "args": ["-y", "@qontrek/solar-mcp-server"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_ANON_KEY": "${SUPABASE_ANON_KEY}",
        "QONTREK_API_KEY": "${QONTREK_API_KEY}"
      }
    }
  }
}
```

---

## Performance Characteristics

### Tool Execution Profile

| Tool | Timeout | Rate Limit | Cacheable |
|------|---------|------------|-----------|
| lead_intake | 5s | 100/min, 5000/day | No |
| site_inspection | 10s | 30/min, 500/day | No |
| roi_calculator | 5s | 60/min, 1000/day | Yes (1h TTL) |
| quotation_builder | 30s | 20/min, 200/day | No |

### Caching Strategy

| Data | Location | TTL | Invalidation |
|------|----------|-----|--------------|
| Tariff rates | Edge | 24h | Manual |
| Equipment catalog | Edge | 1h | On update |
| ROI calculations | Database | 1h | On input change |
| Generated docs | Storage | Permanent | Versioned |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2025-12-05 | Enhanced Qontrek Engine integration documentation |
| 1.0.0 | 2025-12-05 | Initial architecture |
