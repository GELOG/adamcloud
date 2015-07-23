#!/bin/bash

# Inspired by: https://github.com/tothebeat/noaa-gsod-data-munging/

year=$1
# Strip the first line of each of the .op files
for filename in `ls $year/*.op`; do
    tail -n +2 $filename > $filename.header_stripped
    mv $filename.header_stripped $filename
done

# Stack every .op measure file into one for the year
cat $year/*.op > $year.op

rm -rf $year