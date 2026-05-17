"""Sage plot generation utilities."""

import os
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional

def _execute_plot_code(code: str, image_dir: str) -> Dict[str, Any]:
    """
    Execute plot generation code and return the result.
    
    Args:
        code: Sage code that generates a plot
        image_dir: Directory to save the plot
        
    Returns:
        Dictionary containing success status and output/error message
    """
    try:
        # Create a clean namespace for execution
        local_vars = {}
        global_vars = {}
        
        # Execute the code
        exec(code, global_vars, local_vars)
        
        # Check if a plot was created
        if 'p' not in local_vars or not hasattr(local_vars['p'], 'save'):
            return {'success': False, 'error': 'No plot object found. Assign your plot to variable p.'}
        
        plot_obj = local_vars['p']
        
        # Ensure the output directory exists
        Path(image_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate a unique filename based on the code
        code_hash = hashlib.sha1(code.encode('utf-8')).hexdigest()
        
        # Determine if this is a 3D plot
        is_3d = 'Graphics3d' in str(type(plot_obj))
        ext = 'png' if is_3d else 'pdf'
        
        # Create the output filename
        output_path = str(Path(image_dir) / f"{code_hash}_{'3d' if is_3d else '2d'}.{ext}")
        
        # Save the plot with appropriate settings
        save_args = {}
        if not is_3d:
            save_args['typeset'] = 'latex'
            
        plot_obj.save(output_path, **save_args)
        
        return {
            'success': True,
            'output': output_path
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Error generating plot: {str(e)}'
        }

def generate_plot(code: str, image_dir: str) -> Dict[str, Any]:
    """
    Generate a plot from Sage code.
    
    Args:
        code: Sage code that generates a plot (assigned to variable 'p')
        image_dir: Directory to save the generated plot
        
    Returns:
        Dictionary containing:
        - success: Boolean indicating if plot was generated
        - output: Path to the generated plot (if successful)
        - error: Error message (if failed)
    """
    return _execute_plot_code(code, image_dir)
