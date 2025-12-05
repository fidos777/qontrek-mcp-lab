# Solar MCP Toolpack Tool Dependencies

## Overview

This document details the dependencies between tools in the Solar MCP Toolpack, including upstream/downstream relationships, optional vs required dependencies, and integration points with external services.

## Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TOOL DEPENDENCY GRAPH                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│                          ┌─────────────────┐                                 │
│                          │                 │                                 │
│                          │   lead_intake   │                                 │
│                          │                 │                                 │
│                          │  Upstream: None │                                 │
│                          │                 │                                 │
│                          └────────┬────────┘                                 │
│                                   │                                          │
│                                   │ Optional                                 │
│                                   │ (can start here)                         │
│                                   ▼                                          │
│                          ┌─────────────────┐                                 │
│                          │                 │                                 │
│                          │ site_inspection │                                 │
│                          │                 │                                 │
│                          │ Upstream:       │                                 │
│                          │  • lead_intake  │                                 │
│                          │    (optional)   │                                 │
│                          │                 │                                 │
│                          └────────┬────────┘                                 │
│                                   │                                          │
│                                   │ Optional                                 │
│                                   │ (can use manual input)                   │
│                                   ▼                                          │
│                          ┌─────────────────┐                                 │
│                          │                 │                                 │
│                          │  roi_calculator │                                 │
│                          │                 │                                 │
│                          │ Upstream:       │                                 │
│                          │  • site_inspect │                                 │
│                          │    (optional)   │                                 │
│                          │  • lead_intake  │                                 │
│                          │    (optional)   │                                 │
│                          │                 │                                 │
│                          └────────┬────────┘                                 │
│                                   │                                          │
│                                   │ Required                                 │
│                                   │ (must have ROI)                          │
│                                   ▼                                          │
│                          ┌─────────────────┐                                 │
│                          │                 │                                 │
│                          │quotation_builder│                                 │
│                          │                 │                                 │
│                          │ Upstream:       │                                 │
│                          │  • roi_calc     │                                 │
│                          │    (REQUIRED)   │                                 │
│                          │                 │                                 │
│                          │ External:       │                                 │
│                          │  • Qontrek Doc  │                                 │
│                          │    Factory      │                                 │
│                          │                 │                                 │
│                          └─────────────────┘                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Dependency Matrix

### Tool-to-Tool Dependencies

| Tool | lead_intake | site_inspection | roi_calculator | quotation_builder |
|------|-------------|-----------------|----------------|-------------------|
| **lead_intake** | - | Downstream (opt) | Downstream (opt) | Downstream (opt) |
| **site_inspection** | Upstream (opt) | - | Downstream (opt) | Downstream (opt) |
| **roi_calculator** | Upstream (opt) | Upstream (opt) | - | Downstream (req) |
| **quotation_builder** | Upstream (opt) | Upstream (opt) | Upstream (req) | - |

**Legend:**
- `Upstream (opt)`: Can receive data from this tool, but not required
- `Upstream (req)`: Must receive data from this tool
- `Downstream (opt)`: Can send data to this tool
- `Downstream (req)`: Always sends data to this tool

### External Service Dependencies

| Tool | Supabase DB | Supabase Storage | Qontrek Doc Factory | FireCrawl |
|------|-------------|------------------|---------------------|-----------|
| **lead_intake** | Required | Optional | - | Optional |
| **site_inspection** | Required | Required | - | - |
| **roi_calculator** | Required | - | - | - |
| **quotation_builder** | Required | Required | Required | - |

## Detailed Tool Dependencies

### 1. lead_intake

