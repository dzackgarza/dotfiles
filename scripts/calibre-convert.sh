#!/bin/bash

find . -name "*.epub" -o -name ".djvu" | while read line; do
  #base=$(basename "$line")
  new=${line%.*}.pdf
  echo $line
  echo $new
  /opt/calibre/ebook-convert "$line" "$new"
done
