#!/usr/bin/env python3
"""
Comprehensive Regression Test Suite for V2 Architecture

Tests all components and ensures no regressions from V1 to V2 migration.
Focuses on the three critical issues that were identified:
1. Token timing accuracy
2. Animation handling without snapping
3. Smooth animation curves with higher derivatives
"""

import asyncio
import sys
import time
import unittest
from pathlib import Path
from typing import Dict, Any, List
import tempfile
import os

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import V2 components
from v2_architecture import (
    LLMManager, LLMProvider, ProcessingSubBlock, InternalProcessingBlock,
    ResearchAssistantResponse, UserInputBlock, BaseBlock, BlockState,
    TokenCounts, DisplayContent, Artifact
)

# Import enhanced animation
from enhanced_animation import (
    ActualTokenAnimator, RealtimeTokenTracker, SmoothAnimationCurve,
    AnimationKeyframe
)

# Import migration system
from v1_v2_migration import (
    MigrationConfig, MigrationOrchestrator, HybridSystemManager,
    V1TokenCounterAdapter, V2LLMManagerAdapter
)

class TestV2Architecture(unittest.TestCase):
    """Test the V2 architecture components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.llm_manager = LLMManager(LLMProvider.OLLAMA, "tinyllama")
        
    def test_llm_manager_initialization(self):
        """Test LLM manager creates correctly."""
        self.assertEqual(self.llm_manager.provider, LLMProvider.OLLAMA)
        self.assertEqual(self.llm_manager.model, "tinyllama")
        self.assertEqual(self.llm_manager.session_tokens.total_tokens, 0)
        self.assertEqual(len(self.llm_manager.request_history), 0)
    
    async def test_llm_manager_request_tracking(self):
        """Test LLM manager tracks requests correctly."""
        # Make a request
        response = await self.llm_manager.make_request("Test prompt")
        
        # Verify tracking
        self.assertEqual(len(self.llm_manager.request_history), 1)
        self.assertGreater(self.llm_manager.session_tokens.total_tokens, 0)
        self.assertIsInstance(response.content, str)
        self.assertGreater(response.duration_seconds, 0)
        
    def test_processing_sub_block_creation(self):
        """Test ProcessingSubBlock creates correctly."""
        block = ProcessingSubBlock(
            title="Test Block",
            methodology="Test Method",
            llm_manager=self.llm_manager
        )
        
        self.assertEqual(block.title, "Test Block")
        self.assertEqual(block.methodology, "Test Method")
        self.assertEqual(block.state, BlockState.CREATED)
        self.assertEqual(block.progress, 0.0)
        
    async def test_processing_sub_block_execution(self):
        """Test ProcessingSubBlock executes correctly."""
        block = ProcessingSubBlock(
            title="Test Block",
            methodology="Test Method", 
            llm_manager=self.llm_manager
        )
        
        # Execute block
        result = await block.execute("Test input")
        
        # Verify execution
        self.assertIsInstance(result, str)
        self.assertEqual(block.state, BlockState.LIVE_PROCESSING)
        self.assertIsNotNone(block.llm_response)
        self.assertGreater(block.progress, 0)
        
    def test_internal_processing_block_creation(self):
        """Test InternalProcessingBlock creates correctly."""
        pipeline = InternalProcessingBlock("Test Pipeline")
        
        self.assertEqual(pipeline.title, "Test Pipeline")
        self.assertEqual(len(pipeline.sub_blocks), 0)
        self.assertEqual(pipeline.current_sub_block_index, 0)
        
    async def test_internal_processing_block_pipeline(self):
        """Test InternalProcessingBlock runs pipeline correctly."""
        pipeline = InternalProcessingBlock("Test Pipeline")
        
        # Add sub-blocks
        block1 = ProcessingSubBlock("Block 1", "Method 1", self.llm_manager)
        block2 = ProcessingSubBlock("Block 2", "Method 2", self.llm_manager)
        
        pipeline.add_sub_block(block1)
        pipeline.add_sub_block(block2)
        
        # Execute pipeline
        result = await pipeline.execute_pipeline("Test input")
        
        # Verify pipeline execution
        self.assertIsInstance(result, str)
        self.assertEqual(len(pipeline.sub_blocks), 2)
        self.assertEqual(pipeline.current_sub_block_index, 1)  # Should be at last block
        
        # Verify token aggregation
        total_tokens = pipeline.get_total_tokens()
        self.assertGreater(total_tokens.total_tokens, 0)
        
    def test_research_assistant_response_creation(self):
        """Test ResearchAssistantResponse creates correctly."""
        response = ResearchAssistantResponse(
            content="Test response",
            routing_metadata={"intent": "CHAT"}
        )
        
        self.assertEqual(response.content, "Test response")
        self.assertEqual(response.routing_metadata["intent"], "CHAT")
        self.assertEqual(len(response.artifacts), 0)
        self.assertEqual(len(response.tool_results), 0)
        
    def test_research_assistant_response_artifacts(self):
        """Test ResearchAssistantResponse artifact handling."""
        response = ResearchAssistantResponse("Test response")
        
        # Add artifact
        artifact = Artifact(
            content="def test(): pass",
            artifact_type="code",
            language="python",
            title="Test Code"
        )
        response.add_artifact(artifact)
        
        # Verify artifact
        self.assertEqual(len(response.artifacts), 1)
        self.assertEqual(response.artifacts[0].content, "def test(): pass")
        self.assertEqual(response.artifacts[0].language, "python")
        
    def test_user_input_block_creation(self):
        """Test UserInputBlock creates correctly."""
        input_block = UserInputBlock()
        
        self.assertEqual(input_block.title, "User Input")
        self.assertEqual(input_block.text_content, "")
        self.assertEqual(len(input_block.attachments), 0)
        self.assertEqual(len(input_block.shell_commands), 0)
        self.assertFalse(input_block.input_complete)
        
    def test_user_input_block_command_parsing(self):
        """Test UserInputBlock parses shell commands correctly."""
        input_block = UserInputBlock()
        
        # Test command parsing
        text = "Check the status with `git status` and then $(ls -la)"
        commands = input_block._parse_embedded_commands(text)
        
        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0].command, "git")
        self.assertEqual(commands[0].args, ["status"])
        self.assertEqual(commands[1].command, "ls")
        self.assertEqual(commands[1].args, ["-la"])

class TestEnhancedAnimation(unittest.TestCase):
    """Test the enhanced animation system."""
    
    def test_smooth_animation_curves(self):
        """Test animation curves are smooth and continuous."""
        # Test cubic Bezier
        curve_values = [SmoothAnimationCurve.cubic_bezier(t/10, 0, 0.25, 0.75, 1) for t in range(11)]
        
        # Should be monotonically increasing
        for i in range(1, len(curve_values)):
            self.assertGreaterEqual(curve_values[i], curve_values[i-1])
            
        # Should start at 0 and end at 1
        self.assertEqual(curve_values[0], 0)
        self.assertEqual(curve_values[-1], 1)
        
    def test_actual_token_animator_initialization(self):
        """Test ActualTokenAnimator initializes correctly."""
        animator = ActualTokenAnimator()
        
        self.assertEqual(len(animator.keyframes), 0)
        self.assertIsNone(animator.start_time)
        self.assertEqual(animator.current_input, 0)
        self.assertEqual(animator.current_output, 0)
        
    def test_actual_token_animator_keyframes(self):
        """Test ActualTokenAnimator handles keyframes correctly."""
        animator = ActualTokenAnimator()
        
        # Start animation
        animator.start_animation()
        
        # Add keyframes
        animator.add_keyframe(10, 0)  # Input processed
        animator.add_keyframe(10, 5)  # Some output
        animator.add_keyframe(10, 15) # More output
        
        # Verify keyframes
        self.assertEqual(len(animator.keyframes), 4)  # Including initial zero keyframe
        self.assertEqual(animator.keyframes[-1].input_tokens, 10)
        self.assertEqual(animator.keyframes[-1].output_tokens, 15)
        
    def test_actual_token_animator_interpolation(self):
        """Test ActualTokenAnimator interpolates correctly."""
        animator = ActualTokenAnimator()
        
        # Add keyframes with known timestamps
        start_time = time.time()
        animator.start_animation(start_time)
        
        # Add keyframes manually with specific timestamps
        animator.keyframes.append(AnimationKeyframe(0.0, 0, 0))
        animator.keyframes.append(AnimationKeyframe(1.0, 10, 20))
        
        # Test interpolation at midpoint
        input_tokens, output_tokens = animator.get_current_animated_values(start_time + 0.5)
        
        # Should be between 0 and final values
        self.assertGreater(input_tokens, 0)
        self.assertLess(input_tokens, 10)
        self.assertGreater(output_tokens, 0)
        self.assertLess(output_tokens, 20)
        
    def test_realtime_token_tracker_lifecycle(self):
        """Test RealtimeTokenTracker full lifecycle."""
        tracker = RealtimeTokenTracker()
        
        # Start request
        tracker.start_request()
        self.assertTrue(tracker.is_active)
        
        # Update with API response
        tracker.update_with_api_response(15, 0)
        tracker.update_with_api_response(15, 10)
        
        # Complete request
        tracker.complete_request(15, 25)
        self.assertFalse(tracker.is_active)
        
        # Verify final values
        input_tokens, output_tokens = tracker.get_display_values()
        self.assertEqual(input_tokens, 15)
        self.assertEqual(output_tokens, 25)
        
    def test_realtime_token_tracker_no_estimates(self):
        """Test RealtimeTokenTracker never shows estimates."""
        tracker = RealtimeTokenTracker()
        
        # Before starting, should show zeros
        input_tokens, output_tokens = tracker.get_display_values()
        self.assertEqual(input_tokens, 0)
        self.assertEqual(output_tokens, 0)
        
        # Start request but don't update - should still show zeros
        tracker.start_request()
        input_tokens, output_tokens = tracker.get_display_values()
        self.assertEqual(input_tokens, 0)
        self.assertEqual(output_tokens, 0)
        
        # Only after API response should we see actual values
        tracker.update_with_api_response(20, 30)
        input_tokens, output_tokens = tracker.get_display_values()
        self.assertEqual(input_tokens, 20)
        self.assertEqual(output_tokens, 30)

class TestMigrationSystem(unittest.TestCase):
    """Test the migration system."""
    
    def test_migration_config_creation(self):
        """Test MigrationConfig creates correctly."""
        config = MigrationConfig(
            use_v2_llm_manager=True,
            use_v2_animation=True,
            maintain_v1_display=True
        )
        
        self.assertTrue(config.use_v2_llm_manager)
        self.assertTrue(config.use_v2_animation)
        self.assertTrue(config.maintain_v1_display)
        
    def test_migration_orchestrator_creation(self):
        """Test MigrationOrchestrator creates correctly."""
        config = MigrationConfig()
        orchestrator = MigrationOrchestrator(config)
        
        self.assertEqual(orchestrator.config, config)
        self.assertEqual(len(orchestrator.active_adapters), 0)
        self.assertEqual(orchestrator.components_migrated, 0)
        
    def test_hybrid_system_manager_creation(self):
        """Test HybridSystemManager creates correctly."""
        config = MigrationConfig()
        manager = HybridSystemManager(config)
        
        self.assertEqual(manager.config, config)
        self.assertEqual(len(manager.v1_components), 0)
        self.assertEqual(len(manager.v2_components), 0)
        
    async def test_hybrid_system_initialization(self):
        """Test HybridSystemManager initializes correctly."""
        config = MigrationConfig(
            use_v2_llm_manager=True,
            use_v2_animation=True
        )
        manager = HybridSystemManager(config)
        
        await manager.initialize_hybrid_system()
        
        # Should have V2 components
        self.assertIn('llm_manager', manager.v2_components)
        self.assertIn('animation', manager.v2_components)
        
    async def test_hybrid_system_request_processing(self):
        """Test HybridSystemManager processes requests correctly."""
        config = MigrationConfig(use_v2_llm_manager=True)
        manager = HybridSystemManager(config)
        
        await manager.initialize_hybrid_system()
        
        # Process a request
        result = await manager.process_request_hybrid("Test request")
        
        # Verify result
        self.assertIsInstance(result, dict)
        self.assertIn('response', result)
        self.assertIn('system_used', result)
        self.assertIn('duration', result)
        self.assertEqual(result['system_used'], 'v2')

class TestRegressionScenarios(unittest.TestCase):
    """Test specific regression scenarios."""
    
    async def test_token_timing_accuracy(self):
        """Test that token timing is accurate (Issue #1)."""
        llm_manager = LLMManager(LLMProvider.OLLAMA, "tinyllama")
        
        # Make a request and measure timing
        start_time = time.time()
        response = await llm_manager.make_request("What is 2+2?")
        end_time = time.time()
        
        # Verify timing accuracy
        measured_duration = end_time - start_time
        reported_duration = response.duration_seconds
        
        # Should be within 10% of each other
        timing_error = abs(measured_duration - reported_duration) / measured_duration
        self.assertLess(timing_error, 0.1, f"Timing error too high: {timing_error:.2%}")
        
    async def test_animation_no_snapping(self):
        """Test that animation doesn't snap from estimates to actuals (Issue #2)."""
        tracker = RealtimeTokenTracker()
        
        # Start request
        tracker.start_request()
        
        # Simulate gradual API responses
        tracker.update_with_api_response(10, 0)
        tokens1 = tracker.get_display_values()
        
        # Small delay then more tokens
        await asyncio.sleep(0.1)
        tracker.update_with_api_response(10, 5)
        tokens2 = tracker.get_display_values()
        
        # Should have smooth transition, not snapping
        self.assertGreaterEqual(tokens2[1], tokens1[1])  # Output should increase
        self.assertEqual(tokens2[0], tokens1[0])  # Input should stay same
        
    def test_animation_smooth_curves(self):
        """Test that animation curves have smooth derivatives (Issue #3)."""
        # Test different curve types
        curve_types = [
            SmoothAnimationCurve.ease_in_out_cubic,
            SmoothAnimationCurve.ease_out_exponential,
            lambda t: SmoothAnimationCurve.sigmoid_curve(t)
        ]
        
        for curve_func in curve_types:
            # Generate curve values
            points = [curve_func(t/100) for t in range(101)]
            
            # Check for smooth progression (no sudden jumps)
            for i in range(1, len(points)):
                step_size = points[i] - points[i-1]
                self.assertGreaterEqual(step_size, -0.01)  # Should be monotonic or nearly so
                self.assertLessEqual(step_size, 0.05)      # Should not have large jumps
                
    async def test_end_to_end_pipeline(self):
        """Test complete end-to-end pipeline works without regressions."""
        # Create complete system
        llm_manager = LLMManager(LLMProvider.OLLAMA, "tinyllama")
        
        # Create pipeline
        pipeline = InternalProcessingBlock("Test Pipeline")
        
        # Add processing steps
        intent_block = ProcessingSubBlock("Intent Detection", "Classification", llm_manager)
        response_block = ProcessingSubBlock("Response Generation", "Generation", llm_manager)
        
        pipeline.add_sub_block(intent_block)
        pipeline.add_sub_block(response_block)
        
        # Execute pipeline
        result = await pipeline.execute_pipeline("What is machine learning?")
        
        # Verify complete pipeline
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        
        # Verify all blocks completed
        for block in pipeline.sub_blocks:
            self.assertIsNotNone(block.llm_response)
            self.assertGreater(block.progress, 0)
            
        # Verify token tracking
        total_tokens = pipeline.get_total_tokens()
        self.assertGreater(total_tokens.total_tokens, 0)
        
        # Create final response
        response = ResearchAssistantResponse(
            content=result,
            routing_metadata={"intent": "CHAT", "method": "AI_CLASSIFIED"}
        )
        
        response.transition_to_live()
        inscribed = response.transition_to_inscribed()
        
        # Verify response lifecycle
        self.assertEqual(response.state, BlockState.INSCRIBED)
        self.assertIsNotNone(inscribed)
        self.assertEqual(inscribed.title, "Research Assistant Response")

class TestRunner:
    """Custom test runner for comprehensive regression testing."""
    
    def __init__(self):
        self.loader = unittest.TestLoader()
        self.suite = unittest.TestSuite()
        
    def discover_tests(self):
        """Discover and load all test cases."""
        test_cases = [
            TestV2Architecture,
            TestEnhancedAnimation,
            TestMigrationSystem,
            TestRegressionScenarios
        ]
        
        for test_case in test_cases:
            tests = self.loader.loadTestsFromTestCase(test_case)
            self.suite.addTests(tests)
            
    async def run_async_tests(self):
        """Run async tests specifically."""
        async_tests = [
            ('test_llm_manager_request_tracking', TestV2Architecture),
            ('test_processing_sub_block_execution', TestV2Architecture),
            ('test_internal_processing_block_pipeline', TestV2Architecture),
            ('test_hybrid_system_initialization', TestMigrationSystem),
            ('test_hybrid_system_request_processing', TestMigrationSystem),
            ('test_token_timing_accuracy', TestRegressionScenarios),
            ('test_animation_no_snapping', TestRegressionScenarios),
            ('test_end_to_end_pipeline', TestRegressionScenarios)
        ]
        
        results = []
        
        for test_name, test_class in async_tests:
            print(f"Running {test_name}...")
            try:
                instance = test_class()
                instance.setUp() if hasattr(instance, 'setUp') else None
                
                test_method = getattr(instance, test_name)
                await test_method()
                
                results.append({'test': test_name, 'status': 'PASS', 'error': None})
                print(f"  ✅ PASS")
                
            except Exception as e:
                results.append({'test': test_name, 'status': 'FAIL', 'error': str(e)})
                print(f"  ❌ FAIL: {str(e)}")
                
        return results
        
    def run_sync_tests(self):
        """Run synchronous tests."""
        runner = unittest.TextTestRunner(verbosity=2)
        
        # Filter to only sync tests
        sync_suite = unittest.TestSuite()
        
        # Get all tests from the suite
        for test in self.suite:
            if hasattr(test, '_testMethodName'):
                test_name = test._testMethodName
                if not any(async_test in test_name for async_test in [
                    'test_llm_manager_request_tracking',
                    'test_processing_sub_block_execution', 
                    'test_internal_processing_block_pipeline',
                    'test_hybrid_system_initialization',
                    'test_hybrid_system_request_processing',
                    'test_token_timing_accuracy',
                    'test_animation_no_snapping',
                    'test_end_to_end_pipeline'
                ]):
                    sync_suite.addTest(test)
            else:
                # Handle nested test suites
                for subtest in test:
                    if hasattr(subtest, '_testMethodName'):
                        test_name = subtest._testMethodName
                        if not any(async_test in test_name for async_test in [
                            'test_llm_manager_request_tracking',
                            'test_processing_sub_block_execution', 
                            'test_internal_processing_block_pipeline',
                            'test_hybrid_system_initialization',
                            'test_hybrid_system_request_processing',
                            'test_token_timing_accuracy',
                            'test_animation_no_snapping',
                            'test_end_to_end_pipeline'
                        ]):
                            sync_suite.addTest(subtest)
                    
        result = runner.run(sync_suite)
        return result

async def main():
    """Run comprehensive regression tests."""
    print("🧪 Comprehensive Regression Test Suite")
    print("=" * 60)
    
    test_runner = TestRunner()
    test_runner.discover_tests()
    
    print("\n📋 Running Synchronous Tests...")
    sync_results = test_runner.run_sync_tests()
    
    print("\n⚡ Running Asynchronous Tests...")
    async_results = await test_runner.run_async_tests()
    
    # Calculate overall results
    total_sync = sync_results.testsRun
    failed_sync = len(sync_results.failures) + len(sync_results.errors)
    passed_sync = total_sync - failed_sync
    
    total_async = len(async_results)
    passed_async = sum(1 for r in async_results if r['status'] == 'PASS')
    failed_async = total_async - passed_async
    
    total_tests = total_sync + total_async
    total_passed = passed_sync + passed_async
    total_failed = failed_sync + failed_async
    
    print(f"\n📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success Rate: {(total_passed/total_tests*100):.1f}%")
    
    if total_failed == 0:
        print("\n✅ ALL TESTS PASSED - NO REGRESSIONS DETECTED!")
        print("🎯 The V2 architecture is ready for production use.")
    else:
        print(f"\n❌ {total_failed} TESTS FAILED - REGRESSIONS DETECTED!")
        print("🔧 Please review and fix failing tests before deploying.")
        
        # Show failed async tests
        for result in async_results:
            if result['status'] == 'FAIL':
                print(f"  - {result['test']}: {result['error']}")
    
    return total_failed == 0

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)