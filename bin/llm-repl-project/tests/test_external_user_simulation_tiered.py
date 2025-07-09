#!/usr/bin/env python3
"""
Tiered External User Simulation Tests

These tests build up in tiers to validate exactly what works and what doesn't.
Each test fails LOUDLY with specific reasons and celebrates what works correctly.

TIER 1: Basic process spawning
TIER 2: Terminal interface basics  
TIER 3: Startup sequence validation
TIER 4: User interaction validation
TIER 5: Command validation
"""

import pexpect
import sys
import time
import unittest
from pathlib import Path


class TieredExternalUserSimulationTests(unittest.TestCase):
    """
    TIERED EXTERNAL VALIDATION: Build up confidence step by step.
    Each test is specific about what works and what fails.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.timeout = 15  # Shorter timeout for faster feedback
        self.project_root = Path(__file__).parent.parent
        
    def spawn_repl(self, timeout=None):
        """Spawn REPL with proper error handling."""
        if timeout is None:
            timeout = self.timeout
            
        try:
            child = pexpect.spawn('just run', timeout=timeout, cwd=self.project_root, encoding='utf-8')
            return child
        except Exception as e:
            self.fail(f"""
🚨 TIER 1 FAILURE: CANNOT SPAWN PROCESS 🚨

Expected: Successfully spawn 'just run' process
Actual: Failed to spawn process

Error: {e}

FUNDAMENTAL SYSTEM FAILURE: Cannot even start the program.
""")
    
    def test_tier_1_process_spawning_works(self):
        """
        TIER 1: Validate basic process spawning works.
        This is the foundation - if this fails, everything else will fail.
        """
        print("\n🔬 TIER 1: Testing process spawning...")
        
        child = self.spawn_repl(timeout=5)
        
        try:
            # Just verify the process started
            if child.isalive():
                print("✅ TIER 1 SUCCESS: Process spawned successfully")
                print(f"✅ TIER 1 SUCCESS: Process PID: {child.pid}")
                print("✅ TIER 1 SUCCESS: Process is alive and running")
            else:
                self.fail(f"""
🚨 TIER 1 FAILURE: PROCESS NOT ALIVE 🚨

Expected: Process should be alive after spawning
Actual: Process is not alive

Exit status: {child.exitstatus}

The program is not starting correctly.
""")
            
            # Clean up
            child.terminate()
            
        except Exception as e:
            self.fail(f"""
🚨 TIER 1 FAILURE: PROCESS SPAWN ERROR 🚨

Expected: Clean process spawn and basic validation
Actual: Exception during basic process validation

Error: {e}

FUNDAMENTAL SYSTEM FAILURE.
""")
    
    def test_tier_2_terminal_interface_responds(self):
        """
        TIER 2: Validate terminal interface responds to input.
        Tests that we can send input and get some response.
        """
        print("\n🔬 TIER 2: Testing terminal interface...")
        
        child = self.spawn_repl()
        
        try:
            # Wait a moment for any startup
            time.sleep(1)
            
            # Check if process is still alive
            if not child.isalive():
                self.fail(f"""
🚨 TIER 2 FAILURE: PROCESS DIED DURING STARTUP 🚨

Expected: Process should stay alive after startup
Actual: Process died during startup

Exit status: {child.exitstatus}
Before: {repr(child.before)}

The program crashes during startup.
""")
            
            print("✅ TIER 2 SUCCESS: Process survived startup period")
            
            # Try to send input and see if we get any response
            initial_output = child.before or ""
            child.sendline('test')
            
            # Wait for some response
            try:
                child.expect('.+', timeout=3)  # Any output at all
                print("✅ TIER 2 SUCCESS: Program responds to input")
                print(f"✅ TIER 2 SUCCESS: Got response after sending input")
            except pexpect.TIMEOUT:
                # Still alive but no response - that's a specific failure
                if child.isalive():
                    self.fail(f"""
🚨 TIER 2 FAILURE: NO RESPONSE TO INPUT 🚨

Expected: Program should respond to input within 3 seconds
Actual: No response to input 'test'

✅ WORKS: Process spawning
✅ WORKS: Process stays alive
❌ FAILS: Program doesn't respond to input

Initial output: {repr(initial_output)}
Buffer after input: {repr(child.before)}

The program is not processing user input.
""")
                else:
                    self.fail(f"""
🚨 TIER 2 FAILURE: PROCESS DIED AFTER INPUT 🚨

Expected: Program should respond to input
Actual: Process died after receiving input

Exit status: {child.exitstatus}
Before: {repr(child.before)}

The program crashes when processing input.
""")
            
            # Clean up
            child.terminate()
            
        except Exception as e:
            self.fail(f"""
🚨 TIER 2 FAILURE: TERMINAL INTERFACE ERROR 🚨

Expected: Basic terminal interface interaction
Actual: Exception during terminal interface test

Error: {e}

