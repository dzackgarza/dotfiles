# Intelligent Router System

**Branch:** feat/intelligent-router-system
**Summary:** Implement the core Intelligent Router component that analyzes user intent and dynamically routes tasks to the most appropriate plugins, LLMs, or external tools based on query analysis, *contributing to the transparency of the Cognition Block by managing and displaying its internal steps as 'live' sub-blocks with aggregated metrics*.
**Status:** High Priority - Critical Architectural Foundation
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
V3-minimal has **NO QUERY ROUTING** - all user inputs are processed identically through hardcoded cognition steps. The Sacred Timeline architecture requires an "Intelligent Router: A specialized plugin responsible for analyzing user intent and dynamically routing tasks to the most appropriate plugins, LLMs (local, remote, specialized), or external tools." **Furthermore, the router's internal decision-making and execution steps must be transparently displayed within the Cognition Block as 'live' sub-blocks, with their individual wall times, token usage, and intermediate outputs aggregated and presented at the parent Cognition Block level. This is crucial for maintaining the Sacred Timeline's principle of full data transparency and enabling the 'live' vs. 'inscribed' block lifecycle.**

### Success Criteria
- [ ] User queries are analyzed for intent classification
- [ ] Different query types route to optimal processing paths
- [ ] LLM selection is optimized based on task requirements
- [ ] Plugin selection is dynamic based on query analysis
- [ ] Routing decisions are transparent and explainable
- [ ] **Each routing step (e.g., LLM call, plugin execution) is represented as a 'live' sub-block within the parent Cognition Block.**
- [ ] **Wall times, token usage, and intermediate outputs from each routing step are captured and aggregated.**
- [ ] **Aggregated metrics are displayed on the parent Cognition Block as it processes.**
- [ ] **Sub-blocks transition from 'live' to 'inscribed' upon completion of their respective routing steps.**

### Acceptance Criteria
- [ ] Code queries route to code-specialized models and tools
- [ ] Research queries trigger web search and analysis plugins
- [ ] Creative tasks use creative-optimized models
- [ ] Math queries route to calculation-capable tools
- [ ] Routing logic is visible in cognition pipeline
- [ ] **The Cognition Block visually updates with each routing step, showing progress and intermediate results.**
- [ ] **The final Cognition Block (when inscribed) displays total wall time and token usage aggregated from all its routing sub-steps.**
- [ ] **Users can observe the dynamic selection and execution of plugins/LLMs during the routing process.**

## Technical Approach

### Architecture Changes
1. **Intent Classifier**: LLM-based analysis of user query intent
2. **Route Registry**: Configurable mapping of intents to processing paths
3. **Resource Manager**: Optimal selection of LLMs, plugins, and tools
4. **Routing Engine**: Orchestrates routing decisions and execution
5. **Fallback System**: Graceful degradation when routing fails
6. **Live Block Integration**: Mechanisms to create, update, and complete 'live' sub-blocks for each routing step, interacting with the `LiveBlockManager`.
7. **Data Aggregation**: Logic within the `IntelligentCognitionPlugin` to collect and sum metrics (wall time, tokens) from its child routing steps.

### Implementation Plan
1. **Phase 1: Intent Classification & Basic Routing**
   - Create intent classification system using fast local LLMs
   - Define core intent categories (code, research, creative, math, chat)
   - Implement confidence scoring for routing decisions
   - **Integrate with `LiveBlockManager` to create a 'live' sub-block for the intent classification step.**

2. **Phase 2: Route Registry & Step Execution**
   - Build configurable routing table for intent → processing path
   - Add plugin discovery and capability matching
   - Implement LLM provider selection based on task requirements
   - **For each step in the routing path, create a 'live' sub-block, stream its output, and capture its metrics.**

