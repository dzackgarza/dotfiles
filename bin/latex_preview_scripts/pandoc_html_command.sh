cat $PANDOC_DIR/custom/latexmacs.tex "$filepath" \
  > $TMP_DIR/combined.temp ;

if [ $? -ne 0 ]; then
  notify-send "Pandoc=>HTML #0" "Error compiling." --urgency=critical --expire-time=5000;
  exit 1;
fi

cat $TMP_DIR/combined.temp | pandoc \
  --quiet \
  --from=markdown \
  --to=markdown \
  -r markdown+latex_macros+tex_math_single_backslash \
  --lua-filter=$PANDOC_DIR/filters/rmcodeblocks.lua \
  --lua-filter=$PANDOC_DIR/filters/warning-div.lua \
  -o $TMP_DIR/out1.temp ; 

if [ $? -ne 0 ]; then
  notify-send "Pandoc=>HTML #1" "Error compiling." --urgency=critical --expire-time=5000;
  exit 1;
fi
  
cat $TMP_DIR/out1.temp | sed '/^\\\%/d' | pandoc \
  --quiet \
  -r markdown+simple_tables+table_captions+yaml_metadata_block \
  --to html \
  --mathjax \
  --template=$PANDOC_TEMPLATES/templates/tufte-html-vis.html  \
  --css=$PANDOC_TEMPLATES/marked/kultiad-serif.css \
  --filter=pandoc-crossref \
  --citeproc \
  --lua-filter=$PANDOC_DIR/filters/tikzcd.lua \
  --csl=$PANDOC_TEMPLATES/csl/apsa.csl \
  --bibliography=$PANDOC_BIB \
  --toc \
  -V current_date="$$(date +%Y-%m-%d%n)" "${params[@]}" \
  --self-contained \
  -o $TMP_DIR/out.html;

if [ $? -ne 0 ]; then
  notify-send "Pandoc=>HTML #2" "Error compiling." --urgency=critical --expire-time=5000;
  exit 1;
fi

