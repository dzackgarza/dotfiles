# Mock System Isolation

**Branch:** feat/mock-system-isolation
**Summary:** Isolate mock simulation code into dedicated submodule to separate testing infrastructure from production code paths.
**Status:** Planning
**Created:** 2025-07-11
**Updated:** 2025-07-11

## Context

### Problem Statement
Mock simulation code is embedded throughout production classes, creating confusion about which code is for testing vs production use, and making the real system harder to implement.

**Current Issues**:
- 400+ lines of mock simulation code in `live_blocks.py` 
- Mock scenarios mixed with production live block logic
- Complex `CognitionProgress` with threading for fake progress updates
- Simulation methods pollute the `LiveBlock` API surface
- Unclear separation between testing and production code

**Evidence of Mock Code Pollution**:
```python
# live_blocks.py - Production class polluted with mock methods
class LiveBlock:
    # Production methods
    def update_content(self, new_content: str) -> None: ...
    def add_sub_block(self, sub_block: "LiveBlock") -> None: ...
    
    # Mock methods mixed in
    async def start_mock_simulation(self, scenario: str = "default") -> None: ...
    async def _simulate_cognition_block(self) -> None: ...
    async def _simulate_assistant_response(self) -> None: ...
    # ... 8 more mock simulation methods
```

### Success Criteria
- [ ] Mock simulation code isolated in `src/mocks/` submodule
- [ ] Production classes contain only production logic
- [ ] Clear separation between testing and production APIs
- [ ] Mock scenarios configurable via YAML
- [ ] Tests use mock submodule instead of embedded mock methods

### Acceptance Criteria
- [ ] LiveBlock class contains only production methods
- [ ] Mock simulations available through dedicated API
- [ ] Existing tests continue to work with mock submodule
- [ ] Demo applications use mock API consistently
- [ ] Production code paths clearly identifiable

## User-Visible Behaviors

When this ledger is complete, users will see:

- **Cleaner production code** without testing artifacts
- **Dedicated mock API** for testing and demonstrations
- **Configurable mock scenarios** via YAML configuration
- **Clear separation** between real and simulated behavior
- **Faster production code** without mock overhead

## Technical Approach

### Mock Code Analysis

**Current Mock Methods in LiveBlock**:
```python
# 400+ lines of mock code to extract:
async def start_mock_simulation(self, scenario: str = "default") -> None
async def _run_mock_simulation(self, scenario: str) -> None
async def _simulate_cognition_block(self) -> None
async def _simulate_assistant_response(self) -> None  
async def _simulate_basic_block(self) -> None
async def _simulate_tool_execution(self) -> None
async def _simulate_route_analysis(self) -> None
async def _simulate_tool_selection(self) -> None
async def _simulate_response_generation(self) -> None
def stop_simulation(self) -> None
```

**Mock-Specific Data Structures**:
```python
# CognitionProgress - threading system for fake progress
class CognitionProgress:
    def _start_timer_updates(self) -> None:  # Background threading
    def get_status_line(self) -> str:        # Mock status display
```

### Target Architecture

#### Mock Submodule Structure
```
src/mocks/
├── __init__.py                    # Mock API exports
├── scenarios.py                   # Scenario definitions
├── simulation_engine.py           # Core simulation logic
├── cognition_simulator.py         # Cognition pipeline mocks
├── block_simulator.py             # Live block simulation
└── config/
    └── scenarios.yaml            # Configurable mock scenarios
```

#### Mock API Design
```python
# src/mocks/__init__.py - Clean mock API
from .simulation_engine import SimulationEngine
from .scenarios import MockScenario, ScenarioType
from .block_simulator import BlockSimulator

class MockAPI:
    """Clean API for mock simulations"""
    
    @staticmethod
    async def simulate_live_block(
        live_block: LiveBlock, 
        scenario: str = "default"
    ) -> None:
        """Simulate live block behavior using configured scenario"""
        simulator = BlockSimulator(live_block)
        await simulator.run_scenario(scenario)
    
    @staticmethod  
    async def simulate_cognition_pipeline(
        live_block: LiveBlock,
        steps: List[str] = None
    ) -> None:
        """Simulate multi-step cognition pipeline"""
        simulator = CognitionSimulator(live_block)
        await simulator.run_pipeline(steps)
```

