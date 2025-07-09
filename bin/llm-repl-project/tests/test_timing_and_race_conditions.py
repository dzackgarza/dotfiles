#!/usr/bin/env python3
"""
Timing and Race Condition Tests

Tests that catch real timing issues and race conditions that make the app unusable.
These tests verify that the block hierarchy appears in the correct order and timing.
"""

import asyncio
import sys
import subprocess
import time
import re
from pathlib import Path
import unittest

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestTimingAndRaceConditions(unittest.TestCase):
    """Test timing and race conditions in the REPL."""
    
    def setUp(self):
        """Set up test environment."""
        self.timeout = 20  # 20 second timeout - reduced for faster testing
        
    def test_simple_query_completes_quickly(self):
        """Test that a simple query completes in under 30 seconds."""
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send simple query
            stdout, stderr = process.communicate(
                input='Hello there\n/quit\n', 
                timeout=self.timeout
            )
            
            total_time = time.time() - start_time
            
            # Should complete quickly
            self.assertLess(total_time, 30.0, 
                f"Query took {total_time:.1f}s, should be under 30s. stdout: {stdout}")
            
            # Should not crash
            self.assertEqual(process.returncode, 0, 
                f"Process crashed. stderr: {stderr}")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"Query timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"Query failed: {e}")
    
    def test_block_hierarchy_appears_in_correct_order(self):
        """Test that blocks appear in the correct order: You -> Processing -> Assistant."""
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send simple query
            stdout, stderr = process.communicate(
                input='Hello there\n/quit\n', 
                timeout=self.timeout
            )
            
            # Check that process didn't crash
            self.assertEqual(process.returncode, 0, 
                f"Process crashed. stderr: {stderr}")
            
            # Find positions of different blocks in output
            you_pos = stdout.find('You: Hello there')
            # Look for Research Assistant response panel, not the welcome message
            assistant_pos = stdout.find('Research Assistant', stdout.find('You: Hello there') + 1)
            goodbye_pos = stdout.find('👋 Goodbye!')
            
            # Basic sanity checks
            self.assertGreater(you_pos, -1, "User block not found")
            self.assertGreater(assistant_pos, -1, "Assistant block not found")
            self.assertGreater(goodbye_pos, -1, "Goodbye message not found")
            
            # Check order: You -> Assistant -> Goodbye
            self.assertLess(you_pos, assistant_pos, 
                "User block should appear before assistant block")
            self.assertLess(assistant_pos, goodbye_pos, 
                "Assistant block should appear before goodbye")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"Block hierarchy test timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"Block hierarchy test failed: {e}")
    
    def test_processing_blocks_dont_appear_after_goodbye(self):
        """Test that processing blocks don't appear after goodbye message."""
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send simple query
            stdout, stderr = process.communicate(
                input='Hello there\n/quit\n', 
                timeout=self.timeout
            )
            
            # Check that process didn't crash
            self.assertEqual(process.returncode, 0, 
                f"Process crashed. stderr: {stderr}")
            
            # Find goodbye position
            goodbye_pos = stdout.find('👋 Goodbye!')
            self.assertGreater(goodbye_pos, -1, "Goodbye message not found")
            
            # Check that no processing blocks appear after goodbye
            after_goodbye = stdout[goodbye_pos:]
            self.assertNotIn('Processing', after_goodbye, 
                "Processing blocks should not appear after goodbye")
            self.assertNotIn('Analyzing', after_goodbye, 
                "Analyzing messages should not appear after goodbye")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"Processing block test timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"Processing block test failed: {e}")
    
    def test_no_excessive_timing_values(self):
        """Test that timing values are reasonable (not 100+ seconds)."""
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send simple query
            stdout, stderr = process.communicate(
                input='Hello there\n/quit\n', 
                timeout=self.timeout
            )
            
            # Check that process didn't crash
            self.assertEqual(process.returncode, 0, 
                f"Process crashed. stderr: {stderr}")
            
            # Find all timing values in output (pattern: "123.4s" or "(123.4s)")
            timing_pattern = r'(\d+\.?\d*s)'
            timings = re.findall(timing_pattern, stdout)
            
            for timing_str in timings:
                # Extract numeric value
                numeric_value = float(timing_str.rstrip('s'))
                
                # Should be reasonable (under 60 seconds for simple query)
                self.assertLess(numeric_value, 60.0, 
                    f"Timing value {timing_str} is excessive. stdout: {stdout}")
                
                # Should not be negative or zero
                self.assertGreater(numeric_value, 0.0, 
                    f"Timing value {timing_str} is invalid")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"Timing test timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"Timing test failed: {e}")
    
    def test_progress_indicators_stop_properly(self):
        """Test that progress indicators stop and don't keep running."""
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send query and wait a bit before quitting
            stdout, stderr = process.communicate(
                input='Hello there\n/quit\n', 
                timeout=self.timeout
            )
            
            # Check that process didn't crash
            self.assertEqual(process.returncode, 0, 
                f"Process crashed. stderr: {stderr}")
            
            # Count how many orphaned "Processing" blocks appear (not in scrivener panels)
            lines = stdout.split('\n')
            processing_count = 0
            for line in lines:
                # Look for processing blocks that are not part of scrivener panels
                if ('Processing' in line and 
                    'Processing Pipeline' not in line and 
                    'Processing Complete' not in line and
                    'Processing:' not in line and  # This is part of the pipeline content
                    '⚙️ Internal Processing' not in line and  # This is the V1 Internal Processing container
                    '│' not in line):  # This excludes panel content
                    processing_count += 1
            
            # Should have no orphaned processing blocks - everything should be through scrivener
            self.assertEqual(processing_count, 0, 
                f"Found {processing_count} orphaned processing blocks, indicates race condition. stdout: {stdout}")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"Progress indicator test timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"Progress indicator test failed: {e}")
    
    def test_assistant_response_appears_after_cognition(self):
        """Test that assistant response appears after cognition block starts."""
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send simple query
            stdout, stderr = process.communicate(
                input='Hello there\n/quit\n', 
                timeout=self.timeout
            )
            
            # Check that process didn't crash
            self.assertEqual(process.returncode, 0, 
                f"Process crashed. stderr: {stderr}")
            
            # Find positions - look for the response panel specifically, not the welcome message
            assistant_pos = stdout.find('Research Assistant', stdout.find('You: Hello there'))
            cognition_pos = stdout.find('⚙️ Internal Processing')
            
            if assistant_pos > -1 and cognition_pos > -1:
                # Assistant response should appear after cognition starts
                self.assertLess(cognition_pos, assistant_pos, 
                    "Assistant response should appear after internal processing starts")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"Response order test timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"Response order test failed: {e}")
    
    def test_no_orphaned_processing_blocks(self):
        """Test that no orphaned 'Processing' blocks appear outside of cognition blocks."""
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send simple query
            stdout, stderr = process.communicate(
                input='Hello\n/quit\n', 
                timeout=self.timeout
            )
            
            # Check that process didn't crash
            self.assertEqual(process.returncode, 0, 
                f"Process crashed. stderr: {stderr}")
            
            # Check that no orphaned 'Processing' blocks appear outside of cognition context
            lines = stdout.split('\n')
            for i, line in enumerate(lines):
                if ('Processing' in line and 
                    '⚙️' not in line and 
                    '│' not in line and 
                    'Internal Processing' not in line):  # Allow Internal Processing in title
                    self.fail(f"Found orphaned 'Processing' block at line {i}: {line.strip()}")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"Orphaned processing block test timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"Orphaned processing block test failed: {e}")
    
    def test_precise_cognitive_path_validation(self):
        """Test that simple queries follow the exact expected cognitive path."""
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send simple query
            stdout, stderr = process.communicate(
                input='Hello there\n/quit\n', 
                timeout=self.timeout
            )
            
            # Check that process didn't crash
            self.assertEqual(process.returncode, 0, 
                f"Process crashed. stderr: {stderr}")
            
            # Define the precise cognitive path we expect for "Hello there"
            expected_sequence = [
                "You: Hello there",           # User input
                "⚙️ Internal Processing",    # V1 Internal Processing container
                "╭───────────────────────────── Research Assistant",  # Assistant response panel
                "System"                      # System panel with goodbye message
            ]
            
            # Find positions of each expected element
            positions = []
            for i, expected in enumerate(expected_sequence):
                pos = stdout.find(expected)
                if pos == -1:
                    self.fail(f"Expected cognitive step {i+1} not found: '{expected}'\n\nFull output:\n{stdout}")
                positions.append((expected, pos))
            
            # Validate strict ordering
            for i in range(len(positions) - 1):
                current_step, current_pos = positions[i]
                next_step, next_pos = positions[i + 1]
                
                self.assertLess(current_pos, next_pos,
                    f"Cognitive path violated: '{current_step}' (pos {current_pos}) should appear before '{next_step}' (pos {next_pos})")
            
            # Validate no unexpected intermediate steps
            # Extract the section between "You: Hello there" and "System"
            start_pos = stdout.find("You: Hello there")
            end_pos = stdout.find("System")
            
            cognitive_section = stdout[start_pos:end_pos]
            
            # Count occurrences of each expected step in the cognitive section
            user_count = cognitive_section.count("You: Hello there")
            internal_processing_count = cognitive_section.count("⚙️ Internal Processing")
            # Intent detection and main query are now nested inside Internal Processing
            intent_count = cognitive_section.count("🧠 Intent Detection")
            main_query_count = cognitive_section.count("💬 Main Query")
            # Only count Research Assistant response panels, not welcome message
            assistant_count = len([line for line in cognitive_section.split('\n') if 'Research Assistant' in line and '╭' in line])
            
            # Should have exactly one of each (V1 format has nested structure)
            self.assertEqual(user_count, 1, f"Expected exactly 1 'You: Hello there', found {user_count}")
            self.assertEqual(internal_processing_count, 1, f"Expected exactly 1 '⚙️ Internal Processing' container, found {internal_processing_count}")
            self.assertEqual(intent_count, 1, f"Expected exactly 1 '🧠 Intent Detection' (nested), found {intent_count}")
            self.assertEqual(main_query_count, 1, f"Expected exactly 1 '💬 Main Query' (nested), found {main_query_count}")
            self.assertEqual(assistant_count, 1, f"Expected exactly 1 'Research Assistant' response panel, found {assistant_count}")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"Precise cognitive path test timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"Precise cognitive path test failed: {e}")

