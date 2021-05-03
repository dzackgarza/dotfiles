#!/bin/bash

now=$(date +%H:%M)
today=$(date +%Y-%m-%d)
time=$(date +%T)
echo "Note title?"
read temp_title

title=$(echo $temp_title | tr -s ' ' | tr ' ' '_')

outfile="$NOTES/Obsidian/zettelkasten/${today}_${title}.md"
echo "Opening: $outfile"

#[[ ! -f $outfile ]] 

cat >> "$outfile" <<- EOM
---
date: $today $time
tags: 
  - Unfiled
---

EOM

#cd "$NOTES/Obsidian/Quick_Notes" &&
nvim -c "norm Go" \
  -c "startinsert" $outfile;
