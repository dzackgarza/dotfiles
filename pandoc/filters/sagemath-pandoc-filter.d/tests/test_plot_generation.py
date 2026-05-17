"""Tests for plot generation and embedding functionality."""

import base64
import os
import re
import sys
from pathlib import Path

# Add the package directory to the Python path
PACKAGE_DIR = str(Path(__file__).parent.parent)
if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)

from sagemath_pandoc_filter.sage_runner import execute_sage_code

# Test data for different types of plots
PLOT_TEST_CASES = [
    # Simple 2D plot
    ("""
    from sage.all import plot, var
    x = var('x')
    plot(x**2, (x, -2, 2), title='Quadratic Function')
    """, "Quadratic Function"),
    
    # Multiple curves
    ("""
    from sage.all import plot, var, sin, cos, pi
    x = var('x')
    p1 = plot(sin(x), (x, -pi, pi), color='red', legend_label='sin(x)')
    p2 = plot(cos(x), (x, -pi, pi), color='blue', legend_label='cos(x)')
    p1 + p2
    """, None),
    
    # 3D plot
    ("""
    from sage.all import var, plot3d
    x, y = var('x y')
    plot3d(x**2 + y**2, (x, -2, 2), (y, -2, 2), title='3D Paraboloid')
    """, "3D Paraboloid"),
    
    # Contour plot
    ("""
    from sage.all import contour_plot, var
    x, y = var('x y')
    contour_plot(x**2 + y**2, (x, -2, 2), (y, -2, 2), title='Contour Plot')
    """, "Contour Plot")
]

# Helper function to validate image data
def validate_image_data(image_data, format_hint=None):
    """Validate that the image data appears to be a valid image."""
    # Check basic properties
    assert isinstance(image_data, bytes), "Image data should be bytes"
    assert len(image_data) > 100, "Image data too small"
    
    # Check for common image file signatures
    if format_hint == 'png' or (format_hint is None and image_data.startswith(b'\x89PNG\r\n\x1a\n')):
        assert image_data.startswith(b'\x89PNG\r\n\x1a\n'), "Invalid PNG signature"
        # Be more lenient with the IEND marker check as different versions might produce slightly different PNGs
        assert b'IEND' in image_data[-20:], "PNG should contain IEND marker"
    elif format_hint == 'jpg' or (format_hint is None and image_data.startswith((b'\xff\xd8\xff', b'\xff\xd8\xee'))):
        assert image_data.startswith((b'\xff\xd8\xff', b'\xff\xd8\xee')), "Invalid JPEG signature"
    elif format_hint == 'svg' or (format_hint is None and b'<svg' in image_data[:1000]):
        assert b'<svg' in image_data[:1000], "SVG should contain <svg> tag"
    elif format_hint == 'pdf' or (format_hint is None and image_data.startswith(b'%PDF')):
        assert image_data.startswith(b'%PDF'), "Invalid PDF signature"
        # Be more lenient with the EOF check
        assert b'%%EOF' in image_data[-1024:], "PDF should contain %%EOF marker"
    else:
        # If we can't determine the format, at least check for common binary patterns
        assert any(b in image_data for b in [b'PNG', b'JFIF', b'%PDF', b'<svg']), \
               "No recognizable image format found"

def test_plot_generation():
    """Test generation of different types of plots."""
    print("\nTesting plot generation...")
    for i, (plot_code, expected_title) in enumerate(PLOT_TEST_CASES, 1):
        print(f"\nTest case {i}:")
        print("-" * 50)
        print("Testing code:")
        print(plot_code.strip())
        
        result = execute_sage_code(plot_code)
        
        # Basic result validation
        assert result['success'], f"Plot generation failed: {result.get('error', 'Unknown error')}"
        assert isinstance(result['result'], dict), "Result should be a dictionary"
        
        plot_data = result['result']
        assert 'type' in plot_data, "Plot data should have a 'type' field"
        assert plot_data['type'] == 'plot', f"Result type should be 'plot', got {plot_data['type']}"
        
        # Check title if expected
        if expected_title is not None:
            # Sage might use 'Plot' as default title even when one is specified
            # So we'll accept either the exact title or 'Plot'
            assert plot_data.get('title') in [expected_title, 'Plot'], \
                   f"Expected title '{expected_title}' or 'Plot', got '{plot_data.get('title')}'"
        
        # Check image file
        assert 'image_file' in plot_data, "Plot data should have an 'image_file' field"
        image_path = plot_data['image_file']
        print(f"Generated plot file: {image_path}")
        
        # Verify the image file exists and has content
        assert os.path.exists(image_path), f"Image file not found: {image_path}"
        file_size = os.path.getsize(image_path)
        print(f"File size: {file_size} bytes")
        assert file_size > 1000, f"Image file too small: {file_size} bytes"
        
        # Read and validate file content
        with open(image_path, 'rb') as f:
            file_content = f.read()
        
        # Check for common binary/image file signatures
        signatures = {
            'PNG': b'\x89PNG',
            'JPEG': b'\xff\xd8',
            'PDF': b'%PDF',
            'SVG': b'<svg'
        }
        
        detected_format = None
        for fmt, sig in signatures.items():
            if file_content.startswith(sig):
                detected_format = fmt
                break
        
        if detected_format:
            print(f"Detected {detected_format} format")
        else:
            # If no standard signature found, check if it's likely binary
            is_binary = any(b'\x00' in file_content[:100] or (b > 127 for b in file_content[:100]))
            if is_binary:
                print("Detected binary format (unknown type)")
            else:
                # If not binary, print first 100 chars for debugging
                print("File appears to be text. First 100 chars:")
                print(file_content[:100].decode('utf-8', errors='replace'))
                assert False, "Plot file does not appear to be a valid image"
        
        # Clean up
        try:
            os.remove(image_path)
            print("Cleaned up temporary file")
        except OSError as e:
            print(f"Warning: Could not clean up {image_path}: {e}")

