#!/bin/bash

# Get the time range from the user
firstYear=$1
lastYear=$2

# Download the data schema to later convert to CSV
wget https://raw.githubusercontent.com/tothebeat/noaa-gsod-data-munging/master/gsod_schema.csv -O gsod_data_schema.csv

./gsod_dl_all_data.sh $firstYear $lastYear
./gsod_format_all_data.sh $firstYear $lastYear

# Stack every .op year file into one
cat *.op > gsod_data_"$firstYear"_to_"$lastYear".op

# Convert to CSV
#in2csv -s gsod_data_schema.csv gsod_data_"$firstYear"_to_"$lastYear".op > gsod_data_"$firstYear"_to_"$lastYear".csv