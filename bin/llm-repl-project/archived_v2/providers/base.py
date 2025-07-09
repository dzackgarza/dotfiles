"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional
import time


class LLMProvider(Enum):
    """Supported LLM providers."""
    OLLAMA = "ollama"
    GEMINI = "gemini" 
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"


@dataclass
class TokenCounts:
    """Token usage statistics."""
    input_tokens: int = 0
    output_tokens: int = 0
    
    @property
    def total_tokens(self) -> int:
        """Total tokens used."""
        return self.input_tokens + self.output_tokens


@dataclass
class LLMResponse:
    """Standard response from any LLM provider."""
    content: str
    tokens: TokenCounts
    duration_seconds: float
    provider: LLMProvider
    model: str
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, model: str, base_url: Optional[str] = None):
        self.model = model
        self.base_url = base_url
        self.provider = self._get_provider()
    
    @abstractmethod
    def _get_provider(self) -> LLMProvider:
        """Return the provider enum value."""
        pass
    
    @abstractmethod
    async def make_request(self, prompt: str, options: Dict[str, Any] = None) -> LLMResponse:
        """Make a request to the LLM provider."""
        pass
    
    def _create_response(self, content: str, input_tokens: int, output_tokens: int, 
                        duration: float, metadata: Dict[str, Any] = None) -> LLMResponse:
        """Helper to create a standard response."""
        return LLMResponse(
            content=content.strip(),
            tokens=TokenCounts(input_tokens=input_tokens, output_tokens=output_tokens),
            duration_seconds=duration,
            provider=self.provider,
            model=self.model,
            metadata=metadata or {}
        )