SYSTEM FAILURE: Terminal interface is broken.
""")
    
    def test_tier_3_startup_sequence_validation(self):
        """
        TIER 3: Validate startup sequence appears correctly.
        Tests that System_Check and Welcome blocks appear before user interaction.
        """
        print("\n🔬 TIER 3: Testing startup sequence...")
        
        child = self.spawn_repl()
        
        try:
            # Capture startup output
            time.sleep(2)  # Give startup time to complete
            
            startup_output = child.before or ""
            
            print("✅ TIER 3 SUCCESS: Captured startup output")
            print(f"✅ TIER 3 SUCCESS: Startup output length: {len(startup_output)} chars")
            
            # Check for System_Check block
            if 'System_Check' in startup_output:
                print("✅ TIER 3 SUCCESS: System_Check block found in startup")
            else:
                self.fail(f"""
🚨 TIER 3 FAILURE: NO SYSTEM_CHECK BLOCK 🚨

Expected: System_Check block should appear in startup sequence
Actual: No System_Check block found

✅ WORKS: Process spawning
✅ WORKS: Terminal interface
❌ FAILS: System_Check block missing

Startup output: {repr(startup_output[:500])}...

The startup sequence is not running correctly.
""")
            
            # Check for Welcome block
            if 'Welcome' in startup_output:
                print("✅ TIER 3 SUCCESS: Welcome block found in startup")
            else:
                self.fail(f"""
🚨 TIER 3 FAILURE: NO WELCOME BLOCK 🚨

Expected: Welcome block should appear in startup sequence
Actual: No Welcome block found

✅ WORKS: Process spawning
✅ WORKS: Terminal interface
✅ WORKS: System_Check block appears
❌ FAILS: Welcome block missing

Startup output: {repr(startup_output[:500])}...

The welcome message is not appearing.
""")
            
            # Check order: System_Check should come before Welcome
            system_check_pos = startup_output.find('System_Check')
            welcome_pos = startup_output.find('Welcome')
            
            if system_check_pos < welcome_pos:
                print("✅ TIER 3 SUCCESS: System_Check appears before Welcome")
            else:
                self.fail(f"""
🚨 TIER 3 FAILURE: WRONG STARTUP ORDER 🚨

Expected: System_Check should appear before Welcome
Actual: System_Check at {system_check_pos}, Welcome at {welcome_pos}

✅ WORKS: Process spawning
✅ WORKS: Terminal interface
✅ WORKS: System_Check block appears
✅ WORKS: Welcome block appears
❌ FAILS: Wrong order

Startup output: {repr(startup_output[:500])}...

The startup sequence is in the wrong order.
""")
            
            # Clean up
            child.terminate()
            
        except Exception as e:
            self.fail(f"""
🚨 TIER 3 FAILURE: STARTUP SEQUENCE ERROR 🚨

Expected: Valid startup sequence validation
Actual: Exception during startup sequence test

Error: {e}

SYSTEM FAILURE: Startup sequence validation failed.
""")
    
    def test_tier_4_user_interaction_validation(self):
        """
        TIER 4: Validate user interaction works correctly.
        Tests that user input produces expected response blocks.
        """
        print("\n🔬 TIER 4: Testing user interaction...")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup to complete
            time.sleep(2)
            
            # Look for prompt
            startup_output = child.before or ""
            
            if '>' in startup_output:
                print("✅ TIER 4 SUCCESS: Prompt found in startup output")
            else:
                self.fail(f"""
🚨 TIER 4 FAILURE: NO PROMPT FOUND 🚨

Expected: Prompt '>' should appear after startup
Actual: No prompt found

✅ WORKS: Process spawning
✅ WORKS: Terminal interface
❌ FAILS: No prompt for user input

Startup output: {repr(startup_output[:500])}...

Users cannot see where to type input.
""")
            
            # Send user input
            child.sendline('Hello')
            print("✅ TIER 4 SUCCESS: Sent user input 'Hello'")
            
            # Wait for User_Input block
            try:
                child.expect('User_Input', timeout=5)
                print("✅ TIER 4 SUCCESS: User_Input block appeared")
            except pexpect.TIMEOUT:
                self.fail(f"""
🚨 TIER 4 FAILURE: NO USER_INPUT BLOCK 🚨

Expected: User_Input block should appear after sending 'Hello'
Actual: No User_Input block within 5 seconds

✅ WORKS: Process spawning
✅ WORKS: Terminal interface  
✅ WORKS: Prompt appears
❌ FAILS: User_Input block missing

Buffer: {repr(child.before)}

The program is not processing user input correctly.
""")
            
            # Wait for Cognition block
            try:
                child.expect('Cognition', timeout=10)
                print("✅ TIER 4 SUCCESS: Cognition block appeared")
            except pexpect.TIMEOUT:
                self.fail(f"""
🚨 TIER 4 FAILURE: NO COGNITION BLOCK 🚨

Expected: Cognition block should appear after User_Input
Actual: No Cognition block within 10 seconds

✅ WORKS: Process spawning
✅ WORKS: Terminal interface
✅ WORKS: Prompt appears
✅ WORKS: User_Input block appears
❌ FAILS: Cognition block missing

