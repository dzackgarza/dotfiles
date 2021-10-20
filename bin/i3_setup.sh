#!/bin/bash

xmodmap -e "clear lock";
 xmodmap -e "keycode 9 = Caps_Lock NoSymbol Caps_Lock";
 xmodmap -e "keycode 66 = Escape NoSymbol Escape";
 xset r rate 280 45;
 xinput set-prop 17 "libinput Natural Scrolling Enabled" 1;
 xinput set-prop 17 "libinput Tapping Enabled" 1;

screenchanges.sh;
nitrogen --restore &
polybar.sh &
pkill redshift; redshift -x; redshift-gtk &
pkill picom; picom --experimental-backends &
nm-applet &
blueman-applet &
