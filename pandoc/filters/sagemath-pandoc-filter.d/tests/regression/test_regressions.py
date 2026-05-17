"""Regression tests to prevent reintroduction of fixed bugs."""
import os
import sys
import unittest
from unittest import skipIf

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tests.base_test import SageTestBase, execute_sage_code

# Skip tests if Sage is not available
SAGE_AVAILABLE = execute_sage_code is not None

@skipIf(not SAGE_AVAILABLE, "Sage is not available")
class TestRegressions(SageTestBase):
    """Regression tests for fixed bugs."""
    
    def test_previous_bug_handling(self):
        """Test that previously fixed bugs don't reappear."""
        # Add regression tests for any previously fixed bugs here
        # Each test should be documented with the issue it fixes
        pass
    
    def test_division_handling(self):
        """Test that division works correctly (regression test)."""
        # Test case for issue with division in Python 2 vs 3
        code = "3 / 2"  # Should be 1.5 in Python 3, 1 in Python 2
        result = execute_sage_code(code)
        self.assertEqual(result['result'], 1.5)
    
    def test_unicode_handling(self):
        """Test that unicode characters are handled correctly."""
        code = "'π'"
        result = execute_sage_code(code)
        self.assertEqual(result['result'], 'π')
    
    def test_large_integers(self):
        """Test handling of large integers."""
        code = "2**100"
        result = execute_sage_code(code)
        self.assertEqual(result['result'], 2**100)
    
    def test_plot_handling(self):
        """Test that plot generation works and returns expected structure."""
        code = """
        from sage.all import plot, var
        x = var('x')
        plot(x**2, (x, -2, 2))
        """
        result = execute_sage_code(code)
        self.assertTrue(result['success'])
        self.assertIsInstance(result['result'], dict)
        self.assertIn('image_file', result['result'])
        self.assertTrue(os.path.exists(result['result']['image_file']))

if __name__ == '__main__':
    unittest.main()
