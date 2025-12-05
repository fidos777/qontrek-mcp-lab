# Solar MCP Toolpack Architecture Overview

## Introduction

The Solar MCP Toolpack is a collection of Model Context Protocol (MCP) tools designed to streamline solar installation sales and operations workflows. This document provides a comprehensive overview of the architecture, design decisions, and implementation guidelines.

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AI AGENT LAYER                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    LLM (Claude, GPT, etc.)                          │    │
│  │                                                                      │    │
│  │   • Natural language understanding                                   │    │
│  │   • Tool selection and orchestration                                │    │
│  │   • Context management                                              │    │
│  └──────────────────────────────┬──────────────────────────────────────┘    │
│                                 │                                            │
│                                 │ MCP Protocol                               │
│                                 ▼                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                         MCP TOOLPACK LAYER                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                    Solar MCP Server                                  │    │
│  │                                                                      │    │
│  │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │    │
│  │   │ lead_intake │  │    site_    │  │    roi_     │  │ quotation │  │    │
│  │   │             │  │ inspection  │  │ calculator  │  │  builder  │  │    │
│  │   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘  │    │
│  │          │                │                │                │        │    │
│  │          └────────────────┴────────────────┴────────────────┘        │    │
│  │                                 │                                    │    │
│  └─────────────────────────────────┼────────────────────────────────────┘    │
│                                    │                                         │
├────────────────────────────────────┼────────────────────────────────────────┤
│                         DATA & SERVICES LAYER                                │
│                                    │                                         │
│    ┌───────────────────────────────┼───────────────────────────────────┐    │
│    │                               ▼                                    │    │
│    │  ┌─────────────┐  ┌─────────────────┐  ┌─────────────────────┐   │    │
│    │  │  Supabase   │  │    Qontrek      │  │     FireCrawl       │   │    │
│    │  │             │  │  Document       │  │     (Optional)      │   │    │
│    │  │ • Database  │  │    Factory      │  │                     │   │    │
│    │  │ • Auth      │  │                 │  │ • Web scraping      │   │    │
│    │  │ • Storage   │  │ • PDF/DOCX      │  │ • Lead enrichment   │   │    │
│    │  │ • Edge Fn   │  │ • Templates     │  │                     │   │    │
│    │  └─────────────┘  └─────────────────┘  └─────────────────────┘   │    │
│    │                                                                    │    │
│    └────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility |
|-----------|----------------|
| **AI Agent** | Interprets user intent, selects appropriate tools, orchestrates multi-tool workflows |
| **MCP Server** | Exposes tools via MCP protocol, handles request routing, validates inputs/outputs |
| **Tools** | Execute specific business logic (lead capture, inspection, ROI, quotes) |
| **Supabase** | Data persistence, authentication, file storage, edge functions |
| **Document Factory** | Professional document generation (PDF, DOCX, PPTX) |
| **FireCrawl** | Optional web scraping for lead enrichment |

## Design Principles

### 1. Stateless Tool Execution

Each tool invocation is stateless and self-contained:

```
┌──────────────────────────────────────────────────────────────┐
│                    TOOL INVOCATION                           │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   INPUT ────────▶ VALIDATION ────────▶ EXECUTION ────────▶  │
│                                              │               │
│                                              ▼               │
│                                        ┌──────────┐         │
│                                        │ Supabase │         │
│                                        │  (State) │         │
│                                        └──────────┘         │
│                                              │               │
│   OUTPUT ◀────────────────────────────────────               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

**Benefits:**
- Horizontal scalability (run on any serverless platform)
- Fault isolation (one tool failure doesn't affect others)
- Easy testing and debugging
- Compatible with edge functions

### 2. Schema-First Design

All tools follow a schema-first approach:

```
schemas/              # JSON Schema definitions
  ├── site_inspection.schema.json
  ├── roi_calculator.schema.json
  ├── lead_intake.schema.json
  └── quotation_builder.schema.json

tools/                # Tool implementations reference schemas
  ├── site_inspection.json
  └── ...
```

**Benefits:**
- Type safety at API boundaries
- Automatic validation
- Self-documenting APIs
- Client code generation support

### 3. Tool Chaining via References

Tools are connected through UUID references, not direct coupling:

```json
{
  "lead_id": "550e8400-e29b-41d4-a716-446655440000",
  "site_inspection_id": "660e8400-e29b-41d4-a716-446655440001",
  "roi_calculation_id": "770e8400-e29b-41d4-a716-446655440002"
}
```

**Benefits:**
- Loose coupling between tools
- Supports partial workflows
- Enables data lineage tracking
- Allows manual data entry at any stage

### 4. Edge-Function Compatibility

All tools are designed to run within serverless constraints:

| Constraint | Limit | Design Accommodation |
|------------|-------|---------------------|
| Cold start | < 500ms | Minimal dependencies, lazy loading |
| Execution time | < 10s | Async processing for heavy operations |
| Memory | < 128MB | Streaming for large files |
| Bundle size | < 50KB | Tree-shaking, no heavy libraries |

## Security Architecture

### Authentication Flow

```
┌──────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────┐
│  Client  │────▶│  API Gateway │────▶│  MCP Server   │────▶│ Supabase │
└──────────┘     └──────────────┘     └───────────────┘     └──────────┘
                        │                     │
                        │ Bearer Token        │ Service Key
                        │ Validation          │ (RLS Bypass)
                        ▼                     ▼
                 ┌──────────────┐     ┌───────────────┐
                 │   Supabase   │     │    Row-Level  │
                 │     Auth     │     │    Security   │
                 └──────────────┘     └───────────────┘
