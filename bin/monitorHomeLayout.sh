#!/bin/sh
xrandr --output eDP1 --mode 1920x1080 --pos 1920x0 --rotate normal --output HDMI1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output VIRTUAL1 --off
stylusfix
xset -dpms                                                                                                                                                                                                                     
xset s noblank
xset s off
