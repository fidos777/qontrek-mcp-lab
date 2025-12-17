#!/usr/bin/env python3
"""
Governance-Locked MCP Server
Exposes exactly 3 tools with strict validation and shadow logging.
Sprint C-1 Implementation.
"""

import json
import sys
import os
import hashlib
from datetime import datetime
from lib.logger import log
from kuasaturbo.database.connection import get_db_connection

# C-1.1: CANONICAL TOOL SURFACE - EXACTLY 3 TOOLS ALLOWED
TOOLS_ALLOWED = {
    "invoke_workflow",
    "fetch_proof", 
    "export_attestation"
}

# C-1.3: HARD SCHEMA VALIDATION - Strict schemas for each tool
TOOL_SCHEMAS = {
    "invoke_workflow": {
        "type": "object",
        "required": ["workflow_id", "invocation_id", "parameters"],
        "properties": {
            "workflow_id": {
                "type": "string",
                "enum": [
                    "kreator.creative_funnel.v1",
                    "launchkit.branding.v1",
                    "launchkit.prd.v1"
                ]
            },
            "invocation_id": {
                "type": "string",
                "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
            },
            "parameters": {
                "type": "object"
            }
        },
        "additionalProperties": False
    },
    "fetch_proof": {
        "type": "object", 
        "required": ["invocation_id"],
        "properties": {
            "invocation_id": {
                "type": "string",
                "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
            }
        },
        "additionalProperties": False
    },
    "export_attestation": {
        "type": "object",
        "required": ["invocation_id"], 
        "properties": {
            "invocation_id": {
                "type": "string",
                "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"
            }
        },
        "additionalProperties": False
    }
}

def send_message(message):
    """Send JSON-RPC message to stdout."""
    json_str = json.dumps(message)
    sys.stdout.write(json_str + "\n")
    sys.stdout.flush()

def read_message():
    """Read JSON-RPC message from stdin."""
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line.strip())

def log_shadow_entry(request_type, validation_result, reason, request_hash):
    """
    C-1.4: SHADOW LOGGING - Log rejected/malformed requests
    
    HARD RULES:
    - Cannot trigger retries
    - Cannot influence execution  
    - Cannot be queried by MCP tools
    - Logging happens before return
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create shadow log table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mcp_shadow_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                request_type TEXT NOT NULL,
                validation_result TEXT NOT NULL,
                reason TEXT NOT NULL,
                request_hash TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert shadow log entry
        cursor.execute("""
            INSERT INTO mcp_shadow_log 
            (request_type, validation_result, reason, request_hash, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request_type,
            validation_result, 
            reason,
            request_hash,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        
        # Log to stderr for debugging (not stdout to avoid MCP interference)
        print(f"[SHADOW_LOG] {validation_result}: {reason}", file=sys.stderr)
        
    except Exception as e:
        # Shadow logging failure must not affect execution
        print(f"[SHADOW_LOG_ERROR] {str(e)}", file=sys.stderr)

def validate_tool_request(tool_name, arguments):
    """
    C-1.3: HARD SCHEMA VALIDATION
    
    Returns: (is_valid, error_reason)
    """
    # C-1.1: Check if tool is in allowed set
    if tool_name not in TOOLS_ALLOWED:
        return False, f"Tool '{tool_name}' not in allowed set: {TOOLS_ALLOWED}"
    
    # C-1.3: Validate against strict schema
    schema = TOOL_SCHEMAS.get(tool_name)
    if not schema:
        return False, f"No schema defined for tool '{tool_name}'"
    
    # Check required fields
    required = schema.get("required", [])
    for field in required:
        if field not in arguments:
            return False, f"Missing required field: {field}"
    
    # Check additionalProperties = False
    if schema.get("additionalProperties") is False:
        allowed_props = set(schema.get("properties", {}).keys())
        actual_props = set(arguments.keys())
        extra_props = actual_props - allowed_props
        if extra_props:
            return False, f"Extra properties not allowed: {extra_props}"
    
    # Validate specific field constraints
    properties = schema.get("properties", {})
    for field, value in arguments.items():
        if field in properties:
            prop_schema = properties[field]
            
            # Type validation
            expected_type = prop_schema.get("type")
            if expected_type == "string" and not isinstance(value, str):
                return False, f"Field '{field}' must be string, got {type(value).__name__}"
            elif expected_type == "object" and not isinstance(value, dict):
                return False, f"Field '{field}' must be object, got {type(value).__name__}"
            
            # Enum validation
            if "enum" in prop_schema and value not in prop_schema["enum"]:
                return False, f"Field '{field}' must be one of {prop_schema['enum']}, got '{value}'"
            
            # Pattern validation (UUID)
            if "pattern" in prop_schema:
                import re
                if not re.match(prop_schema["pattern"], value):
                    return False, f"Field '{field}' does not match required pattern (UUID format)"
    
    return True, None

def handle_initialize(params):
    """Handle initialize request."""
    # C-1.1: Fail startup if any unauthorized tools exist
    log("info", "MCP Server initializing with governance lockdown")
    log("info", "Allowed tools", tools=list(TOOLS_ALLOWED))
    
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "governance-locked-mcp",
            "version": "1.0.0-c1"
        }
    }

