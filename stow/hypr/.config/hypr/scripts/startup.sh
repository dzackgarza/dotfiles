#!/bin/bash

scrDir="$HOME/.config/hypr/scripts"
wallpaper="$HOME/.config/hypr/.cache/current_wallpaper.png"

# Transition config
FPS=60
TYPE="any"
DURATION=2
BEZIER=".43,1.19,1,.4"
AWWW_PARAMS="--transition-fps $FPS --transition-type $TYPE --transition-duration $DURATION --transition-bezier $BEZIER"

if [ -f "$wallpaper" ]; then
    "$scrDir/awww-start.sh"
    awww img ${wallpaper} $AWWW_PARAMS
else
    "$scrDir/Wallpaper.sh"
fi

"$scrDir/notification.sh" sys
"$scrDir/wallcache.sh"
"$scrDir/system.sh" run &
hyprctl reload
