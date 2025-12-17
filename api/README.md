# Phase D: Runtime REST API (MVP)

## Overview

Minimal FastAPI layer exposing Phase A-C functionality via HTTP endpoints.

## Installation

Install required dependencies:

```bash
pip3 install -r api/requirements.txt
```

Or install individually:

```bash
pip3 install fastapi uvicorn pydantic
```

## Starting the Server

```bash
# Set API key (optional, defaults to test123)
export API_KEY="your_secret_key"

# Start server
./api/server.sh
```

Server will run on `http://0.0.0.0:8080`

## API Endpoints

### POST /skills/execute

Execute a single skill via dispatcher.

**Request:**
```json
{
  "skill_id": "launchkit.branding.generate.v1",
  "payload": {
    "brand_name": "MyBrand",
    "mission": "Our mission",
    "brand_themes": ["Innovation", "Quality"],
    "icp": {
      "demographics": "Target audience"
    }
  }
}
```

**Headers:**
- `Content-Type: application/json`
- `X-API-Key: your_api_key`

**Response:**
```json
{
  "status": "success",
  "output": {
    "brand_identity": {...},
    "visual_guidelines": {...}
  }
}
```

### POST /workflows/execute

Execute a complete workflow via runner_v2.

**Request:**
```json
{
  "workflow_id": "kuasaturbo.launchkit.v1",
  "payload": {
    "brand_name": "MyBrand",
    "mission": "Our mission",
    "brand_themes": ["Innovation", "Quality"],
    "icp": {
      "demographics": "Target audience"
    }
  }
}
```

**Headers:**
- `Content-Type: application/json`
- `X-API-Key: your_api_key`

**Response:**
```json
{
  "workflow_id": "kuasaturbo.launchkit.v1",
  "status": "success",
  "completed_steps": ["branding", "prd", "pricing", "roadmap", "pitchdeck", "socialpack"],
  "pending_steps": [],
  "failed_steps": [],
  "outputs": {
    "branding": {...},
    "prd": {...},
    "pricing": {...},
    "roadmap": {...},
    "pitchdeck": {...},
    "socialpack": {...}
  },
  "errors": [],
  "trace_id": "wf_abc123",
  "started_at": "2025-12-08T...",
  "finished_at": "2025-12-08T..."
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "phase": "D"
}
```

## Error Responses

All errors return consistent envelope format:

### 401 Unauthorized
```json
{
  "status": "failed",
  "error": {
    "type": "unauthorized",
    "message": "Missing X-API-Key header"
  }
}
```

### Unknown Skill
```json
{
  "status": "failed",
  "error": {
    "type": "unknown_skill",
    "message": "Skill not found: invalid.skill.id"
  }
}
```

### Unknown Workflow
```json
{
  "status": "failed",
  "errors": [{
    "step_id": "workflow",
    "type": "unknown_workflow",
    "message": "Workflow not found: invalid.workflow.id"
  }]
}
```

### Invalid Brand Context
```json
{
  "status": "failed",
  "errors": [{
    "step_id": "brand_context_normalization",
    "type": "brand_context_invalid",
    "message": "Missing required fields: brand_name"
  }]
}
```

## Testing

Run the test suite:

```bash
# Start server in one terminal
./api/server.sh

# Run tests in another terminal
bash tests/test_api.sh
```

## Example Usage

### Using curl

```bash
# Execute a skill
curl -X POST http://localhost:8080/skills/execute \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "skill_id": "launchkit.branding.generate.v1",
    "payload": {
      "brand_name": "TechCorp",
      "mission": "Innovate the future",
      "brand_themes": ["Innovation", "Trust"],
      "icp": {
        "demographics": "Tech professionals"
      }
    }
  }'

# Execute a workflow
curl -X POST http://localhost:8080/workflows/execute \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test123" \
  -d '{
    "workflow_id": "kuasaturbo.launchkit.v1",
    "payload": {
      "brand_name": "TechCorp",
      "mission": "Innovate the future",
      "brand_themes": ["Innovation", "Trust"],
      "icp": {
        "demographics": "Tech professionals"
      }
    }
  }'
```

### Using Python

```python
import requests

API_URL = "http://localhost:8080"
API_KEY = "test123"

# Execute skill
response = requests.post(
    f"{API_URL}/skills/execute",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    },
    json={
        "skill_id": "launchkit.branding.generate.v1",
        "payload": {
            "brand_name": "TechCorp",
            "mission": "Innovate the future",
            "brand_themes": ["Innovation", "Trust"],
            "icp": {
                "demographics": "Tech professionals"
            }
        }
    }
)

print(response.json())

# Execute workflow
response = requests.post(
    f"{API_URL}/workflows/execute",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    },
    json={
        "workflow_id": "kuasaturbo.launchkit.v1",
        "payload": {
            "brand_name": "TechCorp",
            "mission": "Innovate the future",
            "brand_themes": ["Innovation", "Trust"],
            "icp": {
                "demographics": "Tech professionals"
            }
        }
    }
)

print(response.json())
```

## Architecture

```
HTTP Request
     ↓
FastAPI (api/main.py)
     ↓
API Key Validation (api/config.py)
     ↓
┌────────────────┬────────────────┐
│                │                │
↓                ↓                ↓
/skills/execute  /workflows/execute  /health
     ↓                ↓
dispatcher_mvp   runner_v2
     ↓                ↓
Phase A          Phase B + C
     ↓                ↓
HTTP Response    HTTP Response
```

## Configuration

### Environment Variables

- `API_KEY`: API key for authentication (default: `test123`)

### Server Settings

- Host: `0.0.0.0` (all interfaces)
- Port: `8080`
- CORS: Enabled (wildcard for MVP)

## Integration with Existing Layers

Phase D is a thin HTTP wrapper that:

1. **Validates API key** - Simple header-based auth
2. **Calls existing functions** - No logic duplication
   - `dispatcher_mvp.execute_skill()` for skills
   - `runner_v2.run_workflow()` for workflows
3. **Returns envelopes as-is** - No transformation

**No changes to:**
- Phase A (dispatcher)
- Phase B (workflow runner)
- Phase C (normalization)
- Any skills or workflows

## Limitations (By Design)

Phase D is intentionally minimal:

- ❌ No async/background tasks
- ❌ No governance layer
- ❌ No reflexion/scoring
- ❌ No versioning system
- ❌ No promotion flows
- ❌ No WebSockets
- ❌ No database
- ❌ No rate limiting (beyond basic auth)

These features belong to future phases.

## Troubleshooting

### Server won't start

Check if port 8080 is available:
```bash
lsof -i :8080
```

### Import errors

Ensure project root is in PYTHONPATH:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### API key issues

Check environment variable:
```bash
echo $API_KEY
```

Set explicitly:
```bash
export API_KEY="your_key"
./api/server.sh
```

## Next Steps

Phase D is complete when:
- ✅ Server runs locally
- ✅ Both routes respond correctly
- ✅ curl requests return envelopes identical to CLI
- ✅ All API tests pass
- ✅ No logging interferes with JSON responses
- ✅ No changes break Phases A, B, or C

Future phases may add:
- Governance and quality gates
- Async execution with status polling
- Promotion flows (dev → staging → prod)
- Advanced auth (JWT, OAuth)
- Rate limiting and quotas
- WebSocket support for streaming
