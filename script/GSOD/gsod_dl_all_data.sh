#!/bin/bash

# Inspired by: https://github.com/tothebeat/noaa-gsod-data-munging/

firstYear=$1
lastYear=$2

for currentYear in `seq $firstYear $lastYear`; do
	echo ===============================
	echo Downloading $currentYear
	echo ===============================
    ./gsod_dl_data_year_XXXX.sh $currentYear
done