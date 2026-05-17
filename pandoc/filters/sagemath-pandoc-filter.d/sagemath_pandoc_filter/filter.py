"""Pandoc filter for processing Sage code blocks."""

import panflute as pf
from .sage_runner import execute_sage_code

def prepare(doc=None):
    """Initialize the filter.
    
    Args:
        doc: The document being processed (unused in this implementation)
    """
    pass

def finalize(doc=None):
    """Clean up after processing.
    
    Args:
        doc: The document being processed (unused in this implementation)
    """
    pass

def process_sage_code(elem, doc):
    """Process a Sage code block.
    
    Args:
        elem: The code block element
        doc: The document being processed
        
    Returns:
        The processed element(s) to replace the code block with
    """
    if not (isinstance(elem, pf.CodeBlock) and 'sage' in elem.classes):
        return None
        
    # Execute the Sage code
    result = execute_sage_code(elem.text)
    
    if not result['success']:
        return pf.Para(pf.Str(f"Error: {result.get('error', 'Unknown error')}"))
    
    # Create output elements
    output = []
    
    # Add the result
    if 'result' in result and result['result'] is not None:
        if isinstance(result['result'], dict) and 'image_file' in result['result']:
            # Handle plot output - wrap Image in a Para
            try:
                with open(result['result']['image_file'], 'rb') as f:
                    image_data = f.read()
                image = pf.Image(
                    url=result['result']['image_file'],
                    title=result['result'].get('title', 'Plot'),
                    identifier='',
                    attributes={}
                )
                # Wrap the image in a Para block
                output.append(pf.Para(image))
            except Exception as e:
                output.append(pf.Para(pf.Str(f"Error loading plot: {str(e)}")))
        else:
            # Handle text output
            output.append(pf.Para(pf.Str(str(result['result']))))
    
    # Add any captured output
    if result.get('output'):
        output.append(pf.Para(pf.Str(result['output'])))
    
    # Return the first element if there's only one, otherwise return a Div containing all elements
    if len(output) == 1:
        return output[0]
    elif output:
        return pf.Div(*output)
    return None

def main(doc=None):
    """Run the Pandoc filter.
    
    Args:
        doc: The document to process (used by Panflute)
        
    Returns:
        The processed document
    """
    if doc is None:
        # Called as a script
        return pf.run_filter(process_sage_code, prepare=prepare, finalize=finalize, doc=doc)
    else:
        # Called as a function
        doc = doc.walk(process_sage_code)
        return doc

if __name__ == '__main__':
    main()
