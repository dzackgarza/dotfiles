# Unused Code Removal

**Branch:** feat/unused-code-removal
**Summary:** Remove unused InputProcessor and consolidate redundant demo files to reduce codebase complexity and eliminate conflicting code paths.
**Status:** Planning
**Created:** 2025-07-11
**Updated:** 2025-07-11

## Context

### Problem Statement
V3-minimal contains unused code paths and redundant implementations that create maintenance overhead and confusion about which systems are active.

**Identified Unused Code**:
1. **InputProcessor** (`input_processor.py`) - completely unused
2. **Redundant demo files** - 7 demos with overlapping functionality
3. **Deprecated imports** - references to removed code
4. **Dead configuration paths** - unused config options

**Evidence of Non-Usage**:
```python
# main.py:47 - InputProcessor created but never used
self.input_processor = InputProcessor(timeline, self.response_generator)

# Only AsyncInputProcessor actually used:
# main.py:179 - await self.async_input_processor.process_user_input_async(event.text)
```

### Success Criteria
- [ ] Unused InputProcessor completely removed
- [ ] Demo files consolidated to 2-3 canonical examples
- [ ] No dead imports or references remain
- [ ] Codebase size reduced by 15-20%
- [ ] Clear separation between active and legacy code

### Acceptance Criteria  
- [ ] Application functions identically after removal
- [ ] No broken imports or missing references
- [ ] Test suite passes without modification
- [ ] Documentation updated to reflect active code paths
- [ ] Code coverage improves due to smaller surface area

## User-Visible Behaviors

When this ledger is complete, users will see:

- **No functional changes** - application behavior identical
- **Cleaner demo organization** with focused examples
- **Faster test execution** due to reduced test surface
- **Clearer codebase** for new developers
- **Reduced maintenance burden** for future changes

## Technical Approach

### Unused Code Audit

#### InputProcessor Analysis
**File**: `src/core/input_processor.py` (227 lines)
**Usage Analysis**:
- Created in `main.py:47` but never called
- Duplicate implementation of `AsyncInputProcessor` functionality
- Nearly identical cognition logic (lines 105-213)

**Safe to Remove**: ✅ - No references found in active code paths

#### Demo File Analysis
**Current Demo Files** (7 total):
```
src/demos/
├── cognition_ux_polish_demo.py     # 200+ lines - Cognition pipeline demo
├── live_streaming_demo.py          # 150+ lines - Live block streaming
├── live_updates_demo.py            # 180+ lines - Real-time updates  
├── simple_ux_polish_demo.py        # 120+ lines - Basic UX demo
├── live_block_demo.py              # 160+ lines - Live block showcase
├── scenario_showcase.py            # 140+ lines - Multiple scenarios
└── static_behavior_proof.py        # 100+ lines - Static behavior test
```

**Overlap Analysis**:
- `cognition_ux_polish_demo.py` + `simple_ux_polish_demo.py` - redundant UX demos
- `live_streaming_demo.py` + `live_updates_demo.py` + `live_block_demo.py` - overlapping live block demos
- `scenario_showcase.py` - duplicates functionality from other demos

**Consolidation Plan**:
- **Keep**: `live_streaming_demo.py` (most comprehensive live demo)
- **Keep**: `static_behavior_proof.py` (unique testing functionality)  
- **Keep**: `cognition_ux_polish_demo.py` (most mature cognition demo)
- **Remove**: 4 redundant demo files

### Implementation Plan

#### Phase 1: InputProcessor Removal

**Step 1: Identify All References**
```bash
# Search for InputProcessor usage
grep -r "InputProcessor" src/
grep -r "input_processor" src/
```

**Step 2: Remove from main.py**
```python
# REMOVE from main.py line 12:
from .core import InputProcessor, ResponseGenerator

# CHANGE to:
from .core import ResponseGenerator

# REMOVE from main.py line 47:
self.input_processor = InputProcessor(timeline, self.response_generator)
```

**Step 3: Delete InputProcessor File**
```bash
rm src/core/input_processor.py
```

**Step 4: Update __init__.py**
```python
# REMOVE from src/core/__init__.py:
from .input_processor import InputProcessor

# Keep only:
from .async_input_processor import AsyncInputProcessor
from .response_generator import ResponseGenerator
```

#### Phase 2: Demo Consolidation

**Files to Remove**:
1. `src/demos/simple_ux_polish_demo.py` - functionality covered by `cognition_ux_polish_demo.py`
2. `src/demos/live_updates_demo.py` - functionality covered by `live_streaming_demo.py`
3. `src/demos/live_block_demo.py` - functionality covered by `live_streaming_demo.py`
4. `src/demos/scenario_showcase.py` - functionality covered by other demos

