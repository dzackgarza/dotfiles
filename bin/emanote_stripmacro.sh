#!/bin/bash

EMA_DIR="/home/zack/notes_site"

# ./myscript.sh filename or cat filename | myscript.sh
[ $# -ge 1 -a -f "$1" ] && $(realpath "$1") input="$1" || input="-"
#cat $input

TMP_DIR=$(mktemp -d -t pandoc-XXXXXXXXXX);

# Change ![[...]] to \!\[\[...\]\] for pandoc
cat $PANDOC_DIR/custom/latexmacs*.tex "$input" | \
  sed 's/\!\[\[/\\!\[\[/g' | \
  sed '/file:\/\//d' > \
  $TMP_DIR/combined.temp ;

# toc doesn't work with emanote yet.

cat $TMP_DIR/combined.temp | pandoc \
  --quiet \
  -r markdown+simple_tables+table_captions+yaml_metadata_block+tex_math_single_backslash \
  --to=markdown-grid_tables-simple_tables-multiline_tables \
  --lua-filter=$EMA_DIR/tikzcd.lua \
  --lua-filter=$EMA_DIR/convert_thm_env.lua \
  --lua-filter=$EMA_DIR/convert_math_delimiters.lua \
  --wrap=none \
  --standalone \
  --wrap=preserve \
  -o "$TMP_DIR/out.temp"; 

if [ $? -ne 0 ]; then
  notify-send "Pandoc StripMacros" "Error compiling." --urgency=critical --expire-time=5000;
  exit 1;
fi

# Send output file, but strip away any tex comments (lines starting with %)
# Change image links
# Remove escapes for Obsidian-style wikilinks and tags
#cat "$TMP_DIR/out.temp" | sed -E -e '/^\\\%/d' \
  #-e 's/\[(.*)\]\((.*).md\)/\[\[\1 \| \2.html\]\]/g' \
  #-e 's/\!\[\]\((.*)\)/\!\[\[\1\]\]/g' \
  #-e 's/\\\[\\\[/\[\[/g' -e 's/\\\]\\\]/\]\]/g' -e 's/\\\#/\#/g' -e 's/\\\|/|/g';

# Delete comment lines "% asdasdsa"
# Unescape brackets: "\[\[" -> "[["
# Unescape brackets: "\]\[" -> "]]"
# Delete envlist lines "\envlist"
# Remove double brackets in div titles inserted by pandoc, particularly for math: ":::{proof title="$\\GL_n$}" -> ":::{proof title="\GL_n}"
# Unescape hashtags: "Tags: \#pdfs" -> "Tags: #pdfs"
# Unescape underscores in brackets: "[[abcd\_efg.pdf]]" -> "[[abcd_efg.pdf]]"

cat "$TMP_DIR/out.temp" | sed '/^\\\%/d' | sed 's/\\\[\\\[/\[\[/g' | sed 's/\\\]\\\]/\]\]/g' | sed '/^\s*\\envlist/d' | sed -e '/title/ s/\\\\/\\/g' | sed 's/\\\#/\#/g' | sed -e '/\[\[/ s/\\\_/\_/g';


#cat "$TMP_DIR/out.tmp" | \
  #sed 's/\!\\\[\\\[/\!\[[/g' | \
  #sed 's/\\\]\\\]/\]\]/g'
