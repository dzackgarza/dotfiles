"""Pytest configuration and fixtures for Sage Filter tests."""
import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Add the package directory to the Python path
PACKAGE_DIR = str(Path(__file__).parent.parent)
if PACKAGE_DIR not in sys.path:
    sys.path.insert(0, PACKAGE_DIR)

# Check if Sage is available
try:
    from sage.all import *  # noqa: F401
    SAGE_AVAILABLE = True
except ImportError:
    SAGE_AVAILABLE = False

# Skip all tests that require Sage if it's not available
if not SAGE_AVAILABLE:
    collect_ignore_glob = ["*"]


@pytest.fixture(scope="session")
def temp_dir() -> Generator[str, None, None]:
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory(prefix="sage_filter_test_") as temp_dir:
        yield temp_dir


@pytest.fixture(autouse=True)
def add_imports(doctest_namespace):
    """Make common imports available in doctests."""
    import math
    import os
    import sys
    from pathlib import Path

    doctest_namespace["math"] = math
    doctest_namespace["os"] = os
    doctest_namespace["sys"] = sys
    doctest_namespace["Path"] = Path

    # Add Sage imports if available
    if SAGE_AVAILABLE:
        from sage.all import *  # noqa: F401, F403
        doctest_namespace.update({
            "sage.all": sage.all,
            "var": sage.all.var,
            "plot": sage.all.plot,
            "show": sage.all.show,
        })


# Configure logging for tests
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sagemath_pandoc_filter")
logger.setLevel(logging.DEBUG if os.environ.get("DEBUG") else logging.INFO)