3. **Phase 3: Routing Engine & Aggregation**
   - Create routing orchestrator that executes optimal paths
   - Add transparency logging for routing decisions
   - Implement parallel routing for complex multi-intent queries
   - **Implement logic within `IntelligentCognitionPlugin` to aggregate wall times and token usage from all executed routing steps.**
   - **Ensure sub-blocks transition from 'live' to 'inscribed' upon completion of their respective routing steps.**

4. **Phase 4: Advanced Routing & UI Transparency**
   - Add context-aware routing (user history, preferences)
   - Implement cost optimization for LLM selection
   - Add performance monitoring and route optimization
   - **Visually represent nested routing steps within the Cognition Block in the UI, showing their live updates and final aggregated metrics.**

### Dependencies
- LLM Integration Foundation (for intent classification and routing)
- Plugin Architecture Foundation (for dynamic plugin selection, nesting)
- Event-Driven Communication (for routing coordination, *and for emitting live block updates and completion events*)
- **`streaming-live-output-system.md` (for managing 'live' blocks and streaming updates).**
- **`timeline.md` (for `TimelineBlock` definition and `TimelineManager` interaction).**

### Risks & Mitigations
- **Risk 1**: Intent classification accuracy affecting routing quality
  - *Mitigation*: Multiple classification approaches, confidence thresholds, fallbacks
- **Risk 2**: Complex routing logic becoming unmaintainable
  - *Mitigation*: Clear routing rules, extensive testing, visual routing tools
- **Risk 3**: Performance overhead from routing analysis
  - *Mitigation*: Fast local models for classification, caching, optimization
- **Risk 4**: Ensuring accurate aggregation of metrics from nested, asynchronous routing steps.
  - *Mitigation*: Robust event-driven metric collection, clear data models for sub-blocks.

## Progress Log

### 2025-07-10 - Initial Planning
- Identified missing intelligent routing in V3-minimal
- Analyzed Sacred Timeline routing requirements
- Designed intent classification and routing architecture
- Created implementation strategy for dynamic routing
- **Elevated priority to address transparent display of routing steps as live sub-blocks and aggregation of metrics.**

## Technical Decisions

### Decision 1: Intent Classification Approach
**Context**: Need fast, accurate intent classification for routing decisions  
**Options**: Rule-based classification, local LLM, remote LLM, hybrid approach  
**Decision**: Fast local LLM with rule-based fallback  
**Reasoning**: Good accuracy with low latency, offline capability, cost-effective  
**Consequences**: Requires local model setup but provides responsive routing

### Decision 2: Routing Configuration Strategy
**Context**: Routing rules need to be configurable and maintainable  
**Options**: Hardcoded rules, YAML configuration, database-driven, plugin-based  
**Decision**: YAML configuration with plugin-based extensions  
**Reasoning**: Human-readable, version-controlled, extensible for custom routing  
**Consequences**: Configuration complexity but flexible routing system

### Decision 3: Resource Selection Algorithm
**Context**: Multiple LLMs/plugins may be suitable for a task  
**Options**: First match, best match scoring, cost optimization, user preference  
**Decision**: Multi-criteria scoring with user preferences and cost consideration  
**Reasoning**: Optimal resource selection balancing quality, cost, and user needs  
**Consequences**: More complex selection but better user experience

## Intent Classification System

