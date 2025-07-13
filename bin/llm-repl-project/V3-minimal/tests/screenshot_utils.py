#!/usr/bin/env python3
"""
Common screenshot utilities for tests to ensure PNG output
"""

from pathlib import Path
from datetime import datetime

try:
    from cairosvg import svg2png
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False
    print("⚠️  cairosvg not available - PNG screenshots will not be generated")


async def save_screenshot(pilot, title: str, filename: str, screenshot_dir: Path = None) -> Path:
    """
    Take a screenshot and save it as PNG (with SVG fallback).
    
    Args:
        pilot: The test pilot instance
        title: Title for the screenshot
        filename: Base filename without extension (e.g., "test_01_initial")
        screenshot_dir: Directory to save screenshots (default: current dir)
        
    Returns:
        Path to the saved file (PNG if conversion successful, otherwise SVG)
    """
    if screenshot_dir is None:
        screenshot_dir = Path(".")

    # Ensure directory exists
    screenshot_dir.mkdir(exist_ok=True)

    # Export screenshot as SVG
    svg_content = pilot.app.export_screenshot(title=title)

    # Try to save as PNG first
    if HAS_CAIROSVG:
        try:
            png_data = svg2png(bytestring=svg_content.encode('utf-8'))
            png_path = screenshot_dir / f"{filename}.png"
            png_path.write_bytes(png_data)
            print(f"📸 Screenshot saved: {png_path}")
            return png_path
        except Exception as e:
            print(f"⚠️  PNG conversion failed: {e}")

    # Fallback to SVG
    svg_path = screenshot_dir / f"{filename}.svg"
    svg_path.write_text(svg_content)
    print(f"📸 Screenshot saved: {svg_path} (PNG conversion unavailable)")
    return svg_path


async def take_timestamped_screenshot(pilot, step_name: str, title: str = None,
                                    screenshot_dir: Path = None, prefix: str = "screenshot") -> Path:
    """
    Take a screenshot with timestamp in filename.
    
    Args:
        pilot: The test pilot instance
        step_name: Name of the step (e.g., "01_initial", "02_typed")
        title: Optional title for the screenshot (defaults to step_name)
        screenshot_dir: Directory to save screenshots
        prefix: Filename prefix
        
    Returns:
        Path to the saved file
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}_{step_name}"

    if title is None:
        title = step_name.replace("_", " ").title()

    return await save_screenshot(pilot, title, filename, screenshot_dir)