```yaml
tool: lead_intake
version: 1.0.0

dependencies:
  upstream:
    tools: []  # No tool dependencies - entry point

  downstream:
    tools:
      - name: site_inspection
        relationship: optional
        data_passed:
          - lead_id
          - address (for location reference)
          - estimated_system_size_kwp (guidance)

  external:
    required:
      - service: supabase_database
        purpose: Store lead records
        tables: [leads]

    optional:
      - service: supabase_storage
        purpose: Store attached documents (electricity bills)
        bucket: lead-attachments

      - service: firecrawl
        purpose: Enrich lead with company website data
        use_case: B2B leads only

  internal:
    - component: lead_scoring_engine
      purpose: Calculate lead score from inputs

    - component: agent_assignment
      purpose: Auto-assign lead to sales agent
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
          - lead_id (reference)
          - address (for GPS verification)
        fallback: Manual lead_id input or create ad-hoc inspection

  downstream:
    tools:
      - name: roi_calculator
        relationship: optional
        data_passed:
          - inspection_id
          - usable_roof_area_sqm
          - recommended_system_size_kwp
          - efficiency_factors
          - shading_factor
        auto_trigger: false (agent confirmation required)

  external:
    required:
      - service: supabase_database
        purpose: Store inspection records
        tables: [site_inspections]

      - service: supabase_storage
        purpose: Store inspection photos
        bucket: inspection-images
        max_file_size: 10MB
        allowed_types: [image/jpeg, image/png, image/webp]

  internal:
    - component: panel_layout_calculator
      purpose: Generate optimal panel arrangement
      inputs: [roof_area, orientation, shading]

    - component: system_sizing_engine
      purpose: Recommend system size based on roof
      inputs: [usable_area, panel_wattage]
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
          - site_inspection_id (reference)
          - system_size_kwp
          - shading_factor
          - orientation_factor
          - tilt_factor
        fallback: Manual system_size_kwp input with default factors

      - name: lead_intake
        relationship: optional
        data_received:
          - monthly_electricity_bill_myr
          - property_type (for tariff lookup)
        fallback: Manual tariff input or use defaults

  downstream:
    tools:
      - name: quotation_builder
        relationship: optional
        data_passed:
          - roi_id
          - financial_summary (all fields)
          - system_specifications
          - year_by_year_projection
          - sensitivity_analysis
        auto_trigger: false

  external:
    required:
      - service: supabase_database
        purpose: Store ROI calculations
        tables: [roi_calculations]

  internal:
    - component: generation_estimator
      purpose: Calculate annual kWh generation
      inputs: [system_size, irradiance, performance_ratio, efficiency_factors]

    - component: financial_calculator
      purpose: Compute payback, NPV, IRR
      inputs: [costs, savings, discount_rate, projection_years]

    - component: sensitivity_analyzer
      purpose: Generate conservative/base/optimistic scenarios
      inputs: [base_calculation, variance_factors]

  reference_data:
    - name: tariff_rates
      source: supabase (solar://tariffs resource)
      cache_ttl: 24h

    - name: irradiance_data
      source: static (built-in)
      coverage: Malaysia regions
```

### 4. quotation_builder

```yaml
tool: quotation_builder
version: 1.0.0

dependencies:
  upstream:
    tools:
      - name: roi_calculator
        relationship: required
        data_received:
          - roi_calculation_id (reference)
          - financial_summary.*
          - system_specifications.*
        validation: roi_id must exist and have complete financial_summary

  downstream:
    tools: []  # Terminal node in the chain

  external:
    required:
      - service: supabase_database
        purpose: Store quotation records
        tables: [quotations]

      - service: supabase_storage
        purpose: Store generated documents
        bucket: quotation-documents

      - service: qontrek_document_factory
        purpose: Generate PDF/DOCX/PPTX documents
        api_endpoint: https://api.qontrek.com/v1/documents
        timeout: 30s
        retry_policy:
          max_retries: 3
          backoff: exponential

  internal:
    - component: quote_number_generator
      purpose: Generate unique quote reference
      format: QT-YYYY-NNNNN

    - component: pricing_calculator
      purpose: Apply discounts and compute totals
      inputs: [base_price, discount, tax_rules]

    - component: template_selector
      purpose: Choose appropriate document template
      inputs: [template_id, customer_type, language]

  reference_data:
    - name: document_templates
      source: supabase (solar://templates resource)
      cache_ttl: 1h

    - name: equipment_catalog
      source: supabase (solar://equipment resource)
      cache_ttl: 1h
```

## Dependency Resolution

### Chain Initialization

When starting a tool chain, the system resolves dependencies:

```javascript
// Example: Starting from ROI Calculator
async function resolveChain(toolName, inputData) {
  const tool = getToolDefinition(toolName);

  // Check required upstream dependencies
  for (const dep of tool.dependencies.upstream) {
    if (dep.relationship === 'required') {
      const refField = `${dep.name.replace('_', '_')}_id`;
      if (!inputData[refField]) {
        throw new ValidationError(
          `${toolName} requires ${dep.name}. ` +
          `Please provide ${refField} or run ${dep.name} first.`
        );
      }

      // Verify referenced record exists
      const record = await fetchRecord(dep.name, inputData[refField]);
      if (!record) {
        throw new NotFoundError(
          `Referenced ${dep.name} record not found: ${inputData[refField]}`
        );
      }
    }
  }

  // Merge data from upstream records
  const enrichedInput = await mergeUpstreamData(tool, inputData);

  return enrichedInput;
}
```

