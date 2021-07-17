#!/bin/bash

template_dir="/home/zack/.pandoc/custom/pandoc_template.tex"
filters_dir="/home/zack/.pandoc/filters/convert_amsthm_envs.lua"

find ~/Notes/Class_Notes -name "*.md" -exec pandoc {} --quiet -t plain --template $template_dir --lua-filter $filters_dir -r markdown+fenced_divs+tex_math_single_backslash+emoji --biblatex \; | strings | grep -o -w '\w\{6,25\}' | sort -u > ~/Notes/corpus.add
find ~/Notes/Obsidian -name "*.md" -exec pandoc {} --quiet -t plain --template $template_dir --lua-filter $filters_dir -r markdown+fenced_divs+tex_math_single_backslash+emoji --biblatex \; | strings | grep -o -w '\w\{6,25\}' | sort -u >> ~/Notes/corpus.add

