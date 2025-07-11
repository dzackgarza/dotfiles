# Contract Enforcement System

**Branch:** feat/contract-enforcement-system
**Summary:** Implement strict plugin contract enforcement to ensure all plugins meet transparency requirements, preventing architectural violations and maintaining Sacred Timeline integrity.
**Status:** Planning
**Created:** 2025-07-10
**Updated:** 2025-07-10

## Context

### Problem Statement
V3-minimal has **NO CONTRACT ENFORCEMENT** for plugins, violating the Sacred Timeline principle that "all plugins must adhere to a strict contract enforced by the Plugin Validator." Without contracts, there's no guarantee that plugins provide transparency metadata (timers, tokens, state), making the timeline opaque instead of transparent. This breaks the core philosophy of radical transparency in AI processing.

### Success Criteria
- [ ] All plugins must implement mandatory transparency contracts
- [ ] Contract violations are detected and prevented at runtime
- [ ] Timeline transparency is guaranteed for all operations
- [ ] Plugin development follows clear, enforceable guidelines
- [ ] System fails fast when contracts are violated

### Acceptance Criteria
- [ ] Plugins without proper contracts cannot be registered
- [ ] Missing transparency metadata (timers, tokens) causes registration failure
- [ ] Contract validation happens both at registration and runtime
- [ ] Clear error messages guide plugin developers
- [ ] Existing plugins must be retrofitted to meet contracts

## Technical Approach

### Architecture Changes
1. **Plugin Contracts**: Formal interface definitions with transparency requirements
2. **Contract Validator**: Runtime validation of contract compliance
3. **Transparency Metadata**: Mandatory timing, token, and state tracking
4. **Enforcement Engine**: Prevents non-compliant plugins from operating
5. **Development Tools**: Contract checking and plugin scaffolding

### Implementation Plan
1. **Phase 1: Planning** - Review and plan implementation
2. **Phase 2: Implementation** - Core development work
3. **Phase 3: Testing** - Testing and validation
4. **Phase 4: UX Polish** - Final polish and user experience improvements
5. **Phase 5: Integration** - Integrate ledger into the main system

### Dependencies
- Plugin Validator System (enforces contracts during registration)
- Plugin Architecture Foundation (base plugin system to retrofit)
- LLM Integration Foundation (real token tracking for contracts)

### Risks & Mitigations
- **Risk 1**: Existing plugins may not comply with new contracts
  - *Mitigation*: Gradual migration with compatibility layer and clear upgrade path
- **Risk 2**: Contract enforcement may be too strict, blocking valid plugins
  - *Mitigation*: Configurable validation levels, clear documentation, good error messages
- **Risk 3**: Performance overhead from constant contract checking
  - *Mitigation*: Efficient validation, caching, opt-out for development mode

## Progress Log

### 2025-07-10 - Initial Planning
- Identified complete lack of contract enforcement in V3-minimal
- Analyzed Sacred Timeline transparency requirements
- Designed contract interface and validation system
- Created enforcement strategy for existing and new plugins

## Technical Decisions

### Decision 1: Contract Definition Approach
**Context**: Need formal way to specify plugin transparency requirements  
**Options**: Interface protocols, abstract base classes, schema validation, decorators  
**Decision**: Protocol-based contracts with runtime validation schemas  
**Reasoning**: Type safety with runtime flexibility, clear contract specification  
**Consequences**: Strong contracts but requires both compile-time and runtime validation

### Decision 2: Enforcement Strictness Level
**Context**: Balance between strict compliance and development flexibility  
**Options**: Always strict, configurable levels, development vs production modes  
**Decision**: Configurable strictness with strict production defaults  
**Reasoning**: Developer productivity during development, strict compliance in production  
**Consequences**: More complex validation logic but better developer experience

### Decision 3: Transparency Metadata Requirements
**Context**: Define exactly what transparency data all plugins must provide  
**Options**: Minimal requirements, comprehensive tracking, configurable requirements  
**Decision**: Comprehensive transparency with minimal opt-out exceptions  
**Reasoning**: Sacred Timeline requires radical transparency for all operations  
**Consequences**: Higher plugin development overhead but guaranteed transparency

## Plugin Contract Definition

