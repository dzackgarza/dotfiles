#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Supply filename as argument"
  exit 1;
fi

print_usage() {
  printf "Usage: ..."
  printf "-f somefile.md"
}


PREFIX=/home/zack/.pandoc/pandoc-templates
CSL=apsa
BIB=/home/zack/Notes/library.bib
standalone=false

while getopts 'f:s' flag; do
  case "${flag}" in
    f) files="${OPTARG}" ;;
    s) standalone="true";;
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

cat ~/Notes/Latex/latexmacs.tex "$filepath" \
  > combined.temp ;
cat combined.temp | pandoc \
  --from=markdown \
  --to=markdown \
  -r markdown+latex_macros+tex_math_single_backslash \
  --lua-filter=/home/zack/Dropbox/rmcodeblocks.lua \
  --lua-filter /home/zack/dotfiles/bin/warning-div.lua \
  --quiet \
  | sed '/^\\\%/d' > out1.temp ;


cat out1.temp | pandoc \
  -r markdown+simple_tables+table_captions+yaml_metadata_block \
  --to html \
  --mathjax \
  --css=$PREFIX/marked/kultiad-serif.css \
  --filter pandoc-crossref \
  --citeproc \
  --lua-filter /home/zack/Notes/Latex/tikzcd.lua \
  --csl=$PREFIX/csl/$CSL.csl \
  --bibliography=$BIB \
  --toc \
  -V current_date="$$(date +%Y-%m-%d%n)" \
  -o "./$filename.html" \
  --quiet \
  >/dev/null

cat "./$filename.html";
rm combined.temp;
rm out1.temp;
rm "./$filename.html";
