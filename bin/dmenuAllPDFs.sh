#!/usr/bin/env bash
IFS=$(echo -en "\n\b")
FONT=( 'size=10' 'font=UbuntuMono' )

# Recently Opened
declare -A BOOKS
while read THISBOOK; do
  NEWNAME=$(basename $THISBOOK .pdf)
  NEWCMD="${THISBOOK}"
  BOOKS[$NEWNAME]=$NEWCMD
done < <(find /home/zack/Dropbox/Library /home/zack/Downloads -type f -iname "*.pdf" -printf '%TY-%Tm-%Td %TT#%p\n' | grep -v Moon | cut -d "#" -f 2) 

choice=$(printf "%s\n" "${!BOOKS[@]}" | dmenu -i)
[ -z "$choice" ] || okular "${BOOKS[$choice]}"