### Core Transparency Contract
```python
from typing import Protocol, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TransparencyLevel(Enum):
    MINIMAL = "minimal"      # Basic timing only
    STANDARD = "standard"    # Timing + tokens
    COMPREHENSIVE = "comprehensive"  # Full metadata

@dataclass
class TransparencyMetadata:
    """Mandatory transparency data all plugins must provide."""
    
    # Timing Requirements
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    
    # Token Tracking (for LLM-using plugins)
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    token_provider: Optional[str] = None
    
    # State Tracking
    plugin_state: str = "unknown"
    state_transitions: List[str] = field(default_factory=list)
    
    # Processing Metadata
    model_used: Optional[str] = None
    provider_used: Optional[str] = None
    processing_mode: Optional[str] = None
    
    # Error Information
    error_occurred: bool = False
    error_message: Optional[str] = None
    error_recovery_attempted: bool = False

class PluginTransparencyContract(Protocol):
    """Contract that all plugins must implement for transparency."""
    
    def get_transparency_metadata(self) -> TransparencyMetadata:
        """Return current transparency metadata."""
        ...
    
    def start_operation_tracking(self, operation_name: str) -> str:
        """Start tracking an operation, return tracking ID."""
        ...
    
    def end_operation_tracking(self, tracking_id: str) -> TransparencyMetadata:
        """End tracking and return final metadata."""
        ...
    
    def add_token_usage(self, input_tokens: int, output_tokens: int, 
                       provider: str, model: str) -> None:
        """Record token usage for transparency."""
        ...
    
    def record_state_transition(self, from_state: str, to_state: str) -> None:
        """Record state changes for transparency."""
        ...
    
    def get_transparency_level(self) -> TransparencyLevel:
        """Return the transparency level this plugin provides."""
        ...

class PluginLifecycleContract(Protocol):
    """Contract for plugin lifecycle management."""
    
    async def validate_prerequisites(self) -> bool:
        """Validate that plugin can operate (dependencies, config, etc.)."""
        ...
    
    async def initialize_with_validation(self, config: Dict[str, Any]) -> bool:
        """Initialize plugin with contract validation."""
        ...
    
    async def shutdown_gracefully(self, timeout_seconds: float = 30.0) -> bool:
        """Graceful shutdown with cleanup."""
        ...
    
    def get_health_status(self) -> Dict[str, Any]:
        """Return current health/status for monitoring."""
        ...
```

### Contract Validation Schema
```python
@dataclass
class ContractValidationResult:
    is_valid: bool
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    transparency_score: float = 0.0  # 0.0 to 1.0

class ContractValidator:
    """Validates plugin contract compliance."""
    
    def __init__(self, strictness: TransparencyLevel = TransparencyLevel.STANDARD):
        self.strictness = strictness
        self.required_methods = self._get_required_methods()
    
    def validate_plugin_contract(self, plugin: Any) -> ContractValidationResult:
        """Validate that a plugin meets contract requirements."""
        result = ContractValidationResult(is_valid=True)
        
        # Check protocol compliance
        if not isinstance(plugin, PluginTransparencyContract):
            result.is_valid = False
            result.violations.append(
                f"Plugin {plugin.__class__.__name__} does not implement PluginTransparencyContract"
            )
        
        # Check lifecycle contract
        if not isinstance(plugin, PluginLifecycleContract):
            result.is_valid = False
            result.violations.append(
                f"Plugin {plugin.__class__.__name__} does not implement PluginLifecycleContract"
            )
        
        # Validate transparency metadata
        transparency_result = self._validate_transparency(plugin)
        result.violations.extend(transparency_result.violations)
        result.warnings.extend(transparency_result.warnings)
        result.transparency_score = transparency_result.transparency_score
        
        if transparency_result.violations:
            result.is_valid = False
        
        return result
    
    def _validate_transparency(self, plugin: Any) -> ContractValidationResult:
        """Validate transparency implementation."""
        result = ContractValidationResult(is_valid=True)
        
        try:
            metadata = plugin.get_transparency_metadata()
            transparency_level = plugin.get_transparency_level()
            
            # Check based on strictness level
            if self.strictness >= TransparencyLevel.MINIMAL:
                if not self._has_timing_data(metadata):
                    result.violations.append("Plugin missing timing data")
            
            if self.strictness >= TransparencyLevel.STANDARD:
                if not self._has_adequate_transparency(metadata):
                    result.violations.append("Plugin missing standard transparency data")
            
            if self.strictness >= TransparencyLevel.COMPREHENSIVE:
                if not self._has_comprehensive_transparency(metadata):
                    result.violations.append("Plugin missing comprehensive transparency data")
            
            # Calculate transparency score
            result.transparency_score = self._calculate_transparency_score(metadata)
            
        except Exception as e:
            result.violations.append(f"Error validating transparency: {e}")
            result.is_valid = False
        
        return result
```

## Contract-Compliant Plugin Base

