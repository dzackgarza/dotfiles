#!/usr/bin/env python3
"""Extract all supported CSS properties from Textual framework"""

import inspect
from textual.css.styles import Styles
from textual.css import properties
import textual.css.styles

def get_all_textual_css_properties():
    """Get all CSS properties supported by Textual framework"""
    
    # Get all attributes from the Styles class
    styles_attrs = dir(Styles)
    
    # Filter for CSS properties (exclude private methods and special attributes)
    css_properties = []
    for attr in styles_attrs:
        if not attr.startswith('_') and not callable(getattr(Styles, attr, None)):
            # Check if it's a property descriptor
            prop = getattr(Styles, attr, None)
            if hasattr(prop, '__get__') and hasattr(prop, '__set__'):
                css_properties.append(attr.replace('_', '-'))
    
    # Also check the properties module
    prop_module_attrs = dir(properties)
    for attr in prop_module_attrs:
        if not attr.startswith('_'):
            obj = getattr(properties, attr, None)
            if inspect.isclass(obj) and hasattr(obj, 'css_name'):
                css_name = getattr(obj, 'css_name', None)
                if css_name and css_name not in css_properties:
                    css_properties.append(css_name)
    
    # Manual inspection of known Textual properties based on documentation
    known_properties = [
        'align', 'align-horizontal', 'align-vertical',
        'background', 'background-tint',
        'border', 'border-top', 'border-right', 'border-bottom', 'border-left',
        'border-title-align', 'border-title-background', 'border-title-color', 'border-title-style',
        'border-subtitle-align', 'border-subtitle-background', 'border-subtitle-color', 'border-subtitle-style',
        'box-sizing',
        'color', 'content-align',
        'display', 'dock',
        'grid-columns', 'grid-gutter', 'grid-rows', 'column-span', 'row-span',
        'hatch', 'height',
        'keyline', 'layer', 'layers', 'layout',
        'link-color', 'link-background', 'link-hover-color', 'link-hover-background',
        'margin', 'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
        'max-height', 'max-width', 'min-height', 'min-width',
        'offset', 'opacity', 'outline', 'overflow', 'overflow-x', 'overflow-y',
        'padding', 'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
        'position',
        'scrollbar-background', 'scrollbar-color', 'scrollbar-color-active', 'scrollbar-color-hover',
        'scrollbar-corner-color', 'scrollbar-gutter', 'scrollbar-size',
        'text-align', 'text-opacity', 'text-overflow', 'text-style', 'text-wrap',
        'tint', 'visibility', 'width'
    ]
    
    # Add border size properties that are commonly used
    border_size_properties = [
        'border-size',
        'border-top-size', 'border-right-size', 'border-bottom-size', 'border-left-size'
    ]
    
    # Combine all properties and remove duplicates
    all_properties = list(set(css_properties + known_properties + border_size_properties))
    
    return sorted(all_properties)

def check_property_validity():
    """Check which properties from the theme.tcss are actually valid"""
    from pathlib import Path
    import re
    
    theme_file = Path("src/theme.tcss")
    if not theme_file.exists():
        print("theme.tcss not found")
        return
        
    content = theme_file.read_text()
    
    # Extract properties from CSS
    property_pattern = r"^\s*([a-z-]+)\s*:"
    properties_in_file = set()
    
    for line in content.split("\n"):
        if line.strip().startswith("/*") or "{" in line or "}" in line:
            continue
        match = re.match(property_pattern, line)
        if match:
            properties_in_file.add(match.group(1))
    
    valid_properties = set(get_all_textual_css_properties())
    
    print("=== PROPERTIES IN theme.tcss ===")
    for prop in sorted(properties_in_file):
        status = "✓ VALID" if prop in valid_properties else "✗ INVALID"
        print(f"{prop:25} {status}")
    
    print(f"\n=== SUMMARY ===")
    print(f"Properties in file: {len(properties_in_file)}")
    print(f"Valid properties: {len(properties_in_file & valid_properties)}")
    print(f"Invalid properties: {len(properties_in_file - valid_properties)}")
    
    if properties_in_file - valid_properties:
        print(f"\nInvalid properties found:")
        for prop in sorted(properties_in_file - valid_properties):
            print(f"  - {prop}")

if __name__ == "__main__":
    print("=== ALL TEXTUAL CSS PROPERTIES ===")
    all_props = get_all_textual_css_properties()
    for i, prop in enumerate(all_props, 1):
        print(f"{i:3d}. {prop}")
    
    print(f"\nTotal: {len(all_props)} properties\n")
    
    check_property_validity()