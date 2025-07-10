"""
Markup validation utility to prevent runtime Rich markup errors.

This module provides validation for Rich markup syntax used in Textual applications.
It ensures that all markup strings are syntactically correct before they reach
the rendering phase, preventing runtime MarkupError exceptions.
"""

import re
import os
from typing import List, Tuple
from textual.content import Content


class MarkupValidationError(Exception):
    """Raised when markup validation fails."""

    pass


def validate_markup(markup_string: str) -> None:
    """
    Validate Rich markup syntax for correctness.

    Args:
        markup_string: The markup string to validate

    Raises:
        MarkupValidationError: If markup is invalid
    """
    # Check for the specific problematic pattern: [[tag]text[/]]
    # This pattern mixes bracket escaping with auto-closing syntax
    problematic_pattern = r"\[\[(\w+)\]([^[]*)\[/\]"
    matches = re.findall(problematic_pattern, markup_string)

    if matches:
        raise MarkupValidationError(
            f"Invalid markup: [[{matches[0][0]}]...text...[/]] mixes bracket escaping with auto-closing. "
            f"Use either [white]text[/white] or [[white]]text[[/white]] but not the mixed pattern"
        )

    # Try to parse the markup using Textual's Content.from_markup
    try:
        Content.from_markup(markup_string)
    except Exception as e:
        raise MarkupValidationError(f"Invalid markup syntax: {e}")


def find_markup_in_file(file_path: str) -> List[Tuple[int, str]]:
    """
    Find all markup strings in a Python file.

    Args:
        file_path: Path to the Python file to scan

    Returns:
        List of (line_number, markup_string) tuples
    """
    markup_strings = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Pattern to match strings that contain markup (simplified)
    markup_pattern = r'["\']([^"\']*\[(?:white|red|green|blue|yellow|magenta|cyan|bold|italic|underline|dim|reverse|strike|blink)\][^"\']*)["\']'

    for i, line in enumerate(lines, 1):
        matches = re.findall(markup_pattern, line)
        for match in matches:
            markup_strings.append((i, match))

    return markup_strings


def validate_all_markup_in_file(file_path: str) -> List[str]:
    """
    Validate all markup strings found in a Python file.

    Args:
        file_path: Path to the Python file to validate

    Returns:
        List of validation error messages
    """
    errors = []
    markup_strings = find_markup_in_file(file_path)

    for line_num, markup_string in markup_strings:
        try:
            validate_markup(markup_string)
        except MarkupValidationError as e:
            errors.append(f"{file_path}:{line_num}: {e}")

    return errors


def validate_project_markup(project_root: str) -> List[str]:
    """
    Validate markup in all Python files in the project.

    Args:
        project_root: Root directory of the project

    Returns:
        List of validation error messages
    """

    errors = []

    for root, dirs, files in os.walk(project_root):
        # Skip virtual environment directories
        dirs[:] = [d for d in dirs if d not in ["venv", "__pycache__", ".git"]]

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_errors = validate_all_markup_in_file(file_path)
                errors.extend(file_errors)

    return errors


if __name__ == "__main__":
    # Command line interface for validation
    import sys
    import os

    if len(sys.argv) < 2:
        print("Usage: python markup_validator.py <file_or_directory>")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
        errors = validate_all_markup_in_file(target)
    elif os.path.isdir(target):
        errors = validate_project_markup(target)
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)

    if errors:
        print("Markup validation errors found:")
        for error in errors:
            print(f"  {error}")
        sys.exit(1)
    else:
        print("All markup validation passed!")
