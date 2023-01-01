#!/usr/bin/env python

import os
import re
import requests
import sys
import json
import subprocess

# MathPix API credentials
APP_ID = 'dzackgarza_gmail_com_6431f8_2115fb'
APP_KEY = 'fbf29df0be9949b51c8dfdf731da563ddb832652dffc7a5d007848b37ce96728'

# MathPix API endpoint
ENDPOINT = 'https://api.mathpix.com/v3/text'

# Regex pattern for image file paths in Markdown files
IMAGE_PATTERN = r'!\[.*\]\((.+)\)'


def find_file(filename):
    # Run the "locate" command and capture the output
    output = subprocess.run(["locate", filename], capture_output=True).stdout
    
    # The output is a bytes object, so we need to decode it
    output = output.decode()
    
    # Split the output into a list of file paths
    file_paths = output.split('\n')
    
    # Return the first file path
    return file_paths[0]


# Function that converts an image to text using the MathPix OCR API
def image_to_text(image_string):
    # Read the image file
    file_path = find_file(image_string)
    with open(file_path, 'rb') as image_file:
        image = image_file.read()

    # Set the request headers
    headers = {
        'app_id': APP_ID,
        'app_key': APP_KEY
    }

    # Send the request to the MathPix API
    response = requests.post(ENDPOINT,
        files={"file": image },
        data={
        "options_json": json.dumps({
            "math_inline_delimiters": ["$", "$"],
            "math_display_delimiters": ["$$", "$$"],
            "rm_spaces": True
        })
        },
        headers=headers
    )

    # Parse the response
    result = response.json()

    # Return the text output
    return result['text']

# Function that scans a Markdown file for images and inserts the
# resulting text below the image
def scan_and_insert(file_path):
    # Read the Markdown file
    with open(file_path, 'r') as file:
        text = file.read()

    # Search for image file paths in the Markdown file
    images = re.findall(IMAGE_PATTERN, text)

    # Iterate over the images
    for image in images:
        # Convert the image to text
        text_output = image_to_text(image)

        # Insert the text below the image
        text = text.replace(f"({image})", f"({image})\n\n- {text_output}")

    # Write the updated Markdown file
    with open(file_path, 'w') as file:
        file.write(text)

# Get the input file path from the command line
file_path = sys.argv[1]

# Check if the input file exists
if not os.path.exists(file_path):
    print(f'Error: file not found: {file_path}')
    sys.exit(1)

# Scan the input file and insert the text below the images
scan_and_insert(file_path)
