#!/bin/bash

find ~/Notes/Class_Notes -name "*.md" -exec pandoc {} --quiet -t plain --template /home/zack/Notes/Latex/pandoc_template.tex --lua-filter /home/zack/dotfiles/bin/warning-div.lua -r markdown+fenced_divs+tex_math_single_backslash+emoji --biblatex \; | strings | grep -o -w '\w\{5,25\}' | sort -u > ~/Notes/corpus.add

