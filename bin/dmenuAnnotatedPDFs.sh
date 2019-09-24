#!/usr/bin/env bash
IFS=$(echo -en "\n\b")
FONT=( 'size=10' 'font=UbuntuMono' )

# Recently Opened
declare -A BOOKS
while read THISBOOK; do
  NEWNAME=$(basename $THISBOOK .pdf)
  NEWCMD="${THISBOOK}"
  BOOKS[$NEWNAME]=$NEWCMD
done < <(/home/zack/dotfiles/bin/recentlyAnnotatedPDFs.sh) 

choice=$(printf "%s\n" "${!BOOKS[@]}" | dmenu -i)
[ -z "$choice" ] || okular "${BOOKS[$choice]}"
 
