"""Unit tests for basic math operations in Sage."""
import os
import sys
import unittest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Use mock Sage environment for testing
from tests.mock_sage import execute_sage_code


class TestBasicMath(unittest.TestCase):
    """Test basic mathematical operations in Sage."""
    
    def test_integer_arithmetic(self):
        """Test basic integer arithmetic operations."""
        test_cases = [
            ("2 + 2", 4),
            ("5 - 3", 2),
            ("6 * 7", 42),
            ("15 / 3", 5.0),
            ("2 ** 10", 1024),
            ("17 % 5", 2),
            ("(2 + 3) * 4", 20),
        ]
        
        for code, expected in test_cases:
            with self.subTest(code=code, expected=expected):
                result = execute_sage_code(code)
                self.assertTrue(result['success'], f"Code execution failed: {result.get('error')}")
                self.assertEqual(result['result'], expected, 
                               f"{code} should equal {expected}, got {result['result']}")
    
    def test_variable_assignment(self):
        """Test variable assignment and retrieval."""
        # Test simple variable assignment and use
        result = execute_sage_code("x = 5")
        self.assertTrue(result['success'], f"Code execution failed: {result.get('error')}")
        
        # Test using the variable in an expression
        result = execute_sage_code("x * 2")
        self.assertTrue(result['success'], f"Code execution failed: {result.get('error')}")
        self.assertEqual(result['result'], 10, f"Expected 10, got {result['result']}")
        
        # Test multiple statements with separate executions
        result = execute_sage_code("a = 10")
        self.assertTrue(result['success'], f"Code execution failed: {result.get('error')}")
        
        result = execute_sage_code("b = 20")
        self.assertTrue(result['success'], f"Code execution failed: {result.get('error')}")
        
        result = execute_sage_code("a + b")
        self.assertTrue(result['success'], f"Code execution failed: {result.get('error')}")
        self.assertEqual(result['result'], 30, f"Expected 30, got {result['result']}")
        
        # Test multiple variables in a single expression
        result = execute_sage_code("a = 3; b = 4; a**2 + b**2")
        self.assertTrue(result['success'], f"Code execution failed: {result.get('error')}")
        self.assertEqual(result['result'], 25, f"Expected 25, got {result['result']}")

    def test_boolean_operations(self):
        """Test boolean operations."""
        test_cases = [
            ("5 > 3", True),
            ("5 < 3", False),
            ("5 == 5", True),
            ("5 != 3", True),
            ("5 >= 5", True),
            ("5 <= 5", True),
            ("True and False", False),
            ("True or False", True),
            ("not False", True),
        ]
        
        for code, expected in test_cases:
            with self.subTest(code=code, expected=expected):
                result = execute_sage_code(code)
                self.assertTrue(result['success'], f"Code execution failed: {result.get('error')}")
                self.assertEqual(result['result'], expected, 
                               f"{code} should be {expected}, got {result['result']}")

    def test_error_handling(self):
        """Test error handling for invalid expressions."""
        test_cases = [
            ("1 / 0", 'division by zero'),
            ("undefined_variable", 'name'),
            ("syntax error", 'syntax'),
            ("x = ", 'syntax'),  # Incomplete expression
        ]
        
        for code, error_type in test_cases:
            with self.subTest(code=code, error_type=error_type):
                result = execute_sage_code(code)
                self.assertFalse(result['success'], 
                              f"Expected code to fail but it succeeded: {code}")
                self.assertIn('error', result, 
                            f"Expected error in result, but got {result}")
                
                error_msg = str(result['error']).lower()
                if error_type == 'division by zero':
                    self.assertIn('division by zero', error_msg,
                                 f"Expected division by zero error, but got {error_msg}")
                elif error_type == 'name':
                    self.assertIn('name', error_msg,
                                 f"Expected name error, but got {error_msg}")
                else:  # syntax error
                    self.assertTrue(any(err in error_msg for err in ['syntaxerror', 'syntax', 'invalid syntax']), 
                                  f"Expected syntax error, but got {error_msg}")

if __name__ == '__main__':
    pass
