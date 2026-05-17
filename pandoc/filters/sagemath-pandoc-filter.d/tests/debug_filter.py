"""Debug the sagemath-pandoc-filter functionality."""

import json
import os
import sys
from pathlib import Path

# Create a simple JSON document that pandoc would pass to the filter
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
    ]}

# Print the input document
print("Input document:")
print(json.dumps(doc, indent=2))
print("\n" + "="*80 + "\n")

# Add the package directory to the Python path
package_dir = str(Path(__file__).parent.parent)
sys.path.insert(0, package_dir)

# Import and run the filter
print("Running filter...\n")
try:
    from sagemath_pandoc_filter.filter import process_sage_code
    
    # Create a simple document with just our code block
    from panflute import Doc, CodeBlock, Para, Str, Image, debug
    
    # Create a panflute document with a CodeBlock
    code_block = CodeBlock(
        "from sage.all import plot, var\nx = var('x')\nplot(x**2, (x, -2, 2), title='Parabola')",
        classes=['sage'],
        attributes={}
    )
    
    # Create a document with the code block
    doc = Doc()
    doc.content.append(code_block)
    
    # Process the document
    print("Processing document...")
    
    # Define a custom walk function to handle the result
    def process_doc(doc):
        from panflute import Para
        
        for i, block in enumerate(list(doc.content)):  # Create a copy of the list for iteration
            if isinstance(block, CodeBlock) and 'sage' in block.classes:
                result = process_sage_code(block, doc)
                if result is not None:
                    # Convert the result to a list if it's not already one
                    results = result if isinstance(result, list) else [result]
                    
                    # Replace the code block with the results
                    for j, res in enumerate(results):
                        # If the result is an Image, wrap it in a Para
                        if hasattr(res, 'tag') and res.tag == 'Image':
                            results[j] = Para(res)
                    
                    # Replace the code block with the processed results
                    doc.content[i:i+1] = results
        return doc
    
    # Process the document
    doc = process_doc(doc)
    
    # Print the result
    print("\nResulting document:")
    
    # Print the document structure
    def print_element(elem, indent=0):
        indent_str = '  ' * indent
        if hasattr(elem, 'tag'):
            print(f"{indent_str}{elem.tag}:")
            if hasattr(elem, 'attributes'):
                for k, v in elem.attributes.items():
                    print(f"{indent_str}  {k}: {v}")
            if hasattr(elem, 'content'):
                for child in elem.content:
                    print_element(child, indent + 1)
        elif hasattr(elem, 'text'):
            print(f"{indent_str}Text: {elem.text}")
        else:
            print(f"{indent_str}{elem}")
    
    # Print the document content
    for i, block in enumerate(doc.content):
        print(f"\nBlock {i}:")
        print_element(block)
    
    # Also print the raw JSON output from the filter
    print("\nRaw filter output:")
    
    # Convert the document to a format that can be serialized to JSON
    def doc_to_dict(doc):
        from panflute import convert_text, dump
        # Convert the document to a JSON string and then parse it back to a dict
        json_str = convert_text(doc, input_format='panflute', output_format='json')
        return json.loads(json_str)
    
    import subprocess
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        doc_dict = doc_to_dict(doc)
        json.dump(doc_dict, f)
        input_file = f.name
    
    try:
        cmd = [sys.executable, '-m', 'sagemath_pandoc_filter.filter']
        with open(input_file, 'r') as f_in:
            result = subprocess.run(
                cmd,
                stdin=f_in,
                capture_output=True,
                text=True
            )
        
        print(f"Exit code: {result.returncode}")
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        if result.stdout:
            print(f"Stdout: {result.stdout}")
    finally:
        if os.path.exists(input_file):
            os.unlink(input_file)
    
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
