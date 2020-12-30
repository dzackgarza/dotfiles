#!/bin/bash

NOTES="/home/zack/Notes"

echo "Updating: Algebraic Groups."
cd "$NOTES/Class_Notes/2020/Fall/Algebraic Groups/"; make clean; make reset;
if make all; then
  echo "Algebraic Groups: Okay"
  make clean;
  cd ~/Notes && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com "cd /var/www/Notes && git pull"
else
  notify-send "Updating Books" "Issue: Algebraic Groups" --urgency=critical --expire-time=50000
fi  

echo "Updating: Algebraic Geometry."
cd "$NOTES/Class_Notes/2020/Fall/Algebraic Geometry/"; make clean; make reset;
if make all; then
  echo "Algebraic Geometry: Okay"
  make clean;
  cd ~/Notes && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com "cd /var/www/Notes && git pull"
else
  notify-send "Updating Books" "Issue: Algebraic Geometry" --urgency=critical --expire-time=50000
fi  

echo "Updating: Algebraic Curves."
cd "$NOTES/Class_Notes/2020/Fall/Algebraic Curves/"; make clean; make reset;
if make all; then
  echo "Algebraic Curves: Okay"
  make clean;
  cd ~/Notes && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com "cd /var/www/Notes && git pull"
else
  notify-send "Updating Books" "Issue: Algebraic Geometry" --urgency=critical --expire-time=50000
fi  

echo "Updating: Étale Cohomology."
cd "$NOTES/Class_Notes/2020/Fall/Etale Cohomology/"; make clean; make reset;
if make all; then
  echo "Étale Cohomology: Okay"
  make clean;
  cd ~/Notes && git add *; git commit -am "Save"; git push; popd; ssh zack@dzackgarza.com "cd /var/www/Notes && git pull"
else
  notify-send "Updating Books" "Issue: Étale Cohomology" --urgency=critical --expire-time=50000
fi  

