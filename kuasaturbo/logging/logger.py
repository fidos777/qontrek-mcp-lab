"""
Tenant-Aware Logger with Rotating Logs

Provides structured logging with request tracking and tenant isolation.
"""

import logging
import uuid
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


# Log directory
LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def generate_request_id() -> str:
    """
    Generate unique request ID
    
    Format: req_<timestamp>_<uuid>
    Example: req_20251208_a1b2c3d4
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    short_uuid = str(uuid.uuid4())[:8]
    return f"req_{timestamp}_{short_uuid}"


def generate_execution_id() -> str:
    """
    Generate unique execution ID
    
    Format: exec_<timestamp>_<uuid>
    Example: exec_20251208_e5f6g7h8
    """
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    short_uuid = str(uuid.uuid4())[:8]
    return f"exec_{timestamp}_{short_uuid}"


class TenantAwareFormatter(logging.Formatter):
    """Custom formatter that includes tenant context"""
    
    def format(self, record):
        # Add tenant context if available
        if not hasattr(record, 'tenant_id'):
            record.tenant_id = 'system'
        if not hasattr(record, 'request_id'):
            record.request_id = 'none'
        if not hasattr(record, 'execution_id'):
            record.execution_id = 'none'
        
        return super().format(record)


def get_logger(
    name: str,
    tenant_id: Optional[str] = None,
    request_id: Optional[str] = None,
    execution_id: Optional[str] = None
) -> logging.Logger:
    """
    Get or create a tenant-aware logger
    
    Args:
        name: Logger name (usually module name)
        tenant_id: Optional tenant identifier
        request_id: Optional request identifier
        execution_id: Optional execution identifier
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler with rotation
        log_file = LOG_DIR / "kuasaturbo.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        
        # Formatter with tenant context
        formatter = TenantAwareFormatter(
            fmt='%(asctime)s [%(levelname)s] [%(tenant_id)s] [%(request_id)s] [%(execution_id)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    # Create adapter with context
    adapter = logging.LoggerAdapter(logger, {
        'tenant_id': tenant_id or 'system',
        'request_id': request_id or 'none',
        'execution_id': execution_id or 'none'
    })
    
    return adapter


def log_with_context(
    logger: logging.Logger,
    level: str,
    message: str,
    tenant_id: Optional[str] = None,
    request_id: Optional[str] = None,
    execution_id: Optional[str] = None,
    **kwargs
):
    """
    Log message with context
    
    Args:
        logger: Logger instance
        level: Log level (info, warning, error, debug)
        message: Log message
        tenant_id: Optional tenant identifier
        request_id: Optional request identifier
        execution_id: Optional execution identifier
        **kwargs: Additional context
    """
    extra = {
        'tenant_id': tenant_id or 'system',
        'request_id': request_id or 'none',
        'execution_id': execution_id or 'none'
    }
    extra.update(kwargs)
    
    log_func = getattr(logger, level.lower())
    log_func(message, extra=extra)
