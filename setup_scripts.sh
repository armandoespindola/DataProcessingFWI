#!/bin/bash

if [ $# -lt 3 ]; then
    echo "This program sets up sbatch scripts for workflow"
    echo "usage: ./setup_scripts.sh account nproc narray verbose[false==0/true==1]"; exit 1;
fi

account=$1
nproc=$2
narray=$3
verbose=$4


if [ -z "$verbose" ]; then
    verbose=0
fi


if [ $verbose -eq 1 ]; then
    echo "##### Setup for sbatch scriptc for workflow"
    echo "Account: " $account
    echo "Nproc: " $nproc
    echo "Narray: " $narray
fi


templates=("converter/convert_to_asdf.sh.template"
           "proc/run_preprocessing.sh.template"
           "windows/select_windows.sh.template"
           "measure/run_measureadj.sh.template"
           "stations/extract_stations.sh.template"
           "filter/filter_windows.sh.template"
           "adjoint/run_pyadj_mt.sh.template"
           "weights/calc_weights.sh.template"
           "sum_adjoint/sum_adjoint.sh.template")

for template in "${templates[@]}"
do
	target=`echo $template | sed -e s/\.template//g`
	cp $template $target
	sed -i "s/:nproc:/$nproc/g" $target
	if [ -z $account ]; then
		sed -i "/:account:/d" $target
	else
		sed -i "s/:account:/$account/g" $target
	fi

	if [ -z $account ]; then
		sed -i "/:array:/d" $target
	else
		sed -i "s/:array:/$narray/g" $target
	fi
	echo "$target is written."
done

