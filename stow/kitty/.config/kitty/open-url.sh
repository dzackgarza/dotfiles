#!/bin/sh
# kitty open_url_with handler: announce the link, then hand it to the desktop opener.
notify-send --app-name=kitty --icon=web-browser "Opening link" "$1"
exec xdg-open "$1"
