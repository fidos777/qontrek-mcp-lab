# SKILL: brandpack.slogan.v1

## Metadata

| Field | Value |
|-------|-------|
| **Skill ID** | `kreator.brandpack.slogan.v1` |
| **Domain** | `kreator` |
| **Version** | `v1` |
| **Owner** | Qontrek Kreator Team |
| **Status** | `production` |
| **Created** | 2024-12-07 |
| **Updated** | 2024-12-07 |

## Overview

Generates brand slogans and taglines based on brand identity, target audience, and positioning strategy. Creates multiple variations with different tones and styles optimized for memorability and brand alignment.

**Purpose**: Generate memorable, on-brand slogans and taglines for marketing campaigns, brand launches, and positioning exercises.

**Use Cases**:
- Brand launch campaigns requiring tagline options
- Rebranding initiatives needing fresh messaging
- Marketing teams exploring positioning alternatives
- SMEs developing brand identity without agency support
- A/B testing different brand messaging approaches

## Input Schema

### Required Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `brand_name` | `string` | `minLength: 1, maxLength: 100` | Name of the brand |
| `industry` | `string` | `minLength: 1, maxLength: 100` | Industry or sector (e.g., "SaaS/Productivity", "Fashion") |
| `target_audience` | `string` | `minLength: 1, maxLength: 500` | Description of target audience demographics and psychographics |
| `brand_values` | `array<string>` | `minItems: 1, maxItems: 10, item maxLength: 50` | Core brand values (e.g., ["efficiency", "trust", "innovation"]) |
| `tone` | `string` | `enum: professional, playful, inspirational, bold, minimalist` | Desired tone for the slogans |

### Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `language` | `string` | `"en"` | Two-letter ISO 639-1 language code (pattern: `^[a-z]{2}$`) |
| `count` | `integer` | `5` | Number of slogan variations to generate (min: 1, max: 10) |

### Example Input

```json
{
  "brand_name": "FlowMind",
  "industry": "SaaS/Productivity",
  "target_audience": "Remote workers and digital nomads aged 25-40",
  "brand_values": ["efficiency", "simplicity", "innovation", "focus"],
  "tone": "professional",
  "language": "en",
  "count": 5
}
```

## Output Schema

### Success Response

| Field | Type | Description |
|-------|------|-------------|
| `status` | `string` | Always `"success"` |
| `output` | `object` | Contains slogans, brand_analysis, and metadata |
| `errors` | `array` | Empty array |

### Output Object Structure

| Field | Type | Description |
|-------|------|-------------|
| `slogans` | `array<object>` | Array of generated slogans with scores |
| `brand_analysis` | `object` | Key themes and positioning summary |
| `metadata` | `object` | Generation timestamp, version, language |

### Slogan Object

| Field | Type | Description |
|-------|------|-------------|
| `text` | `string` | The slogan text |
| `tone` | `string` | Tone used (matches input) |
| `rationale` | `string` | Explanation of why this slogan works |
| `character_count` | `integer` | Length of slogan in characters |
| `memorability_score` | `number` | Score from 0-10 based on linguistic patterns |

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
    "slogans": [
      {
        "text": "Work Smarter, Flow Faster",
        "tone": "professional",
        "rationale": "Emphasizes efficiency and brand name while promising tangible productivity gains",
        "character_count": 26,
        "memorability_score": 8.5
      }
    ],
    "brand_analysis": {
      "key_themes": ["productivity", "simplicity", "efficiency"],
      "positioning_summary": "FlowMind positions as a professional brand focused on efficiency, simplicity, innovation for Remote workers aged 25-40"
    },
    "metadata": {
      "generated_at": "2024-12-07T10:30:00.000000",
      "version": "1.0.0",
      "language": "en"
    }
  },
  "errors": []
}
```

## Logic Breakdown

### Step 1: Input Validation
- Validate all required fields are present
- Check field types and constraints
- Validate tone enum value
- Return structured errors if validation fails

### Step 2: Theme Extraction
- Extract up to 5 core themes from brand values
- Add industry-specific themes based on industry keyword matching
- Deduplicate and prioritize themes
- Use themes as foundation for slogan generation

### Step 3: Slogan Generation
- Select tone-specific pattern templates
- Generate slogans by combining themes with patterns
- Apply linguistic techniques (alliteration, rhythm, parallel structure)
- Ensure brevity (optimal: 3-7 words, 10-60 characters)
- Create rationale for each slogan

### Step 4: Memorability Scoring
- Calculate base score (5.0)
- Add points for optimal word count (3-7 words: +2.0)
- Add points for optimal character count (10-40 chars: +1.5)
- Add points for alliteration (+1.0)
- Add points for rhythm (+0.5)
- Cap score at 10.0

### Step 5: Output Formatting
- Sort slogans by memorability score (descending)
- Build brand analysis with themes and positioning
- Add metadata with timestamp and version
- Return standardized response structure

## Handler Contract

```python
def handle_slogan_generation(input_data: dict) -> dict:
    """
    Execute the slogan generation logic.
    
    Args:
        input_data: Validated input parameters
        
    Returns:
        dict with status, output, errors
    """
    # Implementation follows steps 1-5 above
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
- None (self-contained skill)