### Core Intent Categories
```python
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

class IntentCategory(Enum):
    CODE = "code"                    # Programming, debugging, code analysis
    RESEARCH = "research"            # Information gathering, analysis
    CREATIVE = "creative"            # Writing, brainstorming, art
    MATH = "math"                   # Calculations, problem solving
    CHAT = "chat"                   # General conversation
    TASK = "task"                   # Planning, organization, todo
    TECHNICAL = "technical"          # Documentation, explanations
    FILE = "file"                   # File operations, editing
    WEB = "web"                     # Web search, scraping
    ANALYSIS = "analysis"           # Data analysis, interpretation

@dataclass
class IntentClassification:
    primary_intent: IntentCategory
    confidence: float                # 0.0 to 1.0
    secondary_intents: List[IntentCategory] = field(default_factory=list)
    reasoning: str = ""
    keywords: List[str] = field(default_factory=list)
    complexity: str = "medium"       # low, medium, high
    estimated_tokens: int = 100

class IntentClassifier:
    """Classifies user queries into routing intents."""
    
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider
        self.classification_cache: Dict[str, IntentClassification] = {}
        self._load_classification_rules()
    
    async def classify_intent(self, user_query: str) -> IntentClassification:
        """Classify user query intent for routing."""
        # Check cache first
        query_hash = hashlib.md5(user_query.encode()).hexdigest()
        if query_hash in self.classification_cache:
            return self.classification_cache[query_hash]
        
        # Rule-based quick classification
        rule_result = self._classify_by_rules(user_query)
        if rule_result.confidence > 0.8:
            self.classification_cache[query_hash] = rule_result
            return rule_result
        
        # LLM-based classification for ambiguous cases
        llm_result = await self._classify_by_llm(user_query)
        
        # Combine rule and LLM results
        final_result = self._combine_classifications(rule_result, llm_result)
        self.classification_cache[query_hash] = final_result
        
        return final_result
    
    def _classify_by_rules(self, query: str) -> IntentClassification:
        """Fast rule-based classification."""
        query_lower = query.lower()
        
        # Code patterns
        code_keywords = ["code", "function", "bug", "debug", "implement", "python", "javascript", "error"]
        if any(keyword in query_lower for keyword in code_keywords):
            return IntentClassification(
                primary_intent=IntentCategory.CODE,
                confidence=0.9,
                reasoning="Code-related keywords detected",
                keywords=[kw for kw in code_keywords if kw in query_lower]
            )
        
        # Research patterns
        research_keywords = ["research", "find", "search", "learn", "study", "analyze", "investigate"]
        if any(keyword in query_lower for keyword in research_keywords):
            return IntentClassification(
                primary_intent=IntentCategory.RESEARCH,
                confidence=0.8,
                reasoning="Research-related keywords detected",
                keywords=[kw for kw in research_keywords if kw in query_lower]
            )
        
        # Math patterns
        math_keywords = ["calculate", "solve", "equation", "math", "formula", "compute"]
        if any(keyword in query_lower for keyword in math_keywords):
            return IntentClassification(
                primary_intent=IntentCategory.MATH,
                confidence=0.9,
                reasoning="Math-related keywords detected"
            )
        
        # Default to chat with low confidence
        return IntentClassification(
            primary_intent=IntentCategory.CHAT,
            confidence=0.3,
            reasoning="No specific patterns detected"
        )
    
    async def _classify_by_llm(self, query: str) -> IntentClassification:
        """LLM-based intent classification."""
        system_prompt = """You are an intent classifier for an AI assistant. Analyze the user query and determine the primary intent category.

Categories:
- CODE: Programming, debugging, code analysis, software development
- RESEARCH: Information gathering, learning, investigation, analysis
- CREATIVE: Writing, brainstorming, artistic tasks, creative content
- MATH: Calculations, problem solving, mathematical operations
- CHAT: General conversation, casual questions, social interaction
- TASK: Planning, organization, todo lists, project management
- TECHNICAL: Documentation, explanations, tutorials, how-to guides
- FILE: File operations, editing, reading, writing files
- WEB: Web search, scraping, online research, URL analysis
- ANALYSIS: Data analysis, interpretation, insights, reporting

Respond with JSON format:
{
  "primary_intent": "CATEGORY",
  "confidence": 0.95,
  "secondary_intents": ["CATEGORY2"],
  "reasoning": "Brief explanation",
  "complexity": "low|medium|high",
  "estimated_tokens": 150
}"""
        
        request = LLMRequest(
            messages=[{"role": "user", "content": query}],
            system_prompt=system_prompt,
            model="tinyllama",  # Fast local model
            temperature=0.1,
            max_tokens=200
        )
        
        response = await self.llm_provider.make_request(request)
        
        try:
            result_data = json.loads(response.content)
            return IntentClassification(
                primary_intent=IntentCategory(result_data["primary_intent"].lower()),
                confidence=result_data["confidence"],
                secondary_intents=[IntentCategory(intent.lower()) for intent in result_data.get("secondary_intents", [])],
                reasoning=result_data["reasoning"],
                complexity=result_data.get("complexity", "medium"),
                estimated_tokens=result_data.get("estimated_tokens", 100)
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Fallback to chat intent if LLM response is invalid
            return IntentClassification(
                primary_intent=IntentCategory.CHAT,
                confidence=0.5,
                reasoning=f"LLM classification failed: {e}"
            )
```

