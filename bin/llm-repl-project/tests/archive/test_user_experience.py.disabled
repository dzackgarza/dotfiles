#!/usr/bin/env python3
"""
End-to-End User Experience Tests

These tests simulate actual user workflows to catch real-world failures
that unit tests miss. They test the complete user experience from start to finish.
"""

import asyncio
import sys
import tempfile
import os
import subprocess
import time
from pathlib import Path
import unittest

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestUserExperience(unittest.TestCase):
    """Test actual user workflows end-to-end."""
    
    def setUp(self):
        """Set up test environment."""
        self.timeout = 30  # 30 second timeout for tests
        
    def test_repl_starts_without_crashing(self):
        """Test that 'just run' starts the REPL without immediate crashes."""
        try:
            # Start the REPL process
            process = subprocess.Popen(
                ['python', 'src/main.py', '--config', 'debug'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send quit command immediately
            stdout, stderr = process.communicate(input='/quit\n', timeout=self.timeout)
            
            # Check that it didn't crash
            self.assertEqual(process.returncode, 0, f"REPL crashed on startup. stderr: {stderr}")
            
            # Check that welcome message appeared - v3 uses different text
            self.assertIn("Welcome to LLM REPL v3", stdout, "Welcome message not displayed")
            self.assertIn("Plugin Architecture", stdout, "Plugin architecture not mentioned")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("REPL startup timed out")
        except Exception as e:
            self.fail(f"REPL startup failed: {e}")
    
    def test_help_command_works(self):
        """Test that /help command works without errors."""
        try:
            process = subprocess.Popen(
                ['python', 'src/main.py', '--config', 'debug'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send help command then quit
            stdout, stderr = process.communicate(input='/help\n/quit\n', timeout=self.timeout)
            
            # Check that it didn't crash
            self.assertEqual(process.returncode, 0, f"Help command crashed. stderr: {stderr}")
            
            # Check that help content appeared
            self.assertIn("Available Commands", stdout, "Help content not displayed")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("Help command timed out")
        except Exception as e:
            self.fail(f"Help command failed: {e}")
    
    def test_query_processing_works_or_shows_error(self):
        """Test that query processing either works or shows appropriate error."""
        try:
            process = subprocess.Popen(
                ['python', 'src/main.py', '--config', 'debug'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send a simple query 
            stdout, stderr = process.communicate(
                input='What is 2+2?\n/quit\n', 
                timeout=self.timeout
            )
            
            # Check that it didn't crash completely
            self.assertEqual(process.returncode, 0, f"Query processing crashed. stderr: {stderr}")
            
            # Should either show response or graceful error message
            # If Ollama is running, we get "Research Assistant" response
            # If not, we get "Error" or "Unable to connect"
            self.assertTrue(
                "Research Assistant" in stdout or "Error" in stdout or "Unable to connect" in stdout,
                f"No response or error message displayed. stdout: {stdout[:200]}..."
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("Query processing timed out")
        except Exception as e:
            self.fail(f"Query processing failed: {e}")
    
    def test_stats_command_works(self):
        """Test that /stats command works without errors."""
        try:
            process = subprocess.Popen(
                ['python', 'src/main.py', '--config', 'debug'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send stats command then quit
            stdout, stderr = process.communicate(input='/stats\n/quit\n', timeout=self.timeout)
            
            # Check that it didn't crash
            self.assertEqual(process.returncode, 0, f"Stats command crashed. stderr: {stderr}")
            
            # Check that stats content appeared (even if no queries processed)
            self.assertTrue(
                "No queries processed" in stdout or "SESSION STATISTICS" in stdout,
                "Stats content not displayed"
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("Stats command timed out")
        except Exception as e:
            self.fail(f"Stats command failed: {e}")
    
    def test_clear_command_works(self):
        """Test that /clear command works without errors."""
        try:
            process = subprocess.Popen(
                ['python', 'src/main.py', '--config', 'debug'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send clear command then quit
            stdout, stderr = process.communicate(input='/clear\n/quit\n', timeout=self.timeout)
            
            # Check that it didn't crash
            self.assertEqual(process.returncode, 0, f"Clear command crashed. stderr: {stderr}")
            
            # Check that clear confirmation appeared
            self.assertIn("cleared", stdout, "Clear confirmation not displayed")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("Clear command timed out")
        except Exception as e:
            self.fail(f"Clear command failed: {e}")
    
    def test_invalid_command_handling(self):
        """Test that invalid commands are handled gracefully."""
        try:
            process = subprocess.Popen(
                ['python', 'src/main.py', '--config', 'debug'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send invalid command then quit
            stdout, stderr = process.communicate(input='/invalid\n/quit\n', timeout=self.timeout)
            
            # Check that it didn't crash
            self.assertEqual(process.returncode, 0, f"Invalid command crashed. stderr: {stderr}")
            
            # Check that error message appeared
            self.assertIn("Unknown command", stdout, "Invalid command error not displayed")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("Invalid command timed out")
        except Exception as e:
            self.fail(f"Invalid command failed: {e}")
    
    def test_empty_input_handling(self):
        """Test that empty input is handled gracefully."""
        try:
            process = subprocess.Popen(
                ['python', 'src/main.py', '--config', 'debug'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send empty inputs then quit
            stdout, stderr = process.communicate(input='\n\n\n/quit\n', timeout=self.timeout)
            
            # Check that it didn't crash
            self.assertEqual(process.returncode, 0, f"Empty input crashed. stderr: {stderr}")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("Empty input timed out")
        except Exception as e:
            self.fail(f"Empty input failed: {e}")
    
    def test_keyboard_interrupt_handling(self):
        """Test that Ctrl+C is handled gracefully."""
        try:
            process = subprocess.Popen(
                ['python', 'src/main.py', '--config', 'debug'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send Ctrl+C signal
            time.sleep(1.0)  # Let it start up fully
            process.send_signal(subprocess.signal.SIGINT)
            
            stdout, stderr = process.communicate(timeout=10)
            
            # Should exit gracefully - check for goodbye message in stdout or stderr
            # or simply check that it didn't crash with a bad return code
            output = stdout + stderr
            self.assertTrue(
                "Goodbye" in output or process.returncode == 0,
                f"Keyboard interrupt not handled gracefully. stdout: {stdout[:200]}... stderr: {stderr[:200]}..."
            )
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("Keyboard interrupt timed out")
        except Exception as e:
            self.fail(f"Keyboard interrupt failed: {e}")

class TestJustCommands(unittest.TestCase):
    """Test that just commands work end-to-end."""
    
    def test_just_run_command(self):
        """Test that 'just run' command works."""
        try:
            process = subprocess.Popen(
                ['just', 'run'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            # Send quit command
            stdout, stderr = process.communicate(input='/quit\n', timeout=30)
            
            # Check that it worked
            self.assertEqual(process.returncode, 0, f"'just run' failed. stderr: {stderr}")
            self.assertIn("Research Assistant", stdout, "Welcome message not displayed")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("'just run' timed out")
        except FileNotFoundError:
            self.skipTest("'just' command not available")
        except Exception as e:
            self.fail(f"'just run' failed: {e}")
    
    def test_just_test_command(self):
        """Test that 'just test' command works."""
        try:
            process = subprocess.Popen(
                ['just', 'test'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=Path(__file__).parent.parent
            )
            
            stdout, stderr = process.communicate(timeout=60)
            
            # Check that tests ran
            self.assertEqual(process.returncode, 0, f"'just test' failed. stderr: {stderr}")
            self.assertIn("tests", stdout.lower(), "Test output not found")
            
        except subprocess.TimeoutExpired:
            process.kill()
            self.fail("'just test' timed out")
        except FileNotFoundError:
            self.skipTest("'just' command not available")
        except Exception as e:
            self.fail(f"'just test' failed: {e}")

def run_user_experience_tests():
    """Run all user experience tests."""
    print("🧪 User Experience Test Suite")
    print("=" * 50)
    print("Testing actual user workflows...")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    test_cases = [
        TestUserExperience,
        TestJustCommands
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
    skipped = len(result.skipped)
    passed = total_tests - failures - errors - skipped
    
    print(f"\n📊 USER EXPERIENCE TEST RESULTS")
    print("=" * 50)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed}")
    print(f"Failed: {failures}")
    print(f"Errors: {errors}")
    print(f"Skipped: {skipped}")
    print(f"Success Rate: {(passed/total_tests*100):.1f}%")
    
    if failures == 0 and errors == 0:
        print("\n✅ ALL USER EXPERIENCE TESTS PASSED!")
        print("🎯 The application works correctly from a user perspective")
        return True
    else:
        print(f"\n❌ {failures + errors} USER EXPERIENCE TESTS FAILED!")
        print("🔧 These are critical user-facing issues that must be fixed")
        
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
    success = run_user_experience_tests()
    sys.exit(0 if success else 1)