#!/bin/bash

# Read the file locations from standard input
while read file; do
  # Check if the file exists
  if [ -f "$file" ]; then
    # If the file exists, run the convert_to_flashcards.sh script on it
    ./convert_to_flashcards.sh "$file"
  else
    # If the file doesn't exist, print a message
    echo "Error: file $file does not exist"
  fi
done < /dev/stdin
