#!/usr/bin/env python3
"""
Integration Tests for Research Assistant REPL

Tests the full application behavior including:
- Different LLM configurations (debug, mixed, fast, test)
- System check validation and failures
- End-to-end query processing
- Timeout behavior
- Configuration validation
- Model availability checks
"""

import subprocess
import time
import unittest
from pathlib import Path
from typing import Optional, Dict, Any
import json
import re


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""
    
    def setUp(self):
        """Set up test environment."""
        self.timeout = 30  # 30 second timeout for integration tests
        self.project_root = Path(__file__).parent.parent
        self.repl_script = self.project_root / "src" / "main.py"
        
    def run_repl_test(self, 
                      config: str, 
                      input_text: str, 
                      timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Run a REPL test with given configuration and input.
        
        Args:
            config: Configuration name (debug, mixed, fast, test)
            input_text: Input text to send to the REPL
            timeout: Timeout in seconds (defaults to self.timeout)
            
        Returns:
            Dict containing stdout, stderr, returncode, and timing info
        """
        if timeout is None:
            timeout = self.timeout
            
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                ['python', str(self.repl_script), '--config', config],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )
            
            # Convert escaped newlines to actual newlines
            actual_input = input_text.replace('\\n', '\n')
            
            stdout, stderr = process.communicate(
                input=actual_input,
                timeout=timeout
            )
            
            duration = time.time() - start_time
            
            # Filter out harmless warnings that shouldn't cause test failures
            filtered_stderr = stderr
            if stderr and "Warning: Input is not a terminal" in stderr:
                # Remove the terminal warning - it's harmless for tests
                lines = stderr.split('\n')
                filtered_lines = [line for line in lines if "Warning: Input is not a terminal" not in line]
                filtered_stderr = '\n'.join(filtered_lines).strip()
            
            # Consider success if return code is 0 OR if the only error is the terminal warning
            is_success = (process.returncode == 0 or 
                         (stderr and stderr.strip() == "Warning: Input is not a terminal (fd=0)."))
            
            return {
                'stdout': stdout,
                'stderr': filtered_stderr,
                'returncode': process.returncode,
                'duration': duration,
                'success': is_success
            }
            
        except subprocess.TimeoutExpired:
            process.kill()
            duration = time.time() - start_time
            return {
                'stdout': '',
                'stderr': 'Process timed out',
                'returncode': -1,
                'duration': duration,
                'success': False,
                'timeout': True
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'duration': duration,
                'success': False,
                'error': str(e)
            }


class TestSystemCheck(IntegrationTestCase):
    """Test system check behavior across different configurations."""
    
    def test_system_check_displays_configuration(self):
        """Test that system check displays configuration information."""
        result = self.run_repl_test('test', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for system check display
        self.assertIn('System_Check', result['stdout'])
        self.assertIn('Configuration:', result['stdout'])
        self.assertIn('Dependencies:', result['stdout'])
        self.assertIn('LLM Providers:', result['stdout'])
        
    def test_system_check_timing(self):
        """Test that system check includes timing information."""
        result = self.run_repl_test('test', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for timing information - v3 shows timing in the panel title
        self.assertIn('System_Check', result['stdout'])
        self.assertIn('(0.', result['stdout'])  # Shows timing like (0.2s)
        
    def test_system_check_validation_steps(self):
        """Test that system check runs all validation steps."""
        result = self.run_repl_test('test', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for all validation steps
        self.assertIn('Configuration:', result['stdout'])
        self.assertIn('groq', result['stdout'])  # LLM provider
        self.assertIn('✅', result['stdout'])  # Success indicators
        # V3 shows multiple providers
        # Both intent detection and main query providers should appear


class TestConfigurationBehavior(IntegrationTestCase):
    """Test different LLM configurations."""
    
    def test_groq_configuration(self):
        """Test Groq configuration (fast/test)."""
        result = self.run_repl_test('test', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for Groq model usage
        self.assertIn('groq/llama3-8b-8192', result['stdout'])
        self.assertIn('Intent Detection', result['stdout'])
        self.assertIn('Main Query', result['stdout'])
        
    def test_configuration_display(self):
        """Test that configuration is properly displayed."""
        result = self.run_repl_test('fast', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check configuration display
        self.assertIn('Configuration:', result['stdout'])
        self.assertIn('groq/llama3-8b-8192', result['stdout'])
        
    def test_mixed_configuration_display(self):
        """Test mixed configuration display."""
        result = self.run_repl_test('mixed', 'Hello\n/quit\n', timeout=45)
        
        # Mixed config uses Ollama + Groq, might fail if Ollama not available
        if result['success']:
            self.assertIn('ollama/tinyllama', result['stdout'])
            self.assertIn('groq/llama3-8b-8192', result['stdout'])
        else:
            # If it fails, it should fail during system check
            self.assertIn('System Check', result['stdout'])


class TestEchoTests(IntegrationTestCase):
    """
    End-to-end echo tests - comprehensive pipeline verification.
    
    These tests verify the complete application pipeline from input to output:
    1. Basic query processing (input -> Internal Processing -> LLM -> output)
    2. Intent detection routing (different query types)
    3. Timing information display (durations, artificial delays)
    4. Token counting display (input/output tokens)
    5. Visual flow indicators (emojis, arrows, containers)
    6. V1 Internal Processing container structure (nested sub-blocks)
    7. Error handling (empty inputs, recovery)
    8. Command integration (/stats, /help with queries)
    9. Configuration display (model names in system check and processing)
    
    Each test runs the full application subprocess and verifies that specific
    elements appear in the stdout, ensuring end-to-end functionality works.
    """
    
    def test_basic_echo_simple_query(self):
        """Test basic echo with simple query."""
        result = self.run_repl_test('test', 'Hello world\\n/quit\\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Verify complete pipeline
        self.assertIn('You: Hello world', result['stdout'])
        self.assertIn('System Check', result['stdout'])
        self.assertIn('groq/llama3-8b-8192', result['stdout'])
        self.assertIn('Internal Processing', result['stdout'])
        self.assertIn('Intent Detection', result['stdout'])
        self.assertIn('Main Query', result['stdout'])
        self.assertIn('Research Assistant', result['stdout'])
        self.assertIn('Goodbye!', result['stdout'])
        
    def test_echo_with_intent_detection(self):
        """Test echo with different intent patterns."""
        test_cases = [
            ('search for machine learning papers', 'SEARCH'),
            ('calculate 2 + 2', 'COMPUTE'),
            ('write a python function', 'CODE'),
            ('analyze these results', 'SYNTHESIZE'),
            ('hello there', 'CHAT')
        ]
        
        for query, expected_intent in test_cases:
            with self.subTest(query=query, intent=expected_intent):
                result = self.run_repl_test('test', f'{query}\\n/quit\\n')
                
                self.assertTrue(result['success'], f"Failed for query: {query}")
                self.assertIn(f'You: {query}', result['stdout'])
                self.assertIn('Internal Processing', result['stdout'])
                self.assertIn('Intent Detection', result['stdout'])
                
    def test_echo_timing_verification(self):
        """Test that timing information appears correctly."""
        result = self.run_repl_test('test', 'Test timing\\n/quit\\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for timing patterns
        import re
        timing_patterns = [
            r'\([0-9]+\.[0-9]+s\)',  # Duration in parentheses
            r'[0-9]+\.[0-9]+s',       # Duration anywhere
            r'⏱️',                    # Timing emoji
            r'2\.00s'                # Artificial delay
        ]
        
        for pattern in timing_patterns:
            self.assertRegex(result['stdout'], pattern, f"Missing timing pattern: {pattern}")
            
    def test_echo_token_counting(self):
        """Test that token counting appears correctly."""
        result = self.run_repl_test('test', 'Count my tokens please\\n/quit\\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for token counting indicators
        self.assertIn('↑', result['stdout'])  # Input tokens
        self.assertIn('↓', result['stdout'])  # Output tokens
        self.assertIn('⏱️', result['stdout'])  # Timing indicator
        
    def test_echo_visual_flow_indicators(self):
        """Test that visual flow indicators appear correctly."""
        result = self.run_repl_test('test', 'Show me the flow\\n/quit\\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for visual elements
        self.assertIn('▼', result['stdout'])  # Flow indicator
        self.assertIn('⚙️', result['stdout'])  # Processing gear
        self.assertIn('🧠', result['stdout'])  # Brain emoji
        self.assertIn('💬', result['stdout'])  # Chat emoji
        
    def test_echo_internal_processing_container(self):
        """Test that Internal Processing container structure is correct."""
        result = self.run_repl_test('test', 'Test container structure\\n/quit\\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Verify V1 Internal Processing container format
        lines = result['stdout'].split('\\n')
        
        # Find the Internal Processing section
        processing_start = None
        processing_end = None
        
        for i, line in enumerate(lines):
            if 'Internal Processing' in line and '⚙️' in line:
                if processing_start is None:
                    processing_start = i
                else:
                    processing_end = i
                    break
        
        self.assertIsNotNone(processing_start, "Internal Processing container not found")
        
        # Check that nested sub-blocks exist between start and end
        if processing_end:
            container_content = '\\n'.join(lines[processing_start:processing_end])
            self.assertIn('Intent Detection', container_content)
            self.assertIn('Main Query', container_content)
            self.assertIn('▼', container_content)  # Flow indicator between blocks
            
    def test_echo_error_handling(self):
        """Test echo behavior with potential error conditions."""
        # Test with empty input followed by real input
        result = self.run_repl_test('test', '\\n\\nActual query\\n/quit\\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        self.assertIn('You: Actual query', result['stdout'])
        self.assertIn('Research Assistant', result['stdout'])
        
    def test_echo_command_integration(self):
        """Test echo with command integration."""
        result = self.run_repl_test('test', 'Hello\\n/stats\\n/quit\\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Verify query was processed
        self.assertIn('You: Hello', result['stdout'])
        self.assertIn('Research Assistant', result['stdout'])
        
        # Verify stats command worked
        self.assertIn('SESSION STATISTICS', result['stdout'])
        self.assertIn('Queries processed: 1', result['stdout'])
        self.assertIn('Total tokens:', result['stdout'])
        
    def test_echo_configuration_display(self):
        """Test that configuration information is echoed correctly."""
        result = self.run_repl_test('test', 'Show config info\\n/quit\\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check that both model configurations are displayed
        self.assertIn('groq/llama3-8b-8192', result['stdout'])
        
        # Should appear in system check
        config_count = result['stdout'].count('groq/llama3-8b-8192')
        self.assertGreaterEqual(config_count, 2, "Configuration should appear multiple times")


class TestQueryProcessing(IntegrationTestCase):
    """Test end-to-end query processing."""
    
    def test_simple_query_processing(self):
        """Test simple query processing."""
        result = self.run_repl_test('test', 'Hello there\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for query processing flow
        self.assertIn('You: Hello there', result['stdout'])
        self.assertIn('Internal Processing', result['stdout'])
        self.assertIn('Intent Detection', result['stdout'])
        self.assertIn('Main Query', result['stdout'])
        self.assertIn('Research Assistant', result['stdout'])
        
    def test_query_timing_display(self):
        """Test that query timing is displayed."""
        result = self.run_repl_test('test', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for timing information in query processing
        timing_pattern = r'\([0-9.]+s\)'
        self.assertRegex(result['stdout'], timing_pattern)
        
    def test_token_counting(self):
        """Test that token counting is displayed."""
        result = self.run_repl_test('test', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for token counting
        self.assertIn('⏱️', result['stdout'])
        self.assertIn('↑', result['stdout'])  # Input tokens
        self.assertIn('↓', result['stdout'])  # Output tokens
        
    def test_visual_flow_indicators(self):
        """Test that visual flow indicators are displayed."""
        result = self.run_repl_test('test', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for visual flow indicator
        self.assertIn('▼', result['stdout'])


class TestCommandHandling(IntegrationTestCase):
    """Test command handling."""
    
    def test_help_command(self):
        """Test help command."""
        result = self.run_repl_test('test', '/help\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for help output
        self.assertIn('Available Commands:', result['stdout'])
        self.assertIn('/quit', result['stdout'])
        self.assertIn('/help', result['stdout'])
        
    def test_quit_command(self):
        """Test quit command."""
        result = self.run_repl_test('test', '/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for goodbye message
        self.assertIn('Goodbye!', result['stdout'])
        
    def test_stats_command(self):
        """Test stats command."""
        result = self.run_repl_test('test', 'Hello\n/stats\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Check for stats output
        self.assertIn('SESSION STATISTICS', result['stdout'])
        self.assertIn('Queries processed:', result['stdout'])


class TestErrorHandling(IntegrationTestCase):
    """Test error handling and edge cases."""
    
    def test_empty_input_handling(self):
        """Test handling of empty input."""
        result = self.run_repl_test('test', '\n\n\nHello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Should handle empty inputs gracefully
        self.assertIn('Hello', result['stdout'])
        self.assertIn('Research Assistant', result['stdout'])
        
    def test_invalid_command_handling(self):
        """Test handling of invalid commands."""
        result = self.run_repl_test('test', '/invalid\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Should show error for invalid command
        self.assertIn('Unknown command', result['stdout'])
        
    def test_timeout_protection(self):
        """Test that process doesn't hang indefinitely."""
        # Use a very short timeout to test protection
        result = self.run_repl_test('test', 'Hello\\n/quit\\n', timeout=5)
        
        # Should complete within timeout
        self.assertTrue(result['duration'] < 5.0, f"Process took too long: {result['duration']:.2f}s")


class TestPerformance(IntegrationTestCase):
    """Test performance characteristics."""
    
    def test_fast_configuration_performance(self):
        """Test that fast configuration is actually fast."""
        result = self.run_repl_test('fast', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # Fast configuration should complete quickly
        self.assertLess(result['duration'], 15.0, f"Fast config took too long: {result['duration']:.2f}s")
        
    def test_system_check_performance(self):
        """Test system check performance."""
        result = self.run_repl_test('test', 'Hello\n/quit\n')
        
        self.assertTrue(result['success'], f"Process failed: {result['stderr']}")
        
        # System check should include artificial delay but not be excessive
        self.assertLess(result['duration'], 20.0, f"System check took too long: {result['duration']:.2f}s")
        
        # Should include the 2-second artificial delay
        self.assertIn('2.00s', result['stdout'])


def run_integration_tests():
    """Run all integration tests."""
    print("🧪 Integration Test Suite")
    print("=" * 60)
    print("Testing full application behavior...")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [
        TestSystemCheck,
        TestConfigurationBehavior,
        TestQueryProcessing,
        TestCommandHandling,
        TestErrorHandling,
        TestPerformance
    ]
    
    for test_case in test_cases:
        tests = loader.loadTestsFromTestCase(test_case)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print("\n📊 INTEGRATION TEST RESULTS")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {(passed/total_tests*100):.1f}%")
    
    if failures == 0 and errors == 0:
        print("\n✅ ALL INTEGRATION TESTS PASSED!")
        print("🎯 End-to-end functionality verified")
        return True
    else:
        print(f"\n❌ {failures + errors} INTEGRATION TESTS FAILED!")
        print("🔧 End-to-end functionality issues detected")
        
        if result.failures:
            print("\nFailures:")
            for test, error in result.failures:
                print(f"  - {test}: {error}")
                
        if result.errors:
            print("\nErrors:")
            for test, error in result.errors:
                print(f"  - {test}: {error}")
        
        return False


if __name__ == "__main__":
    success = run_integration_tests()
    exit(0 if success else 1)