#!/usr/bin/env bash
IFS=$(echo -en "\n\b")
FONT=( 'size=10' 'font=UbuntuMono' )

find /home/zack/Dropbox/Library -type f -iname "*.pdf" -printf '%TY-%Tm-%Td %TT#%p\n' | grep -v Moon | sort -nr | head -n 10 | cut -d "#" -f 2
