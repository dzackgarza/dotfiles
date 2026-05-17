"""Test with real Sage environment."""
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Use real Sage environment
from tests.real_sage import execute_sage_code

def test_basic_math():
    """Test basic mathematical operations with real Sage."""
    test_cases = [
        ("2 + 2", 4),
        ("5 - 3", 2),
        ("2 * 3", 6),
        ("6 / 2", 3),
        ("2 ** 3", 8),
        ("5 > 3", True),
        ("5 < 3", False),
        ("5 == 5", True),
        ("5 != 3", True),
        ("5 >= 5", True),
        ("5 <= 5", True),
    ]
    
    for code, expected in test_cases:
        print(f"\nTesting: {code}")
        result = execute_sage_code(code)
        print(f"Result: {result}")
        assert result['success'], f"Code execution failed: {result.get('error')}"
        print(f"Asserting {result['result']} == {expected}")
        assert result['result'] == expected, f"{code} should be {expected}, got {result['result']}"

if __name__ == '__main__':
    test_basic_math()
