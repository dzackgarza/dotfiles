"""Sage code execution for Pandoc filter.

This module provides functions to execute Sage code in the context of a Pandoc filter.
It's designed to be run with Sage's Python interpreter.
"""

import sys
from io import StringIO
from typing import Any

# Import Sage functions at module level
from sage.all import *


def execute_sage_code(code: str) -> dict[str, Any]:
    """
    Execute Sage code and return the result.

    Args:
        code: The Sage code to execute

    Returns:
        A dictionary containing:
        - success: boolean indicating if execution was successful
        - output: captured stdout/stderr output
        - result: the result of the last expression (if any)
        - error: error message if execution failed
    """
    # Redirect stdout to capture output
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # Import Sage modules
        try:
            import sage.all

            # Create a dictionary to store local variables
            local_vars = {}
        except ImportError as e:
            return {
                "success": False,
                "output": "",
                "error": f"Failed to import sage.all: {str(e)}",
            }

        # Split code into lines and remove empty lines
        lines = [line.strip() for line in code.strip().split("\n") if line.strip()]
        if not lines:
            return {"success": True, "output": "", "result": None}

        # Execute all but the last line as statements
        if len(lines) > 1:
            exec("\n".join(lines[:-1]), local_vars, local_vars)

        # Try to evaluate the last line as an expression
        last_line = lines[-1].strip()
        result = None

        try:
            # First try to evaluate the last line as an expression
            result = eval(last_line, local_vars, local_vars)
        except SyntaxError, NameError:
            # If evaluation fails, try to execute it as a statement
            try:
                exec(last_line, local_vars, local_vars)
                # If it was a statement with no return value, use None
                result = None
            except Exception as e:
                # If execution fails, re-raise the exception
                raise e

        # Get the captured output
        output_str = sys.stdout.getvalue()

        # Handle plot objects — detect by module, not just .save() existence.
        # Non-plot Sage objects (Integer, GaloisGroup, etc.) also have .save(),
        # but their module does NOT start with 'sage.plot'.
        is_plot = (
            hasattr(result, "save")
            and callable(getattr(result, "save"))
            and type(result).__module__.startswith("sage.plot")
        )
        if is_plot:
            import hashlib
            import os
            import tempfile

            # Create a unique filename based on the code
            code_hash = hashlib.md5(code.encode()).hexdigest()
            img_dir = os.path.join(tempfile.gettempdir(), "sage_images")
            os.makedirs(img_dir, exist_ok=True)
            img_path = os.path.join(img_dir, f"sage_plot_{code_hash}.png")

            # Save the plot
            result.save(img_path)
            result = {
                "image_file": img_path,
                "type": "plot",
                "title": getattr(result, "title", "Plot") or "Plot",
            }
        # Handle symbolic expressions
        elif hasattr(result, "subs") and callable(getattr(result, "subs")):
            # Convert to string for now
            result = str(result)

        return {"success": True, "output": output_str.strip(), "result": result}

    except Exception as e:
        # Get any output before the error
        output_str = sys.stdout.getvalue()
        return {"success": False, "output": output_str.strip(), "error": str(e)}

    finally:
        # Restore stdout
        sys.stdout = old_stdout
