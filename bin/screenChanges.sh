#!/bin/bash

export XAUTHORITY=/home/zack/.Xauthority
export DISPLAY=:0

STATUS="`xrandr --current | grep HDMI1 | cut -d \  -f 2`"

if [[ "$STATUS" == "disconnected" ]] ; then
  xrandr --output eDP1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP1 --off --output HDMI1 --off --output VIRTUAL1 --off
else
  /home/zack/dotfiles/bin/monitorHomeLayout.sh
  #xrandr --output eDP1 --mode 1920x1080 --pos 0x0 --rotate normal --output DP1 --off --output HDMI1 --primary --mode 1920x1080 --pos 0x1080 --rotate normal --output VIRTUAL1 --off
fi

xset s noblank
xset s off

stylusfix
polybar.sh