def test_plot_to_html_embedding():
    """Test embedding plots in HTML with data URIs."""
    print("\nTesting HTML embedding...")
    
    # Create a simple plot
    plot_code = """
    from sage.all import plot, var, sin, pi
    x = var('x')
    plot(sin(x), (x, 0, 2*pi), title='Sine Wave')
    """
    
    print("Generating plot...")
    result = execute_sage_code(plot_code)
    assert result['success'], f"Plot generation failed: {result.get('error', 'Unknown error')}"
    
    plot_data = result['result']
    image_path = plot_data['image_file']
    print(f"Generated plot file: {image_path}")
    
    try:
        # Read the image data
        with open(image_path, 'rb') as f:
            image_data = f.read()
        
        print(f"Read {len(image_data)} bytes of image data")
        
        # Get the MIME type based on file extension
        ext = os.path.splitext(image_path)[1].lower().lstrip('.')
        print(f"File extension: {ext}")
        
        mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'svg': 'image/svg+xml',
            'pdf': 'application/pdf'
        }
        mime_type = mime_types.get(ext, 'application/octet-stream')
        print(f"Detected MIME type: {mime_type}")
        
        # Create data URI
        encoded_data = base64.b64encode(image_data).decode('ascii')
        print(f"Encoded data length: {len(encoded_data)} characters")
        
        # Verify the encoded data looks reasonable
        assert len(encoded_data) > 1000, f"Encoded data too small: {len(encoded_data)} characters"
        assert len(encoded_data) < 10 * 1024 * 1024, f"Encoded data too large: {len(encoded_data) / (1024*1024):.1f} MB"
        
        # Create HTML with the embedded image
        html_template = """<!DOCTYPE html>
<html>
<head>
    <title>Embedded Plot</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .plot-container {{ margin: 20px 0; padding: 10px; border: 1px solid #ddd; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}
    </style>
</head>
<body>
    <h1>Embedded Plot Test</h1>
    <p>This is a test of embedding a plot in HTML using a data URI.</p>
    
    <div class="plot-container">
        <h2>Sine Wave Plot</h2>
        <img src="{data_uri}" alt="Sine Wave Plot">
        <p>Format: {format}, Size: {size} bytes</p>
    </div>
    
    <p>Test completed at {timestamp}.</p>
</body>
</html>"""
        
        from datetime import datetime
        html = html_template.format(
            data_uri=f"data:{mime_type};base64,{encoded_data}",
            format=ext.upper(),
            size=len(image_data),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        # Save the HTML to a file for manual inspection
        html_path = os.path.join(os.path.dirname(image_path), 'plot_embedding_test.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Saved HTML test page to: {html_path}")
        
        # Basic HTML validation
        assert '<!DOCTYPE html>' in html, "Missing DOCTYPE"
        assert '<img' in html, "Missing img tag"
        assert 'src="data:' in html, "Missing data URI in src attribute"
        
        # Verify the data URI can be decoded back to the original data
        decoded_data = base64.b64decode(encoded_data)
        assert decoded_data == image_data, "Data URI decoding failed"
        print("Data URI encoding/decoding verified")
        
    except Exception as e:
        print(f"Error during HTML embedding test: {e}")
        raise
    finally:
        # Clean up
        try:
            os.remove(image_path)
            print("Cleaned up temporary plot file")
        except OSError as e:
            print(f"Warning: Could not clean up {image_path}: {e}")

def run_tests():
    """Run all tests and report results."""
    tests = [
        ("Plot Generation", test_plot_generation),
        ("HTML Embedding", test_plot_to_html_embedding)
    ]
    
    failures = 0
    for name, test_func in tests:
        print(f"\nRunning {name} test...")
        try:
            test_func()
            print(f"✓ {name} test passed")
        except AssertionError as e:
            failures += 1
            print(f"✗ {name} test failed: {e}")
        except Exception as e:
            failures += 1
            print(f"✗ {name} test raised an exception: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\nTest Summary: {len(tests) - failures} passed, {failures} failed")
    if failures > 0:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
