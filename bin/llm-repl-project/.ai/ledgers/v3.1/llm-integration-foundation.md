# LLM Integration Foundation

**Branch:** feat/llm-integration-foundation
**Summary:** Replace V3-minimal's mock cognition simulation with real LLM integration supporting multiple providers (Ollama, Groq, OpenAI) for actual AI processing in the Sacred Timeline.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
V3-minimal has **NO REAL LLM INTEGRATION** - all cognition steps are hardcoded simulations with fake token counts and mock responses. This violates the core principle that the Sacred Timeline should show transparent AI processing. The current implementation uses `random.randint(5, 15)` for tokens instead of actual LLM usage, making it a UI mockup rather than a functional LLM REPL.

### Success Criteria
- [ ] Real LLM calls replace mock cognition simulation
- [ ] Multiple LLM providers supported (Ollama, Groq, OpenAI, Anthropic)
- [ ] Actual token counting from LLM responses
- [ ] Real timing data from LLM operations
- [ ] Provider-specific model routing and optimization

### Acceptance Criteria
- [ ] User input generates real LLM responses (not simulated)
- [ ] Token counts reflect actual LLM usage
- [ ] Timing data shows real processing duration
- [ ] Multiple providers can be configured and used
- [ ] LLM failures are handled gracefully with error blocks

## Technical Approach

### Architecture Changes
1. **LLM Provider Interface**: Abstract interface for different LLM providers
2. **Model Router**: Intelligent routing to optimal models for each task
3. **Token Tracker**: Real token usage tracking and cost calculation
4. **Response Processor**: Handle streaming and batch LLM responses
5. **Provider Manager**: Configuration and lifecycle management for providers

### Implementation Plan
1. **Phase 1: Provider Interface**
   - Create `LLMProvider` abstract base class
   - Implement basic providers: Ollama, OpenAI, Anthropic
   - Add provider configuration and authentication

2. **Phase 2: Integration Layer**
   - Create `LLMManager` for provider orchestration
   - Implement request/response processing
   - Add real token tracking and timing

3. **Phase 3: Cognition Pipeline Integration**
   - Replace mock cognition with real LLM processing
   - Implement 3-step cognition pipeline with real models
   - Add query routing, tool calling, response formatting

4. **Phase 4: Advanced Features**
   - Add streaming response support
   - Implement cost optimization and provider selection
   - Add error handling and retry logic

### Dependencies
- Plugin Validator System (to validate LLM-based plugins)
- Sacred Timeline Persistence (to store real LLM interaction history)

### Risks & Mitigations
- **Risk 1**: LLM provider API failures breaking application
  - *Mitigation*: Graceful degradation, retry logic, fallback providers
- **Risk 2**: High API costs from excessive LLM usage
  - *Mitigation*: Token budgets, cost tracking, efficient model selection
- **Risk 3**: Slow response times affecting user experience
  - *Mitigation*: Streaming responses, async processing, caching

## Progress Log

### 2025-07-10 - Initial Planning
- Identified complete lack of real LLM integration in V3-minimal
- Analyzed V2 LLM interface system for reference
- Designed provider abstraction for multiple LLM services
- Created integration strategy for cognition pipeline

## Technical Decisions

### Decision 1: Provider Abstraction Pattern
**Context**: Need to support multiple LLM providers with different APIs  
**Options**: Provider-specific implementations, unified interface, adapter pattern  
**Decision**: Abstract provider interface with concrete implementations  
**Reasoning**: Clean separation, easy to add new providers, testable in isolation  
**Consequences**: Consistent interface across providers, maintenance overhead

### Decision 2: Async vs Sync LLM Calls
**Context**: LLM calls can be slow and should not block UI  
**Options**: Synchronous blocking, async/await, threading, multiprocessing  
**Decision**: Async/await with proper event loop integration  
**Reasoning**: Best integration with Textual framework, proper concurrency  
**Consequences**: More complex but better user experience

### Decision 3: Streaming vs Batch Processing
**Context**: Users want to see LLM responses as they're generated  
**Options**: Batch responses only, streaming only, hybrid approach  
**Decision**: Hybrid - streaming for user-facing, batch for internal processing  
**Reasoning**: Best user experience with flexibility for different use cases  
**Consequences**: More implementation complexity but better UX

## LLM Provider Interface

