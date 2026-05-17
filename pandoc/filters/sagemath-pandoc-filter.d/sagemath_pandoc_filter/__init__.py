"""Sage Filter for Pandoc.

This package provides a Pandoc filter for processing SageMath code blocks
and inline expressions in Markdown documents.
"""

__version__ = "0.1.0"

# Import available components
try:
    from .sage_plot import generate_plot
    __all__ = ['generate_plot']
except ImportError:
    generate_plot = None
    __all__ = []

# Import SageRunner if available
try:
    from .sage_runner import SageRunner
    __all__.append('SageRunner')
except ImportError:
    SageRunner = None
