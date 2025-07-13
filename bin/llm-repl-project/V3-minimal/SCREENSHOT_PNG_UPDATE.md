# Screenshot PNG Update Summary

## Changes Made

1. **Updated test files to save PNG files directly instead of SVG files**
   - Modified `tests/test_canonical_pilot.py` to save PNG files with SVG fallback
   - Updated `test_debug_mode_canonical.py` to prefer PNG output
   - Updated `test_real_debug_mode.py` to save PNG first
   - Modified `test_manual_inscription.py` to convert to PNG
   - Enhanced `test_manual_inscription_visual.py` to save only PNG when possible
   - Added helper function to `test_manual_inscription_user_journey.py`

2. **Created screenshot utility module**
   - Added `tests/screenshot_utils.py` with common screenshot functions
   - Provides consistent PNG-first approach with SVG fallback

3. **Cleaned up existing SVG files**
   - Removed SVG files that had corresponding PNG versions
   - Reduced SVG file count from 277 to minimal set

## Pattern for Screenshot Saving

All test files now follow this pattern:

```python
try:
    from cairosvg import svg2png
    png_data = svg2png(bytestring=svg_content.encode('utf-8'))
    png_path = directory / f"{filename}.png"
    png_path.write_bytes(png_data)
    print(f"📸 Screenshot saved: {png_path.name}")
except Exception as e:
    # Fallback to SVG
    svg_path = directory / f"{filename}.svg"
    svg_path.write_text(svg_content)
    print(f"📸 Screenshot saved: {svg_path.name} (PNG conversion failed)")
```

## Benefits

- PNG files are more widely supported and easier to view
- Smaller git repository size (PNG files compress better)
- Consistent screenshot format across all tests
- Graceful fallback to SVG when cairosvg is not available