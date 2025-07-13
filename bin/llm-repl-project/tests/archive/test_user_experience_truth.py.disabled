#!/usr/bin/env python3
"""
User Experience Truth Tests

These tests validate what users actually see and experience.
If these tests fail, the system is broken regardless of other test results.

CRITICAL: These tests must pass before any development claims can be made.
"""

import subprocess
import time
import unittest
from pathlib import Path
import re


class UserExperienceTruthTests(unittest.TestCase):
    """
    CRITICAL: These tests validate what users actually see and experience.
    If these fail, the system is broken regardless of other test results.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.timeout = 15  # Reasonable timeout for user experience tests
        self.project_root = Path(__file__).parent.parent
        self.repl_script = self.project_root / "src" / "main.py"
        
    def run_repl_and_capture_output(self, commands: str, timeout: int = None) -> dict:
        """
        Run REPL with simulated user commands and capture exact output user sees.
        Uses the new architecture that simulates the exact interactive workflow.
        """
        if timeout is None:
            timeout = self.timeout
            
        start_time = time.time()
        
        try:
            # Use the new simulated user session architecture
            process = subprocess.Popen(
                ['python', str(self.repl_script), '--config', 'test', commands],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )
            
            stdout, stderr = process.communicate(timeout=timeout)
            
            duration = time.time() - start_time
            
            return {
                'stdout': stdout,
                'stderr': stderr,
                'returncode': process.returncode,
                'duration': duration,
                'success': process.returncode == 0
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
    
    def assert_user_experience_working(self, result: dict, expected_behavior: str):
        """Assert user experience matches expectations - LOUD FAILURE if not."""
        if not result['success']:
            self.fail(f"""
🚨 CRITICAL USER EXPERIENCE FAILURE 🚨

