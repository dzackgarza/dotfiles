#!/bin/bash

# Check if a value for "markdown_file" was provided as a command line argument
if [ $# -eq 0 ]; then
  # If no value was provided, set the default value for "markdown_file"
  markdown_file="/home/test.md"
else
  # If a value was provided, use it as the value for "markdown_file"
  markdown_file=$1
fi

# Set the directory to which we will copy the matching image file
target_dir="/home/zack/.local/share/Anki2/User\ 1/collection.media/attachments/"

# Extract all links to image files from the markdown file
image_links=$(grep -oE "\(.*.png|.*.jpg|.*.gif\)" "$markdown_file")

# For each image link, extract the base name of the image file
for link in $image_links; do
  # Extract the base name of the image file
  image_file=$(echo $link | grep -oE '[^/]*(jpg|png|gif)')
  # Run the "locate" command to find the image file in the file system
  matching_files=$(locate $image_file)
  # If we found a match, copy the first matching file to the target directory
  if [ ! -z "$matching_files" ]; then
    first_match=$(echo "$matching_files" | head -n 1)
    echo "For $link, copying: $first_match";
    cp "$first_match" "$target_dir"
  fi
done
