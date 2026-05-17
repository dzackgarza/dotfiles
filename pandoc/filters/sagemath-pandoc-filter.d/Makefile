.PHONY: test test-unit test-integration test-regression coverage lint format clean

# Variables
PYTHON ?= python
PIP ?= pip
COVERAGE_FILE = .coverage
COVERAGE_REPORT = htmlcov/

# Default target
all: test lint

# Install development dependencies
install-dev:
	$(PIP) install -r requirements-test.txt

# Run all tests
test:
	$(PYTHON) -m pytest tests/ -v

# Run unit tests
test-unit:
	$(PYTHON) -m pytest tests/unit/ -v

# Run integration tests
test-integration:
	$(PYTHON) -m pytest tests/integration/ -v

# Run regression tests
test-regression:
	$(PYTHON) -m pytest tests/regression/ -v

# Run tests with coverage
coverage:
	$(PYTHON) -m pytest --cov=sagemath_pandoc_filter --cov-report=term --cov-report=html tests/
	@echo "Coverage report generated in $(COVERAGE_REPORT)index.html"

# Run linters
lint:
	flake8 sagemath_pandoc_filter/
	black --check sagemath_pandoc_filter/ tests/
	mypy sagemath_pandoc_filter/

# Format code
format:
	black sagemath_pandoc_filter/ tests/
	isort sagemath_pandoc_filter/ tests/

# Clean up
clean:
	rm -rf $(COVERAGE_FILE) $(COVERAGE_REPORT) .pytest_cache/ .mypy_cache/ __pycache__/ */__pycache__/ */*/__pycache__/
