#!/usr/bin/env python3
"""Script to rename the package from sagemath_pandoc_filter to sagemath_pandoc_filter."""

import os
import re
import shutil
from pathlib import Path

# Configuration
OLD_NAME = 'sagemath_pandoc_filter'
NEW_NAME = 'sagemath_pandoc_filter'
ROOT_DIR = Path(__file__).parent.resolve()

# Files to update with new package name
PYTHON_FILES = [
    '**/*.py',
    '**/*.md',
    '**/*.toml',
    '**/*.txt',
    '**/*.in',
    '**/*.yaml',
    '**/*.yml',
    'Makefile',
    'setup.py',
]

# Directories to rename
DIRS_TO_RENAME = [
    'sagemath_pandoc_filter',
    'sagemath_pandoc_filter.egg-info',
]

def update_file_content(file_path):
    """Update the content of a file with the new package name."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace imports and references
        new_content = re.sub(
            r'\b' + re.escape(OLD_NAME) + r'\b',
            NEW_NAME,
            content
        )
        
        # Replace command names
        new_content = re.sub(
            r'\bsage-filter\b',
            'sagemath-pandoc-filter',
            new_content
        )
        
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated: {file_path}")
            
    except (UnicodeDecodeError, PermissionError) as e:
        print(f"Skipping binary file: {file_path} - {e}")

def rename_directories():
    """Rename directories from old name to new name."""
    for dir_pattern in DIRS_TO_RENAME:
        for old_dir in ROOT_DIR.glob(dir_pattern):
            if old_dir.exists() and old_dir.is_dir():
                new_dir = old_dir.parent / old_dir.name.replace(OLD_NAME, NEW_NAME)
                if old_dir != new_dir:
                    print(f"Renaming: {old_dir} -> {new_dir}")
                    shutil.move(str(old_dir), str(new_dir))

def main():
    print(f"Renaming package from {OLD_NAME} to {NEW_NAME}...")
    
    # First rename directories
    rename_directories()
    
    # Then update file contents
    for pattern in PYTHON_FILES:
        for file_path in ROOT_DIR.rglob(pattern):
            # Skip directories and __pycache__
            if file_path.is_file() and '__pycache__' not in str(file_path):
                update_file_content(file_path)
    
    print("\nPackage renaming complete!")
    print("Please run 'pip install -e .' to reinstall the package with the new name.")

if __name__ == '__main__':
    main()
