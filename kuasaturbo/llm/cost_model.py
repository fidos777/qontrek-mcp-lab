"""
LLM Cost Model (Phase XXI)

Pricing per provider/model/token for credit calculation.
"""

from typing import Dict, Optional


# Cost model: credits per 1K tokens
# Format: "provider:model" -> {"input": X, "output": Y}
COST_MODEL: Dict[str, Dict[str, float]] = {
    # OpenAI Models
    "openai:gpt-4": {
        "input": 30.0,   # 30 credits per 1K input tokens
        "output": 60.0   # 60 credits per 1K output tokens
    },
    "openai:gpt-4-turbo": {
        "input": 10.0,
        "output": 30.0
    },
    "openai:gpt-3.5-turbo": {
        "input": 0.5,
        "output": 1.5
    },
    "openai:gpt-4o": {
        "input": 5.0,
        "output": 15.0
    },
    "openai:gpt-4o-mini": {
        "input": 0.15,
        "output": 0.6
    },
    
    # Claude Models
    "claude:claude-3-opus": {
        "input": 15.0,
        "output": 75.0
    },
    "claude:claude-3-sonnet": {
        "input": 3.0,
        "output": 15.0
    },
    "claude:claude-3-haiku": {
        "input": 0.25,
        "output": 1.25
    },
    "claude:claude-3-5-sonnet": {
        "input": 3.0,
        "output": 15.0
    },
    
    # Gemini Models
    "gemini:gemini-pro": {
        "input": 0.5,
        "output": 1.5
    },
    "gemini:gemini-1.5-pro": {
        "input": 3.5,
        "output": 10.5
    },
    "gemini:gemini-1.5-flash": {
        "input": 0.35,
        "output": 1.05
    },
    
    # Mock (free)
    "mock:mock": {
        "input": 0.0,
        "output": 0.0
    },
    "mock:mock-fast": {
        "input": 0.0,
        "output": 0.0
    },
    "mock:mock-quality": {
        "input": 0.0,
        "output": 0.0
    }
}


def get_model_cost(provider: str, model: str) -> Optional[Dict[str, float]]:
    """
    Get cost configuration for provider:model
    
    Args:
        provider: Provider name (e.g., "openai")
        model: Model name (e.g., "gpt-4")
    
    Returns:
        Cost dict with "input" and "output" rates, or None if not found
    """
    key = f"{provider}:{model}"
    return COST_MODEL.get(key)


def calculate_cost(
    provider: str,
    model: str,
    input_tokens: int,
    output_tokens: int
) -> float:
    """
    Calculate total cost in credits
    
    Args:
        provider: Provider name
        model: Model name
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
    
    Returns:
        Total cost in credits
    """
    cost_config = get_model_cost(provider, model)
    
    if not cost_config:
        print(f"[CostModel] Warning: No cost config for {provider}:{model}, using default")
        # Default fallback: 1 credit per 1K tokens
        cost_config = {"input": 1.0, "output": 1.0}
    
    # Calculate cost per 1K tokens
    input_cost = (input_tokens / 1000.0) * cost_config["input"]
    output_cost = (output_tokens / 1000.0) * cost_config["output"]
    
    total_cost = input_cost + output_cost
    
    print(f"[CostModel] {provider}:{model} - Input: {input_tokens} tokens (${input_cost:.4f}), Output: {output_tokens} tokens (${output_cost:.4f}), Total: ${total_cost:.4f}")
    
    return total_cost


def estimate_cost(
    provider: str,
    model: str,
    estimated_input_tokens: int,
    estimated_output_tokens: int
) -> float:
    """
    Estimate cost before making API call
    
    Args:
        provider: Provider name
        model: Model name
        estimated_input_tokens: Estimated input tokens
        estimated_output_tokens: Estimated output tokens
    
    Returns:
        Estimated cost in credits
    """
    return calculate_cost(provider, model, estimated_input_tokens, estimated_output_tokens)


def get_all_models() -> Dict[str, Dict[str, float]]:
    """
    Get all available models with pricing
    
    Returns:
        Complete cost model dictionary
    """
    return COST_MODEL.copy()


def list_providers() -> list:
    """
    Get list of all providers
    
    Returns:
        List of provider names
    """
    providers = set()
    for key in COST_MODEL.keys():
        provider = key.split(":")[0]
        providers.add(provider)
    return sorted(list(providers))


def list_models_for_provider(provider: str) -> list:
    """
    Get list of models for a specific provider
    
    Args:
        provider: Provider name
    
    Returns:
        List of model names
    """
    models = []
    for key in COST_MODEL.keys():
        if key.startswith(f"{provider}:"):
            model = key.split(":")[1]
            models.append(model)
    return models
