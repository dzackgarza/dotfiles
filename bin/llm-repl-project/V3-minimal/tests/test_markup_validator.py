"""
Tests for markup validation utility.

These tests ensure that the markup validator correctly identifies
problematic markup patterns and prevents runtime errors.
"""

import pytest
import tempfile
import os
from src.markup_validator import (
    validate_markup,
    MarkupValidationError,
    find_markup_in_file,
    validate_all_markup_in_file,
    validate_project_markup,
)


class TestMarkupValidation:
    """Test cases for markup validation."""

    def test_valid_markup_passes(self):
        """Test that valid markup passes validation."""
        valid_markups = [
            "[white]text[/white]",
            "[bold]text[/bold]",
            "[red]text[/red]",
            "[white]text[/] normal text",
            "normal text [green]green[/green] more text",
            "[bold][red]nested[/red][/bold]",
        ]

        for markup in valid_markups:
            validate_markup(markup)  # Should not raise

    def test_problematic_bracket_escaping_fails(self):
        """Test that problematic bracket escaping pattern fails validation."""
        # This is the exact pattern that caused the runtime error
        problematic_markups = [
            "[[white]⏎[/]] Send",
            "[[white]⇧⏎[/]] New line",
            "[[white]enter[/]] Save",
            "[[white]esc[/]] Cancel",
            "[[red]error[/]] message",
        ]

        for markup in problematic_markups:
            with pytest.raises(MarkupValidationError) as exc_info:
                validate_markup(markup)
            assert "mixes bracket escaping with auto-closing" in str(exc_info.value)

    def test_correct_bracket_escaping_passes(self):
        """Test that correct bracket escaping patterns pass validation."""
        correct_markups = [
            "[white]⏎[/] Send",  # Auto-closing syntax
            "[white]⇧⏎[/] New line",
            "[white]enter[/] Save",
            "[white]esc[/] Cancel",
        ]

        for markup in correct_markups:
            validate_markup(markup)  # Should not raise

    def test_find_markup_in_file(self):
        """Test finding markup strings in Python files."""
        test_file_content = """
def test_function():
    widget.border_subtitle = "[white]test[/white]"
    another_string = "no markup here"
    problematic = "[[white]bad[/]] markup"
    return "[green]success[/green]"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_file_content)
            f.flush()

            try:
                markup_strings = find_markup_in_file(f.name)

                # Should find the markup strings
                assert len(markup_strings) >= 2

                # Check that we found some markup
                found_markup = [markup for line_num, markup in markup_strings]
                assert any("[white]" in markup for markup in found_markup)
                assert any("[green]" in markup for markup in found_markup)

            finally:
                os.unlink(f.name)

    def test_validate_all_markup_in_file(self):
        """Test validation of all markup in a file."""
        test_file_content = """
def test_function():
    # This should pass
    widget.border_subtitle = "[white]good[/white]"

    # This should fail
    widget.border_subtitle = "[[white]bad[/]] markup"

    # No markup
    normal_string = "just text"
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(test_file_content)
            f.flush()

            try:
                errors = validate_all_markup_in_file(f.name)

                # Should find one error
                assert len(errors) >= 1
                assert "mixes bracket escaping with auto-closing" in errors[0]

            finally:
                os.unlink(f.name)

    def test_real_world_error_cases(self):
        """Test the actual error cases found in the codebase."""
        # These are the exact strings that caused runtime errors
        error_cases = [
            "[[white]⏎[/]] Send • [[white]⇧⏎[/]] New line",
            "[[white]enter[/]] Save  [[white]esc[/]] Cancel",
        ]

        for case in error_cases:
            with pytest.raises(MarkupValidationError):
                validate_markup(case)

    def test_fixed_versions_pass(self):
        """Test that the fixed versions of the error cases pass validation."""
        # Fixed versions of the problematic markup
        fixed_cases = [
            "[white]⏎[/] Send • [white]⇧⏎[/] New line",
            "[white]enter[/] Save  [white]esc[/] Cancel",
        ]

        for case in fixed_cases:
            validate_markup(case)  # Should not raise

    def test_empty_and_plain_text(self):
        """Test that empty strings and plain text pass validation."""
        safe_strings = [
            "",
            "plain text",
            "text with no markup",
            "brackets [] but no markup",
            "[[escaped brackets]] with no markup",
        ]

        for string in safe_strings:
            validate_markup(string)  # Should not raise


class TestMarkupValidatorIntegration:
    """Integration tests for markup validator."""

    def test_validate_project_markup(self):
        """Test validation of an entire project directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test project structure
            test_file1 = os.path.join(temp_dir, "test1.py")
            test_file2 = os.path.join(temp_dir, "test2.py")

            with open(test_file1, "w") as f:
                f.write('widget.title = "[white]good[/white]"')

            with open(test_file2, "w") as f:
                f.write('widget.title = "[[white]bad[/]] markup"')

            errors = validate_project_markup(temp_dir)

            # Should find one error in test2.py
            assert len(errors) >= 1
            assert "test2.py" in errors[0]
            assert "mixes bracket escaping with auto-closing" in errors[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
