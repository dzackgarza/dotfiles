"""Base classes and implementations for cognitive modules."""

import asyncio
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, AsyncIterator, Union
from pydantic import BaseModel, Field

from .llm_interface import LLMInterface, LLMRequest, LLMResponse, LLMStreamChunk, TokenUsage
from .base import PluginState, RenderContext
from .display import PluginDisplayFormatter, PluginTimer, PluginTokenCounter


@dataclass
class CognitiveModuleMetadata:
    """Metadata for a cognitive module."""
    name: str
    version: str
    description: str
    author: str
    task_type: str  # e.g., "routing", "prompt_enhancement", "reasoning"
    required_llm_capabilities: List[str] = None  # e.g., ["completion", "streaming"]
    
    def __post_init__(self):
        if self.required_llm_capabilities is None:
            self.required_llm_capabilities = ["completion"]


class CognitiveModuleInput(BaseModel):
    """Input to a cognitive module."""
    content: str
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Chain information
    previous_outputs: List[Any] = Field(default_factory=list)
    chain_position: int = 0
    total_chain_length: int = 1


class CognitiveModuleOutput(BaseModel):
    """Output from a cognitive module."""
    content: str
    thoughts: str = ""  # LLM's thinking process
    confidence: float = 1.0
    context: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # LLM interaction details
    llm_response: Optional[LLMResponse] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for chaining."""
        return {
            "content": self.content,
            "thoughts": self.thoughts,
            "confidence": self.confidence,
            "context": self.context,
            "metadata": self.metadata,
            "llm_response": self.llm_response.to_dict() if self.llm_response else None
        }


class CognitiveModule(ABC):
    """
    Base class for cognitive modules.
    
    Cognitive modules are:
    - Stateless: No persistent state between calls
    - Testable in isolation: Work the same alone or in chains
    - LLM-focused: Each module typically uses exactly one LLM call
    - Transparent: All LLM interactions are logged
    - Streamable: Support streaming responses
    """
    
    def __init__(self, module_id: Optional[str] = None):
        self.module_id = module_id or str(uuid.uuid4())
        self.state = PluginState.INACTIVE
        self._timer = PluginTimer()
        self._token_counter = PluginTokenCounter()
        self._last_llm_response: Optional[LLMResponse] = None
        
    @property
    @abstractmethod
    def metadata(self) -> CognitiveModuleMetadata:
        """Get module metadata."""
        pass
    
    @abstractmethod
    async def process(self, 
                     input_data: CognitiveModuleInput,
                     llm_interface: LLMInterface) -> CognitiveModuleOutput:
        """Process input using the LLM interface."""
        pass
    
    @abstractmethod
    async def stream_process(self,
                           input_data: CognitiveModuleInput,
                           llm_interface: LLMInterface) -> AsyncIterator[Union[CognitiveModuleOutput, str]]:
        """Stream process input using the LLM interface."""
        pass
    
    @abstractmethod
    def create_llm_request(self, input_data: CognitiveModuleInput) -> LLMRequest:
        """Create LLM request for this module."""
        pass
    
    async def render(self, context: RenderContext) -> Dict[str, Any]:
        """Render the cognitive module's display."""
        render_data = await self._on_render(context)
        
        # Apply standardized display formatting
        duration = self._timer.get_duration()
        tokens = self._token_counter.get_counts()
        animated = context.display_mode == "live" and self.state == PluginState.PROCESSING
        
        render_data = PluginDisplayFormatter.standardize_render_data(
            render_data,
            self.metadata.name,
            self.state,
            duration,
            tokens,
            animated
        )
        
        # Add cognitive module specific metadata
        render_data.update({
            "module_id": self.module_id,
            "module_name": self.metadata.name,
            "module_state": self.state,
            "task_type": self.metadata.task_type,
            "llm_response": self._last_llm_response.to_dict() if self._last_llm_response else None
        })
        
        return render_data
    
    async def _on_render(self, context: RenderContext) -> Dict[str, Any]:
        """Default rendering implementation."""
        return {
            "render_type": "cognitive_module",
            "content": f"Cognitive module: {self.metadata.name}",
            "display_mode": context.display_mode,
            "style": {
                "box_style": "rounded",
                "border_color": "purple",
                "title_style": "bold",
            }
        }
    
    def get_module_info(self) -> Dict[str, Any]:
        """Get comprehensive module information."""
        return {
            "module_id": self.module_id,
            "metadata": {
                "name": self.metadata.name,
                "version": self.metadata.version,
                "description": self.metadata.description,
                "author": self.metadata.author,
                "task_type": self.metadata.task_type,
                "required_llm_capabilities": self.metadata.required_llm_capabilities
            },
            "state": self.state,
            "duration": self._timer.get_duration(),
            "tokens": self._token_counter.get_counts(),
            "last_llm_response": self._last_llm_response.to_dict() if self._last_llm_response else None
        }
    
    def _update_from_llm_response(self, response: LLMResponse) -> None:
        """Update module state from LLM response."""
        self._last_llm_response = response
        self._token_counter.add_input_tokens(response.tokens.input_tokens)
        self._token_counter.add_output_tokens(response.tokens.output_tokens)
        if response.tokens.thoughts_tokens > 0:
            self._token_counter.add_output_tokens(response.tokens.thoughts_tokens)
    
    def get_token_counts(self) -> Dict[str, int]:
        """Get current token counts."""
        return self._token_counter.get_counts()


