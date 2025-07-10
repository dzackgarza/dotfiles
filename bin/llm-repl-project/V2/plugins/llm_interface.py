"""LLM interface for cognitive modules with token tracking and streaming support."""

import asyncio
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, AsyncIterator, Callable, Union
from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"
    GROQ = "groq"
    MOCK = "mock"


@dataclass
class TokenUsage:
    """Token usage tracking."""
    input_tokens: int = 0
    output_tokens: int = 0
    thoughts_tokens: int = 0  # For models with thinking
    
    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens + self.thoughts_tokens


@dataclass
class LLMRequest:
    """Request to an LLM."""
    messages: List[Dict[str, str]]
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    system_prompt: Optional[str] = None
    tools: Optional[List[Dict[str, Any]]] = None
    
    # Metadata
    request_id: str = ""
    cognitive_module: str = ""
    task_description: str = ""


class LLMStreamChunk(BaseModel):
    """A chunk of streamed LLM response."""
    content: str = ""
    thoughts: str = ""  # For models with thinking
    is_complete: bool = False
    chunk_index: int = 0
    timestamp: datetime = Field(default_factory=datetime.now)


@dataclass
class LLMResponse:
    """Response from an LLM."""
    content: str
    thoughts: str = ""  # For models with thinking
    tokens: TokenUsage = None
    duration_seconds: float = 0.0
    model: str = ""
    request_id: str = ""
    timestamp: datetime = None
    
    # Metadata for transparency
    cognitive_module: str = ""
    task_description: str = ""
    
    def __post_init__(self):
        if self.tokens is None:
            self.tokens = TokenUsage()
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "content": self.content,
            "thoughts": self.thoughts,
            "tokens": {
                "input": self.tokens.input_tokens,
                "output": self.tokens.output_tokens,
                "thoughts": self.tokens.thoughts_tokens,
                "total": self.tokens.total_tokens
            },
            "duration_seconds": self.duration_seconds,
            "model": self.model,
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat(),
            "cognitive_module": self.cognitive_module,
            "task_description": self.task_description
        }


class LLMInterface(ABC):
    """Abstract interface for LLM providers."""
    
    def __init__(self, provider: LLMProvider, config: Dict[str, Any] = None):
        self.provider = provider
        self.config = config or {}
        self.total_tokens = TokenUsage()
        self.request_count = 0
        
    @abstractmethod
    async def make_request(self, request: LLMRequest) -> LLMResponse:
        """Make a request to the LLM."""
        pass
    
    @abstractmethod
    async def stream_request(self, request: LLMRequest) -> AsyncIterator[LLMStreamChunk]:
        """Stream a request to the LLM."""
        pass
    
    def get_total_usage(self) -> TokenUsage:
        """Get total token usage across all requests."""
        return self.total_tokens
    
    def get_request_count(self) -> int:
        """Get total number of requests made."""
        return self.request_count


class MockLLMInterface(LLMInterface):
    """Mock LLM interface for testing."""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(LLMProvider.MOCK, config)
        self.response_delay = config.get("response_delay", 0.1) if config else 0.1
        self.simulate_thinking = config.get("simulate_thinking", False) if config else False
    
    async def make_request(self, request: LLMRequest) -> LLMResponse:
        """Make a mock request."""
        await asyncio.sleep(self.response_delay)
        
        start_time = time.time()
        self.request_count += 1
        
        # Simulate processing
        input_tokens = sum(len(msg["content"].split()) for msg in request.messages)
        output_tokens = 50  # Mock output length
        thoughts_tokens = 30 if self.simulate_thinking else 0
        
        tokens = TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            thoughts_tokens=thoughts_tokens
        )
        
        # Update total
        self.total_tokens.input_tokens += tokens.input_tokens
        self.total_tokens.output_tokens += tokens.output_tokens
        self.total_tokens.thoughts_tokens += tokens.thoughts_tokens
        
        content = f"Mock response to: {request.messages[-1]['content'][:50]}..."
        thoughts = "Mock thinking process..." if self.simulate_thinking else ""
        
        return LLMResponse(
            content=content,
            thoughts=thoughts,
            tokens=tokens,
            duration_seconds=time.time() - start_time,
            model="mock-model",
            request_id=request.request_id,
            cognitive_module=request.cognitive_module,
            task_description=request.task_description
        )
    
    async def stream_request(self, request: LLMRequest) -> AsyncIterator[LLMStreamChunk]:
        """Stream a mock request."""
        await asyncio.sleep(self.response_delay)
        
        content = f"Mock response to: {request.messages[-1]['content'][:50]}..."
        thoughts = "Mock thinking process..." if self.simulate_thinking else ""
        
        # Simulate streaming by yielding chunks
        for i, char in enumerate(content):
            if i > 0 and i % 10 == 0:  # Yield every 10 characters
                await asyncio.sleep(0.01)  # Small delay to simulate streaming
            
            yield LLMStreamChunk(
                content=char,
                thoughts=thoughts if i == 0 else "",
                chunk_index=i,
                is_complete=i == len(content) - 1
            )
        
        # Update token counts
        input_tokens = sum(len(msg["content"].split()) for msg in request.messages)
        output_tokens = len(content.split())
        thoughts_tokens = len(thoughts.split()) if thoughts else 0
        
        self.total_tokens.input_tokens += input_tokens
        self.total_tokens.output_tokens += output_tokens
        self.total_tokens.thoughts_tokens += thoughts_tokens
        self.request_count += 1


class LLMManager:
    """Manages LLM interfaces and provides unified access."""
    
    def __init__(self):
        self.interfaces: Dict[str, LLMInterface] = {}
        self.default_interface: Optional[str] = None
        self.request_history: List[LLMResponse] = []
    
    def register_interface(self, name: str, interface: LLMInterface, is_default: bool = False):
        """Register an LLM interface."""
        self.interfaces[name] = interface
        if is_default or self.default_interface is None:
            self.default_interface = name
    
    def get_interface(self, name: Optional[str] = None) -> Optional[LLMInterface]:
        """Get an LLM interface by name."""
        if name is None:
            name = self.default_interface
        return self.interfaces.get(name)
    
    async def make_request(self, request: LLMRequest, interface_name: Optional[str] = None) -> LLMResponse:
        """Make a request using the specified interface."""
        interface = self.get_interface(interface_name)
        if not interface:
            raise ValueError(f"Unknown LLM interface: {interface_name}")
        
        response = await interface.make_request(request)
        self.request_history.append(response)
        return response
    
    async def stream_request(self, request: LLMRequest, interface_name: Optional[str] = None) -> AsyncIterator[LLMStreamChunk]:
        """Stream a request using the specified interface."""
        interface = self.get_interface(interface_name)
        if not interface:
            raise ValueError(f"Unknown LLM interface: {interface_name}")
        
        async for chunk in interface.stream_request(request):
            yield chunk
    
    def get_total_usage(self) -> Dict[str, TokenUsage]:
        """Get total usage across all interfaces."""
        return {name: interface.get_total_usage() for name, interface in self.interfaces.items()}
    
    def get_request_history(self) -> List[LLMResponse]:
        """Get complete request history for transparency."""
        return self.request_history.copy()
    
    def get_transparency_log(self) -> List[Dict[str, Any]]:
        """Get transparency log showing all LLM interactions."""
        return [response.to_dict() for response in self.request_history]