Buffer: {repr(child.before)}

The program is not processing user input through cognition.
""")
            
            # Wait for Assistant_Response block
            try:
                child.expect('Assistant_Response', timeout=10)
                print("✅ TIER 4 SUCCESS: Assistant_Response block appeared")
            except pexpect.TIMEOUT:
                self.fail(f"""
🚨 TIER 4 FAILURE: NO ASSISTANT_RESPONSE BLOCK 🚨

Expected: Assistant_Response block should appear after Cognition
Actual: No Assistant_Response block within 10 seconds

✅ WORKS: Process spawning
✅ WORKS: Terminal interface
✅ WORKS: Prompt appears
✅ WORKS: User_Input block appears
✅ WORKS: Cognition block appears
❌ FAILS: Assistant_Response block missing

Buffer: {repr(child.before)}

The program is not generating responses to user input.
""")
            
            # Clean up
            child.terminate()
            
        except Exception as e:
            self.fail(f"""
🚨 TIER 4 FAILURE: USER INTERACTION ERROR 🚨

Expected: Complete user interaction validation
Actual: Exception during user interaction test

Error: {e}

SYSTEM FAILURE: User interaction is broken.
""")
    
    def test_tier_5_quit_command_validation(self):
        """
        TIER 5: Validate /quit command works correctly.
        Tests that the program exits cleanly when user types /quit.
        """
        print("\n🔬 TIER 5: Testing /quit command...")
        
        child = self.spawn_repl()
        
        try:
            # Wait for startup
            time.sleep(2)
            
            # Send quit command
            child.sendline('/quit')
            print("✅ TIER 5 SUCCESS: Sent /quit command")
            
            # Wait for goodbye message
            try:
                child.expect('Goodbye', timeout=5)
                print("✅ TIER 5 SUCCESS: Goodbye message appeared")
            except pexpect.TIMEOUT:
                self.fail(f"""
🚨 TIER 5 FAILURE: NO GOODBYE MESSAGE 🚨

Expected: Goodbye message should appear after /quit
Actual: No goodbye message within 5 seconds

✅ WORKS: Process spawning
✅ WORKS: Terminal interface
❌ FAILS: No goodbye message

Buffer: {repr(child.before)}

The /quit command is not working correctly.
""")
            
            # Wait for clean exit
            try:
                child.expect(pexpect.EOF, timeout=5)
                print("✅ TIER 5 SUCCESS: Process exited cleanly")
            except pexpect.TIMEOUT:
                self.fail(f"""
🚨 TIER 5 FAILURE: NO CLEAN EXIT 🚨

Expected: Process should exit cleanly after goodbye
Actual: Process still running after 5 seconds

✅ WORKS: Process spawning
✅ WORKS: Terminal interface
✅ WORKS: Goodbye message appears
❌ FAILS: Process doesn't exit

The program is not exiting cleanly.
""")
            
        except Exception as e:
            self.fail(f"""
🚨 TIER 5 FAILURE: QUIT COMMAND ERROR 🚨

Expected: Clean quit command validation
Actual: Exception during quit command test

Error: {e}

SYSTEM FAILURE: Quit command is broken.
""")


def run_tiered_external_user_simulation_tests():
    """Run tiered external user simulation tests with detailed feedback."""
    print("🔬 RUNNING TIERED EXTERNAL USER SIMULATION TESTS")
    print("=" * 60)
    print("These tests build up in tiers to validate exactly what works and what doesn't.")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TieredExternalUserSimulationTests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Analyze results
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"\n🎯 TIERED EXTERNAL USER SIMULATION RESULTS")
    print("=" * 60)
    print(f"Total Tiers: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    
    if failures == 0 and errors == 0:
        print(f"\n✅ ALL TIERS PASSED!")
        print("🎉 The program works correctly at every tier.")
        print("🔒 External validation confirms system integrity.")
        return True
    else:
        print(f"\n🚨 {failures + errors} TIER FAILURES!")
        print("💥 The program has specific tier-level failures.")
        print("🔧 Fix each tier before proceeding to the next.")
        print()
        
        if result.failures:
            print("💥 TIER FAILURES:")
            for test, error in result.failures:
                tier_num = test._testMethodName.split('_')[1]
                print(f"  - TIER {tier_num}: {test._testMethodName}")
                # Extract the specific failure reason
                lines = error.split('\n')
                for line in lines:
                    if '🚨' in line and 'FAILURE' in line:
                        print(f"    {line.strip()}")
                        break
                print()
                
        if result.errors:
            print("💥 TIER ERRORS:")
            for test, error in result.errors:
                tier_num = test._testMethodName.split('_')[1]
                print(f"  - TIER {tier_num}: {test._testMethodName}")
                print(f"    {error.split(':', 1)[0] if ':' in error else error}")
                print()
        
        return False


if __name__ == "__main__":
    success = run_tiered_external_user_simulation_tests()
    sys.exit(0 if success else 1)