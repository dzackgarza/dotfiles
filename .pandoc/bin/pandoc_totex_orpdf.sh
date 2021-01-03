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
[[ $toex == false ]] && params+=("--pdf-engine=pdflatex")
[[ $vimpreview == true ]] && params+=("--variable=vimpreview")
[[ -z "$TMP_DIR" ]] && TMP_DIR=$(mktemp -d -t ci-XXXXXXXXXX);
[[ -f "$directory/data.md" ]] && DATA_FILE="$directory/data.md" || DATA_FILE="$PANDOC_DIR/custom/preview_data.md";
[[ -f "$directory/$filename.bib" ]] && BIB_FILE="$directory/$filename.bib" || BIB_FILE="$PANDOC_BIB";

cp "$BIB_FILE" "$TMP_DIR/$filename.bib";

cat "$filepath" | pandoc_stripmacros.sh > $TMP_DIR/combined.temp ;

cat "$DATA_FILE" "$TMP_DIR/combined.temp" | pandoc \
    --quiet \
    -r markdown+fenced_divs+tex_math_single_backslash+citations \
    --template=$PANDOC_DIR/custom/pandoc_template.tex \
		--lua-filter=$PANDOC_DIR/filters/tikzcd.lua \
    --lua-filter=$PANDOC_DIR/filters/convert_amsthm_envs.lua \
    --lua-filter=$PANDOC_DIR/filters/convert_math_delimiters.lua \
		--biblatex \
		--bibliography="$TMP_DIR/$filename.bib" \
    -V current_date="$(date +%Y-%m-%d%n)" "${params[@]}" \
    -o $TMP_DIR/out.$EXT;

if [ $? -ne 0 ]; then
  notify-send "Pandoc=>PDF #1" "Error compiling." --urgency=critical --expire-time=5000;
  exit 1;
fi

#echo "PDF generated successfully: $TMP_DIR/out.pdf"

if [[ "$pathonly" == true ]]; then
  echo "$TMP_DIR/out.$EXT";
else
  cat $TMP_DIR/out.$EXT;
fi
