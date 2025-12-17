# Brand Context Normalizer v1

## Overview

The Brand Context Normalizer is a semantic transformer skill that converts creative workflow outputs (slogans, landing pages, social media content) into structured business context including mission statements, positioning, ICP (Ideal Customer Profile), and messaging frameworks.

## Purpose

After running creative workflows, you often need to extract strategic business insights. This skill bridges the gap between creative execution and business strategy by:

1. **Inferring Mission** - Derives mission statements from hero messaging and brand themes
2. **Deriving Positioning** - Constructs positioning statements from slogans and benefits
3. **Extracting Value Proposition** - Identifies core value props from landing page content
4. **Reconstructing ICP** - Builds detailed customer profiles from tone and messaging patterns
5. **Unifying Brand Themes** - Identifies consistent themes across all creative outputs
6. **Producing Messaging Guidelines** - Creates comprehensive messaging frameworks

## Input Schema

### Required Fields

```json
{
  "brand": {
    "brand_name": "string",
    "industry": "string",
    "target_audience": "string",
    "brand_values": ["string"],
    "tone": "string (optional)",
    "value_proposition": "string (optional)"
  },
  "creative": {
    "slogan": {
      "status": "success",
      "output": {
        "slogans": [...],
        "brand_analysis": {...}
      }
    },
    "landing_page": {
      "status": "success",
      "output": {
        "sections": [...],
        "meta": {...}
      }
    },
    "social_pack": {
      "status": "success",
      "output": {
        "graphics": [...],
        "campaign_name": "string"
      }
    }
  }
}
```

### Creative Outputs

The skill accepts output envelopes from:
- `brandpack.slogan.v1` - For brand themes and positioning signals
- `pagegen.landingpage.v1` - For hero content, benefits, and value props
- `graphicgen.socialpack.v1` - For messaging patterns and tone signals

## Output Structure

```json
{
  "status": "success",
  "output": {
    "brand_name": "string",
    "mission": "string",
    "positioning": "string",
    "value_proposition": "string",
    "icp": {
      "demographics": "string",
      "psychographics": ["string"],
      "pain_points": ["string"],
      "goals": ["string"]
    },
    "brand_themes": ["string"],
    "unified_tone": "string",
    "narrative": "string",
    "messaging_framework": {
      "tone": "string",
      "voice_guidelines": {
        "voice": "string",
        "language": "string",
        "style": "string"
      },
      "key_messages": ["string"],
      "do": ["string"],
      "dont": ["string"]
    },
    "metadata": {
      "normalized_at": "ISO8601",
      "version": "1.0.0",
      "sources": {
        "slogan": boolean,
        "landing_page": boolean,
        "social_pack": boolean
      }
    }
  },
  "errors": []
}
```

## Transformation Logic

### 1. Mission Inference
- Extracts hero headline and subheadline
- Combines with brand themes and values
- Constructs action-oriented mission statement

### 2. Positioning Derivation
- Uses top-rated slogan as positioning anchor
- Incorporates primary benefit from landing page
- Formats as: "For [audience], we are the [tone] [industry] solution that delivers [benefit]. [Slogan]."

### 3. Value Proposition Extraction
- Combines hero headline with top 3 benefits
- Creates concise, benefit-focused statement

### 4. ICP Reconstruction
- **Demographics**: From target_audience field
- **Psychographics**: Inferred from tone (professional → results-oriented, playful → creative, etc.)
- **Pain Points**: Extracted from social messaging patterns (time, automation, integration keywords)
- **Goals**: Standard goal set based on industry patterns

### 5. Brand Theme Identification
- Aggregates themes from slogan analysis
- Extracts themes from benefit titles (time → efficiency, AI → innovation)
- Identifies patterns in social messaging
- Returns top 5 unified themes

### 6. Tone Unification
- Compares brand tone with slogan tone
- Defaults to brand tone if consistent
- Ensures single unified tone across all outputs

### 7. Messaging Framework Production
- **Voice Guidelines**: Tone-specific voice, language, and style rules
- **Key Messages**: Top 5 messages from value prop, slogan, and themes
- **Do/Don't Lists**: Actionable messaging guidelines

## WTO Integration

The normalized output is designed to populate these WTO sections:

