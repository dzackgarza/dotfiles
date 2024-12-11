#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Supply current directory as argument"
  exit 1;
fi

print_usage() {
  printf "Usage: ..."
  printf "-f somefile.md"
}

FIG_DIR=""
OUTNAME=""
FILETYPE="svg"
NOW=$(date +%Y-%m-%d_%H-%M);

while getopts 'd:' flag; do
  case "${flag}" in
    d) FIG_DIR="${OPTARG}" ;;
    *) print_usage
       exit 1 ;;
  esac
done

[ ! -d "$FIG_DIR" ] && (echo "Directory not found." && exit 1;)
#echo "Found figure directory."

SVG_FILES="$(  find "$FIG_DIR/" -type f -name "*.svg" -o -name "*.xoj" | sort -r | sed 's#.*/##' )" 
choice=`( ( echo -e "New_Inkscape\tNew_Xournal\t$SVG_FILES" | awk -vRS="\t" -vORS="\n" '1' ) | dmenu -i)`

choice_base="${choice%.*}"
choice_ext="${choice##*.}"
#echo "choice: _base$choice"
#echo "choice_base: $choice_base"
#echo "choice_ext: $choice_ext"

# Create new Inkscape file
if [ "$choice" == "New_Inkscape" ]; then 
  OUTFILE="$FIG_DIR/$NOW";
  if [ -f "$OUTFILE.svg" ]; then 
    echo "File with current date/time already exists!";
    exit 1;
  fi
  cp "$DOTFILES_ROOT/bin/notes/inkscape_template.svg" "$OUTFILE.svg";
  inkscape "$OUTFILE.svg" > /dev/null 2>&1;
  inkscape -D "$OUTFILE.svg" -o "$OUTFILE.pdf" --export-latex > /dev/null 2>&1;
  FILENAME=$(basename -- "$OUTFILE")
read -r -d '' OUT_STR<< EOM
\begin{tikzpicture}
\fontsize{45pt}{1em} 
\node (node_one) at (0,0) { \import{$FIG_DIR}{$FILENAME.pdf_tex} };
\end{tikzpicture}
EOM
  echo "$OUT_STR";
  exit 0;
# Create new Xournal file
elif [ "$choice" == "New_Xournal" ]; then 
  OUTFILE="$FIG_DIR/$NOW";
  if [ -f "$OUTFILE.xoj" ]; then 
    echo "File with current date/time already exists!";
    exit 1;
  fi
  cp "$DOTFILES_ROOT/bin/notes/xournal_template.xoj" "$OUTFILE.xoj";
  xournal "$OUTFILE.xoj" > /dev/null 2>&1;
  echo "<!-- Xournal file: $OUTFILE.xoj -->";
  exit 0;
# File already exists:
# Existing file is for Inkscape
elif [ "$choice_ext" == "svg" ]; then
  inkscape "$FIG_DIR/$choice" > /dev/null 2>&1;
  inkscape -D "$FIG_DIR/$choice" -o "$FIG_DIR/$choice_base.pdf" --export-latex > /dev/null 2>&1;
  exit 0;
# Existing file is for Xornal
elif [ "$choice_ext" == "xoj" ]; then
  xournal "$FIG_DIR/$choice" > /dev/null 2>&1;
  exit 0;
else
  echo "Error: file extension not recognized: ($OUTFILE)";
  exit 1;
fi