class QueryRoutingModule(CognitiveModule):
    """Cognitive module for routing queries to appropriate handlers."""
    
    @property
    def metadata(self) -> CognitiveModuleMetadata:
        return CognitiveModuleMetadata(
            name="query_routing",
            version="1.0.0",
            description="Routes queries to appropriate processing paths",
            author="LLM REPL Team",
            task_type="routing",
            required_llm_capabilities=["completion"]
        )
    
    def create_llm_request(self, input_data: CognitiveModuleInput) -> LLMRequest:
        """Create LLM request for query routing."""
        system_prompt = """You are a query routing system. Analyze the user's query and determine the most appropriate processing path.
        
Available routes:
- chat: General conversation or questions
- code: Code-related requests (debugging, writing, explaining)
- research: Research tasks requiring web search or deep analysis
- creative: Creative writing, brainstorming, artistic tasks
- technical: Technical documentation, explanations, tutorials
- task: Task management, planning, organization

Respond with just the route name and a brief explanation."""
        
        messages = [
            {"role": "user", "content": input_data.content}
        ]
        
        return LLMRequest(
            messages=messages,
            system_prompt=system_prompt,
            model="gpt-4",
            temperature=0.1,
            max_tokens=100,
            request_id=str(uuid.uuid4()),
            cognitive_module=self.metadata.name,
            task_description="Route user query to appropriate handler"
        )
    
    async def process(self, 
                     input_data: CognitiveModuleInput,
                     llm_interface: LLMInterface) -> CognitiveModuleOutput:
        """Process query routing."""
        self.state = PluginState.PROCESSING
        self._timer.start()
        
        try:
            request = self.create_llm_request(input_data)
            response = await llm_interface.make_request(request)
            
            self._update_from_llm_response(response)
            
            # Parse the routing decision
            route_info = self._parse_routing_response(response.content)
            
            self.state = PluginState.COMPLETED
            self._timer.stop()
            
            return CognitiveModuleOutput(
                content=route_info["route"],
                thoughts=response.thoughts,
                confidence=route_info["confidence"],
                context={"route": route_info["route"], "explanation": route_info["explanation"]},
                metadata={"routing_decision": route_info},
                llm_response=response
            )
            
        except Exception as e:
            self.state = PluginState.ERROR
            self._timer.stop()
            raise
    
    async def stream_process(self,
                           input_data: CognitiveModuleInput,
                           llm_interface: LLMInterface) -> AsyncIterator[Union[CognitiveModuleOutput, str]]:
        """Stream process query routing."""
        self.state = PluginState.PROCESSING
        self._timer.start()
        
        try:
            request = self.create_llm_request(input_data)
            request.stream = True
            
            accumulated_content = ""
            accumulated_thoughts = ""
            
            async for chunk in llm_interface.stream_request(request):
                accumulated_content += chunk.content
                accumulated_thoughts += chunk.thoughts
                
                # Yield intermediate content
                yield chunk.content
                
                if chunk.is_complete:
                    # Parse final routing decision
                    route_info = self._parse_routing_response(accumulated_content)
                    
                    self.state = PluginState.COMPLETED
                    self._timer.stop()
                    
                    # Create final response for token tracking
                    final_response = LLMResponse(
                        content=accumulated_content,
                        thoughts=accumulated_thoughts,
                        tokens=TokenUsage(
                            input_tokens=len(request.messages[0]["content"].split()),
                            output_tokens=len(accumulated_content.split()),
                            thoughts_tokens=len(accumulated_thoughts.split())
                        ),
                        duration_seconds=self._timer.get_duration() or 0,
                        model=request.model,
                        request_id=request.request_id,
                        cognitive_module=self.metadata.name,
                        task_description=request.task_description
                    )
                    
                    self._update_from_llm_response(final_response)
                    
                    yield CognitiveModuleOutput(
                        content=route_info["route"],
                        thoughts=accumulated_thoughts,
                        confidence=route_info["confidence"],
                        context={"route": route_info["route"], "explanation": route_info["explanation"]},
                        metadata={"routing_decision": route_info},
                        llm_response=final_response
                    )
                    
        except Exception as e:
            self.state = PluginState.ERROR
            self._timer.stop()
            raise
    
    def _parse_routing_response(self, content: str) -> Dict[str, Any]:
        """Parse the routing response from LLM."""
        # Simple parsing logic - in real implementation, this would be more sophisticated
        content_lower = content.lower()
        
        routes = ["chat", "code", "research", "creative", "technical", "task"]
        detected_route = "chat"  # default
        
        for route in routes:
            if route in content_lower:
                detected_route = route
                break
        
        return {
            "route": detected_route,
            "explanation": content.strip(),
            "confidence": 0.9  # Mock confidence
        }


