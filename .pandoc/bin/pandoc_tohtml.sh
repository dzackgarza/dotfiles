#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Supply filename as argument"
  exit 1;
fi

print_usage() {
  printf "Usage: ..."
  printf "-f somefile.md"
}

vimpreview="false"
pathonly="false"
TMP_DIR=""

while getopts 'f:t:vp' flag; do
  case "${flag}" in
    f) files="${OPTARG}" ;;
    t) TMP_DIR="${OPTARG}" ;;
    v) vimpreview="true";;
    p) pathonly="true";;
    *) print_usage
       exit 1 ;;
  esac
done

filepath=$(realpath "$files")
filename=$(basename -- "$filepath");
extension="${filename##*.}"
filename="${filename%.*}"

if [ ! -f "$filepath" ]; then
  echo "Input file not found"
  exit 1;
fi

[[ $vimpreview == true ]] && params+=("--variable=vimpreview")
[[ -z "$TMP_DIR" ]] && TMP_DIR=$(mktemp -d -t ci-XXXXXXXXXX);

[[ -f "$directory/$filename.bib" ]] && BIB_FILE="$directory/$filename.bib" || BIB_FILE="$PANDOC_BIB";

#echo "$directory/$filename.bib"

cp "$BIB_FILE" "$TMP_DIR/$filename.bib";

cat "$filepath" | pandoc_stripmacros.sh > $TMP_DIR/combined.temp ;

cat >> "$TMP_DIR/combined.temp" <<- EOM

# Bibliography

::: {#refs}
:::
EOM
  
cat $TMP_DIR/combined.temp | pandoc \
  --quiet \
  -r markdown+simple_tables+table_captions+yaml_metadata_block+tex_math_single_backslash \
  --to html \
  --toc \
  --mathjax \
  --self-contained \
  --number-section \
  --filter=pandoc-crossref \
  --lua-filter=$PANDOC_DIR/filters/tikzcd.lua \
  --lua-filter=$PANDOC_DIR/filters/replace_symbols_html.lua \
  --lua-filter=$PANDOC_DIR/filters/convert_math_delimiters.lua \
  --lua-filter=$PANDOC_DIR/filters/convert_amsthm_envs.lua \
  --template=$PANDOC_TEMPLATES/templates/tufte-html-vis.html  \
  --css=$PANDOC_TEMPLATES/marked/kultiad-serif.css \
  --filter=pandoc-citeproc \
  --bibliography="$TMP_DIR/$filename.bib" \
  --csl=$PANDOC_TEMPLATES/csl/apsa.csl \
  -V current_date="$(date +%Y-%m-%d%n)" "${params[@]}" \
  -o $TMP_DIR/out.html;

if [ $? -ne 0 ]; then
  notify-send "Pandoc=>HTML" "Error compiling." --urgency=critical --expire-time=5000;
  exit 1;
fi

if [ "$pathonly" = true ]; then
  echo "$TMP_DIR/out.html";
else
  cat $TMP_DIR/out.html;
fi
