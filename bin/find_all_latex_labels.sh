#! /bin/bash

#find . -type f -iname "*.md" -exec sed -n '/\#/p' {} + | cut -d "{" -f2 | cut -d "}" -f1 | awk -F: '{print "\\cref{" $0 "}" }' | sort | uniq

find . -type f -iname "*.md" -exec sed -n 's/.*#\([^}]*\)}$/\1/p' {} + | sort -u | sed 's/.*/\\cref{&}/'

