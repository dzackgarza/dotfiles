#!/bin/bash


is_muted=`pacmd list-sources | grep -e '* index:' -A 11 | grep -Po  '(?(?<=muted: )(.*))'`; 
echo "$is_muted"

#while true; do
  #is_muted=`pacmd list-sources | grep -e '* index:' -A 11 | grep -Po  '(?(?<=muted: )(.*))'`; 
  #echo "$is_muted" >> /home/zack/m.log;
  #echo "$is_muted";
  #sleep 1 &
  #wait
#done

