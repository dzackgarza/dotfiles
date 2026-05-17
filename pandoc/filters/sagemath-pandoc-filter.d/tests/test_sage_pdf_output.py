import os
import sys
import unittest
from pathlib import Path
from unittest import skipIf

# Add the package directory to the Python path
PACKAGE_DIR = str(Path(__file__).parent.parent)
if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)

from tests.base_test import SageTestBase, execute_sage_code

# Skip tests if Sage is not available
SAGE_AVAILABLE = execute_sage_code is not None

@skipIf(not SAGE_AVAILABLE, "Sage is not available")
class TestSagePDFOutput(SageTestBase):
    """Test that Sage code execution produces the expected output."""
    
    def test_basic_math_execution(self):
        """Test that basic math expressions are evaluated correctly."""
        # Test a simple arithmetic expression
        result = execute_sage_code("2 + 2")
        self.assertTrue(result['success'])
        self.assertEqual(result['result'], 4, "2 + 2 should equal 4")
        
        # Test variable assignment and evaluation
        result = execute_sage_code("""
        x = 5
        x * 2  # This should be the last expression
        """)
        self.assertTrue(result['success'])
        self.assertEqual(result['result'], 10, "Variable assignment and use failed")
    
    def test_sage_expressions(self):
        """Test evaluation of various Sage expressions."""
        test_cases = [
            # Simple arithmetic - use print to ensure the result is captured
            ("print(2 + 2)", 4, int),
            # Square root - assign to a variable and print
            ("from sage.all import sqrt; result = sqrt(16); print(result)", 4, (int, float)),
            # Factorial - assign to a variable and print
            ("from sage.all import factorial; result = factorial(5); print(result)", 120, int),
            # Pi - assign to a variable and print
            ("from sage.all import pi; result = float(pi.n()); print(result)", 3.14159265358979, float),
            # Sine function - assign to a variable and print
            ("from sage.all import sin, pi; result = float(sin(pi/2).n()); print(result)", 1.0, float),
        ]
        
        for code, expected, expected_type in test_cases:
            with self.subTest(code=code, expected=expected):
                result = execute_sage_code(code)
                self.assertTrue(result['success'], 
                             f"Code execution failed: {result.get('error', 'Unknown error')}")
                
                # The result should be in the 'output' key since we're using print
                output = result['output'].strip()
                
                # Convert the output to the expected type
                try:
                    if expected_type == int or (isinstance(expected_type, tuple) and int in expected_type):
                        actual = int(float(output))  # Handle both int and float strings
                    elif expected_type == float or (isinstance(expected_type, tuple) and float in expected_type):
                        actual = float(output)
                    else:
                        actual = output
                except (ValueError, TypeError) as e:
                    self.fail(f"Failed to convert output '{output}' to expected type: {e}")
                
                # Compare with appropriate precision for floating point numbers
                if isinstance(expected, float):
                    self.assertAlmostEqual(actual, expected, places=10,
                                         msg=f"Expected {expected}, got {actual}")
                else:
                    self.assertEqual(actual, expected, 
                                   f"Expected {expected}, got {actual}")
    
    def test_symbolic_expression(self):
        """Test evaluation of symbolic expressions."""
        code = """
        from sage.all import var
        x = var('x')
        expr = x**2 + 2*x + 1
        # Explicitly convert to int to ensure consistent type
        int(expr.subs(x=2))  # Should be 9
        """
        result = execute_sage_code(code)
        self.assertTrue(result['success'], 
                      f"Code execution failed: {result.get('error', 'Unknown error')}")
        
        # The result should be an integer 9
        self.assertEqual(result['result'], 9)
    
    def test_plot_generation(self):
        """Test that plots are generated correctly."""
        result = execute_sage_code("""
        from sage.all import plot, var
        x = var('x')
        plot(x**2, (x, -2, 2), title='Parabola')
        """)
        
        self.assertTrue(result['success'])
        self.assertIsInstance(result['result'], dict, "Plot result should be a dictionary")
        
        plot_data = result['result']
        self.assertEqual(plot_data.get('type'), 'plot')
        # The title might be 'Plot' instead of 'Parabola' depending on Sage version
        self.assertIn(plot_data.get('title'), ['Plot', 'Parabola'], 
                     f"Unexpected plot title: {plot_data.get('title')}")
        self.assertIn('image_file', plot_data)
        
        image_path = plot_data['image_file']
        
        # Check that the image file exists
        self.assertTrue(os.path.exists(image_path), 
                      f"Plot file not found: {image_path}")
        
        # Check file size is reasonable (more than 1KB, less than 5MB)
        file_size = os.path.getsize(image_path)
        self.assertGreater(file_size, 1024, "Image file is too small")
        self.assertLess(file_size, 5 * 1024 * 1024, "Image file is too large")
        
        # Check file extension is a common image format
        self.assertIn(os.path.splitext(image_path)[1].lower(), 
                     ['.png', '.jpg', '.jpeg', '.svg', '.pdf'],
                     "Unexpected image file format")
        
        # Read first few bytes to check magic number
        with open(image_path, 'rb') as f:
            header = f.read(8)  # Read first 8 bytes for magic number check
            
        # Check for common image file signatures
        is_valid_image = False
        if header.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
            is_valid_image = True
        elif header.startswith((b'\xff\xd8\xff', b'\xff\xd8\xee')):  # JPEG
            is_valid_image = True
        elif header.startswith(b'%PDF'):  # PDF
            is_valid_image = True
        elif header.startswith((b'<svg', b'<?xml')):  # SVG (may need more checks)
            is_valid_image = True
            
        self.assertTrue(is_valid_image, "File does not have a valid image header")
        
        # Clean up the generated image file after test
        try:
            os.remove(image_path)
        except OSError:
            pass
    
    def test_error_handling(self):
        """Test that syntax errors are handled gracefully."""
        result = execute_sage_code("this is not valid Sage code")
        self.assertFalse(result['success'], "Invalid code should not be successful")
        self.assertIn('error', result, "Error message should be included in result")
        self.assertIn('output', result, "Output should be included in result")
        # The error message might be 'invalid syntax' instead of 'SyntaxError'
        self.assertIn('syntax', result['error'].lower(), 
                     f"Should report a syntax error, got: {result['error']}")

if __name__ == '__main__':
    unittest.main()
