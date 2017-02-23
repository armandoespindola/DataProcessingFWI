#!/bin/bash



export PYTHONPATH=.:$PYTHONPATH

export gen="python ../generate_path_files.py -p ../paths.yml -s ../settings.yml -e ../event_list"

events=`$gen list_events`
periods=`$gen list_period_bands`

for e in $events
do
    for p in $periods
    do
	mpiexec -n 2 pypaw-measure_adjoint_asdf \
	    -p ../adjoint/parfile/multitaper.adjoint.$p.config.yml \
	    -f ./paths/measure.$e.$p.path.json \
	    -v
    done
done
