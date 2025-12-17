"""
Mock LLM Client (Phase XXI)

Deterministic mock client for testing and development.
"""

from typing import List, Optional
from kuasaturbo.llm.base_client import BaseLLMClient, LLMRequest, LLMResponse


class MockLLMClient(BaseLLMClient):
    """
    Mock LLM client with deterministic outputs
    
    Used for:
    - Testing (deterministic responses)
    - Development (no API costs)
    - Fallback (when real providers fail)
    """
    
    def __init__(self, **kwargs):
        """Initialize mock client"""
        super().__init__(api_key=None, **kwargs)
        self.call_count = 0
    
    def generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate mock completion
        
        Args:
            request: LLM request
        
        Returns:
            Deterministic mock response
        """
        self.call_count += 1
        
        # Deterministic output based on prompt keywords
        content = self._generate_mock_content(request.prompt, request.model)
        
        # Simulate token usage
        input_tokens = len(request.prompt.split())
        output_tokens = len(content.split())
        
        return LLMResponse(
            content=content,
            model=request.model,
            provider="mock",
            usage={
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            },
            metadata={
                "mock": True,
                "call_count": self.call_count,
                "temperature": request.temperature
            }
        )
    
    def _generate_mock_content(self, prompt: str, model: str) -> str:
        """
        Generate deterministic mock content based on prompt
        
        Args:
            prompt: Input prompt
            model: Model identifier
        
        Returns:
            Mock content string
        """
        prompt_lower = prompt.lower()
        
        # Content idea generation
        if "content idea" in prompt_lower or "ideas" in prompt_lower:
            return """1. 10 cara AI boleh automate bisnes SME - jom tengok!
2. Rahsia scale bisnes tanpa tambah staff - AI power!
3. From manual to magic: AI transformation story
4. Boss SME wajib tahu - AI tools yang senang guna
5. Automation hacks untuk bisnes kecil - game changer!"""
        
        # Caption generation
        elif "caption" in prompt_lower or "social media" in prompt_lower:
            return """Hook: Korang rasa AI ni mahal? Think again! 💡

Body: SME owners, listen up! AI automation bukan untuk big corp je. Even with small budget, you can automate repetitive tasks and focus on growing your business. The future is NOW! 🚀

CTA: Drop 'INTERESTED' if nak tahu more!

Hashtags: #AIForSME #AutomationMalaysia #SmartBusiness"""
        
        # Invoice generation
        elif "invoice" in prompt_lower:
            return """INVOICE

Bill To: [Client Name]
Service: [Service Description]
Amount: RM [Amount]
Due Date: [Due Date]

Payment Details:
Bank: [Your Bank]
Account: [Your Account]

Thank you for your business!"""
        
        # Lead intake
        elif "lead" in prompt_lower or "customer" in prompt_lower:
            return """New lead captured successfully. Follow up with personalized consultation.

Suggested reply: Hi [Name]! Thanks for your interest. I'm excited to learn more about your needs. When would be a good time for a quick chat? Looking forward to helping you! 😊"""
        
        # Trade-in evaluation
        elif "trade" in prompt_lower or "vehicle" in prompt_lower or "car" in prompt_lower:
            return """Vehicle details recorded. Based on initial info, this looks like a solid trade-in candidate. Recommend in-person inspection for accurate valuation.

Customer reply: Thanks for the details! Your vehicle looks interesting. Let's schedule an inspection to give you the best trade-in value. When can you come by? 🚗"""
        
        # Loan check
        elif "loan" in prompt_lower or "financing" in prompt_lower:
            return """Based on the information provided, preliminary assessment shows potential eligibility. Monthly income appears sufficient for the requested loan amount. Recommend proceeding with full application and document verification.

Required documents:
- Latest 3 months payslips
- Bank statements (6 months)
- IC copy (front & back)
- Latest EA/BE form"""
        
        # Menu update
        elif "menu" in prompt_lower or "food" in prompt_lower:
            return """Delicious [Item Name] - a perfect blend of flavors that will make your taste buds dance! Freshly prepared with quality ingredients. Available now. 🍽️

NEW on the menu! 🎉 Try our amazing [Item Name] - you won't regret it! Limited time offer. Tag someone who needs to try this! 😋"""
        
        # Attendance
        elif "attendance" in prompt_lower or "employee" in prompt_lower:
            return """Attendance recorded successfully. Employee status updated in local system.

Manager note: Attendance logged for [Employee Name]. All records up to date. 📋"""
        
        # Default response
        else:
            return f"Mock response generated by {model}. This is a simulated completion for testing purposes. Real AI integration is available through OpenAI, Claude, or Gemini providers."
    
    def get_provider_name(self) -> str:
        """Get provider name"""
        return "mock"
    
    def get_supported_models(self) -> List[str]:
        """Get supported models"""
        return ["mock", "mock-fast", "mock-quality"]
    
    def estimate_cost(self, request: LLMRequest, response: Optional[LLMResponse] = None) -> float:
        """
        Estimate cost (mock is always free)
        
        Args:
            request: LLM request
            response: Optional response
        
        Returns:
            Cost in credits (always 0.0 for mock)
        """
        return 0.0