**Demo Preservation Strategy**:
```python
# Keep best features from removed demos in remaining ones
# live_streaming_demo.py - enhance with features from removed live demos
# cognition_ux_polish_demo.py - enhance with features from simple_ux_polish_demo.py
```

#### Phase 3: Import Cleanup

**Update src/demos/__init__.py**:
```python
# Before: 7 demo imports
from .cognition_ux_polish_demo import CognitionUXPolishDemo
from .live_streaming_demo import LiveStreamingDemo
from .live_updates_demo import LiveUpdatesDemo
from .simple_ux_polish_demo import SimpleUXPolishDemo
from .live_block_demo import LiveBlockDemo
from .scenario_showcase import ScenarioShowcase
from .static_behavior_proof import StaticBehaviorProof

# After: 3 demo imports
from .cognition_ux_polish_demo import CognitionUXPolishDemo
from .live_streaming_demo import LiveStreamingDemo  
from .static_behavior_proof import StaticBehaviorProof
```

### Testing Strategy

#### Pre-Removal Testing
```python
class TestCodeRemovalSafety:
    def test_input_processor_truly_unused(self):
        """Verify InputProcessor has no active references"""
        # Static analysis to find any usage
        
    def test_demo_functionality_preservation(self):
        """Verify remaining demos cover all functionality"""
        # Test key features from demos being removed
        
    def test_current_functionality_baseline(self):
        """Establish baseline behavior before removal"""
        # Full functional test suite
```

#### Post-Removal Validation
```python
class TestCodeRemovalValidation:
    def test_no_broken_imports(self):
        """Verify no import errors after removal"""
        
    def test_application_functionality_unchanged(self):
        """Verify app behavior identical to baseline"""
        
    def test_remaining_demos_functional(self):
        """Verify remaining demos work correctly"""
```

### Migration Checklist

#### Pre-Removal Preparation
- [ ] Full test suite run to establish baseline
- [ ] Static analysis to confirm InputProcessor unused
- [ ] Demo functionality mapping to ensure no loss
- [ ] Documentation of removed code for future reference

#### Removal Process
- [ ] Remove InputProcessor from imports
- [ ] Delete InputProcessor file
- [ ] Remove redundant demo files  
- [ ] Update __init__.py files
- [ ] Clean up demo imports

#### Post-Removal Validation
- [ ] Full test suite run (must match baseline)
- [ ] Import validation (no broken imports)
- [ ] Demo functionality verification
- [ ] Code coverage analysis (should improve)

### Specific File Changes

#### main.py
```python
# Line 12: REMOVE InputProcessor import
# Line 47: REMOVE input_processor creation

# Before:
from .core import InputProcessor, ResponseGenerator
self.input_processor = InputProcessor(timeline, self.response_generator)

# After:  
from .core import ResponseGenerator
# (removed line)
```

#### src/core/__init__.py
```python
# REMOVE:
from .input_processor import InputProcessor

# KEEP:
from .async_input_processor import AsyncInputProcessor
from .response_generator import ResponseGenerator
```

#### src/demos/__init__.py
```python
# REMOVE 4 imports, KEEP 3:
from .cognition_ux_polish_demo import CognitionUXPolishDemo
from .live_streaming_demo import LiveStreamingDemo
from .static_behavior_proof import StaticBehaviorProof
```

### Risk Assessment

#### Zero Risk Changes
- Removing InputProcessor (confirmed unused)
- Removing redundant demo files (no production impact)

#### Low Risk Changes
- Import cleanup (static analysis confirms safety)
- Demo consolidation (preserves all functionality)

#### Validation Requirements
- [ ] No import errors after changes
- [ ] Test suite 100% pass rate maintained
- [ ] Application startup successful
- [ ] Demo functionality preserved

### Metrics and Validation

#### Code Reduction Metrics
- **Lines of Code**: Expect 15-20% reduction
- **File Count**: 7 demos → 3 demos (57% reduction)
- **Import Complexity**: Reduced import statements
- **Test Surface**: Smaller test matrix

#### Quality Metrics  
- **Code Coverage**: Should improve (smaller denominator)
- **Cyclomatic Complexity**: Reduced complexity
- **Maintenance Burden**: Fewer files to maintain

## Completion Criteria

### Technical Requirements
- [ ] Zero references to InputProcessor in codebase
- [ ] Demo count reduced from 7 to 3 files
- [ ] No broken imports or missing references
- [ ] All tests pass after removal

### Functional Requirements
- [ ] Application behavior unchanged
- [ ] Remaining demos cover all previous functionality
- [ ] No regression in user-visible features
- [ ] Documentation updated for active code paths

### Quality Requirements
- [ ] Code coverage maintained or improved
- [ ] Static analysis shows no issues
- [ ] Performance impact neutral or positive
- [ ] Maintenance burden measurably reduced

---

*This ledger removes architectural dead weight and eliminates confusion between active and inactive code paths.*