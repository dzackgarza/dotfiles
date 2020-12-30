#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Supply filename as argument"
  exit 1;
fi

print_usage() {
  printf "Usage: ..."
  printf "-f somefile.md"
}

while getopts 'f:h' flag; do
  case "${flag}" in
    f) files="${OPTARG}" ;;
    h) tohtml="true";;
    *) print_usage
       exit 1 ;;
  esac
done

filepath=$(realpath "$1")
directory=$(dirname "$filepath")
filename=$(basename -- "$filepath")
extension="${filename##*.}"
filename="${filename%.*}"
first_run=true

TMP_DIR=$(mktemp -d -t ci-XXXXXXXXXX)

cat data.md $(FILENAME).md | pandoc \
		--quiet \
		-f markdown \
		-t latex \
		-o $(FILENAME).tex \
		--template=$PANDOC_DIR/custom/pandoc_template.tex \
		-r markdown+fenced_divs+tex_math_single_backslash \
		--biblatex \
		--bibliography=$(PANDOC_BIB) \
		--lua-filter=$PANDOC_DIR/filters/warning-div.lua \
		--lua-filter=$PANDOC_DIR/filters/tikzcd.lua \
		-V current_date="$$(date +%Y-%m-%d%n)" \
		-F pandoc-crossref;
