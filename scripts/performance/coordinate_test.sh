#!/bin/bash

basetime=$(($(date +%s%N)/1000000))
for ((i=0;i<=$1;i++))
do
	rot1=$RANDOM
	rot2=$RANDOM
	rot3=$RANDOM
	height=$RANDOM

	curl -s http://zgarza.tinyprints.com:8085/web2print/benchmark/debug/coords/x/$rot1/y/$rot2/z/$rot3/viewheight/$height > ./images/x/$i.png 
done

endtime=$(($(date +%s%N)/1000000))
average=$(( ($endtime-$basetime) / $1 ))
echo "Average time per call:" $average "ms" > coordinate_result$1.txt
