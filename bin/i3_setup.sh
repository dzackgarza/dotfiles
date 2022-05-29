#!/bin/bash

xmodmap -e "clear lock";
xmodmap -e "keycode 9 = Caps_Lock NoSymbol Caps_Lock";
xmodmap -e "keycode 66 = Escape NoSymbol Escape";
xset r rate 280 45;
xinput set-prop "ELAN0511:00 04F3:3041 Touchpad" "libinput Natural Scrolling Enabled" 1;
xinput set-prop "ELAN0511:00 04F3:3041 Touchpad" "libinput Tapping Enabled" 1;

#screenChanges.sh;
nitrogen --restore &
pkill polybar & polybar.sh > /var/log/polybar.log 2>&1
pkill redshift; redshift -x; redshift-gtk &
pkill picom; picom --experimental-backends &
pkill nm-applet & nm-applet &
pkill blueman-applet & blueman-applet &
i3l vstack 0.6
