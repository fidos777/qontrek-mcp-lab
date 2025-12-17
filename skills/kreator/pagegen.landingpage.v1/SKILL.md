# SKILL: pagegen.landingpage.v1

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | `kreator.pagegen.landingpage.v1` |
| **Domain** | `kreator` |
| **Version** | `v1` |
| **Owner** | Qontrek Kreator Team |
| **Status** | `lab` |
| **Created** | 2024-12-07 |
| **Updated** | 2024-12-07 |

## Overview

Generates complete landing page structures with section-by-section content, layout specifications, conversion-optimized copy, and technical requirements. Designed for product launches, lead generation campaigns, event registrations, and app downloads.

**Purpose**: Automate landing page creation with conversion-focused copywriting, strategic section sequencing, and optimization recommendations.

**Use Cases**:
- SaaS product signup pages
- E-book and lead magnet download pages
- Event registration and ticket sales
- Mobile app download campaigns
- Webinar registration pages
- Product pre-launch waitlists

## Input Schema

### Required Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `page_title` | `string` | `minLength: 1, maxLength: 200` | Page title and H1 |
| `page_goal` | `string` | `enum: lead_generation, product_sale, signup, download, registration` | Primary conversion goal |
| `product_name` | `string` | `minLength: 1, maxLength: 100` | Product or offering name |
| `value_proposition` | `string` | `minLength: 1, maxLength: 300` | Core value proposition statement |
| `target_audience` | `string` | `minLength: 1, maxLength: 500` | Target audience description |
| `key_benefits` | `array<string>` | `minItems: 3, maxItems: 6` | Main benefits for the user |
| `cta_primary` | `string` | `minLength: 1, maxLength: 50` | Primary call-to-action text |
| `tone` | `string` | `enum: professional, friendly, urgent, inspirational` | Content tone |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `features` | `array<object>` | `[]` | Product features with name and description |
| `social_proof` | `object` | `{}` | Testimonials, stats, logos |
| `pricing` | `object` | `null` | Pricing information |
| `cta_secondary` | `string` | `null` | Secondary CTA text |
| `brand_identity.colors` | `array<string>` | `[]` | Brand colors (hex codes) |
| `brand_identity.style` | `string` | `"modern"` | Visual style |
| `include_faq` | `boolean` | `true` | Include FAQ section |
| `include_video` | `boolean` | `false` | Include video placeholder |

### Example Input

```json
{
  "page_title": "FlowMind - AI Productivity for Remote Teams",
  "page_goal": "signup",
  "product_name": "FlowMind",
  "value_proposition": "Reclaim 10+ hours every week with AI that automates your workflow",
  "target_audience": "Remote workers and distributed teams struggling with productivity",
  "key_benefits": [
    "Save 10+ hours per week on repetitive tasks",
    "Integrate with tools you already use",
    "AI that learns and adapts to your work style"
  ],
  "cta_primary": "Start Free Trial",
  "cta_secondary": "Watch Demo",
  "tone": "professional",
  "include_faq": true,
  "include_video": true
}
```

## Output Schema

### Success Response

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"success"` |
| `data` | `object` | Contains landing page structure |
| `errors` | `array` | Empty array |

### Data Object Structure

| Field | Type | Description |
|-------|------|-------------|
| `page_title` | `string` | Page title |
| `sections` | `array<object>` | Ordered array of page sections |
| `meta` | `object` | SEO metadata |
| `conversion_elements` | `object` | CTA count, form fields, trust signals |

### Section Object

| Field | Type | Description |
|-------|------|-------------|
| `section_id` | `string` | Unique section identifier |
| `section_type` | `string` | Type of section (hero, benefits, features, etc.) |
| `content` | `object` | Section content (headlines, body, CTAs) |

### Error Response

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"error"` |
| `data` | `null` | No data on error |
| `errors` | `array<string>` | Array of error messages |

### Example Output

