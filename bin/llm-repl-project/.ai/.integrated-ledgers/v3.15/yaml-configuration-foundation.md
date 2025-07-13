# YAML Configuration Foundation

**Branch:** feat/yaml-configuration-foundation
**Summary:** Establish comprehensive YAML configuration system to eliminate hardcoded values and enable fine-tuning without code changes.
**Status:** Planning
**Created:** 2025-07-11
**Updated:** 2025-07-11

## Context

### Problem Statement
V3-minimal has configuration scattered across multiple systems with hardcoded values throughout the codebase, making fine-tuning require code changes instead of simple configuration edits.

**Current State**:
- Animation speeds hardcoded in `live_blocks.py` (lines 87, 95, 103)
- Theme colors hardcoded in `config.py` (lines 176-231)
- Widget dimensions hardcoded in CSS strings
- Mock scenario timing scattered throughout simulation code
- Display formatting constants embedded in widget code

**Impact**: Every UX tweak requires code modification, testing, and deployment.

### Success Criteria
- [ ] All tunable values moved to YAML configuration
- [ ] Hot-reload configuration without restart
- [ ] Validation of YAML configuration on load
- [ ] Default fallbacks for missing configuration
- [ ] Clear configuration schema documentation

### Acceptance Criteria
- [ ] Users can adjust animation speeds via YAML edit
- [ ] Theme customization through configuration file
- [ ] Widget sizing and spacing configurable
- [ ] Mock scenario timing adjustable for demos
- [ ] Configuration validation prevents invalid values

## User-Visible Behaviors

When this ledger is complete, users will see:

- **Configuration changes take effect without code modification**
- **Invalid YAML configuration shows clear error messages**
- **Default configuration file auto-generated if missing**
- **Hot-reload of configuration during development**
- **Schema validation prevents broken configurations**

## Technical Approach

### Configuration Schema Design

```yaml
# config.yaml - Complete V3-minimal configuration
app:
  title: "LLM REPL V3-minimal"
  subtitle: "Sacred Timeline • Elegant Typography"
  default_theme: "nord"
  
animation:
  fps:
    production: 60
    development: 120
    testing: 1000
  typewriter_speeds:
    initial: 1500
    progress: 2000
    completion: 2500
    summary: 1800
  transitions:
    live_to_inscribed: 0.3
    progress_bar: 0.2
    token_counter: 0.5

themes:
  nord:
    name: "Nord"
    description: "arctic minimalism with frost blue accents"
    primary: "#88c0d0"
    secondary: "#b48ead"
    accent: "#81a1c1"
    warning: "#ebcb8b"
    error: "#bf616a"
    success: "#a3be8c"
    dark: true
  # ... other themes

ui:
  timeline:
    margin_bottom: 1
    padding: [0, 1]
    max_content_preview: 50
  widgets:
    live_block:
      border_radius: "round"
      padding: 1
      min_height: 0
    timeline_block:
      margin_bottom: 1
      padding: [0, 1]
  
mock_scenarios:
  cognition:
    route_query:
      time_range: [0.3, 0.8]
      tokens_in_range: [5, 15]
      tokens_out_range: [1, 5]
    call_tool:
      time_range: [1.5, 3.0]
      tokens_in_range: [10, 20]
      tokens_out_range: [1000, 1500]
    format_output:
      time_range: [0.8, 1.5]
      tokens_in_range: [400, 600]
      tokens_out_range: [200, 300]

dev:
  hot_reload: true
  validation: strict
  auto_save_theme: true
```

### Implementation Plan

#### Phase 1: Configuration Infrastructure
1. **Enhanced ConfigLoader** with validation and hot-reload
2. **Configuration Schema** with type checking
3. **Default Configuration Generator** for missing files
4. **Environment-based Configuration** (dev/prod/test)

#### Phase 2: Animation Configuration Migration
1. **Extract animation constants** from `live_blocks.py`
2. **Centralize typewriter speeds** from scattered locations
3. **Transition timing configuration** for state changes
4. **FPS settings** for different environments

#### Phase 3: UI Configuration Migration
1. **Widget dimensions** from CSS to YAML
2. **Theme system** enhancement with YAML themes
3. **Timeline display settings** consolidation
4. **Content formatting** configuration

#### Phase 4: Mock Scenario Configuration
1. **Timing ranges** for realistic simulation
2. **Token count ranges** for different scenario types
3. **Scenario catalog** with configurable parameters
4. **Demo mode settings** for presentations

## Dependencies
- PyYAML for configuration parsing
- Pydantic for configuration validation
- Watchdog for file change detection (hot-reload)

## Testing Strategy

