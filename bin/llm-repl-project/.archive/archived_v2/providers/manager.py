"""LLM Manager - Central manager for all LLM interactions."""

import asyncio
import time
import uuid
from typing import Any, Dict, List, Optional

from .base import LLMProvider, LLMResponse, TokenCounts, BaseLLMProvider
from .ollama import OllamaProvider
from .groq import GroqProvider


class LLMManager:
    """
    Central manager for all LLM interactions. 
    Source of truth for token counts and request lifecycle.
    """
    
    def __init__(self, provider: LLMProvider, model: str, base_url: Optional[str] = None):
        self.provider = provider
        self.model = model
        self.base_url = base_url
        
        # Initialize the appropriate provider
        self._provider_instance = self._create_provider()
        
        # Global token tracking
        self.session_tokens = TokenCounts()
        self.request_history: List[LLMResponse] = []
        
        # Request management
        self.active_requests: Dict[str, asyncio.Task] = {}
        
    def _create_provider(self) -> BaseLLMProvider:
        """Create the appropriate provider instance."""
        if self.provider == LLMProvider.OLLAMA:
            return OllamaProvider(self.model, self.base_url)
        elif self.provider == LLMProvider.GROQ:
            return GroqProvider(self.model, self.base_url)
        else:
            raise NotImplementedError(f"Provider {self.provider} not implemented yet")
    
    async def make_request(self, 
                          prompt: str, 
                          options: Dict[str, Any] = None,
                          request_id: Optional[str] = None) -> LLMResponse:
        """
        Make a tracked LLM request with full lifecycle management.
        This is the ONLY way LLM requests should be made.
        """
        request_id = request_id or str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Make the request through the provider
            response = await self._provider_instance.make_request(prompt, options)
            
            # Update global token tracking
            self.session_tokens.input_tokens += response.tokens.input_tokens
            self.session_tokens.output_tokens += response.tokens.output_tokens
            
            # Store in history
            self.request_history.append(response)
            
            return response
            
        except Exception as e:
            # Return error response with zero tokens
            duration = time.time() - start_time
            error_response = LLMResponse(
                content=f"Error: {str(e)}",
                tokens=TokenCounts(0, 0),
                duration_seconds=duration,
                provider=self.provider,
                model=self.model,
                metadata={"error": True, "exception": str(e)}
            )
            self.request_history.append(error_response)
            return error_response
        finally:
            # Clean up active request tracking
            if request_id in self.active_requests:
                del self.active_requests[request_id]
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get comprehensive session summary."""
        return {
            "total_requests": len(self.request_history),
            "total_tokens": self.session_tokens,
            "total_cost_estimate": self._estimate_cost(),
            "average_duration": sum(r.duration_seconds for r in self.request_history) / len(self.request_history) if self.request_history else 0,
            "provider": self.provider.value,
            "model": self.model
        }
    
    def _estimate_cost(self) -> float:
        """Estimate cost based on provider and token usage."""
        # Simplified cost estimation - could be expanded with actual provider rates
        cost_per_1k_tokens = {
            LLMProvider.GROQ: 0.0002,  # Example rate
            LLMProvider.OLLAMA: 0.0,   # Local, no cost
            LLMProvider.OPENAI: 0.002, # Example rate
            LLMProvider.ANTHROPIC: 0.003, # Example rate
        }
        
        rate = cost_per_1k_tokens.get(self.provider, 0.0)
        total_tokens = self.session_tokens.total_tokens
        return (total_tokens / 1000) * rate