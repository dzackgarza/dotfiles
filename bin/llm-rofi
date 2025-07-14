#!/bin/bash

# Extract only the first line of each chunk for the menu
awk 'BEGIN{RS=""; FS="\n"} {print $1}' my_chunks.txt | \
rofi -dmenu -p "Select:" | \
while read -r summary; do
    # Find and show the full chunk in less
    awk -v s="$summary" 'BEGIN{RS=""; FS="\n"} $1==s {print $0}' my_chunks.txt | less
done
