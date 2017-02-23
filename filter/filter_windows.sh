#!/bin/bash



export gen="python ../generate_path_files.py -p ../paths.yml -s ../settings.yml -e ../event_list"

events=`$gen list_events`
periods=`$gen list_period_bands`

for e in $events
do
    for p in $periods
    do
	pypaw-filter_windows \
	    -p ./parfile/filter_windows.$p.param.yml \
	    -f ./paths/filter.$e.$p.path.json \
	    -v
    done
done