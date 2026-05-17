"""Comprehensive test suite for Sage plot generation and embedding.

This module provides a simple test runner that executes all test cases
and reports the results.
"""

import importlib
import os
import sys
import time
import traceback
from pathlib import Path
from typing import List, Optional, Dict, Any, Callable, Tuple, Union

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ANSI color codes for terminal output
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"

# Package directory
PACKAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Global test counters
total_tests = 0
passed_tests = 0
failed_tests = 0

# Add package to path
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from sagemath_pandoc_filter.sage_runner import execute_sage_code

class TestResult:
    """Container for test results."""
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = None
        self.output = None

    def __str__(self):
        status = f"{GREEN}✓{RESET}" if self.passed else f"{RED}✗{RESET}"
        return f"  {status} {self.name:60} {'PASSED' if self.passed else 'FAILED'}"


def run_test_module(module_name: str) -> List[TestResult]:
    """Run all tests in a module.
    
    Args:
        module_name: Name of the module to test (e.g., 'unit.test_basic_math')
        
    Returns:
        List of TestResult objects, one for each test method or function
    """
    results = []
    
    try:
        # Import the module
        module = importlib.import_module(f"tests.{module_name}")
        module_has_tests = False
        
        # Find all test functions and classes
        for name in dir(module):
            if name.startswith('test_') and callable(getattr(module, name)):
                # Handle test functions
                test_func = getattr(module, name)
                print(f"\n{BOLD}Running test: {module_name}.{name}{RESET}")
                result = run_test(test_func)
                result.name = f"{module_name}.{name}"
                results.append(result)
                module_has_tests = True
                if not result.passed:
                    print(f"{RED}Test failed, stopping test module.{RESET}")
                    break
                        
            elif (name.startswith('Test') and 
                  isinstance(getattr(module, name), type)):
                # Handle test classes - include all classes that start with 'Test'
                test_class = getattr(module, name)
                # Skip classes that explicitly set __test__ = False
                if hasattr(test_class, '__test__') and not test_class.__test__:
                    continue
                test_instance = test_class()
                test_methods = [m for m in dir(test_class) 
                              if m.startswith('test_') and callable(getattr(test_class, m))]
                
                if not test_methods:
                    continue
                    
                print(f"\n{BOLD}Running test class: {module_name}.{name}{RESET}")
                
                # Run setup class method if it exists
                if hasattr(test_class, 'setUpClass') and callable(getattr(test_class, 'setUpClass')):
                    test_class.setUpClass()
                
                for method_name in test_methods:
                    # Create a new test instance for each test method
                    test_instance = test_class()
                    # Run setUp if it exists
                    if hasattr(test_instance, 'setUp') and callable(test_instance.setUp):
                        test_instance.setUp()
                        
                    print(f"  {BOLD}Running test: {module_name}.{name}.{method_name}{RESET}")
                    test_method = getattr(test_instance, method_name)
                    result = run_test(test_method, test_instance)
                    result.name = f"{module_name}.{name}.{method_name}"
                    results.append(result)
                    
                    # Run tearDown if it exists
                    if hasattr(test_instance, 'tearDown') and callable(test_instance.tearDown):
                        test_instance.tearDown()
                        
                    if not result.passed:
                        print(f"{RED}Test failed, stopping test class.{RESET}")
                        break
                
                # Run tearDownClass method if it exists
                if hasattr(test_class, 'tearDownClass') and callable(getattr(test_class, 'tearDownClass')):
                    test_class.tearDownClass()
                        
                module_has_tests = True
                
        if not module_has_tests:
            print(f"{YELLOW}Warning: No tests found in {module_name}{RESET}")
                
    except ImportError as e:
        result = TestResult(f"Module {module_name}")
        result.passed = False
        result.error = f"Failed to import module: {str(e)}"
        results.append(result)
    except Exception as e:
        result = TestResult(f"Module {module_name}")
        result.passed = False
        result.error = f"Error running tests: {str(e)}"
        results.append(result)
    
    return results