## Route Registry System

### Routing Configuration
```yaml
# routing_config.yaml
routes:
  code:
    description: "Programming and software development tasks"
    triggers:
      - "code"
      - "function"
      - "debug"
      - "implement"
    processing_path:
      - plugin: "code_analysis"
        config: { language_detection: true }
      - llm_provider: "ollama"
        model: "codellama"
        config: { temperature: 0.1 }
      - plugin: "syntax_highlighter"
    fallback_path:
      - llm_provider: "ollama"
        model: "llama3.1"
    
  research:
    description: "Information gathering and analysis"
    triggers:
      - "research"
      - "find"
      - "search"
      - "learn"
    processing_path:
      - plugin: "web_search"
        config: { max_results: 5 }
      - llm_provider: "groq"
        model: "llama-3.3-70b-versatile"
        config: { temperature: 0.3 }
      - plugin: "citation_formatter"
    
  math:
    description: "Mathematical calculations and problem solving"
    triggers:
      - "calculate"
      - "solve"
      - "equation"
    processing_path:
      - plugin: "math_parser"
      - plugin: "calculation_engine"
      - llm_provider: "ollama"
        model: "phi-3"
        config: { temperature: 0.0 }
    
  creative:
    description: "Creative writing and brainstorming"
    triggers:
      - "write"
      - "create"
      - "brainstorm"
    processing_path:
      - llm_provider: "anthropic"
        model: "claude-3-sonnet"
        config: { temperature: 0.8 }
      - plugin: "creativity_enhancer"

default_route:
  description: "General conversation and chat"
  processing_path:
    - llm_provider: "ollama"
      model: "tinyllama"
      config: { temperature: 0.7 }
```

### Route Registry Implementation
```python
@dataclass
class RouteConfig:
    description: str
    triggers: List[str]
    processing_path: List[Dict[str, Any]]
    fallback_path: Optional[List[Dict[str, Any]]] = None
    cost_tier: str = "medium"  # low, medium, high
    estimated_latency: float = 5.0  # seconds

class RouteRegistry:
    """Registry of routing configurations and rules."""
    
    def __init__(self, config_path: str = "routing_config.yaml"):
        self.routes: Dict[IntentCategory, RouteConfig] = {}
        self.default_route: Optional[RouteConfig] = None
        self._load_configuration(config_path)
    
    def _load_configuration(self, config_path: str) -> None:
        """Load routing configuration from YAML file."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        for intent_name, route_data in config["routes"].items():
            intent = IntentCategory(intent_name)
            self.routes[intent] = RouteConfig(**route_data)
        
        if "default_route" in config:
            self.default_route = RouteConfig(**config["default_route"])
    
    def get_route_for_intent(self, intent: IntentCategory) -> Optional[RouteConfig]:
        """Get routing configuration for an intent."""
        return self.routes.get(intent, self.default_route)
    
    def get_optimal_route(self, intent: IntentClassification,
                         user_preferences: Dict[str, Any] = None) -> RouteConfig:
        """Get optimal route considering user preferences and constraints."""
        base_route = self.get_route_for_intent(intent.primary_intent)
        
        if user_preferences:
            # Adjust route based on user preferences
            base_route = self._customize_route(base_route, user_preferences)
        
        return base_route or self.default_route
```

## Routing Engine

