#!/usr/bin/env bash
IFS=$(echo -en "\n\b")
FONT=( 'size=10' 'font=UbuntuMono' )

# Recently Opened
declare -A BOOKS
while read THISBOOK; do
  NEWNAME=$(basename $THISBOOK .pdf)
  NEWCMD="${THISBOOK}"
  BOOKS[$NEWNAME]=$NEWCMD
done < <(find /home/dzack/Dropbox/Library /home/dzack/Zotero/storage /home/dzack/Downloads -type f -iname "*.pdf" -printf '%TY-%Tm-%Td %TT#%p\n' | grep -v Moon | cut -d "#" -f 2) 

choice=$(printf "%s\n" "${!BOOKS[@]}" | dmenu -i -l 20)
[ -z "$choice" ] || nohup okular "${BOOKS[$choice]}" & disown
