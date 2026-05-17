#!/usr/bin/env sage -python
"""
Run Sage filter tests using Sage's Python interpreter.

This script should be executed directly with Sage's Python interpreter:
    ./run_sage_tests.py

Or:
    sage -python run_sage_tests.py
"""

import os
import sys
import unittest
from pathlib import Path

def run_tests():
    """Run all Sage filter tests."""
    print("=" * 80)
    print(f"Running tests with: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print("=" * 80)
    
    # Add the package directory to the Python path
    package_dir = str(Path(__file__).parent)
    if package_dir not in sys.path:
        sys.path.insert(0, package_dir)
    
    # Import test modules
    test_modules = [
        'tests.unit.test_basic_math',
        'tests.integration.test_symbolic_math',
        'tests.regression.test_regressions',
        'tests.test_sage_pdf_output'
    ]
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    test_suites = []
    
    for module_name in test_modules:
        try:
            # Import the test module
            __import__(module_name)
            module = sys.modules[module_name]
            
            # Find all test cases in the module
            for name in dir(module):
                obj = getattr(module, name)
                if (isinstance(obj, type) and 
                    issubclass(obj, unittest.TestCase) and 
                    obj is not unittest.TestCase):
                    test_suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(obj))
                    
        except ImportError as e:
            print(f"Error importing {module_name}: {e}")
            continue
    
    if not test_suites:
        print("No test suites found!")
        return 1
    
    # Combine and run all test suites
    combined_suite = unittest.TestSuite(test_suites)
    result = runner.run(combined_suite)
    
    # Return non-zero exit code if any tests failed
    return not result.wasSuccessful()

if __name__ == "__main__":
    sys.exit(run_tests())
