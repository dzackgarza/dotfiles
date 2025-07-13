#!/usr/bin/env python3
"""
External User Simulation Tests

These tests use pexpect to simulate REAL user terminal interaction.
The program cannot lie to these tests because they interact with the actual
terminal interface exactly as a user would.

CRITICAL: These tests validate the true user experience that cannot be faked.
"""

import pexpect
import sys
import time
import unittest
from pathlib import Path


class ExternalUserSimulationTests(unittest.TestCase):
    """
    BULLETPROOF: These tests simulate real user terminal interaction.
    The program cannot fake or bypass these tests.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.timeout = 30  # Reasonable timeout for real interaction
        self.project_root = Path(__file__).parent.parent
        
    def spawn_repl(self, timeout=None):
        """Spawn a real REPL process that thinks it's in a real terminal."""
        if timeout is None:
            timeout = self.timeout
            
        # Change to project directory and use proper encoding
        child = pexpect.spawn('just run', timeout=timeout, cwd=self.project_root, encoding='utf-8')
        
        return child
    
    def test_startup_sequence_appears_in_correct_order(self):
        """
        BULLETPROOF: External validation of startup sequence.
        Program cannot fake this - we see exactly what users see.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for System_Check block to appear first
            child.expect('System_Check.*✅', timeout=10)
            
            # Wait for Welcome block to appear second
            child.expect('Welcome to LLM REPL v3', timeout=5)
            
            # Wait for prompt to appear (indicating ready for user input)
            child.expect('>', timeout=5)
            
            # Send quit to clean up
            child.sendline('/quit')
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

Startup sequence did not appear in correct order.
This is what the program actually shows to users.

Expected: System_Check → Welcome → Prompt
Actual: Timed out waiting for expected sequence

Buffer: {child.before}
Last output: {child.after}

The program is LYING about its startup sequence.
""")
        except pexpect.EOF:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

Program exited unexpectedly during startup.
This is what users actually experience.

Buffer: {child.before}

The program is BROKEN for real users.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_user_types_hello_gets_proper_response(self):
        """
        BULLETPROOF: External validation of user interaction.
        Simulates exactly what happens when user types 'Hello'.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for startup to complete
            child.expect('>', timeout=10)
            
            # Send user input exactly as user would
            child.sendline('Hello')
            
            # Validate that User_Input block appears
            child.expect('User_Input.*Hello', timeout=5)
            
            # Validate that Cognition block appears
            child.expect('Cognition.*✅', timeout=10)
            
            # Validate that Assistant_Response block appears
            child.expect('Assistant_Response.*✅', timeout=10)
            
            # Send quit to clean up
            child.sendline('/quit')
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

User interaction did not work as expected.
This is what users actually experience when they type 'Hello'.

Expected: User_Input → Cognition → Assistant_Response
Actual: Timed out waiting for expected response

Buffer: {child.before}
Last output: {child.after}

The program is BROKEN for real user interaction.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_multiple_user_interactions_work(self):
        """
        BULLETPROOF: External validation of multiple user interactions.
        Simulates real user having a conversation.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('>', timeout=10)
            
            # First interaction
            child.sendline('Hello')
            child.expect('Assistant_Response.*✅', timeout=10)
            
            # Second interaction
            child.sendline('How are you?')
            child.expect('User_Input.*How are you', timeout=5)
            child.expect('Assistant_Response.*✅', timeout=10)
            
            # Third interaction
            child.sendline('What can you do?')
            child.expect('User_Input.*What can you do', timeout=5)
            child.expect('Assistant_Response.*✅', timeout=10)
            
            # Clean exit
            child.sendline('/quit')
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

Multiple user interactions failed.
This is what users experience during real conversations.

Expected: Each input should get a proper response
Actual: Timed out during interaction

Buffer: {child.before}
Last output: {child.after}

The program is BROKEN for real conversations.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_help_command_works_externally(self):
        """
        BULLETPROOF: External validation of /help command.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('>', timeout=10)
            
            # Send help command
            child.sendline('/help')
            
            # Validate help content appears
            child.expect('Available Commands', timeout=5)
            child.expect('/quit', timeout=5)
            
            # Clean exit
            child.sendline('/quit')
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

/help command did not work as expected.
This is what users actually experience.

Expected: Help content with available commands
Actual: Timed out waiting for help

Buffer: {child.before}
Last output: {child.after}

The program's help system is BROKEN.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_stats_command_works_externally(self):
        """
        BULLETPROOF: External validation of /stats command.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('>', timeout=10)
            
            # Do some interaction first
            child.sendline('Hello')
            child.expect('Assistant_Response.*✅', timeout=10)
            
            # Send stats command
            child.sendline('/stats')
            
            # Validate stats content appears
            child.expect('SESSION STATISTICS', timeout=5)
            child.expect('Queries processed', timeout=5)
            
            # Clean exit
            child.sendline('/quit')
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

