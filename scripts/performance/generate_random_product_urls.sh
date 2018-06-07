#!/bin/bash
for ((i=0;i<=$1;i++))
do
	rot1=$(( ($RANDOM % 720)- 360 ))
	rot2=$(( ($RANDOM % 720)- 360 ))
	rot3=$(( ($RANDOM % 720)- 360 ))
	height=$(( ($RANDOM % 200) - 100))

	echo "http://zgarza.tinyprints.com:8085/web2print/gl/product/55726/personalization/53ebe8c8a17aca0965d3e8a1/x/$rot1/y/$rot2/z/$rot3/viewheight/$height/triangle.png" >> urls.txt
done

