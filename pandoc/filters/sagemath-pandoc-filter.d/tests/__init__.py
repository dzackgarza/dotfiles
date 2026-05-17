"""Test suite for sagemath-pandoc-filter."""

__version__ = "1.0.0"

# Import test modules to make them discoverable
from . import unit
from . import integration
from . import regression

__all__ = [
    'unit',
    'integration',
    'regression',
]
