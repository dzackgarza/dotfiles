#!/bin/bash

export XAUTHORITY=/home/zack/.Xauthority
export DISPLAY=:0

STATUS_HDMI="`xrandr --current | grep HDMI | cut -d \  -f 2`"
STATUS_DVI="`xrandr --current | grep DVI| cut -d \  -f 2`"

if [[ "$STATUS_HDMI" == "disconnected" ]] ; then
  xrandr --output eDP1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP1 --off --output HDMI1 --off --output VIRTUAL1 --off
else
  /home/zack/dotfiles/bin/monitorHomeLayout.sh
fi

xset s noblank
xset s off

stylusfix
polybar.sh > /dev/null 2>&1
