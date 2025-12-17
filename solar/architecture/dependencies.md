# Solar MCP - Dependencies Documentation

## Runtime Dependencies

### Python
- **Version**: Python 3.8 or higher
- **Purpose**: Handler execution
- **Modules Used**:
  - `json` (built-in)
  - `sys` (built-in)
  - `os` (built-in)
  - `datetime` (built-in)
  - `re` (built-in)

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
  - `vertical: "solar"`
  - `customer_id` or `property_id`
  - `data` (normalized data object)

### Document Factory
- **Location**: `qontrek-mcp-lab/document-factory/`
- **Purpose**: Generate documents from normalized data
- **Integration Point**: `normalized_data` field in handler output
- **Usage**: Can consume `*_form_fields` objects from normalized data

### FireCrawl Brandpacks
- **Location**: `qontrek-mcp-lab/brandpacks/_template/`
- **Purpose**: Apply branding themes to quotations
- **Integration Point**: `brandpack_id` in quotation input
- **Format**: JSON files with colors, fonts, logos, and style
- **Default**: Falls back to default brandpack if not found

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
├── solar/
│   ├── manifests/
│   │   └── solar_mcp_manifest.json
│   ├── schemas/
│   │   ├── lead_intake.schema.json
│   │   ├── site_inspection.schema.json
│   │   ├── roi.schema.json
│   │   ├── roof_check.schema.json
│   │   └── quotation.schema.json
│   ├── tools/
│   │   ├── lead_intake.json
│   │   ├── site_inspection.json
│   │   ├── roi.json
│   │   ├── roof_check.json
│   │   └── quotation.json
│   ├── handlers/
│   │   ├── handle_lead_intake.py
│   │   ├── handle_site_inspection.py
│   │   ├── handle_roi.py
│   │   ├── handle_roof_check.py
│   │   └── handle_quotation.py
│   └── test/
│       └── test_solar_mcp.json
├── proposal-engine/ (external dependency)
├── document-factory/ (external dependency)
└── brandpacks/
    └── _template/ (external dependency for brandpack files)
```

## Handler Execution Dependencies

### Command-Line Interface
Handlers can be executed via:
```bash
echo '{"input": "data"}' | python solar/handlers/handle_lead_intake.py
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
- Solar irradiance API (for accurate generation estimates)
- Weather API (for shading analysis)
- Roof assessment API (for structural analysis)
- Component pricing API (for real-time pricing)

## Platform Dependencies

### Operating System
- **Linux**: Fully supported
- **macOS**: Fully supported
- **Windows**: Supported (Python 3.8+)

### File Permissions
Handlers require:
- Read access to brandpack files (if brandpack integration is used)
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

## Brandpack Integration

### Brandpack File Format
Brandpacks should be stored as JSON files in `brandpacks/_template/`:

```json
{
  "id": "voltek",
  "name": "Voltek Brandpack",
  "colors": {
    "primary": "#0066CC",
    "secondary": "#00AA44",
    "accent": "#FF6600",
    "background": "#FFFFFF",
    "text": "#333333"
  },
  "logo": "https://example.com/logo.png",
  "fonts": {
    "heading": "Arial, sans-serif",
    "body": "Arial, sans-serif"
  },
  "style": "modern"
}
```

### Default Brandpack
If brandpack file is not found, handlers use a default brandpack structure.

## Summary

**Required Dependencies**: None (Python 3.8+ with standard library)

**Optional Dependencies**: 
- `jsonschema` for full schema validation
- `pytest` for automated testing

**Integration Dependencies**:
- Proposal Engine (for proposal generation)
- Document Factory (for document generation)
- FireCrawl Brandpacks (for quotation theming)