```json
{
  "business": {
    "positioning": {
      "workflow_id": "brand_context.normalize.v1",
      "output": {
        "mission": "...",
        "positioning": "...",
        "narrative": "..."
      }
    },
    "value_prop": {
      "workflow_id": "brand_context.normalize.v1",
      "output": {
        "value_proposition": "..."
      }
    },
    "icp": {
      "workflow_id": "brand_context.normalize.v1",
      "output": {
        "icp": {...}
      }
    },
    "messaging": {
      "workflow_id": "brand_context.normalize.v1",
      "output": {
        "messaging_framework": {...}
      }
    }
  }
}
```

## Usage Example

### Standalone Execution

```bash
echo '{
  "brand": {
    "brand_name": "FlowMind",
    "industry": "SaaS/Productivity",
    "target_audience": "Remote workers aged 25-40",
    "brand_values": ["efficiency", "simplicity"],
    "tone": "professional"
  },
  "creative": {
    "slogan": {...},
    "landing_page": {...},
    "social_pack": {...}
  }
}' | PYTHONPATH=. python3 skills/kreator/brand_context.normalize.v1/handler.py
```

### In Workflow

```json
{
  "steps": [
    {
      "id": "creative_funnel",
      "workflow": "kreator.creative_funnel.v1"
    },
    {
      "id": "normalize",
      "skill": "normalize_brand_context",
      "input_map": {
        "brand": "input.brand",
        "creative.slogan": "creative_funnel.slogan",
        "creative.landing_page": "creative_funnel.landing",
        "creative.social_pack": "creative_funnel.socialpack"
      }
    }
  ]
}
```

### With Packager

```python
from l6.utils.packager import WorkflowPackager

packager = WorkflowPackager()

# Run normalization
result = handler.run(params)

# Add to WTO
wto = packager.add_workflow_output(
    wto,
    category="business",
    output_type="positioning",
    workflow_id="brand_context.normalize.v1",
    workflow_output=result
)
```

## Validation

### JSON Schema Validation
```bash
python3 -m json.tool skills/kreator/brand_context.normalize.v1/schema.json > /dev/null
python3 -m json.tool skills/kreator/brand_context.normalize.v1/manifest.json > /dev/null
```

### Output Envelope Compliance
```bash
# Check output structure matches {status, output, errors}
PYTHONPATH=. python3 skills/kreator/brand_context.normalize.v1/handler.py < sample_inputs.json | jq '.status, .output, .errors'
```

### Import Test
```bash
python3 -c "import sys; sys.path.insert(0, '.'); from skills.kreator.brand_context.normalize.v1 import handler; print('✅ Import successful')"
```

## Error Handling

The skill returns structured errors for:

- **Missing brand context**: `"Missing required field: brand"`
- **Missing creative outputs**: `"Missing required field: creative"`
- **Invalid JSON input**: `"Invalid JSON input: {error}"`
- **Handler exceptions**: `"Handler error: {error}"`

All errors are returned in the `errors` array with `status: "error"`.

## Performance Characteristics

- **Execution Time**: < 100ms for typical inputs
- **Memory Usage**: Minimal (< 10MB)
- **Dependencies**: Python stdlib only
- **Concurrency**: Stateless, fully concurrent-safe

## Limitations

1. **Requires Creative Outputs**: Needs at least one creative output (slogan, landing, or social) to produce meaningful results
2. **English Only**: Currently optimized for English language inputs
3. **Heuristic-Based**: Uses pattern matching and heuristics, not ML models
4. **Theme Extraction**: Limited to predefined theme categories

## Future Enhancements

- Multi-language support
- ML-based theme extraction
- Competitive positioning analysis
- Brand voice scoring
- Sentiment analysis integration

## Integration Points

### Upstream Skills
- `brandpack.slogan.v1` - Provides brand themes and positioning signals
- `pagegen.landingpage.v1` - Provides hero content and benefits
- `graphicgen.socialpack.v1` - Provides messaging patterns

### Downstream Use Cases
- Business strategy documents
- Consultant kits
- Brand guidelines
- Marketing briefs
- Investor presentations

## Metadata

- **Version**: 1.0.0
- **Domain**: kreator
- **Type**: transformer
- **Author**: KuasaTurbo L6 Team
- **Created**: 2024-12-07
- **Python**: >=3.8
- **Dependencies**: stdlib only

## Support

For issues or questions:
1. Check sample_inputs.json and sample_outputs.json for examples
2. Validate input schema compliance
3. Review transformation logic in handler.py
4. Check structured logs for debugging
