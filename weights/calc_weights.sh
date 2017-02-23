#!/bin/bash


export gen="python ../generate_path_files.py -p ../paths.yml -s ../settings.yml -e ../event_list"

events=`$gen list_events`

for e in $events
do
    pypaw-window_weights \
	-p parfile/window_weights.$e.param.yml \
	-f paths/window_weights.$e.path.json \
	-v
done




