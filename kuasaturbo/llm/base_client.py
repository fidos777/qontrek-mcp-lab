"""
Base LLM Client (Phase XXI)

Abstract base class for all LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class LLMResponse:
    """Standardized LLM response"""
    content: str
    model: str
    provider: str
    usage: Dict[str, int]  # {"input_tokens": X, "output_tokens": Y}
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class LLMRequest:
    """Standardized LLM request"""
    prompt: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM providers
    
    All providers must implement:
    - generate(): Main generation method
    - get_provider_name(): Provider identifier
    - get_supported_models(): List of models
    - estimate_cost(): Cost calculation
    """
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize LLM client
        
        Args:
            api_key: Optional API key for provider
            **kwargs: Provider-specific configuration
        """
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate completion from LLM
        
        Args:
            request: LLM request object
        
        Returns:
            LLM response object
        """
        pass
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """
        Get provider identifier
        
        Returns:
            Provider name (e.g., "openai", "claude", "gemini")
        """
        pass
    
    @abstractmethod
    def get_supported_models(self) -> List[str]:
        """
        Get list of supported models
        
        Returns:
            List of model identifiers
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, request: LLMRequest, response: Optional[LLMResponse] = None) -> float:
        """
        Estimate cost in credits
        
        Args:
            request: LLM request
            response: Optional LLM response (for actual usage)
        
        Returns:
            Estimated cost in credits
        """
        pass
    
    def validate_model(self, model: str) -> bool:
        """
        Check if model is supported
        
        Args:
            model: Model identifier
        
        Returns:
            True if supported
        """
        return model in self.get_supported_models()
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} provider={self.get_provider_name()}>"
