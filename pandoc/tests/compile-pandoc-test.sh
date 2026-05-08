#!/usr/bin/env bash
# Compile Pandoc test document
# Sets TEXINPUTS to include lib/ and preambles/

export TEXINPUTS=".:$HOME/.pandoc/styles//:$HOME/.pandoc/lib//:$HOME/.pandoc/preambles//:$HOME/.pandoc/config//:"

pandoc test-pandoc-macros.md \
    -o test-pandoc-macros.pdf \
    --pdf-engine=pdflatex \
    -H test-macros.sty \
    -V documentclass=article \
    -V geometry:margin=1in

echo "Pandoc PDF created: test-pandoc-macros.pdf"
