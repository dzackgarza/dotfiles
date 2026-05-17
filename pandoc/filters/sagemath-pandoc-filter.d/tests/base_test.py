"""Base test class for Sage filter tests."""
import sys
import os
import unittest
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Union, Tuple, List
import json
import hashlib

# Add the package directory to the Python path
PACKAGE_DIR = str(Path(__file__).parent.parent)
if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)

try:
    from sagemath_pandoc_filter.sage_runner import execute_sage_code
except ImportError:
    # This will be handled by individual test files
    execute_sage_code = None

class SageTestBase(unittest.TestCase):
    """Base class for Sage filter tests with common utilities."""
    
    TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.maxDiff = None  # Show full diff for assertion failures
        
        # Create test directories if they don't exist
        self.test_dir = tempfile.mkdtemp(prefix='sage_filter_test_')
        os.makedirs(os.path.join(self.TEST_DATA_DIR, 'input'), exist_ok=True)
        os.makedirs(os.path.join(self.TEST_DATA_DIR, 'expected'), exist_ok=True)
        
    def tearDown(self):
        """Clean up test environment."""
        import shutil
        import errno
        if hasattr(self, 'test_dir') and os.path.exists(self.test_dir):
            try:
                shutil.rmtree(self.test_dir)
            except OSError as e:
                # Ignore errors when removing test directory
                if e.errno != errno.ENOENT:  # No such file or directory
                    raise
    
    def assertSageOutputEqual(self, code: str, expected: Dict[str, Any], 
                            msg: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute Sage code and assert the output matches expected.
        
        Args:
            code: Sage code to execute
            expected: Dictionary with expected output structure
            msg: Optional failure message
            
        Returns:
            Dict with the actual execution result
        """
        result = execute_sage_code(code)
        
        # Check basic structure
        self.assertIn('success', result, "Result missing 'success' key")
        self.assertIn('output', result, "Result missing 'output' key")
        
        # If we expected success but got an error, show the error
        if expected.get('success', True) and not result['success']:
            self.fail(f"Execution failed: {result.get('error', 'Unknown error')}")
        
        # Check each expected key in the result
        for key, expected_value in expected.items():
            self.assertIn(key, result, f"Result missing expected key: {key}")
            
            # Special handling for result comparison
            if key == 'result':
                self._assertResultsEqual(result[key], expected_value, msg)
            else:
                self.assertEqual(result[key], expected_value, 
                               msg or f"Mismatch in {key}")
        
        return result
    
    def _assertResultsEqual(self, actual: Any, expected: Any, msg: Optional[str] = None) -> None:
        """Helper to compare results with special handling for numeric types."""
        # Handle floating point comparison with tolerance
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            self.assertAlmostEqual(float(actual), float(expected), 
                                 places=10, 
                                 msg=msg or f"Numeric values differ: {actual} != {expected}")
        else:
            self.assertEqual(actual, expected, msg or "Results differ")
    
    def get_test_data_path(self, filename: str, data_type: str = 'input') -> str:
        """Get the full path to a test data file."""
        return os.path.join(self.TEST_DATA_DIR, data_type, filename)
    
    def save_test_result(self, filename: str, data: Any) -> str:
        """Save test result data to a file."""
        path = self.get_test_data_path(filename, 'expected')
        with open(path, 'w') as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, indent=2)
            else:
                f.write(str(data))
        return path
    
    def load_expected_result(self, filename: str) -> Any:
        """Load expected result from a file."""
        path = self.get_test_data_path(filename, 'expected')
        with open(path) as f:
            if path.endswith('.json'):
                return json.load(f)
            return f.read()
    
    def get_code_fingerprint(self, code: str) -> str:
        """Generate a fingerprint for a code snippet."""
        return hashlib.md5(code.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    unittest.main()
