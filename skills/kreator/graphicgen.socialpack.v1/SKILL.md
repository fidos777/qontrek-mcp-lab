# SKILL: graphicgen.socialpack.v1

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | `kreator.graphicgen.socialpack.v1` |
| **Domain** | `kreator` |
| **Version** | `v1` |
| **Owner** | Qontrek Kreator Team |
| **Status** | `lab` |
| **Created** | 2024-12-07 |
| **Updated** | 2024-12-07 |

## Overview

Generates comprehensive social media graphic packages with platform-specific dimensions, content variations, and design specifications. Creates cohesive visual campaigns across multiple social platforms with optimized layouts, copy, and accessibility features.

**Purpose**: Automate social media graphic creation for marketing campaigns, ensuring platform compliance, brand consistency, and engagement optimization.

**Use Cases**:
- Product launch announcements across multiple platforms
- Social media campaign content generation
- Brand awareness and engagement campaigns
- Event promotion graphics
- Educational content series
- Quote graphics and motivational content

## Input Schema

### Required Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `campaign_name` | `string` | `minLength: 1, maxLength: 100` | Name of the campaign |
| `campaign_goal` | `string` | `enum: awareness, engagement, conversion, announcement` | Primary campaign objective |
| `message` | `string` | `minLength: 1, maxLength: 500` | Core message to communicate |
| `brand_identity.colors` | `array<string>` | `minItems: 1, maxItems: 10` | Brand color palette (hex codes) |
| `brand_identity.style` | `string` | `enum: modern, playful, corporate, minimal, bold` | Visual style direction |
| `platforms` | `array<string>` | `minItems: 1, enum items: instagram, facebook, twitter, linkedin, tiktok` | Target social platforms |
| `content_type` | `string` | `enum: quote, announcement, product, event, educational` | Type of content |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `brand_identity.fonts` | `array<string>` | `[]` | Font families to use |
| `brand_identity.logo_url` | `string` | `null` | URL to brand logo |
| `variations` | `integer` | `3` | Number of design variations (min: 1, max: 5) |
| `include_copy` | `boolean` | `true` | Generate caption copy |
| `language` | `string` | `"en"` | Two-letter ISO 639-1 language code |

### Example Input

```json
{
  "campaign_name": "FlowMind Launch",
  "campaign_goal": "announcement",
  "message": "Introducing FlowMind - AI-powered productivity that adapts to how you work",
  "brand_identity": {
    "colors": ["#0066FF", "#00C9FF", "#1A1A1A", "#F5F5F5"],
    "fonts": ["Inter", "Space Grotesk"],
    "style": "modern"
  },
  "platforms": ["instagram", "linkedin", "twitter"],
  "content_type": "product",
  "variations": 3,
  "include_copy": true,
  "language": "en"
}
```

## Output Schema

### Success Response

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"success"` |
| `data` | `object` | Contains graphics package and metadata |
| `errors` | `array` | Empty array |

### Data Object Structure

| Field | Type | Description |
|-------|------|-------------|
| `campaign_name` | `string` | Campaign identifier |
| `total_graphics` | `integer` | Total number of graphics generated |
| `platforms` | `array<string>` | Platforms covered |
| `graphics` | `array<object>` | Array of graphic specifications |
| `brand_colors_used` | `array<string>` | Colors applied |
| `fonts_used` | `array<string>` | Fonts applied |

### Graphic Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique graphic identifier |
| `platform` | `string` | Target platform |
| `format` | `string` | Post format (feed_post, story, etc.) |
| `dimensions` | `object` | Width and height in pixels |
| `design_url` | `string` | URL to generated design (simulated) |
| `copy` | `string` | Caption text |
| `hashtags` | `array<string>` | Recommended hashtags |

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
    "campaign_name": "FlowMind Launch",
    "total_graphics": 9,
    "platforms": ["instagram", "linkedin", "twitter"],
    "graphics": [
      {
        "id": "ig_post_001",
        "platform": "instagram",
        "format": "feed_post",
        "dimensions": {"width": 1080, "height": 1080},
        "design_url": "https://cdn.example.com/flowmind_ig_001.png",
        "copy": "Introducing FlowMind 🚀 AI-powered productivity that adapts to you.",
        "hashtags": ["#FlowMind", "#ProductivityAI", "#WorkSmarter"]
      }
    ],
    "brand_colors_used": ["#0066FF", "#00C9FF", "#1A1A1A", "#F5F5F5"],
    "fonts_used": ["Inter", "Space Grotesk"]
  },
  "errors": []
}
```

## Logic Breakdown

### Step 1: Input Validation
- Validate all required fields are present
- Check platform enum values
- Validate color format (hex codes)
- Verify variations count within limits
- Return structured errors if validation fails

### Step 2: Platform Analysis
- Map each platform to required formats (feed, story, etc.)
- Determine optimal dimensions per format
- Calculate total graphics count (platforms × variations)
- Apply platform-specific design constraints