### Enhanced BlockPlugin with Contracts
```python
class ContractCompliantPlugin(BlockPlugin, PluginTransparencyContract, PluginLifecycleContract):
    """Base plugin class that enforces contract compliance."""
    
    def __init__(self, plugin_id: str = None):
        super().__init__(plugin_id)
        self._transparency = TransparencyMetadata()
        self._operation_trackers: Dict[str, datetime] = {}
        self._contract_validator = ContractValidator()
    
    def get_transparency_metadata(self) -> TransparencyMetadata:
        """Return current transparency metadata."""
        return self._transparency
    
    def start_operation_tracking(self, operation_name: str) -> str:
        """Start tracking an operation."""
        tracking_id = f"{operation_name}_{uuid.uuid4().hex[:8]}"
        self._operation_trackers[tracking_id] = datetime.now()
        return tracking_id
    
    def end_operation_tracking(self, tracking_id: str) -> TransparencyMetadata:
        """End tracking and update metadata."""
        if tracking_id in self._operation_trackers:
            start_time = self._operation_trackers.pop(tracking_id)
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self._transparency.start_time = start_time
            self._transparency.end_time = end_time
            self._transparency.duration_seconds = duration
        
        return self._transparency
    
    def add_token_usage(self, input_tokens: int, output_tokens: int,
                       provider: str, model: str) -> None:
        """Record token usage."""
        self._transparency.tokens_input = (self._transparency.tokens_input or 0) + input_tokens
        self._transparency.tokens_output = (self._transparency.tokens_output or 0) + output_tokens
        self._transparency.token_provider = provider
        self._transparency.model_used = model
    
    def record_state_transition(self, from_state: str, to_state: str) -> None:
        """Record state transitions."""
        transition = f"{from_state} -> {to_state}"
        self._transparency.state_transitions.append(transition)
        self._transparency.plugin_state = to_state
    
    def get_transparency_level(self) -> TransparencyLevel:
        """Return transparency level - override in subclasses."""
        return TransparencyLevel.STANDARD
    
    async def validate_prerequisites(self) -> bool:
        """Validate plugin can operate."""
        # Default implementation - override in subclasses
        return True
    
    async def initialize_with_validation(self, config: Dict[str, Any]) -> bool:
        """Initialize with contract validation."""
        # Validate contract compliance
        validation_result = self._contract_validator.validate_plugin_contract(self)
        if not validation_result.is_valid:
            raise PluginContractViolation(
                f"Plugin {self.metadata.name} violates contract: {validation_result.violations}"
            )
        
        # Proceed with normal initialization
        return await self.initialize(config)
    
    def get_health_status(self) -> Dict[str, Any]:
        """Return plugin health status."""
        return {
            "plugin_id": self.plugin_id,
            "state": self.state.value,
            "last_activity": self._transparency.end_time,
            "error_status": self._transparency.error_occurred,
            "transparency_score": self._calculate_transparency_score()
        }
    
    def _calculate_transparency_score(self) -> float:
        """Calculate transparency score for this plugin."""
        score = 0.0
        max_score = 10.0
        
        # Timing data
        if self._transparency.duration_seconds is not None:
            score += 2.0
        
        # Token tracking
        if self._transparency.tokens_input is not None:
            score += 2.0
        if self._transparency.tokens_output is not None:
            score += 2.0
        
        # State tracking
        if self._transparency.state_transitions:
            score += 2.0
        
        # Provider information
        if self._transparency.model_used:
            score += 1.0
        if self._transparency.provider_used:
            score += 1.0
        
        return min(score / max_score, 1.0)
```

## Contract Enforcement Integration

### Enhanced Plugin Validator
```python
class ContractEnforcingValidator(PluginValidator):
    """Plugin validator that enforces contract compliance."""
    
    def __init__(self, strictness: TransparencyLevel = TransparencyLevel.STANDARD):
        super().__init__()
        self.contract_validator = ContractValidator(strictness)
    
    def validate_plugin_for_timeline(self, plugin: Any) -> bool:
        """Validate plugin including contract compliance."""
        # Base validation
        base_valid = super().validate_plugin_for_timeline(plugin)
        if not base_valid:
            return False
        
        # Contract validation
        contract_result = self.contract_validator.validate_plugin_contract(plugin)
        if not contract_result.is_valid:
            raise PluginContractViolation(
                f"Plugin contract violations: {contract_result.violations}"
            )
        
        # Log transparency score
        logger.info(f"Plugin {plugin.metadata.name} transparency score: "
                   f"{contract_result.transparency_score:.2f}")
        
        return True
    
    def get_plugin_transparency_report(self, plugin: Any) -> Dict[str, Any]:
        """Generate transparency compliance report."""
        contract_result = self.contract_validator.validate_plugin_contract(plugin)
        metadata = plugin.get_transparency_metadata()
        
        return {
            "plugin_name": plugin.metadata.name,
            "contract_compliance": contract_result.is_valid,
            "violations": contract_result.violations,
            "warnings": contract_result.warnings,
            "transparency_score": contract_result.transparency_score,
            "transparency_metadata": metadata
        }
```

## Development Tools

