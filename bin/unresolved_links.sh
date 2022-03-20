#!/bin/bash

unresolved_links="/home/zack/Notes/Obsidian/unresolved links output.md";

sed -E '/\.svg|\.png|\.sty|\.asy|\.pdf|\.jpg|\.eps|\.fls|\.JPG|\.pgf|\.zip|\.gif|\.PNG|\.pbsdat/d' -i "$unresolved_links";
mv "$unresolved_links" "$unresolved_links.bak";
cat "$unresolved_links.bak" | awk '{print gsub(",",","), $0}' | sort -nr | cut -d' ' -f2- > "$unresolved_links";
rm "$unresolved_links.bak";

unlinked_files="/home/zack/Notes/Obsidian/unlinked files output.md";
sed -E '/\.svg|\.png|\.sty|\.asy|\.pdf|\.jpg|\.eps|\.fls|\.JPG|\.pgf|\.zip|\.gif|\.PNG|\.pbsdat/d' -i "$unlinked_files";

