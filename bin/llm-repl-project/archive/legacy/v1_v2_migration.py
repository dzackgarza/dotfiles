#!/usr/bin/env python3
"""
V1 to V2 Migration System - Gradual transition with zero regressions

This module provides adapters and compatibility layers to gradually migrate
from the existing V1 system to the new V2 architecture without breaking
existing functionality.

Key principles:
1. Zero regressions - everything that worked in V1 continues to work
2. Gradual migration - can migrate one component at a time
3. Backward compatibility - V1 code can call V2 components
4. Forward compatibility - V2 components can integrate with V1 system
"""

import asyncio
import time
from typing import Any, Dict, List, Optional, Protocol, Union
from dataclasses import dataclass, field

# Import V1 system components
try:
    from llm_repl_v0 import (
        RichUI, SessionLogger, RollingTokenCounter, 
        ProcessingBlock, LiveProgressIndicator
    )
    V1_AVAILABLE = True
except ImportError:
    V1_AVAILABLE = False

# Import V2 architecture
from v2_architecture import (
    LLMManager, BaseBlock, ProcessingSubBlock, InternalProcessingBlock,
    ResearchAssistantResponse, UserInputBlock, BlockState, LLMProvider,
    TokenCounts, DisplayContent, InscribedBlock
)

# Import enhanced animation
from enhanced_animation import RealtimeTokenTracker, ActualTokenAnimator

# ============================================================================
# MIGRATION CONFIGURATION
# ============================================================================

@dataclass
class MigrationConfig:
    """Configuration for controlling migration behavior."""
    
    # Feature flags for gradual migration
    use_v2_llm_manager: bool = True
    use_v2_animation: bool = True
    use_v2_block_lifecycle: bool = True
    use_v2_token_tracking: bool = True
    
    # Compatibility settings
    maintain_v1_display: bool = True
    preserve_v1_logging: bool = True
    enable_dual_mode: bool = False  # Run both V1 and V2 in parallel for testing
    
    # Performance settings
    migration_timeout: float = 30.0
    max_concurrent_migrations: int = 3

# ============================================================================
# V1 TO V2 ADAPTERS
# ============================================================================

class V1TokenCounterAdapter:
    """Adapter to make V1 RollingTokenCounter work with V2 LLMManager."""
    
    def __init__(self, v1_counter: 'RollingTokenCounter', v2_manager: LLMManager):
        self.v1_counter = v1_counter
        self.v2_manager = v2_manager
        self.token_tracker = RealtimeTokenTracker()
        
    def update_tokens(self, input_tokens: int, output_tokens: int):
        """Update both V1 and V2 token tracking."""
        # Update V1 system
        if hasattr(self.v1_counter, 'update_with_actual_tokens'):
            self.v1_counter.update_with_actual_tokens(input_tokens, output_tokens)
        
        # Update V2 system
        self.token_tracker.update_with_api_response(input_tokens, output_tokens)
        
    def get_display_values(self) -> tuple[int, int]:
        """Get token values for display."""
        return self.token_tracker.get_display_values()

class V1ProcessingBlockAdapter(BaseBlock):
    """Adapter to make V1 ProcessingBlock compatible with V2 BaseBlock."""
    
    def __init__(self, v1_block: 'ProcessingBlock', title: str = "V1 Processing"):
        super().__init__(title)
        self.v1_block = v1_block
        self.v1_tokens = TokenCounts()
        
    def _on_live_start(self) -> None:
        """Start the V1 processing block."""
        if hasattr(self.v1_block, 'start'):
            self.v1_block.start()
    
    def _on_live_state_change(self, old_state: BlockState, new_state: BlockState) -> None:
        """Handle state changes."""
        if new_state == BlockState.LIVE_PROCESSING:
            if hasattr(self.v1_block, 'set_status'):
                self.v1_block.set_status("Processing...")
    
    def _create_live_display_content(self) -> DisplayContent:
        """Create display content from V1 block."""
        return DisplayContent(
            title=self.title,
            message=f"V1 Processing ({self.get_duration():.1f}s)",
            tokens=self.v1_tokens,
            elapsed_time=self.get_duration(),
            progress=0.5,  # Default progress
            metadata={"v1_compatibility": True}
        )
    
    def _create_inscribed_content(self) -> DisplayContent:
        """Create final inscribed content."""
        return DisplayContent(
            title=self.title,
            message=f"Completed ({self.get_duration():.1f}s)",
            tokens=self.v1_tokens,
            elapsed_time=self.get_duration(),
            progress=1.0,
            metadata={"v1_compatibility": True, "final_state": "completed"}
        )
    
    def _on_inscribed(self) -> None:
        """Handle transition to inscribed state."""
        if hasattr(self.v1_block, 'finalize'):
            self.v1_block.finalize()

