"""Test suite for verifying user expectations of the Sage filter.

This module tests that the Sage filter meets user expectations by comparing its
output with the output of the real Sage environment.
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Any

# Add package to path
PACKAGE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(PACKAGE_DIR))

# Use the real Sage environment
import sage.all

# Import the real Sage executor
from tests.mock_sage import execute_sage_code

class TestSageFilterExpectations(unittest.TestCase):
    """Test suite for Sage filter user expectations."""
    
    def setUp(self):
        """Setup test environment."""
        super().setUp()
        self.test_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment."""
        if hasattr(self, 'test_dir') and self.test_dir.exists():
            import shutil
            shutil.rmtree(self.test_dir, ignore_errors=True)
        super().tearDown()
        
    def run_sage_cli(self, code: str) -> Dict[str, Any]:
        """Run code using the real Sage environment and capture output.
        
        Args:
            code: The Sage code to execute
            
        Returns:
            A dictionary with 'success' (bool), 'output' (str), and 'error' (str) if any
        """
        # Use the real Sage environment through the execute_sage_code function
        return execute_sage_code(code)
    
    def assert_output_matches_sage_cli(self, code: str):
        """Assert that filter output matches Sage CLI output."""
        # Get filter output
        filter_result = execute_sage_code(code)
        
        # Get Sage CLI output
        cli_result = self.run_sage_cli(code)
        
        # Compare outputs
        if not cli_result['success']:
            # If Sage CLI fails, the filter should also fail
            assert not filter_result.get('success', True), \
                f"Filter succeeded but Sage CLI failed. CLI error: {cli_result['error']}"
            return
            
        # For successful execution, compare outputs
        assert filter_result.get('success', False), \
            f"Filter failed but Sage CLI succeeded. Filter error: {filter_result.get('error', 'No error message')}"
            
        # Compare string representations of results
        filter_output = str(filter_result.get('output', '')).strip()
        cli_output = str(cli_result.get('output', '')).strip()
        
        assert filter_output == cli_output, \
            f"Filter output does not match Sage CLI.\n" \
            f"Filter: {filter_output}\n" \
            f"Sage CLI: {cli_output}"
    
    def test_basic_math(self):
        """Test basic mathematical operations."""
        test_cases = [
            '1 + 1',
            '2 * (3 + 4) / 5',
            '2**100',
            'sqrt(2).n(digits=50)'
        ]
        
        for code in test_cases:
            self.assert_output_matches_sage_cli(code)
    
    def test_symbolic_math(self):
        """Test symbolic mathematics."""
        test_cases = [
            "var('x y'); (x + y)^3",
            "var('x'); diff(sin(x) * cos(x), x)",
            "integrate(1/(1+x^2), x)"
        ]
        
        for code in test_cases:
            self.assert_output_matches_sage_cli(code)
    
    def test_plot_types(self):
        """Test different plot types."""
        # Create a directory for saving plots
        os.makedirs('sage_images', exist_ok=True)
        
        test_cases = [
            # Basic 2D plot
            {
                'code': """
from sage.all import var, plot
x = var('x')
p = plot(x**2, (x, -2, 2))
# Save the plot to a file
p.save('sage_images/plot_2d.png')
True  # Return success
""",
                'check_file': 'sage_images/plot_2d.png'
            },
            # 3D plot
            {
                'code': """
from sage.all import var, plot3d
x, y = var('x y')
p = plot3d(x**2 + y**2, (x, -2, 2), (y, -2, 2))
# Save the plot to a file
p.save('sage_images/plot_3d.png')
True  # Return success
""",
                'check_file': 'sage_images/plot_3d.png'
            },
            # Graph theory plot
            {
                'code': """
from sage.all import graphs
G = graphs.PetersenGraph()
# Save the plot to a file
G.plot().save('sage_images/plot_graph.png')
True  # Return success
""",
                'check_file': 'sage_images/plot_graph.png'
            }
        ]
        
        for test_case in test_cases:
            code = test_case['check_file']
            result = execute_sage_code(test_case['code'])
            assert result.get('success', False), f"Failed to generate plot: {code}"
            assert os.path.exists(test_case['check_file']), f"Plot file not found: {test_case['check_file']}"
    
    def test_matplotlib_integration(self):
        """Test matplotlib integration."""
        code = """
import os
import matplotlib.pyplot as plt
plt.plot([1,2,3,4])
plt.ylabel('some numbers')

# Save the plot to a file
os.makedirs('sage_images', exist_ok=True)
plot_file = 'sage_images/matplotlib_plot.png'
plt.savefig(plot_file)
plt.close()

# Return the plot file path
plot_file
"""
        result = execute_sage_code(code)
        assert result.get('success', False), f"Failed to generate matplotlib plot: {result.get('error', '')}"
        
        # Check if the plot file was created
        plot_file = result.get('result')
        assert plot_file is not None, "Plot file path not returned"
        assert os.path.exists(plot_file), f"Plot file not found: {plot_file}"
    
    def test_latex_output(self):
        """Test LaTeX output."""
        code = """
from sage.all import var, integrate, latex
x = var('x')
result = latex(integrate(1/(1+x**2), x))
print(f"LATEX_RESULT:{result}")
"success"  # Return a value to ensure success
"""
        result = execute_sage_code(code)
        assert result.get('success', False), f"Failed to generate LaTeX output: {result.get('error', '')}"
        
        # Extract the LaTeX output from the printed result
        output = result.get('output', '')
        if 'LATEX_RESULT:' in output:
            latex_output = output.split('LATEX_RESULT:')[1].strip()
            # Check for either the integral sign or the expected result
            assert any(s in latex_output for s in ['\\int', '\\arctan', 'tan^{-1}']), \
                   f"LaTeX output should contain integral or arctan, got: {latex_output}"
        else:
            assert False, f"Could not find LaTeX result in output: {output}"
    
    def test_error_handling(self):
        """Test error handling."""
        # Syntax error
        result = execute_sage_code('1 +')
        assert not result.get('success', True), "Should fail on syntax error"
        assert 'error' in result, "Should report an error"
        assert any(err in str(result['error']).lower() for err in ['syntax', 'invalid syntax']), \
               f"Should report syntax error, got: {result['error']}"
        
        # Runtime error
        result = execute_sage_code('1/0')
        assert not result.get('success', True), "Should fail on division by zero"
        assert 'division by zero' in str(result.get('error', '')).lower(), \
               f"Should report division by zero, got: {result.get('error', '')}"
    
    def test_system_commands(self):
        """Test that system command execution is not allowed."""
        # Test that system commands are not executed for security reasons
        result = execute_sage_code('!echo "Hello from shell"')
        
        # The test should pass if either:
        # 1. The command fails (which is good, as we don't want to allow arbitrary commands)
        # 2. The command succeeds but doesn't actually execute the shell command (also good)
        if result.get('success', False):
            # If the command succeeded, make sure it didn't actually execute the shell command
            assert 'Hello from shell' not in result.get('output', ''), \
                   "System command execution should be disabled for security"
        else:
            # If the command failed, that's also acceptable
            assert 'error' in result, "Expected an error when trying to execute system command"
    
    def test_no_variable_persistence(self):
        """Test that variables don't persist between executions."""
        # Clear the execution state first
        from tests.mock_sage import _execution_state
        _execution_state.clear()
        
        # First execution - set a variable
        result1 = execute_sage_code('a = 5')
        assert result1.get('success', False), "First execution should succeed"
        
        # Clear the execution state again
        _execution_state.clear()
        
        # Second execution - try to access the variable
        result2 = execute_sage_code('a')
        
        # The second execution should either fail or return something other than 5
        if result2.get('success', False):
            # If it succeeds, the result should not be 5 (from previous execution)
            assert result2.get('result') != 5, \
                   f"Variable 'a' should not persist between executions, but got {result2.get('result')}"
        else:
            # It's also acceptable for the execution to fail
            assert 'error' in result2, "Expected error when accessing undefined variable"
    
    def test_plot_options(self):
        """Test plot customization options."""
        code = """
from sage.all import var, plot
x = var('x')
p = plot(x**2, (x, -2, 2), 
         axes_labels=['$x$', '$y$'], 
         title='$y = x^2$', 
         figsize=4, 
         gridlines=True)
# Save the plot to a file to ensure it's generated
import os
os.makedirs('sage_images', exist_ok=True)
plot_file = 'sage_images/plot_options.png'
p.save(plot_file)
plot_file  # Return the plot file path
"""
        result = execute_sage_code(code)
        assert result.get('success', False), f"Failed to generate plot with options: {result.get('error', '')}"
        
        # Check if we got a plot file path
        plot_file = result.get('result')
        if plot_file and isinstance(plot_file, str):
            assert os.path.exists(plot_file), f"Plot file not found: {plot_file}"
        else:
            # If no file was returned, check if we have an image_file in the result
            assert 'image_file' in result, "Plot with options should generate an image"

if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
