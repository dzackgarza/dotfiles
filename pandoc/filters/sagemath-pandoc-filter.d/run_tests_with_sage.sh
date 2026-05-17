#!/bin/bash
# Run tests with Sage's Python interpreter

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the test file with Sage's Python
/usr/bin/sage -python -c "
import sys
import os

# Add the package directory to the Python path
package_dir = os.path.abspath(os.path.join('$SCRIPT_DIR', '.'))
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

# Import and run the test module
test_module = sys.argv[1] if len(sys.argv) > 1 else 'tests.unit.test_basic_math'
print(f'Running tests in {test_module}...\n')

# Import the test module
__import__(test_module)

# Get the test class and run its tests
test_class = None
module = sys.modules[test_module]
for name, obj in module.__dict__.items():
    if name.startswith('Test') and hasattr(obj, '__test__') and obj.__test__:
        test_class = obj
        break

if test_class:
    test = test_class()
    # Run all test methods that start with 'test_'
    for method_name in dir(test):
        if method_name.startswith('test_'):
            print(f'Running {method_name}...')
            getattr(test, method_name)()
            print(f'✓ {method_name} passed\n')
" "$@"
