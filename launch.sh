#!/bin/bash

datafile=$1
counter=$2

outputfile=${datafile#*/}
outputfile=${outputfile%%.*}
outputfile="output/$outputfile.output"

rm "output/scores.txt"

for (( i=1; i<=$counter; i++ ))
do
    python3 hashcode.py $datafile > $outputfile
    echo "Iteration $i finished"
done
