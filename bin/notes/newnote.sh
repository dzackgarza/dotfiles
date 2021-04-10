#!/bin/bash

now=$(date +%H:%M)
today=$(date +%Y-%m-%d)
outfile="$NOTES/Obsidian/Quick_Notes/$today.md"

[[ ! -f $outfile ]] && echo "# $today" > $outfile

nvim -c "norm Go" \
  -c "norm Go## $now" \
  -c "norm G2o" \
  -c "norm zz" \
  -c "startinsert" $outfile
