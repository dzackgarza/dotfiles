"""Check Sage installation and environment."""
import sys
import os
import subprocess
from pathlib import Path

def check_sage():
    """Check Sage installation and environment."""
    print("=" * 80)
    print("Sage Environment Check")
    print("=" * 80)
    
    # Check Python executable
    print(f"\nPython executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Check Sage installation
    try:
        sage_path = subprocess.check_output(["which", "sage"]).decode().strip()
        print(f"\nFound Sage at: {sage_path}")
        
        # Get Sage's Python
        sage_python = subprocess.check_output(["sage", "-python", "-c", 
                                            "import sys; print(sys.executable)"]).decode().strip()
        print(f"Sage's Python: {sage_python}")
        
        # Get Sage's Python version
        sage_version = subprocess.check_output(["sage", "-python", "-c", 
                                             "import sys; print(sys.version)"]).decode().strip()
        print(f"Sage's Python version: {sage_version}")
        
        # Check if we can import sage.all
        try:
            output = subprocess.check_output(["sage", "-python", "-c", 
                                           "from sage.all import *; print('Sage import successful')"])
            print(output.decode().strip())
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to import sage.all: {e}")
            print("Error output:", e.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print("Sage not found in PATH")
        return False

if __name__ == "__main__":
    if check_sage():
        print("\nSage environment is properly set up!")
    else:
        print("\nSage environment check failed.")
        sys.exit(1)
