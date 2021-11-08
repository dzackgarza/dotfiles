#!/bin/bash

now_time=$(date "+%Y-%m-%d, %H:%M")
problems_completed=$(ag "#complete" --stats ~/quals | tail -n5 | head -n1 | cut -d" " -f1)
problems_towork=$(ag "#work" --stats ~/quals | tail -n5 | head -n1 | cut -d" " -f1)
outfile=/home/zack/quals/qual_progress.md

read -r -d '' file_template << EOM
\n| $now_time | $problems_completed | $problems_towork | 
EOM

printf "$file_template" >> $outfile;
