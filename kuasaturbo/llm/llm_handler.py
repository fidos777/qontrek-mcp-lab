"""
Unified LLM Handler (Phase XXI)

High-level handler with retry logic, error handling, and credit deduction.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from kuasaturbo.llm.base_client import LLMRequest, LLMResponse
from kuasaturbo.llm.provider_registry import get_provider, get_default_provider
from kuasaturbo.llm.mock_client import MockLLMClient
from kuasaturbo.resources.wallets import WalletManager
from kuasaturbo.resources.transactions import TransactionManager, TransactionStatus


class LLMHandler:
    """
    Unified LLM handler with credit management
    
    Features:
    - Provider routing
    - Retry with fallback to mock
    - Credit estimation and deduction
    - Error handling
    - Transaction management
    """
    
    def __init__(self, tenant_id: str, execution_id: str):
        """
        Initialize LLM handler
        
        Args:
            tenant_id: Tenant identifier
            execution_id: Execution identifier
        """
        self.tenant_id = tenant_id
        self.execution_id = execution_id
        self.wallet_manager = WalletManager()
        self.transaction_manager = TransactionManager()
    
    def generate(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate LLM completion with credit management
        
        Args:
            prompt: User prompt
            provider: Optional provider override
            model: Optional model override
            temperature: Temperature (0.0-1.0)
            max_tokens: Maximum output tokens
            system_prompt: Optional system prompt
            metadata: Optional metadata
        
        Returns:
            {
                "content": str,
                "model": str,
                "provider": str,
                "usage": dict,
                "cost": float,
                "transaction_id": str,
                "status": str,
                "error": str (optional)
            }
        """
        print(f"[LLMHandler] Starting generation for tenant {self.tenant_id}")
        
        # Determine provider and model
        provider_name = provider or get_default_provider()
        
        # Get provider client
        provider_client = get_provider(provider_name)
        if not provider_client:
            print(f"[LLMHandler] Provider not found: {provider_name}, falling back to mock")
            provider_client = MockLLMClient()
            provider_name = "mock"
        
        # Determine model
        if not model:
            # Use first supported model from provider
            supported_models = provider_client.get_supported_models()
            model = supported_models[0] if supported_models else "mock"
        
        # Build request
        request = LLMRequest(
            prompt=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            system_prompt=system_prompt,
            metadata=metadata
        )
        
        # Estimate cost
        estimated_cost = provider_client.estimate_cost(request)
        print(f"[LLMHandler] Estimated cost: {estimated_cost:.4f} credits")
        
        # Check sufficient balance
        current_balance = self.wallet_manager.get_balance(self.tenant_id)
        if current_balance < estimated_cost:
            print(f"[LLMHandler] Insufficient balance: {current_balance} < {estimated_cost}")
            return {
                "content": "",
                "model": model,
                "provider": provider_name,
                "usage": {"input_tokens": 0, "output_tokens": 0},
                "cost": 0.0,
                "transaction_id": None,
                "status": "insufficient_credits",
                "error": f"Insufficient credits. Required: {estimated_cost:.2f}, Available: {current_balance:.2f}"
            }
        
        # Create transaction (PENDING)
        transaction_id = self.transaction_manager.create_transaction(
            tenant_id=self.tenant_id,
            execution_id=self.execution_id,
            amount=estimated_cost,
            model_id=model,
            metadata={
                "provider": provider_name,
                "estimated_cost": estimated_cost,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Update to EXECUTING
        self.transaction_manager.update_status(transaction_id, TransactionStatus.EXECUTING)
        
        # Attempt generation
        response = provider_client.generate(request)
        
        # Check for errors
        if response.error:
            print(f"[LLMHandler] Provider error: {response.error}")
            
            # Try fallback to mock
            if provider_name != "mock":
                print("[LLMHandler] Falling back to mock provider")
                mock_client = MockLLMClient()
                response = mock_client.generate(request)
                provider_name = "mock"
                model = response.model
        
        # Calculate actual cost
        actual_cost = provider_client.estimate_cost(request, response)
        print(f"[LLMHandler] Actual cost: {actual_cost:.4f} credits")
        
        # Deduct credits
        deduction_success = self.wallet_manager.safe_decrement(
            self.tenant_id,
            actual_cost,
            transaction_id
        )
        
        if not deduction_success:
            print(f"[LLMHandler] Credit deduction failed")
            self.transaction_manager.update_status(
                transaction_id,
                TransactionStatus.FAILED,
                "Credit deduction failed"
            )
            return {
                "content": "",
                "model": model,
                "provider": provider_name,
                "usage": response.usage,
                "cost": actual_cost,
                "transaction_id": transaction_id,
                "status": "deduction_failed",
                "error": "Failed to deduct credits"
            }
        
        # Mark transaction as COMPLETED
        self.transaction_manager.update_status(transaction_id, TransactionStatus.COMPLETED)
        
        print(f"[LLMHandler] Generation completed successfully")
        
        return {
            "content": response.content,
            "model": response.model,
            "provider": response.provider,
            "usage": response.usage,
            "cost": actual_cost,
            "transaction_id": transaction_id,
            "status": "completed",
            "metadata": response.metadata
        }
    
    def estimate_cost(
        self,
        prompt: str,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 1000
    ) -> Dict[str, Any]:
        """
        Estimate cost without making API call
        
        Args:
            prompt: User prompt
            provider: Optional provider
            model: Optional model
            max_tokens: Maximum output tokens
        
        Returns:
            {
                "estimated_cost": float,
                "provider": str,
                "model": str,
                "current_balance": float,
                "sufficient_credits": bool
            }
        """
        # Determine provider and model
        provider_name = provider or get_default_provider()
        
        provider_client = get_provider(provider_name)
        if not provider_client:
            provider_client = MockLLMClient()
            provider_name = "mock"
        
        if not model:
            supported_models = provider_client.get_supported_models()
            model = supported_models[0] if supported_models else "mock"
        
        # Build request
        request = LLMRequest(
            prompt=prompt,
            model=model,
            max_tokens=max_tokens
        )
        
        # Estimate cost
        estimated_cost = provider_client.estimate_cost(request)
        
        # Check balance
        current_balance = self.wallet_manager.get_balance(self.tenant_id)
        sufficient = current_balance >= estimated_cost
        
        return {
            "estimated_cost": estimated_cost,
            "provider": provider_name,
            "model": model,
            "current_balance": current_balance,
            "sufficient_credits": sufficient
        }


def create_handler(tenant_id: str, execution_id: str) -> LLMHandler:
    """
    Factory function to create LLM handler
    
    Args:
        tenant_id: Tenant identifier
        execution_id: Execution identifier
    
    Returns:
        LLM handler instance
    """
    return LLMHandler(tenant_id, execution_id)
