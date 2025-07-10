#!/bin/bash

# Check if a file name was provided as an argument
if [ "$#" -ne 1 ]; then
  echo "Error: please provide a file name as an argument."
  exit 1
fi

# Store the file name in a variable
markdown_file="$1"

# Extract all links to image files from the markdown file
image_links=$(grep -oE ".*.png" "$markdown_file")

# For each image link, extract the base name of the image file
for link in "$image_links"; do
  if grep -q "attachment" <<< "$link"; then
    # Set the directory to which we will copy the matching image file
    target_dir="/home/zack/.local/share/Anki2/User 1/collection.media/attachments"
  else
    # Set the directory to which we will copy the matching image file
    target_dir="/home/zack/.local/share/Anki2/User 1/collection.media"
  fi
  echo "Attempting to find and copy: $link -> $target_dir"
  # Extract the base name of the image file
  image_file=$(echo $link | grep -oP '!\[.*\]\(.*\/\K[^)]+')
  # Run the "locate" command to find the image file in the file system
  matching_files=$(locate $image_file | grep -v collection | grep -v Trash)
  # If we found a match, copy the first matching file to the target directory
  if [ ! -z "$matching_files" ]; then
    first_match=$(echo "$matching_files" | head -n 1)
    echo "Matched. For <$link>, copying <$first_match> to <$target_dir>.";
    cp "$first_match" "$target_dir"
  fi
done
