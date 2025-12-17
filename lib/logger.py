#!/usr/bin/env python3
"""
Structured JSON Logger for MCP Server
Logs to stderr only, keeping stdout clean for JSON-RPC responses.
"""

import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional


def log(level: str, message: str, **context: Any) -> None:
    """
    Write structured JSON log to stderr.
    
    Args:
        level: Log level (debug, info, warn, error)
        message: Human-readable log message
        **context: Additional context fields (method, tool_name, error, etc.)
    """
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level.upper(),
        "message": message,
        **context
    }
    
    json_log = json.dumps(log_entry)
    sys.stderr.write(json_log + "\n")
    sys.stderr.flush()


def log_debug(message: str, **context: Any) -> None:
    """Log debug message."""
    log("debug", message, **context)


def log_info(message: str, **context: Any) -> None:
    """Log info message."""
    log("info", message, **context)


def log_warn(message: str, **context: Any) -> None:
    """Log warning message."""
    log("warn", message, **context)


def log_error(message: str, **context: Any) -> None:
    """Log error message."""
    log("error", message, **context)
