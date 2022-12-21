#!/bin/bash

sudo updatedb;

# Set up an empty array to store the file names
files=()

while IFS= read -r -d '' file; do
    myArr+=("$line")
  # Parse the YAML header metadata
  yaml=$(grep -E '^---$' "$file" -B 1)

  # Check if the "flashcard" variable is present in the YAML header
  if echo "$yaml" | grep -q "flashcard"; then
    # If the "flashcard" variable is present, add the file name to the array
    echo "Adding file:"
    files+=("$file")
    echo $file
    echo $yaml;
    echo "********************************"
  fi
done < <(find . -name '*.md' -print0 | sort -z)

# Iterate over the array of file names
for file in "${files[@]}"; do
  echo "Processing $file"
  # Check if the file exists
  if [ -f "$file" ]; then
    # Extract the file name from the file path
    file_name=$(basename "$file");
    # Remove the ".md" extension from the file name
    output_name="${file_name%.md}";
    # Print the output file name with the ".apkg" extension
    apkg_name="/home/zack/flashcards/${output_name}.apkg";
    echo "$apkg_name";
    # If the file exists, run the make_flashcards.sh script on it
    lists_to_anki.py "$file" "$apkg_name";
    mdimages_to_anki_collection.sh "$file";
  else
    # If the file doesn't exist, print a message
    echo "Error: file $file does not exist"
  fi
done
