"""Real Sage environment for testing.

This module provides a real Sage environment for testing, using the actual Sage installation
on the system rather than a mock implementation.
"""
import sage.all
from sage.repl.rich_output import get_display_manager
from sage.repl.rich_output.display_manager import get_display_manager as get_dm

# Global dictionary to maintain state between execute_sage_code calls
_execution_state = {}

def execute_sage_code(code):
    """Execute Sage code and return the result.
    
    Args:
        code (str): Sage code to execute
        
    Returns:
        dict: Dictionary with 'success' (bool), 'result' (any), 'output' (str),
              and optionally 'error' (str) if execution failed
    """
    global _execution_state
    
    try:
        # Capture the output
        from io import StringIO
        import sys
        import ast
        
        old_stdout = sys.stdout
        sys.stdout = output = StringIO()
        
        # Create a copy of the globals to avoid polluting the namespace
        # and maintain state between calls
        local_vars = _execution_state.copy()
        global_vars = {'__builtins__': {}}
        global_vars.update(sage.all.__dict__)
        
        try:
            # Clean up the code by removing empty lines and comments
            lines = [line for line in code.split('\n') if line.strip() and not line.strip().startswith('#')]
            if not lines:
                return {'success': True, 'result': None, 'output': ''}
                
            # Join non-empty lines with newlines
            clean_code = '\n'.join(lines)
            
            # Try to parse the code to understand its structure
            try:
                # Try to parse as a module to detect expressions vs statements
                parsed = ast.parse(clean_code, mode='exec')
                
                # If there's only one node and it's an expression, evaluate it
                if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
                    # It's a simple expression, evaluate it
                    result = eval(compile(ast.Expression(parsed.body[0].value), '<string>', 'eval'), 
                                global_vars, local_vars)
                else:
                    # It's one or more statements, execute them
                    exec(clean_code, global_vars, local_vars)
                    
                    # If the last statement is an expression, get its value
                    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
                        last_expr = ast.Expression(parsed.body[-1].value)
                        ast.fix_missing_locations(last_expr)
                        result = eval(compile(last_expr, '<string>', 'eval'), 
                                    global_vars, local_vars)
                    else:
                        result = None
            except (SyntaxError, IndentationError):
                # If parsing fails, try direct execution
                try:
                    # Try as a single expression first
                    result = eval(clean_code, global_vars, local_vars)
                except:
                    # If that fails, try as statements
                    exec(clean_code, global_vars, local_vars)
                    result = None
            
            # Update the execution state with any new or modified variables
            _execution_state.update({
                k: v for k, v in local_vars.items() 
                if not k.startswith('_') and k not in global_vars
            })
            
            output_str = output.getvalue()
            return {
                'success': True,
                'result': result,
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

# Alias for backward compatibility
mock_sage = type('MockSage', (), {'execute_code': staticmethod(execute_sage_code)})()