class PromptEnhancementModule(CognitiveModule):
    """Cognitive module for enhancing/optimizing user prompts."""
    
    @property
    def metadata(self) -> CognitiveModuleMetadata:
        return CognitiveModuleMetadata(
            name="prompt_enhancement",
            version="1.0.0",
            description="Enhances and optimizes user prompts for better LLM responses",
            author="LLM REPL Team",
            task_type="prompt_enhancement",
            required_llm_capabilities=["completion", "streaming"]
        )
    
    def create_llm_request(self, input_data: CognitiveModuleInput) -> LLMRequest:
        """Create LLM request for prompt enhancement."""
        system_prompt = """You are a prompt enhancement system. Take the user's query and optimize it for better LLM responses.
        
Enhancement techniques:
- Add context and specificity
- Structure the request clearly
- Include relevant constraints or requirements
- Specify desired output format
- Add examples if helpful

Respond with the enhanced prompt only."""
        
        messages = [
            {"role": "user", "content": f"Original prompt: {input_data.content}"}
        ]
        
        return LLMRequest(
            messages=messages,
            system_prompt=system_prompt,
            model="gpt-4",
            temperature=0.3,
            max_tokens=500,
            request_id=str(uuid.uuid4()),
            cognitive_module=self.metadata.name,
            task_description="Enhance and optimize user prompt"
        )
    
    async def process(self, 
                     input_data: CognitiveModuleInput,
                     llm_interface: LLMInterface) -> CognitiveModuleOutput:
        """Process prompt enhancement."""
        self.state = PluginState.PROCESSING
        self._timer.start()
        
        try:
            request = self.create_llm_request(input_data)
            response = await llm_interface.make_request(request)
            
            self._update_from_llm_response(response)
            
            self.state = PluginState.COMPLETED
            self._timer.stop()
            
            return CognitiveModuleOutput(
                content=response.content,
                thoughts=response.thoughts,
                confidence=0.95,  # High confidence for enhancement
                context={"original_prompt": input_data.content, "enhanced_prompt": response.content},
                metadata={"enhancement_type": "prompt_optimization"},
                llm_response=response
            )
            
        except Exception as e:
            self.state = PluginState.ERROR
            self._timer.stop()
            raise
    
    async def stream_process(self,
                           input_data: CognitiveModuleInput,
                           llm_interface: LLMInterface) -> AsyncIterator[Union[CognitiveModuleOutput, str]]:
        """Stream process prompt enhancement."""
        self.state = PluginState.PROCESSING
        self._timer.start()
        
        try:
            request = self.create_llm_request(input_data)
            request.stream = True
            
            accumulated_content = ""
            accumulated_thoughts = ""
            
            async for chunk in llm_interface.stream_request(request):
                accumulated_content += chunk.content
                accumulated_thoughts += chunk.thoughts
                
                # Yield intermediate content
                yield chunk.content
                
                if chunk.is_complete:
                    self.state = PluginState.COMPLETED
                    self._timer.stop()
                    
                    # Create final response for token tracking
                    final_response = LLMResponse(
                        content=accumulated_content,
                        thoughts=accumulated_thoughts,
                        tokens=TokenUsage(
                            input_tokens=len(request.messages[0]["content"].split()),
                            output_tokens=len(accumulated_content.split()),
                            thoughts_tokens=len(accumulated_thoughts.split())
                        ),
                        duration_seconds=self._timer.get_duration() or 0,
                        model=request.model,
                        request_id=request.request_id,
                        cognitive_module=self.metadata.name,
                        task_description=request.task_description
                    )
                    
                    self._update_from_llm_response(final_response)
                    
                    yield CognitiveModuleOutput(
                        content=accumulated_content,
                        thoughts=accumulated_thoughts,
                        confidence=0.95,
                        context={"original_prompt": input_data.content, "enhanced_prompt": accumulated_content},
                        metadata={"enhancement_type": "prompt_optimization"},
                        llm_response=final_response
                    )
                    
        except Exception as e:
            self.state = PluginState.ERROR
            self._timer.stop()
            raise


