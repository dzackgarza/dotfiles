"""Tests for theme CSS validation - prevents invalid CSS property errors"""

import pytest
from pathlib import Path
import re
from textual.css.parse import parse, DeclarationError


class TestThemeValidation:
    """Test CSS theme files for valid properties using professional tools"""

    def test_css_contains_no_banned_properties(self) -> None:
        """Test CSS contains no properties banned by professional linters"""
        theme_file = Path(__file__).parent.parent / "src" / "theme.tcss"
        assert theme_file.exists(), f"Theme file not found: {theme_file}"

        content = theme_file.read_text()

        # Banned patterns that professional CSS linters would catch
        banned_patterns = {
            r"border-focus\s*:": "Use :focus pseudo-selector instead of border-focus property",
            r"color\s*:\s*inherit\s*;": "Use explicit colors instead of 'inherit' for better compatibility",
            r"@import\s+": "Avoid @import for performance - use bundled CSS instead",
            r"!\s*important": "Avoid !important - indicates poor CSS architecture",
            r"expression\s*\(": "CSS expressions are deprecated and insecure",
        }

        errors = []
        for line_num, line in enumerate(content.split("\n"), 1):
            for pattern, message in banned_patterns.items():
                if re.search(pattern, line, re.IGNORECASE):
                    errors.append(
                        f"Line {line_num}: {message}\n  Found: {line.strip()}"
                    )

        assert not errors, "CSS contains banned patterns:\n" + "\n".join(errors)

    def test_css_parses_without_errors(self) -> None:
        """Test that theme.tcss parses successfully using Textual's CSS parser"""
        theme_file = Path(__file__).parent.parent / "src" / "theme.tcss"
        assert theme_file.exists(), f"Theme file not found: {theme_file}"

        content = theme_file.read_text()

        try:
            # Use Textual's built-in CSS parser
            # CSSLocation is a tuple of (filename, content)
            css_location = (str(theme_file), content)
            parsed_styles = list(parse(scope="", css=content, read_from=css_location))
            assert parsed_styles is not None, "CSS parser returned None"

        except DeclarationError as e:
            pytest.fail(f"CSS parsing failed with DeclarationError: {e}")
        except Exception as e:
            pytest.fail(f"CSS parsing failed: {e}")

    def test_css_properties_are_valid(self) -> None:
        """Test that all CSS properties in theme.tcss are valid Textual properties"""
        # Known valid Textual CSS properties (subset of most common ones)
        valid_properties = {
            "background",
            "color",
            "border",
            "border-title-color",
            "border-title-style",
            "border-subtitle-color",
            "border-left",
            "height",
            "width",
            "min-height",
            "max-height",
            "padding",
            "margin",
            "text-style",
            "scrollbar-background",
            "scrollbar-color",
            "scrollbar-color-hover",
            "scrollbar-color-active",
            "display",  # Added common Textual property
            "visibility",  # Added common Textual property
            "dock",  # Added common Textual property
            "align",  # Added common Textual property
            # Focus states use :focus pseudo-selector, not border-focus
            # "border-focus" is INVALID - should be "border" inside ":focus"
        }

        theme_file = Path(__file__).parent.parent / "src" / "theme.tcss"
        assert theme_file.exists(), f"Theme file not found: {theme_file}"

        content = theme_file.read_text()

        # Extract CSS property names using regex
        # Matches patterns like "property-name: value;"
        property_pattern = r"^\s*([a-z-]+)\s*:"
        properties_found = set()
        invalid_properties = []

        for line_num, line in enumerate(content.split("\n"), 1):
            # Skip comments and selectors
            if line.strip().startswith("/*") or line.strip().startswith("//"):
                continue
            if "{" in line or "}" in line:
                continue

            match = re.match(property_pattern, line)
            if match:
                prop = match.group(1)
                properties_found.add(prop)

                if prop not in valid_properties:
                    invalid_properties.append((line_num, prop, line.strip()))

        # Report all invalid properties with line numbers
        if invalid_properties:
            error_msg = "Invalid CSS properties found:\n"
            for line_num, prop, line in invalid_properties:
                error_msg += f"  Line {line_num}: '{prop}' in '{line}'\n"
            error_msg += f"\nValid properties: {sorted(valid_properties)}"
            pytest.fail(error_msg)

    def test_css_focus_states_use_pseudo_selectors(self) -> None:
        """Test that focus states use :focus pseudo-selector, not border-focus property"""
        theme_file = Path(__file__).parent.parent / "src" / "theme.tcss"
        content = theme_file.read_text()

        # Check for invalid border-focus usage
        invalid_focus_lines = []
        for line_num, line in enumerate(content.split("\n"), 1):
            if "border-focus" in line:
                invalid_focus_lines.append((line_num, line.strip()))

        if invalid_focus_lines:
            error_msg = "Found invalid 'border-focus' property. Use ':focus' pseudo-selector instead:\n"
            for line_num, line in invalid_focus_lines:
                error_msg += f"  Line {line_num}: {line}\n"
            error_msg += "\nCorrect usage:\n"
            error_msg += "  Widget:focus {\n"
            error_msg += "    border: solid #color;\n"
            error_msg += "  }"
            pytest.fail(error_msg)

    def test_css_has_required_components(self) -> None:
        """Test that theme includes styling for all required components"""
        theme_file = Path(__file__).parent.parent / "src" / "theme.tcss"
        content = theme_file.read_text()

        required_selectors = [
            "App",
            "PromptInput",
            "TimelineView",
            ".timeline-block-user",
            ".timeline-block-system",
            ".timeline-block-assistant",
            ".timeline-block-cognition",
        ]

        missing_selectors = []
        for selector in required_selectors:
            if selector not in content:
                missing_selectors.append(selector)

        if missing_selectors:
            pytest.fail(f"Missing required CSS selectors: {missing_selectors}")

    def test_css_textual_framework_compatibility(self) -> None:
        """Test that theme works with Textual framework by loading it in an app"""
        from textual.app import App

        theme_file = Path(__file__).parent.parent / "src" / "theme.tcss"

        class TestApp(App):
            CSS_PATH = theme_file

        try:
            # Try to create an app instance - this will load and validate the CSS
            app = TestApp()
            assert app is not None, "App creation failed"
            # If we get here, the CSS is compatible with Textual

        except Exception as e:
            pytest.fail(f"Theme is not compatible with Textual framework: {e}")
