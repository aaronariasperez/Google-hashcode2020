#!/bin/bash

rm "output/scores.txt"
dir="data/*"

for file in $dir
do
    echo "$file"
    outputfile=${file#*/}
    outputfile=${outputfile%%.*}
    outputfile="output/$outputfile.output"
    python3 hashcode.py $file > $outputfile
done
