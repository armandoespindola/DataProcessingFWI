#!/bin/bash


export PYTHONPATH=.:$PYTHONPATH

export gen="python ../generate_path_files.py -p ../paths.yml -s ../settings.yml -e ../event_list"

events=`$gen list_events`
periods=`$gen list_period_bands`

for e in $events
do
    for p in $periods
    do
	mpiexec -n 2 pypaw-window_selection_asdf \
	    -p ./parfile/window.$p.param.yml \
	    -f ./paths/windows.$e.$p.path.json \
	    -v
    done
done