def handle_list_tools(params):
    """
    C-1.2: STATIC TOOL REGISTRATION - No dynamic discovery
    Handle tools/list request with exactly 3 allowed tools.
    """
    tools = []
    
    # C-1.1: Return only the 3 canonical tools
    for tool_name in TOOLS_ALLOWED:
        schema = TOOL_SCHEMAS[tool_name]
        
        descriptions = {
            "invoke_workflow": "Execute a governed workflow with proof generation",
            "fetch_proof": "Retrieve cryptographic proof for a completed invocation", 
            "export_attestation": "Export attestation data for external verification"
        }
        
        tools.append({
            "name": tool_name,
            "description": descriptions[tool_name],
            "inputSchema": schema
        })
    
    log("info", "Listed canonical tools", tool_count=len(tools))
    return {"tools": tools}

def handle_call_tool(params):
    """
    C-1.3: HARD SCHEMA VALIDATION + C-1.4: SHADOW LOGGING
    Handle tools/call request with strict validation and shadow logging.
    """
    tool_name = params.get("name")
    arguments = params.get("arguments", {})
    
    # Generate request hash for shadow logging
    request_data = json.dumps({"tool": tool_name, "args": arguments}, sort_keys=True)
    request_hash = hashlib.sha256(request_data.encode()).hexdigest()[:16]
    
    log("info", "MCP tool call received", 
        tool_name=tool_name, 
        request_hash=request_hash)
    
    # C-1.3: Validate tool request
    is_valid, error_reason = validate_tool_request(tool_name, arguments)
    
    if not is_valid:
        # C-1.4: Log rejection to shadow log
        validation_result = "rejected" if tool_name in TOOLS_ALLOWED else "scope_violation"
        log_shadow_entry(tool_name or "unknown", validation_result, error_reason, request_hash)
        
        log("error", "Tool request rejected", 
            tool_name=tool_name, 
            reason=error_reason,
            request_hash=request_hash)
        
        raise Exception(f"Tool request rejected: {error_reason}")
    
    # C-1.5: MCP WRITE BOUNDARY - Only allowed operations
    try:
        if tool_name == "invoke_workflow":
            result = handle_invoke_workflow(arguments)
        elif tool_name == "fetch_proof":
            result = handle_fetch_proof(arguments)
        elif tool_name == "export_attestation":
            result = handle_export_attestation(arguments)
        else:
            # This should never happen due to validation, but safety check
            raise Exception(f"Tool '{tool_name}' not implemented")
        
        log("info", "Tool execution successful", 
            tool_name=tool_name,
            request_hash=request_hash)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2)
                }
            ]
        }
        
    except Exception as e:
        # C-1.4: Log malformed requests that pass validation but fail execution
        log_shadow_entry(tool_name, "malformed", str(e), request_hash)
        
        log("error", "Tool execution failed", 
            tool_name=tool_name, 
            error=str(e),
            request_hash=request_hash)
        
        raise e