/stats command did not work as expected.
This is what users actually experience.

Expected: Session statistics display
Actual: Timed out waiting for stats

Buffer: {child.before}
Last output: {child.after}

The program's stats system is BROKEN.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_quit_command_works_externally(self):
        """
        BULLETPROOF: External validation of /quit command.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('>', timeout=10)
            
            # Send quit command
            child.sendline('/quit')
            
            # Validate goodbye message and clean exit
            child.expect('Goodbye', timeout=5)
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

/quit command did not work as expected.
This is what users actually experience.

Expected: Goodbye message and clean exit
Actual: Timed out waiting for quit

Buffer: {child.before}
Last output: {child.after}

The program's quit system is BROKEN.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_ctrl_c_handling_works_externally(self):
        """
        BULLETPROOF: External validation of Ctrl+C handling.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('>', timeout=10)
            
            # Send Ctrl+C
            child.sendcontrol('c')
            
            # Validate graceful exit
            child.expect('Goodbye', timeout=5)
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

Ctrl+C handling did not work as expected.
This is what users actually experience.

Expected: Graceful exit with goodbye message
Actual: Timed out waiting for exit

Buffer: {child.before}
Last output: {child.after}

The program's interrupt handling is BROKEN.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_empty_input_handling_externally(self):
        """
        BULLETPROOF: External validation of empty input handling.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('>', timeout=10)
            
            # Send empty input (just press Enter)
            child.sendline('')
            
            # Should still show prompt (not crash)
            child.expect('>', timeout=5)
            
            # Send actual input to verify system still works
            child.sendline('Hello')
            child.expect('Assistant_Response.*✅', timeout=10)
            
            # Clean exit
            child.sendline('/quit')
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

Empty input handling failed.
This is what users actually experience.

Expected: System handles empty input gracefully
Actual: Timed out or crashed

Buffer: {child.before}
Last output: {child.after}

The program's input handling is BROKEN.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_no_display_artifacts_externally(self):
        """
        BULLETPROOF: External validation that no display artifacts appear.
        """
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            child.expect('>', timeout=10)
            
            # Send input and capture all output
            child.sendline('Hello')
            child.expect('Assistant_Response.*✅', timeout=10)
            
            # Get all output as user would see it
            output = child.before + str(child.after)
            
            # Check for escape sequences that users shouldn't see
            escape_patterns = [
                '\x1b[4A',  # Move up 4 lines
                '\x1b[K',   # Clear line
                '\x1b[3A',  # Move up 3 lines
                '\x1b[2A',  # Move up 2 lines
                '\x1b[1A',  # Move up 1 line
            ]
            
            for pattern in escape_patterns:
                if pattern in output:
                    self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

Display artifacts visible to users.
This is what users actually see in their terminal.

Pattern found: {repr(pattern)}
In output: {repr(output[:500])}...

The program shows TECHNICAL ARTIFACTS to users.
""")
            
            # Clean exit
            child.sendline('/quit')
            child.expect(pexpect.EOF)
            
        except pexpect.TIMEOUT as e:
            self.fail(f"""
🚨 EXTERNAL VALIDATION FAILURE 🚨

Could not complete display artifacts test.

Buffer: {child.before}
Last output: {child.after}

The program may be BROKEN.
""")
        finally:
            if child.isalive():
                child.terminate()


def run_external_user_simulation_tests():
    """Run external user simulation tests that cannot be faked."""
    print("🔍 RUNNING EXTERNAL USER SIMULATION TESTS")
    print("=" * 60)
    print("These tests simulate REAL user terminal interaction.")
    print("The program cannot lie to these tests.")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(ExternalUserSimulationTests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Analyze results
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"\n🎯 EXTERNAL USER SIMULATION TEST RESULTS")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    
    if failures == 0 and errors == 0:
        print(f"\n✅ ALL EXTERNAL USER SIMULATION TESTS PASSED!")
        print("🎉 The program works correctly from REAL user perspective.")
        print("🔒 External validation confirms the system is bulletproof.")
        return True
    else:
        print(f"\n🚨 {failures + errors} EXTERNAL VALIDATION FAILURES!")
        print("💥 The program is BROKEN from REAL user perspective.")
        print("🛑 These are CRITICAL failures that users actually experience.")
        print()
        
        if result.failures:
            print("💥 FAILURES:")
            for test, error in result.failures:
                print(f"  - {test}")
                # Extract just the first line of the error for summary
                error_lines = error.split('\n')
                for line in error_lines:
                    if '🚨' in line:
                        print(f"    {line.strip()}")
                        break
                print()
                
        if result.errors:
            print("💥 ERRORS:")
            for test, error in result.errors:
                print(f"  - {test}")
                print(f"    {error.split(':', 1)[0] if ':' in error else error}")
                print()
        
        return False


if __name__ == "__main__":
    success = run_external_user_simulation_tests()
    sys.exit(0 if success else 1)