# Animation System Consolidation

**Branch:** feat/animation-system-consolidation
**Summary:** Eliminate AnimationRates compatibility wrapper and consolidate all animation timing to YAML-configurable AnimationClock system.
**Status:** Planning
**Created:** 2025-07-11
**Updated:** 2025-07-11

## Context

### Problem Statement
V3-minimal has conflicting animation systems with deprecated compatibility wrappers and hardcoded timing values scattered throughout the codebase.

**Current Issues**:
- `AnimationRates` deprecated wrapper still used in 3+ files
- Hardcoded timing in mock simulations (e.g., `await asyncio.sleep(0.1)`)
- Mixed usage: new code uses `AnimationClock`, old code uses `AnimationRates`
- Animation speeds hardcoded in `live_blocks.py` instead of configuration

**Files Affected**:
- `live_blocks.py:128` - `await AnimationRates.sleep(0.8)`
- `live_blocks.py:472` - `await AnimationRates.sleep(0.8)`
- `demos/cognition_ux_polish_demo.py` - Uses deprecated wrapper

### Success Criteria
- [ ] Single animation system using `AnimationClock`
- [ ] All timing values configurable via YAML
- [ ] Deprecated `AnimationRates` wrapper removed
- [ ] Consistent animation behavior across all components
- [ ] Performance optimization for high-FPS scenarios

### Acceptance Criteria
- [ ] No references to `AnimationRates` in codebase
- [ ] All animations use frame-based timing
- [ ] Animation speeds adjustable without code changes
- [ ] Test mode animations run at maximum speed
- [ ] Production animations smooth at 60fps

## User-Visible Behaviors

When this ledger is complete, users will see:

- **Consistent animation timing across all UI components**
- **Configurable animation speeds for different scenarios**
- **Smoother animations with frame-based timing**
- **Faster test execution with optimized animation speeds**
- **No animation stuttering or inconsistent timing**

## Technical Approach

### Current Animation Usage Audit

**Files Using AnimationRates (DEPRECATED)**:
```bash
# Search results for "AnimationRates"
src/core/live_blocks.py:114    # Compatibility wrapper definition
src/core/live_blocks.py:128    # await AnimationRates.sleep(0.8)
src/core/live_blocks.py:472    # await AnimationRates.sleep(0.8) 
src/core/live_blocks.py:547    # await AnimationRates.sleep(0.2)
src/core/live_blocks.py:577    # await AnimationRates.sleep(0.2)
src/demos/cognition_ux_polish_demo.py  # Multiple usages
```

**Files Using AnimationClock (CORRECT)**:
- `animation_clock.py` - Core implementation
- `live_block_widget.py` - Proper async usage
- Recent additions use frame-based timing

### Migration Strategy

#### Phase 1: Configuration Integration
```yaml
# config.yaml - Animation section
animation:
  clock:
    production_fps: 60
    development_fps: 120 
    testing_fps: 1000
  timing:
    # Standard animation durations (in seconds)
    quick: 0.1
    normal: 0.3
    slow: 0.8
    transition: 0.2
  scenarios:
    # Mock scenario timing ranges
    cognition_step: [0.1, 0.3]
    tool_execution: [0.8, 2.0]
    response_generation: [0.5, 1.5]
```

#### Phase 2: AnimationRates Replacement
Replace all `AnimationRates.sleep(duration)` with configured frame-based timing:

```python
# Before: Hardcoded sleep
await AnimationRates.sleep(0.8)

# After: Configured frame-based timing  
duration = config.animation.timing.slow  # 0.8 from YAML
await AnimationClock.animate_over_time(duration)
```

#### Phase 3: Mock Scenario Integration
```python
# Before: Hardcoded simulation timing
async def _simulate_tool_execution(self):
    self.update_content("🛠️ Executing tool...")
    await AnimationRates.sleep(0.8)  # Hardcoded
    
# After: Configured simulation timing
async def _simulate_tool_execution(self):
    self.update_content("🛠️ Executing tool...")
    timing = config.animation.scenarios.tool_execution
    duration = random.uniform(*timing)  # [0.8, 2.0] from YAML
    await AnimationClock.animate_over_time(duration)
```

### Implementation Plan

#### Step 1: Enhanced AnimationClock
```python
from src.config import config

class AnimationClock:
    """Global animation timing with YAML configuration integration"""
    
    @classmethod
    def configure_from_yaml(cls, animation_config: AnimationConfig):
        """Configure clock from YAML settings"""
        environment = os.getenv('ENVIRONMENT', 'production')
        fps_key = f"{environment}_fps"
        fps = animation_config.clock.get(fps_key, 60)
        cls.set_fps(fps)
    
    @classmethod 
    async def animate_duration(cls, duration_key: str):
        """Animate using configured duration from YAML"""
        duration = config.animation.timing.get(duration_key, 0.3)
        await cls.animate_over_time(duration)
    
    @classmethod
    async def animate_scenario(cls, scenario_key: str):
        """Animate using random duration from scenario range"""
        import random
        timing_range = config.animation.scenarios.get(scenario_key, [0.1, 0.5])
        duration = random.uniform(*timing_range)
        await cls.animate_over_time(duration)
```

