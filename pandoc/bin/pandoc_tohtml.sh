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
directory=$(dirname "$filepath")
extension="${filename##*.}"
filename="${filename%.*}"

if [ ! -f "$filepath" ]; then
  echo "Input file not found"
  exit 1;
fi

[[ $vimpreview == true ]] && params+=("--variable=vimpreview")
[[ -z "$TMP_DIR" ]] && TMP_DIR=$(mktemp -d -t ci-XXXXXXXXXX);

BUILD_LOG="$directory/build.log";
echo -e "" > "$BUILD_LOG";
debug_print() {
  echo "$1" >> "$BUILD_LOG";
}

debug_print "Current directory: $TMP_DIR";
debug_print "Temp Directory: $TMP_DIR";

debug_print "Checking for data file";
if [ -f "$directory/data.yaml" ]; then 
  debug_print "Found data.yaml";
  DATA_FILE="$directory/data.yaml"
else 
  debug_print "Data file not found in $directory"
  debug_print "Using default preview data.";
  DATA_FILE="$PANDOC_DIR/custom/preview_data.yaml";
fi
debug_print "Using data file: $DATA_FILE";


debug_print "Checking for bibfile";
try_bibfile="$directory/$filename.bib"
if [ ! -f "$try_bibfile" ]; then
  debug_print "Did not find bibfile: $try_bibfile";
  BIB_FILE="$PANDOC_BIB";
else
  debug_print "Found bibfile: $try_bibfile";
  BIB_FILE="$try_bibfile";
fi

cp "$BIB_FILE" "$TMP_DIR/$filename.bib";
#cp -r "$directory/figures" .;

#SEDSTR="s/\[\[\([-0-9A-Za-zé_\ ]\{1,\}\)\(\]\]\)/[\1](.\/\1.html)/g"
# See https://regex101.com/r/7jmwwx/1

cat "$filepath" | pandoc_stripmacros.sh | sed -E 's/\\\[\\\[([^]]*)\\\]\\\]/[\1](\1.md)/g' > "$TMP_DIR/combined.temp" ;

cat >> "$TMP_DIR/combined.temp" <<- EOM

# Bibliography

::: {#refs}
:::
EOM


cat "$TMP_DIR/combined.temp" | pandoc \
  --quiet \
  --metadata-file="$DATA_FILE" \
  -r markdown+simple_tables+table_captions+yaml_metadata_block+tex_math_single_backslash \
  --to html \
  --toc \
  --mathjax \
  --embed-resources \
  --standalone \
  --number-section \
  --filter=pandoc-crossref \
  --lua-filter=$PANDOC_DIR/filters/tikzcd.lua \
  --lua-filter=$PANDOC_DIR/filters/replace_symbols_html.lua \
  --lua-filter=$PANDOC_DIR/filters/convert_math_delimiters.lua \
  --lua-filter=$PANDOC_DIR/filters/convert_amsthm_envs.lua \
  --template=$PANDOC_TEMPLATES/templates/tufte-html-vis.html  \
  --css=$PANDOC_TEMPLATES/marked/kultiad-serif.css \
  --citeproc \
  --bibliography="$TMP_DIR/$filename.bib" \
  --resource-path="$TMP_DIR:$PANDOC_RESOURCE_PATH" \
  --metadata link-citations=true \
  --csl=$PANDOC_TEMPLATES/csl/inventiones-mathematicae.csl \
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
