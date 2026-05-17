"""Tests for HTML embedding functionality."""

import os
import base64
from pathlib import Path
from typing import Dict, Any

def test_plot_to_html_embedding():
    """Test converting a plot to an HTML-embedded image."""
    # Create and return a simple plot - the execute_sage_code function will handle saving it
    code = """
    from sage.all import plot, var, sin, pi
    x = var('x')
    p = plot(sin(x), (x, 0, 2*pi), title='Sine Wave')
    p  # Return the plot object
    """
    
    print("\n=== Debug: Starting test_plot_to_html_embedding ===")
    print(f"Code to execute:\n{code}")
    
    # Execute the Sage code
    from sagemath_pandoc_filter.sage_runner import execute_sage_code
    result = execute_sage_code(code)
    
    print("\n=== Debug: execute_sage_code result ===")
    print(f"Success: {result.get('success')}")
    print(f"Output: {result.get('output')}")
    print(f"Error: {result.get('error')}")
    print(f"Result keys: {list(result.keys())}")
    
    # Check if plot was generated
    if not result['success']:
        print(f"\n=== Debug: Plot generation failed ===")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    assert result['success'], f"Plot generation failed: {result.get('error', 'Unknown error')}"
    
    # The image file path is in result['result']['image_file']
    if 'result' not in result or not isinstance(result['result'], dict):
        print("\n=== Debug: Invalid result format ===")
        print(f"Result content: {result}")
        assert False, f"Unexpected result format: {result}"
    
    if 'image_file' not in result['result']:
        print("\n=== Debug: No image file in result['result'] ===")
        print(f"Result content: {result}")
        print(f"Result['result'] content: {result['result']}")
        assert False, f"No image file generated in result: {result}"
    
    # Read the image data
    image_path = result['result']['image_file']
    print(f"\n=== Debug: Image path: {image_path} ===")
    
    # Verify the image file exists
    if not os.path.exists(image_path):
        print(f"\n=== Debug: Image file does not exist at {image_path} ===")
        print(f"Directory contents: {os.listdir(os.path.dirname(image_path))}")
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    print(f"Read {len(image_data)} bytes of image data")
    
    # Convert to base64
    encoded = base64.b64encode(image_data).decode('utf-8')
    
    # Create HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Embedded Plot Test</title>
    </head>
    <body>
        <h1>Embedded Plot Test</h1>
        <img src="data:image/png;base64,{encoded}" alt="Sine Wave">
    </body>
    </html>
    """
    
    # Save HTML to a file for manual verification
    output_dir = Path('test_output')
    output_dir.mkdir(exist_ok=True)
    html_path = output_dir / 'embedded_plot_test.html'
    with open(html_path, 'w') as f:
        f.write(html)
    
    print(f"\n=== Debug: Saved HTML to {html_path} ===")
    
    # Verify the file was created
    if not html_path.exists():
        print(f"\n=== Debug: HTML file was not created at {html_path} ===")
    if html_path.stat().st_size == 0:
        print(f"\n=== Debug: HTML file is empty at {html_path} ===")
    
    assert html_path.exists(), "HTML file was not created"
    assert html_path.stat().st_size > 0, "HTML file is empty"
    
    # Clean up
    if os.path.exists(image_path):
        os.remove(image_path)
    
    return "Successfully generated HTML with embedded plot"
