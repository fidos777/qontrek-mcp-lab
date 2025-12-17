"""
Logging Middleware

FastAPI middleware for request tracking and audit logging.
"""

import time
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from .logger import generate_request_id, get_logger
from .audit import AuditLogger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request tracking and audit logging"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with logging and audit
        
        Args:
            request: FastAPI request
            call_next: Next middleware/endpoint
        
        Returns:
            Response with added headers
        """
        # Generate request ID
        request_id = generate_request_id()
        
        # Add to request state
        request.state.request_id = request_id
        request.state.start_time = time.time()
        
        # Get logger
        logger = get_logger(__name__, request_id=request_id)
        
        # Log request start
        logger.info(f"Request started: {request.method} {request.url.path}")
        
        # Process request
        try:
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = (time.time() - request.state.start_time) * 1000
            
            # Get tenant from request state (set by auth middleware)
            tenant_id = getattr(request.state, 'tenant_id', 'anonymous')
            execution_id = getattr(request.state, 'execution_id', None)
            persona_id = getattr(request.state, 'persona_id', None)
            model_id = getattr(request.state, 'model_id', None)
            
            # Log to audit
            AuditLogger.log_request(
                tenant_id=tenant_id,
                request_id=request_id,
                endpoint=request.url.path,
                method=request.method,
                status_code=response.status_code,
                duration_ms=duration_ms,
                execution_id=execution_id,
                user_agent=request.headers.get('user-agent'),
                ip_address=request.client.host if request.client else None,
                persona_id=persona_id,
                model_id=model_id
            )
            
            # Add request ID to response headers
            response.headers['X-Request-ID'] = request_id
            if execution_id:
                response.headers['X-Execution-ID'] = execution_id
            
            # Log completion
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"[{response.status_code}] ({duration_ms:.2f}ms)"
            )
            
            return response
        
        except Exception as e:
            # Calculate duration
            duration_ms = (time.time() - request.state.start_time) * 1000
            
            # Get tenant from request state
            tenant_id = getattr(request.state, 'tenant_id', 'anonymous')
            
            # Log error to audit
            AuditLogger.log_request(
                tenant_id=tenant_id,
                request_id=request_id,
                endpoint=request.url.path,
                method=request.method,
                status_code=500,
                duration_ms=duration_ms,
                error_message=str(e)
            )
            
            # Log error
            logger.error(f"Request failed: {request.method} {request.url.path} - {str(e)}")
            
            # Re-raise exception
            raise


def add_execution_context(
    request: Request,
    execution_id: str,
    persona_id: Optional[str] = None,
    model_id: Optional[str] = None
):
    """
    Add execution context to request state
    
    Args:
        request: FastAPI request
        execution_id: Execution identifier
        persona_id: Optional persona identifier
        model_id: Optional model identifier
    """
    request.state.execution_id = execution_id
    if persona_id:
        request.state.persona_id = persona_id
    if model_id:
        request.state.model_id = model_id
