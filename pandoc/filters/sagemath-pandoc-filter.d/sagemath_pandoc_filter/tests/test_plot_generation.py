"""
Test script for Sage plot generation functionality.

This script tests the plot generation capabilities of the Sage filter
without using any test frameworks, as per project requirements.
"""

import os
import sys
import json
import unittest.mock
from pathlib import Path
from typing import Dict, Any, Optional

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the function we want to test
from sagemath_pandoc_filter.sage_plot import generate_plot

# Test configuration
TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), '../../test-images')
os.makedirs(TEST_IMAGE_DIR, exist_ok=True)

# Mock Sage functionality for testing
class MockPlot:
    def save(self, path, **kwargs):
        # Create an empty file to simulate plot saving
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).touch()
        return path

class MockSage:
    @staticmethod
    def plot(*args, **kwargs):
        return MockPlot()
    
    @staticmethod
    def plot3d(*args, **kwargs):
        return MockPlot()
    
    @staticmethod
    def var(name):
        return name  # Return the variable name as is for testing
    
    @staticmethod
    def sin(x):
        return f"sin({x})"  # Return a string representation for testing
    
    @staticmethod
    def cos(x):
        return f"cos({x})"  # Return a string representation for testing

# Mock the Sage environment
sys.modules['sage.all'] = MockSage()
from sagemath_pandoc_filter import generate_plot

def run_test(test_name, test_func):
    """Run a test and print the result."""
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print("-" * 80)
    
    try:
        result = test_func()
        if result is None:
            print("✅ Test passed")
        else:
            print(f"❌ Test failed: {result}")
            return False
        return True
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_plot_creation():
    """Test creating a simple 2D plot."""
    # Test with valid plot code
    plot_code = """
from sage.all import *
x = var('x')
p = plot(sin(x), (x, -2*pi, 2*pi), title='Sine Wave')
"""
    
    with unittest.mock.patch('sagemath_pandoc_filter.sage_plot._execute_plot_code') as mock_execute:
        # Mock successful plot generation
        output_path = os.path.join(TEST_IMAGE_DIR, 'test_plot.pdf')
        mock_execute.return_value = {
            'success': True,
            'output': output_path
        }
        
        result = generate_plot(plot_code, TEST_IMAGE_DIR)
        
        assert result['success'], f"Plot generation failed: {result.get('error', 'Unknown error')}"
        assert 'output' in result, "Output path missing from result"
        
        print(f"Test plot generation successful")
        return None

def test_3d_plot():
    """Test creating a 3D plot."""
    # Test with valid 3D plot code
    plot_code = """
from sage.all import *
x, y = var('x y')
p = plot3d(cos(x^2 + y^2), (x, -2, 2), (y, -2, 2), color='red')
"""
    
    with unittest.mock.patch('sagemath_pandoc_filter.sage_plot._execute_plot_code') as mock_execute:
        # Mock successful 3D plot generation
        output_path = os.path.join(TEST_IMAGE_DIR, 'test_3d_plot.png')
        mock_execute.return_value = {
            'success': True,
            'output': output_path
        }
        
        result = generate_plot(plot_code, TEST_IMAGE_DIR)
        
        assert result['success'], f"3D plot generation failed: {result.get('error', 'Unknown error')}"
        assert 'output' in result, "Output path missing from result"
        
        print(f"Test 3D plot generation successful")
        return None

def test_invalid_plot():
    """Test handling of invalid plot code."""
    # This code doesn't create a plot object 'p'
    plot_code = "x = 1 + 1"
    
    with unittest.mock.patch('sagemath_pandoc_filter.sage_plot._execute_plot_code') as mock_execute:
        # Mock failed plot generation
        mock_execute.return_value = {
            'success': False,
            'error': 'No plot object found. Assign your plot to variable p.'
        }
        
        result = generate_plot(plot_code, TEST_IMAGE_DIR)
        
        assert not result['success'], "Expected plot generation to fail"
        assert 'error' in result, "Expected error message in result"
        print(f"Correctly handled invalid plot code: {result['error']}")
        return None

def main():
    """Run all tests and return the number of failures."""
    tests = [
        ("2D Plot Creation", test_plot_creation),
        ("3D Plot Creation", test_3d_plot),
        ("Invalid Plot Handling", test_invalid_plot)
    ]
    
    print("Starting Sage Filter Tests")
    print("=" * 80)
    
    # Create test output directory
    os.makedirs(TEST_IMAGE_DIR, exist_ok=True)
    
    # Run all tests
    failures = 0
    for name, test_func in tests:
        if not run_test(name, test_func):
            failures += 1
    
    # Print final result
    print("\n" + "=" * 80)
    if failures == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print(f"❌ {failures} TEST(S) FAILED")
    
    return failures

if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 1)
