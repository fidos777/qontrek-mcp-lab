# KuasaTurbo Gateway

Lightweight REST API for KuasaTurbo microservices platform.

## Overview

KuasaTurbo Gateway provides a single HTTP endpoint for executing AI-powered business automation workflows. Each service combines:

- **Widget (L3)**: UI field definitions
- **Workflow (L8)**: Execution logic
- **Persona (L5)**: Tone and behavior

## Architecture

```
┌─────────────────────────────────────────────┐
│  POST /v1/execute                           │
│  - Validate request                         │
│  - Load widget, workflow, persona           │
│  - Build AI prompt                          │
│  - Generate output (mock or real)           │
│  - Return structured response               │
└─────────────────────────────────────────────┘
```

## Quick Start

### 1. Setup

```bash
./kuasaturbo/setup.sh
```

### 2. Start Server

```bash
./kuasaturbo/server.sh
```

Server runs on `http://localhost:8081`

### 3. Execute Service

```bash
curl -X POST http://localhost:8081/v1/execute \
  -H "Content-Type: application/json" \
  -H "X-API-Key: kuasa123" \
  -d '{
    "service_id": "content_idea",
    "payload": {
      "topic": "AI automation",
      "audience": "SME owners",
      "platform": "tiktok"
    },
    "model": "mock"
  }'
```

## Available Services

| Service ID | Description | Vertical |
|------------|-------------|----------|
| content_idea | Generate 10 content ideas | content |
| caption_builder | Generate 3-5 captions | content |
| invoice_gen | Generate invoice summary | accounting |
| lead_intake | Process new lead | crm |
| trade_in_eval | Evaluate vehicle trade-in | automotive |
| loan_check | Check loan eligibility | automotive |
| attendance | Record attendance | hr |
| menu_update | Update menu item | fnb |

## API Reference

### POST /v1/execute

Execute a KuasaTurbo service.

**Headers:**
- `X-API-Key`: API key (default: `kuasa123`)
- `Content-Type`: `application/json`

**Request Body:**
```json
{
  "service_id": "content_idea",
  "payload": {
    "topic": "AI automation",
    "audience": "SME owners",
    "platform": "tiktok"
  },
  "persona_override": "jordan_cfo_analyst.v1",
  "model": "mock"
}
```

**Response:**
```json
{
  "status": "success",
  "service_id": "content_idea",
  "workflow_id": "content_idea_workflow.v1",
  "persona_id": "zeyti_bbnu_creator.v1",
  "output": {
    "ideas": [
      "10 cara AI boleh automate bisnes SME...",
      "..."
    ]
  },
  "metadata": {
    "timestamp": "2025-12-08T10:30:00",
    "model": "mock",
    "widget_id": "content_idea_widget.v1",
    "vertical": "content",
    "execution_mode": "mock"
  }
}
```

## Configuration

Environment variables:

```bash
export KUASATURBO_API_KEY=your_key
export KUASATURBO_HOST=0.0.0.0
export KUASATURBO_PORT=8081
```

## Testing

Run all tests:

```bash
./tests/kuasaturbo/run_all_tests.sh
```

Run individual test:

```bash
python3 tests/kuasaturbo/test_service_execution.py
```

## Project Structure

```
kuasaturbo/
├── api/
│   ├── gateway.py          # FastAPI app
│   ├── router.py           # Service execution
│   └── validators.py       # Request validation
├── services/
│   ├── ai_client.py        # AI generation (mock mode)
│   └── prompt_builder.py   # Prompt assembly
├── shared/
│   └── config.py           # Configuration
├── server.sh               # Start server
└── setup.sh                # Setup script
```

## Mock Mode

By default, the gateway runs in mock mode with simulated AI outputs. This allows:

- Testing without API keys
- Predictable outputs
- Fast execution
- No external dependencies

Future phases will add real LLM integration.

## Error Handling

### 401 Unauthorized
Invalid API key.

### 400 Bad Request
- Service not found
- Missing required fields
- Invalid field types
- Invalid persona override

### 500 Internal Server Error
Service execution failed.

## Constraints

KuasaTurbo is governance-free. The following are NOT allowed:

- ❌ Governance gates
- ❌ Ledger events
- ❌ Audit trails
- ❌ Compliance logic
- ❌ Multi-party approvals
- ❌ SLA enforcement

## Next Steps

Future phases:
- Real LLM integration (GPT-4, Claude, Gemini)
- Multi-model routing
- Response caching
- Rate limiting
- Analytics

---

**Version**: 1.0.0  
**Status**: Production Ready (Mock Mode)  
**License**: Proprietary