### Core Routing Engine
```python
class RoutingEngine:
    """Orchestrates intelligent routing of user queries."""
    
    def __init__(self, intent_classifier: IntentClassifier,
                 route_registry: RouteRegistry,
                 plugin_manager: PluginManager,
                 llm_manager: LLMManager,
                 live_block_manager: LiveBlockManager): # Added LiveBlockManager
        self.intent_classifier = intent_classifier
        self.route_registry = route_registry
        self.plugin_manager = plugin_manager
        self.llm_manager = llm_manager
        self.live_block_manager = live_block_manager # Stored
    
    async def route_query(self, user_query: str,
                         context: Dict[str, Any] = None) -> RoutingResult:
        """Route a user query through optimal processing path."""
        
        # Step 1: Classify intent
        # Create a live sub-block for intent classification
        intent_block_id = "intent_" + str(uuid.uuid4())
        self.live_block_manager.start_live_block(intent_block_id, "intent_classification")
        
        intent = await self.intent_classifier.classify_intent(user_query)
        
        # Complete the live sub-block for intent classification
        await self.live_block_manager.complete_live_block(
            intent_block_id,
            {"primary_intent": intent.primary_intent.value, "confidence": intent.confidence},
            {"wall_time_seconds": (datetime.now() - self.live_block_manager._live_blocks[intent_block_id].start_time).total_seconds(), "tokens_in": intent.estimated_tokens} # Example metrics
        )

        # Step 2: Get optimal route
        route = self.route_registry.get_optimal_route(
            intent, 
            context.get("user_preferences") if context else None
        )
        
        # Step 3: Execute routing
        routing_result = await self._execute_route(user_query, intent, route, context)
        
        return routing_result
    
    async def _execute_route(self, query: str, intent: IntentClassification,
                           route: RouteConfig, context: Dict[str, Any]) -> RoutingResult:
        """Execute the routing path."""
        result = RoutingResult(
            intent=intent,
            route_config=route,
            steps=[],
            final_output="",
            total_tokens=0,
            total_duration=0.0
        )
        
        try:
            for step_config in route.processing_path:
                # Create a live sub-block for each routing step
                step_block_id = "step_" + str(uuid.uuid4())
                step_type = step_config.get("plugin", step_config.get("llm_provider")) # Determine type for live block
                self.live_block_manager.start_live_block(step_block_id, step_type)

                step_result = await self._execute_step(query, step_config, context)
                result.steps.append(step_result)
                result.total_tokens += step_result.tokens_used
                result.total_duration += step_result.duration
                
                # Complete the live sub-block for this step
                await self.live_block_manager.complete_live_block(
                    step_block_id,
                    {"output": step_result.output[:200] + "..." if len(step_result.output) > 200 else step_result.output},
                    {"wall_time_seconds": step_result.duration, "tokens_in": step_result.tokens_used} # Example metrics
                )

                # Update query for next step if needed
                if step_result.output:
                    query = step_result.output
            
            result.final_output = query
            result.success = True
            
        except Exception as e:
            # Try fallback route if available
            if route.fallback_path:
                fallback_result = await self._execute_fallback(query, route, context)
                result.fallback_used = True
                result.fallback_result = fallback_result
            else:
                result.error = str(e)
        
        return result
    
    async def _execute_step(self, query: str, step_config: Dict[str, Any],
                          context: Dict[str, Any]) -> StepResult:
        """Execute a single routing step."""
        start_time = datetime.now()
        
        if "plugin" in step_config:
            # Execute plugin
            plugin_name = step_config["plugin"]
            plugin_config = step_config.get("config", {})
            
            plugin = await self.plugin_manager.load_plugin(plugin_name, plugin_config)
            output = await plugin.process(query, context)
            
            return StepResult(
                step_type="plugin",
                step_name=plugin_name,
                output=output.get("content", ""),
                tokens_used=output.get("tokens", 0),
                duration=(datetime.now() - start_time).total_seconds(),
                metadata=output.get("metadata", {})
            )
        
        elif "llm_provider" in step_config:
            # Execute LLM request
            provider_name = step_config["llm_provider"]
            model_name = step_config["model"]
            llm_config = step_config.get("config", {})
            
            provider = self.llm_manager.get_provider(provider_name)
            request = LLMRequest(
                messages=[{"role": "user", "content": query}],
                model=model_name,
                **llm_config
            )
            
            response = await provider.make_request(request)
            
            return StepResult(
                step_type="llm",
                step_name=f"{provider_name}:{model_name}",
                output=response.content,
                tokens_used=response.tokens_input + response.tokens_output,
                duration=response.duration_seconds,
                metadata={"provider": provider_name, "model": model_name}
            )
        
        else:
            raise ValueError(f"Unknown step configuration: {step_config}")

@dataclass
class RoutingResult:
    intent: IntentClassification
    route_config: RouteConfig
    steps: List[StepResult]
    final_output: str
    total_tokens: int
    total_duration: float
    success: bool = False
    error: Optional[str] = None
    fallback_used: bool = False
    fallback_result: Optional['RoutingResult'] = None

@dataclass
class StepResult:
    step_type: str  # "plugin" or "llm"
    step_name: str
    output: str
    tokens_used: int
    duration: float
    metadata: Dict[str, Any] = field(default_factory=dict)
```