### Step 3: Design System Setup
- Parse brand identity (colors, fonts, style)
- Create color palette with primary, secondary, accent
- Define typography hierarchy (headline, body, accent)
- Establish visual consistency rules based on style

### Step 4: Layout Generation
- Select layout templates based on content_type
- Apply style-specific layout patterns
- Optimize text placement for readability
- Balance visual elements and white space
- Ensure mobile-first design principles

### Step 5: Content Adaptation
- Craft platform-specific headlines (respect character limits)
- Generate engaging captions optimized per platform
- Create relevant hashtag sets (3-10 per post)
- Adapt message tone for platform audience
- Apply emoji strategy based on platform and tone

### Step 6: Variation Creation
- Generate design variations (color emphasis, layout, composition)
- Maintain brand consistency across variations
- Create A/B test recommendations
- Ensure each variation has distinct visual identity

### Step 7: Accessibility & Compliance
- Ensure WCAG AA contrast ratios (4.5:1 minimum)
- Generate descriptive alt text for each graphic
- Check text readability on all backgrounds
- Validate against platform specifications
- Verify safe zones for text and logos

### Step 8: Output Formatting
- Structure graphics array with all specifications
- Include design URLs (simulated CDN paths)
- Add usage metadata (colors used, fonts used)
- Return standardized response structure

## Handler Contract

```python
def run(params: dict) -> dict:
    """
    Execute the social media graphics package generation logic.
    
    Args:
        params: Validated input parameters
        
    Returns:
        dict with status, data, errors
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
- Platform specification database (dimensions, formats)
- Design template library
- Hashtag recommendation system

## Performance Criteria

| Metric | Target | Notes |
|--------|--------|-------|
| **Execution Time** | < 8 seconds | For 10 graphics across 3 platforms |
| **Memory Usage** | < 100 MB | Peak usage during generation |
| **Success Rate** | > 99% | For valid inputs |
| **Design Consistency** | > 9/10 | Brand alignment score |
| **Platform Compliance** | 100% | All specs must match platform requirements |

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `VALIDATION_ERROR` | Missing required field or invalid type | Check input against schema |
| `INVALID_PLATFORM` | Platform not in allowed enum | Use: instagram, facebook, twitter, linkedin, tiktok |
| `INVALID_STYLE` | Style not in allowed enum | Use: modern, playful, corporate, minimal, bold |
| `INVALID_CONTENT_TYPE` | Content type not in allowed enum | Use: quote, announcement, product, event, educational |
| `PROCESSING_ERROR` | Core logic failed | Check logs for details |

## Testing Strategy

### Unit Tests
- Test input validation with missing fields
- Test platform dimension mapping
- Test color palette generation
- Test layout selection for each content_type
- Test caption generation for each platform
- Test hashtag generation
- Test error handling

### Property-Based Tests
- Generate random valid inputs
- Verify output structure matches schema
- Check all graphics have valid dimensions
- Verify platform compliance
- Check color contrast ratios

### Integration Tests
- Test via MCP protocol (tools/call)
- Verify schema compliance
- Test all platform combinations
- Test all style variations
- Test edge cases (max variations, single platform)

## Sample Test Cases

### Test Case 1: Multi-Platform Product Launch
```json
{
  "input": {
    "campaign_name": "FlowMind Launch",
    "campaign_goal": "announcement",
    "message": "Introducing FlowMind",
    "brand_identity": {
      "colors": ["#0066FF", "#00C9FF"],
      "style": "modern"
    },
    "platforms": ["instagram", "linkedin"],
    "content_type": "product",
    "variations": 2
  },
  "expected_output": {
    "status": "success",
    "data": {
      "total_graphics": 4,
      "platforms": ["instagram", "linkedin"]
    }
  }
}
```

### Test Case 2: Missing Required Field
```json
{
  "input": {
    "campaign_name": "Test Campaign",
    "message": "Test message"
  },
  "expected_output": {
    "status": "error",
    "errors": [
      "Missing required field: campaign_goal",
      "Missing required field: brand_identity",
      "Missing required field: platforms",
      "Missing required field: content_type"
    ]
  }
}
```

## Implementation Checklist

- [ ] Create `schema.json` with JSON Schema Draft 2020-12
- [ ] Create `handler.py` with `run(params)` method
- [ ] Implement input validation
- [ ] Implement platform dimension mapping
- [ ] Implement design system setup
- [ ] Implement layout generation logic
- [ ] Implement content adaptation (captions, hashtags)
- [ ] Implement variation generation
- [ ] Implement accessibility checks
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
- Design URLs are simulated (no actual image generation)
- No actual design rendering engine
- Limited to 5 style variations
- No actual brand logo integration
- Hashtag generation is pattern-based, not data-driven

**Future Improvements**:
- Integrate with actual design rendering API (Canva, Figma)
- Add AI-powered hashtag recommendations based on trending data
- Support animated graphics and video formats
- Add brand asset library integration
- Implement actual accessibility testing tools
- Support more platforms (Pinterest, Snapchat, YouTube Community)
- Add performance prediction (estimated engagement rates)
