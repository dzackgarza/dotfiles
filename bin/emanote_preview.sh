#!/bin/bash

TMP_DIR="/tmp/emma"
BASE_DIR=$(pwd)
IMAGE_DIR=$BASE_DIR

while getopts i: flag; do
  case "${flag}" in
    i) IMAGE_DIR="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

echo "Image directory: $IMAGE_DIR"

clean_to_temp()
{
  awk 'NF {p=1} p' "$@" | emanote_stripmacro.sh  | sed 's/\:\:\:\s*\(.*\)/\n:::\1\n/g' > /tmp/temp.md;
  #awk 'FNR==1{print ""}1' "$f" | sed '/\\envlist/d' | emanote_stripmacro.sh |sed '/file:\/\//d' | sed '/^$/d' > /tmp/temp.md && cp /tmp/temp.md "$destname" && echo "Copied pandoc page: $destname";
}

update_images()
{
  cp /home/zack/notes_site/tikzcd "$TMP_DIR"/tikzcd -r;
  find "$IMAGE_DIR"/ -type f -iname "*.png" -exec cp {} "$TMP_DIR"/figures/ \;
}

#rm  "$TMP_DIR"/attachments -rf;
rm -rf "$TMP_DIR";
mkdir -p "$TMP_DIR"/figures;
cp /home/zack/notes_site_skel/* "$TMP_DIR" -r;
ln -s /home/zack/quals/attachments "$TMP_DIR"/attachments;
cp "$BASE_DIR"/* "$TMP_DIR" -r;
find "$TMP_DIR" -type f \( -iname 'data.yaml' \) -exec rm {} \;
update_images

while read THISFILE; do
  echo "Stripping macros and cleaning: $THISFILE";
  clean_to_temp "$THISFILE"
  cp /tmp/temp.md "$THISFILE"; 
done < <(find "$TMP_DIR" -type f -iname "*.md" | grep -v "index.md") 

#HOST=0.0.0.0 PORT=8000 emanote &
rm -rf /var/www/notes_temp -rf;
mkdir /var/www/notes_temp;
emanote -L "$TMP_DIR" gen /var/www/notes_temp;
qutebrowser "http://localhost:5000/-/all.html" > /dev/null 2>&1 &
echo "Hosted on http://localhost:5000/";
inotifywait --exclude '/\..+' -m -r --format '%w%f' -e CLOSE_WRITE "$BASE_DIR" | while read f
do
  bf=$(basename "$f")
  relname=$(echo $f | grep -oP "^$BASE_DIR\K.*")
  destname="$TMP_DIR$relname"
  echo "Moving | $f | to | $destname |"

  if [[ $f == *.png ]]; then
    cp "$f" "$destname" && echo "Copied image."
    continue;
  fi
  if [[ $f == index* ]]; then
    cp "$f" "$destname" && echo "Copied image."
    emanote -L "$TMP_DIR" gen /var/www/notes_temp;
    continue;
  fi
  if [[ $f == *.md ]]; then
    outdir=$(dirname "$destname")
    mkdir --parent "$outdir";
    clean_to_temp "$f";
    cp /tmp/temp.md "$destname" && echo "Updated wiki file: $destname";
    emanote -L "$TMP_DIR" gen /var/www/notes_temp;
    update_images
    echo "Regenerated emma site."
    qutebrowser ':reload';
    continue;
  fi
done