## Integration with Cognition Pipeline

### Routed Cognition Plugin
```python
class IntelligentCognitionPlugin(ContractCompliantPlugin):
    """Cognition plugin that uses intelligent routing."""
    
    def __init__(self, routing_engine: RoutingEngine, live_block_manager: LiveBlockManager): # Added LiveBlockManager
        super().__init__()
        self.routing_engine = routing_engine
        self.live_block_manager = live_block_manager # Stored
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="intelligent_cognition",
            version="1.0.0",
            description="Intelligent routing-based cognition processing",
            author="LLM REPL Core",
            capabilities=["query_processing", "intelligent_routing"],
            dependencies=["routing_engine", "llm_manager"]
        )
    
    async def process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Process user input through intelligent routing."""
        # Start a live block for the entire cognition process
        cognition_block_id = "cognition_" + str(uuid.uuid4())
        self.live_block_manager.start_live_block(cognition_block_id, "cognition")

        tracking_id = self.start_operation_tracking("intelligent_routing")
        
        try:
            self.record_state_transition("active", "analyzing")
            
            user_query = input_data.get("content", "")
            
            # Route the query intelligently - this will create its own live sub-blocks
            routing_result = await self.routing_engine.route_query(user_query, context)
            
            # Aggregate metrics from routing steps
            total_cognition_tokens = routing_result.total_tokens
            total_cognition_duration = routing_result.total_duration

            # Update the live cognition block with aggregated metrics
            self.live_block_manager.update_live_block(
                cognition_block_id,
                content_chunk="", # No new content, just updating metadata
                tokens_delta=total_cognition_tokens,
                metadata={
                    "total_wall_time_seconds": total_cognition_duration,
                    "total_tokens_in": total_cognition_tokens # Assuming total_tokens is input tokens for now
                }
            )

            self.record_state_transition("analyzing", "completed")
            
            return {
                "content": routing_result.final_output,
                "sub_blocks": [], # Sub-blocks are managed by LiveBlockManager now
                "metadata": {
                    "intent": routing_result.intent.primary_intent.value,
                    "confidence": routing_result.intent.confidence,
                    "route_used": routing_result.route_config.description,
                    "total_steps": len(routing_result.steps),
                    "fallback_used": routing_result.fallback_used,
                    "aggregated_tokens": total_cognition_tokens,
                    "aggregated_duration": total_cognition_duration
                }
            }
            
        except Exception as e:
            self._transparency.error_occurred = True
            self._transparency.error_message = str(e)
            self.record_state_transition("analyzing", "error")
            # Mark the live cognition block as errored
            self.live_block_manager.update_live_block(
                cognition_block_id,
                content_chunk=f"Error: {str(e)}",
                metadata={"status": "error"}
            )
            raise
        
        finally:
            self.end_operation_tracking(tracking_id)
            # Complete the live cognition block (it will be inscribed by TurnOrchestrator)
            # The actual inscription happens when TurnOrchestrator calls complete_live_block
            pass
```

