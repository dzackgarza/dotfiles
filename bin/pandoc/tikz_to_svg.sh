#!/bin/bash

set -x

if [ $# -eq 0 ]; then
  echo "Supply filename as argument"
  exit 1;
fi

print_usage() {
  printf "Usage: ..."
  printf "-f somefile.md"
}


while getopts 'f:h:' flag; do
  case "${flag}" in
    f) files="${OPTARG}" ;;
    h) FILE_HASH="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

filepath=$(realpath "$files")
directory=$(dirname "$filepath")
filename=$(basename -- "$filepath")
extension="${filename##*.}"
filename="${filename%.*}"

if [ ! -f "$filepath" ]; then
  echo "(Tikz->SVG) Input file not found"
  exit 1;
fi

if [ -z "$FILE_HASH" ]; then
  echo "(Tikz->SVG) File hash not supplied."
  exit 1;
fi


TMP_DIR="/tmp/$FILE_HASH";

mkdir -p "$TMP_DIR";

TMP_TEX_FILE="$TMP_DIR/$FILE_HASH.tex"
TMP_PDF_FILE="$TMP_DIR/$FILE_HASH.pdf"
TMP_SVG_FILE="$TMP_DIR/$FILE_HASH.svg"

cp "$filepath" "$TMP_TEX_FILE";

pdflatex "$TMP_TEX_FILE" --output-directory="$TMP_DIR";

pdf2svg "$TMP_PDF_FILE" "$TMP_SVG_FILE"

OUT_TEXT="<p style=\"text-align:center;\"> <img class=\"tikz\" src=\"$TMP_SVG_FILE\"></p>"

if [ ! -f "$TMP_SVG_FILE" ]; then
  echo "(Tikz->SVG) Error creating SVG"
  echo "Directory: $TMP_DIR";
  exit 1;
fi

echo "$OUT_TEXT"

