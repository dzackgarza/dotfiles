#!/bin/bash

cp ~/.pandoc/custom/default.bib .;
mkdir ./sections/figures;
ln -s ./sections/figures ./figures;
cp ~/.pandoc/custom/latest_data.yaml ./data.yaml;
cp ~/.pandoc/bin/LatestMakefile ./Makefile
cp ~/under_construction.png ./figures/cover.png


nvim data.yaml && nvim Makefile;
echo "Rename default.bib!"
