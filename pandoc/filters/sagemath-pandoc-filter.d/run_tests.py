#!/usr/bin/env python3
"""
Test runner for the Sage Filter package.

This script discovers and runs all tests in the tests/ directory.
"""

import sys
import os
import unittest
from pathlib import Path

def discover_tests():
    """Discover all test files in the tests directory."""
    test_dir = Path(__file__).parent / 'tests'
    test_suites = []
    
    # Discover all test files
    for test_file in test_dir.rglob('test_*.py'):
        # Convert file path to module path
        rel_path = test_file.relative_to(Path(__file__).parent)
        module_path = str(rel_path.with_suffix('')).replace(os.sep, '.')
        
        # Skip __pycache__ and other non-test directories
        if '__pycache__' in str(test_file):
            continue
            
        test_suites.append(unittest.defaultTestLoader.discover(
            start_dir=str(test_file.parent),
            pattern=test_file.name,
            top_level_dir=str(Path(__file__).parent)
        ))
    
    return test_suites

def run_tests():
    """Run all tests and return the number of failures."""
    # Add the package directory to the Python path
    package_dir = os.path.dirname(os.path.abspath(__file__))
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)
    
    print("Discovering tests...")
    test_suites = discover_tests()
    
    if not test_suites:
        print("No test files found.", file=sys.stderr)
        return 1
    
    # Combine all test suites
    combined_suite = unittest.TestSuite(test_suites)
    
    # Run the tests
    print("\n" + "=" * 80)
    print("Running tests...")
    print("=" * 80)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(combined_suite)
    
    # Print summary
    print("\n" + "=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f="Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\nAll tests passed!")
        return 0
    else:
        print(f"\n{len(result.failures) + len(result.errors)} test(s) failed.")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
