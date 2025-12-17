"""
LLM Provider Layer (Phase XXI)

Unified interface for multiple LLM providers with cost tracking and error handling.
"""

from .base_client import BaseLLMClient, LLMRequest, LLMResponse
from .mock_client import MockLLMClient
from .openai_client import OpenAIClient
from .claude_client import ClaudeClient
from .gemini_client import GeminiClient
from .provider_registry import (
    ProviderRegistry,
    get_provider,
    register_provider,
    list_providers,
    get_default_provider,
    set_default_provider
)
from .llm_handler import LLMHandler, create_handler
from .cost_model import (
    calculate_cost,
    estimate_cost,
    get_model_cost,
    list_providers as list_cost_providers,
    list_models_for_provider
)

__all__ = [
    # Base classes
    'BaseLLMClient',
    'LLMRequest',
    'LLMResponse',
    
    # Provider clients
    'MockLLMClient',
    'OpenAIClient',
    'ClaudeClient',
    'GeminiClient',
    
    # Registry
    'ProviderRegistry',
    'get_provider',
    'register_provider',
    'list_providers',
    'get_default_provider',
    'set_default_provider',
    
    # Handler
    'LLMHandler',
    'create_handler',
    
    # Cost model
    'calculate_cost',
    'estimate_cost',
    'get_model_cost',
    'list_cost_providers',
    'list_models_for_provider'
]