class ReasoningModule(CognitiveModule):
    """Cognitive module for structured reasoning and thinking."""
    
    @property
    def metadata(self) -> CognitiveModuleMetadata:
        return CognitiveModuleMetadata(
            name="reasoning",
            version="1.0.0",
            description="Performs structured reasoning and step-by-step thinking",
            author="LLM REPL Team",
            task_type="reasoning",
            required_llm_capabilities=["completion", "streaming"]
        )
    
    def create_llm_request(self, input_data: CognitiveModuleInput) -> LLMRequest:
        """Create LLM request for reasoning."""
        system_prompt = """You are a reasoning system. Break down complex problems into clear, logical steps.
        
Reasoning approach:
1. Understand the problem clearly
2. Identify key components and constraints
3. Consider multiple approaches
4. Work through the logic step by step
5. Arrive at a well-reasoned conclusion

Show your thinking process clearly."""
        
        messages = [
            {"role": "user", "content": input_data.content}
        ]
        
        return LLMRequest(
            messages=messages,
            system_prompt=system_prompt,
            model="gpt-4",
            temperature=0.2,
            max_tokens=1000,
            request_id=str(uuid.uuid4()),
            cognitive_module=self.metadata.name,
            task_description="Perform structured reasoning"
        )
    
    async def process(self, 
                     input_data: CognitiveModuleInput,
                     llm_interface: LLMInterface) -> CognitiveModuleOutput:
        """Process reasoning."""
        self.state = PluginState.PROCESSING
        self._timer.start()
        
        try:
            request = self.create_llm_request(input_data)
            response = await llm_interface.make_request(request)
            
            self._update_from_llm_response(response)
            
            self.state = PluginState.COMPLETED
            self._timer.stop()
            
            return CognitiveModuleOutput(
                content=response.content,
                thoughts=response.thoughts,
                confidence=0.85,  # Reasoning confidence
                context={"reasoning_steps": self._extract_reasoning_steps(response.content)},
                metadata={"reasoning_type": "structured_thinking"},
                llm_response=response
            )
            
        except Exception as e:
            self.state = PluginState.ERROR
            self._timer.stop()
            raise
    
    async def stream_process(self,
                           input_data: CognitiveModuleInput,
                           llm_interface: LLMInterface) -> AsyncIterator[Union[CognitiveModuleOutput, str]]:
        """Stream process reasoning."""
        self.state = PluginState.PROCESSING
        self._timer.start()
        
        try:
            request = self.create_llm_request(input_data)
            request.stream = True
            
            accumulated_content = ""
            accumulated_thoughts = ""
            
            async for chunk in llm_interface.stream_request(request):
                accumulated_content += chunk.content
                accumulated_thoughts += chunk.thoughts
                
                # Yield intermediate content
                yield chunk.content
                
                if chunk.is_complete:
                    self.state = PluginState.COMPLETED
                    self._timer.stop()
                    
                    # Create final response for token tracking
                    final_response = LLMResponse(
                        content=accumulated_content,
                        thoughts=accumulated_thoughts,
                        tokens=TokenUsage(
                            input_tokens=len(request.messages[0]["content"].split()),
                            output_tokens=len(accumulated_content.split()),
                            thoughts_tokens=len(accumulated_thoughts.split())
                        ),
                        duration_seconds=self._timer.get_duration() or 0,
                        model=request.model,
                        request_id=request.request_id,
                        cognitive_module=self.metadata.name,
                        task_description=request.task_description
                    )
                    
                    self._update_from_llm_response(final_response)
                    
                    yield CognitiveModuleOutput(
                        content=accumulated_content,
                        thoughts=accumulated_thoughts,
                        confidence=0.85,
                        context={"reasoning_steps": self._extract_reasoning_steps(accumulated_content)},
                        metadata={"reasoning_type": "structured_thinking"},
                        llm_response=final_response
                    )
                    
        except Exception as e:
            self.state = PluginState.ERROR
            self._timer.stop()
            raise
    
    def _extract_reasoning_steps(self, content: str) -> List[str]:
        """Extract reasoning steps from content."""
        # Simple extraction - look for numbered steps
        steps = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('Step')):
                steps.append(line)
        
        return steps if steps else ["Single reasoning block"]