## Performance Criteria

| Metric | Target | Notes |
|--------|--------|-------|
| **Execution Time** | < 3 seconds | 95th percentile for 10 slogans |
| **Memory Usage** | < 50 MB | Peak usage during generation |
| **Success Rate** | > 99% | For valid inputs |
| **Memorability Score** | > 6.0 | Average across generated slogans |

## Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `VALIDATION_ERROR` | Missing required field or invalid type | Check input against schema |
| `PROCESSING_ERROR` | Core logic failed | Check logs for details |
| `INVALID_TONE` | Tone not in allowed enum | Use: professional, playful, inspirational, bold, minimalist |

## Testing Strategy

### Unit Tests
- Test input validation with missing fields
- Test theme extraction with various industries
- Test memorability scoring algorithm
- Test slogan generation for each tone
- Test error handling

### Property-Based Tests
- Generate random valid inputs
- Verify output structure matches schema
- Check memorability scores are in range 0-10
- Verify slogan count matches input count

### Integration Tests
- Test via MCP protocol (tools/call)
- Verify schema compliance
- Test all tone variations
- Test edge cases (min/max counts, long brand names)

## Sample Test Cases

### Test Case 1: Valid Professional Tone
```json
{
  "input": {
    "brand_name": "Qontrek",
    "industry": "AI Automation",
    "target_audience": "SME Owners",
    "brand_values": ["system", "trust", "clarity"],
    "tone": "professional",
    "count": 3
  },
  "expected_output": {
    "status": "success",
    "output": {
      "slogans": [
        {"text": "Your System Partner", "memorability_score": 9.0}
      ]
    }
  }
}
```

### Test Case 2: Missing Required Field
```json
{
  "input": {
    "brand_name": "TestBrand",
    "industry": "Tech"
  },
  "expected_output": {
    "status": "error",
    "errors": [
      "Missing required field: target_audience",
      "Missing required field: brand_values",
      "Missing required field: tone"
    ]
  }
}
```

## Implementation Checklist

- [x] Create `schema.json` with JSON Schema Draft 2020-12
- [x] Create `handler.py` with `handle_slogan_generation()` function
- [x] Implement input validation
- [x] Implement theme extraction logic
- [x] Implement slogan generation with tone patterns
- [x] Implement memorability scoring
- [x] Add error handling
- [x] Create `sample_inputs.json`
- [x] Create `sample_outputs.json`
- [ ] Migrate to BaseHandler with `run(params)` method
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Update domain manifest

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1 | 2024-12-07 | Initial production implementation | Qontrek Team |

## Notes

**Current Limitations**:
- Handler uses custom `handle_slogan_generation()` instead of standard `run(params)` contract
- Logs to stdout instead of stderr (needs migration to structured logger)
- No actual NLP or trademark checking (uses pattern-based generation)
- Limited to 5 tone variations

**Future Improvements**:
- Migrate to BaseHandler contract
- Add actual NLP-based theme extraction
- Integrate trademark database API
- Support more languages beyond English
- Add A/B testing score predictions
- Generate visual mockups of slogans in context