def run_test(test_func: callable, instance=None) -> TestResult:
    """Run a single test and return the result.
    
    Args:
        test_func: The test function or method to run
        instance: If provided, the instance to call the method on (for test methods)
        
    Returns:
        TestResult object with the test result
    """
    # Get a descriptive name for the test
    if instance is not None:
        test_name = f"{instance.__class__.__name__}.{test_func.__name__}"
    else:
        test_name = test_func.__name__
    
    result = TestResult(test_name)
    start_time = time.time()
    
    try:
        # Run the test
        if instance is not None:
            # It's a test method, check if it's already bound
            if hasattr(test_func, '__self__'):
                # Already bound, call directly
                test_func()
            else:
                # Not bound, call with instance
                test_func(instance)
        else:
            # It's a test function, call it directly
            test_func()
            
        # If we get here, the test passed
        result.passed = True
        result.output = f"{GREEN}✓{RESET} {result.name:<80} {GREEN}PASSED{RESET}"
        
    except AssertionError as e:
        # Test failed an assertion
        result.passed = False
        result.error = str(e)
        result.output = f"{RED}✗{RESET} {result.name:<80} {RED}FAILED{RESET}"
        if str(e).strip():
            result.output += f"\n    {YELLOW}AssertionError:{RESET} {str(e)}"
        
        # Add traceback information
        import traceback
        tb = traceback.extract_tb(sys.exc_info()[2])
        if tb:
            # Get the most recent frame in the traceback
            frame = tb[-1]
            result.output += f"\n    {YELLOW}File{RESET} {frame.filename}, line {frame.lineno}, in {frame.name}"
            result.output += f"\n    {frame.line}"
            
    except Exception as e:
        # Test raised an unexpected exception
        result.passed = False
        result.error = str(e)
        result.output = f"{RED}✗{RESET} {result.name:<80} {RED}ERROR{RESET}"
        
        # Add exception information
        result.output += f"\n    {YELLOW}{type(e).__name__}:{RESET} {str(e)}"
        
        # Add traceback information
        import traceback
        tb = traceback.extract_tb(sys.exc_info()[2])
        if tb:
            # Get the most recent frame in the traceback
            frame = tb[-1]
            result.output += f"\n    {YELLOW}File{RESET} {frame.filename}, line {frame.lineno}, in {frame.name}"
            if frame.line:
                result.output += f"\n    {frame.line}"
    
    finally:
        # Always record the duration
        result.duration = time.time() - start_time
        
        # Print the result
        print(result.output)
    
    return result


def find_test_modules() -> List[str]:
    """Find all test modules in the tests directory and its subdirectories.
    
    Returns:
        List of module paths (e.g., ['unit.test_basic_math', 'integration.test_symbolic_math'])
    """
    test_modules = set()
    tests_dir = Path(__file__).parent
    
    # Walk through all subdirectories
    for test_file in tests_dir.rglob('test_*.py'):
        # Get the relative path from tests directory
        rel_path = test_file.relative_to(tests_dir)
        
        # Convert path to module path (replace / with . and remove .py)
        module_path = str(rel_path.with_suffix('')).replace(os.path.sep, '.')
        
        # Skip the test suite itself
        if module_path != 'test_suite':
            test_modules.add(module_path)
    
    return sorted(test_modules)

def run_tests() -> bool:
    """Run all tests and return True if all passed, False otherwise.
    
    Returns:
        bool: True if all tests passed, False otherwise
    """
    global total_tests, passed_tests, failed_tests
    
    # Reset counters
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    # Print header
    print(f"\n{BOLD}Running test suite for sagemath-pandoc-filter{RESET}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Package directory: {PACKAGE_DIR}")
    
    # Check if Sage is available
    try:
        import sage.all  # noqa: F401
        print(f"{GREEN}✓ SageMath is available{RESET}")
    except ImportError:
        print(f"{YELLOW}Warning: SageMath is not available. Some tests may fail.{RESET}")
    
    all_results = []
    
    # Find and run all test modules
    test_modules = find_test_modules()
    print(f"\n{BOLD}Found {len(test_modules)} test modules to run{RESET}")
    
    # Run test modules
    for module_name in test_modules:
        module_results = run_test_module(module_name)
        all_results.extend(module_results)
        
        # Update counters
        module_passed = sum(1 for r in module_results if r.passed)
        module_failed = len(module_results) - module_passed
        
        total_tests += len(module_results)
        passed_tests += module_passed
        failed_tests += module_failed
        
        # Continue on failure to see all test results
        if module_failed > 0:
            print(f"{YELLOW}✗ {module_failed} test(s) failed in {module_name}{RESET}")
    
    # Run individual test functions if no failures yet
    if failed_tests == 0:
        individual_tests = [
            run_plot_generation_tests,
            test_html_embedding
        ]
        
        for test_func in individual_tests:
            print(f"\n{BOLD}Running {test_func.__name__}...{RESET}")
            result = test_func()
            all_results.append(result)
            
            # Update counters
            total_tests += 1
            if result.passed:
                passed_tests += 1
            else:
                failed_tests += 1
                print(f"{RED}Test {test_func.__name__} failed, stopping test run.{RESET}")
                break
    
    # Print summary
    print_summary(all_results)
    
    return failed_tests == 0

