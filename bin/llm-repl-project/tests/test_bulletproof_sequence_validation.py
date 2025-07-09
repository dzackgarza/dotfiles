#!/usr/bin/env python3
"""
Bulletproof Sequence Validation Tests

These tests validate the EXPECTED user experience sequence:
1. System_Check appears immediately on launch
2. Welcome appears after System_Check  
3. Prompt appears after Welcome (indicating ready for input)
4. User interaction works correctly after proper startup

LOUD REPORTING: Each test reports exactly what worked vs what failed.
"""

import pexpect
import sys
import time
import unittest
from pathlib import Path


class BulletproofSequenceValidationTests(unittest.TestCase):
    """
    BULLETPROOF: Tests that validate expected sequence without false alarms.
    Reports exactly what worked vs what failed.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.timeout = 10  # Reasonable timeout for each step
        self.project_root = Path(__file__).parent.parent
        
    def spawn_repl(self):
        """Spawn REPL with proper setup."""
        return pexpect.spawn('python src/main.py --config debug', timeout=self.timeout, cwd=self.project_root, encoding='utf-8')
    
    def test_correct_startup_sequence_timing(self):
        """
        BULLETPROOF: Test that startup sequence happens in correct order.
        EXPECTED: System_Check → Welcome → Prompt (before any user input)
        """
        print("\n🎯 TESTING CORRECT STARTUP SEQUENCE")
        print("=" * 60)
        print("EXPECTED: System_Check → Welcome → Prompt (before user input)")
        print()
        
        child = self.spawn_repl()
        
        try:
            # STEP 1: System_Check should appear FIRST (immediately on launch)
            print("🔍 STEP 1: Waiting for System_Check block...")
            try:
                child.expect('System_Check.*✅', timeout=5)
                print("✅ SUCCESS: System_Check block appeared immediately on launch")
            except pexpect.TIMEOUT:
                print("❌ FAILURE: System_Check block did NOT appear immediately")
                print("🔍 DIAGNOSIS: Startup sequence broken - System_Check should appear first")
                self.fail(f"""
🚨 STARTUP SEQUENCE FAILURE: NO IMMEDIATE SYSTEM_CHECK 🚨

EXPECTED: System_Check block should appear immediately when 'just run' is executed
ACTUAL: No System_Check block within 5 seconds of launch

✅ WHAT WORKED: Process spawned successfully
❌ WHAT FAILED: System_Check block missing from immediate startup

ARCHITECTURAL ISSUE: Startup sequence is not running immediately on launch.
The program should show System_Check block before waiting for user input.

Buffer content: {repr(child.before)}
""")
            
            # STEP 2: Welcome should appear SECOND (after System_Check)
            print("🔍 STEP 2: Waiting for Welcome block...")
            try:
                child.expect('Welcome to LLM REPL v3', timeout=3)
                print("✅ SUCCESS: Welcome block appeared after System_Check")
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Welcome block did NOT appear after System_Check")
                print("🔍 DIAGNOSIS: Startup sequence broken - Welcome should appear second")
                self.fail(f"""
🚨 STARTUP SEQUENCE FAILURE: NO WELCOME AFTER SYSTEM_CHECK 🚨

EXPECTED: Welcome block should appear after System_Check block
ACTUAL: No Welcome block within 3 seconds after System_Check

✅ WHAT WORKED: System_Check block appeared correctly
❌ WHAT FAILED: Welcome block missing from startup sequence

ARCHITECTURAL ISSUE: Welcome block is not appearing in correct sequence.
The program should show Welcome immediately after System_Check.

Buffer content: {repr(child.before)}
""")
            
            # STEP 3: Prompt should appear LAST (after Welcome, indicating ready for input)
            print("🔍 STEP 3: Waiting for prompt...")
            try:
                child.expect('>', timeout=2)
                print("✅ SUCCESS: Prompt appeared after Welcome (ready for user input)")
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Prompt did NOT appear after Welcome")
                print("🔍 DIAGNOSIS: Startup sequence broken - Prompt should appear last")
                self.fail(f"""
🚨 STARTUP SEQUENCE FAILURE: NO PROMPT AFTER WELCOME 🚨

EXPECTED: Prompt '>' should appear after Welcome block (indicating ready for input)
ACTUAL: No prompt within 2 seconds after Welcome

✅ WHAT WORKED: System_Check and Welcome blocks appeared correctly
❌ WHAT FAILED: Prompt missing from startup sequence

ARCHITECTURAL ISSUE: Prompt is not appearing after startup completion.
The program should show '>' prompt after Welcome to indicate ready for input.