def handle_invoke_workflow(arguments):
    """
    C-1.5: CONTROLLED EXECUTION - Invoke workflow without authority leak
    """
    workflow_id = arguments["workflow_id"]
    invocation_id = arguments["invocation_id"]
    parameters = arguments["parameters"]
    
    # This is a stub - in real implementation, this would:
    # 1. Validate workflow exists and is authorized
    # 2. Execute workflow in sandboxed environment
    # 3. Generate cryptographic proof
    # 4. Return invocation result without exposing internals
    
    return {
        "status": "success",
        "invocation_id": invocation_id,
        "workflow_id": workflow_id,
        "result": "Workflow execution completed",
        "proof_generated": True,
        "message": "This is a governance-locked stub implementation"
    }

def handle_fetch_proof(arguments):
    """
    C-1.5: READ-ONLY PROOF RETRIEVAL - No system mutation
    """
    invocation_id = arguments["invocation_id"]
    
    # This is a stub - in real implementation, this would:
    # 1. Query proof database (read-only)
    # 2. Return cryptographic proof data
    # 3. No system state changes allowed
    
    return {
        "status": "success", 
        "invocation_id": invocation_id,
        "proof": {
            "hash": "0x" + hashlib.sha256(invocation_id.encode()).hexdigest(),
            "timestamp": datetime.now().isoformat(),
            "verified": True
        },
        "message": "This is a governance-locked stub implementation"
    }

def handle_export_attestation(arguments):
    """
    C-1.5: READ-ONLY ATTESTATION EXPORT - No system mutation
    """
    invocation_id = arguments["invocation_id"]
    
    # This is a stub - in real implementation, this would:
    # 1. Query attestation data (read-only)
    # 2. Format for external verification
    # 3. No system state changes allowed
    
    return {
        "status": "success",
        "invocation_id": invocation_id,
        "attestation": {
            "format": "json",
            "data": {
                "invocation_id": invocation_id,
                "exported_at": datetime.now().isoformat(),
                "signature": "0x" + hashlib.sha256(f"attestation_{invocation_id}".encode()).hexdigest()
            }
        },
        "message": "This is a governance-locked stub implementation"
    }

def main():
    """
    C-1: GOVERNANCE-LOCKED MCP SERVER
    Main server loop with strict tool surface and shadow logging.
    """
    log("info", "Starting governance-locked MCP server", 
        allowed_tools=list(TOOLS_ALLOWED),
        tool_count=len(TOOLS_ALLOWED))
    
    # C-1.1: Verify exactly 3 tools are configured
    if len(TOOLS_ALLOWED) != 3:
        log("error", "CRITICAL: Tool surface violation", 
            expected=3, 
            actual=len(TOOLS_ALLOWED))
        sys.exit(1)
    
    # C-1.4: Initialize shadow logging
    try:
        conn = get_db_connection()
        log("info", "Shadow logging initialized")
    except Exception as e:
        log("error", "Failed to initialize shadow logging", error=str(e))
        sys.exit(1)
    
    while True:
        try:
            message = read_message()
            if message is None:
                break
            
            msg_id = message.get("id")
            method = message.get("method")
            params = message.get("params", {})
            
            log("info", "Received MCP request", 
                method=method, 
                msg_id=msg_id)
            
            response = {"jsonrpc": "2.0", "id": msg_id}
            
            try:
                if method == "initialize":
                    response["result"] = handle_initialize(params)
                elif method == "tools/list":
                    response["result"] = handle_list_tools(params)
                elif method == "tools/call":
                    response["result"] = handle_call_tool(params)
                elif method == "notifications/initialized":
                    # No response needed for notifications
                    continue
                else:
                    # C-1.4: Log unknown methods to shadow log
                    request_hash = hashlib.sha256(json.dumps({"method": method, "params": params}, sort_keys=True).encode()).hexdigest()[:16]
                    log_shadow_entry(method or "unknown_method", "rejected", f"Method not found: {method}", request_hash)
                    
                    log("warn", "Method not found", 
                        method=method, 
                        msg_id=msg_id)
                    response["error"] = {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                
                send_message(response)
                
            except Exception as e:
                log("error", "Request processing error", 
                    method=method, 
                    msg_id=msg_id, 
                    error=str(e))
                response["error"] = {
                    "code": -32603,
                    "message": str(e)
                }
                send_message(response)
                
        except Exception as e:
            log("error", "Fatal server error", error=str(e))
            break
    
    log("info", "Shutting down governance-locked MCP server")

if __name__ == "__main__":
    main()