#### Step 2: Systematic Migration

**File: `src/core/live_blocks.py`**
```python
# Lines to change:
# Line 128: await AnimationRates.sleep(0.8)
# Line 472: await AnimationRates.sleep(0.8)  
# Line 547: await AnimationRates.sleep(0.2)
# Line 577: await AnimationRates.sleep(0.2)

# Migration:
await AnimationClock.animate_duration('slow')      # 0.8s
await AnimationClock.animate_duration('slow')      # 0.8s  
await AnimationClock.animate_duration('transition') # 0.2s
await AnimationClock.animate_duration('transition') # 0.2s
```

**File: `src/demos/cognition_ux_polish_demo.py`**
```python
# Replace all AnimationRates usage with scenario-based timing:
await AnimationClock.animate_scenario('cognition_step')
await AnimationClock.animate_scenario('tool_execution')
await AnimationClock.animate_scenario('response_generation')
```

#### Step 3: Remove Deprecated Code
```python
# DELETE from live_blocks.py lines 114-133:
class AnimationRates:
    """DEPRECATED: Use AnimationClock instead. This is for backward compatibility only."""
    # ... entire class removal
```

### Testing Strategy

#### Unit Tests
```python
class TestAnimationSystemConsolidation:
    def test_animation_rates_removed(self):
        """Verify AnimationRates is completely removed"""
        # Search codebase for any AnimationRates references
        
    def test_animation_clock_yaml_integration(self):
        """Verify AnimationClock uses YAML configuration"""
        
    def test_scenario_based_timing(self):
        """Verify scenario timing uses configured ranges"""
        
    def test_environment_based_fps(self):
        """Verify FPS switches based on environment"""
```

#### Integration Tests
```python
class TestAnimationConsistency:
    async def test_live_block_animations_use_clock(self):
        """Verify live blocks use AnimationClock exclusively"""
        
    async def test_demo_animations_configurable(self):
        """Verify demo animations respect YAML timing"""
        
    async def test_mock_scenarios_timing_ranges(self):
        """Verify mock scenarios use configured timing ranges"""
```

#### Performance Tests
```python
class TestAnimationPerformance:
    async def test_high_fps_performance(self):
        """Verify high FPS doesn't degrade performance"""
        
    async def test_test_mode_speed(self):
        """Verify test mode runs animations at maximum speed"""
```

### Migration Checklist

#### Pre-Migration
- [ ] Audit all `AnimationRates` usage locations
- [ ] Document current timing behavior for comparison
- [ ] Create comprehensive test coverage for existing timing

#### Migration Steps
- [ ] Implement enhanced `AnimationClock` with YAML integration
- [ ] Add animation configuration to YAML schema
- [ ] Replace `AnimationRates.sleep()` calls systematically
- [ ] Update mock scenarios to use scenario-based timing
- [ ] Remove deprecated `AnimationRates` class

#### Post-Migration Validation
- [ ] Verify no `AnimationRates` references remain
- [ ] Test animation timing consistency
- [ ] Validate configuration-driven timing changes
- [ ] Performance benchmarks vs previous implementation

### Risk Assessment

#### Low Risk Changes
- Adding new `AnimationClock` methods (additive)
- YAML configuration addition (fallback to defaults)

#### Medium Risk Changes  
- Replacing `AnimationRates` calls (timing behavior change)
- Mock scenario timing modification (could affect demos)

#### High Risk Changes
- Removing `AnimationRates` class (breaking change if missed references)

### Error Handling

```python
class AnimationConfigurationError(Exception):
    """Raised when animation configuration is invalid"""
    pass

class AnimationClock:
    @classmethod
    async def animate_duration(cls, duration_key: str):
        """Animate with error handling for missing configuration"""
        try:
            duration = config.animation.timing[duration_key]
        except KeyError:
            logger.warning(f"Animation duration '{duration_key}' not configured, using default")
            duration = 0.3  # Safe default
        
        await cls.animate_over_time(duration)
```

## Completion Criteria

### Technical Requirements
- [ ] Zero references to `AnimationRates` in codebase
- [ ] All animations use `AnimationClock` exclusively  
- [ ] Animation timing configurable via YAML
- [ ] Performance maintained or improved vs previous system

### Behavioral Requirements
- [ ] Animation timing identical to previous behavior (default config)
- [ ] Test mode animations complete rapidly
- [ ] Production animations smooth and consistent
- [ ] Demo animations respect configured timing ranges

### Code Quality
- [ ] No deprecated animation code remains
- [ ] Clear separation between timing configuration and implementation
- [ ] Comprehensive test coverage for all timing scenarios
- [ ] Documentation for animation configuration options

---

*This ledger eliminates animation system conflicts and enables full configuration control over timing behavior.*