#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pillow",
# ]
# ///

"""
TDD Enforcement Hook - Strict Visual Validation

This hook enforces that any "temporal grid" or "visual proof" actually contains
real GUI screenshots, not placeholder text.

It runs after test-story commands and validates that the temporal grids are legitimate.
"""

import argparse
import json
import sys
import os
from pathlib import Path
from PIL import Image
import numpy as np
from utils.common_logger import create_logger

def is_fake_temporal_grid(image_path):
    """
    Detect if a temporal grid is fake by checking for:
    1. Static text patterns like "Task X Sacred GUI Validation"
    2. Identical frames across the grid
    3. Lack of actual GUI elements
    """
    try:
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Check if image is too uniform (fake grids have mostly white background)
        unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[-1]), axis=0))
        if unique_colors < 100:  # Real screenshots have many more colors
            return True, "Image has too few unique colors - likely a placeholder"
        
        # Convert to grayscale for analysis
        gray = img.convert('L')
        gray_array = np.array(gray)
        
        # Check for repeating patterns (fake grids have identical frames)
        height, width = gray_array.shape
        cell_height = height // 3  # 3 rows
        cell_width = width // 4   # 4 columns
        
        # Compare first cell with others
        first_cell = gray_array[:cell_height, :cell_width]
        identical_cells = 0
        
        for row in range(3):
            for col in range(4):
                if row == 0 and col == 0:
                    continue
                    
                y_start = row * cell_height
                x_start = col * cell_width
                cell = gray_array[y_start:y_start+cell_height, x_start:x_start+cell_width]
                
                # Calculate similarity
                if np.array_equal(first_cell, cell):
                    identical_cells += 1
        
        if identical_cells > 8:  # More than 8 identical cells out of 11
            return True, "Grid contains too many identical frames - not showing real interaction"
        
        # Check for presence of text patterns indicating fake grid
        # This would require OCR, so we'll use a simpler heuristic
        # Real GUIs have more variation in pixel values
        std_dev = np.std(gray_array)
        if std_dev < 30:  # Real screenshots have more variation
            return True, "Image lacks visual complexity of a real GUI"
        
        return False, "Grid appears to be legitimate"
        
    except Exception as e:
        return True, f"Failed to analyze image: {str(e)}"

def main():
    logger = create_logger('tdd_enforcement')
    
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--check-grid', help='Path to temporal grid to validate')
        parser.add_argument('--task-id', help='Task ID being validated')
        args = parser.parse_args()
        
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Extract temporal grid path from various possible locations
        grid_path = None
        
        if args.check_grid:
            grid_path = args.check_grid
        elif 'temporal_grid_path' in input_data:
            grid_path = input_data['temporal_grid_path']
        elif 'output' in input_data and 'temporal_grid_path' in input_data.get('output', {}):
            grid_path = input_data['output']['temporal_grid_path']
        
        if grid_path and os.path.exists(grid_path):
            is_fake, reason = is_fake_temporal_grid(grid_path)
            
            if is_fake:
                error_msg = f"""
❌ INVALID TEMPORAL GRID DETECTED ❌

Task: {args.task_id or input_data.get('task_id', 'Unknown')}
Grid: {grid_path}
Reason: {reason}

This temporal grid appears to be a placeholder, not actual GUI validation.
Real temporal grids must show:
- Actual Sacred GUI with Timeline, Workspace, and Input areas
- Progressive interaction states (not identical frames)
- Real visual changes between frames
- Genuine UI elements, not just text

The task cannot be marked as complete with fake validation.
Generate a real user story test with actual GUI interaction.
"""
                print(error_msg, file=sys.stderr)
                logger.log_event({
                    "validation_failed": True,
                    "task_id": args.task_id or input_data.get('task_id'),
                    "grid_path": grid_path,
                    "reason": reason,
                    "is_fake": True
                })
                sys.exit(1)
            else:
                logger.log_event({
                    "validation_passed": True,
                    "task_id": args.task_id or input_data.get('task_id'),
                    "grid_path": grid_path,
                    "is_fake": False
                })
        
        # Pass through the original data
        json.dump(input_data, sys.stdout)
        sys.exit(0)
        
    except Exception as e:
        logger.log_error(f"TDD enforcement error: {str(e)}", {})
        # Don't block on errors, just log them
        json.dump(input_data if 'input_data' in locals() else {}, sys.stdout)
        sys.exit(0)

if __name__ == "__main__":
    main()