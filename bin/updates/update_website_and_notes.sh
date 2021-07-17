/home/zack/Notes/Obsidian/Unsorted/Quick_Notes/compile_html_notes.sh && echo "Updated math journal.";

cd ~/Quals; git add -A; git commit -am "Save"; git push origin master; popd

cd ~/Notes && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com "cd /var/www/Notes; git stash; git pull;"
notify-send "Website" "Notes updated." --urgency=critical --expire-time=2000

cd ~/website && git add *; git commit -am "Save"; git push; ssh zack@dzackgarza.com ". ~/.rvm/scripts/rvm && ~/updateWebsite.sh"; popd; 
notify-send "Website" "Website updated." --urgency=critical --expire-time=2000

