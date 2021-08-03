/home/zack/Notes/Obsidian/Unsorted/Quick_Notes/compile_html_notes.sh && echo "Updated math journal.";

pushd ~/dotfiles; git add -A; git commit -am "Save"; git push origin master; popd

pushd ~/Quals; git add -A; git commit -am "Save"; git push origin master; popd

pushd ~/Notes && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com "cd /var/www/Notes; git stash; git pull;"

pushd ~/website && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com ". ~/.rvm/scripts/rvm && ~/updateWebsite.sh"; 