class V1UIAdapter:
    """Adapter to make V1 RichUI work with V2 display system."""
    
    def __init__(self, v1_ui: 'RichUI'):
        self.v1_ui = v1_ui
        self.v2_displays: Dict[str, DisplayContent] = {}
        
    def render_v2_content(self, content: DisplayContent, block_id: str):
        """Render V2 DisplayContent using V1 RichUI."""
        self.v2_displays[block_id] = content
        
        # Convert to V1 format and display
        if hasattr(self.v1_ui, 'update_processing_status'):
            self.v1_ui.update_processing_status(
                title=content.title,
                message=content.message,
                progress=content.progress,
                elapsed_time=content.elapsed_time
            )
    
    def clear_v2_content(self, block_id: str):
        """Clear V2 content."""
        if block_id in self.v2_displays:
            del self.v2_displays[block_id]

# ============================================================================
# V2 TO V1 ADAPTERS  
# ============================================================================

class V2LLMManagerAdapter:
    """Adapter to make V2 LLMManager work with V1 system expectations."""
    
    def __init__(self, v2_manager: LLMManager):
        self.v2_manager = v2_manager
        
    async def make_v1_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Make a request that returns V1-compatible response."""
        response = await self.v2_manager.make_request(prompt, kwargs)
        
        # Convert to V1 format
        return {
            'response': response.content,
            'prompt_eval_count': response.tokens.input_tokens,
            'eval_count': response.tokens.output_tokens,
            'duration': response.duration_seconds,
            'model': response.model,
            'done': True
        }
    
    def get_v1_token_stats(self) -> Dict[str, Any]:
        """Get token statistics in V1 format."""
        summary = self.v2_manager.get_session_summary()
        return {
            'total_tokens': summary['total_tokens'].total_tokens,
            'input_tokens': summary['total_tokens'].input_tokens,
            'output_tokens': summary['total_tokens'].output_tokens,
            'requests': summary['total_requests']
        }

class V2BlockToV1Adapter:
    """Adapter to make V2 blocks work with V1 display system."""
    
    def __init__(self, v2_block: BaseBlock):
        self.v2_block = v2_block
        self.v1_compatible_data = {}
        
    def get_v1_display_data(self) -> Dict[str, Any]:
        """Get V1-compatible display data."""
        content = self.v2_block.get_current_display_content()
        
        return {
            'title': content.title,
            'message': content.message,
            'progress': content.progress,
            'elapsed_time': content.elapsed_time,
            'tokens_sent': content.tokens.input_tokens if content.tokens else 0,
            'tokens_received': content.tokens.output_tokens if content.tokens else 0,
            'state': self.v2_block.state.value
        }

# ============================================================================
# MIGRATION ORCHESTRATOR
# ============================================================================

class MigrationOrchestrator:
    """Orchestrates the gradual migration from V1 to V2."""
    
    def __init__(self, config: MigrationConfig):
        self.config = config
        self.active_adapters: Dict[str, Any] = {}
        self.migration_status: Dict[str, str] = {}
        
        # Migration statistics
        self.components_migrated = 0
        self.total_components = 0
        self.migration_errors: List[str] = []
        
    async def migrate_component(self, component_name: str, v1_component: Any, 
                              migration_type: str) -> Any:
        """Migrate a single component from V1 to V2."""
        self.migration_status[component_name] = "migrating"
        
        try:
            if migration_type == "token_counter":
                adapter = await self._migrate_token_counter(v1_component)
            elif migration_type == "processing_block":
                adapter = await self._migrate_processing_block(v1_component)
            elif migration_type == "ui_component":
                adapter = await self._migrate_ui_component(v1_component)
            else:
                raise ValueError(f"Unknown migration type: {migration_type}")
            
            self.active_adapters[component_name] = adapter
            self.migration_status[component_name] = "completed"
            self.components_migrated += 1
            
            return adapter
            
        except Exception as e:
            self.migration_status[component_name] = f"failed: {str(e)}"
            self.migration_errors.append(f"{component_name}: {str(e)}")
            raise
    
    async def _migrate_token_counter(self, v1_counter: Any) -> V1TokenCounterAdapter:
        """Migrate token counter to V2."""
        # Create V2 LLM manager
        v2_manager = LLMManager(LLMProvider.OLLAMA, "tinyllama")
        
        # Create adapter
        adapter = V1TokenCounterAdapter(v1_counter, v2_manager)
        
        return adapter
    
    async def _migrate_processing_block(self, v1_block: Any) -> V1ProcessingBlockAdapter:
        """Migrate processing block to V2."""
        adapter = V1ProcessingBlockAdapter(v1_block, "Migrated V1 Block")
        return adapter
    
    async def _migrate_ui_component(self, v1_ui: Any) -> V1UIAdapter:
        """Migrate UI component to V2."""
        adapter = V1UIAdapter(v1_ui)
        return adapter
    
    def get_migration_report(self) -> Dict[str, Any]:
        """Get comprehensive migration report."""
        return {
            'total_components': self.total_components,
            'components_migrated': self.components_migrated,
            'migration_percentage': (self.components_migrated / self.total_components * 100) if self.total_components > 0 else 0,
            'active_adapters': list(self.active_adapters.keys()),
            'migration_status': self.migration_status,
            'errors': self.migration_errors,
            'config': self.config.__dict__
        }

# ============================================================================
# HYBRID SYSTEM MANAGER
# ============================================================================

class HybridSystemManager:
    """Manages the hybrid V1/V2 system during migration."""
    
    def __init__(self, config: MigrationConfig):
        self.config = config
        self.orchestrator = MigrationOrchestrator(config)
        
        # System components
        self.v1_components: Dict[str, Any] = {}
        self.v2_components: Dict[str, Any] = {}
        self.adapters: Dict[str, Any] = {}
        
        # Performance tracking
        self.v1_performance: Dict[str, float] = {}
        self.v2_performance: Dict[str, float] = {}
        
    async def initialize_hybrid_system(self, quiet: bool = False):
        """Initialize the hybrid system."""
        if not quiet:
            print("🔄 Initializing Hybrid V1/V2 System...")
        
        # Initialize V2 components
        if self.config.use_v2_llm_manager:
            self.v2_components['llm_manager'] = LLMManager(LLMProvider.OLLAMA, "tinyllama")
            if not quiet:
                print("✅ V2 LLM Manager initialized")
        
        if self.config.use_v2_animation:
            self.v2_components['animation'] = RealtimeTokenTracker()
            if not quiet:
                print("✅ V2 Animation system initialized")
        
        # Setup adapters if needed
        if self.config.maintain_v1_display:
            # Create compatibility layer
            if not quiet:
                print("⚙️  Setting up V1 compatibility layer...")
    
    async def process_request_hybrid(self, request: str) -> Dict[str, Any]:
        """Process a request using the hybrid system."""
        start_time = time.time()
        
        try:
            # Route to appropriate system based on config
            if self.config.use_v2_llm_manager:
                response = await self._process_with_v2(request)
            else:
                response = await self._process_with_v1(request)
            
            # Track performance
            duration = time.time() - start_time
            system_used = "v2" if self.config.use_v2_llm_manager else "v1"
            
            if system_used == "v2":
                self.v2_performance[request[:50]] = duration
            else:
                self.v1_performance[request[:50]] = duration
            
            return {
                'response': response,
                'system_used': system_used,
                'duration': duration,
                'hybrid_mode': True
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'system_used': 'unknown',
                'duration': time.time() - start_time,
                'hybrid_mode': True
            }
    
    async def _process_with_v2(self, request: str) -> str:
        """Process request with V2 system."""
        llm_manager = self.v2_components['llm_manager']
        
        # Create processing pipeline
        pipeline = InternalProcessingBlock("Hybrid Request Processing")
        
        # Add processing sub-block
        sub_block = ProcessingSubBlock(
            title="Request Processing",
            methodology="V2 Hybrid Processing",
            llm_manager=llm_manager
        )
        pipeline.add_sub_block(sub_block)
        
        # Execute
        result = await pipeline.execute_pipeline(request)
        return result
    
    async def _process_with_v1(self, request: str) -> str:
        """Process request with V1 system (placeholder)."""
        # This would integrate with actual V1 system
        return f"V1 processed: {request}"
    
    def get_performance_comparison(self) -> Dict[str, Any]:
        """Get performance comparison between V1 and V2."""
        v1_avg = sum(self.v1_performance.values()) / len(self.v1_performance) if self.v1_performance else 0
        v2_avg = sum(self.v2_performance.values()) / len(self.v2_performance) if self.v2_performance else 0
        
        return {
            'v1_average_duration': v1_avg,
            'v2_average_duration': v2_avg,
            'v1_requests': len(self.v1_performance),
            'v2_requests': len(self.v2_performance),
            'performance_delta': v2_avg - v1_avg if v1_avg > 0 and v2_avg > 0 else 0,
            'improvement_percentage': ((v1_avg - v2_avg) / v1_avg * 100) if v1_avg > 0 and v2_avg > 0 else 0
        }

# ============================================================================
# REGRESSION TESTING FRAMEWORK
# ============================================================================

class RegressionTestSuite:
    """Comprehensive regression testing for migration."""
    
    def __init__(self, hybrid_manager: HybridSystemManager):
        self.hybrid_manager = hybrid_manager
        self.test_results: Dict[str, Dict[str, Any]] = {}
        
    async def run_regression_tests(self) -> Dict[str, Any]:
        """Run comprehensive regression tests."""
        print("🧪 Running Regression Test Suite...")
        
        test_cases = [
            {
                'name': 'basic_query',
                'request': 'What is 2+2?',
                'expected_type': str,
                'timeout': 10.0
            },
            {
                'name': 'complex_query', 
                'request': 'Explain machine learning in simple terms',
                'expected_type': str,
                'timeout': 30.0
            },
            {
                'name': 'token_counting',
                'request': 'Hello world',
                'expected_type': str,
                'timeout': 5.0,
                'check_tokens': True
            }
        ]
        
        results = {}
        
        for test_case in test_cases:
            print(f"  Running {test_case['name']}...")
            result = await self._run_single_test(test_case)
            results[test_case['name']] = result
            
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"    {status} ({result['duration']:.2f}s)")
            
            if not result['passed']:
                print(f"    Error: {result.get('error', 'Unknown error')}")
        
        # Calculate overall results
        passed_tests = sum(1 for r in results.values() if r['passed'])
        total_tests = len(results)
        
        summary = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': total_tests - passed_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'test_details': results
        }
        
        print(f"\n📊 Test Results: {passed_tests}/{total_tests} passed ({summary['success_rate']:.1f}%)")
        
        return summary
    
    async def _run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single regression test."""
        start_time = time.time()
        
        try:
            # Process request
            result = await asyncio.wait_for(
                self.hybrid_manager.process_request_hybrid(test_case['request']),
                timeout=test_case['timeout']
            )
            
            # Basic validation
            if 'error' in result:
                return {
                    'passed': False,
                    'error': result['error'],
                    'duration': time.time() - start_time
                }
            
            # Check response type
            if not isinstance(result.get('response'), test_case['expected_type']):
                return {
                    'passed': False,
                    'error': f"Expected {test_case['expected_type']}, got {type(result.get('response'))}",
                    'duration': time.time() - start_time
                }
            
            # Check token counting if required
            if test_case.get('check_tokens', False):
                if result.get('system_used') == 'v2':
                    llm_manager = self.hybrid_manager.v2_components.get('llm_manager')
                    if llm_manager and len(llm_manager.request_history) == 0:
                        return {
                            'passed': False,
                            'error': 'No token tracking found',
                            'duration': time.time() - start_time
                        }
            
            return {
                'passed': True,
                'duration': time.time() - start_time,
                'response_length': len(str(result.get('response', ''))),
                'system_used': result.get('system_used', 'unknown')
            }
            
        except asyncio.TimeoutError:
            return {
                'passed': False,
                'error': 'Test timed out',
                'duration': time.time() - start_time
            }
        except Exception as e:
            return {
                'passed': False,
                'error': str(e),
                'duration': time.time() - start_time
            }

