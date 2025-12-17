# SKILL: slidegen.pitchdeck.v1

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | `kreator.slidegen.pitchdeck.v1` |
| **Domain** | `kreator` |
| **Version** | `v1` |
| **Owner** | Qontrek Kreator Team |
| **Status** | `lab` |
| **Created** | 2024-12-07 |
| **Updated** | 2024-12-07 |

## Overview

Generates complete pitch deck structures with slide-by-slide content, layout recommendations, visual guidance, and speaker notes. Optimized for startup fundraising (seed, Series A/B), corporate presentations, and product launches.

**Purpose**: Automate pitch deck creation with investor-focused storytelling, data visualization recommendations, and presentation timing guidance.

**Use Cases**:
- Seed and Series A/B fundraising decks
- Corporate business proposals
- Product launch presentations
- Partnership pitch decks
- Board meeting presentations
- Demo day pitches

## Input Schema

### Required Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `company_name` | `string` | `minLength: 1, maxLength: 100` | Company or product name |
| `pitch_type` | `string` | `enum: seed, series_a, series_b, corporate, product` | Type of pitch |
| `industry` | `string` | `minLength: 1, maxLength: 100` | Industry or sector |
| `problem_statement` | `string` | `minLength: 1, maxLength: 500` | Problem being solved |
| `solution_description` | `string` | `minLength: 1, maxLength: 500` | Solution overview |
| `target_market` | `string` | `minLength: 1, maxLength: 300` | Target market description |
| `business_model` | `string` | `minLength: 1, maxLength: 300` | Revenue model |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `traction` | `object` | `{}` | Users, revenue, growth metrics |
| `team` | `array<object>` | `[]` | Team members with roles and backgrounds |
| `financials` | `object` | `{}` | Runway, burn rate, unit economics |
| `ask_amount` | `string` | `null` | Funding amount requested |
| `slide_count` | `integer` | `12` | Number of slides (min: 8, max: 20) |
| `style` | `string` | `"modern"` | Visual style (modern, corporate, minimal, bold) |

### Example Input

```json
{
  "company_name": "DataFlow AI",
  "pitch_type": "seed",
  "industry": "Enterprise SaaS / AI",
  "problem_statement": "Data teams spend 60% of their time on manual pipeline maintenance",
  "solution_description": "AI-powered data pipeline automation that self-heals and scales",
  "target_market": "Mid-market to enterprise companies with data teams of 5+ engineers",
  "business_model": "SaaS subscription: $500/month per data source",
  "traction": {
    "users": "15 beta customers",
    "revenue": "$45K ARR",
    "growth": "30% MoM"
  },
  "ask_amount": "$2M seed round",
  "slide_count": 12,
  "style": "modern"
}
```

## Output Schema

### Success Response

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"success"` |
| `output` | `object` | Contains deck structure and design system |
| `errors` | `array` | Empty array |

### Output Object Structure

| Field | Type | Description |
|-------|------|-------------|
| `deck` | `object` | Complete deck with slides array |
| `design_system` | `object` | Colors, typography, visual style |
| `metadata` | `object` | Generation timestamp and version |

### Deck Object

| Field | Type | Description |
|-------|------|-------------|
| `title` | `string` | Deck title |
| `total_slides` | `integer` | Number of slides |
| `estimated_duration` | `string` | Presentation time estimate |
| `slides` | `array<object>` | Array of slide specifications |

### Slide Object

| Field | Type | Description |
|-------|------|-------------|
| `slide_number` | `integer` | Slide position |
| `title` | `string` | Slide title |
| `type` | `string` | Slide type (cover, problem, solution, etc.) |
| `content` | `object` | Headline, body, data points |
| `layout` | `object` | Template, visual elements, color scheme |
| `speaker_notes` | `string` | Presentation guidance |
| `estimated_time` | `string` | Time to spend on this slide |

### Error Response

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"error"` |
| `output` | `null` | No data on error |
| `errors` | `array<string>` | Array of error messages |

### Example Output

```json
{
  "status": "success",
  "output": {
    "deck": {
      "title": "DataFlow AI - Seed Round Pitch",
      "total_slides": 12,
      "estimated_duration": "12 minutes",
      "slides": [
        {
          "slide_number": 1,
          "title": "DataFlow AI",
          "type": "cover",
          "content": {
            "headline": "AI-Powered Data Pipeline Automation",
            "body": ["Seed Round Pitch", "December 2025"]
          },
          "layout": {
            "template": "centered_hero",
            "visual_elements": ["company_logo", "gradient_background"],
            "color_scheme": "primary"
          },
          "speaker_notes": "Strong opening. State company name clearly.",
          "estimated_time": "30 seconds"
        }
      ]
    },
    "design_system": {
      "primary_colors": ["#0066FF", "#00C9FF", "#1A1A1A"],
      "typography": {
        "headline": "Inter Bold, 48px",
        "body": "Inter Regular, 24px"
      },
      "visual_style": "Modern tech with gradient accents"
    },
    "metadata": {
      "generated_at": "2025-12-07T10:35:00Z",
      "version": "1.0.0"
    }
  },
  "errors": []
}
```

## Logic Breakdown

### Step 1: Input Validation
- Validate all required fields are present
- Check pitch_type and style enum values
- Verify slide_count within range (8-20)
- Validate optional objects (traction, team, financials)
- Return structured errors if validation fails

### Step 2: Pitch Analysis & Structure
- Determine pitch stage and audience expectations
- Identify key narrative arc based on pitch_type
- Map required slides (problem → solution → market → traction → team → ask)
- Calculate optimal slide allocation
- Ensure logical flow and storytelling

