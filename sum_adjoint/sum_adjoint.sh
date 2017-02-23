#!/bin/sh

export gen="python ../generate_path_files.py -p ../paths.yml -s ../settings.yml -e ../event_list"

events=`$gen list_events`

for e in $events
do
    pypaw-sum_adjoint_asdf \
	-p parfile/sum_adjoint.param.yml \
	-f paths/adjoint_sum.$e.path.json \
	-v
done



