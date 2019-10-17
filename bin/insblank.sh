#!/bin/bash

INPUT_PDF=$1
BLANK_PDF="/home/zack/dotfiles/blank.pdf"
NUMPAGES=$(pdftk "${INPUT_PDF}" dump_data 2>/dev/null | grep NumberOfPages  | sed 's/[^0-9]*//')
PAGES=$(python -c "print(' B1-1 '.join(['A%d-%d'%(x,x) for x in range(1,${NUMPAGES}+1)]))")

pdftk A="${INPUT_PDF}" B="${BLANK_PDF}" cat ${PAGES} output "blanked_${INPUT_PDF}"
