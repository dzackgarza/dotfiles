#!/bin/sh
# dmenu-based directory browser
# to run from terminal:
#    source /path/to/dbdb.sh
# or bind it to shortcut:
#   echo bind \'\"\\C-o\":\"source /path/to/dbdb.sh\\n\"\' >> ~/.bashrc

IFS=$(echo -en "\n\b")
FONT=( 'size=10' 'font=UbuntuMono' )

choice="placeholder"

DIRS1=$(find $NOTES/Class_Notes/2020 -mindepth 2 -maxdepth 2 -type d )
DIRS2=$( find $NOTES/Class_Notes/2019 -mindepth 1 -maxdepth 1 -type d)
DIRS3=$( find $NOTES/Class_Notes/2017 -mindepth 1 -maxdepth 1 -type d)
DIRS4=$(  find $NOTES/Class_Notes/2016\ and\ Earlier -mindepth 1 -maxdepth 1 -type d)
choice=`( ( echo -e "$DIRS1$DIRS2$DIRS3$DIRS4" | awk -vRS="\t" -vORS="\n" '1' | sed '/^$/d' ) | dmenu -i )`

[ -z "$choice" ] || nohup termite -d "$choice" & disown
