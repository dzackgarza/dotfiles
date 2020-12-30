#!/bin/bash

export XAUTHORITY=/home/zack/.Xauthority
export DISPLAY=:0

STATUS_HDMI="`xrandr --current | grep HDMI | cut -d \  -f 2`"
STATUS_DVI="`xrandr --current | grep DVI| cut -d \  -f 2`"

#if [[ "$STATUS_HDMI" == "disconnected" ]] ; then
  #xrandr --output eDP1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP1 --off --output HDMI1 --off --output VIRTUAL1 --off
#else
  #monitorHomeLayout.sh
#fi

fixbluetooth.sh 
nitrogen --restore 
i3-msg reload
i3-msg restart
sleep 1;
xset s noblank
xset s off
xset r rate 280 45 
stylusfix

polybar.sh > /dev/null 2>&1