Buffer content: {repr(child.before)}
""")
            
            print("\n🎉 STARTUP SEQUENCE VALIDATION COMPLETE!")
            print("✅ System_Check appeared immediately")
            print("✅ Welcome appeared after System_Check")  
            print("✅ Prompt appeared after Welcome")
            print("✅ Program is ready for user interaction")
            
            # Clean up
            child.sendline('/quit')
            child.expect(pexpect.EOF, timeout=3)
            
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
            self.fail(f"""
🚨 STARTUP SEQUENCE VALIDATION ERROR 🚨

EXPECTED: Clean startup sequence validation
ACTUAL: Unexpected error during test

Error: {e}
Buffer: {repr(child.before)}

SYSTEM ISSUE: Test framework encountered unexpected error.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_user_interaction_after_proper_startup(self):
        """
        BULLETPROOF: Test that user interaction works after startup sequence completes.
        EXPECTED: After startup sequence, user can type input and get proper response.
        """
        print("\n🎯 TESTING USER INTERACTION AFTER STARTUP")
        print("=" * 60)
        print("EXPECTED: After startup sequence, user input should work correctly")
        print()
        
        child = self.spawn_repl()
        
        try:
            # First ensure startup sequence completes
            print("🔍 ENSURING STARTUP SEQUENCE COMPLETES...")
            child.expect('System_Check.*✅', timeout=5)
            print("✅ System_Check appeared")
            
            child.expect('Welcome to LLM REPL v3', timeout=3)
            print("✅ Welcome appeared")
            
            child.expect('>', timeout=2)
            print("✅ Prompt appeared - startup complete, ready for user input")
            
            # Now test user interaction
            print("\n🔍 TESTING USER INPUT RESPONSE...")
            child.sendline('Hello')
            print("✅ Sent user input: 'Hello'")
            
            # Check for User_Input block
            try:
                child.expect('User_Input.*Hello', timeout=5)
                print("✅ SUCCESS: User_Input block appeared with correct content")
            except pexpect.TIMEOUT:
                print("❌ FAILURE: User_Input block did NOT appear")
                self.fail(f"""
🚨 USER INTERACTION FAILURE: NO USER_INPUT BLOCK 🚨

EXPECTED: User_Input block should appear after typing 'Hello'
ACTUAL: No User_Input block within 5 seconds

✅ WHAT WORKED: Startup sequence completed correctly
❌ WHAT FAILED: User input processing is broken

ARCHITECTURAL ISSUE: User input is not being processed into User_Input blocks.

Buffer content: {repr(child.before)}
""")
            
            # Check for Cognition block
            try:
                child.expect('Cognition.*✅', timeout=10)
                print("✅ SUCCESS: Cognition block appeared")
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Cognition block did NOT appear")
                self.fail(f"""
🚨 USER INTERACTION FAILURE: NO COGNITION BLOCK 🚨

EXPECTED: Cognition block should appear after User_Input
ACTUAL: No Cognition block within 10 seconds

✅ WHAT WORKED: Startup sequence and User_Input block
❌ WHAT FAILED: Cognition processing is broken

ARCHITECTURAL ISSUE: User input is not being processed through cognition.

Buffer content: {repr(child.before)}
""")
            
            # Check for Assistant_Response block
            try:
                child.expect('Assistant_Response.*✅', timeout=10)
                print("✅ SUCCESS: Assistant_Response block appeared")
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Assistant_Response block did NOT appear")
                self.fail(f"""
🚨 USER INTERACTION FAILURE: NO ASSISTANT_RESPONSE BLOCK 🚨

EXPECTED: Assistant_Response block should appear after Cognition
ACTUAL: No Assistant_Response block within 10 seconds

✅ WHAT WORKED: Startup sequence, User_Input, and Cognition blocks
❌ WHAT FAILED: Assistant response generation is broken

ARCHITECTURAL ISSUE: Cognition is not generating assistant responses.

Buffer content: {repr(child.before)}
""")
            
            print("\n🎉 USER INTERACTION VALIDATION COMPLETE!")
            print("✅ Startup sequence worked correctly")
            print("✅ User_Input block appeared")
            print("✅ Cognition block appeared")
            print("✅ Assistant_Response block appeared")
            print("✅ Full user interaction pipeline works")
            
            # Clean up
            child.sendline('/quit')
            child.expect(pexpect.EOF, timeout=3)
            
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
            self.fail(f"""
🚨 USER INTERACTION VALIDATION ERROR 🚨

EXPECTED: Clean user interaction validation
ACTUAL: Unexpected error during test

Error: {e}
Buffer: {repr(child.before)}

SYSTEM ISSUE: Test framework encountered unexpected error.
""")
        finally:
            if child.isalive():
                child.terminate()
    
    def test_quit_command_works_correctly(self):
        """
        BULLETPROOF: Test that /quit command works after startup sequence.
        EXPECTED: After startup, /quit should show goodbye and exit cleanly.
        """
        print("\n🎯 TESTING /QUIT COMMAND")
        print("=" * 60)
        print("EXPECTED: After startup, /quit should show goodbye and exit cleanly")
        print()
        
        child = self.spawn_repl()
        
        try:
            # First ensure startup sequence completes
            print("🔍 ENSURING STARTUP SEQUENCE COMPLETES...")
            child.expect('System_Check.*✅', timeout=5)
            child.expect('Welcome to LLM REPL v3', timeout=3)
            child.expect('>', timeout=2)
            print("✅ Startup sequence completed")
            
            # Test /quit command
            print("\n🔍 TESTING /QUIT COMMAND...")
            child.sendline('/quit')
            print("✅ Sent /quit command")
            
            # Check for goodbye message
            try:
                child.expect('Goodbye', timeout=5)
                print("✅ SUCCESS: Goodbye message appeared")
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Goodbye message did NOT appear")
                self.fail(f"""
🚨 QUIT COMMAND FAILURE: NO GOODBYE MESSAGE 🚨

EXPECTED: Goodbye message should appear after /quit command
ACTUAL: No goodbye message within 5 seconds

✅ WHAT WORKED: Startup sequence completed correctly
❌ WHAT FAILED: /quit command is not showing goodbye message

ARCHITECTURAL ISSUE: Quit command handling is broken.

Buffer content: {repr(child.before)}
""")
            
            # Check for clean exit
            try:
                child.expect(pexpect.EOF, timeout=3)
                print("✅ SUCCESS: Program exited cleanly")
            except pexpect.TIMEOUT:
                print("❌ FAILURE: Program did NOT exit cleanly")
                self.fail(f"""
🚨 QUIT COMMAND FAILURE: NO CLEAN EXIT 🚨

EXPECTED: Program should exit cleanly after goodbye message
ACTUAL: Program still running after 3 seconds

✅ WHAT WORKED: Startup sequence and goodbye message
❌ WHAT FAILED: Program is not exiting cleanly

ARCHITECTURAL ISSUE: Exit handling is broken.

Buffer content: {repr(child.before)}
""")
            
            print("\n🎉 QUIT COMMAND VALIDATION COMPLETE!")
            print("✅ Startup sequence worked correctly")
            print("✅ /quit command processed")
            print("✅ Goodbye message appeared")
            print("✅ Program exited cleanly")
            
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
            self.fail(f"""
🚨 QUIT COMMAND VALIDATION ERROR 🚨

EXPECTED: Clean /quit command validation
ACTUAL: Unexpected error during test

Error: {e}
Buffer: {repr(child.before)}

SYSTEM ISSUE: Test framework encountered unexpected error.
""")
        finally:
            if child.isalive():
                child.terminate()


