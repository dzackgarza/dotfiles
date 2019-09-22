#!/usr/bin/env bash
IFS=$(echo -en "\n\b")
FONT=( 'size=10' 'font=UbuntuMono' )


# Recently Opened
#names=()
#commands=()
declare -A BOOKS
while read THISBOOK; do
  NEWNAME=$(basename $THISBOOK .pdf)
  NEWCMD="${THISBOOK}"
  BOOKS[$NEWNAME]=$NEWCMD
  #names+=($NEWNAME)
  #commands+=($NEWCMD)
done < <(recentlyOpenedPDFs.sh) 


choice=$(printf "%s\n" "${!BOOKS[@]}" | dmenu -i)
[ -z "$choice" ] || okular "${BOOKS[$choice]}"
