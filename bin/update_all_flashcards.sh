cd /home/zack//orals/rawnotes/0_Study\ Guides && make_flashcards.sh -f false;
cp /home/zack/SparkleShare/github.com/Notes/Class_Notes/2022/Fall/Orals/attachments/*.png "/home/zack/.local/share/Anki2/User 1/collection.media/attachments/";

cd "/home/zack/SparkleShare/github.com/Notes/Obsidian/Projects/0000 Flashcards" && make_flashcards.sh -f true;
echo "------------------------------------------------------------------------------------------------------------";
cd "/home/zack/SparkleShare/github.com/Notes/Obsidian/Annotations" && make_flashcards.sh -f true;
