# Sage Filter Test Suite

This directory contains the test suite for the Sage Filter package. The tests are organized into several categories:

## Test Organization

- `unit/`: Unit tests for individual components
- `integration/`: Integration tests that test multiple components working together
- `regression/`: Regression tests to prevent reintroduction of fixed bugs
- `data/`: Test data and expected outputs

## Running Tests

### Run All Tests

```bash
make test
```

### Run Specific Test Categories

```bash
# Run only unit tests
make test-unit

# Run only integration tests
make test-integration

# Run only regression tests
make test-regression
```

### Run Tests with Coverage

```bash
make coverage
```

This will generate a coverage report in the `htmlcov/` directory.

## Writing Tests

1. Place unit tests in the `unit/` directory
2. Place integration tests in the `integration/` directory
3. Place regression tests in the `regression/` directory
4. Use the `SageTestBase` class from `base_test.py` for common test functionality

## Test Naming Conventions

- Test files should be named `test_*.py`
- Test classes should be named `Test*` and inherit from `SageTestBase`
- Test methods should be named `test_*` and describe what they're testing

## Best Practices

1. Each test should test one specific piece of functionality
2. Tests should be independent of each other
3. Use descriptive test method names
4. Include docstrings that explain what each test is checking
5. Use the helper methods in `SageTestBase` when possible
6. Add regression tests for any fixed bugs

## Debugging Tests

To run a specific test:

```bash
python -m pytest tests/unit/test_specific.py::TestClass::test_method -v
```

To drop into the debugger on failure:

```bash
python -m pytest tests/ -v --pdb
```

## Continuous Integration

The test suite is designed to be run in a CI/CD pipeline. The `Makefile` provides targets that can be used in CI scripts.
