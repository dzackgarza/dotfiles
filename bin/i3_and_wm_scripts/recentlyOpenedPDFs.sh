#!/usr/bin/env bash
IFS=$(echo -en "\n\b")
FONT=( 'size=10' 'font=UbuntuMono' )
find /home/zack/Dropbox/Library -type f -iname "*.pdf" -printf '%AY-%Am-%Ad %TT#%p\n' | grep -v Moon | sort -nr | head -n 10 | sort -rn | cut -d "#" -f 2
