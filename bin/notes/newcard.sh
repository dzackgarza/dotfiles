#!/bin/bash

today=$(date +%Y-%m-%d)
outfile="$NOTES/Obsidian/Flashcards/Decks/Unsorted/Unsorted.md"

read -r -d '' NOTE_TEMPLATE_STR <<- EOM
Title
%
Content 
%
unsorted
---
EOM

nvim -c "norm Go" \
  -c "norm Go$NOTE_TEMPLATE_STR" \
  -c "norm G2o" \
  -c "norm zz" \
  -c "startinsert" $outfile
