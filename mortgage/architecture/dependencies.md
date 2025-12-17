# Mortgage MCP - Dependencies Documentation

## Runtime Dependencies

### Python
- **Version**: Python 3.8 or higher
- **Purpose**: Handler execution
- **Modules Used**:
  - `json` (built-in)
  - `sys` (built-in)
  - `re` (built-in)
  - `datetime` (built-in)

**No external Python packages required** - All handlers use only Python standard library.

## System Dependencies

### JSON Schema Validation
- **Standard**: JSON Schema Draft 2020-12
- **Purpose**: Input validation
- **Implementation**: Schema files follow JSON Schema 2020 specification
- **Validation**: Handlers perform basic validation; full schema validation can be added with `jsonschema` package (optional)

## Integration Dependencies

### Proposal Engine
- **Location**: `qontrek-mcp-lab/proposal-engine/`
- **Purpose**: Generate proposals from normalized data
- **Integration Point**: `proposal_payload` field in handler output
- **Required Fields**:
  - `status: "ready_for_proposal"`
  - `vertical: "mortgage-lppsa"`
  - `customer_id` or `property_id`
  - `data` (normalized data object)

### Document Factory
- **Location**: `qontrek-mcp-lab/document-factory/`
- **Purpose**: Generate documents from normalized data
- **Integration Point**: `normalized_data` field in handler output
- **Usage**: Can consume `*_form_fields` objects from normalized data

## Optional Dependencies

### JSON Schema Validator (Python)
If full JSON Schema validation is desired:
```bash
pip install jsonschema
```

### Testing Framework
For automated testing:
```bash
pip install pytest pytest-json
```

## File Structure Dependencies

```
qontrek-mcp-lab/
├── mortgage/
│   ├── manifests/
│   │   └── mortgage_mcp_manifest.json
│   ├── schemas/
│   │   ├── lppsa_intake.schema.json
│   │   ├── takaful_submission.schema.json
│   │   ├── lawyer_intake.schema.json
│   │   └── property_checklist.schema.json
│   ├── tools/
│   │   ├── lppsa_intake.json
│   │   ├── takaful_submission.json
│   │   ├── lawyer_intake.json
│   │   └── property_checklist.json
│   ├── handlers/
│   │   ├── handle_lppsa_intake.py
│   │   ├── handle_takaful_submission.py
│   │   ├── handle_lawyer_intake.py
│   │   └── handle_property_checklist.py
│   └── test/
│       └── test_mortgage_mcp.json
├── proposal-engine/ (external dependency)
└── document-factory/ (external dependency)
```

## Handler Execution Dependencies

### Command-Line Interface
Handlers can be executed via:
```bash
echo '{"input": "data"}' | python mortgage/handlers/handle_lppsa_intake.py
```

### Standard Input/Output
- **Input**: JSON via `stdin`
- **Output**: JSON via `stdout`
- **Errors**: JSON error responses via `stdout` + `stderr` for logs

## Data Format Dependencies

### Input Format
- **Type**: JSON
- **Encoding**: UTF-8
- **Schema**: Must match corresponding schema file

### Output Format
- **Type**: JSON
- **Encoding**: UTF-8
- **Structure**: 
  ```json
  {
    "status": "success" | "error",
    "normalized_data": { ... } | null,
    "proposal_payload": { ... } | null,
    "errors": [ ... ]
  }
  ```

## External Service Dependencies

### None Required
All handlers operate in **simulation mode** - no external API calls are made.

### Future Extensions
If real API integration is needed:
- LPPSA API (for eligibility verification)
- Takaful provider API (for premium calculation)
- Lawyer panel database (for verification)
- Property registry API (for validation)

## Platform Dependencies

### Operating System
- **Linux**: Fully supported
- **macOS**: Fully supported
- **Windows**: Supported (Python 3.8+)

### File Permissions
Handlers require:
- Read access to schema files (if schema validation is added)
- Execute permission for Python scripts

## Version Compatibility

### Python Versions
- **Python 3.8**: ✅ Supported
- **Python 3.9**: ✅ Supported
- **Python 3.10**: ✅ Supported
- **Python 3.11**: ✅ Supported
- **Python 3.12**: ✅ Supported

### JSON Schema
- **Draft 2020-12**: ✅ Supported (current)
- **Draft 2019-09**: ⚠️ Compatible (with minor adjustments)
- **Draft 7**: ⚠️ Compatible (with minor adjustments)

## Installation

### Minimal Setup
No installation required - handlers use Python standard library only.

### Optional Setup
```bash
# Install JSON Schema validator (optional)
pip install jsonschema

# Install testing framework (optional)
pip install pytest pytest-json
```

## Summary

**Required Dependencies**: None (Python 3.8+ with standard library)

**Optional Dependencies**: 
- `jsonschema` for full schema validation
- `pytest` for automated testing

**Integration Dependencies**:
- Proposal Engine (for proposal generation)
- Document Factory (for document generation)

