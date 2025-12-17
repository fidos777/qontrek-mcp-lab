# Requirements Document: MCP v2 Server Refactor

## Introduction

Transform the current single-domain MCP server into a production-grade, multi-domain MCP stdio server with standardized handler contracts, schema validation, and enterprise-ready logging.

## Glossary

- **MCP Server**: Model Context Protocol server implementing JSON-RPC 2.0 over stdio
- **Domain**: Top-level skill category (kreator, arkitek, mortgage, solar)
- **Skill**: Individual tool within a domain (e.g., brandpack.slogan.v1)
- **Handler Contract**: Standardized `run(params: dict) -> dict` interface
- **Schema Validation**: JSON Schema Draft 2020-12 validation using jsonschema library
- **stdio**: Standard input/output communication channel
- **stderr**: Standard error stream for logging only
- **stdout**: Standard output stream for JSON-RPC responses only

## Requirements

### Requirement 1: Multi-Domain Skill Discovery

**User Story:** As a system architect, I want the MCP server to discover and load skills from multiple domains, so that I can organize tools by business vertical or function.

#### Acceptance Criteria

1. WHEN the server starts THEN the system SHALL scan `skills/{domain}/` directories for all domains
2. WHEN a domain directory contains valid skills THEN the system SHALL load all skills with schema.json and handler.py
3. WHEN registering tools THEN the system SHALL use naming convention `{domain}_{skill}_{action}` (e.g., kreator_slogan_generate)
4. WHEN multiple domains exist THEN the system SHALL load skills from all domains without conflicts
5. WHEN a domain has a domain.json manifest THEN the system SHALL load domain metadata

### Requirement 2: Universal Handler Contract

**User Story:** As a skill developer, I want all handlers to implement a standard `run(params)` interface, so that the dispatcher can invoke any skill uniformly.

#### Acceptance Criteria

1. WHEN creating a handler THEN the handler SHALL extend BaseHandler class
2. WHEN the handler is invoked THEN the system SHALL call `run(params: dict) -> dict` method
3. WHEN the handler returns THEN the output SHALL contain `status`, `data`, and `errors` fields
4. WHEN an error occurs THEN the handler SHALL return `status: "error"` with error details
5. WHEN validation fails THEN the handler SHALL return structured error with field-level details

### Requirement 3: Schema Validation

**User Story:** As a system architect, I want automatic schema validation for all tool inputs, so that invalid requests are rejected before handler execution.

#### Acceptance Criteria

1. WHEN a tool is called THEN the system SHALL validate input against schema.json using jsonschema library
2. WHEN validation fails THEN the system SHALL return MCP error with validation details
3. WHEN schema.json is missing THEN the system SHALL log warning and skip validation
4. WHEN schema is invalid THEN the system SHALL fail skill loading with clear error
5. WHEN input is valid THEN the system SHALL pass validated params to handler

### Requirement 4: Structured Logging

**User Story:** As a DevOps engineer, I want all logs written to stderr in structured JSON format, so that I can aggregate and analyze logs effectively.

#### Acceptance Criteria

1. WHEN the server logs THEN all logs SHALL be written to stderr only
2. WHEN logging THEN the system SHALL use JSON format with timestamp, level, message, context
3. WHEN handlers execute THEN handler logs SHALL go to stderr via logger
4. WHEN JSON-RPC responses are sent THEN stdout SHALL contain only clean JSON
5. WHEN log level is set THEN the system SHALL respect DEBUG, INFO, WARN, ERROR levels

### Requirement 5: Kreator Domain Skills

**User Story:** As a marketing team, I want three kreator skills available (slogan, socialpack, landingpage), so that I can generate marketing content via MCP.

#### Acceptance Criteria

1. WHEN the server starts THEN the system SHALL load brandpack.slogan.v1 skill
2. WHEN the server starts THEN the system SHALL load graphicgen.socialpack.v1 skill
3. WHEN the server starts THEN the system SHALL load pagegen.landingpage.v1 skill
4. WHEN tools/list is called THEN all three kreator skills SHALL be listed
5. WHEN any kreator skill is called THEN the handler SHALL execute via run(params) contract

### Requirement 6: Base Infrastructure

**User Story:** As a system architect, I want reusable base classes and utilities, so that skill development is consistent and maintainable.

#### Acceptance Criteria

1. WHEN creating handlers THEN developers SHALL use BaseHandler abstract class
2. WHEN validating schemas THEN developers SHALL use SchemaValidator utility
3. WHEN logging THEN developers SHALL use StructuredLogger utility
4. WHEN handling errors THEN developers SHALL use ErrorBuilder utility
5. WHEN the lib/ directory exists THEN all utilities SHALL be importable

### Requirement 7: Persistent Session

**User Story:** As a client application, I want the MCP server to maintain a persistent connection, so that I don't incur startup overhead on every request.

#### Acceptance Criteria

1. WHEN the server starts THEN the system SHALL enter message loop and wait for requests
2. WHEN a request is processed THEN the server SHALL remain running for next request
3. WHEN stdin closes THEN the server SHALL shutdown gracefully
4. WHEN an error occurs THEN the server SHALL log error and continue running
5. WHEN skills are loaded THEN they SHALL remain in memory between requests

### Requirement 8: Domain Manifest

**User Story:** As a domain owner, I want to define domain metadata in domain.json, so that the server can display domain information and capabilities.

#### Acceptance Criteria

1. WHEN a domain directory has domain.json THEN the system SHALL load domain metadata
2. WHEN domain.json is missing THEN the system SHALL use default metadata
3. WHEN domain metadata is loaded THEN it SHALL include name, version, description, owner
4. WHEN tools/list is called THEN domain information SHALL be available in tool metadata
5. WHEN domain.json is invalid THEN the system SHALL log warning and use defaults

### Requirement 9: Error Handling

**User Story:** As a client developer, I want consistent error responses with codes and context, so that I can handle errors programmatically.

#### Acceptance Criteria

1. WHEN validation fails THEN the error SHALL include code "VALIDATION_ERROR" and field details
2. WHEN a handler fails THEN the error SHALL include code "HANDLER_ERROR" and stack trace
3. WHEN a tool is not found THEN the error SHALL include code "TOOL_NOT_FOUND"
4. WHEN schema is invalid THEN the error SHALL include code "SCHEMA_ERROR"
5. WHEN any error occurs THEN the response SHALL follow MCP error envelope format

### Requirement 10: Testing Infrastructure

**User Story:** As a quality engineer, I want automated tests for the MCP server and handlers, so that I can verify correctness and prevent regressions.

#### Acceptance Criteria

1. WHEN tests run THEN the system SHALL test BaseHandler contract compliance
2. WHEN tests run THEN the system SHALL test schema validation for all skills
3. WHEN tests run THEN the system SHALL test multi-domain skill loading
4. WHEN tests run THEN the system SHALL test MCP protocol methods (initialize, tools/list, tools/call)
5. WHEN tests run THEN the system SHALL test error handling scenarios
