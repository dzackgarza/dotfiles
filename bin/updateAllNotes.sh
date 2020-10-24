#!/bin/bash

NOTES="/home/zack/Notes"

echo "Updating: Algebraic Groups."
cd "$NOTES/Class_Notes/2020/Fall/Algebraic Groups/";
make clean; make reset; make all; make clean; echo "Made successfully." || echo "Issue: Algebraic Groups"


echo "Updating: Algebraic Geometry."
cd "$NOTES/Class_Notes/2020/Fall/Algebraic Geometry/";
make clean; make reset; make all; make clean; echo "Made successfully." || echo "Issue: Algebraic Geometry"

echo "Updating: Algebraic Curves."
cd "$NOTES/Class_Notes/2020/Fall/Algebraic Curves/";
make compile && echo "Made successfully." || echo "Issue: Algebraic Curves"

cd ~/Notes && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com "cd /var/www/Notes && git pull"