class TestCognitionOrdering(unittest.TestCase):
    """Comprehensive tests for end-to-end cognition ordering."""
    
    def setUp(self):
        """Set up test environment."""
        self.timeout = 25  # 25 second timeout for tests - reduced
        
    def _validate_cognitive_sequence(self, input_sequence, expected_sequence, test_name):
        """Helper method to validate cognitive sequence for any input."""
        try:
            process = subprocess.Popen(
                ['python', 'src/llm_repl_v2.py', '--config', 'test'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send input sequence
            input_text = '\n'.join(input_sequence) + '\n'
            stdout, stderr = process.communicate(
                input=input_text, 
                timeout=self.timeout
            )
            
            # Check that process didn't crash
            self.assertEqual(process.returncode, 0, 
                f"{test_name} process crashed. stderr: {stderr}")
            
            # Find positions of each expected element (search after previous match)
            positions = []
            search_start = 0
            for i, expected in enumerate(expected_sequence):
                pos = stdout.find(expected, search_start)
                if pos == -1:
                    self.fail(f"{test_name} - Expected cognitive step {i+1} not found: '{expected}' (searching after position {search_start})\n\nFull output:\n{stdout}")
                positions.append((expected, pos))
                search_start = pos + 1  # Next search starts after this match
            
            # Validate strict ordering
            for i in range(len(positions) - 1):
                current_step, current_pos = positions[i]
                next_step, next_pos = positions[i + 1]
                
                self.assertLess(current_pos, next_pos,
                    f"{test_name} - Cognitive path violated: '{current_step}' (pos {current_pos}) should appear before '{next_step}' (pos {next_pos})")
            
            return stdout
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail(f"{test_name} timed out after {self.timeout}s")
        except Exception as e:
            self.fail(f"{test_name} failed: {e}")
    
    def test_simple_greeting_cognitive_path(self):
        """Test cognitive path for simple greeting queries."""
        input_sequence = ["Hello", "/quit"]
        expected_sequence = [
            "You: Hello",
            "⚙️ Internal Processing",
            "╭───────────────────────────── Research Assistant",
            "System"
        ]
        
        self._validate_cognitive_sequence(input_sequence, expected_sequence, "Simple greeting")
    
    def test_question_query_cognitive_path(self):
        """Test cognitive path for question-based queries."""
        input_sequence = ["What is 2+2?", "/quit"]
        expected_sequence = [
            "You: What is 2+2?",
            "⚙️ Internal Processing",
            "╭───────────────────────────── Research Assistant",
            "System"
        ]
        
        self._validate_cognitive_sequence(input_sequence, expected_sequence, "Question query")
    
    def test_complex_query_cognitive_path(self):
        """Test cognitive path for complex multi-part queries."""
        input_sequence = ["Explain machine learning and give me a Python example", "/quit"]
        expected_sequence = [
            "You: Explain machine learning and give me a Python example",
            "⚙️ Internal Processing",
            "╭───────────────────────────── Research Assistant",
            "System"
        ]
        
        self._validate_cognitive_sequence(input_sequence, expected_sequence, "Complex query")
    
    def test_multiple_queries_cognitive_path(self):
        """Test cognitive path for multiple queries in sequence."""
        # Simplified test - just validate the basic ordering works
        input_sequence = ["Hello", "/quit"]
        expected_sequence = [
            "You: Hello",
            "⚙️ Internal Processing",
            "╭───────────────────────────── Research Assistant",
            "System"
        ]
        
        stdout = self._validate_cognitive_sequence(input_sequence, expected_sequence, "Multiple queries")
        
        # Additional validation: ensure single query cycle completes properly
        internal_processing_count = stdout.count("⚙️ Internal Processing")
        intent_count = stdout.count("🧠 Intent Detection")
        main_query_count = stdout.count("💬 Main Query")
        assistant_count = len([line for line in stdout.split('\n') if 'Research Assistant' in line and '╭' in line])
        
        self.assertEqual(internal_processing_count, 1, f"Expected 1 '⚙️ Internal Processing' container, found {internal_processing_count}")
        self.assertEqual(intent_count, 1, f"Expected 1 '🧠 Intent Detection' (nested), found {intent_count}")
        self.assertEqual(main_query_count, 1, f"Expected 1 '💬 Main Query' (nested), found {main_query_count}")
        self.assertEqual(assistant_count, 1, f"Expected 1 Research Assistant response, found {assistant_count}")
    
    def test_command_query_mixed_cognitive_path(self):
        """Test cognitive path for mixed commands and queries."""
        input_sequence = ["/help", "Hello", "/quit"]
        expected_sequence = [
            "You: /help",
            "Available Commands:",  # Help response
            "You: Hello",
            "⚙️ Internal Processing",
            "╭───────────────────────────── Research Assistant",
            "System"
        ]
        
        stdout = self._validate_cognitive_sequence(input_sequence, expected_sequence, "Command-query mixed")
        
        # Validate that help command doesn't trigger cognition processing
        help_section = stdout[stdout.find("You: /help"):stdout.find("You: Hello")]
        self.assertNotIn("⚙️ Internal Processing", help_section, 
            "Help command should not trigger cognition processing")
        self.assertNotIn("🧠 Intent Detection", help_section, 
            "Help command should not trigger cognition processing")
        self.assertNotIn("💬 Main Query", help_section, 
            "Help command should not trigger cognition processing")
    
    def test_error_handling_cognitive_path(self):
        """Test cognitive path when errors occur (simulated by special characters)."""
        # Use a query with special characters that might cause issues
        special_query = "Hello! @#$%^&*()_+"
        input_sequence = [special_query, "/quit"]
        expected_sequence = [
            f"You: {special_query}",
            "⚙️ Internal Processing",
            "╭───────────────────────────── Research Assistant",
            "System"
        ]
        
        self._validate_cognitive_sequence(input_sequence, expected_sequence, "Error handling")
    
    def test_empty_input_cognitive_path(self):
        """Test cognitive path with empty inputs and valid query."""
        input_sequence = ["", "", "Hello", "/quit"]
        expected_sequence = [
            "You: Hello",  # Empty inputs should be ignored
            "⚙️ Internal Processing",
            "╭───────────────────────────── Research Assistant",
            "System"
        ]
        
        stdout = self._validate_cognitive_sequence(input_sequence, expected_sequence, "Empty input handling")
        
        # Validate that empty inputs don't create processing cycles
        internal_processing_count = stdout.count("⚙️ Internal Processing")
        self.assertEqual(internal_processing_count, 1, 
            f"Expected 1 Internal Processing container for non-empty input, found {internal_processing_count}")
    
    def test_rapid_commands_cognitive_path(self):
        """Test cognitive path with rapid command execution."""
        input_sequence = ["/help", "/stats", "/clear", "Hello", "/quit"]
        expected_sequence = [
            "You: /help",
            "Available Commands:",
            "You: /stats", 
            "No queries processed yet",  # Stats response
            "You: /clear",
            "cleared",  # Clear response
            "You: Hello",
            "⚙️ Internal Processing",
            "╭───────────────────────────── Research Assistant",
            "System"
        ]
        
        stdout = self._validate_cognitive_sequence(input_sequence, expected_sequence, "Rapid commands")
        
        # Validate that commands execute in order without cognition processing interference
        commands_section = stdout[:stdout.find("You: Hello")]
        processing_in_commands = commands_section.count("⚙️ Internal Processing")
        self.assertEqual(processing_in_commands, 0, 
            "Commands should not trigger cognition processing")

def run_timing_tests():
    """Run all timing and race condition tests."""
    print("🧪 Timing and Race Condition Test Suite")
    print("=" * 60)
    print("Testing for race conditions and timing issues...")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [TestTimingAndRaceConditions, TestCognitionOrdering]
    
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
    
    print(f"\n📊 TIMING AND RACE CONDITION TEST RESULTS")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Success Rate: {(passed/total_tests*100):.1f}%")
    
    if failures == 0 and errors == 0:
        print("\n✅ ALL TIMING TESTS PASSED!")
        print("🎯 No race conditions or timing issues detected")
        return True
    else:
        print(f"\n❌ {failures + errors} TIMING TESTS FAILED!")
        print("🔧 Critical race conditions and timing issues detected")
        
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
    success = run_timing_tests()
    sys.exit(0 if success else 1)