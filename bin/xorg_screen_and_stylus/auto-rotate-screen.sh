#!/bin/sh

# Automatically rotate the screen when the device's orientation changes.
# Use 'xrandr' to get the correct display for the first argument (for example, "eDP-1"),
# and 'xinput' to get the correct input element for your touch screen, if applicable
# (for example,  "Wacom HID 486A Finger").
#
# The script depends on the monitor-sensor program from the iio-sensor-proxy package.

DISPLAYNAME="eDP-1"
TOUCHSCREEN="ELAN9004:00 04F3:299E"
STYLUS="ELAN9004:00 04F3:299E stylus"
ERASER="ELAN9004:00 04F3:299E eraser"

monitor-sensor \
	| grep --line-buffered "Accelerometer orientation changed" \
	| grep --line-buffered -o ": .*" \
	| while read -r line; do
		line="${line#??}"
		if [ "$line" = "normal" ]; then
			rotate=normal
			matrix="0 0 0 0 0 0 0 0 0"
		elif [ "$line" = "left-up" ]; then
			rotate=left
			matrix="0 -1 1 1 0 0 0 0 1"
		elif [ "$line" = "right-up" ]; then
			rotate=right
			matrix="0 1 0 -1 0 1 0 0 1"
		elif [ "$line" = "bottom-up" ]; then
			rotate=inverted
			matrix="-1 0 1 0 -1 1 0 0 1"
		else
			echo "Unknown rotation: $line"
			continue
		fi

		xrandr --output "$DISPLAYNAME" --rotate "$rotate" && i3-msg restart
    xinput set-prop "$TOUCHSCREEN" --type=float "Coordinate Transformation Matrix" $matrix
    xinput set-prop "$STYLUS" --type=float "Coordinate Transformation Matrix" $matrix
    xinput set-prop "$ERASER" --type=float "Coordinate Transformation Matrix" $matrix
	done