def print_summary(results: List[TestResult]) -> None:
    """Print a summary of test results.
    
    Args:
        results: List of TestResult objects
    """
    # Calculate statistics
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    success_rate = (passed / total * 100) if total > 0 else 0
    
    # Print summary header
    print("\n" + "=" * 100)
    print(f"{BOLD}TEST SUITE SUMMARY{RESET}".center(100))
    print("=" * 100)
    
    # Print detailed results for failed tests
    failed_tests = [r for r in results if not r.passed]
    if failed_tests:
        print(f"\n{BOLD}{RED}FAILED TESTS:{RESET}")
        for i, result in enumerate(failed_tests, 1):
            print(f"\n{i}. {result.name}")
            if result.error:
                print(f"   {RED}Error:{RESET} {result.error}")
    
    # Print overall statistics
    print("\n" + "=" * 100)
    print(f"{BOLD}OVERALL RESULTS:{RESET}".center(100))
    print("-" * 100)
    print(f"{BOLD}Total tests:{RESET} {total}")
    print(f"{GREEN}{BOLD}Passed:{RESET} {passed}")
    if failed > 0:
        print(f"{RED}{BOLD}Failed:{RESET} {failed}")
    
    # Print success rate with color coding
    if success_rate == 100:
        status = f"{GREEN}ALL TESTS PASSED{RESET}"
        color = GREEN
    elif success_rate >= 80:
        status = f"{YELLOW}MOST TESTS PASSED{RESET}"
        color = YELLOW
    else:
        status = f"{RED}MANY TESTS FAILED{RESET}"
        color = RED
    
    print(f"{BOLD}Success rate:{RESET} {color}{success_rate:.1f}% {status}")
    print("=" * 100 + "\n")


def main():
    """Main entry point for the test suite."""
    try:
        success = run_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest run interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Error running tests: {e}{RESET}")
        traceback.print_exc()
        sys.exit(1)


def run_plot_generation_tests():
    """Run plot generation tests.
    
    Returns:
        TestResult: The test result
    """
    result = TestResult("Plot Generation")
    
    try:
        # Test basic plot
        from sage.all import plot, var, sin, cos, pi
        
        # Test 1: Basic plot
        x = var('x')
        p = plot(x**2, (x, -2, 2), title='Test Plot')
        assert p is not None, "Plot creation failed"
        
        # Test 2: Plot with multiple curves
        p1 = plot(sin(x), (x, -pi, pi), color='red', legend_label='sin(x)')
        p2 = plot(cos(x), (x, -pi, pi), color='blue', legend_label='cos(x)')
        combined = p1 + p2
        assert combined is not None, "Combined plot creation failed"
        
        # Test 3: 3D plot
        try:
            from sage.all import plot3d
            y = var('y')
            p3d = plot3d(x**2 + y**2, (x, -2, 2), (y, -2, 2), title='3D Plot')
            assert p3d is not None, "3D plot creation failed"
        except ImportError:
            print(f"{YELLOW}Skipping 3D plot test - 3D plotting not available{RESET}")
        
        result.passed = True
    except Exception as e:
        result.passed = False
        result.error = str(e)
    
    return result


