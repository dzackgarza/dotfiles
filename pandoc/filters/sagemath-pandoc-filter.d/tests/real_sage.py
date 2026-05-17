"""Real Sage environment for testing."""
import sage.all
from sage.repl.rich_output import get_display_manager
from sage.repl.rich_output.display_manager import get_display_manager as get_dm

def execute_sage_code(code):
    """Execute Sage code and return the result.
    
    Args:
        code (str): Sage code to execute
        
    Returns:
        dict: Dictionary with 'success' (bool), 'result' (any), and 'output' (str)
    """
    try:
        # Capture the output
        from io import StringIO
        import sys
        
        old_stdout = sys.stdout
        sys.stdout = output = StringIO()
        
        # Execute the code in the Sage environment
        local_vars = {}
        try:
            # First try to evaluate as an expression
            result = eval(code, {'__builtins__': {}}, sage.all.__dict__)
            output_str = output.getvalue()
            return {
                'success': True,
                'result': result,
                'output': output_str
            }
        except:
            # If evaluation fails, try execution
            try:
                exec(code, {'__builtins__': {}}, sage.all.__dict__)
                output_str = output.getvalue()
                return {
                    'success': True,
                    'result': None,
                    'output': output_str
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e),
                    'output': output.getvalue()
                }
        finally:
            sys.stdout = old_stdout
            output.close()
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'output': ''
        }
