#!/bin/bash

PREVIEW_BROWSER=zathura

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
echo "(VP) Rendering: $filepath"

if [ ! -f "$filepath" ]; then
  echo "(VP) Input file not found"
  exit 1;
fi

VIEWER_PID="";
clean_up() {
  notify-send "VimPreview" "Caught stop signal." --urgency=critical --expire-time=5000;
  kill -9 $(jobs -p %1) > /dev/null  2>&1;
  #pkill $PREVIEW_BROWSER;
  kill -9 $VIEWER_PID || echo "Couldn't find viewer PID";
	exit
}
trap clean_up SIGHUP SIGINT SIGTERM INT TERM EXIT

TMP_DIR=$(mktemp -d -t ci-XXXXXXXXXX);
echo "(VP) Temp directory: $TMP_DIR";

while true; do
  if [[ $vimpreview == true ]]; then  
    outfile=$(pandoc_totex_orpdf.sh -f "$filepath" -p -t "$TMP_DIR" -v);
  else
    outfile=$(pandoc_totex_orpdf.sh -f "$filepath" -p -t "$TMP_DIR");
  fi
  echo "(VP) PDF converted at: $outfile";
  if [ "$first_run" = true ]; then
    echo "(VP) First run"
    $PREVIEW_BROWSER "$outfile" --page=-1> /dev/null 2>&1 &
    VIEWER_PID=$!;
    first_run="false";
  #else
    #$PREVIEW_BROWSER ':reload';
  fi
  inotifywait -e CLOSE_WRITE -r "$directory" --exclude '.*\.pdf' -qq;
  echo "File change detected."
done
clean_up
