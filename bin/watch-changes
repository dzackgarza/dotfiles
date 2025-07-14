#!/bin/bash
DIR=$(pwd)

inotifywait --exclude '/\..+' -m -r --format '%w%f' -e CLOSE_WRITE "$DIR" | while read f
do
  bf=$(basename "$f")
  echo "$f" 
  echo "$bf"
  destname="$(echo $f | sed 's/\/home\/zack\//\.\//g')"
  echo "Moving |$f| to |$destname|"
  if [[ $bf == index.md ]]; then
    cp "$f" "$destname" && echo "Copied index page."
    cp ./Notes/index.md ./index.md;
    continue;
  fi
  if [[ $f == *.png ]]; then
    echo "Image changed."
    outdir=$(dirname "$destname")
    mkdir --parent "$outdir";
    cp "$f" "$destname" && echo "Copied image."
    continue;
  fi
  if [[ $f == *.md ]]; then
    outdir=$(dirname "$destname")
    mkdir --parent "$outdir";
    awk 'FNR==1{print ""}1' "$f" | ./pandoc_stripmacros.sh > /tmp/temp.md && mv /tmp/temp.md "$destname" && echo "Copied pandoc page";
    #awk 'FNR==1{print ""}1' "$f" | sed '/file:\/\//d' > /tmp/temp.md && mv /tmp/temp.md "$destname" && echo "Copied pandoc page";
    sleep 1 && touch "$destname";
    continue;
  fi
done
