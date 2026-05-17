#!/usr/bin/env python3

"""
Direct test of Sage code execution.
"""

import sys
import os

print("=== Starting Sage Test ===")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"sys.path: {sys.path}")

try:
    print("\n=== Importing Sage modules ===")
    from sage.all import *
    print("Successfully imported sage.all")
    
    # Test basic math
    print("\n=== Testing basic math ===")
    result = 2 + 2
    print(f"2 + 2 = {result}")
    assert result == 4, f"Expected 4, got {result}"
    
    # Test variable assignment
    print("\n=== Testing variable assignment ===")
    x = 2 + 2
    y = x * 2
    print(f"x = {x}, y = {y}")
    assert x == 4, f"Expected x to be 4, got {x}"
    assert y == 8, f"Expected y to be 8, got {y}"
    
    # Test Sage expressions
    print("\n=== Testing Sage expressions ===")
    x = var('x')
    f = x**2 + 1
    result = f.subs(x=2)
    print(f"f(x) = {f}")
    print(f"f(2) = {result}")
    assert result == 5, f"Expected 5, got {result}"
    
    # Test plot
    print("\n=== Testing plot ===")
    p = plot(x**2, (x, -2, 2), title='Parabola')
    print(f"Created plot: {p}")
    print(f"Plot type: {type(p)}")
    print(f"Has save method: {hasattr(p, 'save')}")
    
    # Test saving the plot
    plot_file = "test_plot.png"
    p.save(plot_file)
    print(f"Saved plot to {plot_file}")
    assert os.path.exists(plot_file), f"Plot file {plot_file} was not created"
    print(f"Plot file size: {os.path.getsize(plot_file)} bytes")
    
    print("\n=== All tests passed! ===")
    
except Exception as e:
    print(f"\n=== Test failed ===")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
