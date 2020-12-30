#!/bin/bash

INPUT_PDF=$1
BLANK_PDF="/home/zack/dotfiles/blank.pdf"
NUMPAGES=$(pdftk "${INPUT_PDF}" dump_data 2>/dev/null | grep NumberOfPages  | sed 's/[^0-9]*//')
echo "Counted pages."
PAGES=$(python -c "print(' B1-1 '.join(['A%d-%d'%(x,x) for x in range(1,${NUMPAGES}+1)]))")
echo "Running Python"

pdftk A="${INPUT_PDF}" B="${BLANK_PDF}" cat ${PAGES} output "blanked_${INPUT_PDF}"
