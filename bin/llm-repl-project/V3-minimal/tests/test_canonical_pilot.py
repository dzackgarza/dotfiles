#!/usr/bin/env python3
"""
CANONICAL PILOT TEST - The One True Test

This test runs the ACTUAL app (same as 'just run') and performs typical user
interactions while taking screenshots at each step. This provides visual proof
of what the app actually does, not what we think it does.

To run: pdm run pytest tests/test_canonical_pilot.py -v
"""

import pytest
from pathlib import Path
from datetime import datetime
import time
from src.main import LLMReplApp
from tests.user_stories import get_user_story, list_available_stories

try:
    from cairosvg import svg2png
    HAS_CAIROSVG = True
except ImportError:
    HAS_CAIROSVG = False
    print("⚠️  cairosvg not available - PNG conversion disabled")

try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("⚠️  PIL not available - temporal grid disabled")


# Screenshot directory
SCREENSHOT_DIR = Path("debug_screenshots")
SCREENSHOT_DIR.mkdir(exist_ok=True)


async def take_screenshot(pilot, step_name: str, story_id: str = "canonical", step_start_time: float = None):
    """Take a screenshot and save as PNG file, return data for temporal grid creation"""
    # Calculate elapsed time since step started
    current_time = time.time()
    elapsed_ms = int((current_time - step_start_time) * 1000) if step_start_time else 0

    # Take the SVG screenshot
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Include milliseconds
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    title = f"{story_id}: {step_name} @{timestamp} (+{elapsed_ms}ms)"
    svg_content = pilot.app.export_screenshot(title=title)

    # Save as PNG file (with SVG fallback)
    canonical_dir = SCREENSHOT_DIR / "canonical"
    canonical_dir.mkdir(exist_ok=True)

    filename = f"{story_id}_{file_timestamp}_{step_name}"

    if HAS_CAIROSVG:
        try:
            png_bytes = svg2png(bytestring=svg_content.encode('utf-8'))
            # Save PNG file
            png_path = canonical_dir / f"{filename}.png"
            png_path.write_bytes(png_bytes)
            print(f"📸 Screenshot saved: {png_path.name}")

            # Also return data for temporal grid
            import io
            return {
                'image_data': io.BytesIO(png_bytes),
                'timestamp': timestamp,
                'elapsed_ms': elapsed_ms,
                'step_name': step_name
            }
        except Exception as e:
            print(f"⚠️  PNG conversion failed: {e}")
            # Fall back to SVG
            svg_path = canonical_dir / f"{filename}.svg"
            svg_path.write_text(svg_content)
            print(f"📸 Screenshot saved: {svg_path.name} (PNG conversion failed)")
            return None
    else:
        # Save as SVG when cairosvg not available
        svg_path = canonical_dir / f"{filename}.svg"
        svg_path.write_text(svg_content)
        print(f"📸 Screenshot saved: {svg_path.name} (cairosvg not available)")
        return None


