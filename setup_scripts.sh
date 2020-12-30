#!/bin/bash

echo "Setup Environment"
read -p "Number of processors per node: " nproc
if [[ -z $nproc ]]; then
	echo "Number of processors cannot be empty."
	exit
fi
read -p "Account name: " account

root=`pwd`
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
	if [[ -z $account ]]; then
		sed -i "/:account:/d" $target
	else
		sed -i "s/:account:/$account/g" $target
	fi
	echo "$target is written."
done

