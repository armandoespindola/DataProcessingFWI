#!/bin/bash

export gen="python ../generate_path_files.py -p ../paths.yml -s ../settings.yml -e ../event_list"

events=`$gen list_events`

for e in $events
do
    pypaw-extract_station_info -f paths/stations.$e.path.json
done