### Implementation Plan

#### Phase 1: Mock Submodule Infrastructure

**Create Mock Configuration**:
```yaml
# src/mocks/config/scenarios.yaml
scenarios:
  default:
    type: "basic"
    duration_range: [0.1, 0.5]
    steps: 4
    
  cognition:
    type: "cognition_pipeline"
    steps:
      route_query:
        duration_range: [0.3, 0.8]
        tokens_in_range: [5, 15]
        tokens_out_range: [1, 5]
        model: "tinyllama-v2"
      call_tool:
        duration_range: [1.5, 3.0]
        tokens_in_range: [10, 20]
        tokens_out_range: [1000, 1500]
        model: "brave_web_search"
      format_output:
        duration_range: [0.8, 1.5]
        tokens_in_range: [400, 600]
        tokens_out_range: [200, 300]
        model: "mistral-7b-instruct"
        
  assistant_response:
    type: "response_generation"
    duration_range: [1.0, 3.0]
    streaming: true
    token_estimation: 5  # chars per token
```

**Core Simulation Engine**:
```python
# src/mocks/simulation_engine.py
from typing import Dict, Any, List
from dataclasses import dataclass
import yaml
import asyncio
import random

@dataclass
class MockScenario:
    name: str
    type: str
    config: Dict[str, Any]

class SimulationEngine:
    """Core engine for running mock scenarios"""
    
    def __init__(self):
        self.scenarios = self._load_scenarios()
    
    def _load_scenarios(self) -> Dict[str, MockScenario]:
        """Load scenarios from YAML configuration"""
        config_path = Path(__file__).parent / "config" / "scenarios.yaml"
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        scenarios = {}
        for name, scenario_config in config["scenarios"].items():
            scenarios[name] = MockScenario(
                name=name,
                type=scenario_config["type"],
                config=scenario_config
            )
        return scenarios
    
    async def run_scenario(
        self, 
        scenario_name: str, 
        target: Any,
        callbacks: Dict[str, Callable] = None
    ) -> None:
        """Run a mock scenario on target object"""
        scenario = self.scenarios[scenario_name]
        
        if scenario.type == "basic":
            await self._run_basic_scenario(scenario, target, callbacks)
        elif scenario.type == "cognition_pipeline":
            await self._run_cognition_scenario(scenario, target, callbacks)
        elif scenario.type == "response_generation":
            await self._run_response_scenario(scenario, target, callbacks)
```

#### Phase 2: LiveBlock Mock Extraction

**Clean Production LiveBlock**:
```python
# Cleaned src/core/live_blocks.py - LiveBlock class
class LiveBlock:
    """Production live block without mock simulation methods"""
    
    def __init__(self, role: str, initial_content: str = ""):
        self.id = str(uuid.uuid4())
        self.role = role
        self.state = BlockState.LIVE
        self.created_at = datetime.now()
        self.data = LiveBlockData(content=initial_content)
        self.update_callbacks: List[Callable] = []
        
        # Remove cognition progress threading for production
        # Only add if role is cognition AND in test/demo mode
        
    # Production methods only
    def update_content(self, new_content: str) -> None: ...
    def append_content(self, additional_content: str) -> None: ...
    def stream_content(self, target_content: str) -> None: ...
    async def stream_content_animated(self, target_content: str, chars_per_second: float = 50.0, replace: bool = False) -> None: ...
    # ... other production methods
    
    # NO MOCK METHODS - moved to mock submodule
```

**Mock Block Simulator**:
```python
# src/mocks/block_simulator.py
from src.core.live_blocks import LiveBlock, BlockState
from .simulation_engine import SimulationEngine

class BlockSimulator:
    """Handles mock simulation of LiveBlock behavior"""
    
    def __init__(self, live_block: LiveBlock):
        self.live_block = live_block
        self.engine = SimulationEngine()
    
    async def run_scenario(self, scenario_name: str) -> None:
        """Run mock scenario on the live block"""
        await self.engine.run_scenario(
            scenario_name,
            self.live_block,
            callbacks={
                'update_content': self.live_block.update_content,
                'update_progress': self.live_block.update_progress,
                'update_tokens': self.live_block.update_tokens,
                'add_sub_block': self.live_block.add_sub_block
            }
        )
```

