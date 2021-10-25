#!/bin/bash

now=$(date +%H:%M)
today=$(date +%Y-%m-%d)
outfile="$NOTES/Obsidian/Quick_Notes/$today-quick_note.md"

read -r -d '' file_template << EOM
---
date: $today
tags: [quick_notes]
---

# $today

Tags:
#untagged

Refs:
?

EOM

[[ ! -f "$outfile" ]] && echo "$file_template" > $outfile;
notify-send "New Note" "Opening $outfile" --urgency=critical --expire-time=5000;

nvim -c "norm Go" \
  -c "norm Go## $now" \
  -c "norm G2o" \
  -c "norm zz" \
  -c "startinsert" $outfile;
