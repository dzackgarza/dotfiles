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
to_tex="false"
EXT="pdf"

while getopts 'f:t:vpx' flag; do
  case "${flag}" in
    f) files="${OPTARG}" ;;
    t) TMP_DIR="${OPTARG}" ;;
    v) vimpreview="true";;
    p) pathonly="true";;
    x) totex='true' ;;
    *) print_usage
       exit 1 ;;
  esac
done

#echo "Temp dir: $TMP_DIR"

filepath="$(realpath "$files")";
filename="$(basename -- "$filepath")";
directory="$(dirname "$filepath")";
extension="${filename##*.}";
filename="${filename%.*}";

[[ ! -f "$filepath" ]] && echo "Input file not found" && exit 1;

[[ $totex == true ]] && EXT="tex";
[[ $totex == false ]] && params+=("--pdf-engine=pdflatex")
[[ $vimpreview == true ]] && params+=("--variable=vimpreview")
[[ -z "$TMP_DIR" ]] && TMP_DIR=$(mktemp -d -t ci-XXXXXXXXXX);
[[ -f "$directory/data.yaml" ]] && DATA_FILE="$directory/data.yaml" || DATA_FILE="$PANDOC_DIR/custom/preview_data.yaml";

BUILD_LOG="$directory/build.log";
echo -e "" > "$BUILD_LOG";

debug_print() {
  echo "$1" >> "$BUILD_LOG";
}

debug_print "Temp Directory: $TMP_DIR";
debug_print "Checking for bibfile";
try_bibfile="$directory/$filename.bib"
if [ ! -f "$try_bibfile" ]; then
  debug_print "Did not find bibfile: $try_bibfile";
  BIB_FILE="$PANDOC_BIB";
else
  debug_print "Found bibfile: $try_bibfile";
  # Avoid issues with spaces in path.
  cp "$try_bibfile" "$TMP_DIR";
  BIB_FILE="$TMP_DIR/$filename.bib";
fi
debug_print "Using bib: $BIB_FILE";

cp "$filepath" "$TMP_DIR";

cat "$filepath" | pandoc_stripmacros.sh > $TMP_DIR/combined.temp ;

cat "$TMP_DIR/combined.temp" | pandoc \
    --quiet \
    --metadata-file="$DATA_FILE" \
    -r markdown+fenced_divs+tex_math_single_backslash+citations \
    --template=$PANDOC_DIR/custom/pandoc_paper_template.tex \
		--lua-filter=$PANDOC_DIR/filters/tikzcd.lua \
    --lua-filter=$PANDOC_DIR/filters/convert_amsthm_envs.lua \
    --lua-filter=$PANDOC_DIR/filters/convert_math_delimiters.lua \
		--bibliography="$filename.bib" \
		--biblatex \
    -V current_date="$(date +%Y-%m-%d%n)" "${params[@]}" \
    -o "$TMP_DIR/out.$EXT";

if [ $? -ne 0 ]; then
  notify-send "Pandoc=>PDF #1" "Error compiling." --urgency=critical --expire-time=5000;
  exit 1;
fi

debug_print "$EXT generated successfully: $TMP_DIR/out.pdf"

if [[ "$pathonly" == true ]]; then
  echo "$TMP_DIR/out.$EXT";
else
  cat $TMP_DIR/out.$EXT;
fi