```json
{
  "status": "success",
  "data": {
    "page_title": "FlowMind - AI Productivity for Remote Teams",
    "sections": [
      {
        "section_id": "hero",
        "section_type": "hero",
        "content": {
          "headline": "Reclaim 10+ Hours Every Week",
          "subheadline": "AI-powered automation that learns your workflow",
          "cta_primary": "Start Free Trial",
          "cta_secondary": "Watch Demo"
        }
      }
    ],
    "meta": {
      "description": "Reclaim 10+ hours every week with AI-powered workflow automation.",
      "keywords": ["AI productivity", "workflow automation", "remote work tools"]
    },
    "conversion_elements": {
      "primary_cta_count": 4,
      "form_fields": ["email", "full_name"],
      "trust_signals": ["14-day free trial", "No credit card required"]
    }
  },
  "errors": []
}
```

## Logic Breakdown

### Step 1: Input Validation
- Validate all required fields are present
- Check field types and constraints
- Validate page_goal and tone enum values
- Verify key_benefits count (3-6 items)
- Return structured errors if validation fails

### Step 2: Page Strategy & Structure
- Analyze page_goal to determine conversion funnel type
- Map user journey from arrival to conversion
- Identify key decision points and objections to address
- Define optimal section sequence based on goal
- Calculate recommended section count (6-10 sections)

### Step 3: Hero Section Design
- Craft compelling headline (5-10 words, benefit-focused)
- Write supporting subheadline (10-15 words)
- Design primary CTA (action-oriented, contrasting color)
- Add secondary CTA if provided
- Select hero visual recommendation (product shot, lifestyle, video)

### Step 4: Benefits Section
- Transform key_benefits into emotional outcomes
- Use "You get" or "You can" framing
- Add supporting icons or illustrations
- Maintain scannable format (3-column grid typical)
- Prioritize benefits by impact

### Step 5: Features Section (if provided)
- Present features with benefit-first framing
- Use alternating layout (image-text, text-image)
- Include visual demonstration recommendations
- Link features to user pain points
- Keep descriptions concise (2-3 sentences)

### Step 6: Social Proof Integration
- Position testimonials strategically (after benefits)
- Display trust metrics (users, ratings, awards)
- Show customer logos if B2B
- Add case study snippets if available
- Format for credibility and scannability

### Step 7: Pricing/Offer Section (if provided)
- Present pricing clearly and transparently
- Highlight value and savings
- Add guarantee or risk reversal
- Include secondary CTA
- Show comparison if multiple tiers

### Step 8: FAQ Section (if enabled)
- Address common objections
- Keep answers concise (2-3 sentences)
- Include 5-8 most critical questions
- End with CTA
- Use expandable format recommendation

### Step 9: Closing CTA Section
- Reinforce value proposition
- Create urgency (limited time, spots, etc.)
- Simplify action (one-click, no credit card)
- Add final trust signal
- Use contrasting design

### Step 10: Conversion Optimization
- Ensure CTA appears every 2-3 scrolls
- Minimize form fields (3-5 maximum)
- Add trust badges near forms
- Optimize for mobile-first experience
- Calculate CTA density and placement

### Step 11: SEO Metadata Generation
- Generate meta description (150-160 characters)
- Extract keywords from content
- Create Open Graph tags
- Ensure title optimization

### Step 12: Output Formatting
- Structure sections array in optimal order
- Add conversion elements summary
- Include technical requirements
- Return standardized response structure

## Handler Contract

```python
def run(params: dict) -> dict:
    """
    Execute the landing page generation logic.
    
    Args:
        params: Validated input parameters
        
    Returns:
        dict with status, data, errors
    """
    # Implementation follows steps 1-12 above
    pass
```

## Dependencies

### Python Standard Library
- `json` - JSON processing
- `datetime` - Timestamp generation
- `sys` - Standard I/O

### External Libraries
- None (uses standard library only)

### Domain Dependencies
- Copywriting templates library
- Layout pattern database
- Conversion optimization rules engine
- SEO metadata generator

## Performance Criteria

