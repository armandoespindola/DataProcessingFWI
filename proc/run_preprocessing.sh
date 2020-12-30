#!/bin/bash
#SBATCH --job-name=proc
##SBATCH --account=GEO111
#SBATCH --exclusive
#SBATCH --export=ALL
#SBATCH --nodes=1
#SBATCH --time=01:00:00

export gen="python ../generate_path_files.py -p ../paths.yml -s ../settings.yml -e ../event_list"

events=`$gen list_events`
periods=`$gen list_period_bands`

for e in $events
do
    for p in $periods
    do
	sh process.sh $e $p
    done
done