### Core Provider Interface
```python
@dataclass
class LLMRequest:
    messages: List[Dict[str, str]]
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stream: bool = False
    system_prompt: Optional[str] = None

@dataclass  
class LLMResponse:
    content: str
    tokens_input: int
    tokens_output: int
    duration_seconds: float
    model: str
    provider: str

class LLMProvider(ABC):
    @abstractmethod
    async def make_request(self, request: LLMRequest) -> LLMResponse:
        pass
    
    @abstractmethod
    async def stream_request(self, request: LLMRequest) -> AsyncIterator[str]:
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        pass
```

### Provider Implementations
```python
class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    async def make_request(self, request: LLMRequest) -> LLMResponse:
        # Ollama API integration
        
class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def make_request(self, request: LLMRequest) -> LLMResponse:
        # OpenAI API integration
```

## Cognition Pipeline Integration

### Real Cognition Processing
```python
class CognitionProcessor:
    def __init__(self, llm_manager: LLMManager):
        self.llm_manager = llm_manager
    
    async def process_user_input(self, user_input: str) -> CognitionResult:
        # Step 1: Route Query
        route_response = await self._route_query(user_input)
        
        # Step 2: Call Tool/Process
        tool_response = await self._call_tool(user_input, route_response)
        
        # Step 3: Format Output  
        final_response = await self._format_output(tool_response)
        
        return CognitionResult(
            steps=[route_response, tool_response, final_response],
            final_output=final_response.content
        )
```

### Model Routing Strategy
- **Query Routing**: Fast local model (tinyllama, phi-3)
- **Tool Calling**: Capable model (llama3.1, gpt-4)  
- **Response Formatting**: Balanced model (mistral, claude-3)
- **Fallback**: Always have working local model available

## Testing Strategy

### Unit Tests
- [ ] LLM provider interface implementations
- [ ] Request/response processing
- [ ] Token counting accuracy
- [ ] Error handling for API failures

### Integration Tests
- [ ] Full cognition pipeline with real LLMs
- [ ] Provider switching and fallback
- [ ] Streaming response handling
- [ ] Cost tracking and budgets

### Manual Testing
- [ ] Various user queries with different providers
- [ ] Provider failure scenarios
- [ ] Streaming response visualization
- [ ] Token usage verification

## Configuration System

### Provider Configuration
```yaml
llm_providers:
  ollama:
    enabled: true
    base_url: "http://localhost:11434"
    models: ["tinyllama", "phi-3", "llama3.1"]
    
  openai:
    enabled: false
    api_key: "${OPENAI_API_KEY}"
    models: ["gpt-4", "gpt-3.5-turbo"]
    
  anthropic:
    enabled: false
    api_key: "${ANTHROPIC_API_KEY}"
    models: ["claude-3-sonnet", "claude-3-haiku"]

routing_strategy:
  query_routing: "ollama:tinyllama"
  tool_calling: "ollama:llama3.1"
  response_formatting: "ollama:phi-3"
  fallback: "ollama:tinyllama"
```

## Documentation Updates

- [ ] LLM provider setup and configuration guide
- [ ] Model selection and routing documentation
- [ ] Token usage and cost tracking guide
- [ ] Troubleshooting guide for LLM integration issues

## Error Handling Strategy

### Provider Failures
- Graceful fallback to alternative providers
- Clear error messages in timeline blocks
- Retry logic with exponential backoff
- Offline mode with local models only

### API Rate Limits
- Automatic rate limiting and queuing
- Provider rotation for high-volume usage
- User notification of rate limit issues
- Cost budget enforcement

## Performance Considerations

### Response Time Optimization
- Parallel requests where possible
- Caching for repeated queries
- Model warm-up for faster first responses
- Connection pooling for API efficiency

### Cost Optimization
- Intelligent model selection based on task complexity
- Token usage monitoring and alerts
- Provider cost comparison and automatic selection
- Batch processing for efficiency

## Completion

### Final Status
- [ ] Real LLM integration replacing mock simulation
- [ ] Multiple providers configured and working
- [ ] Cognition pipeline using actual AI processing
- [ ] Token tracking showing real usage data
- [ ] Streaming responses implemented

### Follow-up Items
- [ ] Advanced model fine-tuning support
- [ ] Custom provider plugin system
- [ ] LLM performance analytics and optimization
- [ ] Enterprise provider management features

---

*This ledger tracks the transformation of V3-minimal from a UI mockup into a functional LLM REPL with real AI integration.*

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system
