"""
OpenAI LLM Client (Phase XXI)

Production-ready OpenAI integration with error handling and retry logic.
"""

import os
import time
from typing import List, Optional
from kuasaturbo.llm.base_client import BaseLLMClient, LLMRequest, LLMResponse
from kuasaturbo.llm.cost_model import calculate_cost


class OpenAIClient(BaseLLMClient):
    """
    OpenAI LLM client
    
    Supports:
    - GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
    - GPT-4o, GPT-4o Mini
    - Automatic retry with exponential backoff
    - Cost tracking
    """
    
    SUPPORTED_MODELS = [
        "gpt-4",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
        "gpt-4o",
        "gpt-4o-mini"
    ]
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize OpenAI client
        
        Args:
            api_key: OpenAI API key (or use OPENAI_API_KEY env var)
            **kwargs: Additional configuration
        """
        super().__init__(api_key=api_key, **kwargs)
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("[OpenAIClient] Warning: No API key provided. Set OPENAI_API_KEY environment variable.")
        
        # Retry configuration
        self.max_retries = kwargs.get("max_retries", 3)
        self.retry_delay = kwargs.get("retry_delay", 1.0)
        
        # Import OpenAI library (lazy import)
        self._openai = None
    
    def _get_openai_client(self):
        """
        Lazy load OpenAI client
        
        Returns:
            OpenAI client instance
        """
        if self._openai is None:
            try:
                import openai
                self._openai = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "OpenAI library not installed. Install with: pip install openai"
                )
        return self._openai
    
    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate completion from OpenAI
        
        Args:
            request: LLM request
        
        Returns:
            LLM response
        """
        if not self.api_key:
            return LLMResponse(
                content="",
                model=request.model,
                provider="openai",
                usage={"input_tokens": 0, "output_tokens": 0},
                error="No API key provided"
            )
        
        # Validate model
        if not self.validate_model(request.model):
            return LLMResponse(
                content="",
                model=request.model,
                provider="openai",
                usage={"input_tokens": 0, "output_tokens": 0},
                error=f"Unsupported model: {request.model}"
            )
        
        # Retry loop
        last_error = None
        for attempt in range(self.max_retries):
            try:
                print(f"[OpenAIClient] Attempt {attempt + 1}/{self.max_retries} for {request.model}")
                
                # Get OpenAI client
                client = self._get_openai_client()
                
                # Build messages
                messages = []
                if request.system_prompt:
                    messages.append({"role": "system", "content": request.system_prompt})
                messages.append({"role": "user", "content": request.prompt})
                
                # Make API call
                response = client.chat.completions.create(
                    model=request.model,
                    messages=messages,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                )
                
                # Extract response
                content = response.choices[0].message.content
                usage = response.usage
                
                # Calculate cost
                input_tokens = usage.prompt_tokens
                output_tokens = usage.completion_tokens
                cost = calculate_cost("openai", request.model, input_tokens, output_tokens)
                
                print(f"[OpenAIClient] Success: {input_tokens} input + {output_tokens} output tokens, cost: {cost:.4f} credits")
                
                return LLMResponse(
                    content=content,
                    model=request.model,
                    provider="openai",
                    usage={
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens
                    },
                    metadata={
                        "cost": cost,
                        "finish_reason": response.choices[0].finish_reason,
                        "attempt": attempt + 1
                    }
                )
            
            except Exception as e:
                last_error = str(e)
                print(f"[OpenAIClient] Error on attempt {attempt + 1}: {last_error}")
                
                # Exponential backoff
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"[OpenAIClient] Retrying in {delay}s...")
                    time.sleep(delay)
        
        # All retries failed
        print(f"[OpenAIClient] All {self.max_retries} attempts failed")
        return LLMResponse(
            content="",
            model=request.model,
            provider="openai",
            usage={"input_tokens": 0, "output_tokens": 0},
            error=f"Failed after {self.max_retries} attempts: {last_error}"
        )
    
    def get_provider_name(self) -> str:
        """Get provider name"""
        return "openai"
    
    def get_supported_models(self) -> List[str]:
        """Get supported models"""
        return self.SUPPORTED_MODELS.copy()
    
    def estimate_cost(self, request: LLMRequest, response: Optional[LLMResponse] = None) -> float:
        """
        Estimate cost
        
        Args:
            request: LLM request
            response: Optional actual response
        
        Returns:
            Cost in credits
        """
        if response and response.usage:
            # Use actual usage
            return calculate_cost(
                "openai",
                request.model,
                response.usage["input_tokens"],
                response.usage["output_tokens"]
            )
        else:
            # Estimate based on prompt length
            estimated_input = len(request.prompt.split()) * 1.3  # ~1.3 tokens per word
            estimated_output = request.max_tokens * 0.75  # Assume 75% of max
            
            return calculate_cost(
                "openai",
                request.model,
                int(estimated_input),
                int(estimated_output)
            )