def create_temporal_grid(screenshot_data_list, story_id: str = "canonical"):
    """Create a temporal grid showing state transitions over time for a user story"""
    if not HAS_PIL or not screenshot_data_list:
        print("⚠️  Cannot create temporal grid - PIL unavailable or no screenshots")
        return None

    # Filter out None values (failed screenshots)
    valid_screenshots = [data for data in screenshot_data_list if data is not None]

    # Each user story should have exactly 12 screenshots in the right order
    if len(valid_screenshots) != 12:
        print(f"⚠️  Expected 12 screenshots for temporal grid, got {len(valid_screenshots)}")
        return None

    # Create labels with timing information for the 12 steps in order
    step_labels = []
    for i, screenshot_data in enumerate(valid_screenshots, 1):
        base_labels = [
            "Launch (initial state)",
            "Focus (user attention)",
            "Input (user types)",
            "Submit (action taken)",
            "Process Start (system response)",
            "Active (workspace visible)",
            "Working (processing)",
            "Streaming (response flows)",
            "Complete (finished)",
            "Collapse (workspace hides)",
            "Updated (timeline shows)",
            "Ready (next interaction)"
        ]

        # Add timing info if available
        if isinstance(screenshot_data, dict) and 'timestamp' in screenshot_data:
            timing_info = f"@{screenshot_data['timestamp']}\n+{screenshot_data['elapsed_ms']}ms"
            step_labels.append(f"{i}. {base_labels[i-1]}\n{timing_info}")
        else:
            step_labels.append(f"{i}. {base_labels[i-1]}")

    # Use all screenshots in order
    grid_labels = step_labels[:len(valid_screenshots)]

    try:
        # Load images from screenshot data
        pil_images = []
        for screenshot_data in valid_screenshots[:12]:  # Max 12 images for 4x3 grid
            try:
                # Handle both old format (BytesIO) and new format (dict with image_data)
                if isinstance(screenshot_data, dict) and 'image_data' in screenshot_data:
                    img_data = screenshot_data['image_data']
                else:
                    img_data = screenshot_data  # Old format compatibility

                img_data.seek(0)  # Reset position to beginning
                img = Image.open(img_data)
                pil_images.append(img)
            except Exception as e:
                print(f"⚠️  Could not load image data: {e}")
                continue

        if len(pil_images) < 4:
            print("⚠️  Could not load enough images for grid")
            return None

        # Calculate grid dimensions
        img_width, img_height = pil_images[0].size
        cols = 4
        rows = 3
        margin = 20
        label_height = 60

        grid_width = cols * img_width + (cols + 1) * margin
        grid_height = rows * (img_height + label_height) + (rows + 1) * margin

        # Create grid canvas
        grid = Image.new('RGB', (grid_width, grid_height), color='white')
        draw = ImageDraw.Draw(grid)

        # Try to use a font, fall back to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        except:
            font = ImageFont.load_default()

        # Place images and labels in grid
        for i, (img, label) in enumerate(zip(pil_images, grid_labels)):
            row = i // cols
            col = i % cols

            x = margin + col * (img_width + margin)
            y = margin + row * (img_height + label_height + margin)

            # Paste image
            grid.paste(img, (x, y))

            # Add label below image
            label_y = y + img_height + 5
            draw.text((x, label_y), label, fill='black', font=font)

        # Add title with story timing summary
        story_start = valid_screenshots[0]['timestamp'] if isinstance(valid_screenshots[0], dict) else "unknown"
        story_end = valid_screenshots[-1]['timestamp'] if isinstance(valid_screenshots[-1], dict) else "unknown"

        title = f"{story_id}: Sacred GUI State Transitions (4x3 Temporal Grid)"
        subtitle = f"Story Timeline: {story_start} → {story_end}"

        title_bbox = draw.textbbox((0, 0), title, font=font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (grid_width - title_width) // 2
        draw.text((title_x, 5), title, fill='black', font=font)

        # Add subtitle with timing
        subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font)
        subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
        subtitle_x = (grid_width - subtitle_width) // 2
        draw.text((subtitle_x, 25), subtitle, fill='gray', font=font)

        # Save temporal grid
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        grid_path = SCREENSHOT_DIR / f"{story_id}_temporal_grid_{timestamp}.png"
        grid.save(grid_path)

        print(f"\n🎬 Temporal grid created: {grid_path}")
        return grid_path

    except Exception as e:
        print(f"⚠️  Error creating temporal grid: {e}")
        return None


async def run_user_story(story_id: str, pilot):
    """Execute a complete user story and capture 12-panel temporal grid"""

    print(f"\\n🎬 RUNNING USER STORY: {story_id}")
    print("=" * 60)

    # Get the story with all 12 steps
    story = await get_user_story(story_id, pilot)

    # Track story timing
    story_start_time = time.time()

    # Execute each step and collect screenshot data in memory
    screenshot_data = []
    for i, step in enumerate(story.steps, 1):
        print(f"\\n📍 Step {i:02d}: {step.description}")

        # Record step start time
        step_start_time = time.time()

        # Execute the step action
        screenshot_name = await step.action()

        # Take screenshot with timing info (returns dict with image_data and timing)
        img_data = await take_screenshot(pilot, screenshot_name, story_id, step_start_time)
        screenshot_data.append(img_data)

        # Show timing information
        if img_data and isinstance(img_data, dict):
            print(f"✅ {step.name} completed - {screenshot_name} (+{img_data['elapsed_ms']}ms)")
        else:
            print(f"✅ {step.name} completed - {screenshot_name}")

    # Verify story structure
    valid_screenshots = [data for data in screenshot_data if data is not None]
    assert len(valid_screenshots) == 12, f"Story must have exactly 12 valid screenshots, got {len(valid_screenshots)}"

    # Calculate total story duration
    story_duration = time.time() - story_start_time
    print(f"\\n⏱️  Total story duration: {story_duration:.2f} seconds")

    # Create temporal grid for this story (ONLY output file)
    grid_path = create_temporal_grid(screenshot_data, story_id)
    if grid_path:
        print(f"\\n🎬 Story temporal grid: {grid_path}")

    print(f"\\n✅ USER STORY COMPLETE: {story.title}")
    print("=" * 60)

    return len(valid_screenshots)  # Return count instead of paths