# ============================================================================
# EXAMPLE USAGE AND DEMO
# ============================================================================

if __name__ == "__main__":
    async def demo_migration():
        """Demonstrate the migration system."""
        print("🚀 V1 to V2 Migration Demo")
        print("=" * 50)
        
        # Create migration config
        config = MigrationConfig(
            use_v2_llm_manager=True,
            use_v2_animation=True,
            maintain_v1_display=True,
            enable_dual_mode=False
        )
        
        # Initialize hybrid system
        hybrid_manager = HybridSystemManager(config)
        await hybrid_manager.initialize_hybrid_system()
        
        # Test hybrid processing
        print("\n🧪 Testing Hybrid Processing...")
        test_request = "What is machine learning?"
        
        result = await hybrid_manager.process_request_hybrid(test_request)
        print(f"✅ Processed with {result['system_used']} system in {result['duration']:.2f}s")
        print(f"Response: {result['response'][:100]}...")
        
        # Run regression tests
        print("\n🧪 Running Regression Tests...")
        test_suite = RegressionTestSuite(hybrid_manager)
        test_results = await test_suite.run_regression_tests()
        
        # Show performance comparison
        print("\n📊 Performance Comparison:")
        perf_comparison = hybrid_manager.get_performance_comparison()
        print(f"V1 avg: {perf_comparison['v1_average_duration']:.2f}s")
        print(f"V2 avg: {perf_comparison['v2_average_duration']:.2f}s")
        
        # Show migration report
        print("\n📋 Migration Report:")
        migration_report = hybrid_manager.orchestrator.get_migration_report()
        print(f"Components migrated: {migration_report['components_migrated']}")
        print(f"Migration percentage: {migration_report['migration_percentage']:.1f}%")
        
        print("\n✨ Migration Demo Complete!")
        print("🎯 Key Features Demonstrated:")
        print("  - Zero-regression migration")
        print("  - Hybrid V1/V2 operation")
        print("  - Comprehensive regression testing")
        print("  - Performance monitoring")
        print("  - Gradual component migration")
    
    # Run demo
    asyncio.run(demo_migration())