### Contract Checking CLI
```python
class ContractChecker:
    """CLI tool for checking plugin contract compliance."""
    
    def check_plugin_file(self, plugin_path: Path) -> ContractValidationResult:
        """Check a plugin file for contract compliance."""
        # Load plugin dynamically
        plugin_module = self._load_plugin_module(plugin_path)
        plugin_class = self._find_plugin_class(plugin_module)
        plugin_instance = plugin_class()
        
        # Validate contract
        validator = ContractValidator()
        return validator.validate_plugin_contract(plugin_instance)
    
    def generate_compliance_report(self, plugin_directory: Path) -> Dict[str, Any]:
        """Generate compliance report for all plugins in directory."""
        report = {
            "total_plugins": 0,
            "compliant_plugins": 0,
            "violations": [],
            "plugin_scores": {}
        }
        
        for plugin_file in plugin_directory.glob("*.py"):
            try:
                result = self.check_plugin_file(plugin_file)
                report["total_plugins"] += 1
                
                if result.is_valid:
                    report["compliant_plugins"] += 1
                else:
                    report["violations"].append({
                        "plugin": plugin_file.name,
                        "violations": result.violations
                    })
                
                report["plugin_scores"][plugin_file.name] = result.transparency_score
                
            except Exception as e:
                report["violations"].append({
                    "plugin": plugin_file.name,
                    "error": str(e)
                })
        
        return report
```

### Plugin Scaffolding Tool
```python
class PluginScaffolder:
    """Generate contract-compliant plugin templates."""
    
    def create_plugin_template(self, plugin_name: str, 
                             plugin_type: str = "basic") -> str:
        """Create a new plugin template with contracts."""
        template = f'''
from typing import Dict, Any
from src.plugins.base import ContractCompliantPlugin, TransparencyLevel
from src.plugins.contracts import PluginMetadata

class {plugin_name}Plugin(ContractCompliantPlugin):
    """Generated plugin template with contract compliance."""
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="{plugin_name.lower()}",
            version="1.0.0",
            description="TODO: Describe what this plugin does",
            author="TODO: Your name",
            capabilities=["TODO: List capabilities"]
        )
    
    def get_transparency_level(self) -> TransparencyLevel:
        return TransparencyLevel.STANDARD
    
    async def process(self, input_data: Any, context: Dict[str, Any]) -> Any:
        """Process input with transparency tracking."""
        # Start transparency tracking
        tracking_id = self.start_operation_tracking("process")
        
        try:
            # Record state transition
            self.record_state_transition("active", "processing")
            
            # TODO: Implement your processing logic here
            result = {{"processed": input_data}}
            
            # Record completion
            self.record_state_transition("processing", "completed")
            
            return result
            
        except Exception as e:
            self._transparency.error_occurred = True
            self._transparency.error_message = str(e)
            self.record_state_transition("processing", "error")
            raise
        
        finally:
            # End transparency tracking
            self.end_operation_tracking(tracking_id)
'''
        return template
```

## Testing Strategy

### Unit Tests
- [ ] Contract validation for various plugin types
- [ ] Transparency metadata tracking accuracy
- [ ] Contract enforcement blocking invalid plugins
- [ ] Plugin scaffolding template generation

### Integration Tests
- [ ] Contract-compliant plugins in full Sacred Timeline
- [ ] Plugin registration with contract enforcement
- [ ] Timeline transparency guarantee validation
- [ ] Error handling for contract violations

### Manual Testing
- [ ] Plugin development workflow with contracts
- [ ] Contract violation error messages and debugging
- [ ] Transparency report generation and analysis
- [ ] Performance impact of contract enforcement

## Documentation Updates

- [ ] Plugin contract specification and requirements
- [ ] Plugin development guide with contract examples
- [ ] Transparency requirements documentation
- [ ] Contract validation and debugging guide

## Migration Strategy

### Existing Plugin Retrofit
1. Audit all existing V3-minimal functionality for contract compliance
2. Create contract-compliant versions of hardcoded classes
3. Add transparency tracking to all plugin operations
4. Test contract enforcement with migrated plugins

### Gradual Enforcement
1. Start with warning-only mode for contract violations
2. Add comprehensive transparency tracking
3. Enable strict enforcement for new plugins
4. Migrate existing plugins to full compliance

## Completion

### Final Status
- [ ] All plugins implement mandatory transparency contracts
- [ ] Contract enforcement prevents non-compliant plugins
- [ ] Timeline transparency is guaranteed
- [ ] Plugin development tools support contract compliance
- [ ] Existing functionality migrated to contract-compliant plugins

### Follow-up Items
- [ ] Advanced contract specifications for specialized plugins
- [ ] Automated contract compliance testing in CI/CD
- [ ] Plugin marketplace with contract validation
- [ ] Runtime contract monitoring and alerting

---

*This ledger tracks the implementation of strict contract enforcement to ensure all plugins meet Sacred Timeline transparency requirements and architectural integrity.*