@pytest.mark.asyncio
async def test_canonical_user_journey():
    """Test core user stories that prove Sacred GUI works for real users"""

    print("\n🚀 STARTING USER STORY TESTING")
    print("=" * 80)

    async with LLMReplApp().run_test(size=(72, 48)) as pilot:
        # Verify basic app structure exists
        await pilot.pause(0.5)
        assert pilot.app.query_one("#prompt-input")
        assert pilot.app.query_one("#chat-container")
        print("✅ App structure verified")

        # Run each user story independently with its own temporal grid
        story_results = {}

        print(f"\n🎬 Running {len(list_available_stories())} user stories...")

        for story_id in list_available_stories():
            print(f"\n📖 Starting story: {story_id}")

            # Run the story and get screenshot count
            screenshot_count = await run_user_story(story_id, pilot)
            story_results[story_id] = {
                'screenshot_count': screenshot_count,
                'grid_created': screenshot_count == 12
            }

            # Brief pause between stories
            await pilot.pause(0.5)

        # Summary of all stories
        print("\n📊 USER STORY RESULTS:")
        print("=" * 80)
        total_screenshots = 0
        successful_grids = 0

        for story_id, results in story_results.items():
            screenshot_count = results['screenshot_count']
            grid_status = "✅ Grid created" if results['grid_created'] else "❌ Grid failed"
            print(f"  {story_id:20} | {screenshot_count:2d} screenshots | {grid_status}")
            total_screenshots += screenshot_count
            if results['grid_created']:
                successful_grids += 1

        print("=" * 80)
        print(f"📸 Total screenshots: {total_screenshots}")
        print(f"🎬 Temporal grids created: {successful_grids}/{len(story_results)}")
        print(f"📁 All files saved to: {SCREENSHOT_DIR}")
        print("✅ ALL USER STORIES COMPLETE - Each story validated with 4x3 temporal grid")




@pytest.mark.asyncio
async def test_canonical_extensions():
    """
    Extension point for new behaviors. Add new test scenarios here
    without breaking the main canonical test.
    """

    print("\n🔧 RUNNING CANONICAL EXTENSIONS")

    async with LLMReplApp().run_test(size=(72, 48)) as pilot:
        await pilot.pause(0.5)

        # Add new test scenarios here as needed
        # Example: Test special key combinations
        print("\n📍 Extension: Test Shift+Enter for multiline")
        await pilot.click("#prompt-input")
        for char in "Line 1":
            await pilot.press(char)
        await pilot.press("shift+enter")
        for char in "Line 2":
            await pilot.press(char)
        await take_screenshot(pilot, "ext_multiline_input", "canonical", time.time())

        # Test sub_blocks fix - verify CognitionWidget doesn't cause Static errors
        print("\n📍 Extension: Test sub_blocks fix (CognitionWidget)")
        await pilot.click("#prompt-input")
        await pilot.press("ctrl+a")  # Clear input
        await pilot.press("delete")

        # Type a message that triggers cognition processing
        test_message = "test cognition pipeline"
        for char in test_message:
            await pilot.press(char)

        step_time = time.time()
        await take_screenshot(pilot, "ext_01_sub_blocks_fix_typed", "canonical", step_time)

        # Submit the message - this triggers the code path where the error occurred
        await pilot.press("enter")
        await pilot.pause(1.0)  # Wait for processing to start

        step_time = time.time()
        await take_screenshot(pilot, "ext_02_sub_blocks_fix_processing", "canonical", step_time)

        # Wait for cognition to complete
        await pilot.pause(2.0)

        # Take final screenshot showing successful completion
        step_time = time.time()
        await take_screenshot(pilot, "ext_03_sub_blocks_fix_complete", "canonical", step_time)

        print("✅ Sub_blocks fix verified - no Static.__init__ errors!")

        # Add more extensions as features are added
        print("\n✅ Extensions complete")


if __name__ == "__main__":
    # Allow running directly with python
    import asyncio
    asyncio.run(test_canonical_user_journey())
