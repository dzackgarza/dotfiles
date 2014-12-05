#!/bin/bash

# cyclescript.sh script_to_cycle powers_of_two
for ((i=1;i<$2;i++))
do
	echo $i
	w=`echo 2^$i | bc`
	echo $w
	($1 "$w")
done
