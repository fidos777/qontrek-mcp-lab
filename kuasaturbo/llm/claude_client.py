"""
Claude LLM Client (Phase XXI)

Anthropic Claude integration (SECONDARY priority).
"""

import os
import time
from typing import List, Optional
from kuasaturbo.llm.base_client import BaseLLMClient, LLMRequest, LLMResponse
from kuasaturbo.llm.cost_model import calculate_cost


class ClaudeClient(BaseLLMClient):
    """
    Claude LLM client (Anthropic)
    
    Supports:
    - Claude 3 Opus, Sonnet, Haiku
    - Claude 3.5 Sonnet
    """
    
    SUPPORTED_MODELS = [
        "claude-3-opus",
        "claude-3-sonnet",
        "claude-3-haiku",
        "claude-3-5-sonnet"
    ]
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Claude client
        
        Args:
            api_key: Anthropic API key (or use ANTHROPIC_API_KEY env var)
            **kwargs: Additional configuration
        """
        super().__init__(api_key=api_key, **kwargs)
        
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            print("[ClaudeClient] Warning: No API key provided. Set ANTHROPIC_API_KEY environment variable.")
        
        self.max_retries = kwargs.get("max_retries", 3)
        self.retry_delay = kwargs.get("retry_delay", 1.0)
        
        self._anthropic = None
    
    def _get_anthropic_client(self):
        """Lazy load Anthropic client"""
        if self._anthropic is None:
            try:
                import anthropic
                self._anthropic = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "Anthropic library not installed. Install with: pip install anthropic"
                )
        return self._anthropic
    
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate completion from Claude"""
        if not self.api_key:
            return LLMResponse(
                content="",
                model=request.model,
                provider="claude",
                usage={"input_tokens": 0, "output_tokens": 0},
                error="No API key provided"
            )
        
        if not self.validate_model(request.model):
            return LLMResponse(
                content="",
                model=request.model,
                provider="claude",
                usage={"input_tokens": 0, "output_tokens": 0},
                error=f"Unsupported model: {request.model}"
            )
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                print(f"[ClaudeClient] Attempt {attempt + 1}/{self.max_retries} for {request.model}")
                
                client = self._get_anthropic_client()
                
                # Build messages
                messages = [{"role": "user", "content": request.prompt}]
                
                # Make API call
                response = client.messages.create(
                    model=request.model,
                    max_tokens=request.max_tokens,
                    temperature=request.temperature,
                    system=request.system_prompt or "",
                    messages=messages
                )
                
                # Extract response
                content = response.content[0].text
                input_tokens = response.usage.input_tokens
                output_tokens = response.usage.output_tokens
                
                cost = calculate_cost("claude", request.model, input_tokens, output_tokens)
                
                print(f"[ClaudeClient] Success: {input_tokens} input + {output_tokens} output tokens, cost: {cost:.4f} credits")
                
                return LLMResponse(
                    content=content,
                    model=request.model,
                    provider="claude",
                    usage={
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens
                    },
                    metadata={
                        "cost": cost,
                        "stop_reason": response.stop_reason,
                        "attempt": attempt + 1
                    }
                )
            
            except Exception as e:
                last_error = str(e)
                print(f"[ClaudeClient] Error on attempt {attempt + 1}: {last_error}")
                
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"[ClaudeClient] Retrying in {delay}s...")
                    time.sleep(delay)
        
        print(f"[ClaudeClient] All {self.max_retries} attempts failed")
        return LLMResponse(
            content="",
            model=request.model,
            provider="claude",
            usage={"input_tokens": 0, "output_tokens": 0},
            error=f"Failed after {self.max_retries} attempts: {last_error}"
        )
    
    def get_provider_name(self) -> str:
        """Get provider name"""
        return "claude"
    
    def get_supported_models(self) -> List[str]:
        """Get supported models"""
        return self.SUPPORTED_MODELS.copy()
    
    def estimate_cost(self, request: LLMRequest, response: Optional[LLMResponse] = None) -> float:
        """Estimate cost"""
        if response and response.usage:
            return calculate_cost(
                "claude",
                request.model,
                response.usage["input_tokens"],
                response.usage["output_tokens"]
            )
        else:
            estimated_input = len(request.prompt.split()) * 1.3
            estimated_output = request.max_tokens * 0.75
            
            return calculate_cost(
                "claude",
                request.model,
                int(estimated_input),
                int(estimated_output)
            )