```

### Authorization Model

```sql
-- Role-Based Access Control (RBAC)
CREATE TYPE user_role AS ENUM ('admin', 'manager', 'agent', 'viewer');

-- Row Level Security Policies
CREATE POLICY "Agents see own leads"
  ON leads FOR SELECT
  USING (
    auth.uid() = assigned_agent_id
    OR EXISTS (
      SELECT 1 FROM users
      WHERE users.id = auth.uid()
      AND users.role IN ('admin', 'manager')
    )
  );
```

### Data Protection

| Data Type | Protection Measure |
|-----------|-------------------|
| Customer PII | Encrypted at rest, masked in logs |
| API Keys | Environment variables, never in code |
| Documents | Signed URLs with expiration |
| Webhooks | HMAC-SHA256 signature verification |

## Deployment Architecture

### Recommended Stack

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PRODUCTION DEPLOYMENT                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                     Cloudflare (CDN/WAF)                         │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │              Supabase Edge Functions (MCP Server)                │   │
│   │                                                                  │   │
│   │   Region: Singapore (ap-southeast-1)                            │   │
│   │   Replicas: Auto-scaling                                        │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│          ┌─────────────────────────┼─────────────────────────┐          │
│          ▼                         ▼                         ▼          │
│   ┌─────────────┐          ┌─────────────┐          ┌─────────────┐    │
│   │  Supabase   │          │  Supabase   │          │   Qontrek   │    │
│   │  Postgres   │          │   Storage   │          │   Doc Fac   │    │
│   │             │          │             │          │             │    │
│   │ • leads     │          │ • images    │          │ • templates │    │
│   │ • quotes    │          │ • documents │          │ • rendering │    │
│   └─────────────┘          └─────────────┘          └─────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Environment Configuration

```bash
# Required Environment Variables
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_KEY=eyJ...
QONTREK_API_KEY=qk_...

# Optional
FIRECRAWL_API_KEY=fc_...
WEBHOOK_SECRET=whsec_...
LOG_LEVEL=info
```

## Performance Considerations

### Caching Strategy

| Data | Cache Location | TTL | Invalidation |
|------|---------------|-----|--------------|
| Tariff rates | Edge | 24h | Manual |
| Equipment catalog | Edge | 1h | On update |
| ROI calculations | Database | 1h | On input change |
| Generated documents | Storage | Permanent | Never (versioned) |

### Optimization Techniques

1. **Connection Pooling**: Supabase handles connection pooling via PgBouncer
2. **Lazy Loading**: Heavy dependencies loaded only when needed
3. **Batch Operations**: Multiple database writes combined where possible
4. **Async Document Generation**: Quote PDFs generated asynchronously

## Monitoring and Observability

### Metrics

| Metric | Type | Alert Threshold |
|--------|------|-----------------|
| Tool invocation count | Counter | N/A |
| Tool latency (p99) | Histogram | > 5s |
| Error rate | Gauge | > 5% |
| Active leads | Gauge | N/A |
| Quote conversion rate | Gauge | < 10% (warning) |

### Logging

```json
{
  "timestamp": "2025-12-05T10:30:00Z",
  "level": "info",
  "tool": "site_inspection",
  "action": "execute",
  "lead_id": "550e8400-e29b-41d4-a716-446655440000",
  "duration_ms": 1234,
  "status": "success"
}
```

## Extension Points

### Adding New Tools

1. Create schema in `schemas/new_tool.schema.json`
2. Create tool definition in `tools/new_tool.json`
3. Implement handler in MCP server
4. Update manifest in `manifests/solar_mcp_manifest.json`
5. Add to relevant tool chains

### Custom Templates

Document templates can be added to Qontrek Document Factory:

```
templates/
  ├── standard/
  │   ├── quote.pptx
  │   └── quote.docx
  ├── premium/
  │   └── quote.pptx
  └── commercial/
      └── quote.pptx
```

### Webhook Integration

External systems can subscribe to events:

```javascript
// Webhook handler example
app.post('/webhooks/solar', (req, res) => {
  const signature = req.headers['x-qontrek-signature'];
  if (!verifySignature(req.body, signature)) {
    return res.status(401).send('Invalid signature');
  }

  const { event, data } = req.body;

  switch (event) {
    case 'quote.accepted':
      // Trigger downstream process
      break;
  }

  res.status(200).send('OK');
});
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial architecture |
