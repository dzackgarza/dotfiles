#!/bin/bash

# ./myscript.sh filename or cat filename | myscript.sh
[ $# -ge 1 -a -f "$1" ] && $(realpath "$1") input="$1" || input="-"
#cat $input

TMP_DIR=$(mktemp -d -t pandoc-XXXXXXXXXX);

cat $PANDOC_DIR/custom/latexmacs*.tex "$input" > $TMP_DIR/combined.temp ;

cat $TMP_DIR/combined.temp | pandoc \
  --quiet \
  -r markdown+latex_macros+tex_math_dollars+tex_math_single_backslash \
  --to=markdown \
  --lua-filter=$PANDOC_DIR/filters/convert_amsthm_envs.lua \
  --lua-filter=$PANDOC_DIR/filters/convert_math_delimiters.lua \
  --resource-path="/home/zack/Notes/Obsidian:/home/zack/Notes" \
  --wrap=none \
  -o "$TMP_DIR/out.temp"; 

if [ $? -ne 0 ]; then
  notify-send "Pandoc StripMacros" "Error compiling." --urgency=critical --expire-time=5000;
  exit 1;
fi

# Send output file, but strip away any tex comments (lines starting with %)
cat "$TMP_DIR/out.temp" | sed '/^\\\%/d'