## Performance Optimization

### Caching and Optimization
```python
class RoutingOptimizer:
    """Optimizes routing performance and accuracy."""
    
    def __init__(self):
        self.route_performance: Dict[str, List[float]] = {}
        self.intent_accuracy: Dict[str, float] = {}
    
    def record_route_performance(self, route_id: str, duration: float,
                               user_satisfaction: float) -> None:
        """Record performance metrics for route optimization."""
        if route_id not in self.route_performance:
            self.route_performance[route_id] = []
        
        self.route_performance[route_id].append(duration)
        # Update satisfaction metrics
    
    def get_optimal_route_variant(self, intent: IntentCategory,
                                constraints: Dict[str, Any]) -> Optional[RouteConfig]:
        """Get optimized route variant based on performance data."""
        # Analyze performance history and suggest optimizations
        pass
    
    def analyze_routing_patterns(self) -> Dict[str, Any]:
        """Analyze routing patterns for optimization insights."""
        return {
            "most_used_intents": self._get_intent_usage_stats(),
            "performance_bottlenecks": self._identify_slow_routes(),
            "accuracy_issues": self._identify_misclassifications(),
            "optimization_recommendations": self._generate_recommendations()
        }
```

## Testing Strategy

### Unit Tests
- [ ] Intent classification accuracy across query types
- [ ] Route configuration loading and validation
- [ ] Routing engine step execution
- [ ] Fallback mechanism functionality
- [ ] **Live sub-block creation, update, and completion within the RoutingEngine.**
- [ ] **Aggregation of metrics from routing steps in `IntelligentCognitionPlugin`.**

### Integration Tests
- [ ] End-to-end routing through cognition pipeline
- [ ] Multi-step routing with plugin and LLM coordination
- [ ] Error handling and fallback route execution
- [ ] Performance optimization and caching
- [ ] **Visual verification of live routing sub-blocks in the UI.**
- [ ] **Accuracy of aggregated wall times and token counts on the Cognition Block.**

### Manual Testing
- [ ] Various query types and routing accuracy
- [ ] Route customization and user preferences
- [ ] Performance under different load conditions
- [ ] Routing transparency and explainability
- [ ] **Observe live updates of routing steps and their metrics.**
- [ ] **Verify correct inscription of Cognition Blocks with aggregated data.**

## Documentation Updates

- [ ] Intelligent routing architecture guide
- [ ] Intent classification and route configuration documentation
- [ ] Plugin integration guide for routing
- [ ] Performance optimization and monitoring guide
- [ ] **Guide on transparent routing and live sub-block visualization.**

## Completion

### Final Status
- [ ] Intelligent routing replaces hardcoded cognition processing
- [ ] Intent classification accurately routes different query types
- [ ] Route registry supports configurable processing paths
- [ ] Routing decisions are transparent and explainable
- [ ] Performance is optimized for real-time operation
- [ ] **Live sub-blocks for routing steps are displayed and managed.**
- [ ] **Aggregated metrics from routing steps are transparently presented on the Cognition Block.**

### Follow-up Items
- [ ] Advanced multi-intent query handling
- [ ] Machine learning-based routing optimization
- [ ] User feedback integration for routing improvement
- [ ] Cross-session routing pattern analysis
- [ ] **Refinement of visual indicators for nested live blocks.**

---

*This ledger tracks the implementation of the Intelligent Router system that transforms V3-minimal from uniform processing to dynamic, intent-based routing for optimal task handling, with a critical focus on transparent live updates and robust timeline inscription.*