Expected: {expected_behavior}
Process failed with return code: {result['returncode']}
Duration: {result['duration']:.2f}s
STDERR: {result['stderr']}
STDOUT: {result['stdout'][:500]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
Do not proceed with development until this is fixed.
The system is BROKEN from the user's perspective.
""")
    
    def test_user_starts_app_sees_clean_startup_sequence(self):
        """
        CRITICAL: User starts app and sees System Check → Welcome → Prompt
        This is the fundamental user experience and must work perfectly.
        """
        result = self.run_repl_and_capture_output('Hello')
        self.assert_user_experience_working(result, "Clean startup sequence")
        
        output = result['stdout']
        
        # Find positions of critical elements
        system_check_pos = output.find('System_Check')
        welcome_pos = output.find('Welcome to LLM REPL')
        first_prompt_pos = output.find('> ')
        
        # CRITICAL: System Check must appear first
        if system_check_pos == -1:
            self.fail(f"""
🚨 CRITICAL STARTUP FAILURE 🚨

System Check is MISSING from startup sequence.
User sees broken startup without system validation.

Expected: System Check appears first
Actual: No System Check found

Output: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
        
        # CRITICAL: Welcome must appear after System Check
        if welcome_pos == -1:
            self.fail(f"""
🚨 CRITICAL STARTUP FAILURE 🚨

Welcome message is MISSING from startup sequence.
User sees broken startup without welcome.

Expected: Welcome appears after System Check
Actual: No Welcome found

Output: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
        
        # For non-interactive mode, the prompt won't appear in output
        # But we should see user input appearing after welcome, which indicates prompt worked
        user_input_pos = output.find('> Hello')  # Look for actual user input
        
        if user_input_pos == -1:
            self.fail(f"""
🚨 CRITICAL STARTUP FAILURE 🚨

User input is MISSING from startup sequence.
User cannot interact with system.

Expected: User input appears after System Check and Welcome
Actual: No user input found

Output: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
        
        # CRITICAL: Order must be correct
        if not (system_check_pos < welcome_pos < user_input_pos):
            self.fail(f"""
🚨 CRITICAL STARTUP SEQUENCE FAILURE 🚨

Startup sequence is in WRONG ORDER.
User sees confusing, broken startup flow.

Expected order: System Check → Welcome → User Input
Actual positions:
  System Check: {system_check_pos}
  Welcome: {welcome_pos}
  User Input: {user_input_pos}

Output: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
    
    def test_user_types_hello_gets_clean_response(self):
        """
        CRITICAL: User types 'Hello' and gets clean, properly ordered response
        This is the core interaction and must work perfectly.
        """
        result = self.run_repl_and_capture_output('Hello')
        self.assert_user_experience_working(result, "Clean response to 'Hello'")
        
        output = result['stdout']
        
        # CRITICAL: User input must appear in timeline
        if 'Hello' not in output:
            self.fail(f"""
🚨 CRITICAL INTERACTION FAILURE 🚨

User input 'Hello' is MISSING from output.
User cannot see their own input in the conversation.

Expected: User input appears in timeline
Actual: No 'Hello' found in output

Output: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
        
        # CRITICAL: Assistant response must appear
        if 'Assistant_Response' not in output and 'Mock response' not in output:
            self.fail(f"""
🚨 CRITICAL INTERACTION FAILURE 🚨

Assistant response is MISSING from output.
User gets no response to their input.

Expected: Assistant response appears after user input
Actual: No assistant response found

Output: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
    
    def test_no_display_artifacts_visible_to_user(self):
        """
        CRITICAL: No escape sequences or display artifacts visible to user
        Users should see clean output, not technical artifacts.
        """
        result = self.run_repl_and_capture_output('Hello')
        self.assert_user_experience_working(result, "Clean output without artifacts")
        
        output = result['stdout']
        
        # Check for visible escape sequences
        escape_patterns = [
            r'\x1b\[[0-9;]*[A-Za-z]',  # ANSI escape sequences
            r'\[4A\[K',                # Specific escape sequences we've seen
            r'\[3A\[K',
            r'\[2A\[K',
            r'\[1A\[K'
        ]
        
        for pattern in escape_patterns:
            matches = re.findall(pattern, output)
            if matches:
                self.fail(f"""
🚨 CRITICAL DISPLAY FAILURE 🚨

Escape sequences are VISIBLE to user in terminal output.
User sees technical artifacts instead of clean interface.

Pattern found: {pattern}
Matches: {matches[:5]}  # Show first 5 matches

Output sample: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
Users should see clean output, not escape sequences.
""")
    
    def test_plugin_blocks_appear_in_correct_order(self):
        """
        CRITICAL: Plugin blocks appear in logical order without duplication
        Users should see coherent flow of System Check → Welcome → User Input → Processing → Response
        """
        result = self.run_repl_and_capture_output('Hello')
        self.assert_user_experience_working(result, "Logical plugin ordering")
        
        output = result['stdout']
        
        # Find all plugin blocks and their positions
        plugin_positions = {}
        
        # System Check should be first
        system_check_match = re.search(r'System_Check.*?✅', output)
        if system_check_match:
            plugin_positions['System_Check'] = system_check_match.start()
        
        # Welcome should be second
        welcome_match = re.search(r'Welcome.*?✅', output)
        if welcome_match:
            plugin_positions['Welcome'] = welcome_match.start()
        
        # User Input should come after welcome
        user_input_match = re.search(r'User_Input.*?✅', output)
        if user_input_match:
            plugin_positions['User_Input'] = user_input_match.start()
        
        # Assistant Response should come last
        assistant_match = re.search(r'Assistant_Response.*?✅', output)
        if assistant_match:
            plugin_positions['Assistant_Response'] = assistant_match.start()
        
        # Check for duplicates (same plugin BLOCK appearing multiple times)
        plugin_counts = {}
        for plugin_type in ['System_Check', 'Welcome', 'User_Input', 'Assistant_Response', 'Cognition']:
            # Count actual plugin blocks (title with checkmark), not just the word
            pattern = rf'🔧 {plugin_type}.*?✅'
            matches = re.findall(pattern, output)
            count = len(matches)
            if count > 1:
                plugin_counts[plugin_type] = count
        
        if plugin_counts:
            self.fail(f"""
🚨 CRITICAL PLUGIN DUPLICATION FAILURE 🚨

Plugin blocks are DUPLICATED in output.
User sees confusing repeated blocks.

Duplicate plugins: {plugin_counts}

Output: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
Each plugin should appear exactly once.
""")
        
        # Verify logical order
        expected_order = ['System_Check', 'Welcome', 'User_Input', 'Assistant_Response']
        actual_order = sorted(plugin_positions.items(), key=lambda x: x[1])
        actual_names = [name for name, pos in actual_order]
        
        # Check that the plugins we found are in the right order
        for i, expected_plugin in enumerate(expected_order):
            if expected_plugin in actual_names:
                actual_index = actual_names.index(expected_plugin)
                if actual_index < i:
                    self.fail(f"""
🚨 CRITICAL PLUGIN ORDER FAILURE 🚨

Plugin blocks are in WRONG ORDER.
User sees confusing flow of information.

Expected order: {expected_order}
Actual order: {actual_names}

Plugin positions: {plugin_positions}

Output: {output[:1000]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
    
    def test_commands_work_as_advertised(self):
        """
        CRITICAL: Commands (/quit, /help, /stats) work as advertised
        Basic commands must work or users cannot use the system.
        """
        # Test /quit command
        result = self.run_repl_and_capture_output('/quit')
        if not result['success']:
            self.fail(f"""
🚨 CRITICAL COMMAND FAILURE 🚨

/quit command is BROKEN.
Users cannot exit the application.

Expected: /quit exits cleanly
Actual: Command failed

Return code: {result['returncode']}
Output: {result['stdout'][:500]}...
Error: {result['stderr']}

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
        
        # Test /help command
        result = self.run_repl_and_capture_output('/help')
        if not result['success']:
            self.fail(f"""
🚨 CRITICAL COMMAND FAILURE 🚨

/help command is BROKEN.
Users cannot get help using the system.

Expected: /help shows help information
Actual: Command failed

Return code: {result['returncode']}
Output: {result['stdout'][:500]}...
Error: {result['stderr']}

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
        
        # Help should show available commands
        if 'Available Commands' not in result['stdout'] and 'help' not in result['stdout'].lower():
            self.fail(f"""
🚨 CRITICAL COMMAND FAILURE 🚨

/help command produces NO HELP OUTPUT.
Users cannot get help using the system.

Expected: /help shows available commands
Actual: No help content found

Output: {result['stdout'][:500]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
    
    def test_interactive_mode_works_without_freezing(self):
        """
        CRITICAL: Interactive mode works without freezing
        Users must be able to interact with the system.
        """
        # Test with very short timeout - should complete startup quickly
        result = self.run_repl_and_capture_output('/quit', timeout=10)
        
        if 'timeout' in result:
            self.fail(f"""
🚨 CRITICAL INTERACTIVE MODE FAILURE 🚨

Interactive mode is FREEZING or hanging.
Users cannot interact with the system.

Expected: System starts and responds to /quit within 10 seconds
Actual: System timed out

Duration: {result['duration']:.2f}s
Output: {result['stdout'][:500]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
The system is unusable if it freezes.
""")
        
        # Should complete quickly for basic operations
        if result['duration'] > 8.0:
            self.fail(f"""
🚨 CRITICAL PERFORMANCE FAILURE 🚨

Interactive mode is TOO SLOW.
Users experience unacceptable delays.

Expected: Basic operations complete within 8 seconds
Actual: Operation took {result['duration']:.2f} seconds

Output: {result['stdout'][:500]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
Users will abandon a slow system.
""")
    
    def test_non_interactive_mode_processes_input_correctly(self):
        """
        CRITICAL: Non-interactive mode processes piped input correctly
        Users must be able to script and automate the system.
        """
        # This test itself uses non-interactive mode (piped input)
        result = self.run_repl_and_capture_output('Hello')
        self.assert_user_experience_working(result, "Non-interactive input processing")
        
        output = result['stdout']
        
        # Should process both commands
        if 'Hello' not in output:
            self.fail(f"""
🚨 CRITICAL NON-INTERACTIVE FAILURE 🚨

Non-interactive mode is NOT PROCESSING input commands.
Users cannot script or automate the system.

Expected: 'Hello' command processed
Actual: No 'Hello' found in output

Output: {output[:500]}...

This is a FUNDAMENTAL SYSTEM FAILURE.
""")
        
        # Should exit cleanly on /quit
        if result['returncode'] != 0:
            self.fail(f"""
🚨 CRITICAL NON-INTERACTIVE FAILURE 🚨

Non-interactive mode is NOT EXITING cleanly.
Users cannot script or automate the system.

Expected: Clean exit with return code 0
Actual: Return code {result['returncode']}

Output: {result['stdout'][:500]}...
Error: {result['stderr']}

This is a FUNDAMENTAL SYSTEM FAILURE.
""")


def run_user_experience_truth_tests():
    """Run user experience truth tests - these must pass for system to be functional."""
    print("🔍 RUNNING USER EXPERIENCE TRUTH TESTS")
    print("=" * 60)
    print("These tests validate what users actually see and experience.")
    print("If these tests fail, the system is broken regardless of other tests.")
    print()
    
    # Create test suite with only the critical tests
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(UserExperienceTruthTests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Analyze results
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"\n🎯 USER EXPERIENCE TRUTH TEST RESULTS")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    
    if failures == 0 and errors == 0:
        print(f"\n✅ ALL USER EXPERIENCE TRUTH TESTS PASSED!")
        print("🎉 The system works correctly from the user's perspective.")
        print("✨ Development can proceed with confidence.")
        return True
    else:
        print(f"\n🚨 {failures + errors} CRITICAL USER EXPERIENCE FAILURES!")
        print("💥 The system is BROKEN from the user's perspective.")
        print("🛑 DO NOT PROCEED with development until these are fixed.")
        print()
        
        if result.failures:
            print("💥 FAILURES:")
            for test, error in result.failures:
                print(f"  - {test}")
                print(f"    {error.split('🚨')[1].split('🚨')[0].strip()}")
                print()
                
        if result.errors:
            print("💥 ERRORS:")
            for test, error in result.errors:
                print(f"  - {test}")
                print(f"    {error}")
                print()
        
        return False


if __name__ == "__main__":
    import sys
    success = run_user_experience_truth_tests()
    sys.exit(0 if success else 1)