### Automatic Data Propagation

```javascript
// When site_inspection completes, prepare roi_calculator input
function prepareDownstreamInput(sourceOutput, targetTool) {
  const mapping = {
    'site_inspection -> roi_calculator': {
      'inspection_id': 'site_inspection_id',
      'recommended_system_size_kwp': 'system_size_kwp',
      'efficiency_factors.shading_factor': 'shading_factor',
      'efficiency_factors.orientation_factor': 'orientation_factor'
    },
    'roi_calculator -> quotation_builder': {
      'roi_id': 'roi_calculation_id'
    }
  };

  const key = `${sourceOutput._tool} -> ${targetTool}`;
  const fieldMap = mapping[key];

  const preparedInput = {};
  for (const [source, target] of Object.entries(fieldMap)) {
    preparedInput[target] = getNestedValue(sourceOutput, source);
  }

  return preparedInput;
}
```

## Failure Handling

### Dependency Failure Scenarios

| Scenario | Impact | Recovery Strategy |
|----------|--------|-------------------|
| Lead not found | site_inspection fails | Create lead first or provide manual data |
| Inspection data incomplete | ROI uses defaults | Warn user, proceed with conservative estimates |
| ROI calculation missing | Quotation blocked | Must complete ROI first |
| Document Factory unavailable | Quote generation fails | Retry with backoff, queue for later |
| Supabase down | All tools fail | Circuit breaker, return error |

### Circuit Breaker Configuration

```javascript
const circuitBreakers = {
  supabase: {
    failureThreshold: 5,
    resetTimeout: 30000,  // 30 seconds
    fallback: () => ({ error: 'Database temporarily unavailable' })
  },
  qontrek_document_factory: {
    failureThreshold: 3,
    resetTimeout: 60000,  // 1 minute
    fallback: async (input) => {
      // Queue for retry
      await queueDocumentGeneration(input);
      return {
        status: 'queued',
        message: 'Document generation queued, will be available shortly'
      };
    }
  }
};
```

## Version Compatibility

### Schema Versioning

```yaml
compatibility_matrix:
  lead_intake:
    v1.0.0:
      compatible_with:
        site_inspection: ["1.0.x"]
        roi_calculator: ["1.0.x"]

  site_inspection:
    v1.0.0:
      compatible_with:
        lead_intake: ["1.0.x"]
        roi_calculator: ["1.0.x"]

  roi_calculator:
    v1.0.0:
      compatible_with:
        site_inspection: ["1.0.x"]
        quotation_builder: ["1.0.x"]

  quotation_builder:
    v1.0.0:
      compatible_with:
        roi_calculator: ["1.0.x"]
```

### Migration Strategy

When upgrading tools:

1. **Backward Compatible Changes**: Add new optional fields
2. **Breaking Changes**: Bump major version, maintain v1 endpoint
3. **Deprecation Period**: 6 months before removing old versions

## Testing Dependencies

### Mock Services

```javascript
// Test configuration for isolated tool testing
const testConfig = {
  supabase: {
    mock: true,
    fixtures: './test/fixtures/supabase'
  },
  qontrek_document_factory: {
    mock: true,
    response: {
      document_urls: {
        pdf: 'https://mock.storage/test.pdf'
      }
    }
  },
  firecrawl: {
    mock: true,
    response: null  // Disabled in tests
  }
};
```

### Integration Test Chains

```javascript
describe('Full Chain Integration', () => {
  it('should complete lead-to-quote flow', async () => {
    // 1. Create lead
    const lead = await invokeTool('lead_intake', leadFixture);
    expect(lead.lead_id).toBeDefined();

    // 2. Create inspection
    const inspection = await invokeTool('site_inspection', {
      lead_id: lead.lead_id,
      ...inspectionFixture
    });
    expect(inspection.inspection_id).toBeDefined();

    // 3. Calculate ROI
    const roi = await invokeTool('roi_calculator', {
      site_inspection_id: inspection.inspection_id
    });
    expect(roi.roi_id).toBeDefined();
    expect(roi.financial_summary.payback_period_years).toBeLessThan(10);

    // 4. Generate quote
    const quote = await invokeTool('quotation_builder', {
      roi_calculation_id: roi.roi_id
    });
    expect(quote.document_urls.pdf).toBeDefined();
  });
});
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial tool dependencies documentation |
