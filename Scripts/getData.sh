#!/bin/bash

# Get data from both sources and store in appropriate place

# On mac
# time=$(date -v-1d '+%m_%d_%y')


time=$(date -d "yesterday 13:00" '+%m_%d_%y')
# curl -o ../Majestic/top1m/"${time}.csv" https://downloads.majestic.com/majestic_million.csv 


# On mac
cisco_date=$(date -v-1d '+%Y-%m-%d')

# cisco_date=$(date -d "yesterday 13:00" '+%Y-%m-%d')
curl -o ../Umbrella/top1m/"${time}.zip" http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m-"${cisco_date}".csv.zip
cd ../Umbrella/top1m && unzip "${time}.zip" && mv -f top-1m.csv "${time}.csv" && rm -r -f "${time}.zip"
