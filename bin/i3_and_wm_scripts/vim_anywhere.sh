#!/bin/sh
file=$(mktemp)
notify-send "Vim" "Starting terminal: $file" --urgency=critical --expire-time=1000

termite -e "nvim -c 'startinsert | colorscheme afterglow | hi Normal guibg=NONE ctermbg=NONE | hi clear conceal | set filetype=pandoc' $file" &
pid="$!"

# Wait for the window to open and grab its window ID
winid=''
while : ; do
    winid="`wmctrl -lp | awk -vpid=$pid '$3==pid {print $1; exit}'`"
    [[ -z "${winid}" ]] || break
done

# Focus the window we found
wmctrl -ia "${winid}"

# Make it float
i3-msg floating enable > /dev/null;

# Move it to the center for good measure
i3-msg move position center > /dev/null;

# Wait for the application to quit
wait "${pid}";

head -c -1 $file | pandoc --from=markdown --to=markdown -r markdown+tex_math_single_backslash | xdotool type --clearmodifiers --delay 0 --file -
rm $file
