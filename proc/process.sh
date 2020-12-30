#!/bin/bash

if [ -z "$2" ]
  then
    echo "Event name and frequency band are required."
else
    echo "++++++"
    echo "process observed file..."
    mpirun -np 36 pypaw-process_asdf \
    	-p ./parfile/proc_obsd.${2}.param.yml \
    	-f ./paths/proc_obsd.${1}.${2}.path.json \
    	-v

    echo "++++++"
    echo "process synthetic file..."
    mpirun -np 36 pypaw-process_asdf \
    	-p ./parfile/proc_synt.${2}.param.yml \
    	-f ./paths/proc_synt.${1}.${2}.path.json \
    	-v
    echo "++++++"
fi
