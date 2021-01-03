#!/usr/bin/env bash
IFS=$(echo -en "\n\b")
FONT=( 'size=10' 'font=UbuntuMono' )

echo "Books | iconName=accessories-dictionary-symbolic"

echo "---"
echo "Recently Opened | iconName=document-send-symbolic"
find /home/zack/Dropbox/Library -type f -iname "*.pdf" -printf '%AY-%Am-%Ad %TT#%p\n' | grep -v Moon | sort -nr | head -n 10 | sort -rn | cut -d "#" -f 2 | while read THISBOOK; do
  NEWCMD="okular \"${THISBOOK}\""
  echo "$(basename $THISBOOK .pdf) | refresh=true bash='$NEWCMD' terminal=false"
done

echo "---"
echo "Recently Annotated | iconName=error-correct-symbolic"
find /home/zack/Dropbox/Library -type f -iname "*.pdf" -printf '%TY-%Tm-%Td %TT#%p\n' | grep -v Moon | sort -nr | head -n 10 | cut -d "#" -f 2 | while read THISBOOK; do
  NEWCMD="okular \"${THISBOOK}\""
  echo "$(basename $THISBOOK .pdf) | refresh=true bash='$NEWCMD' terminal=false"
done

echo "---"
