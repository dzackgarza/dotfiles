#! /bin/bash

find . -type f -iname "*.md" -exec sed -n '/\\label/p' {} + | cut -d "{" -f2 | cut -d "}" -f1 | awk -F: '{print "\\cref{" $0 "}" }' | sort | uniq