def run_bulletproof_sequence_validation_tests():
    """Run bulletproof sequence validation tests with detailed reporting."""
    print("🎯 RUNNING BULLETPROOF SEQUENCE VALIDATION TESTS")
    print("=" * 80)
    print("These tests validate the EXPECTED user experience sequence.")
    print("Each test reports exactly what worked vs what failed.")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(BulletproofSequenceValidationTests)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Analyze results
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"\n🎯 BULLETPROOF SEQUENCE VALIDATION RESULTS")
    print("=" * 80)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    
    if failures == 0 and errors == 0:
        print(f"\n✅ ALL BULLETPROOF TESTS PASSED!")
        print("🎉 The program works exactly as expected.")
        print("🔒 Startup sequence and user interaction are correct.")
        return True
    else:
        print(f"\n🚨 {failures + errors} BULLETPROOF TEST FAILURES!")
        print("💥 The program has specific architectural issues.")
        print("🛠️ Fix the reported issues to align with expected behavior.")
        print()
        
        if result.failures:
            print("💥 ARCHITECTURAL FAILURES:")
            for test, error in result.failures:
                test_name = test._testMethodName.replace('test_', '').replace('_', ' ').title()
                print(f"  - {test_name}")
                # Extract the specific failure reason
                lines = error.split('\n')
                for line in lines:
                    if '🚨' in line and 'FAILURE' in line:
                        print(f"    {line.strip()}")
                        break
                print()
                
        if result.errors:
            print("💥 SYSTEM ERRORS:")
            for test, error in result.errors:
                test_name = test._testMethodName.replace('test_', '').replace('_', ' ').title()
                print(f"  - {test_name}")
                print(f"    {error.split(':', 1)[0] if ':' in error else error}")
                print()
        
        return False


if __name__ == "__main__":
    success = run_bulletproof_sequence_validation_tests()
    sys.exit(0 if success else 1)