### Unit Tests
- [ ] Configuration loading and validation
- [ ] Default value fallbacks
- [ ] Schema validation edge cases
- [ ] Hot-reload functionality

### Integration Tests
- [ ] Animation speed changes via configuration
- [ ] Theme switching through YAML
- [ ] Widget sizing configuration
- [ ] Mock scenario timing adjustments

### Manual Testing
- [ ] Configuration file editing workflow
- [ ] Invalid configuration error handling
- [ ] Hot-reload during application running
- [ ] Performance impact of configuration changes

## Migration Strategy

### Step 1: Infrastructure Setup
- Implement enhanced `ConfigLoader` with validation
- Add configuration schema with Pydantic models
- Create default configuration generator

### Step 2: Animation Migration
- Extract hardcoded animation values to YAML
- Update `AnimationConfig` to load from enhanced system
- Remove hardcoded timing from mock scenarios

### Step 3: UI Configuration
- Move widget CSS constants to YAML
- Enhance theme system with YAML-based themes
- Centralize UI dimension and spacing settings

### Step 4: Validation and Polish
- Add comprehensive configuration validation
- Implement hot-reload for development
- Create configuration documentation

## Technical Implementation

### Enhanced ConfigLoader
```python
from pydantic import BaseModel, ValidationError
from typing import Dict, Any, Optional
import yaml
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AppConfig(BaseModel):
    title: str = "LLM REPL V3-minimal"
    subtitle: str = "Sacred Timeline • Elegant Typography"
    default_theme: str = "nord"

class AnimationConfig(BaseModel):
    fps: Dict[str, int] = {
        "production": 60,
        "development": 120, 
        "testing": 1000
    }
    typewriter_speeds: Dict[str, int] = {
        "initial": 1500,
        "progress": 2000,
        "completion": 2500,
        "summary": 1800
    }
    transitions: Dict[str, float] = {
        "live_to_inscribed": 0.3,
        "progress_bar": 0.2,
        "token_counter": 0.5
    }

class V3Config(BaseModel):
    app: AppConfig = AppConfig()
    animation: AnimationConfig = AnimationConfig()
    # ... other sections

class EnhancedConfigLoader:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self._find_config_file()
        self.config: V3Config = V3Config()
        self._observers: List[Observer] = []
        
    def load_config(self) -> V3Config:
        """Load and validate configuration from YAML file"""
        if not self.config_path or not self.config_path.exists():
            self._generate_default_config()
            
        try:
            with open(self.config_path, 'r') as f:
                yaml_data = yaml.safe_load(f) or {}
            self.config = V3Config(**yaml_data)
            return self.config
        except ValidationError as e:
            raise ConfigurationError(f"Invalid configuration: {e}")
        except yaml.YAMLError as e:
            raise ConfigurationError(f"YAML parsing error: {e}")
    
    def enable_hot_reload(self, callback: Callable[[V3Config], None]):
        """Enable hot-reload of configuration changes"""
        handler = ConfigFileHandler(self, callback)
        observer = Observer()
        observer.schedule(handler, str(self.config_path.parent), recursive=False)
        observer.start()
        self._observers.append(observer)
```

### Configuration Usage Pattern
```python
# Before: Hardcoded values
class LiveBlock:
    async def animate_tokens(self, duration_seconds: float = 0.5):
        # Hardcoded timing
        
# After: Configuration-driven
class LiveBlock:
    async def animate_tokens(self, duration_seconds: Optional[float] = None):
        if duration_seconds is None:
            duration_seconds = config.animation.transitions.token_counter
```

## Risk Assessment

### Low Risk
- Adding new configuration infrastructure (no existing code changes)
- Default value fallbacks (maintains current behavior)

### Medium Risk  
- Migrating hardcoded animation values (timing-sensitive)
- Theme system changes (visual consistency)

### High Risk
- Widget CSS to YAML migration (layout changes)
- Hot-reload implementation (could affect stability)

## Completion Criteria

### Technical Requirements
- [ ] All hardcoded values identified and migrated
- [ ] Configuration validation prevents invalid states
- [ ] Hot-reload working for development workflow
- [ ] Performance impact minimal (< 10ms config load)

### User Experience
- [ ] Configuration changes visible immediately
- [ ] Clear error messages for invalid configuration
- [ ] Default configuration works out-of-box
- [ ] Documentation for all configuration options

### Testing Coverage
- [ ] 90%+ test coverage for configuration code
- [ ] Integration tests for all migrated values
- [ ] Performance benchmarks for configuration loading
- [ ] Error handling tests for invalid configurations

---

*This ledger establishes the foundation for eliminating hardcoded values and enabling configuration-driven fine-tuning throughout V3-minimal.*