def test_html_embedding():
    """Test embedding plots in HTML with data URIs.
    
    Returns:
        TestResult: The test result
    """
    result = TestResult("HTML Embedding")
    
    try:
        from sage.all import plot, var, sin, pi
        import base64
        import tempfile
        import os
        from datetime import datetime
        
        # Create a simple plot
        x = var('x')
        p = plot(sin(x), (x, 0, 2*pi), title='Sine Wave')
        
        # Create a temporary directory for our test files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the plot to a file
            plot_path = os.path.join(temp_dir, 'test_plot.png')
            p.save(plot_path)
            
            # Read the image data
            with open(plot_path, 'rb') as f:
                image_data = f.read()
            
            # Get the MIME type based on file extension
            ext = os.path.splitext(plot_path)[1].lower().lstrip('.')
            mime_types = {
                'png': 'image/png',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'svg': 'image/svg+xml',
                'pdf': 'application/pdf'
            }
            mime_type = mime_types.get(ext, 'application/octet-stream')
            
            # Create data URI
            data_uri = f"data:{mime_type};base64,{base64.b64encode(image_data).decode('ascii')}"
            
            # Create a simple HTML file with the embedded image
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Test Plot Embedding</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1 {{ color: #333; }}
                    .plot {{ margin: 20px 0; }}
                </style>
            </head>
            <body>
                <h1>Test Plot Embedding</h1>
                <p>This is a test of embedding a Sage plot in HTML using a data URI.</p>
                
                <div class="plot">
                    <h2>Sine Wave Plot</h2>
                    <img src="{data_uri}" alt="Sine wave plot" />
                </div>
                
                <p>Plot generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </body>
            </html>
            """
            
            # Save the HTML file
            html_path = os.path.join(temp_dir, 'plot_embedding_test.html')
            with open(html_path, 'w') as f:
                f.write(html_content)
            
            print(f"Saved HTML test file to: {html_path}")
            print(f"Temporary plot file: {plot_path}")
            
            # Verify the HTML file was created
            assert os.path.exists(html_path), f"HTML file was not created at {html_path}"
            assert os.path.getsize(html_path) > 0, f"HTML file is empty: {html_path}"
            
            result.passed = True
    
    except Exception as e:
        result.passed = False
        result.error = str(e)
        print(f"Error in HTML embedding test: {e}")
        traceback.print_exc()
    
    return result


def run_compliance_suite():
    """Run the complete compliance test suite."""
    print(f"{BOLD}Sage Filter Test Suite{RESET}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Package directory: {PACKAGE_DIR}")
    
    # Check Sage version
    try:
        sage_version = subprocess.check_output(['sage', '--version']).decode().strip()
        print(f"Sage version: {sage_version}")
    except (subprocess.SubprocessError, FileNotFoundError):
        print(f"{YELLOW}Warning: Could not determine Sage version. Make sure 'sage' is in your PATH.{RESET}")
    
    print(f"\n{BOLD}Test Suite Summary{RESET}")
    start_time = datetime.now()
    print(f"Started at:  {start_time.isoformat()}")
    
    # Run all test modules
    all_results = []
    
    # List of all test modules to run
    test_modules = [
        # Core functionality tests
        'test_plot_generation',
        'test_html_embedding',
        'test_expectations',
        'test_pdf_output',
        'test_pdf_output_fixed',
        'test_sage_pdf_output',
        
        # Unit tests
        'unit.test_basic_math',
        
        # Integration tests
        'integration.test_symbolic_math',
        
        # Regression tests
        'regression.test_regressions',
    ]
    
    # Run all test modules
    for module_name in test_modules:
        try:
            all_results.extend(run_test_module(module_name))
        except ModuleNotFoundError as e:
            print(f"{YELLOW}Warning: Could not load test module {module_name}: {e}{RESET}")
    
    # Calculate statistics
    duration = datetime.now() - start_time
    total = len(all_results)
    passed = sum(1 for r in all_results if r.passed)
    failed = total - passed
    
    # Print detailed results
    print(f"\n{BOLD}Detailed Results:{RESET}")
    for i, result in enumerate(all_results, 1):
        status = f"{GREEN}✓{RESET}" if result.passed else f"{RED}✗{RESET}"
        print(f"{i:4d}. {result.name:60} {status} {result.duration:.3f}s")
        if not result.passed and result.error:
            print(f"      {RED}Error:{RESET} {result.error}")
    
    # Print summary
    print(f"\n{BOLD}Test Suite Summary{RESET}")
    print(f"Started at:  {start_time.isoformat()}")
    print(f"Duration:    {duration.total_seconds():.3f} seconds")
    print(f"Total tests: {total}")
    print(f"{GREEN}✓ Passed:     {passed}{RESET}")
    if failed > 0:
        print(f"{RED}✗ Failed:     {failed}{RESET}")
    success_rate = (passed / total * 100) if total > 0 else 0
    color = GREEN if success_rate > 90 else YELLOW if success_rate > 50 else RED
    print(f"{BOLD}Success rate:{RESET} {color}{success_rate:.1f}%{RESET}")
    
    # Exit with non-zero code if any tests failed
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
