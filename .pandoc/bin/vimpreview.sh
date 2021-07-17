#!/bin/bash

PREVIEW_BROWSER=qutebrowser

if [ $# -eq 0 ]; then
  echo "Supply filename as argument"
  exit 1;
fi

print_usage() {
  printf "Usage: ..."
  printf "-f somefile.md"
}

vimpreview="false"

while getopts 'f:v' flag; do
  case "${flag}" in
    f) files="${OPTARG}" ;;
    v) vimpreview="true";;
    *) print_usage
       exit 1 ;;
  esac
done

filepath=$(realpath "$files")
directory=$(dirname "$filepath")
filename=$(basename -- "$filepath")
extension="${filename##*.}"
filename="${filename%.*}"
first_run=true

#echo "(VP): $files"
cd "$directory"
echo "(VP) Rendering: $filepath"

if [ ! -f "$filepath" ]; then
  echo "(VP) Input file not found"
  exit 1;
fi

clean_up() {
  notify-send "VimPreview" "Stopped." --urgency=critical --expire-time=5000;
  kill -9 $(jobs -p %1) > /dev/null  2>&1;
  #pkill $PREVIEW_BROWSER;
	exit
}
trap clean_up SIGHUP SIGINT SIGTERM 

TMP_DIR=$(mktemp -d -t ci-XXXXXXXXXX);
echo "(VP) Current directory: $(pwd)";
echo "(VP) Temp directory: $TMP_DIR";

if [ ! -d "./figures" ]; then
  mkdir ./figures;
fi

ln -s "$(realpath ./figures)" $TMP_DIR/figures

while true; do
  if [[ $vimpreview == true ]]; then  
    outfile=$(pandoc_tohtml.sh -f "$filepath" -p -t "$TMP_DIR" -v);
  else
    outfile=$(pandoc_tohtml.sh -f "$filepath" -p -t "$TMP_DIR");
  fi
  echo "(VP) HTML converted at: $outfile";
  if [ "$first_run" = true ]; then
    echo "(VP) First run"
    $PREVIEW_BROWSER "$outfile" > /dev/null 2>&1 &
    first_run="false";
  else
    $PREVIEW_BROWSER ':reload';
  fi
  inotifywait -e CLOSE_WRITE -r "$directory" --exclude '.*\.pdf' -qq;
  echo "File change detected."
done
clean_up
