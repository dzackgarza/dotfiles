"""Direct test of the sagemath-pandoc-filter functionality."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

def test_sage_filter_basic_math():
    """Test that the sage filter correctly processes basic math expressions."""
    # Create a simple JSON document that pandoc would pass to the filter
    doc = {
        "pandoc-api-version": [1, 22],
        "meta": {},
        "blocks": [
            {
                "t": "CodeBlock",
                "c": [
                    ["", ["sage"], []],
                    "2 + 2"
                ]
            }
        ]
    }
    
    # Write the document to a temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        json.dump(doc, f)
        input_file = f.name
    
    try:
        # Get the path to the filter module
        package_dir = Path(__file__).parent.parent
        
        # Use the current Python interpreter (which should be Sage's Python)
        cmd = [sys.executable, '-m', 'sagemath_pandoc_filter.filter']
        
        # Set PYTHONPATH to include the package directory
        env = os.environ.copy()
        env['PYTHONPATH'] = str(package_dir) + (os.pathsep + env.get('PYTHONPATH', '') if env.get('PYTHONPATH') else '')
        
        with open(input_file, 'r') as f_in:
            result = subprocess.run(
                cmd,
                stdin=f_in,
                capture_output=True,
                text=True,
                env=env
            )
        
        # Check that the command succeeded
        assert result.returncode == 0, f"Filter failed with return code {result.returncode}"
        assert not result.stderr, f"Filter produced stderr: {result.stderr}"
        
        # Parse the output
        output = json.loads(result.stdout)
        
        # Check the output structure
        assert 'blocks' in output, "Output missing 'blocks' key"
        assert len(output['blocks']) == 1, f"Expected 1 block, got {len(output['blocks'])}"
        assert output['blocks'][0]['t'] == 'Para', f"Expected Para block, got {output['blocks'][0]['t']}"
        assert len(output['blocks'][0]['c']) == 1, f"Expected 1 element in Para, got {len(output['blocks'][0]['c'])}"
        assert output['blocks'][0]['c'][0]['t'] == 'Str', f"Expected Str element, got {output['blocks'][0]['c'][0]['t']}"
        assert output['blocks'][0]['c'][0]['c'] == '4', f"Expected '4', got {output['blocks'][0]['c'][0]['c']}"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(input_file):
            os.unlink(input_file)

def test_sage_filter_plot():
    """Test that the sage filter correctly processes plot expressions."""
    print("Starting test_sage_filter_plot...")
    # Create a JSON document with a plot expression
    doc = {
        "pandoc-api-version": [1, 22],
        "meta": {},
        "blocks": [
            {
                "t": "CodeBlock",
                "c": [
                    ["", ["sage"], []],
                    "from sage.all import plot, var\nx = var('x')\nplot(x**2, (x, -2, 2), title='Parabola')"
                ]
            }
        ]
    }
    print("Created test document")
    
    # Write the document to a temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        json.dump(doc, f)
        input_file = f.name
    
    try:
        # Get the path to the filter module
        package_dir = Path(__file__).parent.parent
        
        # Use the current Python interpreter (which should be Sage's Python)
        cmd = [sys.executable, '-m', 'sagemath_pandoc_filter.filter']
        
        # Set PYTHONPATH to include the package directory
        env = os.environ.copy()
        env['PYTHONPATH'] = str(package_dir) + (os.pathsep + env.get('PYTHONPATH', '') if env.get('PYTHONPATH') else '')
        
        with open(input_file, 'r') as f_in:
            result = subprocess.run(
                cmd,
                stdin=f_in,
                capture_output=True,
                text=True,
                env=env
            )
        
        # Check that the command succeeded
        assert result.returncode == 0, f"Filter failed with return code {result.returncode}"
        assert not result.stderr, f"Filter produced stderr: {result.stderr}"
        
        # Parse the output
        output = json.loads(result.stdout)
        
        # Check the output structure
        assert 'blocks' in output, "Output missing 'blocks' key"
        assert len(output['blocks']) == 1, f"Expected 1 block, got {len(output['blocks'])}"
        assert output['blocks'][0]['t'] == 'Para', f"Expected Para block, got {output['blocks'][0]['t']}"
        assert len(output['blocks'][0]['c']) == 1, f"Expected 1 element in Para, got {len(output['blocks'][0]['c'])}"
        
        # The output should be a Para containing an Image
        assert output['blocks'][0]['t'] == 'Para', f"Expected Para block, got {output['blocks'][0]['t']}"
        assert len(output['blocks'][0]['c']) == 1, f"Expected 1 element in Para, got {len(output['blocks'][0]['c'])}"
        assert output['blocks'][0]['c'][0]['t'] == 'Image', f"Expected Image element, got {output['blocks'][0]['c'][0]['t']}"
        
        # Check the image details
        image = output['blocks'][0]['c'][0]['c']
        assert len(image) == 3, f"Expected 3 elements in Image, got {len(image)}"
        assert isinstance(image[0], list), f"Expected list as first element of Image, got {type(image[0])}"
        assert isinstance(image[1], list), f"Expected list as second element of Image, got {type(image[1])}"
        assert len(image[2]) == 2, f"Expected 2 elements in image path/title, got {len(image[2])}"
        
        # Check the image path and title
        image_path, image_title = image[2]
        assert image_path.endswith('.png'), f"Expected .png image path, got {image_path}"
        assert 'sage_plot_' in image_path, f"Expected sage_plot_ in image path, got {image_path}"
        
    finally:
        # Clean up the temporary file
        if os.path.exists(input_file):
            os.unlink(input_file)

def run_tests():
    """Run all tests and exit with appropriate status code."""
    tests = [
        test_sage_filter_basic_math,
        test_sage_filter_plot
    ]
    
    failures = 0
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__} passed")
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failures += 1
    
    if failures == 0:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print(f"\n{failures} test(s) failed")
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