#### Phase 3: Demo and Test Migration

**Update Demo Usage**:
```python
# Before: Embedded mock methods
await live_block.start_mock_simulation("cognition")

# After: Mock API
from src.mocks import MockAPI
await MockAPI.simulate_live_block(live_block, "cognition")
```

**Update Test Usage**:
```python
# Before: Direct mock method calls
class TestLiveBlocks:
    async def test_cognition_simulation(self):
        block = LiveBlock("cognition")
        await block.start_mock_simulation("cognition")
        
# After: Mock API usage
class TestLiveBlocks:
    async def test_cognition_simulation(self):
        block = LiveBlock("cognition")
        await MockAPI.simulate_live_block(block, "cognition")
```

### Testing Strategy

#### Mock Submodule Tests
```python
class TestMockSubmodule:
    def test_scenario_loading(self):
        """Verify scenarios load from YAML correctly"""
        
    async def test_simulation_engine(self):
        """Verify simulation engine runs scenarios"""
        
    async def test_block_simulator(self):
        """Verify block simulator integrates with live blocks"""
        
    def test_mock_api_interface(self):
        """Verify mock API provides clean interface"""
```

#### Integration Tests
```python
class TestMockIntegration:
    async def test_demo_mock_usage(self):
        """Verify demos work with mock API"""
        
    async def test_existing_tests_with_mock_api(self):
        """Verify existing tests work with mock submodule"""
        
    def test_production_code_clean(self):
        """Verify production classes contain no mock code"""
```

#### Migration Tests
```python
class TestMockMigration:
    async def test_behavior_identical_after_migration(self):
        """Verify mock behavior identical before/after migration"""
        
    def test_api_surface_reduced(self):
        """Verify LiveBlock API surface reduced appropriately"""
```

### Migration Checklist

#### Pre-Migration Preparation
- [ ] Audit all mock code in production classes
- [ ] Document current mock behavior for preservation
- [ ] Identify all usage of mock methods in tests/demos
- [ ] Create baseline behavior tests

#### Migration Process
- [ ] Create mock submodule infrastructure
- [ ] Implement mock API and simulation engine
- [ ] Extract mock methods from LiveBlock class
- [ ] Update demo applications to use mock API
- [ ] Update test suite to use mock API
- [ ] Remove mock methods from production classes

#### Post-Migration Validation
- [ ] All tests pass with mock API
- [ ] Demo applications work identically
- [ ] Production classes contain only production code
- [ ] Mock behavior identical to previous implementation

### Benefits Analysis

#### Code Quality Improvements
- **Separation of Concerns**: Production vs testing code clearly separated
- **API Surface Reduction**: LiveBlock class focused on production functionality
- **Maintainability**: Mock code easier to modify without affecting production
- **Performance**: Production code without mock overhead

#### Developer Experience
- **Clarity**: Clear distinction between real and simulated behavior
- **Configurability**: Mock scenarios easily configurable via YAML
- **Extensibility**: Easy to add new mock scenarios without code changes
- **Testing**: Dedicated mock API improves test organization

## Completion Criteria

### Technical Requirements
- [ ] Mock code completely isolated in `src/mocks/` submodule
- [ ] Production classes contain only production methods
- [ ] Mock API provides equivalent functionality to embedded methods
- [ ] Mock scenarios configurable via YAML

### Functional Requirements
- [ ] All existing tests pass with mock API
- [ ] Demo applications work identically
- [ ] Mock behavior identical to previous implementation
- [ ] New mock scenarios easily configurable

### Code Quality Requirements
- [ ] Production code paths clearly identifiable
- [ ] Mock API well-documented and easy to use
- [ ] Clear separation between testing and production concerns
- [ ] Reduced complexity in production classes

---

*This ledger isolates testing infrastructure from production code, improving clarity and maintainability while preserving all mock functionality.*