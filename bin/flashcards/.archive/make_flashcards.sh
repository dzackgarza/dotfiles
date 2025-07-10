#!/bin/bash

copy_images=false

# Parse the argument using getopts
# The "f" option expects a value of "true" or "false"
while getopts ":f:" opt; do
  case $opt in
    f) copy_images=$OPTARG;;
    \?) echo "Invalid option: -$OPTARG" >&2; exit 1;;
    :) echo "Option -$OPTARG requires an argument." >&2; exit 1;;
  esac
done

sudo updatedb;

# Set up an empty array to store the file names
files=()

echo "Finding files"
while IFS= read -r -d '' file; do
  myArr+=("$line")
  if grep -q "flashcard:" "$file"; then
    echo "$file-- is a flashcard. Adding..."
    files+=("$file")
    echo "********************************"
  else 
    echo "Not a flashcard."
  fi
  # Parse the YAML header metadata
  #yaml=$(cat "$file" | yq --front-matter=extract '.flashcard')

  # Check if the "flashcard" variable is present in the YAML header
  #echo "Checking if markdown file ($file) is a flashcard..."
  #echo "$yaml"
  #if [ "$yaml" = "null" ]; then
    #echo "Not a flashcard."
  #else
    #If the "flashcard" variable is present, add the file name to the array
    #echo "Adding file:"
    #files+=("$file")
    #echo $file
    #echo "********************************"
  #fi
done < <(find . -maxdepth 1 -name '*.md' -print0| sort -z)

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
    apkg_name="$HOME/flashcards/${output_name}.apkg";
    echo "$apkg_name";
    # If the file exists, run the make_flashcards.sh script on it
    lists_to_anki.py "$file" "$apkg_name";
    if $copy_images; then
      echo "Copying images from $file";
      mdimages_to_anki_collection.py "$file";
    else
      echo "Not copying images from $file";
    fi
  else
    # If the file doesn't exist, print a message
    echo "Error: file $file does not exist"
  fi
done
echo "Done."
