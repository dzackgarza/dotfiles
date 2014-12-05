#!/bin/bash

basetime=$(($(date +%s%N)/1000000))

total=0

for ((i=0;i<$1;i++));
do
	for id in `cat test_pids.txt`;
	do
		add=`curl -s http://zgarza.tinyprints.com:8085/web2print/benchmark/texture/$id`
		echo "PID: " $id ", Textures: " $add
		((total=total+add))
	done
done

finaltime=$(($(date +%s%N)/1000000))
productAverage=$(( ($finaltime-$basetime)/(5*$1) ))
textureAverage=$(( ($finaltime-$basetime)/($total) ))

echo "Total textures loaded: " $total > ./results/$1_results.txt
echo "Average time to load a product: " $productAverage "ms" >> ./results/$1_results.txt

echo "Average time to load a texture:" $textureAverage "ms" >> ./results/$1_results.txt