### Step 3: Slide Sequence Planning
- Define slide order based on pitch_type
- Allocate content weight per slide
- Identify critical slides (problem, solution, traction, ask)
- Plan transition points and narrative beats
- Adjust sequence for slide_count constraint

### Step 4: Content Generation Per Slide
- Create compelling headlines (6-8 words max)
- Generate bullet points (3-5 per slide, max 15 words each)
- Craft data visualization recommendations
- Write speaker notes with presentation guidance
- Estimate time per slide (30 seconds to 2 minutes)

### Step 5: Layout Assignment
- Match content to optimal layout templates
- Suggest visual elements (charts, icons, images, diagrams)
- Define hierarchy and white space
- Apply color scheme per slide type
- Ensure visual consistency

### Step 6: Design System Creation
- Generate color palette based on industry and style
- Define typography hierarchy (headline, body, accent)
- Establish visual style guidelines
- Ensure brand consistency across slides
- Provide design recommendations

### Step 7: Timing & Flow Optimization
- Estimate total presentation duration
- Assign time per slide based on content density
- Identify pacing adjustments
- Mark transition points
- Ensure 10-20 minute total duration

### Step 8: Output Formatting
- Structure slides array in presentation order
- Include design system specifications
- Add metadata with timestamp
- Return standardized response structure

## Handler Contract

```python
def run(params: dict) -> dict:
    """
    Execute the pitch deck generation logic.
    
    Args:
        params: Validated input parameters
        
    Returns:
        dict with status, output, errors
    """
    # Implementation follows steps 1-8 above
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
- Business model templates library
- Market sizing frameworks
- Slide layout templates
- Design system generator
- Financial projection formatter

## Performance Criteria

| Metric | Target | Notes |
|--------|--------|-------|
| **Execution Time** | < 5 seconds | For 12-slide deck |
| **Memory Usage** | < 80 MB | Peak usage during generation |
| **Success Rate** | > 99% | For valid inputs |
| **Content Clarity** | > 8/10 | Headline and bullet clarity |
| **Narrative Flow** | > 8/10 | Story progression score |
| **Investor Readiness** | > 7/10 | Completeness for fundraising |

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `VALIDATION_ERROR` | Missing required field or invalid type | Check input against schema |
| `INVALID_PITCH_TYPE` | Pitch type not in allowed enum | Use: seed, series_a, series_b, corporate, product |
| `INVALID_STYLE` | Style not in allowed enum | Use: modern, corporate, minimal, bold |
| `INVALID_SLIDE_COUNT` | Slide count outside range 8-20 | Provide slide_count between 8 and 20 |
| `PROCESSING_ERROR` | Core logic failed | Check logs for details |

## Testing Strategy

### Unit Tests
- Test input validation with missing fields
- Test slide sequence generation for each pitch_type
- Test content generation (headlines, bullets)
- Test layout assignment logic
- Test design system generation
- Test timing calculation
- Test error handling

### Property-Based Tests
- Generate random valid inputs
- Verify output structure matches schema
- Check slide count matches input
- Verify total duration is 10-20 minutes
- Check all slides have required fields

### Integration Tests
- Test via MCP protocol (tools/call)
- Verify schema compliance
- Test all pitch_type variations
- Test all style variations
- Test with/without optional fields (traction, team, financials)
- Test edge cases (min/max slide counts)

## Sample Test Cases

### Test Case 1: Seed Stage Pitch
```json
{
  "input": {
    "company_name": "DataFlow AI",
    "pitch_type": "seed",
    "industry": "Enterprise SaaS",
    "problem_statement": "Data teams waste 60% of time on maintenance",
    "solution_description": "AI-powered automation",
    "target_market": "Enterprise data teams",
    "business_model": "SaaS subscription",
    "slide_count": 12
  },
  "expected_output": {
    "status": "success",
    "output": {
      "deck": {
        "total_slides": 12,
        "slides": [
          {"type": "cover"},
          {"type": "problem"},
          {"type": "solution"}
        ]
      }
    }
  }
}
```

### Test Case 2: Missing Required Field
```json
{
  "input": {
    "company_name": "TestCo",
    "pitch_type": "seed"
  },
  "expected_output": {
    "status": "error",
    "errors": [
      "Missing required field: industry",
      "Missing required field: problem_statement",
      "Missing required field: solution_description",
      "Missing required field: target_market",
      "Missing required field: business_model"
    ]
  }
}
```

## Implementation Checklist

- [ ] Create `schema.json` with JSON Schema Draft 2020-12
- [ ] Create `handler.py` with `run(params)` method
- [ ] Implement input validation
- [ ] Implement pitch analysis and structure logic
- [ ] Implement slide sequence planning
- [ ] Implement content generation per slide
- [ ] Implement layout assignment
- [ ] Implement design system creation
- [ ] Implement timing and flow optimization
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
- No actual slide rendering (structure only)
- No data visualization generation
- Limited to 4 style variations
- No actual financial modeling
- No integration with presentation tools

**Future Improvements**:
- Generate actual PowerPoint/Keynote/Google Slides files
- Integrate with design tools (Pitch, Beautiful.ai, Canva)
- Add data visualization generation (charts, graphs)
- Implement financial modeling and projections
- Add competitive analysis slide generation
- Support video and animation recommendations
- Generate presenter view notes
- Add audience engagement recommendations
- Integrate with CRM for investor tracking
