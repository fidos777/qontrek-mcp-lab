"""
Provider Registry (Phase XXI)

Central registry for all LLM providers with dynamic loading.
"""

from typing import Dict, Optional, List
from kuasaturbo.llm.base_client import BaseLLMClient


class ProviderRegistry:
    """
    Central registry for LLM providers
    
    Manages provider instances and routing logic.
    """
    
    def __init__(self):
        """Initialize empty registry"""
        self._providers: Dict[str, BaseLLMClient] = {}
        self._default_provider = "mock"
    
    def register(self, provider_name: str, client: BaseLLMClient):
        """
        Register a provider
        
        Args:
            provider_name: Provider identifier
            client: Provider client instance
        """
        self._providers[provider_name] = client
        print(f"[ProviderRegistry] Registered provider: {provider_name}")
    
    def get(self, provider_name: str) -> Optional[BaseLLMClient]:
        """
        Get provider by name
        
        Args:
            provider_name: Provider identifier
        
        Returns:
            Provider client or None
        """
        return self._providers.get(provider_name)
    
    def list_providers(self) -> List[str]:
        """
        Get list of registered providers
        
        Returns:
            List of provider names
        """
        return list(self._providers.keys())
    
    def set_default(self, provider_name: str):
        """
        Set default provider
        
        Args:
            provider_name: Provider identifier
        """
        if provider_name not in self._providers:
            raise ValueError(f"Provider not registered: {provider_name}")
        
        self._default_provider = provider_name
        print(f"[ProviderRegistry] Default provider set to: {provider_name}")
    
    def get_default(self) -> str:
        """
        Get default provider name
        
        Returns:
            Default provider identifier
        """
        return self._default_provider
    
    def get_default_client(self) -> Optional[BaseLLMClient]:
        """
        Get default provider client
        
        Returns:
            Default provider client
        """
        return self.get(self._default_provider)


# Global registry instance
_global_registry: Optional[ProviderRegistry] = None


def get_registry() -> ProviderRegistry:
    """
    Get global provider registry (singleton)
    
    Returns:
        Global registry instance
    """
    global _global_registry
    
    if _global_registry is None:
        _global_registry = ProviderRegistry()
        _initialize_default_providers()
    
    return _global_registry


def _initialize_default_providers():
    """Initialize default providers in registry"""
    from kuasaturbo.llm.mock_client import MockLLMClient
    from kuasaturbo.llm.openai_client import OpenAIClient
    from kuasaturbo.llm.claude_client import ClaudeClient
    from kuasaturbo.llm.gemini_client import GeminiClient
    
    registry = _global_registry
    
    # Always register mock (no API key needed)
    registry.register("mock", MockLLMClient())
    
    # Register OpenAI (PRIMARY)
    try:
        openai_client = OpenAIClient()
        registry.register("openai", openai_client)
        print("[ProviderRegistry] OpenAI provider initialized")
    except Exception as e:
        print(f"[ProviderRegistry] Warning: Failed to initialize OpenAI: {e}")
    
    # Register Claude (SECONDARY)
    try:
        claude_client = ClaudeClient()
        registry.register("claude", claude_client)
        print("[ProviderRegistry] Claude provider initialized")
    except Exception as e:
        print(f"[ProviderRegistry] Warning: Failed to initialize Claude: {e}")
    
    # Register Gemini (TERTIARY)
    try:
        gemini_client = GeminiClient()
        registry.register("gemini", gemini_client)
        print("[ProviderRegistry] Gemini provider initialized")
    except Exception as e:
        print(f"[ProviderRegistry] Warning: Failed to initialize Gemini: {e}")
    
    # Set mock as default (safe fallback)
    registry.set_default("mock")


def get_provider(provider_name: str) -> Optional[BaseLLMClient]:
    """
    Get provider by name
    
    Args:
        provider_name: Provider identifier
    
    Returns:
        Provider client or None
    """
    registry = get_registry()
    return registry.get(provider_name)


def register_provider(provider_name: str, client: BaseLLMClient):
    """
    Register a provider
    
    Args:
        provider_name: Provider identifier
        client: Provider client instance
    """
    registry = get_registry()
    registry.register(provider_name, client)


def list_providers() -> List[str]:
    """
    Get list of registered providers
    
    Returns:
        List of provider names
    """
    registry = get_registry()
    return registry.list_providers()


def get_default_provider() -> str:
    """
    Get default provider name
    
    Returns:
        Default provider identifier
    """
    registry = get_registry()
    return registry.get_default()


def set_default_provider(provider_name: str):
    """
    Set default provider
    
    Args:
        provider_name: Provider identifier
    """
    registry = get_registry()
    registry.set_default(provider_name)
