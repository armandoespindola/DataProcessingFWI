#!/bin/bash

trap ' check_status 1 $(basename $0) ' ERR


function create_sbatch(){
    local file=$1

    target=`echo $file | sed -e s/\.sh.template//g`
    cp -v $file ${target}.sh



    ###### FRONTERA
    line=$(grep \\-\\-output ${target}.sh)
    sed -i "s/$line/${line}\n$SBATCH_OPTIONAL/g" ${target}.sh
    sed -i "s/mpirun.*-np/$MPIEXEC/g" ${target}.sh
    ######
    
    sed -i "s/_:job_id://g" ${target}.sh
    
    if [ -z $ACCOUNT ]; then sed -i "/:account:/d" ${target}.sh
    else
	sed -i "s/:account:/$ACCOUNT/g" ${target}.sh
    fi

    if [ -z $PARTITION ]; then sed -i "/.*partition.*/d" ${target}.sh
    else
	sed -i "s/:partition:/$PARTITION/g" ${target}.sh
    fi


    if [ -z $NODE ]; then sed -i "/.*nodes.*/d" ${target}.sh
    else
	sed -i "s/:nodes:/$NODE/g" ${target}.sh
    fi

    if [ -z $NTASK ]; then sed -i "/.*tasks.*/d" ${target}.sh
    else
	sed -i "s/:nproc:/$NTASK/g" ${target}.sh
    fi

    if [ -z $NARRAY ]; then sed -i "/.*array.*/d" ${target}.sh
    else
	sed -i "s/:array:/$NARRAY/g" ${target}.sh
    fi

    if [ -z $TIME ]; then sed -i "/.*time.*/d" ${target}.sh
    else
	sed -i "s/:time:/$TIME/g" ${target}.sh
    fi

    sed -i "/.*gres.*/d" ${target}.sh
    
    echo "$target.sh is written."
     
}


if [ $# -lt 2 ]; then
    echo "This program sets up sbatch scripts for workflow"
    echo "usage: ./setup_scripts.sh ACCOUNT NTASK NARRAY PARTITION NODES TIME MPIEXEC verbose[false==0/true==1]"; exit 1;
fi

ACCOUNT=$1
NTASK=$2
NARRAY=$3
PARTITION=$4
NODES=$5
TIME=$6
MPIEXEC=$7
verbose=$8


if [ $verbose -eq 1 ]; then
    echo "##### Setup for sbatch scriptc for workflow"
    echo "Account: " $ACCOUNT
    echo "Nproc: " $NTASK
    echo "Narray: " $NARRAY
    echo "PARTITION: " $PARTITION
    echo "NODES: " $NODES
    echo "TIME: " $TIME
    echo "MPIEXEC: " $MPIEXEC
fi

misfit=$(grep ^misfit settings.yml | cut -d: -f2 | xargs)
misfit_prefix=${misfit/'misfit_'/}
echo "#########"
echo "misfit: "$misfit
echo "#########"

templates=("converter/convert_to_asdf.sh.template"
           "proc/run_preprocessing.sh.template"
	   "proc/run_preprocessing_cmt.sh.template"
           "windows/select_windows.sh.template"
           "measure/run_measureadj_${misfit_prefix}.sh.template"
           "stations/extract_stations.sh.template"
           "filter/filter_windows.sh.template"
	   "adjoint/run_pyadj_${misfit_prefix}.sh.template"
           "weights/calc_weights_${misfit_prefix}.sh.template"
           "sum_adjoint/sum_adjoint.sh.template")


for template in "${templates[@]}"
do
    create_sbatch $template
done