| Metric | Target | Notes |
|--------|--------|-------|
| **Execution Time** | < 8 seconds | For complete page with 8 sections |
| **Memory Usage** | < 100 MB | Peak usage during generation |
| **Success Rate** | > 99% | For valid inputs |
| **Copy Clarity Score** | > 8/10 | Readability and persuasiveness |
| **Conversion Optimization** | > 8/10 | CTA placement, form optimization |
| **Mobile Readiness** | > 9/10 | Mobile-first design compliance |

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `VALIDATION_ERROR` | Missing required field or invalid type | Check input against schema |
| `INVALID_PAGE_GOAL` | Page goal not in allowed enum | Use: lead_generation, product_sale, signup, download, registration |
| `INVALID_TONE` | Tone not in allowed enum | Use: professional, friendly, urgent, inspirational |
| `INVALID_BENEFITS_COUNT` | key_benefits must have 3-6 items | Provide 3-6 benefit statements |
| `PROCESSING_ERROR` | Core logic failed | Check logs for details |

## Testing Strategy

### Unit Tests
- Test input validation with missing fields
- Test section generation for each page_goal
- Test hero headline generation
- Test benefits transformation logic
- Test FAQ generation
- Test SEO metadata generation
- Test error handling

### Property-Based Tests
- Generate random valid inputs
- Verify output structure matches schema
- Check section count is within optimal range (6-10)
- Verify CTA appears multiple times
- Check headline length constraints

### Integration Tests
- Test via MCP protocol (tools/call)
- Verify schema compliance
- Test all page_goal variations
- Test all tone variations
- Test with/without optional fields
- Test edge cases (max benefits, no social proof)

## Sample Test Cases

### Test Case 1: SaaS Signup Page
```json
{
  "input": {
    "page_title": "FlowMind - AI Productivity",
    "page_goal": "signup",
    "product_name": "FlowMind",
    "value_proposition": "Reclaim 10+ hours every week",
    "target_audience": "Remote workers",
    "key_benefits": ["Save time", "Integrate easily", "AI learning"],
    "cta_primary": "Start Free Trial",
    "tone": "professional"
  },
  "expected_output": {
    "status": "success",
    "data": {
      "sections": [
        {"section_type": "hero"},
        {"section_type": "benefits_grid"},
        {"section_type": "call_to_action"}
      ],
      "conversion_elements": {
        "primary_cta_count": 3
      }
    }
  }
}
```

### Test Case 2: Missing Required Field
```json
{
  "input": {
    "page_title": "Test Page",
    "product_name": "TestProduct"
  },
  "expected_output": {
    "status": "error",
    "errors": [
      "Missing required field: page_goal",
      "Missing required field: value_proposition",
      "Missing required field: target_audience",
      "Missing required field: key_benefits",
      "Missing required field: cta_primary",
      "Missing required field: tone"
    ]
  }
}
```

## Implementation Checklist

- [ ] Create `schema.json` with JSON Schema Draft 2020-12
- [ ] Create `handler.py` with `run(params)` method
- [ ] Implement input validation
- [ ] Implement page strategy and structure logic
- [ ] Implement hero section generation
- [ ] Implement benefits section generation
- [ ] Implement features section generation
- [ ] Implement social proof section generation
- [ ] Implement FAQ generation
- [ ] Implement closing CTA generation
- [ ] Implement conversion optimization logic
- [ ] Implement SEO metadata generation
- [ ] Add error handling
- [x] Create `sample_inputs.json`
- [x] Create `sample_outputs.json`
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Update domain manifest

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1 | 2024-12-07 | Initial lab implementation | Qontrek Team |

## Notes

**Current Limitations**:
- No actual HTML/CSS generation (structure only)
- No A/B testing recommendations
- Limited to 4 tone variations
- No actual conversion rate predictions
- No integration with page builders

**Future Improvements**:
- Generate actual HTML/CSS/JS code
- Integrate with page builders (Webflow, Unbounce, Framer)
- Add A/B testing recommendations with predicted lift
- Implement conversion rate prediction models
- Support multi-step forms and progressive disclosure
- Add heatmap and scroll depth predictions
- Generate mobile and desktop mockups
- Integrate with analytics for performance tracking
