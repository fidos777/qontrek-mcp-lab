"""
Gemini LLM Client (Phase XXI)

Google Gemini integration (TERTIARY priority).
"""

import os
import time
from typing import List, Optional
from kuasaturbo.llm.base_client import BaseLLMClient, LLMRequest, LLMResponse
from kuasaturbo.llm.cost_model import calculate_cost


class GeminiClient(BaseLLMClient):
    """
    Gemini LLM client (Google)
    
    Supports:
    - Gemini Pro
    - Gemini 1.5 Pro, Flash
    """
    
    SUPPORTED_MODELS = [
        "gemini-pro",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google API key (or use GOOGLE_API_KEY env var)
            **kwargs: Additional configuration
        """
        super().__init__(api_key=api_key, **kwargs)
        
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        
        if not self.api_key:
            print("[GeminiClient] Warning: No API key provided. Set GOOGLE_API_KEY environment variable.")
        
        self.max_retries = kwargs.get("max_retries", 3)
        self.retry_delay = kwargs.get("retry_delay", 1.0)
        
        self._genai = None
    
    def _get_genai_client(self):
        """Lazy load Google GenAI client"""
        if self._genai is None:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._genai = genai
            except ImportError:
                raise ImportError(
                    "Google GenAI library not installed. Install with: pip install google-generativeai"
                )
        return self._genai
    
    def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate completion from Gemini"""
        if not self.api_key:
            return LLMResponse(
                content="",
                model=request.model,
                provider="gemini",
                usage={"input_tokens": 0, "output_tokens": 0},
                error="No API key provided"
            )
        
        if not self.validate_model(request.model):
            return LLMResponse(
                content="",
                model=request.model,
                provider="gemini",
                usage={"input_tokens": 0, "output_tokens": 0},
                error=f"Unsupported model: {request.model}"
            )
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                print(f"[GeminiClient] Attempt {attempt + 1}/{self.max_retries} for {request.model}")
                
                genai = self._get_genai_client()
                
                # Create model
                model = genai.GenerativeModel(request.model)
                
                # Build prompt
                full_prompt = request.prompt
                if request.system_prompt:
                    full_prompt = f"{request.system_prompt}\n\n{request.prompt}"
                
                # Make API call
                response = model.generate_content(
                    full_prompt,
                    generation_config={
                        "temperature": request.temperature,
                        "max_output_tokens": request.max_tokens
                    }
                )
                
                # Extract response
                content = response.text
                
                # Estimate tokens (Gemini doesn't always provide usage)
                input_tokens = len(full_prompt.split()) * 1.3
                output_tokens = len(content.split()) * 1.3
                
                cost = calculate_cost("gemini", request.model, int(input_tokens), int(output_tokens))
                
                print(f"[GeminiClient] Success: ~{int(input_tokens)} input + ~{int(output_tokens)} output tokens, cost: {cost:.4f} credits")
                
                return LLMResponse(
                    content=content,
                    model=request.model,
                    provider="gemini",
                    usage={
                        "input_tokens": int(input_tokens),
                        "output_tokens": int(output_tokens)
                    },
                    metadata={
                        "cost": cost,
                        "estimated_tokens": True,
                        "attempt": attempt + 1
                    }
                )
            
            except Exception as e:
                last_error = str(e)
                print(f"[GeminiClient] Error on attempt {attempt + 1}: {last_error}")
                
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"[GeminiClient] Retrying in {delay}s...")
                    time.sleep(delay)
        
        print(f"[GeminiClient] All {self.max_retries} attempts failed")
        return LLMResponse(
            content="",
            model=request.model,
            provider="gemini",
            usage={"input_tokens": 0, "output_tokens": 0},
            error=f"Failed after {self.max_retries} attempts: {last_error}"
        )
    
    def get_provider_name(self) -> str:
        """Get provider name"""
        return "gemini"
    
    def get_supported_models(self) -> List[str]:
        """Get supported models"""
        return self.SUPPORTED_MODELS.copy()
    
    def estimate_cost(self, request: LLMRequest, response: Optional[LLMResponse] = None) -> float:
        """Estimate cost"""
        if response and response.usage:
            return calculate_cost(
                "gemini",
                request.model,
                response.usage["input_tokens"],
                response.usage["output_tokens"]
            )
        else:
            estimated_input = len(request.prompt.split()) * 1.3
            estimated_output = request.max_tokens * 0.75
            
            return calculate_cost(
                "gemini",
                request.model,
                int(estimated_input),
                int(estimated_output)
            )
