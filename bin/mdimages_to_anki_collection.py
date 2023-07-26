#!/usr/bin/python    

import mistune
import sys
import subprocess

from mistune.renderers.markdown import MarkdownRenderer


# Store the file name in a variable
file_name = sys.argv[1]

# Define a custom renderer class that stores the file names of image links
class ImageLinkRenderer(MarkdownRenderer):
    def __init__(self):
        self.image_links = []
        # Add an options attribute to the class
        self.options = {}

    def image(self, src, title, text):
        self.image_links.append(src)
        return ""


# Open the markdown file for reading
with open(file_name, "r") as f:
  # Read the contents of the file into a string
  contents = f.read()

# Create an instance of the custom renderer
renderer = ImageLinkRenderer()

# Create a markdown parser using the custom renderer
parser = mistune.Markdown(renderer=renderer)

# Parse the markdown file and extract the image links
parser.parse(contents)

# Iterate over the list of image links
for link in renderer.image_links:
    if "attachment" in link:
        target_dir="/home/zack/.local/share/Anki2/User 1/collection.media/attachments"
    else:
        target_dir="/home/zack/.local/share/Anki2/User 1/collection.media"
    file_name = link.split("/")[-1]
    # Run the locate command and get the output as a list of lines
    output = subprocess.run(["locate", file_name], capture_output=True).stdout.decode().split("\n")

    # Filter the list to only include files whose directories do not contain "collection" or "trash"
    filtered_output = [line for line in output if "collection" not in line and "trash" not in line and "Trash" not in line]

    # Check if any matches were found
    if len(filtered_output) > 0:
        # Get the first match
        first_match = filtered_output[0]
        print("Copying {} to {}".format(first_match, target_dir))
        # Use the shutil module to copy the file to the /collections directory
        import shutil
        shutil.copy(first_match, target_dir)
    else:
        print("No matches found.")
