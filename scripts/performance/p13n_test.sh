#!/bin/bash

basetime=$(($(date +%s%N)/1000000))

for ((i=0;i<=$1;i++))
do
	rot1=$RANDOM
	rot2=$RANDOM
	rot3=$RANDOM
	height=$RANDOM

	curl -s http://zgarza.tinyprints.com:8085/web2print/benchmark/personalization/53ebe8c8a17aca0965d3e8a1 > /dev/null
done

endtime=$(($(date +%s%N)/1000000))
average=$(( ($endtime-$basetime) / $1 ))

echo "Average time per call:" $average "ms" > personalization_$1_times.txt
