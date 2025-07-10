#cd /home/zack//orals/rawnotes/0_Study\ Guides && make_flashcards.sh -f false;
#cp /home/zack/SparkleShare/github.com/Notes/Class_Notes/2022/Fall/Orals/attachments/*.png "/home/zack/.local/share/Anki2/User 1/collection.media/attachments/";

#cd "/home/zack/SparkleShare/github.com/Notes/Obsidian/Projects/0000 Flashcards" && make_flashcards.sh -f true;
#echo "------------------------------------------------------------------------------------------------------------";
#cd "/home/zack/SparkleShare/github.com/Notes/Obsidian/Annotations" && make_flashcards.sh -f true;
#
anki >/dev/null 2>&1 &

DIR1="/home/dzack/Notes/Obsidian/Flashcards"
cd $DIR1; update_anki_decks.py $DIR1

DIR1="/home/dzack/dissertation/Flashcards"
cd $DIR1; update_anki_decks.py $DIR1
